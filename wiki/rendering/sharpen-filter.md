---
tags: [rendering, post-processing, image-filter, sharpening]
date: 2026-04-19
sources: 1
---

# 锐化后处理（Sharpen Filter）

锐化是把图像高频分量放大的线性滤波：原图减去自身的低通版本得到"细节层"，按系数加回原图，边缘被强化、观感变"脆"。在实时后处理里常作为时域抗锯齿 / DLSS / FSR 之后的补偿步骤，或者用来在低分辨率渲染 + 上采样后"找回锐度"。

## 最简单的 unsharp mask 公式

```
out = original + k * (original - blur(original))
```

这里 `k` 就是 Ilett 在 *Snapshot Shaders Pro* Sharpen 效果里暴露的 **Intensity** 参数——`k = 0` 原图不变，`k` 越大边缘越硬。`blur(original)` 的成本决定了整条效果的代价：最便宜的是 3×3 box，稍好是两次 [[convolution-separability-blur|可分离高斯]]。

等价地可以写成一次 3×3 卷积 kernel（Laplacian + 1 在中心）：

```
 0  -1   0
-1   5  -1
 0  -1   0
```

这正是 [[image-convolution-kernel]] 里经典的 sharpen kernel——把中心权重拉到 `1 + 4k`、四邻权重拉到 `-k`，和上面的 unsharp mask 是同一个东西的两种写法。

## 为什么实时引擎还要再做一次锐化

1. **上采样后补偿**：DRS / FSR1 / TAAU 的输出天然偏糊，最后走一遍 sharpen 或 CAS（Contrast-Adaptive Sharpening）把细节拿回来。
2. **TAA 破坏**：TAA 的历史帧 blending 会把高频吃掉，sharpen 是常规补偿。
3. **风格化**：配合 [[crt-shader-effects|CRT]] / [[color-quantization-retro|色阶量化]] 等复古 post，可以让像素边缘更硬、更"数码"。

## 实践注意

- **过锐化会放大噪点与 artifact**：sharpen 对噪声和 TAA ghost 同样敏感，调参看的是"边缘锐度 vs 噪点"的 tradeoff。
- **放在色调映射哪一侧**：通常锐化在 linear HDR 空间或线性 SDR 空间做，放在 tonemap 之前更稳；在 gamma 空间做会把亮部细节过度放大。
- **和 [[chromatic-aberration-post]] / film grain 的顺序**：sharpen 一般排在最后几个节点，靠近输出端。

## 相关

- [[image-convolution-kernel]] —— 3×3 Laplacian + 中心权 = sharpen kernel 的卷积表达
- [[convolution-separability-blur]] —— unsharp mask 依赖的高斯低通
- [[kuwahara-filter]] —— 风格化"保边"滤波，和 sharpen 是两条正交的图像处理路线
- [[urp-volume-post-processing]] —— 在 URP Volume 里做成 override 的集成位置
- [[dynamic-resolution-scaling]] —— 上采样后补锐化的典型搭配

## Sources

- [[sources/danielilett-snapshot-pro-sharpen]]
