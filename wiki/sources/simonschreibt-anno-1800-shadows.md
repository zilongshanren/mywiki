---
tags: [source, 渲染, 阴影, 美术方向, anno-1800]
date: 2026-04-14
sources: 1
---

# Anno 1800 — Shadows of Beauty（simonschreibt.de / Simon Trümpler）

[[simon-trumpler]] 于 2025 年 2 月发表的 VFX 观察：在 **《Anno 1800》** 这款城市建造游戏里，太阳的位置其实是锁死相对于相机的，而不是世界坐标系。结果是旋转相机时阴影永远落在同一个方向——看起来像一个加速的日晷。

## 摘要

Simon 发现 Anno 1800 默认把太阳位置设为相机的函数：无论玩家如何旋转视角，建筑的阴影始终从左上往右下落。游戏也提供一个「真实太阳」选项让太阳固定在世界里做对照。直觉告诉我们「真实」才好，但 Simon 演示了反例：当玩家转到某个角度，世界锁定的太阳会让阴影全部落到相机背后，此时画面里几乎看不到阴影，整个场景变得像引擎的 unlit 模式一样扁平。相机相对的太阳则保证任何视角下构图都有稳定的光影节奏。评论区补充这个技巧至少可以追溯到 2006 年的 Anno 1701，并在 Islanders、Islands&Trains 这类 low-poly 建造游戏里被独立重新发明——最早是为了掩盖地形接缝，但留下来是因为画面始终好看。这是一个 **把光照当演出工具而非物理仿真** 的典型小 trick。

## 关键要点

- 太阳位置可以是相机相对的，而不是固定在世界坐标
- 世界固定太阳 + 自由相机会遇到「阴影全在相机背后」的构图灾难
- 相机相对的太阳让阴影方向在任何视角下都一致
- 物理正确 ≠ 美术正确；城市建造类游戏应优先构图
- Anno 系列至少从 2006 年就在用；Islanders、Islands&Trains 等 low-poly 建造游戏同理

## 链接到的概念
- [[camera-relative-sun-shadows]]
- [[shadow-mapping-basics]]
- [[simon-trumpler]]
- [[thomas-poulet-anno-1800-frame]] — Anno 1800 完整帧分析（同一引擎不同视角）

## 原文

- 链接：https://simonschreibt.de/gat/anno-1800-shadows-of-beauty/
- 本地：`raw/articles/simonschreibt.de/2025-02-12_simonschreibt.md`
