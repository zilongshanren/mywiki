---
tags: [渲染, 路径追踪, NVIDIA, RTX, 产品平台]
date: 2026-04-19
sources: 1
---

# NVIDIA Omniverse：实时路径追踪产品化平台

NVIDIA 面向内容创作/协作推出的 USD 中心平台，渲染后端的核心卖点是**实时、近乎无噪的路径追踪**。[[sam-lapere|Sam Lapere]] 在 2020 年 RTX 30 发布会后的博客笔记里，把 Marbles RTX 夜景 demo 作为这个平台的标志性展示来讨论。

## Marbles RTX at night 里值得记下的事实

- **Many lights is notoriously hard for path tracers**：一个场景里几十到上百个小光源，对普通 path tracer 是棘手问题（直接光采样的方差、light sampling PDF 的选择），更不用说实时。Lapere 明确引用了 Dartmouth 的 Bitterli 2020 [Spatiotemporal reservoir resampling](https://cs.dartmouth.edu/~wjarosz/publications/bitterli20spatiotemporal.html)——即后来普遍称为 ReSTIR 的工作——作为"这件事现在为什么能实时"的关键一环。
- **单 GPU 上实时渲染**：Marbles 的 dusk/night 版本在 RTX 30 级单卡上实时跑完整 path tracing（加 DLSS + denoiser），相比 2018 年 Turing 首发时的 hybrid rasterization + RT 反射是质变。
- **Omniverse open beta**：2020 年 12 月开放测试，进入 CGI 工作流的入口阶段。

## 产品节点（Lapere 视角时间线）

- **2020-09 Marbles RTX**：RTX 30 发布会上首次出现的夜景/多光源版本，被 Lapere 视为 Omniverse 平台能力的标志。
- **2021 Siggraph**：Omniverse 在 GTC keynote making-of 里亮相，包括 "Realistic digital human rendering with Omniverse RTX Renderer"（数字人实时路径追踪）。
- **2022-09 Racer RTX**：完全实时光追的小游戏 demo，跑在单张 RTX 40 上，Lapere 记下了它相对 Marbles 的又一代跃迁。

这些节点在 Lapere 的原文里多为视频链接和短评，但合在一起是"消费级 GPU 从 hybrid ray tracing 走向完整 real-time path tracing"的产品化路线图。

## 与其它实时路径追踪脉络的对照

- **研究/独立脉络**：Jacco Bikker 的 Brigade → [[lighthouse-2-optix|Lighthouse 2]]，强调开源、小而美、算法可热改。
- **商业引擎脉络**：游戏引擎里的混合光追（[[hybrid-raytracing-pipeline]]、[[hybrid-raytraced-shadows-reflections]]）长期并行存在，直到 ReSTIR + 硬件 RT Core + DLSS 叠加后，"全路径追踪"才在消费硬件上接近可接受的性能区间。
- **算法基础**：许多结论仍来自 [[monte-carlo-integration]] / [[path-tracing-monte-carlo]] / importance sampling / [[quasi-monte-carlo]]；Omniverse 是把这些做成稳定产品体验的一端，而非新原理的源头。

## 相关

- [[lighthouse-2-optix]]
- [[hybrid-raytracing-pipeline]]
- [[path-tracing-monte-carlo]]
- [[monte-carlo-integration]]
- [[sam-lapere]]

## Sources

- [[sources/raytracey-marbles-rtx-omniverse]]
