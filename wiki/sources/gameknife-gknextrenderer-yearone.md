---
tags: [source, 渲染, 光线追踪, 引擎, 年度总结]
date: 2026-04-14
sources: 1
---

# gkNextRenderer - YearOne（gameKnife / gameknife.github.io）

[[people/gameknife]] 发表于 2025 年 5 月 16 日的年度总结。作者从 2024 年五一节开始在 _Ray Tracing in One Weekend_ 基础上启动 [[gknext-renderer|gkNextRenderer]] 项目，一年后回顾自己"从 DX11 级别的渲染知识重新追赶现代渲染"的过程。

## 摘要

这篇 YearOne 是一个资深图形程序员的"重新学习"札记。作者坦言长期做移动渲染让他的知识停留在 PS3 晚期/PS4 早期，错过了硬件光追、bindless、temporal jitter、样本重用等革命。买了 M3 Max 笔记本接触硬件光追后，从 RTIO 起步，一年里做出了纯 path tracing、基于 [[visibility-buffer|Visibility Buffer]] 的 [[hybrid-raytracing-pipeline|hybrid renderer]]、reverse-hybrid、ambient cube probe、编辑器、slang shader 迁移等大量课题。文章覆盖 hardware-raytracing、pathtracing、visibilitybuffer、hybridtracing、bindless、vcpkg、cross-platform、tinybvh、imgui、slang、quickjs、moltenvk、android、AI 协作、gkNextEngine 共 15 个主题，每段都夹带作者的工程取舍与反思。

## 关键要点

- 未来是硬件光追的：显卡厂商 RTX 20→50 光追性能提升是光栅化的数倍，照片级真实感只能靠 path tracing。
- 纯 path tracing shader 代码量可以低于 100 行，瓶颈在实时性；下一步要啃 reservoir 样本复用。
- Visibility Buffer 可以**完美替代 primary ray**，triangleId 要么靠顶点拆分要么靠 provoking vertex + meshoptimizer。
- Hybrid 管线 = VB primary + 短距离硬件光追 secondary + cache 远场，city 场景 2K@120fps。
- 反向 hybrid：primary ray 写 VB + compute shading 完成剩下一切，"drawcall 优化的整套技术都不复存在"。
- [[bindless-rendering|Bindless]] 让 RenderDoc 里的 Rockstar / Decima 引擎 shader"异常精简"。
- Vulkan + vcpkg + GitHub Actions + MoltenVK + 骁龙 8 Gen 2 / 865 让跨平台成本极低。
- tinybvh 单头文件、CPU/GPU 同构 BVH，支持 NEON；10k rays/frame 轻松 120fps。
- slang 完全兼容 hlsl 基础上提供泛型 / module / interface / 自动微分（slangpy 可用于神经纹理压缩）。
- quickjs 的"小体积与轻微性能约束"反而逼迫正确地只把事务性逻辑放进脚本。
- 作者大量使用 Claude 3.7 Sonnet 协作写 C++/GLSL/HLSL，认为 AGI 可能就在大语言模型上出现。

## 链接到的概念

- [[visibility-buffer]]
- [[hybrid-raytracing-pipeline]]
- [[bindless-rendering]]
- [[gknext-renderer]]
- [[gkengine]]
- [[deferred-rendering]]

## 原文

- 链接：<http://gameknife.github.io/tech/2025/05/16/gknextrenderer-yearone/>
- 本地：`raw/articles/gameknife.github.io/2025-05-16_gknextrenderer-yearone.md`
