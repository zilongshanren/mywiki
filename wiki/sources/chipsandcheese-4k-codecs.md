---
tags: [source, 视频编解码, hevc, av1, vvc, 压缩效率, 专利]
date: 2026-04-27
sources: 1
---

# Codecs for the 4K Era: HEVC, AV1, VVC and Beyond（Chips and Cheese）

Dingo Networks 于 2023 年 4 月发表的视频编解码器横向对比文章，以 4K 存档场景为基准，测试 HEVC（x265）、AV1（SVT-AV1）和 VVC（VVenC）在压缩效率与计算复杂度上的差异。

## 摘要

文章分析了视频编解码的技术格局：AVC 老化、HEVC 被专利阻碍普及、AV1 以免专利为优势但在 2023 年仍缺乏主流硬件支持、VVC 理论压缩效率最佳但实用性极低。测试以 VMAF 为质量指标，在 AMD Ryzen 7950X 上完成。结果显示 VVC 压缩效率最高，但编码时间以"天"计；AV1 与 HEVC 总体相当，AV1 在低质量段略优，HEVC 在高质量段（VMAF 94-96）有 5.6% 的码率优势。文章还深入讨论了 VMAF 与感知质量的偏差——Adaptive Quantization（AQ）会让 VMAF 评分更不稳定，但实际观感反而更好。

## 关键要点

- 压缩效率排名：VVC > HEVC ≈ AV1（在高质量目标下 HEVC 略优）
- 编码速度：HEVC >> AV1（慢 7.5x）>> VVC（需数天编码 14 分钟片源）
- VMAF 度量偏差：会惩罚 Adaptive Quantization 等感知优化，导致新编解码器得分看起来更差
- AV1 最大优势在于免版权，但 Sisvel 专利池已对其提出挑战
- VVC 目前缺乏硬件解码支持，播放器支持几乎为零
- HEVC 在家用存档场景依然是最实用选择（专利在个人使用中影响较小）

## 链接到的概念

- [[rendering/video-codec-hevc-av1-vvc]]
- [[rendering/video-codec-licensing-tradeoffs]]

## 原文

- 链接：https://chipsandcheese.com/p/codecs-for-the-4k-era-hevc-av1-vvc-and-beyond
- 本地：`raw/articles/chipsandcheese.com/2023-04-16_codecs-for-the-4k-era-hevc-av1-vvc-and-beyond.md`
