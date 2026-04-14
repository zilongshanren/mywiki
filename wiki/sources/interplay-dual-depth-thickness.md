---
tags: [source, 渲染, 次表面散射, alpha混合, 深度]
date: 2026-04-14
sources: 1
---

# Dual depth buffering for translucency rendering（Kostas Anagnostou / Interplay of Light）

[[kostas-anagnostou|Kostas Anagnostou]] 2013 年 7 月的笔记：为 [[fast-translucency-wraplight|Barré-Brisebois 的假 SSS]] 动态估计物体厚度，用 **ShaderX6** 里的 dual depth buffer 技巧做了一个单 pass 方案，并修补了它在复杂实心物体上的过估计问题。

## 摘要

假 SSS 需要物体厚度——原论文用离线烘焙，但动态物体（雾、毛发、液体）需要实时求解。朴素做法是跑两次几何渲染取前后深度相减，成本是重复提交。Oat & Scheuermann 在 ShaderX6 的 **dual depth buffer** 用「关 cull + `Min` 混合 + R 存 depth + G 存 `1-depth`」一次 pass 就能搞定，厚度 = `(1-G) - R`。Kostas 实测该方法对体积物体效果很好，但对**有叶片挡在前面的雕像**这种复杂实心物体会**过估计**厚度：视线上最远的背面和最近的正面之间夹着叶片，被当成连续实体。他给出的改法是**把正面和背面分流写入不同通道**——front 写 `(depth, 1, ...)`、back 写 `(1, depth, ...)`，仍用 `Min`，结果 R 保留最近正面、G 保留最近背面，厚度 = `G - R`，也就是沿视线**第一段**实体的厚度。叶子不再影响雕像像素的厚度。代价是丢掉多段实体的累加厚度——对 B-B 假 SSS 来说这是合理的取舍。

## 关键要点

- Barré-Brisebois 的假 SSS 需要厚度作为输入参数
- 离线烘焙厚度 → 无法处理动态 / 体积 / 流体；两次几何渲染 → 翻倍开销
- Dual depth buffer = 关 cull + `Min` blend + R 存 depth + G 存 `1-depth`
- `Min` 混合在 G 通道上对 `1-depth` 操作相当于求 `max(depth)`
- 该方法对体积物体（烟、毛发）效果好，对复杂实心物体（多层叶片 + 雕像）过估计厚度
- 改进：按 `frontfacing` 分流，R 只被正面写、G 只被背面写，取的都是「最近」而非「最远」
- 改进后 `thickness = G - R` = 沿视线第一段实体的厚度，叶子不影响雕像
- 假设实体单段连续——对假 SSS 够用

## 链接到的概念

- [[dual-depth-buffer-thickness]]
- [[fast-translucency-wraplight]]
- [[alpha-blending]]
- [[z-buffer]]

## 原文

- 链接：https://interplayoflight.wordpress.com/2013/07/16/dual-depth-buffering-for-transluncency-rendering/
- 本地：`raw/articles/interplayoflight.wordpress.com/2013-07-16_dual-depth-buffering-for-translucency-rendering.md`
