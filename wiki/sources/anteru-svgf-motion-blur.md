---
tags: [source, 渲染, 运动模糊, 降噪, 时空滤波]
date: 2026-04-27
sources: 1
---

# Spatiotemporal Variance-Guided Filtering for Motion Blur（Anteru's blog）

[[matthaeus-chajdas|Matthäus G. Chajdas]] 等提出的运动模糊渲染方案，将路径追踪降噪器中的时空方差引导滤波（SVGF）扩展到运动模糊场景，实现单样本每像素的实时高质量运动模糊。

## 摘要

运动模糊能在低帧率下传递速度感，但准确的蒙特卡洛光追运动模糊收敛需要大量每像素采样。传统后处理方案只用单样本，速度快但质量差，容易产生视觉瑕疵。

本文基于已有的路径追踪降噪器（SVGF 系列），设计其运动模糊变体：通过局部估计运动方向与方差，用不同尺度的小波滤波器进行引导滤波，在单样本每像素的条件下生成高质量、时间连贯的运动模糊。

1920×1080 全屏分辨率下运算不超过 4ms，达到实时帧率。

## 关键要点

- 在 SVGF 框架内扩展：时空方差引导 → 运动方向 + 方差局部估计
- 多尺度小波滤波在不同频率分量上分别处理，时间一致性好
- 单样本每像素，后处理级别的成本但质量接近多样本光追
- <4ms @ 1920×1080，适合实时应用

## 链接到的概念

- [[motion-blur-variance-filter]]
- [[svgf-denoiser]]

## 原文

- 链接：https://anteru.net/research/spatiotemporal-variance-guided-filtering-for-motion-blur
- 本地：`raw/articles/anteru.net/2025-02-16_spatiotemporal-variance-guided-filtering-for-motion-blur.md`
