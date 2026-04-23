---
tags: [source, rendering, hdr, bloom, indie]
date: 2026-04-19
sources: 1
---

# Overbright colours, blur and faking it（Joost van Dongen / Joost's Dev Blog）

[[joost-van-dongen]] 2010 年 9 月发表的文章，讲 *Proun* 如何在 8-bit UNorm framebuffer 上"伪装"HDR bloom：渲染时颜色乘 0.5 存进普通 8-bit RT、模糊 pass 在 8-bit 上跑、最后合成乘 2 还原。

## 摘要

8-bit UNorm framebuffer 会把亮度 > 255 的值全部 clamp 到 255——未模糊时监视器本来就显示不出区别，问题出在 **模糊**：亮度 255 和 400 的白区域在和黑区域做 blur 时行为应该不同，亮区应该"胀"到周围把暗细节吞掉，这是真 HDR bloom 的核心表现。硬件路线是打开 fp16 RT（实际是 16-bit float 每通道），代价是带宽 / blend 成本，对 2010 年的中低端显卡仍然显著。van Dongen 的 trick：所有颜色先乘 0.5 存进 8-bit RT（实际亮度 510 会存成 255 而不是被 clamp 成 255），模糊照常跑，最后合成乘 2。视觉上拿到 bloom 效果，上限被锁死在 2×（510 亮度），暗部精度折半（127 级而非 255）。极端 bloom 场景会在隧道里看到量化伪影，但 Proun 的纯色抽象风格让伪影大多不可见。**意外的副作用**：两个不同色亮物体模糊重叠 + 后期乘 2 会产生高饱和混色光晕，他说"挺好看的"。

## 关键要点

- 问题本质：8-bit RT 在模糊之前就 clamp 超亮信息，丢了 bloom 需要的动态范围
- Trick：渲染时 × 0.5（"超亮"藏进 UNorm 的高半段），模糊，最后 × 2 还原
- 代价：动态范围上限 2×（510）；暗部精度折半（banding 风险翻倍）
- 副作用：多色高亮混合会产生意外高饱和光晕（他当卖点用）
- 工程动机：避免 fp16 RT 的带宽 / blend 开销，保持老显卡兼容
- 今日适用性：低 —— R11G11B10F / fp16 bloom buffer 已是现代 GPU 标配；作为"硬件受限下 visual / storage space 解耦"的思路样本仍有参考价值

## 链接到的概念

- [[fake-hdr-half-brightness]]
- [[bloom-threshold-blur-composite]]
- [[gamma-correction-srgb]]
- [[unorm-snorm-hardware-conversion]]

## 原文

- 链接：http://joostdevblog.blogspot.com/2010/09/overbright-colours-blur-and-faking-it.html
- 本地：`raw/articles/joostdevblog.blogspot.com/2010-09-18_overbright-colours-blur-and-faking-it.md`
