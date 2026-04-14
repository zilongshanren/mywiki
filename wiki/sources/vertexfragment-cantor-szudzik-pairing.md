---
tags: [source, math, algorithms, hashing, pairing-function]
date: 2026-04-14
sources: 1
---

# Pairing Functions: Cantor & Szudzik（Steven Sell / Vertex Fragment）

[[steven-sell]] 发表于 2019 年 5 月的 ramble，系统比较两种将 `(x, y)` 映射为唯一整数的经典配对函数。

## 摘要

配对函数 `pair(x, y) = z` 的任务是把两个值无歧义地打包成一个整数 id，作者曾在着色器、地图系统和实例化渲染器（参见 [[performance-conscious-webgl]]）中反复使用这类函数。文章对比 Cantor 与 Szudzik 两种实现。**Cantor** 按对角线扫描 2D 网格，公式 `(x+y)(x+y+1)/2 + y`，几何上优雅但打包效率只有 50%：`cantor(9,9) = 200` 而不是 99；落到 32 位有符号整数时，`cantor(33000, 33000)` 就溢出。**Szudzik** 按方框 L 形扫描，公式分两支：`x >= y ? x*x + x + y : y*y + x`；几何含义是“先填满边长为 max(x,y) 的方框再扩一层”，打包效率达到 100%，`szudzik(9,9) = 99` 恰好命中。32 位有符号可安全输入到 46340，无符号到 65535，空间比 Cantor 多近一倍。两者对负输入的支持都需要先做奇偶 Z 变换把负数折进正整数域，Szudzik 还有一种按符号组合把一半结果挪到负轴的改写以回收空间。性能上（jsperf）两者都在 8.8–8.9 亿 ops/sec 区间，Szudzik 以 <1% 的微弱优势胜出。作者强调：在两个值都有明确上界的情形下，Szudzik 的空间效率几乎总是更好的选择。

## 关键要点

- 配对函数是双射：给定 `(x, y)` 唯一得到 `z`，也可反解，这使它比哈希更严格
- Cantor 公式：`(x+y)(x+y+1)/2 + y`，对角线遍历；Szudzik 公式：`x>=y ? x*x+x+y : y*y+x`，方框 L 形遍历
- Szudzik 打包效率 100%，Cantor 50%；32 位整数场景下 Szudzik 的可用输入空间是 Cantor 的 2 倍
- Cantor 的溢出边界约为 (33000, 33000)，Szudzik 约为 (46340, 46340)
- 两者都要求非负输入，支持负数需先做 Z 变换；Szudzik 另有“按符号挪到负轴”的压缩变体
- 性能几乎一样（约 8.9 亿 ops/sec），Szudzik 微幅胜出
- 典型用途：`Map` key、着色器寻址、稀疏 2D 空间 id

## 链接到的概念

- [[cantor-szudzik-pairing]]
- [[performance-conscious-webgl]]
- [[non-cryptographic-hash]]
- [[steven-sell]]

## 原文

- 链接：https://www.vertexfragment.com/ramblings/cantor-szudzik-pairing-functions/
- 本地：`raw/articles/vertexfragment.com/2019-05-14_pairing-functions-cantor-szudzik.md`
- 参考：Szudzik, *An Elegant Pairing Function*; Wikipedia *Pairing function*
