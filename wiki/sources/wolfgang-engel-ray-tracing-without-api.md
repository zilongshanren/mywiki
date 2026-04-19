---
tags: [source, graphics, 光线追踪, 混合管线, compute-shader, forge, 跨平台]
date: 2026-04-19
sources: 1
---

# Ray Tracing without Ray Tracing API（Wolfgang Engel）

[[people/wolfgang-engel|Wolfgang Engel]] 2018 年 9 月的后续博客，对应 **[[ray-tracing-api-debate|DXR 之辩]]** 的工程落地：*既然我认为 RT API 不必要，那就用 compute shader 手写一条跨平台 hybrid RT，看跑得多好*。

## 摘要

文章宣布 [[the-forge-renderer|The Forge]] 的一个新版本落地了 [[kostas-anagnostou|Kostas Anagnostou]] 的 *Hybrid Ray Traced Shadows*。上下文：当时 Engel 正在跟 Kostas 约 *GPU Zen 2* 的 culling 章节稿子，顺便邀请他把自己的 hybrid shadow 实验移植到 Confetti 的跨平台框架里。Kostas 借这次机会回头把原型大幅优化，最终得到一个**在 The Forge 所有平台（PC DX12 / Vulkan / Linux / macOS Metal 2 / iOS / Xbox）都能跑**的纯 compute shader hybrid ray tracer。

当前版本只做了 **shadow**，目标是 shadow + reflection + AO 全套 hybrid RT 可用。Engel 在文中发出一个对比断言：**即便跑在 NV RTX 上，DXR 版的 hybrid shadow 也不会比 Confetti 的手写 compute 版快多少**——除了 RTX 之外，其它硬件上 DXR 会是"subpar 性能"。他在评论区追问时澄清：他比较的对象是微软的 DXR reference / 当时能跑的 DXR 实现，并邀请读者下载源码自己测。

iPhone 7 跑 1334×750 的 Sponza 场景被作为跨平台表现的示例——"astonishingly well"。文章很短，本质是个 release note + 政策声明：**「hybrid ray tracing 不用 RT API 也能做，The Forge 已经证明了」。**

## 关键要点

- 当前 real-time ray tracing 的游戏用例集中在三块：**shadow、reflection、AO**——都可以用 compute shader 替代
- **移植路径**：原型在 Windows DX12 / Vulkan 上开发 → 平移到 macOS / iOS / Xbox；iOS 还有进一步优化空间
- 下一步是 hybrid reflection，最终目标是在**所有 GPU / 所有平台**提供 shadow + reflection + AO 套件
- 对 DXR 版本的直接挑战：**即便是 RTX，我们的 compute 版对比 DXR 也应该表现"admirably and practically useful"**
- iPhone 7 Sponza 1334×750 运行良好，证明 compute ray tracing 在移动端可达
- 技术细节可参见 [[hybrid-raytraced-shadows-reflections]]（同一套算法的 wiki 概念页，来自 Kostas 的博客）

## 链接到的概念

- [[hybrid-raytraced-shadows-reflections]]
- [[ray-tracing-api-debate]]
- [[hybrid-raytracing-pipeline]]
- [[the-forge-renderer]]
- [[people/wolfgang-engel]]
- [[kostas-anagnostou]]

## 原文

- 链接：http://diaryofagraphicsprogrammer.blogspot.com/2018/09/ray-tracing-without-ray-tracing-api.html
- 本地：`raw/articles/diaryofagraphicsprogrammer.blogspot.com/2018-09-07_ray-tracing-without-ray-tracing-api.md`
