---
tags: [source, rendering, shader, post-processing, outline, unity]
date: 2026-04-14
sources: 1
---

# Surface Angle Silhouette with Unity Post-Processing（Steven Sell / Vertex Fragment）

[[steven-sell]] 发表于 2019 年 9 月的教程，演示如何在 Unity 延迟渲染管线里用 Post Processing v2 stack 自定义一个后处理效果，并以"表面角剪影"作为示例。

## 摘要

文章分两层。第一层是**如何在 Unity 延迟管线里写一个自定义后处理**：安装 `com.unity.postprocessing` 包、给相机挂 `Post Process Layer`、场景里放 `Post Process Volume`，然后用两个 C# 类——`PostProcessEffectSettings` 声明参数、`PostProcessEffectRenderer<T>` 实现 `Render` 方法——把 shader blit 到全屏三角形。里面讲清了 `PostProcessEvent`（`BeforeTransparent` / `BeforeStack` / `AfterStack`）三个注入点的意义和 GBuffer 的四张 texture 分别是什么（`_CameraGBufferTexture0/1/2/3`）。第二层是**表面角剪影算法本身**：`edge = 1 - abs(dot(V, S))`，其中 V 是指向相机的方向、S 是表面法线。由于透视投影下相机方向不是统一常量，文章展示了如何在 vertex shader 里用 `_ViewProjectInverse` 把 NDC 坐标反投影回世界空间得到 per-pixel 的"local camera direction"，并且顺带给出了从深度 + camera ray 反推 world position 的方法。最后通过 `_OutlineThickness`、`_OutlineDensity`、`_OutlineColor` 三个参数调出从细高光到粗漫画描边的各种效果。作者自己承认该法对平面物体失效，在下一篇文章里改用 Sobel 边缘检测。

## 关键要点

- **Unity Post Processing v2 自定义效果**的两个类套路：`PostProcessEffectSettings`（参数+注入点） + `PostProcessEffectRenderer<T>`（实际 blit）。
- **`BeforeTransparent` / `BeforeStack` / `AfterStack`** 决定了自定义 pass 插在内建 AA/DoF 等效果之前还是之后，对结果的视觉链很关键。
- GBuffer 布局：`_CameraGBufferTexture0 = {diffuse.rgb, occlusion}`、`_CameraGBufferTexture1 = {specular.rgb, roughness}`、`_CameraGBufferTexture2 = {normal.rgb, unused}`、`_CameraGBufferTexture3 = cumulative lighting`。normal 需要 `*2-1` 解码。
- **表面角剪影公式**：`1 - abs(dot(V, S))`，V 指向相机、S 是表面法线。点积绝对值让凹凸两面都能识别。
- 在透视投影下**相机方向不是常量**，必须用 `_ViewProjectInverse` 把每个像素的 UV 反投影回世界空间再减去 `_WorldSpaceCameraPos`，这是一个可复用的 camera-ray 反投影套路。
- `worldPos = cameraDir * LinearEyeDepth(depth) + _WorldSpaceCameraPos` —— 有了这两个就能在后处理里重建任意像素的世界坐标。
- **局限**：平面或扁平物体上法线几乎恒定，点积不跨越 0，无法形成轮廓。作者随后改用 [[sobel-edge-detection|Sobel]]。

## 链接到的概念

- [[surface-angle-silhouette]]
- [[sobel-edge-detection]]
- [[cel-shader-outline]]
- [[deferred-rendering]]

## 原文

- 链接：https://www.vertexfragment.com/ramblings/unity-deferred-post-processing/
- 本地：`raw/articles/vertexfragment.com/2019-09-03_surface-angle-silhouette-with-unity-post-processing.md`
