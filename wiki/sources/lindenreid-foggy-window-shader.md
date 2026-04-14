---
tags: [source, unity, shader, blur, grabpass]
date: 2026-04-14
sources: 1
---

# Foggy Window Shader in Unity（Linden Reid）

[[linden-reid]] 2018 年 11 月的综合教程，把三种常用技巧——GrabPass、可分离 Gaussian blur、把时间戳编码进纹理通道——串起来做一个"可以用鼠标擦出晴朗区域、一段时间后雾气重新聚拢"的可交互窗户 shader。

## 摘要

教程分三部分。第一部分讲 GrabPass：用 `GrabPass { "_BGTex" }` 把窗户物体后方的 backbuffer 像素抓成纹理，用 `ComputeGrabScreenPos` 算正确的屏幕空间 UV，再跑 Gaussian blur + 色调 tint。作者坦言用的是"懒版" blur——没做正经的两 pass 分离卷积，而是在同一 pass 里把水平和垂直 blur 结果相加，然后乘 tint 色掩盖亮度翻倍问题。第二部分建一张 `TextureFormat.RFloat` 的 `Texture2D`，用 `OnMouseDrag` + `ScreenPointToRay` 把鼠标击中位置以半径 brush 的方式写入纹理。第三部分是关键 trick：写入的不是颜色，而是 `Time.timeSinceLevelLoad`——也就是"这个像素最后一次被擦过的时间戳"。shader 读回 R 通道，用 `age = _Time.y - timeDrawn` / `percentMaxAge = age / _MaxAge` 算当前雾气强度，驱动 blur 半径和色调在 "clear" 与 "fog" 之间插值。结果是"擦一下就清晰，过一会儿自己糊回来"的连续动效。

## 关键要点

- GrabPass 的成本是一次全屏拷贝，用一次贵一次——现代 URP/HDRP 改用 `_CameraOpaqueTexture`。
- 高斯核可分离这个性质没被作者"正确"使用，这是**教学取舍**：把教程焦点留给第 3 部分的时间编码。
- `TextureFormat.RFloat`（32-bit 单通道）是存时间戳的最低精度要求，普通 `RGBA32` 会迅速溢出。
- 纹理不是颜色——它是 per-pixel float 存储，任何"每像素一个数字"的状态都可以塞进去。
- 算法全文：`percentMaxAge = saturate((_Time.y - timeDrawn) / _MaxAge)`，然后 `blurRadius = _BlurRadius * percentMaxAge`、`color = lerp(clear, fog, percentMaxAge)`。

## 链接到的概念

- [[unity-grabpass-blur]]
- [[texture-encoded-state]]
- [[fragment-shader]]
- [[alpha-blending]]
- [[linden-reid]]

## 原文

- 链接：https://lindenreidblog.com/2018/11/19/foggy-window-shader-in-unity/
- 本地：`raw/articles/lindenreid.wordpress.com/2018-11-19_foggy-window-shader-in-unity.md`
