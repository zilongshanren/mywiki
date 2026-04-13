"""Discover historical article URLs for a blog: sitemap -> archive -> wayback."""
from __future__ import annotations

import logging
import re
from typing import Iterable, TYPE_CHECKING
from urllib.parse import urljoin, urlparse

from lxml import etree, html as lxml_html

from .opml import Blog

if TYPE_CHECKING:
    from .fetch import Fetcher

log = logging.getLogger(__name__)

# Candidate archive page paths, probed in order.
_ARCHIVE_PROBES = ("/posts", "/archive", "/archives", "/blog", "/articles")

# Candidate sitemap filenames at the site root.
_SITEMAP_CANDIDATES = ("sitemap.xml", "sitemap_index.xml", "sitemap-0.xml")

_SITEMAP_NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}

# Sitemap filenames that never contain real article pages (WordPress, Hugo, ...).
# We skip walking these entirely — both to save requests and to avoid polluting
# the URL set with tag/category/author/attachment pages that are not articles.
# The keyword may be preceded by `/`, `_`, or `-` — e.g. both `/tag-sitemap.xml`
# and `/post_tag-sitemap.xml` should be skipped.
_SITEMAP_SKIP_PATTERNS = re.compile(
    r"(?:[/_-])(?:"
    r"tag|tags|category|categories|author|authors|attachment|attachments|"
    r"wp-content|wp-json|image|images|media|comment|comments|taxonomy|"
    r"term|terms|user|users|product|products|shop|page|pages"
    r")-sitemap",
    re.IGNORECASE,
)

# URL paths that look like listings/archives rather than actual articles.
# Anything matching is dropped from the final URL set.
_NON_ARTICLE_PATH = re.compile(
    r"(?:^|/)(?:"
    r"tag|tags|category|categories|author|authors|page|pages|feed|feeds|"
    r"rss|atom|comments|search|archive|archives|wp-content|wp-json|"
    r"wp-login|wp-admin|wp-includes|comment-page|amp|trackback|embed|"
    r"attachment_id"
    r")(?:/|$|\?|\.)",
    re.IGNORECASE,
)

# Locale path prefixes we drop so multilingual blogs (e.g. Unity) don't duplicate
# every post 8× — one per language. We keep the default (English / no prefix).
_LOCALE_PREFIX = re.compile(
    r"^/(?:"
    r"cn|de|es|fr|ja|pt|ru|kr|ko|zh|zh-cn|zh-tw|zh-hk|en|en-us|en-gb|"
    r"jp|br|it|nl|pl|tr|vi|id|th|ar|he|hi|fa|ua|cz|sv|fi|da|no|el|ro|hu"
    r")(?:/|$)",
    re.IGNORECASE,
)

# Year-in-path filter: most date-slug blog URLs embed the year as /YYYY/...
# or as a suffix like `sitemap-2009.xml`. If the path has a year < MIN_YEAR,
# drop it. Paths without a year are kept and filtered later by the
# published-date check in extract.
_URL_YEAR = re.compile(r"(?:^|[/_-])(19\d{2}|20\d{2})(?:[/_\-.]|$)")
MIN_YEAR = 2010

# Trailing file extensions we never want to ingest as articles.
_NON_ARTICLE_EXT = re.compile(
    r"\.(?:jpg|jpeg|png|gif|webp|svg|avif|ico|bmp|tiff|"
    r"css|js|mjs|map|json|xml|rss|atom|woff2?|ttf|eot|otf|"
    r"mp4|mp3|wav|ogg|pdf|zip|tar|gz|bz2|7z|rar)$",
    re.IGNORECASE,
)


def _is_article_url(url: str) -> bool:
    """Conservative heuristic for whether a URL is plausibly a post.

    We reject:
      * listing pages (tag/category/author/feed/archive/pagination)
      * binary asset URLs (images, fonts, media, archives)
      * WordPress admin/includes paths
      * locale-prefixed duplicates (/cn/, /de/, ...)
      * malformed URLs (e.g. concatenated `unity.comhttps://docs...`)
      * site-root URLs (`https://example.com/` with no path)
    """
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return False
    # Guard against concatenation bugs in upstream sitemaps ("example.comhttps").
    if "http" in parsed.netloc or not parsed.netloc or parsed.netloc.count(".") == 0:
        return False
    path = parsed.path or "/"
    if path in ("", "/"):
        return False
    if _NON_ARTICLE_EXT.search(path):
        return False
    if _NON_ARTICLE_PATH.search(path):
        return False
    if _LOCALE_PREFIX.match(path):
        return False
    m = _URL_YEAR.search(path)
    if m and int(m.group(1)) < MIN_YEAR:
        return False
    return True


