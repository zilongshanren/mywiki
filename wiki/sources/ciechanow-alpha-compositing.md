---
tags: [source, 渲染, 透明]
date: 2026-04-14
sources: 1
---

# Alpha Compositing（Bartosz Ciechanowski）

[[bartosz-ciechanowski|Bartosz Ciechanowski]] 2019 年 7 月发表的长文，从「玫瑰色眼镜」这种日常隐喻出发，一步步推导出 Porter-Duff **source-over** 合成公式和 **premultiplied alpha** 的必要性。

## 摘要

文章先把 alpha 拆成 **opacity × coverage** 两个物理来源：对象本身挡住多少光 × 它在像素内覆盖多少面积。用交互演示展示低 bit-depth 的 alpha 怎么在 gradient 上产生色带。然后通过「三层合成、两种顺序」的例子说明需要结合律——导出合成方程，发现非预乘形式里藏着一个除以 `R_A`，直到改用**预乘 α** 方程才变干净、可组合、硬件友好。

## 关键要点

- **α = opacity × coverage**：一旦相乘不可分离，这就是为什么「alpha」和「opacity」两词常混用。
- **部分覆盖是文字渲染的物理基础**：矢量图形抗锯齿完全依赖它。
- **Porter-Duff over 方程**：`R_A = S_A + D_A(1-S_A)`，RGB 类似。
- **预乘 α 的三大好处**：合成可结合、滤波正确、GPU blend state 原生支持。
- **零 α 带颜色**：只有预乘形式能表达「完全透明但贡献自发光」的 additive 粒子。

## 链接到的概念

- [[alpha-compositing]]
- [[alpha-blending]]
- [[rasterization]]
- [[aliasing]]
- [[bartosz-ciechanowski]]

## 原文

- 链接：https://ciechanow.ski/alpha-compositing/
- 本地：`raw/articles/ciechanow.ski/2019-07-24_alpha-compositing-bartosz-ciechanowski.md`
