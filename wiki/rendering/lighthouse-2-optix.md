---
tags: [渲染, 路径追踪, OptiX, RTX, 开源框架]
date: 2026-04-19
sources: 1
---

# Lighthouse 2：基于 OptiX 7 的开源实时 GPU 路径追踪框架

Jacco Bikker 在 2019 年开源的 Apache 2.0 实时路径追踪框架，是 Brigade / Brigade 2 的精神续作。前辈 Brigade 早在 2010 年就在 GPU 上演示过游戏级实时 path tracing，比 NVIDIA 把 RTX 摆上台面早了将近十年。[[sam-lapere|Sam Lapere]] 在博客上追踪整个谱系，把 Lighthouse 2 定位为"Brigade 在 RTX 时代的重写"。

## 关键设计取向

- **完全基于 OptiX**：利用 NVIDIA 的 BVH 构建/遍历基础设施，内建的 two-level BVH 让带上千实例的**动态场景**几乎免费支持刚体动画。
- **三套手调 render core 并存**：OptiX 5、OptiX Prime（都面向 Maxwell / Pascal）与 OptiX 7（面向 Turing + RT Core）。OptiX 7 比 OptiX 5 低层很多，交给开发者更多控制、运行时开销更低，在 Turing 上相对 OptiX 5 还能再快 ~35%。
- **RT Core 红利**：Lighthouse 2 跑在 RTX 2060（OptiX 7）上相对 Pascal（OptiX 5）**整整快约 6×**。这是 [[hybrid-raytracing-pipeline|混合光追管线]]与全路径追踪之间差距被硬件快速拉近的一个早期数据点。
- **Eric Heitz 风格的 blue-noise 采样**：直接采用 Heitz 小组发表的蓝噪声方案（[eheitzresearch.wordpress.com/762-2](https://eheitzresearch.wordpress.com/762-2/)），低 sample per pixel 下图像噪声分布更舒服，尤其配合 TAA / denoiser。
- **完整场景图 + Disney "principled" BRDF**：含实例化、相机、灯光、材质，GUI 可实时调 BRDF 参数，便于把它当成算法实验台。

## 为什么它对学习路径追踪有用

相对 PBRT 这种"offline、千页教材"，Lighthouse 2 代码量小、跑得动、可热改，和 [[path-tracing-basics|Peters 的 path tracing 入门资源]]正好互补：Peters 的两阶段教学负责讲清楚 rendering equation 和 importance sampling，Lighthouse 2 则演示了"同一套原理在 RTX 硬件上如何工程化成产品"。Bikker 自己把它当成算法/denoiser 实验床——把新 sampler 或 denoiser 塞进去、看 RT Core 上实测数字是实时 path tracing 研究常见工作流。

## 与 Brigade、Omniverse 的关系

Brigade（2010）→ Brigade 2（全 GPU）→ Lighthouse 2（OptiX 7 / RTX）这条线是**独立研究者驱动**的实时 path tracing 脉络；与之平行的商业脉络是 OTOY Octane 和之后 NVIDIA 的 [[nvidia-omniverse|Omniverse]] 等平台。Lapere 的观察是：Lighthouse 2 因其简洁和宽松 license，有机会被塞进 Blender 等 DCC 工具做实时预览。

## 相关

- [[path-tracing-basics]]
- [[path-tracing-monte-carlo]]
- [[monte-carlo-integration]]
- [[hybrid-raytracing-pipeline]]
- [[quasi-monte-carlo]]
- [[nvidia-omniverse]]
- [[sam-lapere]]

## Sources

- [[sources/raytracey-lighthouse-2]]
