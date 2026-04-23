---
tags: [source, glsl, g-buffer, shader]
date: 2026-04-19
sources: 1
---

# FMTT, GLSL Edition（Ben Supnik / The Hacks of Life）

[[ben-supnik|Ben Supnik]] 发表于 2010 年 12 月的四行贴——标题沿用他 *I Hate C* 系列的 *FMTT*（"for me the trouble"）吐槽风，实际内容是前一篇 [[sources/supnik-gbuffer-format|G-Buffer 格式]]的 GLSL 实现样本。

## 摘要

四行 `gl_FragData[0..3]` 把 X-Plane 10 G-Buffer 的 16 字节布局直接翻译成片元着色器输出：`gl_FragData[0]` 写 albedo × 顶点颜色 × alpha（alpha 通道用 `tex_color.a + lit_color.a` 钳位合成）；`gl_FragData[1]` 把 shiny×AO、深度归一化（`position_eye.z/-1024.0`）以及 `cut_pos` 打成一个 RGBA；`gl_FragData[2]` 写眼空间法线 XYZ × `cut_pos`；`gl_FragData[3]` 输出 emissive + texture × 场景色。其中 `cut_pos` 显然是作者用作 discard 代理的标志位（乘 0 即丢弃）。帖子本身没有叙述，只有代码——作为 G-Buffer 格式文档的实现侧佐证有意义。

## 关键要点

- 用乘法 × `cut_pos` 代替 discard，给 MRT 做统一的「输出 0」把戏。
- 深度通道直接手写归一化 `z / −1024.0`——匹配 G-Buffer 文档里 16F 深度只覆盖近距的设计。
- MRT 各 RT 共享同一 rasterization 状态（包括 `cut_pos`），符合 [[multiple-render-targets]] 里「所有 RT 一次几何一起写」的约束。
- 第四行写 emissive 时 alpha 通道用元组语法 `(a+b, 0.0, 1.0)`——这是一个原文 typo（逗号运算符），实际产出是 `1.0`，不影响功能。

## 链接到的概念

- [[xplane-gbuffer-format]]
- [[multiple-render-targets]]
- [[fragment-shader]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2010/12/fmtt-glsl-edition.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2010-12-09_fmtt-glsl-edition.md`
