---
tags: [source, software-design, tooling, minimalism]
date: 2026-04-19
sources: 1
---

# Stop Over-engineering Static Websites（Apoorva Joshi）

[[apoorva-joshi]] 2025 年 10 月的短评 + 实战脚本。主张：静态网站本来只是「把 markdown 编译成 HTML 再扔到 CDN」，但现代 JAMstack 工具链（Astro + Netlify CI VM + git hook + CDN）把它搞成需要五层抽象。他建议直接本机 Pandoc + `wrangler` 一步推到 Cloudflare Pages。

## 摘要

作者列举自己过去用过的各种静态生成器：每一个都在某处失败（SEO 糟糕、RSS 坏、主题不自由、升级破坏构建）。更根本的问题是**构建过程本身的过度设计**：把 markdown 推到 git，触发 Netlify hook，Netlify 起 Linux VM，clone 仓库，装 Astro，npm install，跑 build，推 CDN——「一次写博客要用到五台计算机」。他的替代方案：

1. **本地编译、本地推送**——Cloudflare 的 `wrangler` 可以直接把 `dist/` 发到它的 CDN，根本不需要远端 builder；
2. **HTML + fetch 替代 includes**——运行时 `fetch` 共享 header/footer 片段，像浏览器原生的 `#include`；
3. **Pandoc 替代 SSG**——一个 Python 库调用就能把 markdown 转成 HTML，带模板、数学公式、语法高亮；
4. **一个 Python 脚本完事**——他附了 50 行 `run.py`，提供 serve/deploy 两个子命令与文件监听。

文章的 tone 是「reclaim your independence」——不是反对 JAMstack 而是反对把个人博客当工业生产线。

## 关键要点

- **VM-based CI 是 CDN 厂商的商业模式，不是你的技术需要**——本地构建 + `wrangler` 一样能 push 到 CDN。
- **Markdown → HTML 本质上是 Pandoc 一行**，不需要 React/Vue/Astro 这套前端生态。
- **fetch 片段** 是「运行时 include」，对小站来说几毫秒的代价换来零构建依赖；
- 「vibe-coded」的 50 行 Python 比 10MB 的 node_modules 更容易理解、调试、搬迁。

## 链接到的概念

- [[static-site-antiframework]]
- [[complexity]]

## 原文

- 链接：https://apoorvaj.io/stop-overengineering-static-websites
- 本地：`raw/articles/apoorvaj.io/2025-10-04_stop-over-engineering-static-websites.md`
