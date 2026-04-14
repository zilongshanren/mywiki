---
tags: [source, shader, shadergraph, 深度, 透明物体]
date: 2026-04-14
sources: 1
---

# Scene Color & Depth Nodes（Cyan）

[[cyanilux|Cyan]] 2019 年 6 月发表的 Shader Graph 教程，讲解两个特殊节点——**Scene Color** 和 **Scene Depth**——在不同 Unity 渲染管线（Built-in / LWRP / URP / HDRP）下的行为差异、启用条件、以及典型使用场景。

## 摘要

Scene Color 节点在 URP 下采样 `_CameraOpaqueTexture`——只包含不透明物体的结果，要求 URP Asset 上启用 Opaque Texture 选项，并且使用它的 shader 必须是 Transparent 模式（或 Render Queue ≥ 2501）。HDRP 则用 `_ColorPyramidTexture`（带 mip），还有一个 HD Scene Color 节点访问其它 LOD。这个节点的 UV 默认是屏幕坐标，偏移它就能做**折射**（玻璃、水、热浪）。

Scene Depth 节点采样 `_CameraDepthTexture`，URP 下需要启用 Depth Texture 选项——而且在 URP v7.3 时期有个 bug：Camera 必须同时启用 Post Processing，depth pass 才会真的跑。节点有 3 档采样模式：**Raw**（原始非线性深度，可能是 reversed-Z）、**Linear01**（通过 `Linear01Depth` 转成 `[0,1]`，仅透视投影）、**Eye**（通过 `LinearEyeDepth` 转成世界单位，仅透视投影）。正交投影因为 depth buffer 天然线性，只能用 Raw。文章还给出了 `Linear01Depth` / `LinearEyeDepth` 函数的 HLSL 定义以及 `_ZBufferParams` 的四个分量在普通/反转 Z 下的含义。

最后讲到一个关键 trick：用 `Screen Position` 节点（Raw 模式）的 W/A 分量可以拿到**当前片段自己的**深度，和 Scene Depth（场景背景的深度）相减就得到深度相交距离——水面泡沫、雾墙、力场、粒子软边都是同一技术。

## 关键要点

- Scene Color 在 URP 下只包含不透明物体；使用它的 shader 必须避免写入它自己读的 buffer（所以必须是 Transparent 或 Render Queue ≥ 2501）。
- Scene Depth 的 Raw 模式在透视投影下是**非线性**的，还可能是 **reversed Z**——近面是 1、远面是 0。
- Linear01 / Eye 模式只能用于透视投影；正交相机的 Z-buffer 本就线性，必须用 Raw。
- URP v7.3 的已知 bug：Camera 上的 Post Processing 开关同时控制 depth pass 的生成——和它作为后处理开关的语义不符。
- 深度相交 = `LinearEyeDepth(Scene Depth) - LinearEyeDepth(Screen Position W)`，这是水面、雾墙、力场、粒子软边、深度淡化等一大批效果的共同基石。

## 链接到的概念

- [[scene-color-depth-nodes]]
- [[z-buffer]]
- [[reversed-z]]

## 原文

- 链接：https://cyangamedev.wordpress.com/2019/06/01/scene-color-depth-nodes/
- 本地：`raw/articles/cyangamedev.wordpress.com/2019-06-01_scene-color-depth-nodes.md`
