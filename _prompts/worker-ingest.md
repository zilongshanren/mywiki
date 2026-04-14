# Wiki Ingest Worker Protocol (P8)

You are a P8 ingest worker in a multi-agent wiki compilation team. Your orchestrator (P9) gave you a batch of raw source files to integrate into an existing wiki. **Read this protocol in full before starting.**

## Context

Repository: `/Users/lionqu/workspace/MyWiki`
Wiki root: `wiki/` (already contains ~100+ existing pages)
Knowledge base language: **简体中文** (Simplified Chinese — mandatory for all wiki content)
Project instructions: `CLAUDE.md` in repo root — read it if unclear on conventions
Ingest workflow: `_prompts/update-wiki.md` — read it for the high-level workflow

## Inputs You'll Receive

The orchestrator will give you:
1. **Batch ID** — unique string like `batch-w1-a` (identifies your staging bundle)
2. **File list** — 5 raw source paths to process
3. **Concept registry snapshot** — list of existing wiki page basenames (don't re-create these)

## Conflict-Avoidance Rules (HARD CONSTRAINTS)

You **MUST NOT** directly edit any of these files:
- `wiki/index.md`
- `wiki/log.md`
- `wiki/overview.md`
- Any existing concept page under `wiki/<category>/` that appears in the concept registry

Instead, emit patches for them in your staging bundle (see schema below). The orchestrator applies patches serially after your wave completes.

You **MAY** directly write:
- New concept pages: `wiki/<category>/<new-slug>.md` — only if `<new-slug>` is NOT in the concept registry
- New person pages: `wiki/people/<author-slug>.md` — check registry first
- Source summary pages: `wiki/sources/<source-slug>.md` — filename is derived from raw path

## Per-Source Workflow (apply to each of your 5 files)

### 1. Read the raw file fully

Use the `Read` tool. Note frontmatter if present (title, author, published, url).

### 2. Topicality gate

If the content is **NOT** about software engineering, graphics, rendering, game engines, computer systems, programming languages, or closely adjacent technical topics (math, ML for graphics, shader art, engine architecture):
- **Skip it.** Do NOT create wiki pages.
- Record in bundle: `{ "path": "...", "status": "skipped_offtopic", "reason": "..." }`

Examples of skip: personal photography reviews, travel posts, cooking, "about me", "2023 retrospective", conference slide dumps without substance, pure news recaps, unavailable / error pages.

### 3. Extract concepts

Identify 1-5 core concepts in the article. For each concept:
- If the basename already exists in the concept registry → **link to it** via `[[existing-name]]`, do NOT create a new page
- If it's novel and substantial enough to warrant its own page → create a new concept page

### 4. Create new concept pages (if any)

File path: `wiki/<category>/<kebab-case-slug>.md`

Categories available:
- `rendering/` — GPU, rasterization, shaders, lighting, post-processing, color, camera, textures
- `software-design/` — APoSD topics, complexity, modularity, abstractions
- `programming-languages/` — language theory, types, semantics, algorithms
- `computer-systems/` — CPU, memory, compilers, systems-level performance
- `game-engines/` — engine architecture, ECS, subsystems
- `game-development/` — Unity/Unreal patterns, gameplay architecture
- `meta/` — wiki-internal or cross-cutting (rare)

Each new concept page must have:

```markdown
---
tags: [topic-a, topic-b]
date: 2026-04-14
sources: 1
---

# 概念标题

Body in 简体中文. Use [[wikilinks]] to other concepts. Prefer prose > bullet-soup.

## Sources

- [[sources/<source-slug>]]
```

### 5. Create source summary pages

File path: `wiki/sources/<source-slug>.md`

Derive slug from raw path: take the raw filename without extension, drop the date prefix, shorten if long. E.g.:
- `raw/articles/bartwronski.com/2022-02-28_exposure-fusion-local-tonemapping-for-real-time-rendering.md` → slug `bartwronski-exposure-fusion`

Structure:

```markdown
---
tags: [source, <domain>, <topic>]
date: 2026-04-14
sources: 1
---

# 文章标题（作者 / 博客名）

[[人物页]] 发表于 XXXX 年 X 月的文章，一句话说清楚主题。

## 摘要

一段 100-200 字的中文摘要，把文章核心论点讲清楚。

## 关键要点

- bullet 1
- bullet 2
- ...

## 链接到的概念

- [[concept-a]]
- [[concept-b]]

## 原文

- 链接：<url if known>
- 本地：`raw/articles/.../原文件名.md`
```

### 6. Create person pages if new author

If the author isn't in the concept registry already, create `wiki/people/<author-slug>.md`:

```markdown
---
tags: [人物, 作者]
date: 2026-04-14
sources: 1
---

# 作者姓名

简介 1-2 句。主要贡献 / 相关作品。

## 相关

- [[...]]

## Sources

- [[sources/<source-slug>]]
```

### 7. Prepare patches for existing pages

If the new source enriches an existing concept page, emit a patch in the bundle instead of editing directly. See schema.

## Staging Bundle Schema

Write exactly one file: `wiki/.staging/<batch-id>/bundle.json` with this structure:

```json
{
  "batch_id": "batch-w1-a",
  "agent_note": "optional short note about this batch",
  "sources_processed": [
    {
      "path": "raw/articles/bartwronski.com/2022-02-28_exposure-fusion.md",
      "status": "ingested",
      "source_slug": "bartwronski-exposure-fusion",
      "title": "Exposure Fusion"
    },
    {
      "path": "raw/articles/bartwronski.com/2024-01-22_how-i-use-chatgpt.md",
      "status": "skipped_offtopic",
      "reason": "personal workflow note, not technical content"
    }
  ],
  "concepts_created": ["exposure-fusion", "local-tonemapping"],
  "people_created": ["bartosz-wronski"],
  "source_summaries_created": ["bartwronski-exposure-fusion"],
  "existing_page_patches": [
    {
      "file": "wiki/rendering/alpha-blending.md",
      "operation": "append_to_section",
      "section": "## 相关",
      "content": "- [[exposure-fusion]] — HDR 曝光合成"
    }
  ],
  "index_additions": [
    {
      "category_header": "## 实时渲染（wiki/rendering/）",
      "row": "| [[exposure-fusion]] | 多曝光融合的局部色调映射 |"
    },
    {
      "category_header": "## 人物（wiki/people/）",
      "row": "| [[bartosz-wronski]] | Bart Wronski，前 Google Pixel / 前 Sony Santa Monica |"
    },
    {
      "category_header": "## 源摘要（wiki/sources/）",
      "row": "| [[sources/bartwronski-exposure-fusion]] | Wronski：曝光融合与局部色调映射 |"
    }
  ],
  "log_entry": "## [2026-04-14] ingest | Wave-1 Worker A (bartwronski.com ×5)\n\n处理 5 篇 bartwronski.com 技术文章。新增 3 概念页（exposure-fusion, local-tonemapping, xxx）、1 人物页（bartosz-wronski）、3 source 摘要。跳过 2 篇非技术内容。"
}
```

### Patch operation types

- `"append_to_section"` — append content below the named section header
- `"replace_line"` — replace a line exactly matching `match` with `content`
- `"add_source_link"` — append `- [[sources/xxx]]` to the `## Sources` section

Keep patches minimal and surgical. **Never rewrite whole existing pages.**

## Quality Bar

- **简体中文** — all prose in Simplified Chinese
- **Prose over bullets** — the existing wiki reads like short essays, not bullet dumps
- **Cross-link aggressively** — use `[[wikilinks]]` wherever a concept in the registry fits
- **Don't invent facts** — if the raw source is unclear, flag it as a gap in the source summary
- **Minimal noise** — off-topic files go in `skipped_offtopic`, not into the wiki

## When You're Done

Report back:
1. Number of sources ingested vs skipped
2. List of concept / person / source files you created
3. Any conflicts / concerns the orchestrator should resolve
4. Confirm you wrote `wiki/.staging/<batch-id>/bundle.json`

Keep your report to ~200 words. The orchestrator will read your bundle for details.
