---
tags: [source, 渲染, 视觉设计, 后处理, 美术]
date: 2026-04-19
sources: 1
---

# GM Shaders: Vis Dev（Xor / mini.gmshaders.com）

[[xor-shader-artist|Xor]] 发表于 2024 年 9 月的文章，讲**程序员没有美术天赋时，怎么用 shader 和后处理技巧把自己的画面「调教」得看得过去**。

## 摘要

Xor 的观察：SUPERHOT、INK、OTXO、Thomas Was Alone、Minecraft、Inside 这些高完成度游戏其实视觉很简单，核心不是画技而是**一致性和意图**。他总结了四个维度——色板、分辨率、细节分布、灯光——程序员美术应该主动在这四块上做选择而不是「想到什么画什么」。色板上少即是多，3~6 色配合 dithering / LUT 足以出风格；要看直方图检查亮度范围有没有用满。分辨率上绝不混用 pixel scale。细节分布上**整屏密度要连续**，背景空就补点程序化低频图案。灯光上软 drop shadow 几乎零成本却能立刻抠出前景，bloom / outline / vignette / fog 都是引导视线的廉价工具。文章结尾推荐 Foxy Of Jungle 的 Crystal 2D lighting 方案和 Jan Orszulik 的 Precursor，是「程序员美术走到极致」的示范。

## 关键要点

- **色板**：程序员常配色过花，SUPERHOT / OTXO 2~3 色就能成风格。
- **看直方图**：GIMP 打开截图看亮度分布，最亮像素往往没到 255，整体乘一个系数就能大幅提升。
- **Pixel scale 一致**：16×16 tile 就全项目 16×16 tile，不混用。
- **细节分布连续**：角色精致、背景空 → 补程序化波纹 / 轻阴影 / 柔光。
- **软 drop shadow**：Xor 的偏爱，抠前景 + 给 2D 画面加深度感。
- **Bloom / outline / vignette / fog**：视线引导四件套。

## 链接到的概念

- [[programmer-art-vis-dev]]
- [[color-lut]]
- [[color-quantization-kmeans]]
- [[color-banding]]
- [[gamma-correction-srgb]]
- [[cel-shader-outline]]
- [[bloom-threshold-blur-composite]]
- [[chromatic-aberration-post]]
- [[creative-coding-process]]

## 原文

- 链接：<https://mini.gmshaders.com/p/visdev>
- 本地：`raw/articles/mini.gmshaders.com/2024-09-01_gm-shaders-vis-dev.md`
