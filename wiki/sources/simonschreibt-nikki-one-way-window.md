---
tags: [source, 渲染, 剔除, 阴影, infinity-nikki, unreal]
date: 2026-04-19
sources: 1
---

# Infinity Nikki — One-Way Window（simonschreibt.de / Simon Trümpler）

[[simon-trumpler]] 于 2025 年 2 月发表的 Game Art Tricks 拆解：在开放世界游戏《Infinity Nikki》里，Simon 发现房子一侧的窗户**看得到室内**，从另一侧的窗**却完全看不到「对穿」**，而阳光仍能透过房间照进地板。

## 摘要

Simon 和评论区共同推出一个合理猜想：外墙是**单面几何**，朝外那面正常渲染、朝内的背面被 back-face culling 丢掉，所以从外头第一扇窗看进去不会被「大背面」挡住。远处那扇窗所在的墙用离线 [[occlusion-culling|occlusion 体积]] 整体挡住，避免透视穿越建筑。阳光透进来是因为 shadow map 的投射者只用 **front-face**，背面不参与投影计算，所以单面墙不会给室内盖一块阴影。Simon 顺便回忆自己做《Sacred 2》时反向用了 back-face 投射，结果必须给所有桌椅底面补齐几何否则桌子会变「透光」——这一节是 [[shadow-caster-culling-front-back]] 的教科书案例。文章更新里还揭露 Nikki 用**基于 dot product** 而非视锥来关 NPC 动画，超宽屏下露馅。

## 关键要点

- 「单向窗户」= 单面外墙 + back-face culling 做遮挡
- 优势不仅是几何省面，更是省 overdraw、回避半透明排序、配合手工 occlusion volume
- Shadow map caster 选 front-face / back-face 是独立的工程决策
- 相机外动画剔除可能用 `dot(forward, npcDir)`，在 32:9 屏会出 bug

## 链接到的概念

- [[one-way-window-backface-culling]]
- [[shadow-caster-culling-front-back]]
- [[occlusion-culling]]
- [[overdraw]]
- [[simon-trumpler]]

## 原文

- 链接：https://simonschreibt.de/gat/infinity-nikki-one-way-window/
- 本地：`raw/articles/simonschreibt.de/2025-02-23_simonschreibt.md`
