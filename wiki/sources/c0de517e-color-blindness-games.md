---
tags: [source, 渲染, 辅助功能, 色彩, 色盲]
date: 2026-04-27
sources: 1
---

# Color Blindness and Videogames（Angelo Pesce / C0DE517E）

[[angelo-pesce]] 发表于 2013 年 2 月的技术调研文章，探讨如何为色觉缺陷玩家（约占男性的 8%）提供色盲友好的游戏体验，重点介绍了基于 LMS 色彩空间的 daltonization 线性变换算法及其在游戏后处理管线中的集成方案。

## 摘要

文章从一篇 PC Gamer 报道出发，调研了现有学术文献，定位出核心参考：Fidaner、Lin 和 Ozguven 的《Analysis of Color Blindness》，该文推导了一套从 RGB 到 LMS 色彩空间、模拟色觉缺陷、计算差值并以可感知颜色补偿的线性变换算法。整个算法简单到可以做成全局 volume LUT，与现有色彩校正后处理管线无缝叠加。作者同时指出静态全局变换的局限，并提出多种低成本落地方案：将误差项馈入 bloom、与 unsharp mask 联用实现局部对比增强等。

## 关键要点

- 色盲模拟的核心链路：RGB → LMS → 丢失某通道（模拟三色觉缺陷）→ 计算差值 → 将差值转换为可感知颜色反馈回原图（daltonization）
- RGB→LMS 转换需要先做 degamma（sRGB 非线性），直接在 gamma 空间做会引入误差
- 静态全局 LUT 方案成本极低；对内容自适应的变换效果更好但不适合逐帧变化的游戏画面
- 误差项可复用到 bloom 或 unsharp mask，节省一个后处理 pass
- 作者认为色盲模式既能辅助玩家，也能帮助 UI 设计师自测色彩对比度

## 链接到的概念

- [[color-blindness-accessibility]]
- [[color-space]]
- [[image-effect-colour-transform]]

## 原文

- 链接：https://c0de517e.blogspot.com/2013/02/color-blindness.html
- 本地：`raw/articles/c0de517e.blogspot.com/2013-02-10_color-blindness-and-videogames.md`
