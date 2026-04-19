---
tags: [渲染, 后处理, 色差, 屏幕效果, vfx, unity]
date: 2026-04-14
sources: 2
---

# 色差后处理（Chromatic Aberration as Post-Process）

**Teleglitch** 在玩家使用传送器时，整个画面会闪一下——红 / 绿 / 蓝三个通道被各自**独立地**偏移，像是一台出故障的 CRT 显示器。这是一类常见的屏幕后处理效果：**把单张已完成的 framebuffer 按通道分别采样并偏移**，合成出「光学失常」或「信号出错」的视觉。

## 两种不同的目的

Simon 的一位读者在评论里做了很有价值的区分：

- **光学意义上的色差（chromatic aberration）**——模拟真实镜头在边缘处因波长折射率不同而产生的颜色分离。典型的色调是**黄 vs 青** 或 **绿 vs 品红**（这正是标准 Bayer demosaic / lens Kent 建模里出现的颜色对）。应用包括 Crytek 水面 shader、Black Mesa 的「受伤」反馈。
- **数字意义上的 RGB 偏移**——三通道彼此独立失相，更像是一盘松了的 VHS 磁带或者一台年久失修的 CRT。Teleglitch 的传送器特效属于这一类，和真实镜头色差无关。

区别不仅在视觉，还在**哪个通道偏多少**：真实色差是确定性的、径向的、两对色相反的；数字「glitch」是可以任意的、可以用噪声驱动、可以每帧变化。

Alisavakis 在 [[glitch-image-effect|glitch 后处理]] 里直接采用「数字意义上的 RGB 偏移」这一派：三通道各自独立偏移、和距中心无关、可随条纹 mask 每帧变化——典型的 VHS / CRT 故障美学而非光学色差。

## Deadlight 的径向梯度

Deadlight 的后处理作者本人也来评论区澄清实现：**强度随像素到屏幕中心的距离增大**——用一张从中心向外径向渐变的 gradient 作为畸变偏移的权重。这是一个细微但关键的细节：

$$\text{offset}(u,v) = \text{baseOffset} \cdot g(\|uv - 0.5\|)$$

屏幕中心几乎不偏移（读者看主要游戏内容的区域保真），边缘逐渐加大到肉眼可见的色散。这正好和真实镜头的行为一致——成像主轴处光线几乎垂直穿过镜片，边缘光线才被折射分光——所以即便作者是在做「故障艺术」风格，用径向梯度也自然落到类似镜头色差的视觉。

## 实现层的简洁性

着色器几乎是最简单的后处理：

```hlsl
float2 dir = uv - 0.5;
float  k   = length(dir);
float  amt = k * k * intensity;          // 径向，非线性
float3 col;
col.r = tex2D(screen, uv + dir * amt * 1.0).r;
col.g = tex2D(screen, uv + dir * amt * 0.5).g;
col.b = tex2D(screen, uv + dir * amt * 0.0).b;
```

三次纹理采样 + 一次 length。要做 Teleglitch 式的无规律闪烁，把偏移方向换成噪声或随时间抖动即可。要做 Deadlight 的光学感，就按径向对称。

## 与其它「屏幕受伤」效果的关系

RGB 偏移常和 **scanline / interlace / vignette / bloom / grain** 一起被塞进一个「故障后处理包」里，彼此正交、可以 toggle 独立的 keyword：参见 [[crt-shader-effects]] 对整组 CRT 特效的拆解。它们都有一个共同的数学形式——**在已合成的 framebuffer 上做非均匀 UV 变形 + 通道级别的采样**，这也是所有 post-process 的共性。

## 相关
- [[crt-shader-effects]] — 同属「屏幕设备模拟」家族
- [[urp-volume-post-processing]]
- [[thin-lens-model]] — 真实光学色差的来源
- [[unity-image-effect-basics]] —— Alisavakis 2017 教程的实现骨架
- [[harry-alisavakis]] —— *My take on shaders* 第四篇用对角线均匀偏移做的 R/G/B 三通道色差版本
- [[scatter-bokeh-dof]] — scatter 路线允许做**物理正确**的色差：把不同波长烘成不同大小的 bokeh 光斑而不是 RGB 偏移
- [[underwater-post-effect]] —— caustics 的 Color Separation 是色差思路的 caustics 变体
- [[vortex-distortion]] —— 与色差叠加常见（漩涡越强、色差越强）

## Sources

- [[sources/simonschreibt-teleglitch-rgb]]
- [[sources/halisavakis-image-effects-chromatic-aberration]]
