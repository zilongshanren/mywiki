---
tags: [source, 渲染, 透明, alpha, x-plane, 纹理压缩]
date: 2026-04-19
sources: 1
---

# Premultiplication: Pros and Cons（Ben Supnik / Hacks of Life）

[[ben-supnik]] 2010 年 10 月的文章，用 X-Plane 里的 **tree ring** bug 作为引子，讨论预乘 alpha 的优缺点以及为什么 X-Plane 最终没有采用它。

## 摘要

X-Plane 的树贴图经常在边缘出现一圈杂色的"ring"。根因是 GPU 的 bilinear filter 会把完全透明像素（α=0）里遗留的 RGB 值（常被 Photoshop 填成白色）和相邻不透明树叶的绿色**按通道插值**——边缘像素于是变成"发白的绿"。传统的手工补救是让透明区 RGB 也填成接近可见色的值（"more green"），但这个信息美术在软件里根本看不见，非常脆弱。**预乘 alpha 天然解决这个问题**：透明像素 RGB 按定义就是 0，bilinear 插值得到"更暗的绿"——这正是预乘 over 合成期望的结果。

但 Supnik 指出两个让 X-Plane 不转的理由。其一是**纹理压缩**（BC1/BC3/BC7）：非预乘时压缩器可以把有限色彩端点预算都花在树叶本色上；预乘后 α 变化带来的亮度渐变也要用端点表达，色彩精度被稀释。理论上需要 α-aware 的压缩器，现实里没有。其二是"ring"还有一个更严重的来源——**Z-buffer 对半透明的不友好**。X-Plane 选择直接关 blending、走 alpha test + bilinear，于是 ring 问题被"非 0 即 1 的 alpha"掩盖，同时绕开 Z-artifact。评论区问是否能离线预乘到 DDS 缓存，Supnik 回答不值得做，因为 X-Plane 发布时已经 ship 压好的 DDS。

## 关键要点

- Bilinear filtering 和 alpha 乘法**不可交换**——预乘把乘法放在插值之前，非预乘放在之后。
- Photoshop 的 alpha=0 区域 RGB 默认白色，是 ring artifact 的制度性原因。
- 预乘 α + BCn 压缩在实践中互相伤害——精度预算被稀释。
- X-Plane 的最终选择是 alpha test + bilinear，而非 blending + 预乘。

## 链接到的概念

- [[premultiplied-alpha-bilinear-ring]]
- [[alpha-compositing]]
- [[alpha-blending]]
- [[srgb-premultiplied-alpha-compression]]
- [[dither-alpha-clipping]]
- [[bc7-solid-color-blocks]]
- [[ben-supnik]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2010/10/premultiplication-pros-and-cons.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2010-10-06_premultiplication-pros-and-cons.md`
