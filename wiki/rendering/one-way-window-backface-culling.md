---
tags: [渲染, 剔除, 优化, 阴影, unreal]
date: 2026-04-19
sources: 1
---

# 单向窗户：用 back-face culling 做「只能从外看进来」的房间

**场景**：游戏里一座房子侧面开了窗，玩家凑近能看到房间内部。但是如果房子另一侧也开了窗，正常情况下两边窗能「对穿」，从一扇窗能直接看到背后的另一扇，这对艺术和性能都不好。[[simon-trumpler]] 在《Infinity Nikki》里注意到这种透视被**刻意禁掉**了——这就是 simonschreibt 起的名字「**one-way window**」。

## 原理

房子的外壳是一块**单面**的几何体。你朝房子外部看它的**正面**（法线朝外）时，它正常渲染；但当你的视线穿过第一扇窗口进入室内后，再看背面（法线朝内）那一大块墙时，**back-face culling 把它直接丢掉了**——所以室内并没有被一张巨大的背面贴到屏幕上，你能看见家具、NPC、灯光。

同时，远处那一侧的窗户本身是**另一块几何**，但它位于被剔除的大墙后面——用离线 / 手工放置的 [[occlusion-culling|occlusion 体积]] 把那一带整个遮住，就能避免从第一扇窗望穿房子看到后窗。

## 为什么不是「省三角形」

Simon 最初的猜想是「省几何量」，评论区纠正了几个更实际的好处：

- **省 overdraw**：透过两扇窗看到的室内+背景会产生多层透明叠加，back-face 剔掉大墙等于砍掉一整层。
- **回避半透明排序**：窗玻璃、纱帘、粒子这些半透物本来就头疼，少一层就是少一层排序问题。
- **配合 occlusion culling**：如果墙真的是双面的，放手工 occlusion volume 时就纠结了——挡住就连窗内也看不见、不挡就白放。单向墙让「从背面剔掉」和「从正面正常画」自洽共存。

## 和 shadow map 的衔接

一个自然的担心：如果背面被剔，那阳光怎么透过「被剔掉的那面墙」照进室内？答案——**shadow map 只用 front-face 做 caster**（见 [[shadow-caster-culling-front-back]]）。太阳从外面看房子时只「看到」正面墙，于是正面墙投下阴影；室内没有大片背面来把光挡住，阳光就能落到地板上。这又反过来要求 front-face shadow casting 里要注意 peter-panning 等副作用。

## 相机外 NPC 的动画剔除（bonus）

Simon 在同一篇文章里还揪出了另一条优化：**离相机方向过远的 NPC 不做骨骼动画**。判据似乎不是相机视锥，而是类似 `dot(cameraForward, npcDir) < threshold`——这在 32:9 超宽屏下露馅：有些 NPC 还在屏幕边缘就已经停止动画。典型的「测试覆盖只到 16:9 / 21:9」问题。

## 相关

- [[occlusion-culling]]
- [[shadow-caster-culling-front-back]]
- [[overdraw]]
- [[culling]]
- [[shadow-mapping-basics]]

## Sources

- [[sources/simonschreibt-nikki-one-way-window]]
