---
tags: [shader, shadergraph, 透明, 折射, urp, 游戏复刻]
date: 2026-04-14
sources: 1
---

# MGS 潜行迷彩 Shader：Scene Color + 噪声扭曲

[[daniel-ilett|Daniel Ilett]] 2024 年的 Shader Graph 教程里复刻《Metal Gear Solid 2》的 **Stealth Camo**——Snake 披上后整个人变成半透明果冻，背景物体的直线穿过他身体时会变成扭曲的波浪。这个 shader 的价值不在于"做了点什么"，而在于把**读取屏幕已渲染像素 + 按噪声扭曲 UV** 这一套屏幕空间 trick 的最短路径教出来——它是 glass / heat haze / force field 一类"透过物体看背景"效果的最基本骨架。

## 数据源：Opaque Texture

想让透明物体读取它身后已经画好的不透明像素，必须走 [[scene-color-depth-nodes|Scene Color 节点]]，而 Scene Color 在 URP 下采样的是 **`_CameraOpaqueTexture`**——这张纹理**默认不生成**，要在 **URP Asset → Opaque Texture** 打钩才会有。一个 URP 工程默认有三个 quality 档的 UniversalRenderPipelineAsset（Low/Medium/High），三份都要勾，否则切质量档会出意外。

URP 在一次 frame 里的时序是：先画所有不透明物体 → **在画透明物体之前 copy color buffer 到 `_CameraOpaqueTexture`** → 画透明物体。所以 shader 的 Graph Settings 必须把 **Surface Type 设为 Transparent**——如果它是 Opaque，它自己会先被写进 `_CameraOpaqueTexture`，然后读到自己，产生反馈或全黑。

## Graph 本体

只有三个 property：

- `Base Color`（Color，含 Alpha）—— RGB 决定果冻的底色，**Alpha 控制果冻色和背景像素的混合比例**（不是 Unity 自己管理的透明度）。
- `Noise Size`（Float）—— 噪声云的尺度。
- `Noise Strength`（Float）—— 扭曲强度。

输出栈里有个反直觉的设定：**Alpha 直接接常数 1**。Ilett 不让 Unity 自己做透明度，因为整个像素颜色都是 shader 手动控制的混合；如果 Alpha < 1，Unity 的 alpha blend 会再混一次，结果是双重混合。`Base Color` 的输出是 `Lerp(SceneColor, BaseColor, BaseColor.a)`——alpha 越高，越多地显示 Base Color；alpha 越低，越透明。

扭曲的核心是**偏移 Scene Color 节点的 UV**。Scene Color 默认用 **Screen Position** 作 UV（归一化屏幕坐标 = 当前像素自己的屏幕位置）。

1. `Simple Noise` 吃 `Noise Size`，输出 [0, 1] 范围的灰度云。
2. `Remap` 节点把 [0, 1] 重映射到 **[-1, 1]**——关键一步：没有这步的话噪声只会把像素往屏幕左下方推（因为偏移全是正的），扭曲是有方向性的；remap 之后噪声可以向四个方向均匀推。
3. 乘 `Noise Strength` 得到偏移量。
4. 把偏移量加到 `Screen Position`，当作新 UV 喂给 Scene Color 节点。

## 为什么这是一个"教科书骨架"

- **"透过它看背景"的所有效果都同构**：玻璃、热浪、scope 瞄具、水面波纹、力场冲击波——都是"Scene Color + 某种 UV 扰动"。区别仅在扰动来源：Stealth Camo 是 `Simple Noise`，玻璃可能是法线贴图重定向，热浪是 `Voronoi + Time`，冲击波是径向 radial gradient 加 `sin(time)`。
- **Noise 的 [0, 1] → [-1, 1] 重映射**是任何用噪声做位移的 shader 都必须做的事，否则位移场有系统性 bias。[[pokemon-terastallize-shader|Terastallize]]里的反射也用了同类 `Remap`。
- **为什么不用 Alpha Scissor**：因为本 shader 不需要剪掉任何像素，它要的只是"让我决定每个像素显示什么"，Alpha Scissor 会丢像素。

## 性能和限制

- URP 每帧复制 `_CameraOpaqueTexture` 是全屏 blit，移动端和 Nintendo Switch 是真实代价；项目里尽量只在需要的 feature 下开。
- 这个 shader 在透明对象穿插透明对象时表现会退化——Scene Color 只包含 opaque 阶段的内容，所以披了 Stealth Camo 的 Snake 后面如果站着一个半透明粒子，看不到。真正的 MGS 实现应该会处理这件事，教程里简化掉了。
- 想同时还有光照交互，可以把图建在 **Lit** 模板上而不是 Unlit；Ilett 为了教程简洁选了 Unlit。

## 相关

- [[daniel-ilett]]
- [[scene-color-depth-nodes]] — Scene Color 节点的前置和陷阱
- [[shader-graph-lighting-primer]]
- [[classic-shader-noise]]
- [[bluk-2d-fog-sprite-shader]] — 另一个基于 `_CameraOpaqueTexture` 的 shader
- [[pokemon-terastallize-shader]] — 同系列教程的"反向案例"（向 Emission 做加法而不是向 UV 做位移）

## Sources

- [[sources/danielilett-mgs-stealth-camo]]
