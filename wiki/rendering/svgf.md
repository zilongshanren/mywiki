---
tags: [渲染, 光线追踪, 去噪, svgf, 时域滤波, 方差引导]
date: 2026-04-27
sources: 1
---

# SVGF 与 A-SVGF — 时空方差引导滤波

**Spatio-Temporal Variance Guided Filter（SVGF）**由 Christoph Schied 于 2017 年提出，是实时光追去噪领域最广泛部署的算法之一，Quake 2 RTX 和 Minecraft RTX 均以其为基础降噪方案。Control 游戏也使用了 SVGF 的变体（见 [[rendering/northlight-frame-analysis]]）。

## SVGF 核心流程

SVGF 将时空重投影与方差驱动的双边滤波合并为一个反馈回路：

1. **时空重投影**：利用速度缓冲将上一帧样本投影到当前帧，通过比较法线/深度/物体 ID 判断是否可以复用。
2. **历史长度追踪**：`histLen` 记录一个像素成功累积的帧数，用于驱动 `accumulationFactor`（当前样本占最终辐照度的权重比例）。
3. **方差估计**：以 3×3 高斯核计算辐照度均值及其平方均值，差值即为空间方差。
4. **À-Trous 双边滤波**：以法线、深度、网格 ID 为权重，重复 3–5 次逐步缩小步长（按 2 的幂递减）。

## A-SVGF 改进

**Adaptive SVGF（A-SVGF）**（Schied et al., 2018）引入**动量缓冲区（Moment Buffer）**，将"方差变化量"作为比历史长度更可靠的累积因子启发量：不再靠成功重投影次数，而是靠亮度变化量来决定用多少历史样本。此举减少了快速运动或场景切换时的时域滞后，代价是引入了动量缓冲区的额外存储。

方差估计核心代码（简化自 Schied 实现）：

```hlsl
float2 moment = tMomentPrev.Load(ipos).rg;
// ... 7×7 高斯核加权累积 ...
float variance = (1.0 + 2.0 * (1.0 - histlen)) *
                 max(0.0, moment.y - moment.x * moment.x);
```

## 已知局限

- **时域滞后（Temporal Lag）**：高累积历史样本区域与新出现区域之间存在亮度差，在游戏中偶尔可见。
- **运动物体/遮挡变化**：重投影失败时质量退化明显；通过增加当前帧采样数（暗区用 2 spp）可部分缓解。
- A-SVGF 的动量缓冲区减少了滞后但无法完全消除。

## Sources

- [[sources/alain-rt-denoising]]
