---
tags: [渲染, 光栅化, GPU, 优化]
date: 2026-04-14
sources: 1
---

# 分层光栅化（Hierarchical / Coarse Rasterization）

[[pineda-edge-rasterization|Pineda 边方程算法]] 把覆盖测试变成了大规模整数加法，但还有一个浪费：如果直接在三角形 bounding box 里逐 8×8 块测试，会有大量「64 次加法之后发现 0 个覆盖像素」的空块。**Coarse rasterization** 就是在 fine rasterizer 之前再放一个更粗粒度的剔除阶段，把这种浪费消掉。

## 思想：用边方程的极值剔除整块

每个 8×8 tile 上，三个边方程都是线性的，所以**最大值和最小值必然出现在 tile 的 4 个角点之一**——而且从 `a, b` 的符号就能判断是哪一个角。换言之：

1. 对一个 tile，只算一个角点的 `E` 即可知道整块的 `E` 上下界；
2. 如果某个 `E` 的最大值都为负，则整块全部在边外 → 可以直接剔除；
3. 如果三个 `E` 在 tile 上都「整体内部」，可以一次性 trivial accept。

这个判定本身用的还是几个并行整数加法器，硬件代价极低。整个 coarse rast 的「单位 work」是一个 tile，不是一个像素，所以 cull 同样工作量的空区域时它比 fine rast 便宜很多倍。

## 它和 fine rasterization 协作

- **coarse rast**：输入三角形，输出「可能被覆盖的 tile 列表」。每个被接受的 tile 顺便把角点 `E` 值传下去——fine rast 立刻就能用，省掉一次重算。
- **fine rast**：在每个候选 tile 内部跑 [[pineda-edge-rasterization|Pineda 算法]]，输出 64-bit 覆盖掩码，组织成 2×2 quad 喂给 [[fragment-shader|pixel shader]]。

可以再继续往上堆层级（Greene 1996、Abrash 在 Larrabee 上实现的「完全分层」），但桌面 GPU 通常只用 2 层就够：再多层会让小三角形的固定开销变高，而硬件的目标恰恰是「fine rast 已经能比 shader 更快地造像素了」。

## False positive

**lower-bound 测试有 false positive**：tile 的 `E` 上下界都过线、但实际上 tile 与三角形并不真相交时（典型情况是三角形的角剐到 tile 边缘），coarse rast 仍会接受这个 tile。代价是 fine rast 这次会 64 次加法都得到「全部不覆盖」。修正这种情况比直接做空 fine rast 还贵——所以硬件干脆放过。

## 与 tile-based renderer 的区别

注意：这里的「8×8 tile」**不是** [[tbdr-vs-imr|TBDR]] 中的「屏幕 tile」（通常 32×32 或更大）。TBDR 还要在所有几何到齐后做一次「ultra-coarse rast」（binning）来决定每个屏幕 tile 跑哪些三角形；那是另一层。Pineda + 2 层 coarse rast 描述的是「sort-last」桌面 GPU 架构。

## 相关

- [[pineda-edge-rasterization]]
- [[rasterization]]
- [[triangle-setup]]
- [[tbdr-vs-imr]]
- [[fabian-giesen]]

## Sources

- [[sources/ryg-trip-through-graphics-pipeline-2011-part-6]]
