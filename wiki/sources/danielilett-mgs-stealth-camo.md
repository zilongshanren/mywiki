---
tags: [source, unity, shadergraph, 透明, 折射, 游戏复刻]
date: 2026-04-14
sources: 1
---

# MGS Stealth Camo in Shader Graph（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] 2024 年 3 月的教程，用 Unity URP + Shader Graph 复刻《Metal Gear Solid 2》的 **Stealth Camo**（潜行迷彩）效果。Snake 披上后整个人像一个半透明的绿色果冻，背景透过他时会有轻微的波纹扭曲。

## 摘要

作者把效果拆成两件事：**"果冻感" = 半透明 + 自定义颜色混合**；**"折射感" = 扭曲背景像素**。实现用 Shader Graph 的 `Scene Color` 节点读取 `_CameraOpaqueTexture`——这是 URP 在画所有不透明物体之后、画透明物体之前的一张 copy，前置条件是在 URP Asset 上勾选 Opaque Texture（所有 quality 档都要勾）。shader 本身建在 Unlit 模板上，Graph Settings 里 Surface Type 必须是 Transparent，否则 shader 会在 opaque pass 里执行，把自己写进 `_CameraOpaqueTexture` 再读到自己。三个 property：`Base Color`（颜色 + alpha 做混合比）、`Noise Size`、`Noise Strength`。Alpha 输出硬接 1，不让 Unity 自己做 alpha blend——由 shader 手动 `Lerp(SceneColor, BaseColor, BaseColor.a)`。扭曲部分用 `Simple Noise` 吃 `Noise Size` 输出 [0, 1] 灰度，`Remap` 到 [-1, 1]，乘 `Noise Strength` 得偏移量，加在 `Screen Position` 上作为 `Scene Color` 的 UV 输入。图小到几乎一眼就能看完，但展示的是 URP 屏幕空间效果的最基本骨架。

## 关键要点

- URP 下想读场景颜色必须勾 **Opaque Texture**，三个 quality 档位都要勾；`Scene Color` 节点底层采样的是 `_CameraOpaqueTexture`，它的时序是"所有不透明物体渲染完 → copy → 透明物体渲染"。
- shader 的 Surface Type **必须是 Transparent**，否则 `Scene Color` 读到的是自身（透明物体在 opaque copy 之后才渲染）。
- **Alpha 输出写常数 1**，避免 Unity 的 alpha blend 和 shader 手动 `Lerp` 双重混合。
- Simple Noise 的 [0, 1] 输出必须 **`Remap` 到 [-1, 1]**，否则扭曲只能往屏幕左下方推，不是全方向。
- `Scene Color` 的 UV 默认是 `Screen Position`，偏移这个 UV 就能实现折射；这是"透过物体看背景"效果的通用骨架——玻璃、水面、热浪、力场都是同一个架构换扰动源。
- 教程采用 Unlit 模板做 simplicity；想要光照交互也可以用 Lit 模板。
- 限制：`Scene Color` 只含 opaque 像素，所以披 Camo 的 Snake 后面的**半透明粒子不会被扭曲进来**。

## 链接到的概念

- [[mgs-stealth-camo-shader]]
- [[scene-color-depth-nodes]]
- [[classic-shader-noise]]
- [[shader-graph-lighting-primer]]

## 原文

- 链接：<https://danielilett.com/2024-03-26-tut7-9-mgs-stealth-camo/>
- 本地：`raw/articles/danielilett.com/2024-03-26_mgs-stealth-camo-in-shader-graph.md`
