---
tags: [source, rendering, texture-compression, dxt, lzma, entropy, firefall]
date: 2026-04-14
sources: 1
---

# DXT compression - part 4 - Entropy（Jon Olick, 2013）

[[jon-olick]] 的 DXT 压缩系列第 4 篇（标注 Jason Hughes 协作），发表于 2013 年 8 月，系列目前的收官之作。

## 摘要

这是整个系列最有干货的一篇。Olick 给出了把 Firefall 纹理从 2.5 bpp 压到 1.5 bpp 而画质近乎无损的算法。关键实测发现：LZMA(DXT5) 的压缩瓶颈不在颜色/alpha 端点（只占 25% 体积），而在 **selection bits**（占 75%）。他用一个简单的 rate–distortion 替换流程——为每个块找频次排序前 N 名候选选择位里 MSE 最低者，失败则退化为贪心——把整体码率压到 **1.51 bpp、MSE 0.64**。参数 `greedyAfter` 用 9 次二分搜索迭代命中目标 MSE。同一函数共用于颜色与 alpha 选择位。对比 Rich Geldreich 的 crunch 库：同码率下 MSE 差 4.3 倍，速度差 16 倍以上（15 分钟 vs 4~24 小时）。文末给出一长串可以继续走的改进方向。

## 关键要点

- selection bits 占 LZMA 后体积 75%，是压缩的真正瓶颈。
- 降熵 = 把罕见选择位替换成高频选择位，受 MSE 上限约束。
- 算法两段式：top-N 最优候选 + 贪心回退；外层二分搜 `greedyAfter` 命中全局 MSE 目标。
- 实测 1.51 bpp / MSE 0.64 / 21.19:1 压缩比；crunch 同码率下 MSE 2.77~6.92。
- 速度：15 min（本方法，单线程，2.6 GB）vs 4~24 h（crunch）。
- 改进方向：非贪心 rate–distortion、同时优化端点与选择位、fabricate 新选择位、针对 LZMA literal coder 建模、感知度量替代 MSE。
- Firefall 在后续补丁中投入使用，流媒体加载显著改善。

## 链接到的概念

- [[jon-olick]]
- [[dxt-entropy-reduction]]
- [[dxt-codebooks-sliding-window]]

## 原文

- 链接：https://www.jonolick.com/home/dxt-compression-part-4-entropy
- 本地：`raw/articles/jonolick.com/2013-08-16_dxt-compression-part-4-entropy.md`
