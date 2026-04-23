---
tags: [人物, 作者, 引擎架构, 渲染, bitsquid, stingray]
date: 2026-04-19
sources: 1
---

# Tobias Persson

Bitsquid 共同创始人之一，与 [[niklas-frykholm]] 一起主导 Bitsquid → Autodesk Stingray 的渲染架构，之后与 Niklas 联合创立 Our Machinery / The Machinery 引擎。在 Stingray 时期的对外技术表达里，Tobias 偏重**数据驱动 renderer 架构**与**跨平台 flexible rendering**。

## 主要贡献与公开发表

- **GDC 2012: Flexible Rendering for Multiple Platforms** — Bitsquid 如何用一份 data-driven `render_config` 覆盖多平台。
- **GDC 2011: Benefits of data-driven renderer** — 把 data-driven 从 gameplay 推到 render pipeline 的早期宣言。
- **Render Config Extensions（Stingray 1.5, 2016）** — 参见 [[render-config-extension-points]]，为 plugin 引入"命名插入点 + append 补丁"的扩展接口。
- **The Machinery / Our Machinery 引擎** — Niklas 与 Tobias 在 Autodesk 宣布停产 Stingray 之后创立，延续 data-driven / C-API plugin 的设计哲学。

## 相关
- [[niklas-frykholm]]
- [[render-config-extension-points]]
- [[stingray-data-driven-render-config]]
- [[data-driven-architecture]]
- [[stingray-renderer-three-stage-pipeline]] —— Stingray 渲染 CPU 侧三阶段数据并行架构
- [[stingray-render-resource-context]] —— RenderResource + RRC 的跨 API 资源抽象
- [[main-render-thread-state-reflection]] —— 主/渲染线程状态镜像（Tobias 在 Walkthrough #1 里引用 Asplund 专文）

## Sources
- [[sources/bitsquid-render-config-extensions]]
- [[sources/bitsquid-renderer-walkthrough-1-overview]]
- [[sources/bitsquid-renderer-walkthrough-2-resources]]
