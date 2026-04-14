---
tags: [source, 渲染, 反射, 立方体贴图, ibl]
date: 2026-04-14
sources: 1
---

# Parallax-corrected cubemapping with any cubemap（Kostas Anagnostou / Interplay of Light）

[[kostas-anagnostou|Kostas Anagnostou]] 2013 年 4 月的一篇实战笔记：把 Sébastien Lagarde 的 **视差修正 cubemap** 技术用到一个**不是为当前场景烘焙**的通用 cubemap 上，给非正方形房间的玻璃加一点接地的反射。

## 摘要

视差修正 cubemap 通过给反射探针绑一个 AABB，沿反射方向求交再重映射采样方向，让原本漂浮于无穷远的 cubemap 反射「锚定」到场景空间。Lagarde 2012 年的文章里的公式**假设 cubemap 是专为这块空间烘焙**的——烘焙阶段把非正方房间压缩成立方体，采样阶段再解压回来。Kostas 的项目里只有一张通用的模糊 cubemap 可用，房间又是 `2x × x × 0.5x` 的非正方形，直接套原版会导致明显的扭曲反射。他的 hack 是取三边最短的那条做基准，算出一个 `BoxScale = minDim / BoxDiff` 的补偿向量，把修正后的反射方向再乘一次。效果上 cubemap 内容仍然和房间不匹配（因为从头到尾都是通用的），但不再脱节于摄像机运动。评论区 Lagarde 指出原代码本就支持任意 AABB/OBB——这个区分其实是在讨论「cubemap 专烘焙 vs. cubemap 泛用」两种不同语境。

## 关键要点

- Parallax-corrected cubemap 的核心公式：沿反射方向做 AABB slab test，取最远交点，以中心→交点为新采样方向
- `±inf` / `x/0` 的自然退化让 slab test 在 GPU 上几行代码就能写完
- Lagarde 原版**假设 cubemap 为该空间专烘焙**，AABB 修正是「解压」
- 非专烘焙 cubemap + 非正方房间 → 需要额外的 `BoxScale` 均匀化
- Hack 是把三边最短那条当基准，按比值缩小反射向量
- 解决的是「反射跟不上摄像机移动」而不是「反射内容匹配场景」
- 原作者评论里澄清原版本就支持任意 AABB / OBB，区别在于 cubemap 是否为场景烘焙

## 链接到的概念

- [[parallax-corrected-cubemap]]
- [[environment-probe-placement]]
- [[physically-based-shading]]

## 原文

- 链接：https://interplayoflight.wordpress.com/2013/04/29/parallax-corrected-cubemapping-with-any-cubemap/
- 本地：`raw/articles/interplayoflight.wordpress.com/2013-04-29_parallax-corrected-cubemapping-with-any-cubemap.md`
