"""CLI entry point: feedly-ingest — sync OPML into blogs.yaml, then scrape.

Subcommands:
  sync    Merge a Feedly OPML export into blogs.yaml (never clobbers edits).
  run     Walk blogs.yaml, discover historical URLs, save markdown to raw/articles.
  list    Print the tracked-blogs registry (counts by category, optional filter).

Incremental behaviour:
  - blogs.yaml is the authoritative tracked-blogs list. `sync` adds new entries
    from an OPML file without touching anything that's already there.
  - state/seen.sqlite dedupes URLs across runs, so `run` after a previous run
    only fetches posts that are actually new.
"""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from urllib.parse import urlparse

import yaml

from concurrent.futures import ThreadPoolExecutor, as_completed

from src.blogs_store import TrackedBlog, load_blogs, save_blogs, sync_from_opml
from src.dedupe import SeenStore
from src.discover import discover_all_urls
from src.extract import extract_article
from src.fetch import Fetcher
from src.opml import Blog, parse_opml
from src.writer import save_article


DEFAULT_BLOGS_YAML = "blogs.yaml"
DEFAULT_CONFIG_YAML = "config.yaml"


def _url_path(url: str) -> str:
    return urlparse(url).path or "/"


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Ingest subscribed blogs into raw/articles/",
    )
    p.add_argument("--config", default=DEFAULT_CONFIG_YAML, help="Path to config.yaml")
    p.add_argument(
        "--blogs-yaml",
        default=DEFAULT_BLOGS_YAML,
        help="Path to tracked-blogs registry",
    )
    p.add_argument("--verbose", "-v", action="count", default=0)
    sub = p.add_subparsers(dest="cmd", required=True)

    sp_sync = sub.add_parser("sync", help="Merge OPML into blogs.yaml")
    sp_sync.add_argument("--opml", required=True, help="Path to Feedly OPML export")
    sp_sync.add_argument(
        "--categories",
        help="Comma-separated OPML categories to include (default: all)",
    )

    sp_run = sub.add_parser("run", help="Scrape tracked blogs into raw/articles/")
    sp_run.add_argument(
        "--blog",
        help="Restrict to blogs whose site URL or host contains this substring",
    )
    sp_run.add_argument(
        "--tag",
        help="Restrict to blogs that carry this tag in blogs.yaml",
    )
    sp_run.add_argument(
        "--category",
        help="Restrict to blogs in this category",
    )
    sp_run.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Max NEW articles per blog (0 = no limit)",
    )
    sp_run.add_argument(
        "--contains",
        help="Only process discovered URLs whose URL contains this substring",
    )
    sp_run.add_argument(
        "--follow-links",
        action="store_true",
        help="For aggregator posts, fetch every outbound link as a child article",
    )
    sp_run.add_argument(
        "--dry-run",
        action="store_true",
        help="Discover URLs only; do not fetch or write",
    )
    sp_run.add_argument(
        "--include-disabled",
        action="store_true",
        help="Also walk blogs marked enabled: false",
    )
    sp_run.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Number of blogs to process in parallel (each gets its own Fetcher; "
        "per-domain rate-limit still applies inside a single blog). Default 1.",
    )

    sp_list = sub.add_parser("list", help="Print tracked blogs")
    sp_list.add_argument("--category", help="Only list this category")
    sp_list.add_argument("--tag", help="Only list blogs with this tag")

    return p


def _synth_blog_for_link(link: str, parent: Blog) -> Blog:
    parsed = urlparse(link)
    return Blog(
        title=parsed.netloc,
        site_url=f"{parsed.scheme}://{parsed.netloc}",
        feed_url=None,
        category=f"{parent.title} → linked",
    )


def load_config(path: Path) -> dict:
    cfg = yaml.safe_load(path.read_text()) or {}
    base = path.parent.resolve()
    cfg["output"]["articles_dir"] = str(
        (base / cfg["output"]["articles_dir"]).resolve()
    )
    cfg["output"]["assets_dir"] = str(
        (base / cfg["output"]["assets_dir"]).resolve()
    )
    cfg["state"]["db_path"] = str((base / cfg["state"]["db_path"]).resolve())
    cfg["state"]["cache_dir"] = str((base / cfg["state"]["cache_dir"]).resolve())
    return cfg


