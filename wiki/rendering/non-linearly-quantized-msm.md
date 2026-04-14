---
tags: [渲染, 阴影, 矩, 量化, compute-shader]
date: 2026-04-14
sources: 1
---

# 非线性量化矩阴影贴图（Non-linearly Quantized MSM）

**Non-linearly Quantized Moment Shadow Maps** 是 [[christoph-peters]] 在 HPG 2017 提出的对 [[moment-shadow-mapping|矩阴影贴图]] 存储格式的进一步压缩与改写。基础 MSM 在 16-bit `RGBA16_UNORM`（64 bits/texel）下已经很省，但因为四个原始幂矩 `(z, z², z³, z⁴)` 的取值之间存在强相关性，实际用于「区分阴影状态」的有效比特并不多——而舍入误差又必须用 bias 补偿，bias 一加，**漏光（light leaking）就被强化了一档**。这篇论文用一个**非线性变换**把四矩重新参数化为「更直接描述深度分布」的四个量，再做量化，于是 64 bits/texel 的非线性版本几乎和原版 128 bits/texel 不可区分，32 bits/texel 也只多了一点 banding。

## 关键观察：原始幂矩冗余

四个幂矩之间不是独立的：`z²` 必然介于 `z` 的某个区间内、`z³` 又被 `z, z²` 限制——它们的联合分布躺在一个非常瘦的「Hausdorff 矩流形」上。把它们当作四个独立通道做线性量化，就是在把比特预算分给一个「绝大多数取值都被禁止」的盒子。Peters 的非线性变换沿着这个流形重新选坐标，等价于**把存储空间紧贴在数据真正存在的低维曲面上**。

## 重建的副产品：更便宜

非线性参数化不是只对存储有利。原版 MSM 解码要先做 4×4 的反量化矩阵乘法、再 Cholesky、再三次方程；新参数化里有些步骤可以直接跳过——存的本来就更接近 Cholesky 之后的中间量。**重建的算术量净减少**，再加上更窄的 bias，在 GPU 上变成一个少见的「同时省带宽、省 ALU、省视觉漏光」的三赢改写。

## 32 位的代价

32 bits/texel 是这篇论文的「极限挑战」。在该精度下：

- **漏光基本不增加**——因为非线性变换把误差分配到了「人眼最不敏感的方向」；
- **banding 出现**——量化阶距开始大于「视觉上能察觉」的阈值，会在大面积平滑阴影上看出条带。

也就是说，32 位版本最适合「要么原本就有点 dithering / 噪声的场景，要么内存预算极度紧张的场景（VR、高分辨率移动端）」。论文给出了用 [[blue-noise-dithering|蓝噪声 dithering]] 来缓解 banding 的方案。

## On-chip filtering：用 compute shader 把所有事情锁在 LDS 里

非线性量化有一个**和硬件双线性滤波不兼容**的天然限制——quantize 和 dequantize 之间的非线性会让"先解码再混合"和"先混合再解码"得出不同的结果。Peters 的对策是把整个「MSAA resolve + 9² 两遍高斯模糊」打包进一个 compute shader：

- shadow map 以高精度（例如 32-bit float 或未量化的中间格式）渲染；
- compute shader 把整个 tile 拉进 **shared memory（LDS）**，在那里完成 MSAA resolve 与两遍 9-tap 高斯模糊；
- 模糊后的结果**在 LDS 里**做非线性量化，**最后只把量化后的小 footprint 写回 device memory 一次**。

这样一来：device-memory 带宽只在最后一步付一次量化后的代价；而最贵的 9² 高斯模糊**全程跑在 LDS 上**，硬件 cache 几乎闲着。Peters 报告这种「on-chip filtering」让非线性 MSM 的端到端帧时间**和 32 bits/texel 的 VSM 大致相当**——也就是说几乎免费拿到了 MSM 级的质量。

## 采样阶段：blue noise dithering 替代双线性

由于硬件 bilinear filter 不能用，shadow lookup 阶段需要一个等效物。Peters 的选择是**做 nearest sample + 蓝噪声 dithering**——每个像素根据预生成的 [[blue-noise-dithering|blue noise]] 偏移落在邻近 texel 之一。蓝噪声的高频特性使得「未滤波」的伪影在视觉上趋近于"均匀薄雾"而不是"锯齿"，对人眼非常友好，而且 cost 只是一次额外的纹理读 + 偏移 add，比软件 bilinear（4 次读 + 加权和）便宜。

## 在 MSM 家族里的位置

| 变体 | 存储 | 滤波 | 漏光 | 备注 |
|---|---|---|---|---|
| MSM（原版） | 128 bits | 硬件 bilinear/MSAA | 极小 | 质量上限 |
| MSM 16-bit 量化 | **64 bits** | 硬件 bilinear/MSAA | 小但需 bias | I3D 2015 默认 |
| **非线性 MSM** | **64 bits** | compute shader on-chip | **接近 128-bit 版本** | HPG 2017 |
| 非线性 MSM 极限 | **32 bits** | compute shader + dithering | 略增 + banding | HPG 2017 |

非线性 MSM 是 MSM 故事里"工程优化吃干抹净"的那一步：把储存格式从「四个独立通道」重写成「贴着信号流形的四个数」，把滤波从"硬件双线性"换成"片上 compute"，于是该方案在质量、带宽、ALU 三个方向同时再压一档。

## 相关

- [[moment-shadow-mapping]] — 母系工作
- [[christoph-peters]]
- [[shadow-mapping-basics]]
- [[blue-noise-dithering]]
- [[cubic-equation-solver-hlsl]] — 解码端的数值核心

## Sources

- [[sources/peters-non-linearly-quantized-msm]]
