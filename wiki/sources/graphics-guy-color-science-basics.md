---
tags: [source, rendering, color-science, hdr, color-space]
date: 2026-04-27
sources: 1
---

# Basic Color Science for Graphics Engineer（A Graphics Guy's Note）

[[people/graphics-guy-notes]] 发表于 2018 年 11 月的文章，为图形程序员系统梳理色彩科学基础：从光谱功率分布到 CIE 色度图，再到 sRGB、Rec.709、Rec.2020 的矩阵变换与传输函数，背景是为《Skull & Bones》实现 HDR 显示器支持。

## 摘要

文章以 HDR 显示器普及为背景，解释了为什么图形程序员必须理解色彩科学。首先介绍光谱功率分布（SPD）与人眼三种锥体细胞的响应机制，由此引出用三个数值表示颜色的生理学依据。颜色匹配实验揭示了 RGB 基下存在负值区域，促成了纯虚拟 XYZ 色彩空间的诞生——XYZ 是所有可见色的正值基。通过向 `x+y+z=1` 平面投影，得到二维 CIE 1931 色度图，可在设备无关的坐标系中讨论颜色。在此基础上，文章推导了白点（white point）如何隐式确定各基向量的缩放因子，并给出 Rec.709/sRGB/Rec.2020 的色域三角形坐标、XYZ↔RGB 变换矩阵和各自的传输函数（gamma/PQ）。sRGB 仅覆盖 CIE 1931 的 35.9%，Rec.2020 达到 75.8%。

## 关键要点

- 可见光波长范围约 380–750 nm；PBRT 取 400–700 nm
- CIE RGB 色彩匹配实验中存在负值，XYZ 基向量是"虚拟"原色以使全域为正
- 白点定义了颜色空间中各基向量的缩放因子，求解方程 `S_r*R_xyz + S_g*G_xyz + S_b*B_xyz = W_xyz/W_y`
- sRGB 与 Rec.709 的色域基本相同，但传输函数（gamma 曲线）略有差异
- Rec.2020 色域覆盖率是 sRGB 的两倍以上；其传输函数通常使用 PQ（Perceptual Quantizer）
- 游戏引擎中"线性色彩空间"默认意味着 linear sRGB；向 Rec.2020 的全面迁移尚待 HDR 工作流普及

## 链接到的概念

- [[rendering/color-space]]
- [[rendering/gamma-correction-srgb]]
- [[rendering/spectral-rendering]]
- [[rendering/spectral-vs-rgb-comparison]]
- [[rendering/display-edid-colorspace]]
- [[rendering/hdr-video-edr-metal]]

## 原文

- 链接：https://agraphicsguynotes.com/posts/basic_color_science_for_graphcis_engineer/
- 本地：`raw/articles/agraphicsguynotes.com/2018-11-29_basic-color-science-for-graphics-engineer.md`
