---
tags: [渲染, 透明, alpha, blend-state, opengl]
date: 2026-04-19
sources: 1
---

# Front-to-Back Alpha Blending（前向 alpha 混合）

常规 [[alpha-blending]] 从后往前画，用 `GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA`。**Front-to-back** 反过来——先画最近的半透明层、再依次把远层「填到」它背后。动机是如果一个像素的前层已经几乎不透明，就不需要再 shade 后层；结合 [[early-z-late-z|early-Z]] 和 occlusion 可以省 fragment 工作。Ben Supnik 2010 年这篇短文给出三种情形下的 blend-state 配方。

## 前向合成本身

目标 framebuffer 必须有 alpha 通道——它用来记「还剩多少光能穿到后层」。三个条件：

1. framebuffer 初值 `(0,0,0,0)`——全黑全透明；
2. blend function 设为 `GL_ONE_MINUS_DST_ALPHA, GL_ONE`——新 fragment 被已积累的不透明度 _dst_alpha_ 扣减；
3. fragment shader 自行把 `RGB *= alpha`——因为硬件 blend 不再做这个乘法（参见 [[alpha-compositing|预乘 alpha 的数学]]）。

代价：无法叠在既有场景上，除非既有场景的 alpha 通道已经清零。一般场景渲染完后 framebuffer 的 alpha 往往是 1 或未定义，直接前向叠层会出错。

## Compositing：把前向层贴回主场景

前向层渲完后要合成到主 framebuffer，用 `GL_ONE, GL_ONE_MINUS_SRC_ALPHA`。为什么？前向层是画在黑底上的，相当于 **已经预乘**，因此不用再 `GL_SRC_ALPHA`。

## 后向合成的「alpha 透穿」问题

传统 back-to-front 有个隐疾：如果 4 层 50% 不透明纸叠起来，framebuffer 里最终的 alpha 仍接近 0.5，而物理正确值是 `1 - 0.5^4 = 0.9375`。如果后续还要把这张累积纹理 blit 到更外层 framebuffer，alpha 就是错的。

Supnik 给出的 voodoo 是**让 alpha 通道反转存储**（0 = 不透明，1 = 透明）并用乘法累积：

- 初值 `(0,0,0,1)`；
- 颜色 blend 保持 `GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA`，但 alpha 通道用 `GL_ZERO, GL_ONE_MINUS_SRC_ALPHA`（需要 `glBlendFuncSeparate` / GL 1.4）——这样 `dst_A *= (1 - src_A)`，乘法累积透明度；
- 最终 blit 时用 `GL_ONE, GL_SRC_ALPHA`——因为现在 dst 的 alpha 已经是「透明度」语义。

本质是：**乘法倾向把值拉向 0，所以把 0 当不透明、1 当透明**，让「越来越不透明」在数学上对应「越来越小」。

## 何时用

- 粒子系统（烟雾、火焰）如果数量庞大且前向 early-out 能省 shader，可以考虑前向。
- 要把半透明层 cache 成 texture 再二次合成时（典型如全屏粒子 / UI 合成），必须在意 blit 时 alpha 是否正确——这就是 Supnik 拐到反转 alpha 方案的动机。
- 绝大多数实时管线仍然直接 back-to-front + `GL_ONE, GL_ONE_MINUS_SRC_ALPHA`（预乘 over）了事。

## 相关
- [[alpha-blending]]
- [[alpha-compositing]]
- [[ben-supnik]]
- [[scatter-bokeh-dof]] —— 同样用预乘 additive + 归一化做累积的实例
- [[deferred-alpha-lighting]]
- [[premultiplied-alpha-bilinear-ring]] —— 同一时期 Supnik 讨论预乘为何能自动修 bilinear ring artifact
- [[sources/supnik-alpha-blending-lets-try-again]] —— 作者本人对先前那篇配方的重写，给出更对称的 `(1, 1-SA)` vs `(1-DA, 1)` 形式
- [[triangle-plane-sort-translucency]] —— 互不相交单面三角形的视角无关预排序

## Sources
- [[sources/supnik-alpha-front-to-back]]
