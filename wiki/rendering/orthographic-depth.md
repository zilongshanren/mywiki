---
tags: [shader, shadergraph, 深度, 正交相机, 渲染]
date: 2026-04-14
sources: 1
---

# 正交相机的 Scene Depth（线性 buffer + 平台差异）

[[scene-color-depth-nodes|Scene Depth 节点]] 的三档采样模式 Raw / Linear01 / Eye 文档里写得很清楚——但前提是相机是**透视投影**。换到 **Orthographic** 投影，整个语义颠倒：**深度 buffer 本来就是线性的**，`Linear01Depth` / `LinearEyeDepth` 反而会把它折坏。这是 2.5D / 等距 / 顶视角 / 侧视角游戏做基于深度的效果（水面相交、雾、轮廓、深度淡化）时最容易栽的坑之一。

## 透视 vs 正交：buffer 含义不同

透视投影下的深度 buffer 存的是 clip-space 的 `z/w`，是个**双曲**函数——近裁剪面附近精度高、远裁剪面附近精度低（这正是 [[reversed-z|reversed Z]] 想反转的精度分布）。Shader Graph 的 Linear01 / Eye 模式调用 `Linear01Depth` / `LinearEyeDepth`，本质上是把这个双曲扭曲解开。

正交投影下没有透视除法（`w = 1`），clip-space `z` 和「相机到片段的距离」之间是**纯线性**关系。深度 buffer 直接存的就是 `[0, 1]` 内的线性值——但是！具体是 `0 = 近, 1 = 远` 还是 `0 = 远, 1 = 近` 取决于平台是否启用 reversed Z。这意味着不能直接用 `Linear01Depth`（它假设 input 是双曲），必须**用 Raw 模式**然后自己处理平台差异。

## 平台差异的处理

正交模式下的标准做法是：

1. Scene Depth 设为 **Raw**。
2. 用 **Camera 节点** 的 `Z Buffer Sign` 输出（对应 `_ProjectionParams.x`）做条件分支：返回 `-1` 表示当前平台用 reversed Z，`1` 表示正常。
3. 在 reversed-Z 平台上对 raw 深度做 **One Minus**，让 `0 = 近, 1 = 远` 在所有平台一致。

得到一个 `[0, 1]` 的统一线性深度后，通常还要用 **Lerp(near clip, far clip, depth)** 转换到「相机空间单位」——这一步等价于透视投影下的 `LinearEyeDepth`。Camera 节点直接给出 `Near Plane` 和 `Far Plane` 作为输入。

## 深度相交 / 深度差技巧的正交版本

[[scene-color-depth-nodes|深度相交]] 是水面泡沫、雾墙、力场最常用的技巧——透视模式下用 `Screen Position` 节点（Raw）的 `W/A` 分量当作「当前片段自己的 view-space 深度」，和 Scene Depth 做差。这个 `W` 分量来自 perspective divide，所以正交模式下它就是 `1`，没用了。

正交模式下要拿当前片段深度，必须用 `Screen Position` 的 **B/Z** 分量——这是 NDC 空间下的 `z`，范围 `[-1, 1]`（OpenGL）或 `[0, 1]`（Direct3D / Metal / 主机）。这是为什么 Cyan 在文章里特意写一个 `GetClipValues_float` Custom Function：用 `UNITY_NEAR_CLIP_VALUE` 和 `UNITY_RAW_FAR_CLIP_VALUE` 两个宏返回一个 Vector2，告诉 shader 当前平台的近/远裁剪值。然后用 `Lerp(NEAR, FAR, depth)` 把 NDC z 映射回 `[0, 1]`：

- D3D / Metal / 主机：`NEAR = 1, FAR = 0`（reversed）
- OpenGL / GLES：`NEAR = -1, FAR = 1`（不 reversed）

把这个值再用 `Lerp(camera near, camera far)` 转到 view-space 距离，最后和 Scene Depth 转出来的 view-space 距离相减——就得到了正交版本的「片段到背景物体的深度差」，可以做泡沫、淡入淡出、深度雾等所有透视模式下的效果。

## 从深度重建世界坐标

「[[scene-color-depth-nodes|Reconstruct World Position from Depth]]」在透视模式下相对简单：用 `View Direction / fragment depth` 把方向归一化、再 `* Scene Depth` 得到偏移、最后加到 `Camera Position`。正交模式下这条公式不能用——所有像素的 view direction 都是相机的 forward 向量，没有「从相机出发的射线」的概念。

正交版本的世界坐标重建要走 **clip space 反推**：从 NDC 坐标 `(screen.xy * 2 - 1, depth)` 出发，用相机的 inverse view-projection matrix 变回世界空间。Shader Graph 里同样需要把 raw depth 经过 reverse-Z 处理后塞进 NDC.z，再经过 `Transform` 节点反变换。Cyan 在文章里给出的 graph 把这些步骤都展开了——节点很多但思路是机械的：clip-space → view-space → world-space。

## 精度坑

在 OpenGL ES 等老移动端平台上，正交相机的 `[Near, Far]` 跨度太大（例如几千个 unit）会导致 depth buffer 出现明显 banding——表现为深度淡化的地方有「台阶」状色带。这不是 shader 的问题，是 depth buffer 本身的位深不够。解决方法是把 near/far 收紧到实际场景需要的范围，或者用 32-bit depth format。

## 相关

- [[scene-color-depth-nodes]]
- [[reversed-z]]
- [[z-buffer]]
- [[coordinate-spaces]]
- [[depth-texture-silhouette]]
- [[mvp-transform]]

## Sources

- [[sources/cyan-orthographic-depth]]
