---
tags: [source, shader, toon, cel-shading, urp, unity]
date: 2026-04-19
sources: 1
---

# Toon Shaders Pro for URP — Toon（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] 的 *Toon Shaders Pro for URP* 资产包核心 shader **Toon** 的参数手册页，2026 年 1 月发布。文档本身偏 reference 而非教程，列举了 toon 光照的可调旋钮——把 **diffuse / specular / rim / shadow** 四部分各自独立做 smoothstep 阈值化。

## 摘要

Toon shader 在 URP Lit 的基础上把光照的每一层都加了一个 **cutoff 阈值对**（min/max），用 `smoothstep` 把连续的 `N·L` 之类的值切成硬色阶。面板按 Surface Options / Diffuse / Metallic & Specular / Rim / Normal Mapping 五组暴露。关键设计点：每个阈值背后都是 `smoothstep(min, max, value)`——min 和 max 相同则得到硬 step；支持 *Use Second Threshold* 做三段色阶（shadow / mid / light）；specular 有 *Specular Boost* 补偿阈值剔除后的亮度损失；rim lighting 即 Fresnel，用 `1 - V·N`；可选 Metallic 或 Specular 工作流。整个光照是加性叠加，多光源会产生过曝。

## 关键要点

- **Workflow Mode**：Metallic / Specular 两套工作流并行，影响面板和内部 lighting 计算。
- **Shadow Thresholds**：realtime 阴影也被 smoothstep 切硬阶，独立于 diffuse。
- **Diffuse 二阈值**：`Use Second Threshold` 开启时有三段（shadow / mid / light）和两个阈值对。
- **Specular Offset Noise Map**：给 specular 形状加噪声，做手绘 splotch 效果。
- **Specular Boost**：阈值剔除 specular 大部分时，放大峰值补偿亮度丢失。
- **Rim = Fresnel**：`1 - V·N`，*Rim Extension* 让 rim 沿表面蔓延。
- **Normal Map + Strength**：受光信号层的细节增强，注意使用 toon lighting 时凹凸细节会被阶梯化放大。
- **Global Illumination Strength**：金属材质的 IBL 反射不经 toon ramp，是唯一需要手动压低的"非 toon"来源。
- **加性光照**：多灯会叠出过曝；*Outline* post-process 是 asset 内另一组件。

## 链接到的概念

- [[cel-shading-pipeline]]
- [[cel-shader-outline]]
- [[diffuse-lighting-lambertian]]
- [[fresnel-edge-highlight]]
- [[tangent-space-normal-mapping]]

## 原文

- 链接：<https://danielilett.com/toon-shaders-pro/toon/>
- 本地：`raw/articles/danielilett.com/2026-01-01_toon-shaders-pro-for-urp-toon.md`
