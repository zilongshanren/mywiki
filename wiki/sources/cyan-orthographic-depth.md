---
tags: [source, shader, shadergraph, 深度, 正交相机]
date: 2026-04-14
sources: 1
---

# Orthographic Depth（Cyan）

[[cyanilux|Cyan]] 2020 年 3 月发表的 Shader Graph 教程，针对**正交相机**下的 Scene Depth 节点行为给出完整的处理方案——包括平台差异（reversed Z）的判断、深度差技巧的正交版、以及世界坐标重建的正交版。这是他几篇 shader breakdown（水面、雾墙）反复用到的「深度」技巧体系的补完。

## 摘要

文章核心论点：**正交投影下深度 buffer 本来就是线性的**，所以不能用 `Linear01Depth` / `LinearEyeDepth`（这两个函数假设 input 是透视的双曲深度，对线性输入会给出错误结果）。Scene Depth 节点必须用 **Raw 模式**。

但 raw 值是 0-near-1-far 还是 1-near-0-far 取决于平台是否启用 reversed Z。处理方法：用 **Camera 节点**的 `Z Buffer Sign` 输出（对应 `_ProjectionParams.x`，返回 `-1` 或 `1`）做 Branch；reversed 平台对 raw 取 One Minus；之后 `Lerp(near plane, far plane)` 转到「相机空间单位」（等价于透视下的 `LinearEyeDepth`）。

文章重点示范了两个常见技巧的正交版本：

- **Depth Difference**（深度相交）：透视下用 `Screen Position(Raw).w` 拿当前片段的 view-space 深度；正交下 `w = 1` 没用，必须用 `Screen Position(Raw).z`，但这是 NDC 空间的 `[-1, 1]`（OpenGL）或 `[0, 1]`（D3D/Metal）。Cyan 用一个 `GetClipValues_float` Custom Function 返回 `(UNITY_NEAR_CLIP_VALUE, UNITY_RAW_FAR_CLIP_VALUE)`：D3D 平台是 `(1, 0)`，OpenGL 平台是 `(-1, 1)`。然后 `Lerp(NEAR, FAR)` 把 NDC z 重新映到 `[0, 1]`。
- **Reconstruct World Position from Depth**：透视版用 `View Direction / fragmentDepth * Scene Depth` 加 Camera Position；正交版要走 NDC→view→world 的反变换（因为正交相机所有像素的 view direction 都一样），文章给了完整 graph。

文章顶部加了一段更新提示：Scene Color 节点在新版 Shader Graph 里有更新，最新版本去看 [cyanilux.com/tutorials/depth/#orthographic-scene-depth](https://www.cyanilux.com/tutorials/depth/#orthographic-scene-depth)。

## 关键要点

- 正交投影深度 buffer **本来就是线性**——不能用 Linear01/Eye 模式，必须用 Raw。
- 用 Camera 节点的 `Z Buffer Sign` 输出判断是否 reversed Z，reversed 时对 raw 取 One Minus。
- 正交模式下 `Screen Position(Raw).w = 1`，没法用透视那套；要用 `.z` 经过 `UNITY_NEAR_CLIP_VALUE` / `UNITY_RAW_FAR_CLIP_VALUE` 重映射。
- 世界坐标重建在正交下要走 NDC → view → world 的完整反变换，比透视版复杂。
- 移动端老平台正交相机的 near/far 跨度太大会有 banding，要么收紧 clip planes，要么用 32-bit depth。

## 链接到的概念

- [[orthographic-depth]]
- [[scene-color-depth-nodes]]
- [[reversed-z]]
- [[coordinate-spaces]]

## 原文

- 链接：https://cyangamedev.wordpress.com/2020/03/05/orthographic-depth/
- 本地：`raw/articles/cyangamedev.wordpress.com/2020-03-05_orthographic-depth.md`
