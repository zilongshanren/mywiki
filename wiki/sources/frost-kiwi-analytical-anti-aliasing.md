---
tags: [source, 渲染, 反走样, sdf, webgl]
date: 2026-04-14
sources: 1
---

# AAA - Analytical Anti-Aliasing（Frost / frost.kiwi）

[[frost-kiwi|Frost]] 发表于 2024 年 11 月的长文，是整个 wiki 里关于反走样最深的一篇文章。文章用一个在圆圈里绕圈运动的 WebGL 演示做「同一个测试用例」，依次跑过 SSAA、MSAA（各档数）、FXAA、以及他称之为 **Analytical Anti-Aliasing（AAA）** 的路线，最后深入剖析 AAA 的每一个实现细节。

## 摘要

Frost 的立论是：传统反走样都在「先光栅化、再补救」——但对于**你已经知道数学形状**的情形，有一种完全不同的路：直接在 fragment shader 里按 [[sdf-2d-primitives|signed distance field]] 把边缘淡出恰好一个像素，得到完美平滑、不依赖硬件、不依赖后处理、不依赖历史帧的结果。他把这种思路命名为 [[analytical-antialiasing|Analytical Anti-Aliasing]]，并追溯到一系列业界对**已知形状**做逐像素数学求值的做法——The Last of Us 的胶囊软阴影与模糊反射（Michał Iwanicki）、Inigo Quilez 的解析 AO、MSDF 字体渲染，都属于同一类。文章的后半展开了 AAA 实现里的三个真正「热门话题」：**怎么知道一个像素多大**（`fwidth` 的 L1 近似带来菱形偏差；`dFdx + dFdy + length` 更准；或者**直接 per-object 算出来当 uniform 传进去**，这是 Frost 的推荐做法，连扩展都省了）；**用什么做淡出**（他的暴论：不要用 `smoothstep`——Hermite 插值在一个像素宽度内毫无意义，用线性步函数就够）；以及 **quad 必须扩大一个像素** 以免边缘被光栅化吃掉。文章还配上了 SSAA 实施里的现实陷阱（2x 之上就得多 tap，不只是 linear downsample）、MSAA 在手机端的奇葩（iOS 2x 实际是 4x 再 round）、FXAA 的 3×3 邻域先天缺陷与 `fxaaQualityEdgeThreshold` 调参等细节，是 Frost 多年实现 AAA 的自我总结。

## 关键要点

- **Analytical AA** = 已知 SDF → 在 shader 里按距离淡出一个像素宽度的边
- 传统 [[msaa-ssaa|SSAA]] 在不接触渲染管线内部的情况下只能做 2x，再高就得 multi-tap
- [[msaa-ssaa|MSAA]] 的支持度因硬件而异：iOS 的「2x」其实是 4x 再 round，TBDR 移动 GPU 上 4x 几乎免费
- FXAA 只看 3×3 邻域，对大形状完全无法感知 → 运动时产生形变与「呼吸」伪影
- AAA 的公式：`alpha = (1 - dist) / pixelSize`，blend 自动截断到 [0,1]
- **别用 `smoothstep`**——一个像素宽度内没有曲线可言，浪费算力
- `fwidth()` 是 `length()` 的 L1 近似，**在对角方向过估**，把小圆压成菱形（Freya Holmér 的 Shapes 把它叫 "Fast Local AA"）
- 最干净的方案是 **per-object 计算像素尺寸**当 uniform 传进来——连 `dFdx` 扩展都不用，跑在最老的 GPU 上
- Quad 要比形状大 1 像素，给 AA 淡出留呼吸空间
- 同一套 shader 可以通过切换 API 状态跑在 AAA（alpha blend）或 MSAA + Alpha-to-Coverage 两种路径上
- AAA 的局限：**不适用于传统光栅化几何**、无法处理纹理内部高频、不处理延迟渲染的屏幕空间走样

## 链接到的概念

- [[analytical-antialiasing]]
- [[aliasing]]
- [[msaa-ssaa]]
- [[temporal-antialiasing]]
- [[sdf-2d-primitives]]
- [[fragment-shader]]
- [[frost-kiwi]]

## 原文

- 链接：<https://blog.frost.kiwi/analytical-anti-aliasing/>
- 本地：`raw/articles/blog.frost.kiwi/2024-11-20_aaa-analytical-anti-aliasing.md`
