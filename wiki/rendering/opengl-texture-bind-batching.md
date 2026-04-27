---
tags: [渲染, opengl, 性能, 纹理, draw-call]
date: 2026-04-27
sources: 1
---

# OpenGL 纹理绑定批处理（Texture Bind Grouping）

2012 年 Outerra 团队在对象渲染器中发现了一个严重的 NVIDIA 特有性能问题：每次调用 `glBindMultiTextureEXT` 后，**紧随其后的 draw call（如 `glDrawRangeElements`）在 CPU 和 GPU 两侧都出现异常延迟**，最终导致对象渲染 pass 从约 4–5 ms 暴涨到 15 ms（NVIDIA GTX 460，驱动 306.97）。

## 问题诊断

通过 NVIDIA Nsight 确认，延迟集中在纹理绑定变更后的 draw call，而非绑定调用本身。相同的渲染状态在地形渲染器中不触发该问题，因为地形每个 tile 使用唯一纹理（不重复绑定）。当尝试单纹理、按 material 排序等方法后，发现问题的根因与 NVIDIA SM4 硬件暴露的 `MAX_COMBINED_TEXTURE_IMAGE_UNITS`（96–192 个）有关：NVIDIA 的驱动在该缓冲内跟踪所有绑定状态，频繁变更会触发某种内部同步或状态校验。

AMD 的 `MAX_COMBINED_TEXTURE_IMAGE_UNITS` 仅 32 个（符合 GL3.3 最低规格 48 个），因此不受同等影响。

## 解决方案：Texture Bind Groups

核心思路：**一次性把场景内所有纹理绑定到不同 unit，整帧不再重新绑定，用 uniform 传递当前 mesh 使用哪个 unit**。

具体步骤：

1. 帧初始化时将所有纹理绑定到连续的 texture unit（NVIDIA 可达 160+ 个）。
2. 对每个 mesh，仅调用一次 `glUniform1iv` 传递该 mesh 所用纹理的 unit 索引。
3. Shader 内用索引采样，无额外绑定调用。

对于 AMD（只有 32 个 unit），采用"分组"策略：按 `MAX_COMBINED_TEXTURE_IMAGE_UNITS - 其他占用` 个 unit 切分 mesh 组，每组内不绑定纹理，组间才切换绑定——比逐 mesh 绑定大幅减少绑定次数。

## 性能对比（NVIDIA GTX 460，400k tris / 250 meshes / 42 纹理）

| 方案 | NVIDIA (ms) | AMD (ms) |
|------|------------|---------|
| 无排序，逐 mesh 绑定 | 15.0 | 5.0 |
| 单纹理 baseline | 3.3 | 4.0 |
| 按 material 排序 | 6.8 | 4.3 |
| **Texture Bind Group** | **3.36** | **4.1** |

Bind Group 在 NVIDIA 上达到接近单纹理的最优性能，在 AMD 上也优于按材质排序版本。

## 与 Bindless Rendering 的关系

这是到达 [[bindless-rendering]] 之前的一个工程妥协路线：在不支持 bindless 扩展的旧硬件上（2012 年的 GL3.3 环境），通过将所有纹理预绑定到连续 unit 来模拟"绑定一次、按索引访问"的语义。现代 bindless 通过 `GL_ARB_bindless_texture` 或 Vulkan descriptor indexing 可以更彻底地解决同类问题。

## 相关

- [[bindless-rendering]] — 真正的无绑定资源访问，现代 GPU 的彻底解决方案
- [[draw-call]] — 纹理绑定是 draw call 开销的重要组成部分
- [[batching]] — 减少状态切换的更广泛策略

## Sources

- [[sources/outerra-texture-bind-perf]]
