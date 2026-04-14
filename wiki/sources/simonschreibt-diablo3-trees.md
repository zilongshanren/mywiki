---
tags: [source, 渲染, 植被, 美术技巧, diablo, alpha]
date: 2026-04-14
sources: 1
---

# Diablo 3: Trees（Simon Trümpler）

[[simon-trumpler|Simon Trümpler]] 2013 年的 Game Art Tricks 拆解，讲 Blizzard 如何用**两张三角形**做出 Diablo 3 里那些剪影细到不可思议的树。

## 摘要

Diablo 3 的树从斜俯视的 ARPG 视角看起来有密集、干净、几乎不走锯齿的轮廓。Simon 一开始以为是高多边形 + 抗锯齿的胜利，直到用 MPQ 导出工具把模型拆出来后发现——Blizzard 是把**带 alpha 的 hand-painted 纹理贴在微弯的 plane 上**，把树枝的每一条细缺口都压进了纹理本身。两张三角形 + 一次采样，就能得到几千个三角形才能做出来的剪影。

这种技巧的前提是 **相机固定**：ARPG 永远是同一个斜角俯视，玩家不会从侧面或背面看树，所以贴面从来不会穿帮。Simon 把它视为「gameplay 约束反哺美术技巧」的典范案例。文章末尾对比了一根完整树枝：三角形两张 vs. 正经模型几千个三角形——美术和性能同时赢。作者强调这不是 bake-highpoly-to-plane，而是先搭几段弯曲 base plane，再在上面反复绘制。

## 关键要点

- 树的视觉焦点是**剪影**，而剪影能被「画进 alpha 贴图」而非「雕进几何」
- 剪影的抗锯齿因此免费获得了 bilinear 采样的过渡带
- 相机固定的 gameplay 给美术让出了 3D→2D 的自由度
- 静态光照是硬约束：动态光会让贴面与场景脱节，评论区里 Simon 猜测需要额外的 shadow geometry 来支持
- 原文附了树的 diffuse + alpha 贴图——属于「看一眼就懂为什么比生成几何好」的直观展示

## 链接到的概念

- [[painted-foliage-bent-planes]]
- [[dither-alpha-clipping]]

## 原文

- 链接：https://simonschreibt.de/gat/diablo-3-trees/
- 本地：`raw/articles/simonschreibt.de/2013-01-21_simonschreibt-3.md`
