---
tags: [source, rendering, shader, unity, post-processing]
date: 2026-04-14
sources: 1
---

# My take on shaders: Night time shader（Harry Alisavakis / Technically Art）

[[harry-alisavakis]] 于 2017 年 4 月发表的「My take on shaders」系列第二篇，在第一篇 [[unity-image-effect-basics]] 的框架上写一支把白天画面染成夜晚感的全屏后处理，用于他自己的游戏 Sling Toss。

## 摘要

作者把「night time」拆成三条可调的色彩操作——**降低饱和度、往蓝色偏移、整体变暗**，并声明只要三个都做才能骗过眼睛。实现上新加一个 `_NightTime` 滑杆（0.001~1），在 [[fragment-shader]] 里先 `tex2D` 取原色，用 Unity 内置的 `Luminance(col.rgb)` 算出灰度 `lum`，再 `lerp(col.rgb, fixed3(lum,lum,lum), _NightTime)` 把 RGB 向灰度推进——这就是「按权重抽饱和度」的等价实现；然后一行 `(output + _NightTime * fixed4(0, 0, 0.8, 1)) * (1 - _NightTime)` 同时做蓝色偏移和乘法式变暗，一次性把三个诉求揉进一个表达式。整篇文章等于一堂「用 lerp 调参数化后处理」的迷你示范，并顺手提醒读者：Sling Toss 里玩家角色之所以不受夜色影响，是因为他把角色放在独立相机独立 layer 上，后处理只挂到环境相机——这是 built-in 管线时代做选择性后处理最常用的土法。

## 关键要点

- `Luminance(rgb)` 是 Unity 内置的亮度函数（按 Rec.601/709 系数加权），可以当作「灰度参考值」
- 把 `lerp(col, luminance_gray, t)` 当作**手动饱和度控制**：`t=0` 原色、`t=1` 全灰
- 偏色用 `+ t * fixed4(0, 0, 0.8, 1)` 直接加在 RGB 上，变暗用 `* (1 - t)` 一行搞定，是最廉价的「色温 + 亮度」调整组合
- 三种效果必须同时用才能骗过眼睛——单独抽饱和会显得发灰、单独加蓝会显得假、单独变暗会显得只是关灯
- 用多相机分层（player cam vs world cam）+ 只给其中一个挂 image effect，是 built-in 管线下实现「角色不受后处理影响」的经典 workaround，URP/HDRP 时代应换成 Volume 层级或自定义 pass
- 这篇对应 `UnityObjectToClipPos`（Unity 5.6 起替代 `UNITY_MATRIX_MVP`）的过渡时期写法

## 链接到的概念

- [[night-time-tint-shader]]
- [[unity-image-effect-basics]]
- [[fragment-shader]]

## 原文

- 链接：<https://halisavakis.com/my-take-on-shaders-night-time-shader-introduction-to-image-effects-part-ii/>
- 本地：`raw/articles/halisavakis.com/2017-04-19_my-take-on-shaders-night-time-shader-introduction-to-image-e.md`
