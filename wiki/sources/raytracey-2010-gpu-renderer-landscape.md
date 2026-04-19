---
tags: [source, 渲染, 路径追踪, GPU, 历史]
date: 2026-04-19
sources: 1
---

# Fuck yeah! — 2010 GPU 非偏置渲染器大爆发（Sam Lapere / Ray Tracey's blog）

[[sam-lapere|Sam Lapere]] 于 2010-01-22 写的一篇"行业感慨"博客。以极度兴奋的口吻把 2009-2010 之交 GPU 渲染器井喷盘了一遍——对研究这波 GPU 非偏置渲染商业化起点的时间线是难得的一手档案。

## 摘要

作者开篇预测 2010 是 GPU 光线追踪的"breakthrough year"，列出短时间内密集冒出的 GPU 渲染器：V-Ray RT CUDA（Chaos, 2009 Siggraph）、iray（mental images, 2009 GTC, 15 张 Tesla）、LuxRender OpenCL（2009-12）、Octane Render（2010-01，前 LuxRender 主程）。紧接着他分析了触发这一轮集体觉醒的原因：2009-12 Intel 宣布 [[larrabee-cancellation|Larrabee 推迟]]，此前一大批渲染器厂商在等 Larrabee 这种"多核 x86 GPU"，Larrabee 死掉后继续只做 CPU 就等于让出市场，于是 Fryrender（Arion）、Bunkspeed、Indigo 集体宣布 GPU 加速计划。作者观察到让这些传统渲染器厂商相信 GPU 有用的"存在证明"是 OptiX（NVIRT）、V-Ray GPU、iray、以及 OTOY 的 raytraced Ruby demo。结尾展望 GPU 云端光追（RealityServer、Fusion Render Cloud）。

## 关键要点

- 2010 年初 GPU 非偏置渲染器清单：V-Ray RT GPU / iray / LuxRender OpenCL / Octane / Arion / BrazilRT
- Octane 靠单张 GTX 260 就做 demo，iray 在 15 张 Tesla 上——两代硬件成本的巨大反差
- Larrabee 取消是非直接但关键的触发器：让"等 Intel 救世主"的 CPU 渲染器厂商被迫拥抱 GPGPU
- 让不懂 GPGPU 的老派程序员相信 GPU 行的存在证明：OptiX、V-Ray GPU、iray、OTOY Ruby demo
- 文末猜测的下一步——"GPU 云光追"——后来由 [[otoy-cloud-rendering|OTOY 云渲染架构]]和 NVIDIA 体系逐步兑现

## 链接到的概念

- [[gpu-unbiased-path-tracing]]
- [[path-tracing-basics]]
- [[path-tracing-monte-carlo]]
- [[lighthouse-2-optix]]
- [[otoy-cloud-rendering]]
- [[sam-lapere]]

## 原文

- 链接：http://raytracey.blogspot.com/2010/01/fuck-yeah.html
- 本地：`raw/articles/raytracey.blogspot.com/2010-01-22_fuck-yeah.md`
