---
tags: [source, unity, urp, shader, glitter, voronoi, fresnel]
date: 2026-04-19
sources: 1
---

# Shader Toolbox for URP - Glitter（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] 为 *Shader Toolbox for URP* 撰写的 **Glitter** 参数手册——用 Voronoi 单元作为 glitter 粒子分布 + Fresnel 门控的闪片效果。

## 摘要

Glitter 在 [[sources/danielilett-toolbox-urp-base-lit|Base Lit]] 表面基础上叠一层 Voronoi 细胞——每个单元是一粒 glitter 颗粒。*Noise Scale* 控 Voronoi 平铺密度；*Spot Thresholds* 是一对 smoothstep 阈值（要求第二个值 ≥ 第一个）作用在每个 cell 的距离场上——阈值远离 0 时形成规则的圆形颗粒、接近 0 时颗粒变成锯齿碎片；*Spot Offset* 是整体旋转偏移，0 时颗粒排成规则网格；*Noise Rotation Speed* 让每个 cell 的"随机向量方向"随时间转动——粒子反射光的朝向在变，观察者相对表面移动时部分粒子"亮"、部分"灭"，产生 sparkle 的闪烁观感；*Glitter Offset* 是全局门控——决定有多少比例的 Voronoi cell 真的变成发光 glitter（其余透明）；*Sparkliness* 是每粒子反射的"视角容忍度"——值越高要求观察方向越精确对齐粒子方向，可见的闪亮粒子就越少但越稀疏的每粒都亮——视觉上"更 sparkly"；*Glitter Color* / *Glitter Color 2* 是随机范围两端色，每个 cell 在这两色之间随机染色；*Fresnel Power* + *Fresnel Color* 给整体外观叠一层边缘 rim 光。

## 关键要点

- Voronoi 细胞是天然适合 glitter 的空间结构：每个 cell 独立位置 + 独立随机向量 = 一颗粒子的朝向
- **Spot Thresholds 控颗粒形状**：smoothstep 双阈值挤压 distance field——数学上完全等价于 [[texture-dissolve|dissolve 边缘]] 的做法，只是语义换成"颗粒体"
- **Sparkliness 的反直觉**：值高看起来更稀疏但每粒更亮——因为对观察角度的容忍度下降了，只有精确对齐的粒子才能亮
- **Noise Rotation Speed** 是闪烁感的关键——每个 cell 的反射向量随时间旋转等价于观察者的小范围运动，glitter 逐个"触发-熄灭"
- 两色随机染色是比单色更真实的闪片效果——真实 glitter 是多色金属片混合
- Fresnel 给整体外观加 rim 光，glitter 颗粒在 Fresnel 高的边缘也会同时更明亮（视角掠射时粒子可见性增强）

## 链接到的概念

- [[worley-voronoi-noise]]
- [[fresnel-edge-highlight]]
- [[holofoil-rainbow-shader]]
- [[shaping-functions]]
- [[classic-shader-noise]]

## 原文

- 链接：https://danielilett.com/shader-toolbox/glitter/
- 本地：`raw/articles/danielilett.com/2026-01-01_shader-toolbox-for-urp-glitter.md`