def discover_all_urls(blog: Blog, fetcher: "Fetcher", cfg: dict) -> list[str]:
    """Return a deduplicated, sorted list of article URLs for the blog.

    Strategy order (short-circuits as soon as a strategy yields enough URLs):
      1. sitemap.xml (and sitemap index files) — authoritative when present.
      2. on-site archive pages — fallback when sitemap is missing or thin.
      3. Wayback Machine CDX API — final fallback for deleted/migrated posts.
    """
    urls: set[str] = set()
    # Threshold above which we trust the current strategy and skip the rest.
    # Five is low enough to catch blogs with only a handful of posts, but high
    # enough to tolerate a stub sitemap (e.g. a single homepage entry).
    enough = int(cfg.get("short_circuit_threshold", 5))

    if cfg.get("try_sitemap", True):
        before = len(urls)
        urls.update(from_sitemap(blog.site_url, fetcher))
        log.info("  sitemap  → +%d", len(urls) - before)

    article_count = sum(1 for u in urls if _is_article_url(u))

    if article_count < enough and cfg.get("try_archive", True):
        before = len(urls)
        urls.update(from_archive(blog.site_url, fetcher))
        log.info("  archive  → +%d", len(urls) - before)
        article_count = sum(1 for u in urls if _is_article_url(u))

    if article_count < enough and cfg.get("try_wayback", True):
        before = len(urls)
        urls.update(
            from_wayback(
                blog.site_url,
                fetcher,
                cfg.get("wayback_cdx_url", "http://web.archive.org/cdx/search/cdx"),
            )
        )
        log.info("  wayback  → +%d", len(urls) - before)

    before = len(urls)
    urls = {u for u in urls if _is_article_url(u)}
    dropped = before - len(urls)
    if dropped:
        log.info("  filtered → -%d non-article URLs (kept %d)", dropped, len(urls))

    return sorted(urls)


def from_sitemap(site_url: str, fetcher: "Fetcher") -> Iterable[str]:
    """Walk sitemap.xml and any nested sitemap indexes.

    Probes are rooted at ``scheme://host/`` (NOT at ``site_url``) so blogs
    whose Feedly ``htmlUrl`` points at a subpath — e.g.
    ``https://chickensoft.games/blog`` or ``https://www.gamasutra.com/blogs/expert/``
    — still find the site-level sitemap. ``robots.txt`` ``Sitemap:`` lines are
    also honoured.
    """
    parsed = urlparse(site_url)
    root = f"{parsed.scheme}://{parsed.netloc}/"
    candidates: list[str] = [urljoin(root, name) for name in _SITEMAP_CANDIDATES]

    robots = fetcher.get_html(urljoin(root, "robots.txt"))
    if robots:
        for line in robots.splitlines():
            if line.lower().startswith("sitemap:"):
                candidates.append(line.split(":", 1)[1].strip())

    urls: set[str] = set()
    visited: set[str] = set()
    for sm in candidates:
        if sm in visited:
            continue
        urls.update(_walk_sitemap(sm, fetcher, visited, depth=0))
    return sorted(urls)


