---
tags: [渲染, 光线追踪, 去噪, denoising, svgf, restir, 机器学习, 时域]
date: 2026-04-27
sources: 1
---

# 实时光追去噪技术综述

蒙特卡洛光线追踪依赖累积随机样本来逼近场景的正确渲染结果，天然存在高方差噪声。实时场景受算力限制往往只能用极低的每像素采样数（1–2 spp），去噪因此成为实时光追管线中不可绕开的一环。[[people/alain-galvan|Alain Galvan]] 2020 年对该领域做了系统性梳理，将去噪方案分为四大类。

## 四类去噪方案

### 1. 滤波（Filtering）

高斯、双边、À-Trous、引导滤波等核心在于对高方差区域做模糊，代价是损失高频细节。**À-Trous 双边滤波**用跳步采样覆盖比 5×5 核更大的有效半径，同时以法线/深度/物体 ID 等 G-Buffer 特征引导边缘保留，可重复 3–5 次逐步缩小 `stepWidth`（每次除以 2）。

特征缓冲区（G-Buffer attachments）通常包括：法线、反照率、深度/位置、物体 ID，以及专用的首次反弹数据、重投影路径长度等。

### 2. 时空重投影（Spatio-Temporal Reprojection）

将前帧样本投影到当前帧加以复用。核心依赖**速度缓冲区（Velocity Buffer）**——记录每个顶点在 NDC 空间的帧间位移：

```hlsl
float3 ndc = inPosition.xyz / inPosition.w;
float3 ndcPrev = inPositionPrev.xyz / inPositionPrev.w;
outVelocity = ndc.xy - ndcPrev.xy;
```

重投影时需要判断遮挡变化，方法是比较当前帧与重投影位置的法线/深度/物体 ID，失败则放弃历史样本。

**历史缓冲区（History Buffer）**记录样本的累积时长，用于驱动累积权重或估计方差。

### 3. 采样改进（Sampling）

**SVGF**（Spatio-Temporal Variance Guided Filter，[[rendering/svgf|SVGF]]）是时空重投影 + 方差引导 À-Trous 滤波的组合，是当前商业实现（Quake 2 RTX、Minecraft RTX）的基础。**A-SVGF** 增加了"动量缓冲区（Moment Buffer）"，用方差变化量代替历史长度来驱动累积比例，减少时域滞后。

**ReSTIR**（[[rendering/restir-di-math|ReSTIR DI]]）将时空重投影提前到采样阶段，通过复用邻近像素的采样概率统计来优化多光源直接光照，实现了数量级上的采样效率提升。

### 4. 近似缓存（Approximation Techniques）

RTXGI 用光探针离线预计算场景辐照度，通过光追更新探针的辐照度，避免实时蒙特卡洛积分，可与屏幕空间技术叠加使用。NeRF 类方法将辐射信息编码到神经场，用于近似视角相关效果如反射，或直接对场景降噪。

## 机器学习去噪

**去噪自编码器（Denoising Autoencoder）**，如 Intel OIDN 和 NVIDIA Optix 7 降噪器，接受带噪图像、法线、反照率为输入，输出滤波后图像。OIDN 和 Optix 在同等质量下速度优先级不同（Optix 更快但质量略低）。

**DLSS（Deep Learning Super Sampling）**将低分辨率渲染结果超分到目标分辨率（如 1080p → 4K），DLSS 3.5 进一步整合了 Ray Reconstruction（神经网络驱动的去噪 + 超采样）。

## 理想降噪管线设计

Galvan 总结的最优管线骨架：

1. **预通道（Prepass）** — 写 G-Buffer（法线、反照率、深度）、速度缓冲
2. **光追通道** — 自适应采样（AI 采样图驱动，高亮/阴影区域多采样），反射/GI/AO 分通道
3. **时空积累** — 重投影 + 历史缓冲 + ReSTIR 重要性重采样
4. **统计分析** — 方差估计、火球剔除（Firefly Rejection）
5. **滤波** — À-Trous 双边滤波 × 3–5 次，或 ML 自编码器
6. **历史写回** — 保存预通道数据供下帧重投影

## Sources

- [[sources/alain-rt-denoising]]
