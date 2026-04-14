---
tags: [渲染, shader, 次表面散射, 半透明, 实时, unity]
date: 2026-04-14
sources: 1
---

# 廉价次表面散射近似（Barré-Brisebois 模型）

真正的次表面散射（SSS）要求模拟光在材质内部多次弹射后从另一点再发出——这在 shader 的 per-vertex / per-fragment 局部信息假设下几乎是反直觉的（你拿不到**邻居**的属性）。Colin Barré-Brisebois 和 Marc Bouchard 在 GDC 2011 提出了一个**假 SSS**：不做任何能量传输，用一个简单的"背光 + 方向扭曲"解析式在 Blinn-Phong 风格的代价下得到「光线好像穿过来了」的视觉。这套方法被整合进了 **Frostbite 2**，在《Battlefield 3》上线。[[alan-zucconi|Alan Zucconi]] 的 Fast Subsurface Scattering in Unity 把它完整移植到 Unity Surface Shader。

## 核心思想：双灯照明

对每个顶点 / 像素，把"光照"分成两份：

1. **front lighting** — 常规的 [[physically-based-shading|PBR]] 反射，用光源方向 $L$ 和表面法线 $N$ 计算，照亮朝向光源的一面。
2. **back lighting** — 用同一个光源但方向取反（$-L$）再加上一个扰动项，照亮"背面透光"的那一面。这一项就是伪 SSS。

最终颜色 = front + back。两份都用的是 local information（$N$、$L$、$V$），因此完全兼容 GPU 着色器的"像素独立"假设。

## Subsurface distortion：让背光受法线影响

最粗糙的 back-light 可以直接写成 $V \cdot (-L)$——观察方向与背光方向的对齐度。但这样完全忽视了表面朝向，耳朵、叶片这种薄结构就会失去"形状感"。作者引入一个参数 **subsurface distortion** $\delta \in [0, 1]$，把背光方向从纯 $-L$ 扰动成：

$$I_{back} = V \cdot -\left\langle L + N\delta \right\rangle$$

其中 $\langle X \rangle = X / \|X\|$。

- $\delta = 0$：退化到 $V \cdot -L$——纯"穿透"，形状与法线无关。
- $\delta = 1$：$-\langle L + N \rangle$ 恰好是 **Blinn-Phong 半程向量 $H$ 的反向**——背光方向被法线完全拖动，表现像反向的 Blinn-Phong 高光。

所以 $\delta$ 是在 "纯穿透 / 纯反射高光" 两个极端之间滑动的一个手柄，艺术家可以调出不同材质（皮肤 / 蜡烛 / 叶片）的感觉。

## Power / scale 曲线

$I_{back}$ 一出来是 $[-1, 1]$，需要 clamp 到 $[0, 1]$ 并塑型。作者没有走"用一张曲线纹理"的路子，而是直接用代码：

$$I_{back} = \mathrm{saturate}\left(V \cdot -\left\langle L + N\delta \right\rangle\right)^p \cdot s$$

其中 `p`（power）控制衰减尖锐度、`s`（scale）控制总强度。优点是全部参数都是 uniform float，美术在 inspector 里调，不需要额外纹理通道。

## 为什么不加 $N \cdot L$

front lighting 里的 Lambert 项用的是 $N \cdot L$（和光线夹角 > 90° 就不照亮）。back lighting 里**刻意不用**这一项——因为"光从物体内部出来"这一行为对表面法线的方向基本不敏感，我们只关心"观察者是不是正对着背光"。这是对"真正 SSS"的一个重要简化：把"光从哪里出来"的空间位置扭曲成"光从哪个角度出来"的方向扭曲，用后者在纯局部信息内近似前者。

## 和真正 SSS 的差距

- 没有**距离相关**的衰减——薄耳朵和厚耳朵表现相同。真正 SSS 会根据穿透距离给出指数级衰减。
- 没有**颜色相关**的扩散——真 SSS 里红色波长穿得最远，所以皮肤阴影边缘偏红。本方法需要用 `scale` 上染一个偏红色 tint 手动伪装。
- 没有**邻居采样**——所以皮肤特写下不会有典型的 gathered-blur。更适合中远景、薄植被、翡翠玉石等"轮廓透光"的场景，而不是脸部特写。

GPU Gems 的 *Real-Time Approximations to Subsurface Scattering* 给出了更精细但更贵的方案（diffuse profile + multi-tap 高斯），是这套廉价近似的下一步。

## 相关

- [[physically-based-shading]] — front lighting 仍然走 PBR
- [[microfacet-brdf]] — 和镜面反射叠加时的参考骨架
- [[shader-vector-math-primer]] — $H = \langle L + N \rangle$ 的来历
- [[alan-zucconi]]

## Sources

- [[sources/alanzucconi-fast-sss-1]]