def _walk_sitemap(
    sm_url: str, fetcher: "Fetcher", visited: set[str], depth: int
) -> list[str]:
    if depth > 5 or sm_url in visited:
        return []
    visited.add(sm_url)

    # Skip tag/category/attachment sitemap shards — they never contain posts,
    # and WordPress sites often expose 5-10 of them.
    if _SITEMAP_SKIP_PATTERNS.search(sm_url):
        log.debug("sitemap skip (non-article): %s", sm_url)
        return []

    # Year-in-sitemap-name filter: sites like gamasutra/gamedeveloper.com
    # expose one sitemap shard per month going back to the 90s. Skip any
    # shard whose path contains a pre-MIN_YEAR year — this prunes hundreds of
    # slow requests on archived blogs.
    m = _URL_YEAR.search(urlparse(sm_url).path)
    if m and int(m.group(1)) < MIN_YEAR:
        log.debug("sitemap skip (pre-%d): %s", MIN_YEAR, sm_url)
        return []

    xml_text = fetcher.get_html(sm_url)
    if not xml_text:
        return []
    try:
        root = etree.fromstring(xml_text.encode("utf-8"))
    except etree.XMLSyntaxError as e:
        log.warning("sitemap parse failed %s: %s", sm_url, e)
        return []

    tag = etree.QName(root.tag).localname  # strip namespace

    if tag == "sitemapindex":
        out: list[str] = []
        for loc in root.findall(".//sm:sitemap/sm:loc", _SITEMAP_NS) or root.findall(
            ".//sitemap/loc"
        ):
            if loc.text:
                out.extend(
                    _walk_sitemap(loc.text.strip(), fetcher, visited, depth + 1)
                )
        return out

    if tag == "urlset":
        locs = root.findall(".//sm:url/sm:loc", _SITEMAP_NS) or root.findall(
            ".//url/loc"
        )
        return [loc.text.strip() for loc in locs if loc.text]

    log.info("sitemap %s: unknown root <%s>", sm_url, tag)
    return []


def from_archive(site_url: str, fetcher: "Fetcher") -> Iterable[str]:
    """Probe common archive paths and collect sibling article links.

    Heuristic:
      1. Try each probe path (/posts, /archive, ...)
      2. On 200, parse the HTML and collect every <a href> whose absolute URL
         sits under the same path prefix (e.g. /posts/<slug>) on the same host
      3. Filter out the archive root itself and any fragment/query cruft
      4. Return the first probe that yields >0 links (fast exit)

    After the named probes fail, we also try the **site root** (empty probe).
    At the root we can't restrict by a path prefix, so we rely on
    ``_is_article_url`` to throw away navigation/tag/category links. This is
    how we recover sites like ``nullprogram.com`` that list every post on
    their home page without exposing any sitemap at all.
    """
    parsed_site = urlparse(site_url)
    base_host = parsed_site.netloc

    # Use the real site host root for the empty probe, since site_url may point
    # at a subpath (e.g. .../blog).
    site_root = f"{parsed_site.scheme}://{parsed_site.netloc}"

    for probe in _ARCHIVE_PROBES:
        probe_url = site_url.rstrip("/") + probe
        found = _scrape_archive_page(probe_url, fetcher, base_host, probe)
        if found:
            log.info("archive probe hit: %s → %d links", probe_url, len(found))
            return found

    # Final fallback: the homepage. No prefix restriction — rely on
    # _is_article_url (applied downstream) to drop garbage.
    found = _scrape_archive_page(site_root + "/", fetcher, base_host, "")
    if found:
        log.info("archive root-fallback hit: %s → %d links", site_root, len(found))
        return found

    return []


def _scrape_archive_page(
    page_url: str, fetcher: "Fetcher", base_host: str, probe: str
) -> list[str]:
    html_text = fetcher.get_html(page_url)
    if not html_text:
        return []
    try:
        doc = lxml_html.fromstring(html_text)
    except Exception as e:  # noqa: BLE001
        log.warning("archive parse failed %s: %s", page_url, e)
        return []

    probe_path = probe.rstrip("/") if probe else ""
    results: set[str] = set()
    for a in doc.iter("a"):
        href = a.get("href")
        if not href:
            continue
        full = urljoin(page_url, href)
        parsed = urlparse(full)
        if parsed.netloc != base_host:
            continue
        if probe_path and not parsed.path.startswith(probe_path + "/"):
            continue
        clean = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        results.add(clean)
    return sorted(results)


def from_wayback(site_url: str, fetcher: "Fetcher", cdx_url: str) -> Iterable[str]:
    """Query the Wayback Machine CDX API for every snapshot under the domain.

    TODO:
      1. Build query: ?url=<domain>/*&output=json&fl=original,timestamp,statuscode,mimetype
         &filter=statuscode:200&filter=mimetype:text/html&collapse=urlkey
      2. GET, parse JSON (first row is the header)
      3. Yield each unique `original` URL
    """
    return []
