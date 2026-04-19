---
tags: [source, 渲染, 纹理压缩, BC7]
date: 2026-04-19
sources: 1
---

# BC7 optimal solid-color blocks（Fabian Giesen / ryg）

[[fabian-giesen|ryg]] 2024 年 11 月的短文，给 BC7 encoder 处理「整 4×4 块都是同一颜色」这类 run-length 常见情形提供一条**无需查表、恒为精确、最短的编码方案**。

## 摘要

BC7 没有像 ASTC 那样的 void-extent 专属模式，但 mode 5（RGB 7 bit 端点 + A 8 bit 端点 + 每像素 2 bit 索引）足够承载 8-bit RGBA 的精确还原。Alpha 通道直接塞到端点 0，索引全 0 即可。颜色通道只要索引全 1，endpoint 之间用 BC7 规范的 21/64 权重插值，就能覆盖 [0, 255] 全部 256 个值。ryg 给出闭式 endpoint 构造：`e0 = target >> 1; e1 = ((target < 128) ? (target+1) : (target-1)) >> 1`——两个 7-bit 端点的平均（加上 21/64 的偏置）刚好等于目标 8-bit 值，**每个通道两条指令**搞定。这个构造对所有 256 个输入精确命中，RAD 的所有 BC7 编码器从 RDO 到 non-RDO 都用这同一套。

## 关键要点

- **Mode 5 是 BC7 处理纯色块的最佳选择**：RGB 端点 7 bit、Alpha 端点 8 bit，两通道独立编码。
- **索引全用 1 不是偶然**：index 0/3 只给出端点原值（7-bit dequantize 后只有 128 个候选），index 2 和 index 1 对称（swap endpoints）不添新选择，唯一能给 256 选项覆盖的就是 index 1。
- **闭式 endpoint**：对任意 target ∈ [0,255]，`(43·expand7(e0) + 21·expand7(e1) + 32) >> 6 == target` 的两端点解是 `e0 = target>>1, e1 = (target±1)>>1`，符号取决于 target 是否小于 128。
- **纯色块经常 run**：很多图里连续好几百块都是同一颜色，编码方案**一致**才能让 RDO / 后续熵编码充分利用冗余——不要在「几种都行」里随机挑。
- **对比 BC1**：BC1 里纯色块没法完全命中，还有 decoder spec 欠规范的历史包袱；BC7 没有任何一个。

## 链接到的概念

- [[bc7-solid-color-blocks]]
- [[oodle-compression-suite]]
- [[fabian-giesen]]

## 原文

- 链接：https://fgiesen.wordpress.com/2024/11/03/bc7-optimal-solid-color-blocks/
- 本地：`raw/articles/fgiesen.wordpress.com/2024-11-03_bc7-optimal-solid-color-blocks.md`
