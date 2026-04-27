---
tags: [人物, 作者]
date: 2026-04-19
sources: 10
---

# Wolfgang Engel

图形程序员，博客 **Diary of a Graphics Programmer**（diaryofagraphicsprogrammer.blogspot.com）的作者，Confetti FX 的联合创始人，跨平台渲染框架 **[[the-forge-renderer|The Forge]]** 的主要推动者，也是 *ShaderX* / *GPU Pro* / *GPU Zen* 系列技术文集的编辑。2009 年他在 SIGGRAPH 上提出 **Light Pre-Pass**（延迟光照的一种变体），后来成为游戏中多年被采用的管线之一。

2015 年前后，他和 Confetti 团队开始把 Christoph Schied / Carsten Dachsbacher 的 *Deferred Attribute Interpolation* 与 Burns & Hunt 的 *Visibility Buffer* 工程化，用 `ExecuteIndirect` + async compute 重新组织，最终形成一条跨 DirectX 12 / Vulkan / Metal 2 / Linux / 主机平台都能跑的 [[visibility-buffer|Triangle Visibility Buffer]] 管线。这个系列的文章和源码是实时 VB 管线最权威的公开参考之一。

2018 年 DXR 公开提案时，他是少数公开质疑**给 ray tracing 单独建一套 API** 是否对游戏开发者和发行商经济上合理的人之一：他担心黑箱化的加速结构会重演「驱动-API-QA」三方扯皮的老账，建议改走 compute feature level 扩展的路线。随后他与 [[kostas-anagnostou|Kostas Anagnostou]] 合作把后者的 **[[hybrid-raytraced-shadows-reflections|hybrid ray-traced shadow]]** 移植到 The Forge，跨 PC / macOS / iOS / Xbox 运行，以此证明「不用 DXR 也能做 hybrid ray tracing」。

Confetti 用 The Forge 为 Supergiant 重写了 *Hades* 的引擎（PC / macOS / Switch 三平台）。2020 年他明确把 The Forge 的定位说成「新一代 GPU Zen」——相比书本 + 幻灯片，提供可以直接编译运行并已在出货游戏上验证过的源码，是更有价值的知识共享形式。

## 相关

- [[the-forge-renderer]] —— Confetti 跨平台开源渲染框架
- [[visibility-buffer]] —— Triangle VB 核心页
- [[triangle-filtering-pipeline]] —— 三角形剔除 → VB 填充 → Forward++ 的完整流水线
- [[ray-tracing-api-debate]] —— 他 2018 年对 DXR 黑箱化的公开质疑
- [[hybrid-raytraced-shadows-reflections]] —— 与 Kostas 合作移植到 The Forge 的 hybrid 实现
- [[deferred-rendering]]
- [[async-compute]]
- [[kostas-anagnostou]]
- [[graphics-subsystem-no-lut]] — 避免查找表的图形子系统设计原则
- [[graphics-subsystem-even-error-distribution]] — 均匀误差分布设计规则
- [[msaa-deferred-edge-detection]] — 延迟管线 MSAA 边缘检测
- [[screen-space-filter-kernel]] — 屏幕空间滤波核设计规则

## Sources

- [[sources/wolfgang-engel-hdr10-tv-setup]]
- [[sources/wolfgang-engel-triangle-visibility-buffer]]
- [[sources/wolfgang-engel-dxr-api-debate]]
- [[sources/wolfgang-engel-ray-tracing-without-api]]
- [[sources/wolfgang-engel-forge-history]]
- [[sources/humus-hardware-tessellation]]
- [[sources/humus-edge-detection-trick]]
- [[sources/humus-screen-space-rules]]
- [[sources/humus-tile-based-deferred-forward]]
- [[sources/humus-graphics-programmer-knowledge]]
- [[sources/humus-no-lut-rules]]
- [[sources/humus-even-error-distribution-rules]]
- [[sources/humus-dx11-1-notes]]
