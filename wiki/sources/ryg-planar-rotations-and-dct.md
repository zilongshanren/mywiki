---
tags: [source, 压缩, dct, simd]
date: 2026-04-14
sources: 1
---

# Planar rotations and the DCT（Fabian Giesen）

[[fabian-giesen|ryg]] 2010 年 11 月在研究快速 DCT 算法时写下的一篇笔记，把平面旋转这一 DCT 的核心算子的四种实现并列陈列，并指出「乘法贵 / 加法便宜」「只看算术运算数」这两条经典假设在 FMA + SIMD 时代已经错位。

## 摘要

几乎所有快速 DCT 都分解为蝴蝶（butterfly）+ 平面旋转两类操作。蝴蝶没什么可优化，而旋转有四种写法：直接 2×2 矩阵乘法（2 FMA + 2 mul）；经典提取公因子（少一次乘，依赖链变长）；AA&N scaled rotation（把一个公共缩放因子吸收到后续蝴蝶里，2 条独立 FMA 就完成一次旋转）；三次剪切分解（long 依赖链但**整数可逆**，BinDCT 的基础，lifting 小波的同根生）。ryg 强调真正的瓶颈常常不是算术，而是 load / unpack / transpose / pack / store——Xbox 360 上 FMA 版 8×8 IDCT 一半时间都在数据搬运，但整段算下来 4.5 cycles/pixel，瓶颈已经转移到熵编码器：变长 shift 在 PPC / Cell 上慢且锁另一条硬件线程，而熵解码天生串行，与 H.265 之前所有多媒体格式的「单核解码」假设死锁在一起。评论区 ryg 本人补充了 Bink 2 后来为什么选「scaled but orthogonal」而不是 lifting：重度量化下 lifting 非正交性让 trellis 量化失效。

## 关键要点

- FMA 时代乘法和加法同价，经典 DCT 文献的「少一次乘」优化常常变成「加长依赖链」的陷阱。
- AA&N / scaled rotation 是浮点 SIMD + FMA 下最干净的选择，可以把 scale 因子向下游 butterfly 吸收。
- 三次剪切分解下旋转在截断整数下天然可逆，是 integer-to-integer DCT / 小波 lifting 的通用构造法。
- 定点实现反而怕乘法堆叠：每次乘法一次 round-off，会污染误差路径；Bink 2 最终选择 scaled-but-orthogonal 而非 lifting。
- IDCT 的 4.5 cycles/pixel 实测并不慢，但熵解码是串行的单核瓶颈，主流视频容器的架构都没给多核解码留接口。

## 链接到的概念

- [[planar-rotation-dct]]
- [[fabian-giesen]]
- [[adaptive-arithmetic-coding]]
- [[sse-tricks]]

## 原文

- 链接：https://fgiesen.wordpress.com/2010/11/05/planar-rotations-and-the-dct/
- 本地：`raw/articles/fgiesen.wordpress.com/2010-11-05_planar-rotations-and-the-dct.md`