def _filter_blogs(
    blogs: list[TrackedBlog],
    *,
    blog_substr: str | None = None,
    tag: str | None = None,
    category: str | None = None,
    include_disabled: bool = False,
) -> list[TrackedBlog]:
    out = []
    for b in blogs:
        if not include_disabled and not b.enabled:
            continue
        if blog_substr and blog_substr not in (b.site_url or "") and blog_substr not in (b.title or ""):
            continue
        if tag and tag not in b.tags:
            continue
        if category and (b.category or "") != category:
            continue
        out.append(b)
    return out


def cmd_sync(args, log: logging.Logger) -> int:
    opml_path = Path(args.opml)
    blogs_path = Path(args.blogs_yaml)

    opml_blogs = parse_opml(opml_path)
    log.info("OPML: %d entries from %s", len(opml_blogs), opml_path)

    categories: set[str] | None = None
    if args.categories:
        categories = {c.strip() for c in args.categories.split(",") if c.strip()}
        log.info("Filtering to categories: %s", sorted(categories))

    existing = load_blogs(blogs_path)
    log.info("blogs.yaml: %d existing entries", len(existing))

    merged, added = sync_from_opml(existing, opml_blogs, categories)
    save_blogs(blogs_path, merged)
    log.info("Wrote %s — total=%d  added=%d", blogs_path, len(merged), added)
    return 0


def cmd_list(args, log: logging.Logger) -> int:
    blogs = load_blogs(Path(args.blogs_yaml))
    blogs = _filter_blogs(
        blogs,
        tag=args.tag,
        category=args.category,
        include_disabled=True,
    )
    if not blogs:
        print("(no blogs)")
        return 0
    from collections import Counter
    cats = Counter((b.category or "(uncategorized)") for b in blogs)
    print(f"Total: {len(blogs)} blogs")
    for cat, n in sorted(cats.items(), key=lambda x: -x[1]):
        print(f"  {n:3d}  {cat}")
    print()
    for b in blogs:
        mark = " " if b.enabled else "x"
        print(f"  [{mark}] {b.category or '-':16s}  {b.title[:40]:40s}  {b.site_url}")
    return 0


