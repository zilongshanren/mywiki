"""HTML → clean markdown via trafilatura, plus outbound-link extraction."""
from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from datetime import date
from urllib.parse import urljoin, urlparse

import trafilatura
from lxml import html as lxml_html

log = logging.getLogger(__name__)

_IMG_RE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)")
_WAYBACK_RE = re.compile(r"^https?://web\.archive\.org/web/\d+/(https?://.+)$")

_HEADING_TAGS = frozenset(("h1", "h2", "h3", "h4", "h5", "h6"))

# Hosts we never want to fan out into, even from an aggregator's main content.
_JUNK_HOSTS = {
    "fonts.googleapis.com",
    "fonts.gstatic.com",
    "cdn.jsdelivr.net",
    "cdnjs.cloudflare.com",
    "unpkg.com",
    "www.google-analytics.com",
    "www.googletagmanager.com",
    "twitter.com",
    "x.com",
    "www.patreon.com",
    "patreon.com",
    "github.com",   # repos are fine to reference but rarely articles
}


@dataclass
class Article:
    url: str
    title: str
    markdown: str
    author: str | None = None
    published: date | None = None
    image_urls: list[str] = field(default_factory=list)
    outbound_links: list[str] = field(default_factory=list)


def _parse_date(raw: str | None) -> date | None:
    if not raw:
        return None
    try:
        return date.fromisoformat(raw[:10])
    except ValueError:
        return None


def _is_in_heading(elem) -> bool:
    """True if ``elem`` has any <h1>..<h6> ancestor within 5 levels."""
    parent = elem
    for _ in range(5):
        parent = parent.getparent()
        if parent is None:
            return False
        if isinstance(parent.tag, str) and parent.tag in _HEADING_TAGS:
            return True
    return False


def extract_outbound_links(html: str, base_url: str) -> list[str]:
    """Return absolute, deduplicated heading-anchor links from the main area.

    Used for aggregator-style posts (link roundups): we only collect <a> tags
    that sit inside an <h1>..<h6>. That structural signal cleanly separates
    article-title links (always headings in link-roundup newsletters) from
    author credits, inline citations and icon links. Links pointing back to
    the current host or to a known junk host are dropped; (original,
    web.archive.org mirror) pairs are collapsed to the original.
    """
    try:
        doc = lxml_html.fromstring(html)
    except Exception as e:  # noqa: BLE001
        log.warning("outbound: parse failed for %s: %s", base_url, e)
        return []

    main = doc.find(".//article")
    if main is None:
        main = doc.find(".//main")
    if main is None:
        main = doc

    self_host = urlparse(base_url).netloc
    seen: set[str] = set()
    ordered: list[str] = []

    for a in main.iter("a"):
        href = (a.get("href") or "").strip()
        if not href or href.startswith("#") or href.startswith("mailto:"):
            continue
        if not _is_in_heading(a):
            continue
        if not (a.text_content() or "").strip():
            continue

        full = urljoin(base_url, href)
        parsed = urlparse(full)
        if parsed.scheme not in ("http", "https"):
            continue
        if parsed.netloc == self_host:
            continue
        if parsed.netloc in _JUNK_HOSTS:
            continue
        canonical = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        if canonical in seen:
            continue
        seen.add(canonical)
        ordered.append(full.split("#")[0])

    return _dedupe_wayback_pairs(ordered)


def _dedupe_wayback_pairs(links: list[str]) -> list[str]:
    """Drop a web.archive.org mirror when:

    - its embedded original URL is also present in ``links`` (the classic pair
      case: we prefer the original over the snapshot), or
    - its embedded original URL points to a junk host that would have been
      filtered out upstream (so the mirror is an orphan we also don't want).
    """
    originals_norm: set[str] = set()
    for u in links:
        if not _WAYBACK_RE.match(u):
            originals_norm.add(u.rstrip("/"))

    kept: list[str] = []
    for u in links:
        m = _WAYBACK_RE.match(u)
        if m:
            original = m.group(1)
            if original.rstrip("/") in originals_norm:
                continue
            if urlparse(original).netloc in _JUNK_HOSTS:
                continue
        kept.append(u)
    return kept


def _parse_min_date(raw) -> date | None:
    if not raw:
        return None
    if isinstance(raw, date):
        return raw
    try:
        return date.fromisoformat(str(raw)[:10])
    except ValueError:
        log.warning("invalid min_article_date: %r", raw)
        return None


def extract_article(url: str, html: str, cfg: dict) -> Article | None:
    """Run trafilatura and return a normalised Article, or None on failure."""
    markdown = trafilatura.extract(
        html,
        output_format="markdown",
        include_images=True,
        include_links=True,
        include_tables=True,
        favor_precision=True,
        url=url,
    )
    if not markdown:
        log.info("trafilatura returned empty for %s", url)
        return None

    min_chars = cfg.get("min_content_chars", 200)
    if len(markdown) < min_chars:
        log.info("extracted body too short (%d < %d) for %s", len(markdown), min_chars, url)
        return None

    metadata = trafilatura.extract_metadata(html)
    title = (metadata.title if metadata else None) or url
    author = metadata.author if metadata else None
    published = _parse_date(metadata.date if metadata else None)

    min_date = _parse_min_date(cfg.get("min_article_date"))
    if min_date and published and published < min_date:
        log.info("dropping pre-%s post (%s): %s", min_date, published, url)
        return None

    image_urls = _IMG_RE.findall(markdown)
    outbound_links = extract_outbound_links(html, url)

    return Article(
        url=url,
        title=title.strip(),
        markdown=markdown,
        author=author.strip() if isinstance(author, str) else None,
        published=published,
        image_urls=image_urls,
        outbound_links=outbound_links,
    )
