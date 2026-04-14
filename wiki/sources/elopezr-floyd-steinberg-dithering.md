---
tags: [source, 图像处理, dither, 误差扩散, java, android]
date: 2026-04-14
sources: 1
---

# Dithering Algorithm（Emilio López Ros / The Code Corsair）

[[emilio-lopez-ros|Emilio López Ros]] 2014 年发表的短文，记录了他在一款 Android 低端机游戏（[[sources/elopezr-dragon-mania|Dragon Mania]]）里为把 32-bit 颜色压到 **16-bit 1555** 而手写 Floyd–Steinberg dither 的四次优化迭代。

## 摘要

目标机型 Galaxy Ace 显存吃不下 RGBA8888，美术原图必须被量化到 1555（每通道 5 bit），直接 round 会产生明显的色带。作者实现了最朴素的 Floyd–Steinberg 误差扩散作为起点，然后进行了四步工程优化：**朴素双重数组 → 倒置索引 → 用 padding 消除边界 if → scanline alternation 的两行滚动 buffer**。每一步都针对 Java/JVM 的具体行为（数组布局、分支预测、内存占用）进行调整。最终版本比朴素实现快约 30%，内存从 `imgW × imgH` 降到 `2 × (imgW + padding)`。文章给出 4 种分辨率下的毫秒数对照表。

## 关键要点

- **第 1 步**：`int[RGBA][pixel]` 二维数组，干净但慢（512² 用时 47 ms）；
- **第 2 步**：调换为 `int[pixel][RGBA]`，小分辨率变快（40 ms），大分辨率反而变慢——JVM 在不同尺寸下对二维数组访存有意外行为；
- **第 3 步**：目标数组上下左右各 pad 一行，消掉 Floyd–Steinberg 循环里 4 个边界 `if`，512² 降到 33 ms，越往大尺寸优化越明显；
- **第 4 步**：scanline 滚动 buffer，只保留当前行和下一行，写完一行就刷入目标纹理。2 * (width + pad) 的工作集同时带来轻微的 cache friendliness 改进；
- 1920×1200 下最终版 70 ms vs 初版 104 ms，2560×1600 下 99 ms vs 145 ms；
- 项目是 Eclipse + Java Android，后续有 C++ 移植计划。

## 链接到的概念

- [[floyd-steinberg-dithering]]
- [[dither-alpha-clipping]]
- [[color-banding]]
- [[cache-friendliness]]

## 原文

- 链接：https://www.elopezr.com/dithering-algorithm/
- 本地：`raw/articles/elopezr.com/2014-03-09_dithering-algorithm.md`
