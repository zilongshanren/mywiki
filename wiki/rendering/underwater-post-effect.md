---
tags: [渲染, unity, urp, 后处理, underwater, caustics, flow-map]
date: 2026-04-19
sources: 1
---

# 水下后处理效果（Underwater Post Effect）

水下视觉的两个视觉签名是**UV 扭曲**（摇晃感）和**caustics**（光斑纹）——前者骗视觉系统「介质在动」、后者骗视觉系统「光被水面折射过」。Daniel Ilett 的 *Snapshot Shaders 2* Underwater 后处理把这两者都做成了屏幕空间的 [[urp-volume-post-processing|URP Volume]] override——代价低、完全不需要改场景几何。

## UV 扭曲：Flow Map 驱动的屏幕位移

传统"摇晃"用 `sin(uv.y * f + t)` 硬编码——效果僵硬，且无法表现「某处扭得强、某处扭得弱」。**Flow map** 是更一般的做法：一张纹理，R/G 通道分别编码 UV 位移的 X/Y 分量（通常 0.5 = 零位移，<0.5 = 负向，>0.5 = 正向）。渲染时：

```hlsl
float2 flow = SAMPLE_TEXTURE2D(_FlowMap, uv * tiling + _Time.y * speed).rg * 2 - 1;
float2 distortedUV = uv + flow * strength;
color = SAMPLE_TEXTURE2D(_Main, distortedUV);
```

这让 UV 扭曲完全由**贴图设计**决定——美术画什么波纹就出什么波纹。滚动 flow map 本身（`* tiling + _Time.y * speed`）产生时间变化。

Flow map 的概念并不专属水下——[[animated-parallax-cloth-fold|动画视差布褶皱]]、火焰、风场也都用 flow map 驱动位移，思路一致。

## Caustics：三种投影模式的取舍

Caustics 是水面弯曲把阳光聚焦/发散产生的亮斑，在真实世界由折射 + 焦散计算而来（photon mapping、adaptive sampling 等）；屏幕空间版本用一张纹理**贴**上去就行，但**怎么把 2D 纹理贴到 3D 场景**是关键问题。Snapshot 2 给出两种模式：

**Triplanar**（三平面投影）：沿世界坐标的 XY / YZ / XZ 三平面各做一次贴图采样，然后按**表面法线**加权混合。法线朝 +Y 则 XZ 平面权重大、朝 +X 则 YZ 平面权重大——每个面总能找到一个"正对它"的投影平面。代价是 3× 的 caustics 纹理采样，换回来的是"从任意角度看都不会被拉伸"的贴合感。参见 [[triplanar-projection|triplanar mapping]] 条目。

**Light Aligned**：把 caustics 的采样 UV 对齐到主光方向——相当于"光从哪来就从哪投"。只需 1× 采样，适合室外大太阳；但室内或多光源场景里光斑方向单一会露馅。

两种模式之外还有三个关键细节：

1. **两层 caustics 异频叠加**：推荐设置两套 Tiling / Scroll Velocity，**tiling 接近但不同、velocity 方向相反**。单张贴图循环会暴露周期性，两层异频叠加把可见周期拉得很长，视觉上接近自然光斑。
2. **Color Separation**：按 RGB 通道各自偏移采样位置——相当于 [[chromatic-aberration-post|色差]] 作用于 caustics，让亮斑边缘呈彩虹色。代价是**采样数再 ×3**——triplanar + color separation 总采样数 = 9，开启需谨慎。
3. **距离衰减**：*Start Fade* + *Fade Falloff*。远处 caustics 在屏幕上小于一个像素时必然走 mip 层、必然产生 aliasing——远处直接淡出到 0 更干净，也省采样。

## 是屏幕空间，不是物理

这个 effect 是**纯屏幕空间贴图叠加**，不是物理模拟：

- 没考虑水的吸收（真实水下远处应当偏蓝偏暗）——要配合 fog 或 color grading 补
- 没考虑物体被水折射变形（只有屏幕 UV 扭曲，没有几何折射）——真正物理水下需要 [[refractive-glass-shader|折射 shader]] 级别的 IOR 处理
- caustics 不跟物体几何互动（物体不遮挡 caustics、不产生真实的焦散投影）——这些是屏幕空间伪造的必然限制

但作为视觉签名够了——玩家的大脑会自动补全"哦这是水下"。这是 [[urp-volume-post-processing|Volume 后处理]] 与 [[shaping-functions|感知导向合成]] 的典型案例。

## 进入水下的过渡

把这个 effect 挂在 Local Volume + 水体 Collider 上，配合 Volume 的 **Blend Distance** 参数，玩家穿越水面时就能自动平滑过渡——**不需要一行额外代码**。这是 Volume 系统架构选择"基于体积而非基于事件"带来的直接好处。

## 相关
- [[urp-volume-post-processing]] —— 所依附的 Volume 系统
- [[chromatic-aberration-post]] —— Color Separation 的同源思路
- [[triplanar-projection]] —— Triplanar caustics 的采样方式
- [[classic-shader-noise]]
- [[animated-parallax-cloth-fold]] —— Flow map 驱动位移的另一应用
- [[refractive-glass-shader]] —— 真正的折射，与 UV 扭曲的差异
- [[fog-shader]] —— 水的吸收需要搭配的效果
- [[vortex-distortion]] —— 另一种 UV 扭曲后处理（极坐标驱动），可与水下扭曲叠加

## Sources
- [[sources/danielilett-snapshot2-underwater]]
- [[sources/danielilett-snapshot-pro-underwater]] —— Snapshot Shaders Pro 的简化版 Underwater（bump + fog，无 caustics / flow map / triplanar）
