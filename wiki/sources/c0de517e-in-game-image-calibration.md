---
tags: [source, rendering, color, calibration]
date: 2026-04-27
sources: 1
---

# In-Game Image Calibration（Angelo Pesce / C0DE517E）

[[angelo-pesce]] 发表于 2011 年 7 月的文章，系统讨论游戏内显示校准屏的设计原则。

## 摘要

文章指出游戏行业对色彩管理普遍不重视，且现实用户的电视出厂设置往往严重偏差。通过梳理信号链（渲染 → 视频卡 → 电视机）、不同视频标准的黑白电平定义（PAL/NTSC/HDMI limited/extended）、以及 PS3 与 360 的默认行为差异，得出一个核心结论：**动态范围（dynamic range）比 gamma 校准更关键**，传统的「深灰 logo 法」虽然流行但效果有限。建议使用多级灰阶色条配合动画闪烁图案，让用户直接校准黑白边界，同时提供硬件 gamma 控制（非线性曲线）、可选对比度曲线、以及锐度/降噪指引。

## 关键要点

- 动态范围失真比 gamma 偏差对可玩性的影响更大
- 跨平台首先要对齐硬件输出的 gamma 行为（360 vs PS3 默认不同）
- 在 framebuffer 后处理做修正精度有限（8 位），调电视硬件设置才是根本方案
- 动画闪烁图案比静态图案更易识别细节差异
- 校准屏应在中性背景下展示，防止 TV 动态背光算法干扰测试图案

## 链接到的概念

- [[in-game-display-calibration]]
- [[gamma-correction-srgb]]
- [[color-space]]
- [[linear-lighting-pipeline]]

## 原文

- 链接：https://c0de517e.blogspot.com/2011/07/in-game-image-calibration.html
- 本地：`raw/articles/c0de517e.blogspot.com/2011-07-09_in-game-image-calibration.md`
