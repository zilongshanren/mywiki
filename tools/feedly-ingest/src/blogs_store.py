"""Tracked-blogs registry persisted as YAML.

`blogs.yaml` is the authoritative list of blogs the ingester walks. The OPML
export is a *seed*: `sync_from_opml()` merges new entries in without clobbering
existing ones, so manual edits (enabling/disabling, retitling, adding tags)
survive every re-sync.

Identity is the normalised site host (lower-cased, `www.` stripped). That makes
re-syncs idempotent even if Feedly renames a blog or re-orders outlines.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse

import yaml

from .opml import Blog


@dataclass
class TrackedBlog:
    title: str
    site_url: str
    feed_url: str | None = None
    category: str | None = None
    tags: list[str] = field(default_factory=list)
    enabled: bool = True
    # Optional: only keep discovered URLs whose path starts with one of these
    # prefixes. Use this to tame noisy sitemaps (e.g. Unity's site-wide
    # sitemap covers products, careers, legal, ...).
    path_prefixes: list[str] = field(default_factory=list)
    # Free-form notes the user can add; the ingester never reads them.
    notes: str | None = None

    def to_blog(self) -> Blog:
        """Adapter back to the fetch/extract pipeline's Blog record."""
        return Blog(
            title=self.title,
            site_url=self.site_url,
            feed_url=self.feed_url,
            category=self.category,
        )

    def to_dict(self) -> dict:
        d: dict = {
            "title": self.title,
            "site_url": self.site_url,
        }
        if self.feed_url:
            d["feed_url"] = self.feed_url
        if self.category:
            d["category"] = self.category
        if self.tags:
            d["tags"] = list(self.tags)
        if self.path_prefixes:
            d["path_prefixes"] = list(self.path_prefixes)
        if not self.enabled:
            d["enabled"] = False
        if self.notes:
            d["notes"] = self.notes
        return d


def _host_key(site_url: str) -> str:
    """Identity key for a tracked blog.

    We use host + normalised path so two blogs that share a hostname but live
    under different paths (e.g. ``cnblogs.com/miloyip`` and
    ``cnblogs.com/clayman``) are treated as distinct, while repeats of the same
    site with differing Feedly display titles still collapse.
    """
    parsed = urlparse(site_url or "")
    host = parsed.netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    path = (parsed.path or "").rstrip("/")
    return host + path


def load_blogs(path: Path) -> list[TrackedBlog]:
    if not path.exists():
        return []
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    raw = data.get("blogs") or []
    out: list[TrackedBlog] = []
    for item in raw:
        if not isinstance(item, dict) or not item.get("site_url"):
            continue
        out.append(
            TrackedBlog(
                title=item.get("title") or "",
                site_url=item["site_url"],
                feed_url=item.get("feed_url"),
                category=item.get("category"),
                tags=list(item.get("tags") or []),
                path_prefixes=list(item.get("path_prefixes") or []),
                enabled=bool(item.get("enabled", True)),
                notes=item.get("notes"),
            )
        )
    return out


def save_blogs(path: Path, blogs: Iterable[TrackedBlog]) -> None:
    items = sorted(blogs, key=lambda b: (b.category or "~", _host_key(b.site_url)))
    payload = {"blogs": [b.to_dict() for b in items]}
    path.write_text(
        "# Tracked blogs — authoritative list for `ingest.py run`.\n"
        "# Edit freely: new entries are picked up on next run, `enabled: false`\n"
        "# pauses a blog without losing its metadata, and `sync` merges new\n"
        "# OPML entries without touching your edits.\n"
        + yaml.safe_dump(payload, allow_unicode=True, sort_keys=False, width=120),
        encoding="utf-8",
    )


def sync_from_opml(
    existing: list[TrackedBlog],
    opml_blogs: list[Blog],
    categories: set[str] | None = None,
) -> tuple[list[TrackedBlog], int]:
    """Merge OPML blogs into ``existing``. Returns (merged, added_count).

    Rules:
    - Skip OPML rows that are not in the requested categories (if given).
    - Match existing entries by normalised host; existing metadata wins.
    - Fill in missing ``feed_url``/``category`` on existing entries from the OPML.
    - New entries are appended with ``enabled=True``.
    """
    by_host = {_host_key(b.site_url): b for b in existing if b.site_url}
    added = 0
    for opml_b in opml_blogs:
        if not opml_b.site_url:
            continue
        if categories and (opml_b.category or "") not in categories:
            continue
        host = _host_key(opml_b.site_url)
        if not host:
            continue
        if host in by_host:
            existing_b = by_host[host]
            if not existing_b.feed_url and opml_b.feed_url:
                existing_b.feed_url = opml_b.feed_url
            if not existing_b.category and opml_b.category:
                existing_b.category = opml_b.category
            continue
        by_host[host] = TrackedBlog(
            title=opml_b.title,
            site_url=opml_b.site_url,
            feed_url=opml_b.feed_url,
            category=opml_b.category,
        )
        added += 1
    return list(by_host.values()), added
