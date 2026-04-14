---
tags: [source, shader, outline, unity, sdf]
date: 2026-04-14
sources: 1
---

# Animated Dotted Outline Shader in Unity（Linden Reid）

[[linden-reid]] 2017 年 12 月 24 日的 Unity shader 教程，把 [[cel-shader-outline|cel shader 的两 pass 描边]] 的 outline fragment shader 改造成"会沿着描边爬动的虚线"——整篇只改几行 fragment 代码，是她系列里最短最精的一篇。

## 摘要

延续此前 cel shader 的两 pass 结构：Pass 1 原模型 + stencil 写入，Pass 2 沿法线外推 + stencil masking。本文只动 Pass 2 的 fragment shader，分两步把纯色描边变成动画虚线。第一步用 `sin(_OutlineDot * distance(_SourcePos.xy, pos)) + _OutlineDot2`——`sin` 在正负之间周期性摆动，正段代表"画"、负段被 `clip` 丢掉——形成一圈一圈的实/虚同心环。参数 `_OutlineDot` 控制频率，`_OutlineDot2` 控制占空比。第二步用 `pos = input.pos.xy + _Time * _OutlineSpeed` 平移采样位置，由于 `sin` 是位置的函数，平移位置等价于平移相位，于是断线看起来沿 `_OutlineSpeed` 方向移动。作者强调这是屏幕空间距离场，相机旋转/远近会让密度变化。

## 关键要点

- 延用现有两 pass outline 管线，只改 outline fragment shader
- `sin(distance) + bias` + `clip` 产生断续描边
- `_Time * _OutlineSpeed` 平移位置等价于平移 sin 相位，实现动画
- 参考点 `_SourcePos` 让同心环从一点发散
- 完整代码在作者的 GitHub `Unity-Shader-Tutorials` 仓库

## 链接到的概念

- [[animated-dotted-outline-shader]]
- [[cel-shader-outline]]
- [[sdf-2d-primitives]]
- [[shaping-functions]]
- [[stencil-buffer]]
- [[linden-reid]]

## 原文

- 链接：https://lindenreidblog.com/2017/12/24/animated-dotted-outline-shader-in-unity/
- 本地：`raw/articles/lindenreid.wordpress.com/2017-12-24_animated-dotted-outline-shader-in-unity.md`
