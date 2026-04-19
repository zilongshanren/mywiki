---
tags: [rendering, blur, post-processing]
date: 2026-04-19
sources: 1
---

# Kawase Blur

**Kawase Blur** 由 Masaki Kawase 在 GDC 2003 的《Frame Buffer Postprocessing Effects in DOUBLE-S.T.E.A.L.》里首次公开，是对 [[separable-gaussian-blur]] 的一次重要精简。它把每个 pass 的采样数固定到**四个对角 tap**（4 次 `texture2D`），并利用硬件的 [[bilinear-sample-blur-optimization|双线性采样]]——把 tap 位置精确地放在 2×2 像素中心，让每次 texture 读取自然地等价于 4 个像素的均值。数学上这不是严格的高斯，但在频域上高度"高斯样"（Gaussian-like），在视觉上几乎看不出差别。

Kawase 的巧思在于：它放弃了"精确卷积"的幻想，转而承认**视觉上等价的低通滤波**才是游戏图形真正要的东西。为了继续扩大有效模糊半径，经典的 Kawase 做法是**链式多个 pass**，每个 pass 把 tap 偏移半径加大（0.5、1.5、2.5、…），这样总 tap 数随半径线性增长而不是平方增长，彻底解决了朴素 Box / Gaussian 在大半径时的带宽灾难。

Kawase 后来被 [[dual-kawase-blur]]（Bjørge 2015）进一步改造成金字塔式的下采样+上采样结构，这也是今天绝大多数游戏引擎和桌面合成器里实际跑的版本。

## Sources

- [[sources/frost-kiwi-video-game-blurs]]
