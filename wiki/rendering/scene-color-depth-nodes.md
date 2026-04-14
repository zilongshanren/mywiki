---
tags: [shader, shadergraph, 透明物体, 深度, 渲染, unity]
date: 2026-04-14
sources: 1
---

# Scene Color 与 Scene Depth 节点

Shader Graph 里有两个看起来普通但很特殊的节点：**Scene Color** 和 **Scene Depth**。它们让透明物体 shader 能够**读取相机已经渲染好的场景结果**——颜色 buffer 和深度 buffer——从而实现一大批依赖"屏幕背后已有像素"的效果：玻璃折射、水面、力场、雾墙、UI 扭曲等。这两个节点的行为强绑定 **[[scriptable-render-pipeline|渲染管线]]**，在 Built-in / URP / HDRP 上各不相同，是 shader 新手最常踩的坑之一。

## Scene Color = 读场景颜色

Scene Color 节点的输出**不是**当前 fragment 的最终颜色，而是采样当前渲染管线维护的"场景颜色纹理"。

- 在 **URP**（以及它的前身 LWRP）里，它采样的是 **`_CameraOpaqueTexture`**——这意味着它只包含**不透明物体**的结果。必须在 URP Asset 上勾选 **Opaque Texture** 选项（或 Camera 上的同名开关），这张纹理才会真的被生成，否则 Scene Color 读到全黑。
- 透明物体想读取它的 shader 必须走 **Transparent** 渲染模式——否则它会写入 `_CameraOpaqueTexture` 自身（或者根本不生成），结果采到自己。如果你非要用 Opaque，就得把 Material 的 Render Queue 手动改到 **2501** 或更高，使它被排在 opaque 纹理捕获之后。
- **HDRP** 则采样一个多 mip 的 **`_ColorPyramidTexture`**（原文说 "believe" `_ColorPyramidTexture`，因为 Cyan 本人不常用 HDRP），LOD 0 是最高分辨率，`HD Scene Color` 节点可以访问其它 LOD。输出还可能需要手动乘 `Exposure` 节点才正确。
- **Built-in 渲染管线**：Scene Color 节点在 Built-in 上不工作——SRP 的 Shader Graph 实现要求每条管线自己定义该节点的行为，没定义就返回 0。

Scene Color 的 UV 输入默认是 `Screen Position`（归一化屏幕坐标），采到的恰好是"当前片段身后本该显示的像素"。偏移这个 UV 就能做**折射**：玻璃、热浪、透视扭曲都是同一个技术。HDRP Master 节点上有内置 Distortion 输出，可以绕开这个节点，但原文作者没成功配通。

## Scene Depth = 读深度 buffer

Scene Depth 采样 **`_CameraDepthTexture`**——所有主流管线都叫这个名字，但启用条件不同：

- **URP**：必须在 Asset 上开 **Depth Texture**（或相机上"On"），否则节点返回 `1`（白）。URP v7.3 时代有个古怪的 bug——**Camera 上必须开 Post Processing** 才会真的触发 depth pass；也有人发现开 HDR / MSAA / Opaque Texture 也能"意外"地触发。这是早期 URP 的一个已知缺陷。
- **HDRP**：深度纹理有多个 mip level，shader 代码需要用 `SampleCameraDepth` 函数族（定义在 `ShaderVariables.hlsl`），节点端已经处理好。
- **透明物体**同样的陷阱：如果 shader 写入 depth（ZWrite On），就会读到自己。必须 **ZWrite Off** 或走 Transparent 模式。

## 三种采样模式：Raw / Linear01 / Eye

Scene Depth 节点在 Inspector 上有 3 档模式：

- **Raw**：直接返回深度纹理里存的原始值——在透视投影下这个值**不是线性**的，因为 Z-buffer 的精度分布偏向近裁剪面（见 [[reversed-z|reversed Z]] 的讨论）。再加上大部分现代硬件启用 reversed Z，raw `0` 实际上是**远裁剪面**而不是近。
- **Linear01**：把 raw 深度转成 `[0, 1]` 线性范围（0 = 相机位置、1 = 远裁剪面）。内部使用 `Linear01Depth` 函数，**只能**用于透视投影。
- **Eye**：线性化为**世界单位的 eye-space 深度**（0 在相机处，10 表示前方 10 个 Unity 单位）。内部使用 `LinearEyeDepth`。同样**只能**用于透视投影。

**正交投影下深度 buffer 本就是线性的**，所以要用 Raw 模式——这是很多人用正交相机做 2.5D 时栽的坑。

## `_ZBufferParams` 与线性化公式

线性化本身只是一个双曲函数倒数：

```hlsl
float Linear01Depth(float depth, float4 zBufferParam) {
    return 1.0 / (zBufferParam.x * depth + zBufferParam.y);
}
float LinearEyeDepth(float depth, float4 zBufferParam) {
    return 1.0 / (zBufferParam.z * depth + zBufferParam.w);
}
```

`_ZBufferParams` 的四个分量取决于近远裁剪面**以及 Z 是否反转**：标准 `{1 − f/n, f/n, (1 − f/n)/f, (f/n)/f}`，reversed 时变成 `{−1 + f/n, 1, (−1 + f/n)/f, 1/f}`。

## 拿到当前片段自己的深度

Scene Depth 采场景里**别的**物体的深度。要同时拿到**当前 fragment 自己**的深度，用 `Screen Position` 节点设为 **Raw** 模式，然后 Split 取 `W/A` 分量——那就是 clip-space z / w 的值，可以喂给 `LinearEyeDepth`。两者一减就得到"当前透明片段离它身后场景的距离"，这是**深度相交**技术的基石，用于：

- **水面岸边的泡沫**：距离小的位置加一条白边。
- **雾墙**：距离做密度函数，用 `1 - exp(-distance * density)` 得到经典体积雾。
- **力场 / 护盾**：距离越小颜色越亮。
- **云、粒子穿透软边**：避免粒子 quad 和不透明几何硬交切。

## 和 [[z-buffer]]、[[reversed-z]]、[[z-fighting]] 的关系

Scene Depth 的"不线性"是 perspective projection 本身的性质——[[reversed-z]] 是为了把精度从远端拉到近端而对 buffer 做反向存储。Scene Depth 的 Linear01 / Eye 模式本质上就是把 Z-buffer 里"为了精度做的扭曲"解开，还原线性距离。所以这个节点是 shader 里观察 [[z-buffer]] 行为最直观的窗口——也是理解 reversed-Z 为什么重要的最好案例。

## 相关

- [[z-buffer]]
- [[reversed-z]]
- [[urp-volume-post-processing]]
- [[blit-render-feature]]
- [[fragment-shader]]
- [[alpha-blending]]
- [[orthographic-depth]] —— 正交相机下 Scene Depth 必须用 Raw 模式，平台差异和深度差技巧的正交版

## Sources

- [[sources/cyan-scene-color-depth]]
- [[sources/danielilett-mgs-stealth-camo]] —— MGS Stealth Camo 是 `Scene Color` 最短的实战样板：URP Opaque Texture + Transparent shader + Simple Noise remap → Screen Position 偏移
