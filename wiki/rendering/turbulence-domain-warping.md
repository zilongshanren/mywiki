---
tags: [rendering, shader, noise, fluid, domain-warping]
date: 2026-04-19
sources: 1
---

# 湍流 Domain Warping（叠加旋转正弦波）

Xor 在 Turbulence 里总结了一个极其简单、却能伪装成「液体、火、烟、雾、魔法」的技巧——**把坐标反复用正弦波扭曲，每次旋转 + 缩放**。它并不是 Navier-Stokes 模拟（那要多 pass、显存和数值代价），而是一种**低成本 domain warping**，思路和 [[layered-grid-noise]]、[[fractal-texturing]] 一脉相承：把多层细节叠起来，让大脑觉得「这玩意儿在流」。

## 核心片段

单次波的写法只是在 `pos` 上加一个沿旋转方向的正弦偏移：

```glsl
float phase = freq * (pos * rot).y + SPEED * iTime + i;
pos += AMP * rot[0] * sin(phase) / freq;
rot *= mat2(0.6, -0.8, 0.8, 0.6); // 每次转一个无理角
freq *= 1.4;                       // 频率递增、振幅随 1/freq 衰减
```

关键点：

- **旋转角别取 45° / 90°**，否则会露出对齐纹路；任意「看起来自然」的角就行。
- **振幅 = AMP / freq**：高频低幅，和 fBm 一样保持能量守恒感。
- **8–10 次迭代**足以出漂亮涡流；乘数越大越碎、越少越平滑。

## 从湍流到火焰

火焰用同样的架构，只再加两个技巧：初始坐标**纵向压缩 + 向上滚动**模拟热气上升，到高处再**横向拉伸**模拟横向扩散。变量相同，整个效果仍在单 pass fragment shader 内完成。

## 在工具链里的位置

- 和 [[classic-shader-noise]]、[[worley-voronoi-noise]] 相比，这种纯 sin 叠加**无需采样纹理、无哈希**，指令极少，天生向量化；代价是出来的结构偏「螺旋涡」而非「云絮」。
- 和真 Navier-Stokes（vorticity confinement 等）比，缺少守恒量和物理交互，但适合背景 / VFX。
- 常被用作 [[shader-art-design-principles]] 里「多尺度纹理」的那一层。

## Sources

- [[sources/xor-mini-turbulence]]
