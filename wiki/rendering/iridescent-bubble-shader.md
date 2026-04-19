---
tags: [shader, vfx, fresnel, 折射, iridescent, bubble, unity, urp]
date: 2026-04-19
sources: 1
---

# 彩虹肥皂泡 Shader

**肥皂泡**的视觉特征是两层叠加：一层是**薄膜干涉造成的彩虹**——厚度变化让不同波长相长/相消，呈现彩色条纹；另一层是**折射**——看泡泡时背景会有轻微扭曲。真实物理模型（thin-film interference）计算昂贵，实时渲染的常规做法是用 [[fresnel-edge-highlight|Fresnel 因子]]当「边缘权重」、查一张彩虹 color ramp 当「频谱色」，再叠一点 noise 让色彩随表面漂移。[[daniel-ilett|Daniel Ilett]] 在 *Shader Toolbox for URP* 的 Bubble shader 就是这个配方的完整工程化版本。

## Fresnel 作为彩虹门控

Fresnel 的数学 `pow(1 - dot(N, V), power)` 在掠射角接近 1、正视接近 0。肥皂泡真实的光学规律是**掠射角下反射更强、色散更明显**——和 Fresnel 的输出曲线同向。shader 里的做法是把 Fresnel 值作为**彩虹 color ramp 的 U 坐标**：

- *Color Ramp Texture*：一张 1D 彩虹渐变（红→橙→黄→绿→青→蓝→紫），美术可换成任何风格。
- *Fresnel Power*：越大，彩虹越集中在边缘一圈；越小，铺得越开。
- *Iridescent Strength*：ramp 查出的颜色以多大权重混合进最终颜色。

这是 [[cel-shading-pipeline|Ilett 的 cel-shading Part 3]] 里 Fresnel rim light 同一套骨架，只是替换了「单色 tint」→「ramp 查表」，色彩立刻从单调的边缘光升级为彩虹膜。

## 让色彩流动：noise offset + flow direction

单纯 Fresnel 查 ramp 产生的彩虹是静态的——同一个视角下每个像素的 Fresnel 值几乎一致，色彩就像贴花贴在球面上。加两个扰动让它动起来：

- **Fresnel Noise Strength / Scale**：用一张 noise 把 Fresnel 查 ramp 的 U 坐标做偏移。不同位置查到不同色，整体看上去是彩虹斑块而不是纯净渐变。
- **Iridescent Flow Direction**：世界空间里的 2D 方向向量，乘以时间让 noise 沿该方向滚动。结果是色彩条纹像液体表面一样流过——这正是肥皂泡上色彩漂移的经典观感。

`world space` 而非 `object space` 是重要细节：肥皂泡一般不会跟随自身旋转——色彩是薄膜厚度的体现，空气流动主宰。

## 折射层：`_CameraOpaqueTexture` 或 `_CameraTransparentTexture`

真正的折射需要读背景像素然后按入射角扭曲偏移 UV——这在内建管线用 [[unity-grabpass-blur|GrabPass]] 实现，URP 下用 `_CameraOpaqueTexture`（内置的 opaque-only 帧拷贝）代替。Bubble shader 暴露了一个少见的 toggle——**Camera Texture Mode**：

- `_CameraOpaqueTexture`（默认）：只包含 opaque 物体；透明物体互相看不见折射。
- `_CameraTransparentTexture`（Toolbox 自带）：包含到当前为止已绘制的全部物体（包括其它半透明）。解决了「两个肥皂泡叠在一起时后面的泡泡不通过前面泡泡折射」的 URP 典型缺陷。

*Refractive Index* 直接控制 UV 偏移强度——值越高，背景畸变越重。底层实现一般是 `uvOffset = normal.xy * (1 - 1/n)` 的 Snell-like 近似，不做物理精确的多波长色散。

## Use Emission toggle 的小设计

*Use Emission* 决定 Fresnel 彩虹层是写到 *Base Color* 还是 *Emission* 输出槽：

- 写到 Base Color：彩虹受场景光照影响，暗处的泡泡彩虹也暗。
- 写到 Emission：彩虹独立于光照且可走 bloom —— 这是 [[bloom-threshold-blur-composite|HDR + Bloom]] 配方的入口，暗处的肥皂泡彩虹依然会「发光」。

两种都合理，取决于是追写实还是风格化（动画场景里常选 Emission 配 Bloom）。

## 相关

- [[fresnel-edge-highlight]] —— Fresnel 是肥皂泡效果的核心门控函数
- [[refractive-glass-shader]] —— 同一套 camera texture 折射机制，不叠彩虹的玻璃版本
- [[unity-grabpass-blur]] —— 内建管线的 GrabPass 与 URP `_CameraOpaqueTexture` 的等价关系
- [[color-lut]] —— color ramp 查表的通用方法
- [[bloom-threshold-blur-composite]] —— HDR emission + bloom 让彩虹「真发光」
- [[daniel-ilett]]

## Sources

- [[sources/danielilett-toolbox-urp-bubble]]
