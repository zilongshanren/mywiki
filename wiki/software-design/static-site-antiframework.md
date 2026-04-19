---
tags: [minimalism, tooling, complexity, web]
date: 2026-04-19
sources: 1
---

# 静态网站反框架主义

[[apoorva-joshi]] 的 *Stop Over-engineering Static Websites* 是「反框架主义」在个人博客语境下的一份示范文。核心论点：markdown → HTML → CDN 这条链本质上是三步，却被现代 JAMstack（Astro/Next/Gatsby + Netlify/Vercel 远端 builder）拉长成五台计算机协同。对于绝大多数静态站，这种链条不但没有收益，还带来升级风险与调试不透明。

## 最小可行方案

```
markdown → Pandoc → HTML → wrangler/rsync/scp → CDN
```

- **Pandoc** 一行命令把 markdown 转 HTML，支持数学公式、语法高亮、模板；既是可执行程序也是 Python / Haskell 库；
- **`wrangler`**（Cloudflare）/ `rsync` / `scp` 把产物推到 CDN 或 VPS，无需远端 CI；
- 一个 50 行 Python 脚本串起 serve/deploy/watch 子命令，全过程本机完成。

作者甚至讨论了更激进的方案：**HTML + `fetch` 做运行时 include**（把 header/footer 写成独立 HTML 片段，页面里 `fetch` 进来），用多一次网络请求换零构建依赖——对个人博客这种场景是合理的 tradeoff。

## 和 [[complexity]] 主题的连接

[[john-ousterhout]] *APoSD* 把复杂度定义为「两类：从系统本身长出来的 essential complexity、为了解决某个具体问题的 accidental complexity」。现代 JAMstack 堆栈里：

- **essential**：markdown 变 HTML（不可省）、静态托管（不可省）；
- **accidental**：远端 VM 构建、Node 生态依赖、YAML/JSON 配置、主题 DSL、SSR 混入 SSG、hydrate/preload 策略……

Joshi 的主张等价于「把 accidental 层全砍掉」。这和 [[red-flags]] 里 Peter Norvig 说的「software complexity multiplier」是同一个矛盾的两端。

## 这不是「永远不要用框架」

对于大流量站、多作者协作、需要 i18n / preview / A/B 的商业站，框架的价值是真实的。但对「一个人的技术博客」这种最常见场景，VM 构建只是 CDN 厂商的增值销售——本地推送能覆盖 95% 的需求。

## 相关

- [[complexity]]
- [[tactical-programming]]
- [[cognitive-load]]

## Sources

- [[sources/apoorvaj-static-site-antiframework]]
