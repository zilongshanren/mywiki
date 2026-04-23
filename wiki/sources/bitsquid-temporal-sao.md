---
tags: [source, bitsquid, 渲染, ssao, temporal]
date: 2026-04-19
sources: 1
---

# Temporal Reprojection and SAO（Jean-Philippe Guertin / Bitsquid）

Bitsquid 渲染工程师 **Jean-Philippe "Jp" Guertin** 在 2015 年 9 月发的一篇短文——[[niklas-frykholm|Niklas Frykholm]] 之外，Bitsquid 末期渲染组的核心作者之一。讲他们把 Morgan McGuire 的 **Scalable Ambient Obscurance (SAO)** 压到 Xbox One 1–1.5 ms 预算时，在 temporal reprojection 这一层做的几个小优化。

## 摘要

核心问题：SAO 要压到主机预算，必须把 per-pixel tap 数砍到 6–8 次，靠 temporal 累积把有效样本数升回去。Jp 的三个关键点。

**采样分布**：角度 rotation 用 base-3 Halton 的前 8 项 `{1/3, 2/3, ...}` × 2π，半径用 4×4 Bayer 矩阵 dither——Halton 来自 Brian Karis 的 TAA 实践，Bayer 专治 Halton 带来的残留 banding。

**Reprojection similarity function = 三项乘积**：(1) disocclusion 用 Huw Bowles 的相对深度比 `(prev/current)^4`；(2) velocity term 线性衰减；(3) Dangerous samples term 抓"我不动但我的 AO tap 打到了动的邻居"这类二阶 ghost。

**最精彩的是 dangerous samples 的落地方式**：把 "moving" 编成 depth buffer 里的一个 bit，并且在 SAO 自己的 depth mip chain 下采样时把这 bit 传下去；AO tap 读深度的时候顺手就读出了运动信息，**零额外纹理访问**。思路出自 Anton Michels 在 Siggraph 2015 *Rise of the Tomb Raider* 的讲座。之后按 Oliver Mattausch GPU Pro 2 的 "smooth invalidation" 方式沿时间累积，用 `lerp(..., 0.9)` 拉一段记忆。文中附了 before/after，有 dangerous-samples term 后大部分 ghost 消失。

## 关键要点

- SAO temporal reprojection 的采样分布由 **Halton (角) + Bayer (径)** 两层组合，和 TAA 的 subpixel jitter 是同源思路。
- Similarity function 拆成**可独立可视化的三项**（depth / velocity / dangerous-samples），调试时逐项看。
- **Moving bit 塞进 depth buffer** 是 Rise of the Tomb Raider 的原创；mip 下采样也要 forward 这位——这样 SAO 读深度时天然带运动信息。
- Dangerous-samples term 必须沿时间累积（`lerp 0.9`），否则一帧碰到移动物体、下一帧就无脑恢复，ghost 会周期性出现。
- 这是 [[temporal-supersampling|temporal supersampling]] 在 SAO 上的一条独立路径，和 Bart Wronski 的 AC4 方案（仅 depth rejection、3 帧 spiral 轮换）构成**同一家族的两种实现**。
- 全文只有 1–1.5 ms 目标预算这一个工程量化指标，大部分参数（`LOW_VELOCITY_SIMILARITY` 等）作为 magic number 呈现——要重现需要自行调。

## 链接到的概念

- [[temporal-sao-reprojection]]
- [[temporal-supersampling]]
- [[hbao-interleaved-sampling]]
- [[ground-truth-ambient-occlusion]]
- [[temporal-antialiasing]]
- [[motion-vectors]]
- [[low-discrepancy-sequence]]
- [[niklas-frykholm]]

## 原文

- 链接：https://bitsquid.blogspot.com/2015/09/temporal-reprojection-and-sao.html
- 本地：`raw/articles/bitsquid.blogspot.com/2015-09-10_temporal-reprojection-and-sao.md`
