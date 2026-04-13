# feedly-ingest

Scrape every historical post from the blogs you track in `blogs.yaml` and land
them in `raw/articles/<blog-host>/YYYY-MM-DD_slug.md` so the wiki pipeline can
digest them.

The Feedly OPML export is only a **seed**: `sync` merges new OPML entries into
`blogs.yaml` without clobbering your edits. `blogs.yaml` is then the
authoritative, editable registry of tracked blogs — add one by appending a row,
pause one by flipping `enabled: false`, or delete one to forget it.

Incremental by default: `state/seen.sqlite` records every URL that's been
ingested, so re-running `run` only fetches posts that are actually new.

## Quick start

```bash
cd tools/feedly-ingest
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 1. Seed blogs.yaml from a Feedly OPML export, filtered to game-dev categories.
python ingest.py sync \
    --opml feedly-opml-2026-04-13.opml \
    --categories "game programming,graphics,unreal engine"

# 2. Inspect what will be walked.
python ingest.py list
python ingest.py list --category "graphics"

# 3. Dry-run: discover URLs only, no fetch.
python ingest.py -v run --dry-run > dry-run.urls

# 4. Full historical scrape (commit to disk).
python ingest.py -v run

# 5. Later, add a new blog: edit blogs.yaml by hand or re-sync a fresh OPML.
python ingest.py sync --opml feedly-opml-2026-05-01.opml
python ingest.py -v run   # only fetches new posts on existing blogs + all posts on new blogs
```

## Subcommands

| Command | Purpose |
|---|---|
| `sync --opml FILE [--categories "a,b,c"]` | Merge OPML blogs into `blogs.yaml`. Idempotent on re-sync; existing entries keep their edits. |
| `run [--blog X] [--tag X] [--category X] [--limit N] [--contains X] [--follow-links] [--dry-run]` | Walk `blogs.yaml`, discover historical URLs, fetch + extract + save. |
| `list [--category X] [--tag X]` | Print tracked blogs, grouped by category. |

`run` filters stack: `--blog` matches the host/title substring, `--tag` matches
a tag in `blogs.yaml`, `--category` matches the Feedly category.

## Discovery strategy

Per blog, article URLs are harvested in this order and unioned:

1. **`sitemap.xml`** (plus `robots.txt` sitemap lines and sitemap indexes) — fastest and cleanest.
2. **On-site archive pages** (`/posts`, `/archive`, `/blog`, ...) — fallback when there is no sitemap.
3. **Wayback Machine CDX API** — optional third fallback, currently stubbed.

RSS feeds are only used for blog *identity* (via OPML). They are never a content
source because they only carry recent posts.

## Layout

```
tools/feedly-ingest/
├── README.md
├── requirements.txt
├── config.yaml             global settings (rate limits, paths, ...)
├── blogs.yaml              tracked-blogs registry (source of truth)
├── ingest.py               CLI entry point (sync | run | list)
├── feedly-opml-*.opml      Feedly exports (gitignored, used as seed)
├── state/
│   ├── seen.sqlite         url → filepath dedupe store
│   └── cache/              raw HTML cache for debugging
└── src/
    ├── opml.py             OPML → [Blog]
    ├── blogs_store.py      blogs.yaml load/save/merge
    ├── discover.py         Blog → [article URL]  (sitemap / archive / wayback)
    ├── fetch.py            rate-limited httpx client with retries
    ├── extract.py          HTML → Article (trafilatura)
    ├── frontmatter.py      Article + Blog → YAML frontmatter
    ├── writer.py           save markdown + download images to raw/assets/
    └── dedupe.py           SeenStore (sqlite)
```
