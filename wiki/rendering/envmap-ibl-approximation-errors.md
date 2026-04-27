---
tags: [rendering, ibl, physically-based-shading, cubemap, brdf, approximation]
date: 2026-04-27
sources: 1
---

# 环境贴图 IBL 近似误差清单

基于 cubemap 的实时 IBL（Image-Based Lighting）流程在实践中包含多层近似假设。理解每一层误差的来源有助于在性能约束下做出有依据的权衡，并在需要时选择有针对性的修正方案。

## 标准流程回顾

1. 烘焙（或实时捕获）一张 radiance cubemap
2. 用 cosine 核卷积得到漫反射 irradiance cubemap
3. 用不同粗糙度的 Phong 核卷积 mip 链，得到镜面预过滤 cubemap
4. 运行时：漫反射用法线采样，镜面用反射向量 + roughness 对应 mip 采样
5. split-sum 修正（[[rendering/split-sum-approximation]]）：用预积分 FG LUT 补偿 Fresnel + G 项

## 误差来源逐项分析

### 1. 反射向量 ≠ 半程向量

cubemap 卷积以反射向量 R 为中心，但 Cook-Torrance BRDF 以半程向量 H 为中心。当掠角较大（H ≠ N）时，波瓣被拉伸并不再径向对称，而以 R 为中心的径向对称卷积无法准确描述这一形状。

**实践建议**：roughness 在掠角需要做一个简单的常量修正（`roughness_corrected = roughness + offset`），记得做。

### 2. BRDF 波瓣中心被 Fresnel / G 项推移

Fresnel 和几何遮蔽函数不仅缩放 BRDF，还会将有效波瓣中心推离反射向量。Split-sum 方案用 bias 修正了最主要的差异，但并非精确。更精确的做法是存储一张 3D 纹理（参数：V·N、roughness、F0），编码最优 lobe 朝向和形状。

### 3. 遮挡在预过滤后处理——错误

任何在预过滤 cubemap 后再乘以 AO 因子的做法都不正确，因为遮挡应发生在积分之前。正确做法的近似：

- Screen-space 或 voxel 追踪的锥形 AO，沿反射向量方向发射（即使不考虑 roughness）
- 另一选项：renormalization（Black Ops 2 / Lazarov 方案），对平均遮挡方向重新归一化 cubemap 贡献

### 4. 捕获位置误差（视差）

cubemap 从单一点捕获，用于其他位置时存在视差误差。缓解方案是 parallax-corrected cubemap（[[rendering/parallax-corrected-cubemap]]），用盒体/球体 reprojection 调整采样向量。但这同时扭曲了预卷积的假设——卷积核在重投影后不再保持原来的形状。

### 5. 法线方差未传入镜面 roughness

强制指定 mip level（`texCubeLod`）阻止了硬件对法线变化的自动抗锯齿。正确流程是把像素内的法线方差（通过 ddx/ddy 或 LEAN 映射估计）推入 roughness。

然而这本身也有问题：法线锥的精确积分会产生比同等 roughness 原始 BRDF 更"平坦"的高光，即不存在能精确匹配的等效 roughness。仍应执行此操作，但需了解其局限性。

### 6. 镜面波瓣未截断到半球

径向对称卷积没有将波瓣截断在表面法线半球内，导致掠角处的 Fresnel 计算受到影响。类似于面积光积分中未对光源几何体做 horizon clipping 的问题。理论修正：将反射向量向半球内部偏移，并缩放（fit to clipped lobe）。

### 7. 旧硬件 / 压缩格式的边缘不连续

DX9 时代部分硬件不支持跨 cubemap face 的双线性过滤，需要手动复制边缘纹素。但若使用 DXT/BCn 压缩，block boundary 会再次引入不连续，需要确保边缘 block 的 reference color 一致。即使现代硬件支持跨 face 过滤，底层实现可能走慢路径；**避免使用最小几级 mip**（分辨率太低，误差显著）。

## 实践优先级

| 误差 | 修正难度 | 视觉影响 | 推荐优先级 |
|------|---------|---------|-----------|
| 反射向量 ≠ H + roughness 修正 | 极低（一行代码） | 中 | **必做** |
| Split-sum FG LUT | 低 | 高 | **必做** |
| 法线方差 → roughness | 低 | 中-高（高频几何） | **必做** |
| 遮挡（锥形 AO 或 renorm） | 中 | 高（室内） | 推荐 |
| Parallax correction | 中 | 高（室内近距离） | 推荐 |
| 波瓣截断 | 高 | 低-中 | 视项目需求 |

## 验证方法

用 importance sampling 对未过滤 cubemap 做多次 tap 生成参考图，与预过滤结果对比，是量化误差的可靠手段。运行时可作为调试模式慢速参考渲染器使用。

## Sources

- [[sources/c0de517e-envmap-wrong]]
- [[sources/c0de517e-parallax-corrected-followup]]
