---
tags: [source, unity, shader, 光照, cel-shading]
date: 2026-04-14
sources: 1
---

# Cel Shading Part 0 - Lighting Models（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] 2019 年 6 月发表的卡通渲染系列先导篇。与后续几篇动手实现不同，Part 0 纯粹是**理论铺垫**：把整个 Phong 光照家族的四个分量——ambient、diffuse、specular、fresnel/rim——用自然语言和一点点数学各讲一遍，为后面在 shader 里"把平滑光照打成硬阶梯"提供概念基础。

## 摘要

文章先用一段 PBR / ray tracing 的开场提醒读者：光照模型的复杂度是一个谱系，Phong 是"前 PBR 时代"的经典起点。然后对比了 flat shading / Gouraud shading / Phong shading 的代价差别——逐面、逐顶点、逐像素——解释了为什么 Phong 更贵但更平滑。接着分四节依次讲 **ambient**（漫反射的基底亮度，光线多次反弹后的近似）、**diffuse**（`L·N`，和视角无关，决定光斑形状）、**specular**（半向量 + `pow` 集中的高亮斑，和视角相关）、**fresnel/rim**（`1 - V·N`，只看视线掠射角度，用于物体边缘高光）。最后顺带预告这个系列会使用 **Unity Surface Shader**，让 Unity 处理多光源 / 多路径的样板代码，开发者只需要写光照函数和表面属性。

## 关键要点

- Phong shading 和 Gouraud shading 的区别不在光照公式，而在"在哪里计算"——前者逐像素插值法线后算 diffuse，后者逐顶点算完再插值颜色。flat shading 甚至连插值都没有。
- `L_total = L_ambient + L_diffuse + L_specular (+ L_fresnel)` 是一个**加法式**堆栈——cel shading 后面会对每一项都做量化、再加起来。
- Specular 用 **half-vector**（`normalize(L + V)`）和法线做点乘，是 Blinn-Phong 的写法；Ilett 直接管它叫 Phong 但其实用的是 Blinn 版本——原始 Phong 用的是反射向量 `reflect(-L, N)` 和 `V` 的点乘。
- Fresnel 的物理意义在 Part 0 被简化成了"视线掠射角度下观察到的反射增强"，真实物理的 Schlick 近似 `F0 + (1 - F0)(1 - V·N)^5` 没有出现——Ilett 故意不讲 PBR 公式。
- Ambient 在这篇里只是一个常数，**完全没有环境贴图、SH 光照、LPV** 之类的进阶内容——系列目标只是 cel shading，不是真实感。

## 链接到的概念

- [[cel-shading-pipeline]]
- [[diffuse-lighting-lambertian]]
- [[normalised-blinn-phong-shader]]
- [[unity-surface-shaders]]

## 原文

- 链接：https://danielilett.com/2019-06-01-tut2-0-lighting-models/
- 本地：`raw/articles/danielilett.com/2019-06-01_cel-shading-part-0-lighting-models.md`
