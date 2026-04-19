---
tags: [dxt, texture-compression, entropy, lzma, firefall]
date: 2026-04-14
sources: 1
---

# DXT Entropy Reduction（降熵压缩 DXT 选择位）

DXT 纹理在磁盘上二次压缩的瓶颈并不在 color line / alpha line 这部分数据，而在每个 4×4 块的 **selection bits**（颜色与 alpha 的选择位）。Jon Olick 在 Firefall 的纹理管线上实测：LZMA 压完后 color/alpha selection bits 占 75% 体积，而 color/alpha line 只占 25%。真正要动的就是选择位。

核心 insight：选择位之所以难压，是因为它们的**熵（entropy）**太高——大量块出现频次极低。在一套 32×32×3 DXT5 块的样本里，900 种颜色选择位变体中有 600 种只出现了一次。只要能把这些罕见变体替换成更高频的变体，同时把均方误差（MSE，见 [[mrsse-hdr-error-metric]] 对 MSE 作为质量度量的讨论）控制在可接受范围内，整体码率就会大幅下降，因为 LZMA 的 LZ 部分能更高效地复用字典。

算法框架是一种 **rate–distortion** 贪心替换：

1. 扫全部块，建立 `uniqueBits[]` 表与频次 `uniqueBitsCnt[]`；
2. 按频次降序排序；
3. 对每个块，把它的选择位替换为频次排序前 N 位中 MSE 最小者；若都不满足阈值就退化成 **greedy**（接受第一个低于 `mseLimit` 的候选）。

参数 `greedyAfter`（top-N 窗口大小）与 `mseLimit`（单块 MSE 上限）共同控制 quality/bitrate trade-off。作者进一步用**二分搜索** `greedyAfter` 来命中一个目标整体 MSE（例如颜色 0.5、alpha 1.0），9 次迭代就能穿完 0-511 的搜索空间。同样的函数在代码里通过参数复用，既处理颜色选择位也处理 alpha 选择位。

**实测结果（Firefall Orbital Comm Tower 数据集，2.6 GB）**：

- 基线：LZMA(DXT5) ≈ 2.28 bpp（Part 2 结论）
- 本方法：**1.51 bpp，整体 MSE 0.64**，压缩比 21.19:1
- 极端：1.43 bpp，MSE 0.84（贪心但偶现渐变块状伪影）
- 编码时间 15 分钟（单线程）

对比 **crunch**（Rich Geldreich 出品，业内常用的 DXT rate–distortion 压缩库）：目标 1.51 bpp 时 crunch MSE 6.92（肉眼明显劣化）；退而求其次按 quality factor 调到 1.52 bpp 时 MSE 2.77，仍是本方法的 4.3 倍。更关键的是 crunch 全流程耗时 4~24 小时。Rich 后来澄清 crunch 设计目标是从源 RGB 而非已编码 DXT 出发，不完全是同一场景，但在 Firefall 这种"已经有现成 DXT 资产、只想再挤一轮磁盘空间"的管线里，直接改选择位的熵显然更对路。

剩下的改进方向都是现成的开口：用非贪心搜索（把 rate–distortion 当真正的 Lagrangian 去解）、同时优化 line 端点和选择位、**fabricate** 新的高频选择位（而不是只在既有池里挑）、针对 LZMA literal coder 分布做建模、改用比 MSE 更贴近感知的度量等。block 伪影主要出在低频渐变处，作者试过误差扩散没明显效果，降 MSE 目标是最稳的办法。

这套思路和 [[color-quantization-kmeans]]、[[color-quantization-retro]] 里的**码表优化**一脉相承，区别在于降熵对象是编码好的块索引而不是像素，rate–distortion loop 是外挂在已有 [[bc7-solid-color-blocks]] 风格的块压缩之外的二次流程。

## Sources

- [[sources/jonolick-dxt-part4-entropy]]
