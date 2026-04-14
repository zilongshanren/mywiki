---
tags: [source, rendering, shader, post-processing, edge-detection, outline, unity]
date: 2026-04-14
sources: 1
---

# Sobel Outline with Unity Post-Processing（Steven Sell / Vertex Fragment）

[[steven-sell]] 发表于 2019 年 9 月的 Unity 后处理教程续篇，把上一篇"表面角剪影"失效的平面场景替换成基于 [[sobel-edge-detection|Sobel 算子]] 的深度+法线差分描边。

## 摘要

Sobel 算子是一种经典的二维边缘检测卷积核，通过对一个像素的上下左右邻居做差并求绝对和来估计局部梯度。文章把这个算子作为 Unity 后处理效果实现两次：一次作用在 `_CameraDepthTexture`（**深度 Sobel**，擅长外轮廓和平面边），一次作用在 `_CameraGBufferTexture2`（**法线 Sobel**，擅长凹陷和圆转边）。两者的结果分别用 `pow(sobel * multiplier, bias)` 调整——multiplier 线性缩放，bias 做 gamma 形状的降噪——然后求和作为描边掩膜，用它在 `_MainTex` 和 outline color 之间 `lerp`。

文章同时给出了**排除特定几何**的两种做法：forward 场景里用一个专门的 `OutlineOcclusionCamera` 只渲染某几个 layer 的深度到 `_OcclusionDepthMap`，供 shader 读；deferred 场景（例如草地）则用一个讨巧的信号位——把 normal 的 `.w` 写成 `0.0`，让 Sobel shader 认出来跳过。作者同时指出 Sobel 本身不抗锯齿，最好配合 SMAA 等后处理 AA。最后作为 "其他 Sobel 应用" 一节，还演示了把 Sobel 当作均匀屏幕模糊以及用它从高度图生成法线图。

## 关键要点

- **为什么采样 4 个邻居**（上下左右）：这是能在全方向上产生描边所需的**最少采样数**，加到 8 邻居对结果提升很小却翻倍开销。
- **为什么深度和法线都要采**：深度在平面交界和外轮廓上表现最佳，法线在凹陷边和同深度的结构边上表现最佳——两者互补。
- **`pow(sobel * mul, bias)` 的作用**：mul 是线性缩放（对远平面很远的场景尤其有用），bias 通过 gamma 曲线把细噪声压平但保留强边。
- **注入点选 `BeforeStack`**：让描边能被内建 AA 后续平滑，否则描边边缘会非常硬。
- **`LinearEyeDepth`** 必须用来解 `_CameraDepthTexture` 里非线性编码的深度；这个函数在 `com.unity.postprocessing` v2.1.7 里签名从 `float4 → float4` 改成了 `float → float`。
- **排除几何**的两条路径：forward 用 `OutlineOcclusionCamera` + `_OcclusionDepthMap`；deferred 用 `normal.w = 0` 作为跳过标志。
- **副作用应用**：Sobel 也能当**屏幕模糊**（把 Sobel 直接输出为结果）和**高度图转法线图**（水平差分作 dx，竖直差分作 dy，叠加一个可配 strength）。
- 作者与 [[cel-shader-outline]] 的对比：Sobel 是**屏幕空间纯 image effect**，不依赖 mesh manifold 性质；法线 extrude + stencil 是**几何描边**，需要额外 draw call 但描边粗细完全受控。

## 链接到的概念

- [[sobel-edge-detection]]
- [[surface-angle-silhouette]]
- [[cel-shader-outline]]
- [[deferred-rendering]]

## 原文

- 链接：https://www.vertexfragment.com/ramblings/unity-postprocessing-sobel-outline/
- 本地：`raw/articles/vertexfragment.com/2019-09-12_sobel-outline-with-unity-post-processing.md`
- 配套仓库：https://github.com/ssell/UnitySobelOutline
