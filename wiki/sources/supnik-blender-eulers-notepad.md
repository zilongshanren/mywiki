---
tags: [source, blender, euler-angles, asset-pipeline, x-plane]
date: 2026-04-19
sources: 1
---

# Blender Notepad - Eulers（Ben Supnik / Hacks of Life）

[[ben-supnik]] 2015 年 11 月的一则"备忘录式"短帖，把 Blender 里 "XYZ Euler" 的约定还原清楚，顺带记下 Blender 2.49 OBJ exporter 的历史 bug。

## 摘要

Blender 用 "XYZ Euler" 表示三个欧拉角，含义是：Z 是 up（Y 指向远方，右手系），三次旋转按 X→Y→Z 顺序、绕**全局坐标轴外旋**应用。关键推论：**最后施加的 Z 旋转不受前两次影响**，而**先施加的 X 被后面两者影响**。从飞行员视角看等同于"先 yaw、再 roll、再 pitch"——pitch 放最后违背真实飞机操纵习惯。匹配 X-Plane 姿态语义应选 YXZ。X-Plane OBJ 的 `ANIM_rotate` 只有局部变换——Blender 全局 XYZ 导出到 OBJ 必须反向写 Z→Y→X。Blender 2.49 exporter 把欧拉分解在 X-Plane 坐标系里做，于是 Blender XYZ 里"yaw 不变"的性质在 OBJ 里变成"roll 不变"——修复需要在源坐标系里分解、再坐标变换。通用教训：**Euler 分解只在同坐标系里无歧义**，跨坐标系要么先转成坐标无关表达（矩阵/四元数）、要么完成分解再变换。

## 关键要点

- "XYZ Euler" = Z-up + 三次绕全局轴（extrinsic）依序旋转
- 外旋 XYZ ≡ 内旋 ZYX（顺序反转 + 内外旋对调）
- Blender XYZ 的"yaw 不变"与 X-Plane OBJ 的"roll 不变"是同一性质在不同坐标系中的表现
- 导出到局部变换链（X-Plane OBJ）时，Blender 全局顺序要反转
- Blender 2.49 exporter 在错误坐标系里做 Euler 分解是一条经典跨坐标系陷阱
- 要匹配飞行语义（yaw / roll / pitch 顺序），Blender 里应选 YXZ

## 链接到的概念

- [[blender-euler-extrinsic-xyz-export]]
- [[3d-rotation-math]]
- [[gimbal-lock-euler-interpolation]]
- [[exponential-map-rotations]]
- [[asset-exchange-format-strategy]]
- [[ben-supnik]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2015/11/blender-notepad-eulers.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2015-11-21_blender-notepad-eulers.md`
