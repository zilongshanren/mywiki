---
tags: [source, 渲染, 路径追踪, 教学, 蒙特卡洛, 重要性采样]
date: 2026-04-19
sources: 1
---

# Path tracing lectures（Christoph Peters）

[[christoph-peters|Christoph Peters]] 2024 年给 TU Delft 硕士准备、后公开发布的 path tracing 系列讲座：113 分钟视频 + 一个开源 Vulkan 实现——填补了之前 [[sources/peters-path-tracing-workshop|path tracing workshop]] 未写的 Part 3（重要性采样）。

## 摘要

两节讲座。**Lecture 1** 和 workshop Part 2 相仿——讲到 naive path tracer 为止。**Lecture 2** 深入重要性采样：BRDF importance sampling、light sampling（直连光源、next-event estimation）、Multiple Importance Sampling（MIS）。格式上没有 ShaderToy 习题，但有开源 Vulkan 实现作为参考：C + GLFW + Nuklear（替代 imgui）、Frostbite BRDF、spherical light source、stratified random numbers + blue noise texture、progressive rendering（无 denoiser）。代码 **7575 行、345 KB、~1 秒编译**，延续 Peters "keep it simple" 的 toy renderer 哲学——紧凑到能读完、能 hack。文件格式与之前的 toy renderer 兼容。Lectures 和 workshop 配合使用：workshop 教"如何写一个能跑的 path tracer"，lectures 教"如何让它低方差"。

## 关键要点

- 113 分钟、两节课，lecture 2 是 workshop 未完成的 Part 3。
- **重要性采样三件套**：BRDF IS、light IS、MIS。
- 开源 Vulkan 实现：7.5K 行，C 写的，Frostbite BRDF + spherical light。
- 没有 denoiser、没有 path guiding、没有 ReSTIR——把这些都作为 future extensions。
- 代码风格与 [[sources/peters-spectral-rendering-2-real-time|Peters 其它实现]] 一致，互为延伸。

## 链接到的概念

- [[path-tracing-basics]]
- [[radiometry-integral-view]]
- [[microfacet-brdf]]
- [[christoph-peters]]

## 原文

- 链接：http://momentsingraphics.de/PathTracingLectures.html
- 本地：`raw/articles/momentsingraphics.de/2024-12-19_path-tracing-lectures.md`
