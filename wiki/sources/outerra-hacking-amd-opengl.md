---
tags: [source, graphics, opengl, depth-buffer, amd, 驱动调试, reversed-z]
date: 2026-04-27
sources: 1
---

# Hacking AMD OpenGL Drivers（Outerra Blog）

[[people/outerra-team]] 发表于 2013 年 7 月的短文，记录了一次用二进制驱动 patch 证明"AMD 完全可以支持非钳制 glDepthRange"的实验——核心目的是为行星引擎争取 reversed-Z 浮点深度缓冲在 OpenGL / AMD 上的可用性。

## 摘要

背景是 Outerra 已使用[[logarithmic-depth-buffer|对数深度缓冲]]来解决行星尺度下的 z 精度问题，但该方案需要在片段着色器写 `gl_FragDepth`，会关闭 GPU 的 Early-Z 优化，带来额外带宽开销。理论上，在 OpenGL 中使用 reversed-Z 浮点深度缓冲（把远近平面对调）可以达到相近的精度，且不需要写片段深度——但这要求 `glDepthRange` 接受负值参数（如 `-1` 到 `1`）来抵消 OpenGL NDC 的 `[-1,1]` 偏置问题。NVIDIA 硬件通过非标准扩展 `glDepthRangedNV` 支持此特性；AMD 驱动则将参数钳制到 `[0,1]`，拒绝负值。

Outerra 找到 AMD OpenGL 驱动二进制中执行钳制的指令，绕过它之后，`glDepthRange(-1, 1)` 立即生效，reversed-Z 浮点深度缓冲开始正常工作，在 `near=0.01m` 的条件下实测精度为：100m 处约 0.03mm、10km 处约 0.003m、1000km 处约 0.3m——足以覆盖整个宇宙尺度。文章最后明确说明这只是可行性演示，正式使用驱动 hack 不现实；真正的目的是向 AMD 证明没有技术障碍，希望他们正式支持该扩展。

## 关键要点

- OpenGL NDC 的 z ∈ [-1,1] 设计引入了一个 0.5 偏置，导致 reversed-Z 精度优势消失（不同于 Direct3D 的 [0,1] NDC）
- AMD 驱动在 `glDepthRange` 调用时强制钳制下界到 0，通过 patch 单条汇编指令即可跳过
- patch 后 reversed-Z 投影矩阵的 far 项为零（远平面映射到 0），深度精度对数分布，不再需要片段写深度
- 作者认为 AMD 没有技术理由不支持 `glDepthRangedNV` 等价扩展，文章本质是一份可复现的 bug report
- 与 [[logarithmic-depth-buffer]] 的关系：两者都是应对 OpenGL 深度精度不足的路线，对数深度缓冲无需驱动扩展但有 Early-Z 代价，reversed-Z 需要厂商扩展但性能更优

## 链接到的概念

- [[logarithmic-depth-buffer]]
- [[reversed-z]]
- [[people/outerra-team]]

## 原文

- 链接：https://outerra.blogspot.com/2013/07/hacking-amd-opengl-drivers.html
- 本地：`raw/articles/outerra.blogspot.com/2013-07-19_hacking-amd-opengl-drivers.md`
