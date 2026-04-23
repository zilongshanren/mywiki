---
tags: [渲染, temporal, taa, 抗锯齿, 采样]
date: 2026-04-14
sources: 1
---

# Temporal Supersampling（时域超采样）

**把超采样的 N 倍计算分摊到连续 N 帧**——这是 Wronski 2014 年反复讲的核心观察：在相邻帧之间，屏幕上的大部分内容对应同一些表面，只要知道它们在上一帧屏幕上的位置（[[motion-vectors|motion vectors]]），就可以把「多样本」变成「多帧采样后累积」，把 N 倍成本摊成 ~1.05 倍。这个思路比狭义的 [[temporal-antialiasing|TAA]] 更一般——它是一种采样分摊框架，TAA 只是它应用在「最终帧颜色」上的一种特例。

## 与 TAA 的关系

[[temporal-antialiasing|TAA]] 是 temporal supersampling 在最终图像上的落地：对投影矩阵做 subpixel jitter、历史帧 reproject、按很小权重 blend 进当前帧。它的历史可以追到 Tiago Sousa 在 Siggraph 2011 的 Crysis 2 讲座。但同一个机制可以应用在任何效果上：

- **SSAO** — 把 3 个不同的空间采样图案轮换到 3 帧里，再按深度 rejection 合并，等效于把 AO 样本数乘以 3，blur 半径反而可以砍。
- **[[screenspace-reflections|SSR]]** — 半分辨率 ray pass 的 noise 用历史累积压掉。
- **volumetric fog / 体积光** — 抖动 slice 位置后时域收敛。
- **阴影去噪**、**GI probe 更新** 同样适用。

关键在于每种效果都需要针对性的 **rejection / 接受策略**（见下），不能照搬最终图像的 color clamping。

## 机制四件套

无论应用到哪里，temporal supersampling 都由四个部件构成：

1. **空间 / 时域样本分布**：要让 N 帧的 N 个样本尽量覆盖不同位置。对最终图像是投影矩阵的 jitter 序列（Halton / Sobol），对 SSAO 是 sampling pattern 旋转。
2. **Reprojection**：用当前深度反投影到世界空间，再用上一帧 V·P 矩阵投影到上一帧屏幕，得到历史采样位置。动态物体额外需要 motion vectors。
3. **Rejection / weighting**：判断历史样本是否还代表「这个表面此刻的信号」。最终帧用 color clamping + velocity + depth，SSAO 用纯深度差，SSR 用深度 + hit confidence。
4. **累积 / blend**：通常是很小的当前权重（5%–15%）与历史 blend，等价于 IIR 低通滤波。

## 为什么说「工程泥潭」

Wronski 对 AC4 的复盘里明确列出了落地过程中的痛：

- **motion vectors 必须逐像素精确**——per-object motion blur 的精度远远不够。布料 / 软体 / 海洋 / 程序化植被 / teleport 骨骼，每一类都要单独修 pipeline。
- **motion-magnitude rejection 阈值难调**：threshold 大了 ghost，小了 shake。8-bit motion vector 精度不够用。
- **阴影 / 粒子 / 贴花**没有 motion vector，会把纹理动画当静态累积出拖影。Wronski 的兜底是「位移 > ~2 像素直接不混」。
- **Edge cases**：菜单弹出、暂停、camera cut、post-effect 启动——每一种都要单独关 jitter 和 accumulation。
- **颜色指标**：Sousa 2013 之后业界转向 color-based metric（color clamping），也就是现代 [[taa-history-rectification|history rectification]] 的起点。

## SSAO 的特殊例子

文章里 SSAO 的 temporal 化是一个「**一天就接完**」的反例：3 个 spiral 采样图案轮换，深度 rejection 就够（按 AO 定义，深度连续区域本来就应该相似），所以没有最终帧那种 ghost 问题。副作用是需要两张额外 history texture，但 blur 半径减小反而补回来。Wronski 强烈建议所有屏幕空间效果都做一遍 temporal 分量。

Wronski 在 2014 年 4 月又专门写了一篇 [[sources/bartwronski-temporal-ssao|before/after 演示文]]，补做了 AC4 上 temporal SSAO 的对比截图和视频。里面额外解释了几个实现细节：采样图案按 3 帧轮换（每个屏幕像素位置本身也 unique），在 **blur 之前**做 temporal 是为了保留细节——blur 后低通已经把信息丢了；rejection 用的 depth 是免费的，因为 Scalable AO 已经把 16-bit 深度压进 AO 纹理的两个 8-bit 通道；motion 下的等效样本数会到几百倍（不同屏幕位置的 unique 图案被重投影汇到一起）。他也强调自己的动机和 DICE（_Battlefield 3_）/Epic（_Gears_）不同：后两者是为了 flicker 降噪，只对不稳定像素做混合；Wronski 的思路是**尽可能多保留历史**，因为目的是真正的多样本超采样。

## 相关
- [[temporal-antialiasing]]
- [[taa-history-rectification]]
- [[motion-vectors]]
- [[aliasing]]
- [[screenspace-reflections]]
- [[hbao-interleaved-sampling]]
- [[msaa-ssaa]]
- [[bartosz-wronski]]
- [[temporal-sao-reprojection]] —— Bitsquid Stingray 把 SAO temporal 化、用 depth-mip 里的 moving bit 抓 dangerous samples

## Sources

- [[sources/bartwronski-temporal-supersampling]]
- [[sources/bartwronski-temporal-ssao]]
