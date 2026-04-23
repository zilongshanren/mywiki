---
tags: [source, bitsquid, rotation, animation]
date: 2026-04-19
sources: 1
---

# What is gimbal lock and why do we still have to worry about it?（Niklas Frykholm / Bitsquid, 2013-03-15）

[[niklas-frykholm]] 2013 年 3 月的博客，把 gimbal lock 还原为一个表示+插值问题，并解释动画师为何把这个问题"永久"带进了引擎。

## 摘要

文章先澄清 gimbal lock 这个机械学名词在计算机里的误导性：引擎里没有东西被"锁住"，任意姿态都能用某套欧拉角表达。真正的问题是**表示不唯一且在奇异点附近欧拉角之间不连续**——当中间那个角靠近 90°、两个旋转轴重合时，两个现实中很近的姿态对应的欧拉角会差 180°，关键帧之间做线性插值就会多出一次翻滚。标准修法是插值前把关键帧转成四元数，slerp 没有奇异点；但四元数始终走最短路径，单帧超过 180° 的"多圈旋转"需要先提高采样率再导出。然而，动画师需要的 UI 是**可编辑的曲线**——四元数分量画成曲线没有语义，能编辑的曲线只能来自欧拉角，gimbal lock 因此被锁在 DCC 流程里赶不走。Stingray cutscene 系统因而标配轴序切换、quaternion 往返、Euler filter 等常规规避手段。

## 关键要点

- gimbal lock 是欧拉角表示+插值的奇异，不是"旋转能力"的缺失
- XYZ、XZX 等 12 种欧拉轴序都有各自的奇异点；切轴序是动画师常用的缓解手段
- 四元数 slerp 避免奇异，但只能走最短路径（单帧 >180° 要加采样）
- 动画曲线编辑器使欧拉角无法被完全淘汰，引擎必须提供 Euler filter 等工具
- 作者推荐用 `euler_xyz[0]` 这样带轴序的变量名，不要用含义模糊的 pitch/yaw/roll

## 链接到的概念

- [[gimbal-lock-euler-interpolation]]
- [[3d-rotation-math]]
- [[exponential-map-rotations]]

## 原文

- 链接：https://bitsquid.blogspot.com/2013/03/what-is-gimbal-lock-and-why-do-we-still.html
- 本地：`raw/articles/bitsquid.blogspot.com/2013-03-15_what-is-gimbal-lock-and-why-do-we-still-have-to-worry-about.md`
