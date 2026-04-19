---
tags: [source, 渲染, shader, blur, gaussian, 优化, gamemaker]
date: 2026-04-19
sources: 1
---

# Blur Philosophy 2（Xor / GM Shaders）

[[xor-shader-artist|Xor]] 2024 年 3 月 2 日的 blur 系列第二篇，续 [[sources/xor-mini-blur-philosophy|Part 1]]。核心是**用硬件双线性插值把采样数再砍一半**——写实战优化的一篇。

## 摘要

Part 1 讲的是"box→Gaussian→kernel→separable"的概念演进，Part 2 纯谈性能。关键 insight：**texture interpolation 是 GPU 的免费算力**，比手动读 4 texel 再 mix 要快得多。把采样点从 texel 中心偏移到 texel 之间（0.5 偏移），一次 `texture2D` 就拿到 2 个（1D）或 4 个（2D）texel 的加权平均。把这招和 [[separable-gaussian-blur|可分离卷积]]叠起来，一个朴素 3×3 box blur 从 9 次采样降到 4 次、17-tap 1D Gaussian 从 17 次降到 9 次。文章 preview 段还提到继续用这招"递归"做大半径 blur 的思路，但完整版在 paywall 之后，免费部分止于 3×3 到 4 次采样这个例子。Xor 明确点出这招对**移动端和 Nintendo Switch** 特别关键——那些平台 texture fetch 贵得离谱，同样算力下能 saved 出几帧。

## 关键要点

- **免费的加权平均**：GPU bilinear 的硬件实现比"手动 4 次点采样 + mix"快，利用它做 blur 是白送性能。
- **偏移 0.5 的魔法**：1D 两 texel 的中点、2D 四 texel 的中心采样——**Separable Gaussian 的 "linear sampling trick"** 即此。
- **4 次采样覆盖 9 texel**：3×3 box blur 近似 Gaussian 的最经济实现（中心 4x 权重、边 2x、角 1x 自然出现）。
- **等权需要 `±sqrt(0.5) ≈ 0.707`**：偏移 0.5 会给中心 texel 4x 权重；改偏移就改权重分布——手里多一个调节旋钮。
- **前提是 linear filter 打开**：`gpu_set_texfilter(true)` 或对应 GL 调用；点采样下这招完全失效。
- **移动端/Switch 尤其受益**：texture fetch 数是移动 GPU 的主要瓶颈。
- **和多 pass 递归组合**：小半径优化 + ping-pong 多 pass = 指数扩展的有效半径（后续教程方向，但 paywall 后了）。

## 链接到的概念

- [[bilinear-sample-blur-optimization]]
- [[separable-gaussian-blur]]
- [[sampler-filter-wrap-modes]]
- [[mipmap-generation-sampling]]
- [[ping-pong-surfaces]]
- [[xor-shader-artist]]

## 原文

- 链接：https://mini.gmshaders.com/p/blur2
- 本地：`raw/articles/mini.gmshaders.com/2024-03-02_gm-shaders-blur-philosophy-2.md`
