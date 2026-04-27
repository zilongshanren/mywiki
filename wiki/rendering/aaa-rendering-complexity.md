---
tags: [渲染, aaa, 复杂度, 工业, 组织, 光线追踪, 创新周期]
date: 2026-04-27
sources: 1
---

# AAA 渲染复杂度的组织根源

AAA 游戏实时渲染引擎持续增长的复杂度，其根本驱动力不是技术本身，而是组织结构与市场竞争的必然产物。

## 核心论点

[[people/angelo-pesce]] 在 2020 年的文章中，以 John Carmack 2001 年展示 Doom 3 时"stencil shadows 将统一所有光照"的承诺开篇：那次技术革命并没有让引擎变简单，反而使之更复杂。他进而问：每次渲染硬件跃迁后，引擎是变简单了还是更复杂了？答案始终是更复杂。

根本原因是经济激励：AAA 工作室愿意花一个月工程师时间换一毫秒帧时间。只要这个等式成立，引擎就永远不会变简单——工程师会把可用算力全部填满。这与 Clayton Christensen 的创新周期理论吻合：AAA 渲染处于差异化竞争阶段，未进入商品化，工程投入持续向定制化、性能极限倾斜，而非向标准化、可复用倾斜。

## 光线追踪案例

光线追踪的支持者常声称它将"统一"阴影、反射、GI 等各类 hack。Pesce 的反驳是：即便光追简化了某些子问题，整体引擎也会因开拓新可能性而填入更多技术。RT 阴影和 RT 反射在实现层面远比听起来难（见 CoD:CW 的 RT 阴影分享），混合路径（hybrid rasterize + RT）是必然结果，见 [[rendering/hybrid-raytracing-pipeline]]。

## 两个平行世界

Pesce 同时指出，这只是 AAA 这一条轨道的命运。低端市场（Unity 免费版、Unreal 免费版、Three.js、Roblox）已高度商品化：不需要任何渲染知识也能做出 3D 游戏。这两个世界平行运行，互不干扰。新硬件（包括光追）在低端市场的技术变化对用户是透明的，永远隐藏在工具层之下。

## 与相关概念的关系

这个论点与 [[rendering/rendering-roi-philosophy]] 和 [[rendering/realtime-quality-vs-quantity]] 相互补充但视角不同：前者讨论在复杂度内部如何做优先级，后者讨论质量与功能数量的取舍，而本页的核心是"AAA 为什么注定越来越复杂"的结构性解释。

## Sources

- [[sources/c0de517e-rt-wont-simplify]]
