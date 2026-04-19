---
tags: [source, rendering, path-tracing, optix, open-source]
date: 2026-04-19
sources: 1
---

# LightHouse 2：基于 OptiX 的新一代实时 GPU 路径追踪框架开源（Sam Lapere / Ray Tracey's blog）

[[sam-lapere|Sam Lapere]] 发表于 2019 年 9 月的博文，介绍 Jacco Bikker 开源的 [[lighthouse-2-optix|Lighthouse 2]] 框架——Brigade / Brigade 2 的 OptiX 7 / RTX 时代续作。

## 摘要

Lighthouse 2 是 Jacco Bikker 在 GitHub（Apache 2.0）发布的实时 GPU 路径追踪框架，目标是把 Brigade 的"实时 unbiased rendering"思路移植到 NVIDIA 新一代 OptiX/RTX 硬件上。框架并存三套 render core：OptiX 5、OptiX Prime（Maxwell/Pascal）和 OptiX 7（Turing + RT Core）。OptiX 7 更底层、开销更低，在 Turing 上比 OptiX 5 再快约 35%；RTX 2060 跑 OptiX 7 比 Pascal 跑 OptiX 5 整体快约 6×。Lighthouse 2 还用 Eric Heitz 的蓝噪声采样、Disney "principled" BRDF，自带支持数千实例动画的两级 BVH，并提供可实时调参的轻量 GUI，使其既是能用的渲染器也是算法/denoiser 实验台。

## 关键要点

- Brigade（2010）→ Brigade 2（全 GPU）→ Lighthouse 2（OptiX 7/RTX）是 Jacco Bikker 主导的实时路径追踪谱系。
- OptiX 内建 two-level BVH，让带上千实例的动画场景"几乎免费"支持刚体动画。
- OptiX 7 相对 OptiX 5/6 是一次抽象下沉：更多控制、更少开销，在 Turing 上约 +35%；叠加 RT Core 后整体约 6× Pascal。
- 采用 Heitz 小组的蓝噪声采样策略，低 spp 下画面更干净，配合 TAA/denoiser。
- 场景图含实例、相机、灯光、材质；Disney principled BRDF 参数在 GUI 实时可调。
- 代码简洁、license 宽松，作者认为有机会被塞进 Blender 等 DCC 工具做实时预览。

## 链接到的概念

- [[lighthouse-2-optix]]
- [[path-tracing-basics]]
- [[path-tracing-monte-carlo]]
- [[monte-carlo-integration]]
- [[hybrid-raytracing-pipeline]]
- [[quasi-monte-carlo]]
- [[sam-lapere]]

## 原文

- 链接：http://raytracey.blogspot.com/2019/09/lighthouse-2-new-optix-based-real-time.html
- 本地：`raw/articles/raytracey.blogspot.com/2019-09-15_lighthouse-2-the-new-optix-based-real-time-gpu-path-tracing.md`
