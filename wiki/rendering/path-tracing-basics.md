---
tags: [渲染, 路径追踪, 蒙特卡洛, 物理渲染, 教学]
date: 2026-04-19
sources: 2
---

# 路径追踪入门的最小可行路径

[[christoph-peters|Christoph Peters]] 面向 Intel 开设的 [path tracing workshop](http://momentsingraphics.de/PathTracingWorkshop.html)（76 分钟视频 + ShaderToy 习题）和面向 TU Delft 硕士的 [path tracing lectures](http://momentsingraphics.de/PathTracingLectures.html)（113 分钟视频 + 开源 Vulkan 实现）共同给出了一条**最小可行路径**：从"写一个功能正确的 path tracer"到"写一个收敛合理的 path tracer"。两者侧重不同，合起来是一套完整的起步资源。

## 两阶段法

### 阶段 1：正确性（workshop part 1 + 2）

目标：写出能跑但不管收敛速度的 path tracer。

- **Part 1 - Ray tracing**：GLSL + ShaderToy 入门、计算相机射线、ray-triangle / ray-mesh 交。没有 acceleration structure，慢但正确。结果：未着色的 Cornell Box。
- **Part 2 - Path tracing**：引入 [[radiometry-integral-view|radiance / rendering equation]] 和 [[monte-carlo-integration|Monte Carlo integration]]；在半球上均匀采样方向，直接光 + 递归追踪；收敛需要大量 sample，但结果是正确的带全局光照 Cornell Box。

**特征**：每一步都**简化到极致**——没有 acceleration structure、没有重要性采样、没有 denoiser。这让初学者**看得见**每部分代码对应什么物理量。

### 阶段 2：低方差（lectures part 2）

workshop Part 3（importance sampling）从未写完——取而代之的是**TU Delft 的 lectures**，覆盖相同话题但更深：

- **BRDF 重要性采样**：`sample(ω_i | x, ω_o)` 按 BRDF · cos 做重要性采样。
- **Light sampling / Next event estimation**：直连光源采样，低方差高效。
- **Multiple Importance Sampling (MIS)**：两种 estimator 的平衡权重（balance heuristic / power heuristic）。

伴随的开源 Vulkan 实现（C + Nuklear + GLFW）：Frostbite BRDF、球形光源、stratified blue-noise 随机数、progressive rendering、无 denoiser。代码量**紧**（7.5K 行、345 KB、1 秒编译），延续 Peters "keep it simple" 的 toy renderer 谱系。

## 为什么值得学这个而不是 PBRT 第 4 版

- **PBRT 体量大**（>1000 页）、目标是 offline production-ready——对"搞懂基本原理"用力过猛。
- Peters 的两套资源总计**2–3 小时视频 + 合理的习题**，实时渲染从业者能挤出周末看完。
- 教学选择和**实时路径追踪**硬件的契合度高（DirectX 12 RT / Vulkan RT 出现后，很多 offline 概念开始实时化）。
- 代码是**真的可 hack 的**（7.5K 行对比 PBRT 的几十万行）。

## 与其它教学资源的定位

- Keenan Crane / 姜文渊等的 CMU 15-468 系列：更学术、课程时长大。
- Eric Veach 的 PhD thesis：MIS 和 BDPT 的原始文献。
- Ray Tracing in One Weekend 三部曲：CPU 版本、更轻量、无 MC 深度。
- **Peters 的两套资源**：填补"**GPU + MC + 有工业视角**"这个 slot。

## 想继续深入时的 entry points

- [[hero-wavelength-spectral-sampling]] — 把 MC 扩展到波长维度
- [[spectral-rendering]] — 做 spectral path tracer
- [[projected-solid-angle-sampling]] — spherical cap 上的重要性采样
- [[moment-shadow-mapping]] — Peters 经典贡献

## 相关

- [[christoph-peters]]
- [[radiometry-integral-view]]
- [[photometry-luminance]]
- [[microfacet-brdf]]
- [[quasi-monte-carlo]]

## Sources

- [[sources/peters-path-tracing-workshop]]
- [[sources/peters-path-tracing-lectures]]
