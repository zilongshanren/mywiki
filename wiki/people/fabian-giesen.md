---
tags: [人物, 作者]
date: 2026-04-14
sources: 9
---

# Fabian "ryg" Giesen

**Fabian Giesen**（网名 **ryg**）是 RAD Game Tools / Epic 的资深程序员，长期博客 [The ryg blog](https://fgiesen.wordpress.com/) 是低层图形与压缩算法领域最受敬重的技术写作之一。他参与过 Bink、Oodle 等商用压缩 / 视频代码库的开发，与 Charles Bloom 是同事；早年还是 demoscene 团体 Farbrausch 的成员之一。

## 风格

- **从硬件出发解释抽象**：解释一个软件 trick 时，先讲它在 ALU、cache、流水线层面发生了什么。
- **数学不省**：从 IEEE 754 round-to-nearest 的精度证明，到 Pineda 边方程的整数加法器实现，全部展开。
- **对「过早优化」的态度反过来**：「if you've never measured, you've never optimized」——但一旦确实是热点，就钻到指令调度和 cache 行的层级。
- **历史感**：博客横跨 15 年，常常顺手提到一个东西在 80 年代 / 90 年代是怎么做的，以及为什么现在不那样做了。

## 代表作品

- **A Trip Through the Graphics Pipeline 2011** 系列：13 篇长文从 IA stage 一路写到 ROP，是公开材料里关于桌面 GPU 内部最细的描述之一。
- **rANS / FSE / ANS 系列文章**：把 Jarek Duda 的 ANS 理论翻译成可工程化的实现，并直接成为 Oodle Kraken / LZNA / Mermaid 的算法基础。
- **A Whirlwind Tour of Dataflow Graphs**、**SIMD transposes**、**Reading bits in far too many ways**：经典系列。

## 对本 wiki 的贡献

| 文章 | 贡献的概念 |
|---|---|
| Exact UNORM8 to float | [[unorm-float-conversion]] |
| sinc and Polynomial interpolation | [[sampling-theorem-sinc]] |
| SSE: mind the gap! | [[sse-tricks]] |
| A Trip Through the Graphics Pipeline 2011 Part 6 | [[pineda-edge-rasterization]]、[[hierarchical-rasterization]]、[[triangle-setup]] |
| Models for adaptive arithmetic coding | [[adaptive-arithmetic-coding]] |

## 相关

- [[rasterization]]
- [[rendering-pipeline]]
- [[unorm-float-conversion]]
- [[sse-tricks]]
- [[adaptive-arithmetic-coding]]
- [[cellular-texture-generation]]
- [[carry-save-adder-pixel-avg]]
- [[data-structure-invariants]]
- [[planar-rotation-dct]]
- [[ppc-int-float-lhs]]
- [[negative-space-in-programming]]
- [[ring-buffer-virtual-stream]]
- [[texture-swizzle-nested-tiling]]

## Sources

- [[sources/ryg-exact-unorm8-to-float]]
- [[sources/ryg-sinc-and-polynomial-interpolation]]
- [[sources/ryg-sse-mind-the-gap]]
- [[sources/ryg-trip-through-graphics-pipeline-2011-part-6]]
- [[sources/ryg-models-for-adaptive-arithmetic-coding]]
- [[sources/c0de517e-tiled-hardware-speculations]] —— 评论区给出 TBDR bin buffer / vertex split / in-order blending / triangle density 等硬件侧权威修正
- [[sources/ryg-cellular-textures-1]]
- [[sources/ryg-cellular-textures-2]]
- [[sources/ryg-carry-save-adders]]
- [[sources/ryg-data-structures-and-invariants]]
- [[sources/ryg-cycle-detection]]
- [[sources/ryg-64-bit-tidbits]]
- [[sources/ryg-view-frustum-culling]]
- [[sources/ryg-frustum-culling-notes]]
- [[sources/ryg-finish-your-derivations]]
- [[sources/ryg-planar-rotations-and-dct]]
- [[sources/ryg-more-ppc-compiler-babysitting]]
- [[sources/ryg-negative-space-in-programming]]
- [[sources/ryg-ring-buffers-and-queues]]
- [[sources/ryg-texture-tiling-and-swizzling]]
