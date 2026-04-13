"""Build YAML frontmatter for a raw/articles/ markdown file."""
from __future__ import annotations

from datetime import datetime

import yaml

from .extract import Article
from .opml import Blog


def build(article: Article, blog: Blog) -> str:
    data = {
        "title": article.title,
        "url": article.url,
        "author": article.author,
        "published": article.published.isoformat() if article.published else None,
        "source_blog": blog.title,
        "source_site": blog.site_url,
        "category": blog.category,
        "fetched": datetime.utcnow().date().isoformat(),
    }
    # drop keys with None values so the frontmatter stays clean
    data = {k: v for k, v in data.items() if v is not None}
    return "---\n" + yaml.safe_dump(data, allow_unicode=True, sort_keys=False) + "---\n\n"
