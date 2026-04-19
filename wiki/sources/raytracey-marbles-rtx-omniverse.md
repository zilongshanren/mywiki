---
tags: [source, rendering, path-tracing, nvidia, omniverse, many-lights]
date: 2026-04-19
sources: 1
---

# Marbles RTX 夜景版在 NVIDIA Omniverse 上实时渲染（Sam Lapere / Ray Tracey's blog）

[[sam-lapere|Sam Lapere]] 发表于 2020 年 9 月 RTX 30 发布会后的短文，抓住 Marbles RTX 夜景版作为 [[nvidia-omniverse|NVIDIA Omniverse]] 实时路径追踪能力的关键样本。

## 摘要

NVIDIA 在 RTX 30 发布会上展示了 Marbles RTX 的夜景/改进版本：场景里包含数十个小光源却没有明显噪声劣化——Lapere 在博文里明确指出这一点"对任何路径追踪器都是出了名的难题"，并链到 Dartmouth 的 Bitterli 2020 [Spatiotemporal reservoir resampling](https://cs.dartmouth.edu/~wjarosz/publications/bitterli20spatiotemporal.html)（后来被通称为 ReSTIR）作为这件事得以实时的理论基础之一。整段渲染在 Omniverse 平台上实时完成，Omniverse 被定位为一个"协作 + 实时路径追踪"的新平台，并在同年 12 月开放 open beta。文章还顺带串联了 Siggraph 2020 的 Omniverse 深度介绍。

## 关键要点

- "Many lights is notoriously hard for a path tracer, let alone a real-time one"——many-light 场景是 Omniverse 这轮展示的核心卖点。
- 点明 ReSTIR / spatiotemporal reservoir resampling（Bitterli 2020）是让 many-light 实时路径追踪可行的关键研究之一。
- Marbles RTX 在单张 RTX 30 级 GPU 上实时完成完整 path tracing（配合 DLSS + denoiser）。
- Omniverse 是 NVIDIA 面向内容创作的"实时、近乎无噪"路径追踪协作平台；2020 年 12 月进入 open beta。
- 博文实质是产品节点记录：之后的 2021 Siggraph kitchen-sink making-of 与 2022 的 Racer RTX 是同一脉络的延伸（Lapere 在其他帖子里接着跟踪）。

## 链接到的概念

- [[nvidia-omniverse]]
- [[path-tracing-monte-carlo]]
- [[monte-carlo-integration]]
- [[hybrid-raytracing-pipeline]]
- [[lighthouse-2-optix]]
- [[sam-lapere]]

## 原文

- 链接：http://raytracey.blogspot.com/2020/09/marbles-rtx-at-night.html
- 本地：`raw/articles/raytracey.blogspot.com/2020-09-10_marbles-rtx-at-night-rendered-in-nvidia-omniverse.md`
