---
tags: [source, rendering, shader, 次表面散射, 半透明, unity]
date: 2026-04-14
sources: 1
---

# Fast Subsurface Scattering in Unity – Part 1（Alan Zucconi）

[[alan-zucconi|Alan Zucconi]] 2017 年 8 月的文章，把 Colin Barré-Brisebois & Marc Bouchard 在 GDC 2011 提出、被整合进 Frostbite 2（Battlefield 3）的廉价 SSS 近似移植到 Unity Surface Shader。

## 摘要

严格的次表面散射要模拟光在材质内部多次反弹 + 从不同点发出——这和 GPU 像素着色器的"只用局部信息"假设冲突。作者介绍的 Barré-Brisebois 方法完全放弃能量传输，改成一个纯解析的"背光伪 SSS"：对每盏光源同时算正面 PBR + 背面"假穿透"两份贡献，背光方向不是单纯的 $-L$，而是受法线扰动的 $-\langle L + N\delta \rangle$（其中 $\delta$ 是 subsurface distortion）。结果再用 $(\cdot)^p \cdot s$ 塑型。$\delta$ 在 0（纯穿透）和 1（反向 Blinn-Phong 半程向量）之间滑动，给艺术家一个"从透光到反射"的单一手柄。整套方法只用局部信息，代价约等于一次 Blinn-Phong 高光——没有邻居采样、没有纹理查表，但对薄植被、蜡烛、玉石这类"轮廓透光"场景足够好。Part 2 会讲 Unity 实现。

## 关键要点

- Barré-Brisebois & Bouchard GDC 2011 / Frostbite 2 的廉价假 SSS
- front lighting 用标准 PBR、back lighting 用反向扰动光方向 $-\langle L+N\delta \rangle$
- $\delta$ 参数：0 = 纯穿透，1 = 反向 Blinn-Phong 半程向量 $H$
- back lighting **不乘 $N\cdot L$**——光是从内部出来的
- 塑型：$I_{back} = \mathrm{saturate}(V \cdot -\langle L+N\delta\rangle)^p \cdot s$
- 不捕捉距离衰减 / 颜色扩散 / 邻居采样——适合中远景而非人脸特写
- 更精细方案参考 GPU Gems 的 *Real-Time Approximations to Subsurface Scattering*

## 链接到的概念

- [[fast-translucency-wraplight]]
- [[physically-based-shading]]
- [[microfacet-brdf]]
- [[shader-vector-math-primer]]

## 原文

- 链接：<https://www.alanzucconi.com/2017/08/30/fast-subsurface-scattering-1/>
- 本地：`raw/articles/alanzucconi.com/2017-08-30_fast-subsurface-scattering-in-unity-part-1-alan-zucconi.md`
