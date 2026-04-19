---
tags: [source, 压缩, oodle, kraken, ps5, rdo]
date: 2026-04-14
sources: 1
---

# Oodle, Kraken etc. misconceptions（fgiesen / Fabian Giesen）

[[fabian-giesen]] 2024 年 8 月发表的澄清文：作为 Oodle 核心作者之一，系统性纠正网上关于 Oodle Data、Oodle Network、Oodle Texture 三条产品线常被混淆的说法，以及"PS5 游戏比 PS4 小是因为 Kraken"这个流行误解。

## 摘要

Oodle 不是一个算法而是三条互不重叠的产品线：Oodle Data（对标 Deflate/Zstd/LZ4，内部有 Kraken/Mermaid/Selkie/Leviathan 四档解压速度 vs 压缩率）、Oodle Network（UDP 小包专用）、Oodle Texture（BCn GPU 纹理的 RDO 编码器）。Kraken 相对 Deflate 的典型压缩率提升是 10–15%，虽在无损界已是大新闻，但远不是外界传说的"砍半"。PS5 游戏包体比 PS4 小得多的主因并非 Kraken，而是 Sony 打包工具的**跨资源大段去重**：PS4 为机械盘避免 seek 会在光盘上重复摆多份相同资源，PS5 走 SSD 后这些重复可以被发现并消除——功劳归打包团队而非压缩算法。Oodle Texture RDO 的洞察则是让 BCn 编码器"意识到"下游会再过一次无损压缩、主动生成相邻块相似的编码，让磁盘体积常减半而 VRAM 占用保持不变。整篇强调区分"per-byte 熵编码收益"与"宏观去重收益"——二者数量级差 10 倍，被混为一谈是普遍错误。

## 关键要点

- Oodle 不是一个算法：Data / Network / Texture 三条独立产品线
- Kraken 对 Deflate 约 10–15% 压缩率提升，不是"砍半"
- PS5 游戏变小主因是**打包工具去重**，不是 Kraken 压缩算法
- 分清 per-byte 熵编码收益 vs 宏观去重收益
- Oodle Texture RDO：BCn 编码偏向"可被无损压缩吃掉"的模式，磁盘 ÷2、VRAM 不变
- 追求目标：RDO 输出的保真度"接近非 RDO 编码器"

## 链接到的概念

- [[oodle-compression-suite]]
- [[bc7-solid-color-encoding]]
- [[adaptive-arithmetic-coding]]

## 原文

- 链接：<https://fgiesen.wordpress.com/2024/08/08/oodle-kraken-etc-misconceptions/>
- 本地：`raw/articles/fgiesen.wordpress.com/2024-08-08_oodle-kraken-etc-misconceptions.md`
