---
tags: [渲染, shader]
date: 2026-04-05
sources: 1
---

# Fragment Shader

**每 fragment 执行**的可编程着色阶段（也叫 Pixel Shader）。

## 职责

- 采样纹理
- 计算光照
- 输出最终颜色（可多个 Render Target，见 MRT）
- 可选择 discard（丢弃此 fragment）

## 关键性能特征

- **Texture Sampling 是移动端最昂贵**的操作。
- 分支（dynamic branching）可能让同 warp 的其它线程空转。
- 精度：使用 `half`/`fixed` 代替 `float` 大幅降低移动端带宽消耗。

## Fragment vs Pixel

一个 pixel 可能对应多个 fragment（MSAA、透明叠加）。fragment shader 运行在 fragment 粒度。

## 破坏 Early-Z 的做法

- 写 `gl_FragDepth`（自定义深度输出）
- 调用 `discard`
- 使用 alpha test

详见 [[early-z-late-z]]。

## 相关

- [[rendering-pipeline]]
- [[early-z-late-z]]
- [[overdraw]]
- [[tbdr-vs-imr]]
- [[compute-vs-raster-points]] —— 单像素点的 2×2 quad overshading 现象
- [[gpu-image-editor-brush]] —— 2D 图像编辑器把笔刷合成写成 fragment shader + ping-pong framebuffer
- [[shaping-functions]] — step/smoothstep/lerp/sin/frac 等片元着色器基础塑形原语
- [[uv-manipulation-nodes]] —— Shader Graph 里的 UV 变换节点
- [[sampler-filter-wrap-modes]] —— 纹理采样器的 Filter / Wrap 设置
- [[scene-color-depth-nodes]] —— 透明物体如何读回场景颜色与深度
- [[particle-custom-vertex-streams]] —— 粒子系统到 shader 的逐粒子数据通道
- [[unity-grabpass-blur]] —— Unity GrabPass + 可分高斯模糊的入门实现
- [[texture-encoded-state]] —— 把 per-pixel 时间戳/状态塞进纹理通道，供 fragment shader 消费
- [[shader-vector-math-primer]]
- [[metal-shading-language-basics]] —— MSL 的 fragment 函数限定符与 `[[stage_in]]` 插值语义

## Sources

- [[sources/rtr-day05]]