def _process_blog(
    index: int,
    total: int,
    tb: TrackedBlog,
    cfg: dict,
    args,
    seen: SeenStore,
    log: logging.Logger,
) -> tuple[int, int]:
    """Handle one blog end-to-end. Returns (new_urls, saved).

    Creates a fresh ``Fetcher`` so workers never contend on the per-domain
    throttler. Catches every per-URL failure inline so one bad post never
    kills the blog run.
    """
    blog = tb.to_blog()
    log.info("=== [%d/%d] %s (%s) ===", index, total, blog.title, blog.site_url)
    fetcher = Fetcher(cfg["fetch"])
    new_urls_count = 0
    saved_count = 0
    try:
        try:
            urls = discover_all_urls(blog, fetcher, cfg["discovery"])
        except Exception as e:  # noqa: BLE001
            log.warning("discovery crashed for %s: %s", blog.site_url, e)
            return (0, 0)

        if tb.path_prefixes:
            prefixes = tuple(tb.path_prefixes)
            before = len(urls)
            urls = [
                u for u in urls
                if any(_url_path(u).startswith(p) for p in prefixes)
            ]
            log.info(
                "  path_prefixes %s → %d (dropped %d)",
                list(prefixes), len(urls), before - len(urls),
            )
        if args.contains:
            urls = [u for u in urls if args.contains in u]
            log.info("  filtered by --contains=%r → %d", args.contains, len(urls))
        new_urls = [u for u in urls if not seen.contains(u)]
        log.info(
            "  discovered=%d  new=%d  (skipped %d already-seen)",
            len(urls), len(new_urls), len(urls) - len(new_urls),
        )
        if args.limit:
            new_urls = new_urls[: args.limit]
        new_urls_count = len(new_urls)

        if args.dry_run:
            for u in new_urls:
                print(u, flush=True)
            return (new_urls_count, 0)

        for url in new_urls:
            try:
                html = fetcher.get_html(url)
            except Exception as e:  # noqa: BLE001
                log.warning("fetch crashed %s: %s", url, e)
                continue
            if not html:
                continue
            try:
                article = extract_article(url, html, cfg["extract"])
            except Exception as e:  # noqa: BLE001
                log.warning("extract crashed %s: %s", url, e)
                continue
            if not article:
                continue
            try:
                path = save_article(article, blog, cfg, fetcher)
            except Exception as e:  # noqa: BLE001
                log.warning("save crashed %s: %s", url, e)
                continue
            seen.add(url, path)
            saved_count += 1
            log.info("  saved %s", path)

            if args.follow_links and article.outbound_links:
                log.info(
                    "  fan-out: %d outbound links from %s",
                    len(article.outbound_links), url,
                )
                for link in article.outbound_links:
                    if seen.contains(link):
                        continue
                    try:
                        child_html = fetcher.get_html(link)
                    except Exception:  # noqa: BLE001
                        continue
                    if not child_html:
                        continue
                    child = extract_article(link, child_html, cfg["extract"])
                    if not child:
                        continue
                    child_blog = _synth_blog_for_link(link, blog)
                    try:
                        child_path = save_article(child, child_blog, cfg, fetcher)
                    except Exception as e:  # noqa: BLE001
                        log.warning("child save crashed %s: %s", link, e)
                        continue
                    seen.add(link, child_path)
                    saved_count += 1
                    log.info("    ↳ saved %s", child_path)
    finally:
        fetcher.close()
    return (new_urls_count, saved_count)


def cmd_run(args, log: logging.Logger) -> int:
    cfg = load_config(Path(args.config))
    tracked = load_blogs(Path(args.blogs_yaml))
    tracked = _filter_blogs(
        tracked,
        blog_substr=args.blog,
        tag=args.tag,
        category=args.category,
        include_disabled=args.include_disabled,
    )
    log.info("Walking %d tracked blog(s) with %d worker(s)", len(tracked), args.workers)
    if not tracked:
        log.warning("No blogs match the filters — nothing to do.")
        return 0

    seen = SeenStore(Path(cfg["state"]["db_path"]))
    total = len(tracked)
    total_saved = 0
    total_new_urls = 0

    try:
        if args.workers <= 1:
            for i, tb in enumerate(tracked, 1):
                nu, sv = _process_blog(i, total, tb, cfg, args, seen, log)
                total_new_urls += nu
                total_saved += sv
        else:
            with ThreadPoolExecutor(max_workers=args.workers) as pool:
                futures = {
                    pool.submit(_process_blog, i, total, tb, cfg, args, seen, log): tb
                    for i, tb in enumerate(tracked, 1)
                }
                for fut in as_completed(futures):
                    tb = futures[fut]
                    try:
                        nu, sv = fut.result()
                    except Exception as e:  # noqa: BLE001
                        log.warning("worker crashed for %s: %s", tb.site_url, e)
                        continue
                    total_new_urls += nu
                    total_saved += sv
    finally:
        seen.close()

    log.info("Run complete. new_urls=%d  saved=%d", total_new_urls, total_saved)
    return 0


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    logging.basicConfig(
        level=[logging.WARNING, logging.INFO, logging.DEBUG][min(args.verbose, 2)],
        format="%(asctime)s %(levelname)-7s %(name)s %(message)s",
    )
    log = logging.getLogger("ingest")

    if args.cmd == "sync":
        return cmd_sync(args, log)
    if args.cmd == "list":
        return cmd_list(args, log)
    if args.cmd == "run":
        return cmd_run(args, log)
    raise SystemExit(f"unknown command: {args.cmd}")


if __name__ == "__main__":
    sys.exit(main())
