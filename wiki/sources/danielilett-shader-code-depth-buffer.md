---
tags: [source, shader, urp, hlsl, depth-buffer, 教程]
date: 2026-04-19
sources: 1
---

# The Depth Buffer | Unity Shader Code Basics 04（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] *Shader Code Basics* 系列第 4 篇——专讲 **depth buffer / z-buffer** 在 URP 手写 shader 下的用法。三个主题：ZWrite/ZTest 命令、读 `_CameraDepthTexture` 做 silhouette、写 `DepthOnly` / `DepthNormals` 两个 prepass + URP *Render Objects* Renderer Feature 做 X-ray 效果。

## 摘要

Depth buffer 是和 color buffer 同尺寸的单通道图，每次成功画 opaque 对象时把 clip-space z 写进去，下次画新对象时**per-pixel** 比较 z——小于就覆盖、大于就丢弃。这一步叫 **depth testing**。opaque 用 `ZWrite On` + `ZTest LEqual`（默认），transparent 用 `ZWrite Off`——不破坏深度让后续透明物可自由互相 blend。ShaderLab 的 `ZTest` 8 档：Never/Less/Equal/LEqual/Greater/NotEqual/GEqual/Always。

要在 fragment shader 里读深度，Unity 暴露 `_CameraDepthTexture`——**不是真 depth buffer 本身**而是它的拷贝。`#include ".../DeclareDepthTexture.hlsl"` 提供 `SampleSceneDepth(uv)`；屏幕 UV 要用 `ComputeScreenPos(positionCS)` 算再 `xy / w`（透视除法）拿到。值是非线性 `1/z` 分布，近处精度高远处精度低——`Linear01Depth(raw, _ZBufferParams)` 把它映到线性 `[0,1]`。Silhouette 效果就是 `lerp(_Foreground, _Background, linearDepth)`。

Unity 对 opaque 渲染后**不总是**直接复制 depth buffer 到 depth texture——像 SSAO 这类需要 pre-pass depth 的效果强制走 **DepthOnly** 或 **DepthNormals prepass**。自定义 shader 要正确支持 depth texture 必须加这两个 Pass：每个 Pass 需要 `LightMode = DepthOnly` / `DepthNormals` tag，`ZWrite On`，DepthOnly 还要 `ColorMask R`（只写一个通道）。已有的主 Pass 也要显式标 `LightMode = SRPDefaultUnlit`（否则 Unity 自动补上但不明显）。DepthNormals pass 把世界空间法线写进 `_CameraNormalsTexture`——SSAO / edge detection 要用到法线时读它。

最后演示 URP 的 **Render Objects Renderer Feature** 做 X-ray：把需要透视查看的对象挪到自定义 layer，在 Universal Renderer Data 里加一个 Render Objects pass、layer mask 选该 layer、Event = `AfterRenderingOpaques`、override material 为红色 unlit、override Depth Test 为 `Greater`——只在被遮挡时画。整个效果不写一行 C# 脚本。

## 关键要点

- **Depth test per-pixel**：一个"部分挡住另一部分"的物体对也能正确排序；不是 per-object。
- **Depth texture ≠ depth buffer**：是 opaque 绘制后的一张拷贝；transparent 默认不写深度所以不出现在里面。
- **`ComputeScreenPos` + `xy/w`**：URP 里从 clip space 到 screen UV 的标准手法；作者承认"除以 w 的原理"延后解释。
- **`Linear01Depth` + `_ZBufferParams`**：近/远 clip 参数由 Unity 自动填；默认 0.3–1000，80% 的精度给 ≤1.5m。
- **DepthOnly vs DepthNormals 两套 prepass**：前者 `ColorMask R`、只写 z；后者把 world normal 编进 4 通道（`float4(normalWS, 0)`）。要正常配合 URP 特性（SSAO / depth-normals outline），**每个自定义 shader 都得补这两 Pass**。
- **LightMode tag 驱动一切**：没标 tag 就被归 `SRPDefaultUnlit`；URP / Toon / Deferred shader 分别是 `UniversalForward` / `UniversalForwardOnly` / `UniversalGBuffer`。
- **Render Objects Feature**：URP 提供的 14 个 inject event 之一（`BeforeRenderingOpaques` … `AfterRendering`），配合 layer mask + material override + depth test override = 可见 / 隐藏 / X-ray 三态。
- **vertex 位移 / alpha clip 的 shader 必须在 DepthOnly/DepthNormals Pass 里重写 vertex 数学和 clip 逻辑**——否则深度写入的是未位移 mesh，出错。

## 链接到的概念

- [[depth-texture-silhouette]]
- [[z-buffer]]
- [[urp-depth-prepass-passes]]
- [[urp-render-objects-feature]]
- [[early-z-late-z]]

## 原文

- 链接：<https://danielilett.com/2026-01-02-tut10-04-depth/>
- 本地：`raw/articles/danielilett.com/2026-01-02_the-depth-buffer-unity-shader-code-basics-04.md`
