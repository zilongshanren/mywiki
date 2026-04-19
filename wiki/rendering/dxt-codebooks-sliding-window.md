---
tags: [dxt, texture-compression, codebook, lzma, zeng]
date: 2026-04-14
sources: 1
---

# DXT Codebooks 与 Sliding Window（滑窗码表）

DXT 纹理的无损二次压缩里有几条"路人皆知"的套路。Jon Olick 在 Firefall 早期实验阶段比过三种基线：

1. 原始 DXT 数据直接 LZMA；
2. 对 DXT 数据做 **transpose**（把各块的端点聚在一起、选择位聚在一起）再 LZMA；
3. 颜色线做 Golomb + PNG 风 DPCM、选择位走原始 bit，再 LZMA。

大多数情况下 (2) 胜出，(1) 在 trivial 纹理上更好，(3) 在某些巧合的数据分布上能捡漏。三种方法都不新，相关原理见 crunch 与 Zeng 的研究。

**Zeng codebook 优化**：一种公开已久的调色板重排技术，通过重排调色板项让相邻像素的 delta 最小，后续再套 delta 编码 + zip / Golomb（信息论最优）。降 delta 熵等价于降二次压缩器的工作量。

**Sliding window codebook** 则解决了"码表比 8-bit 索引能表示的还大"的老问题：任何时候索引第 256 项，码表窗口左移一格、掉掉最末元素。这样即使码表大小 > 256，索引仍恒为 8 bit。代价是码表里会出现重复项；但只要索引次数远大于码表条目数，净收益为正。

Olick 在此基础上提出一个扩展：把第 256 项改成"转义"——后跟一字节显式指定新项插入到窗口的哪个位置。这样有两个意义：

- **可做非贪心优化**：能像 Zeng 那样重排码表位置以提高压缩率；
- **掌控条目生命周期**：条目插入的位置直接决定它会在窗口里存活多久。牺牲两个码表位（255 = 追加、256 = 带位置插入）就能把两种策略叠起来，用位置去权衡"条目存活窗口"和"索引序列可压缩性"。

这一串想法后来在 [[dxt-entropy-reduction]] 的 Part 4 被放弃了——Olick 在数据上实测发现，对 Firefall 的资产而言，码表/滑窗/delta 这些手段对 LZMA 的增益几乎可以忽略，瓶颈全在 selection bits 的熵上。但作为小 payload 的通用字典压缩技巧，它们仍是值得留在工具箱的。

## Sources

- [[sources/jonolick-dxt-codebooks-sliding-windows]]
