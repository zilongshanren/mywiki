---
tags: [人物, 作者, rendering, ui]
date: 2026-04-19
sources: 3
---

# Steven Wittens

博客 [Hackery, Math & Design — Acko.net](https://acko.net) 作者，独立开发者。声音辛辣、论点尖锐，技术写作横跨图形渲染、UI 架构与 Web 平台批判。

代表作品是 [Use.GPU](https://usegpu.live) —— 一套基于 WebGPU 的声明式/响应式渲染运行时，内建 shader linker、reconciler、reactive run-time，官方定位是"给每个 draw call 独立 shader"的实验平台。其个人设计观是：前端、渲染、数据建模本质上都是同一个 reconciler 问题，跨层强行切分（后端/前端、数据/视图、intent/state）才是大多数应用复杂度的来源。

写作风格融合技术细节与辛辣评论，常见主题：

- UI 架构中的 [[intent-vs-state]] 区分、patch 驱动的数据流
- WebGPU / Use.GPU 渲染实现，近期聚焦 [[ground-truth-ambient-occlusion]] 与 [[render-pass-orchestration]]
- 对 DOM/CSS/HTML 的系统性批判，主张重新设计 [[dom-replacement-rethink]]

## 相关

- [[use-gpu-reactive-runtime]]
- [[intent-vs-state]]
- [[ground-truth-ambient-occlusion]]
- [[dom-replacement-rethink]]

## Sources

- [[sources/acko-i-is-for-intent]]
- [[sources/acko-occlusion-with-bells-on]]
- [[sources/acko-html-is-dead]]
