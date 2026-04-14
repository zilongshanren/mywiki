---
tags: [source, gpgpu, parsing, 并行算法]
date: 2026-04-14
sources: 1
---

# A sketch of string unescaping on GPGPU（Raph Levien 2018）

[[raph-linus]] 2018 年 4 月的一篇短 post，用 JSON 字符串反转义做例子，展示"看起来必须串行的 parsing"其实可以拆成 GPU 友好的 parallel prefix sum。

## 摘要

文章的核心论点是：**一个状态机完全可以被改写成 monoid 同态，从而被 parallel scan 高效并行化**。Raph 用 JSON 字符串反转义的四状态机（外/内/转义后/错）做具体例子：把每个输入字符 map 到一个"从状态到状态的函数"——四状态下只有 64 种这样的函数、可以压缩到一个字节表达。函数复合 `compose(a, b)[i] = b[a[i]]` 是关联的（但不交换），配上一个 identity `(0, 1, 2)`，就构成一个完整 monoid。于是"这个字符所在位置的当前状态"可以通过对这些函数做 prefix scan 一次性全量计算——CUDA 的 Thrust 库直接提供了 `transform_inclusive_scan`。反转义的第二半是丢掉非 state-1 字符，这是经典的 stream compaction：打 0/1 标签做 prefix sum 得到目标下标，然后 scatter。原型在 GTX 1060 上测到约 4 GB/s，相比 scalar CPU 约 20 倍加速，瓶颈是全局内存带宽。文章结尾坦白："这不算实用的证据，但算一个有意思的思想实验"。

## 关键要点

- **状态机 → monoid 同态** 是通用技巧，来源是 Dan Piponi 2009 年关于"用 monoid 做增量正则匹配"的 blog
- **四状态 → 256 函数 → 实际 64 个**（因为错误状态总是吸收态），一个字节就够表达
- Raph 指出**同一个技巧在 xi-editor 的 rope 里用于 O(log n) 增量**（offset ↔ line number），这里用于 O(log n) 并行——同一抽象，两种性能目标
- CUDA **Thrust `transform_inclusive_scan`** 把 "map + scan" 一次搞定
- 瓶颈分析：scatter 吃全局内存带宽；优化方向是 tile 化 + shared memory 本地处理
- 作者自评：**证明了可行，没证明实用**——scalar CPU 还能用 SIMD 打大，对比不公平

## 链接到的概念

- [[gpgpu-string-unescaping]]
- [[raph-linus]]
- [[cuda-memory-hierarchy]]
- [[functions-as-vectors]]

## 原文

- 链接：https://raphlinus.github.io/personal/2018/04/25/gpu-unescaping.html
- 本地：`raw/articles/raphlinus.github.io/2018-04-25_a-sketch-of-string-unescaping-on-gpgpu.md`
