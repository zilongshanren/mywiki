---
tags: [source, 渲染, 全局光照, GI, raymarching, radiance-cascades, 优化, gamemaker]
date: 2026-04-19
sources: 1
---

# Radiance Cascades Part 2（Yaazarai / GM Shaders Guest）

[[alex-yaazarai|Alex (Yaazarai)]] 2024 年 7 月 13 日在 GM Shaders 发表的 RC 系列续篇——专讲 **pre-averaging + direction-first 两项优化**，完整代码深剖。Part 1 的实现在他自己看来"过于复杂、不支持非方形分辨率、性能差、内存浪费"，这一篇把它重写成**不到 100 行的单 shader**。

## 摘要

Part 1 的四类毛病分别对应四类修复。**Complicated**：射线计算和 merge 分两个 shader → 合并成一个 pass（raymarch + 和上级 merge 同时做）。**Not Dynamic**：整套数学假设方形分辨率 → 加严"探针 spacing 是 2 的幂次"的约束，距离用 `length(renderExtent)` 归一化，支持任意宽高比。**Performance/Memory**：引入两个优化——**Pre-Averaging**（既然 merge 就是要把 4 条同向射线平均，那就直接 cast 4 条 raymarch 出平均值，只存 1 个值 → 内存 -75%、merge 采样 -75%）和 **Direction-First 布局**（把"同方向不同位置"的射线放一起，merge 时启用硬件双线性，1 次采样完成 4 个邻近探针的插值 → merge 采样从 16 降到 1）。**UPDATE 声明**特别重要：作者 2024-07 后补了一条更新，纠正自己早先说的"direction-first 更快"——实际是他当时 GM 版本的一个 bug 让 position-first 表现变差；direction-first 真正的价值是**调试友好**（所有同方向射线物理上挨着）。代码深剖给了 probe_info 抽象、raymarch 函数（注意：在 pixel 空间做、距离用对角归一化，避免非方形 UV 扭曲）、merge 函数的 bilinear 插值细节（关键：`probe * 0.5 + 0.25` 的偏移让当前探针在 N+1 上落到正确插值位置，clamp 避开方向块边界防漏光）。Main 函数最后只用 4 次 raymarch loop 就完成一个 texel 的工作。Benchmark：Position-first 1024² 0.25 spacing 4 rays → 29.91ms；Direction-first 1920×1080 同参数 → 25.95ms（更大分辨率反而更快）——同一条提醒了引擎因素。评论区两个质疑值得记：(1) 几乎所有 2D RC 实现都有**同心干涉条纹**——why？(2) 6 cascade × 4 rays ≈ 24 rays per pixel，性能为什么不一定胜过朴素 24-ray + bilateral filter？作者没直接答，但暗示取决于硬件 cache 行为。

## 关键要点

- **单 shader 重写**：raymarch + merge 合到一 pass，代码从 Part 1 的 shader-pair 压到 < 100 行。
- **Pre-Averaging**：cast 4 条同向射线，存 1 个平均值。内存 -75%、merge 采样 -75%。
- **Direction-First 布局**：同方向的所有探针射线挨着放，硬件双线性做 merge 的 4 邻近探针插值——**16 次采样降到 1 次**（叠加 pre-averaging）。
- **作者的诚实更正**：更新 note 指出原 "direction-first 更快" 的说法是 GM 引擎 bug 造成的——事实上这个布局主要价值在**调试**。
- **Pixel space raymarch**：在像素坐标做距离运算，texture lookup 前换算回 UV——支持非方形分辨率的关键。
- **Light leak fix**：每级射线长度加一点 overlap（`range += length(spacingN+1)`），相邻级联轻微重叠填补过渡缝。
- **Merge 的 bilinear weight = `0.25`**：当前探针在 N+1 的 4 个邻居中位置恰好是 `0.25,0.25` / `0.75,0.25` / ...，所以 `probe*0.5 + 0.25` 能一步到位。
- **Direction-first 块要 clamp 1 probe 边界**：否则 bilinear 会跨到相邻方向块，造成可见 artifact。
- **Part 1 → Part 2 性能提升**：1024² 到 1920×1080 更大分辨率下反而更快，优化叠加效果明显。
- **Missing Piece**：2D RC 的**同心干涉条纹**还是 open problem，评论区集体发问。
- **vs 朴素采样**：总射线数相近下，RC 不一定更快；优势是 noise-free + 不需要时域降噪——**质量优势而非性能优势**。

## 链接到的概念

- [[radiance-cascades]]
- [[penumbra-hypothesis]]
- [[alexander-sannikov]]
- [[alex-yaazarai]]
- [[jump-flooding-algorithm]]
- [[bilinear-sample-blur-optimization]]
- [[instant-radiosity-vpl]]
- [[xor-shader-artist]]

## 原文

- 链接：https://mini.gmshaders.com/p/radiance-cascades2
- 本地：`raw/articles/mini.gmshaders.com/2024-07-13_gm-shaders-guest-radiance-cascades-2.md`
