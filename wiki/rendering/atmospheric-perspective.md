---
tags: [rendering, atmosphere, scattering, color, fog]
date: 2026-04-19
sources: 1
---

# 空气透视（Atmospheric Perspective）

远处物体（尤其是层叠的山）颜色发蓝并最终趋白的现象，在美术语境中叫 *aerial perspective* 或 *atmospheric perspective*。[[rune-skovbo-johansen]] 在 2025 年日本旅行后写了一篇观察笔记，澄清了游戏里常用的 *fog trick*（单色雾）所无法表达的关键事实。

## 直观事实（作者的日本观察）

- 远山并非无限趋近"某一单色"（例如天空色）。它们先趋近一个相当饱和的蓝，再**继续远离**时**变得更淡**，最终接近近地平线的那种苍白。
- 同一座山的山面：**迎光时偏绿**（日光下的树压过大气蓝色），**背光时偏蓝**（只剩大气散射贡献）。
- 山峰的大气色不会**淡于紧贴其后的天空**——因为看山时穿过的空气总比看其后天空时的空气**少**。

## 物理解释（作者的最佳推测）

一道空气叠加得越厚，"从透明 → 蓝 → 近白"的曲线就走得越远。Rayleigh 散射让薄空气显蓝，而**更厚空气的散射累积**让颜色在色空间里弯到淡色区域；Mie 散射则主要贡献太阳附近的光晕。这同样解释了天空在天顶深蓝、靠近地平线发白——那条路径上空气更厚。

## 工程意义：为什么 *fog trick* 不够

用单一 fog color 做雾（OpenGL 原始文档就指出这可以模拟大气）的问题：

- 雾色设得太接近天顶深蓝 → 近地平线处山变得比天空还深，不自然。
- 雾色设得接近近地平线苍白 → 有些山峰会比紧贴的天空**还淡**，这在真实里永不发生，看上去就是假的。
- 任何**朝单一颜色淡出**的方案在**远距离**下都无法复现"深蓝 → 苍白"这段弯折。

## 可行的工程替代

- **分通道不同 exp**：红/绿/蓝三通道用不同指数，让雾在距离上从蓝漂白。iq 的 [*fog* 博文](https://iquilezles.org/articles/fog/)提供代码。
- **Unreal Sky Atmosphere Component**：基于 [Bruneton-Neyret, 2008]《Precomputed Atmospheric Scattering》的工业实现。EGSR 2020 有论文与代码。
- **Unity HDRP Physically Based Sky**：同一套思路，但论坛反馈指出实现问题较多。
- **Shadertoy 级实现**：像 [这个](https://www.shadertoy.com/view/wlBXWK) 的 Rayleigh + Mie 散射，可作实验原型。

## 是否必须上大气散射？

作者自我澄清：上述弯折只在**极远距离**才明显。很多游戏用简单 fog trick 就已经足够好看——关键在于画面里是否真的需要渲染"一层一层叠到视线极限"的山脉。他自己的 *The Big Forest* 里至今仍在用 fog trick，只是承认它不够理想。

## 相关

- [[spectral-rendering]]
- [[volumetric-fog-froxels]]
- [[volumetric-fog-raymarch-shadows]]
- [[hero-wavelength-spectral-sampling]]
- [[color-space]]

## Sources

- [[sources/runevision-hair-and-atmosphere]]
