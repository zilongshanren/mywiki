---
tags: [source, graphics, coordinate-system, reference]
date: 2026-04-19
sources: 1
---

# 3D Software Coordinate System Table（Pekka Väänänen / 30fps.net）

[[pekka-vaananen]] 2023 年 3 月发布并持续维护的一张速查表，列出主流引擎、图形 API、DCC 软件在 **view space** 与 **world space** 的「Right / Up / Forward」约定和手性。

## 摘要

这是一张对照表，不是教程：左手/右手系、哪根轴是 Up、Forward 指向哪边——每家引擎都不一样。OpenGL、Three.js、ARKit、Maya、Houdini 在 view space 上一致（+x 右 / +y 上 / -z 前，右手）；Direct3D 与 Unity 用 +z 前、左手。世界空间里 Blender、3ds Max、Quake 全都把 **Z 当 Up**，而 Unreal 干脆用 `Forward = +X, Right = +Y, Up = +Z` 的左手系，glTF 则用独特的 `-x` 当 Right。作者提醒「Right / Forward」直觉上对应地理的东 / 北，"Up" 背离重力。

## 关键要点

- view space 的 Forward 轴正负号由手性决定：右手系多用 -z，左手系用 +z。
- Unreal 的轴分配在主流引擎里最反常，资产迁移时最容易踩坑。
- glTF 的 `-x` right 是规范特例，容易误认成文件错误。
- 这张表的价值在于「**一眼看全三轴 + 手性**」，而不只是手性。

## 链接到的概念

- [[coordinate-system-table]]
- [[coordinate-spaces]]

## 原文

- 链接：<https://30fps.net/xyz/>
- 本地：`raw/articles/30fps.net/2023-03-17_3d-software-coordinate-system-table.md`
