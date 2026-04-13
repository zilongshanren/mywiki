"""Persist Article -> raw/articles/<blog>/YYYY-MM-DD_slug.md, download images to raw/assets/."""
from __future__ import annotations

import hashlib
import logging
import os
import re
from datetime import date
from pathlib import Path
from urllib.parse import urljoin, urlparse

from slugify import slugify

from .extract import Article
from .frontmatter import build as build_frontmatter
from .opml import Blog

log = logging.getLogger(__name__)

_IMG_RE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


def _blog_slug(blog: Blog) -> str:
    """Directory-safe slug for a blog — its hostname, www-stripped."""
    host = urlparse(blog.site_url or "").netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    if host:
        return host
    return slugify(blog.title) or "unknown-blog"


def save_article(article: Article, blog: Blog, cfg: dict, fetcher) -> Path:
    articles_dir = Path(cfg["output"]["articles_dir"])
    assets_dir = Path(cfg["output"]["assets_dir"])

    # Each blog gets its own subdirectory under raw/articles/.
    target_dir = articles_dir / _blog_slug(blog)
    target_dir.mkdir(parents=True, exist_ok=True)
    assets_dir.mkdir(parents=True, exist_ok=True)

    # Relative link from the article file → assets dir, used when rewriting
    # image markdown. With the blog-folder layout this is "../../assets".
    rel_assets = os.path.relpath(assets_dir, target_dir).replace(os.sep, "/")

    body = article.markdown
    if cfg["extract"].get("download_images", True):
        body = _download_images(body, article.url, assets_dir, rel_assets, fetcher)

    d = article.published or date.today()
    slug = slugify(article.title or "untitled", max_length=60) or "untitled"
    path = target_dir / f"{d.isoformat()}_{slug}.md"

    # conflict: append -2, -3, ... until we find an unused name
    n = 2
    while path.exists():
        path = target_dir / f"{d.isoformat()}_{slug}-{n}.md"
        n += 1

    path.write_text(build_frontmatter(article, blog) + body, encoding="utf-8")
    return path


def _download_images(
    markdown: str,
    article_url: str,
    assets_dir: Path,
    rel_assets: str,
    fetcher,
) -> str:
    """Replace every ![](remote) with a local path after downloading.

    Relative image URLs are resolved against ``article_url`` so Hugo/Jekyll
    blogs that emit paths like ``/img/foo.png`` still work. The rewritten
    markdown uses ``rel_assets`` as the path prefix so subdirectory-nested
    articles can still point at ``raw/assets/``.
    """
    def repl(match: re.Match) -> str:
        alt, raw_url = match.group(1), match.group(2)
        if raw_url.startswith("data:"):
            return match.group(0)
        full_url = urljoin(article_url, raw_url)
        if not full_url.startswith(("http://", "https://")):
            return match.group(0)
        try:
            data = fetcher.get_bytes(full_url)
            if not data:
                return match.group(0)
            ext = _guess_ext(full_url)
            name = hashlib.sha1(full_url.encode()).hexdigest()[:16] + ext
            (assets_dir / name).write_bytes(data)
            return f"![{alt}]({rel_assets}/{name})"
        except Exception as e:  # noqa: BLE001 — best-effort per-image
            log.warning("image download failed %s: %s", full_url, e)
            return match.group(0)

    return _IMG_RE.sub(repl, markdown)


def _guess_ext(url: str) -> str:
    path = urlparse(url).path.lower()
    for ext in (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".avif"):
        if path.endswith(ext):
            return ext
    return ".img"
