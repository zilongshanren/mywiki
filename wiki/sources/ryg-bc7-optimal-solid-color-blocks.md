---
tags: [source, 渲染, 纹理压缩, bc7]
date: 2026-04-19
sources: 1
---

# BC7 optimal solid-color blocks（Fabian Giesen / ryg）

[[fabian-giesen|ryg]] 2024 年 11 月的短文，给 BC7 encoder 的"整 4×4 块都是同色"情形提供了一条精确且闭式的编码方案。

## 摘要

BC7 没有 ASTC 的 void-extent 专属模式，但 mode 5 的 RGB 7-bit 端点 + A 8-bit 端点 + 2-bit 索引已足够精确编码任意 8-bit RGBA。Alpha 用一个端点 + 索引 0 解决。RGB 通道：索引 0/3 只给 128 个取值，索引 1/2 以端点对称，故把所有索引设为 1 即可通过 21/64 权重的插值拿到第 256 个取值。闭式构造：`e0 = target >> 1; e1 = ((target < 128) ? (target+1) : (target-1)) >> 1`——两个 7-bit 端点送进 BC7 的 21/64 插值加 32 再右移 6 就严格等于 target。对所有 256 个输入穷举验证。Oodle Texture 所有 BC7 encoder 都用这段逻辑处理纯色块，RDO 效率尤其依赖这种**一致性**（连续 run 的编码不随机变化，熵编码才能压得紧）。

## 关键要点

- **Mode 5 的 mismatch 解法**：7-bit 端点 + 21/64 插值 = 精确覆盖 8-bit 全集。
- **索引 1 vs 索引 2 对称**：swap endpoints 等价，不增加选项。
- **一致性重要于"多种等价"**：run-length 场景下熵编码受益。
- **两行代码每通道**：无需 LUT、无数据依赖。

## 链接到的概念

- [[bc7-solid-color-blocks]]
- [[oodle-compression-suite]]
- [[fabian-giesen]]

## 原文

- 链接：https://fgiesen.wordpress.com/2024/11/03/bc7-optimal-solid-color-blocks/
- 本地：`raw/articles/fgiesen.wordpress.com/2024-11-03_bc7-optimal-solid-color-blocks.md`
