---
tags: [source, software-design, ui, dom, css, web]
date: 2026-04-19
sources: 1
---

# HTML is Dead, Long Live HTML（Steven Wittens / acko.net）

[[steven-wittens]] 发表于 2025 年 8 月的长文，主题一句话：DOM/CSS/HTML 三件套已过时但没人有动力换掉，[[dom-replacement-rethink|应直接在 DOM 之外开新表面]]而非继续修补。

## 摘要

作者从 `document.body` 的 350+ key、660 个 CSS property 开篇，指出 DOM 膨胀仍在继续，Web Components 生态迟到且不 popular。他给出 CSS 的正确 mental model——先 outside-in 再 inside-out 两遍，而非 constraint solver——并解释 flex speculative layout 的递归依赖陷阱、`contain: size` / `will-change` 为何是 "subtractive API"。他强调 CSS 其实是"富文本继承样式 + 无继承 block/inline 布局"两套系统缝在一起的历史错误；SVG 与 CSS 的能力交错、`text-ellipsis` / `position: sticky` / `z-index` 全部卡在 v1；WICG "HTML in Canvas" 提案被一条条拆解为方向错误——接管整棵子树的交互只为定制外观，canvas 自身又缺系统字体 API，左右都是死胡同。替代路径：把 DOM 里早已存在的"HTML fragment as composite value"做成公开 API，新表面在 DOM 之外另起，Servo/Ladybird 式新实现最有希望；配合 Spectre 导致的多进程/多 origin 隔离强制重构，是可见的 carrot。存在性证明是作者自己的 [[use-gpu-reactive-runtime|Use.GPU]] HTML-like renderer：完整 X/Y flex 模型，单人一小部分代码量，垂直居中 trivial，div 上直接挂 shader。

## 关键要点

- `document.body` 350+ property，`document.body.style` 660 CSS property，property 与 method 界线模糊
- Web Components 迟到且 Shadow DOM 过度嵌套；DOM 的 SGML/XML 血统导致 stringly-typed
- CSS 正确 mental model：outside-in（父约束下传）+ inside-out（子撑开父）两遍，不是 constraint solver
- Flex speculative layout 有递归依赖风险，`contain: size` / `flex-basis` 是 subtractive 补丁
- CSS = 富文本继承样式系统 + 无继承 block/inline 布局系统混缝，历史错误
- SVG 与 CSS 能力交错：SVG 有 polygonal hit-testing 但弱渲染效果；CSS 有 SVG-envy 但不完整
- `text-ellipsis` 不能整段、`position: sticky` 需嵌套 hack、`z-index` 无相对值——全部卡在 v1
- "HTML in Canvas" 提案批判：接管子树交互只为定制外观，canvas 无系统字体 API
- 新方向：view tree / render tree 的分离是真实的；view tree 该是什么、该 lower 成什么是真问题
- Servo / Ladybird / Tauri 是更干净的实现者；Spectre 导致的 SharedArrayBuffer 死刑为重构提供动机
- Use.GPU 的 HTML-like renderer 是存在性证明：90% 覆盖，一小部分代码量

## 链接到的概念

- [[dom-replacement-rethink]]
- [[use-gpu-reactive-runtime]]
- [[steven-wittens]]
- [[intent-vs-state]]

## 原文

- 链接：https://acko.net/blog/html-is-dead-long-live-html/
- 本地：`raw/articles/acko.net/2025-08-06_html-is-dead-long-live-html.md`
