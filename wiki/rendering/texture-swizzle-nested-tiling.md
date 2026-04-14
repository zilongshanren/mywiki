---
tags: [纹理, gpu, 内存布局, morton, cache, 位运算]
date: 2026-04-14
sources: 1
---

# 纹理 swizzle 与嵌套分块的「减-与」增量

GPU 为什么不按 `y * stride + x` 这种行主序存纹理？因为按行主序走一列时，每一个像素都落在不同的 cache line，拿一次纹理就等于错 miss 一次 [[memory-hierarchy|缓存层级]]。**分块（tiling）**和**swizzle**是硬件层对这个问题的统一回答：打乱像素在内存里的位置，让空间上相邻的像素在地址上也相邻。[[fabian-giesen|ryg]] 这篇文章把各家 GPU 的常见 swizzle 模式归纳为「嵌套分块 + 位交错」，并给出一个只用一次 `sub` + 一次 `and` 就能在任意 swizzle 模式下沿 x / y 增量更新像素地址的软件通用解法。

## 三层思想

**分块（tiling）**：把图像切成 `M × N`（M, N 都是 2 的幂）的小矩形；每个小块在内存里连续，`widthInTiles * (tileW * tileH)` 就是一行的 stride。4×4 的 32bpp tile 刚好一行 cache line，向任意方向走 4 像素都不会踩出去。

**swizzle**：把像素的线性地址表达成各坐标 bit 的排列。行主序是 `[y_hi ... y_lo | x_hi ... x_lo | c1 c0]`；4×4 tile 相当于把 x、y 的低两位挪到 `c` 上方；Morton / Z 序则是把 x 和 y 的每一位完全交错。硬件实现层面没有额外逻辑——只是布线。你甚至可以看到更怪的模式：低位 Morton、中间夹一段 channel bits、高位又塞入 x 和 y 的另外几位。

**嵌套分块**：任意「保序交错」（即 x bits 内部和 y bits 内部顺序不变）的 swizzle 都可以理解成**一层套一层的 tile**。Morton 序是 2×2 嵌在 4×2 嵌在 4×4……一直嵌上去的极端情形。这个视角在两件事上非常好用：一是**非正方形**的 2 的幂纹理——`W × H` 纹理 `(W > H)` 可以自然地用 `H × H` 顶层 tile 加 Morton 序，不再需要 pad 成正方形的浪费布局；二是**非 2 的幂**尺寸——顶层 tile 以下照原 swizzle 做，顶层以上退化回行主序。

## 关键技巧：带「位空洞」的进位传播

软件里做 swizzle 最麻烦的是：沿 x 方向走一步，需要「递增 x bits 的同时让进位跨过 y bits 的空洞」。Morton 序下人们常用一系列 bit-interleave 魔数把 x 展开到交错位置；ryg 的观察是可以**用加法本身承担这件事**——只要你预先在所有「y 空洞」上填 1。

形式上，设 `x_mask` 是所有 x bits 为 1 的掩码，`y_mask` 同理，两者不相交。沿 x 增量一步：

```c
offs_x = (offs_x - x_mask) & x_mask;
```

`- x_mask` 等价于 `+ (~x_mask + 1)`；`~x_mask` 在所有空洞位上恰好是 1；`+1` 从最低位出发，传播到第一个 x 位时恰好变成了 `... x0++`；这之后每一次 x bit 的进位都会跑过一段全 1 的 y bits 空洞，再进入下一个 x bit；最后一次 `& x_mask` 把空洞里的垃圾清零。换句话说，这条公式直接把「沿任意嵌套 swizzle 模式的 x 方向走一步」压缩成两条指令，并且对 Morton、4×4 tile、任意 nested tile 的模式**完全通用**——只需要换 `x_mask`。

y 方向同理。总的地址可以写成 `dest + offs_y + offs_x`，因为 x 和 y 的 bit 不相交，加法等价于按位或；而选择加法的好处是可以把 `(dest + offs_y)` 在外层循环里一次算好，再在内层循环里和 `offs_x` 相加。对应的 PowerPC 内循环可以压缩到 4 条指令：`lwzu, subf, stwx, and`。

## 写 cache line 对齐 + 源顺序遍历

另一个实现细节是：swizzle 后的纹理往往在 **non-cached write-combined** 内存里——写入时只要**以 cache line 为单位**做就不会付非顺序写的代价，所以内层循环一次处理一个 cache line 大小的目标 tile（4×4 或 8×4）。外层循环则按**源纹理的线性顺序**遍历（方便处理 dirty rect 增量更新），每走到一个 4×4 / 8×4 子块就 shuffle 一把，写一整行 cache line 出去。非 2 的幂尺寸下，x 掩码包含顶层 tile index，走到右边界时 tile index 就会自动加一；y 跨越顶层 tile 行时补一次 `tilesPerRow` 的加法就够了。

## 为什么值得记

ryg 这篇文章最后成了 Intel 4th-Gen Core Graphics Developer's Guide 里共享 GPU/CPU 资源访问的推荐实现。它本质上是把一条**纹理映射内循环的老行话**（「把 bit field 拆开、用 1 填洞让进位跨过去」）第一次写清楚，并推广到任意嵌套 swizzle——不再限定在 Morton 序或 `x * stride + y` 这种简单情形。等价的技巧同样适用于 Morton-order 矩阵（BLAS tiling 里也在用），以及 3D 体纹理（`offs_x` + `offs_y` + `offs_z` 三路都用同一套 `-mask & mask` 的更新）。

## 和其他话题的连线

- [[cache-friendliness]]：这是在物理内存布局层解决 cache line 对齐/ spatial locality 的典型案例。
- [[memory-hierarchy]] / [[gpu-latency-hiding]]：为什么纹理读为了 cache，要付出这么复杂的地址计算。
- [[gpu-hazard-tracking]]、[[d3d12-resource-binding]]：桌面驱动通常会替你做 swizzle；这篇讲的是需要上层手动走 swizzle 的低层 / 嵌入式场景（Vivante "supertiling" 等）。
- [[bits-and-context]]：位运算层面的「空位填 1 让进位跨越」与位流 reader 里的技巧同源。

## 相关

- [[fabian-giesen]]
- [[cache-friendliness]]
- [[memory-hierarchy]]
- [[hierarchical-z-buffer]]
- [[tbdr-vs-imr]]
- [[locality-principle]]

## Sources

- [[sources/ryg-texture-tiling-and-swizzling]]
