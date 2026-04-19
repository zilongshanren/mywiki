---
tags: [source, unity, shadergraph, urp, zelda]
date: 2026-04-19
sources: 1
---

# Zelda Recall Rune in Unity URP（danielilett.com / Daniel Ilett）

[[daniel-ilett]] 2025 年 10 月的 Unity URP 教程：复刻《王国之泪》里 Recall 时之逆转的视觉效果。

## 摘要

把物体过去位置上的半透明残像叠在现在位置上，用 mask RT 记录受影响物体，再用噪声屏幕擦除的 shader 让残像有流动感；最后配合屏幕边缘的扫描 outline 传达时间回溯的感觉。技术栈：URP `DrawRendererList` + override material 单独画一层 mask 到 RT，Fullscreen Graph 做边缘描边与噪声擦除。

## 关键要点

- `DrawRendererList` + override material + `ShaderTagId` 是 URP 自绘 layer mask 的官方方式
- 把受控物体渲染到专属 RT，shader 采样 RT 再叠回主画面
- 屏幕擦除的噪声动画用时间偏移 + step 阈值实现

## 链接到的概念

- [[draw-renderer-list-mask-urp]]
- [[world-scan-shader-effect]]

## 原文

- 链接：<https://danielilett.com/2025-10-11-zelda-recall-rune-in-unity-urp/>
- 本地：`raw/articles/danielilett.com/2025-10-11_zelda-recall-rune-in-unity-urp.md`
