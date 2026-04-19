---
tags: [rendering, blur, math, post-processing]
date: 2026-04-19
sources: 1
---

# 卷积的可分离性与模糊优化

朴素的二维卷积模糊（[[image-convolution-kernel|卷积核]]）是一次 `N×N` 的 tap 操作，复杂度随半径 N 平方增长——大半径模糊一旦要做 64 像素的 kernel，单像素就得读 4096 次纹理，移动端直接崩。**可分离性（separability）** 是突破这条平方曲线的关键数学性质：如果一个 2D kernel 能写成两个 1D kernel 的外积（`K_2D(x,y) = K_x(x) · K_y(y)`），那么这个卷积就可以拆成两次 1D pass——先一个水平方向的 `N` tap pass，把结果写入中间 framebuffer，再来一个垂直方向的 `N` tap pass 读取中间结果。总 tap 数从 `N²` 降到 `2N`。

高斯函数恰好是为数不多的"天生可分离"连续分布之一（`G(x,y) = G(x) · G(y)`），所以 [[separable-gaussian-blur]] 是这个技巧的主要应用场景。Box Blur 同样可分离（均匀权重分布），因此实际工程中也常被写成两 pass。不过可分离并不是免费的——它要求至少一张等尺寸的中间 framebuffer、两个 draw call、两次 framebuffer 切换，在移动 GPU 的 tiling 架构上可能打碎 on-chip tile 缓存，实际收益并不总是线性的。

Frost Kiwi 在这篇博客里强调了一个被频繁忽略的细节：离开了朴素卷积的语义之后（例如用 [[bilinear-sample-blur-optimization|双线性采样]] 在像素之间读取），"kernel" 的概念变得模糊——[[kawase-blur]] 就不是严格的卷积，而是一系列"在像素中间"的 tap；它们在频域上依然做低通，但已经很难用一个固定权重矩阵去描述。这是从"严格数学卷积"走向"视觉等价的频域滤波"的关键转折点。

## Sources

- [[sources/frost-kiwi-video-game-blurs]]
