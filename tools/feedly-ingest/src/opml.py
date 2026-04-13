"""Parse Feedly OPML export into a list of Blog records."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from lxml import etree


@dataclass
class Blog:
    title: str
    site_url: str
    feed_url: str | None   # RSS URL, used only for blog identity, never for content
    category: str | None   # Feedly category (parent <outline> text)


def parse_opml(path: Path) -> list[Blog]:
    """Parse a Feedly-style OPML file into Blog records.

    Feedly OPML layout:
        <opml><body>
          <outline text="Category1">
            <outline type="rss" text="Blog" xmlUrl="...rss" htmlUrl="...site"/>
          </outline>
        </body></opml>
    """
    tree = etree.parse(str(path))
    blogs: list[Blog] = []
    for outline in tree.iterfind(".//outline[@type='rss']"):
        parent = outline.getparent()
        category = parent.get("text") if parent is not None and parent.tag == "outline" else None
        blogs.append(
            Blog(
                title=outline.get("text") or outline.get("title") or "",
                site_url=outline.get("htmlUrl") or "",
                feed_url=outline.get("xmlUrl"),
                category=category,
            )
        )
    return blogs
