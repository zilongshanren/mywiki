---
tags: [source, 渲染, 透明, alpha, blend-state]
date: 2026-04-19
sources: 1
---

# Alpha Blending, Lets Try Again（Ben Supnik / Hacks of Life）

[[ben-supnik]] 2010 年 10 月回到自己早先那篇"back-to-front vs front-to-back"blend state 配方。他说那篇写得太绕——重新用**预乘 alpha**重推一遍，公式立即统一、也不再需要 `glBlendFuncSeparate` 这种"恐龙硬件以外才支持"的高级特性（其实自 Radeon 8500 起都是 commodity）。

## 摘要

目标是把多个半透明贴图合成到一张中间 framebuffer、再把这张中间层合成到主场景上，让结果与按原顺序直接画等价。Supnik 的推荐是**所有中间层与最终 blit 都使用预乘 alpha**。在预乘约定下，back-to-front 合成的 blend state 是 `(1, 1-SA)`（因为 source 的 RGB 已经乘过 SA），front-to-back 是 `(1-DA, 1)`——两者在形式上对称，只差哪一侧当"主掩码"。

他重点讲清了 back-to-front 合成为什么**需要预乘才能正确累积 alpha 通道**：在传统 `(SA, 1-SA)` 下，一层 10% 的浅色遮罩会把已经不透明（α=1）的底层 alpha 拉到 `0.1 + 0.9 = 1.0`——这次恰好对。但多层叠加后 α 会漂；预乘 + `(1, 1-SA)` 下，`α_new = α_src + α_dst × (1 - α_src)`，这就是 Porter-Duff over 的 α 方程，可保正确。Front-to-back 则给出对偶：已有 `α_dst` 越大、新 layer 的贡献越少，`(1-DA, 1)` 正好表达这一点，且永远不会让已有颜色变暗——符合"画在后面的东西不会变亮前面"的物理直觉。

## 关键要点

- 一旦全链路预乘，back-to-front 和 front-to-back 只是 `(1, 1-SA)` vs `(1-DA, 1)` 的对称切换。
- Back-to-front + 非预乘会累积 alpha 误差，多层堆叠时 `α_final` 不等于 `1 - ∏(1-α_i)`。
- Front-to-back 的优势是前景几乎不透明时可以跳过对后景 shader 的 invocation（结合 early-Z）。
- Split blend function（`glBlendFuncSeparate`）在预乘方案里不再必须——简化了老硬件兼容。

## 链接到的概念

- [[alpha-blending]]
- [[alpha-blending-front-to-back]]
- [[alpha-compositing]]
- [[premultiplied-alpha-bilinear-ring]]
- [[srgb-premultiplied-alpha-compression]]
- [[ben-supnik]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2010/10/alpha-blending-lets-try-again.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2010-10-07_alpha-blending-lets-try-again.md`
