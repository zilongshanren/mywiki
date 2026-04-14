---
tags: [人物, 作者, 渲染, shader, unity]
date: 2026-04-14
sources: 5
---

# Ronja Böhm（Ferris Systems）

**Ronja Böhm**（之前以 Ronja's Shader Tutorials 为笔名，现与伴侣一同运营 [Ferris Systems](https://ferrissystems.gay/)）是一位以 [ronja-tutorials.com](https://www.ronja-tutorials.com/) 为主要阵地的 shader 教学作者。她的文章几乎是 Unity 社区里中等难度 shader 学习曲线的事实标准之一：从最基础的 `Properties`、`CGPROGRAM` 写起，沿着逐步演化的编号顺序（`001 → 002 → …`）把读者从「HelloWorld 纯色 shader」带到表面 shader、程序化噪声、SDF、Compute、GPU-driven rendering。

## 风格

- **Unity Built-in / CG + HLSL 为主**。教程以 Unity 的 surface shader 和 vertex/fragment 管线为默认载体，很多示例是 ShaderLab `.shader` 文件，也会涉及 `.cginc` 工具库。和 URP / HDRP 的 Shader Graph 教程生态形成互补。
- **渐进式 + 相互引用**。每篇教程都以「上一节做的东西」为起点，强调读者应先掌握前置知识。相关概念 wiki 里若已存在（例如 [[planar-mapping]]、[[sdf-2d-primitives]]），她会直接跳转而不是重复解释。
- **代码全量贴出**。文章末尾几乎都附完整可跑的 shader 源，而不是只给核心片段。
- **偏教学、轻理论**。相比 [[christoph-peters]] 的论文式推导或 [[bartosz-wronski]] 的工业 debrief，Ronja 更接近「一位助教手把手带你写出第一个能跑的效果」。
- **覆盖 VFX 常见需求**。溶解、描边、扭曲、贴花、triplanar、Compute Shader 基础、GPU-driven rendering——都是游戏美术/TA 日常会被问到的主题。

## 和其他作者的谱系

- 与 [[xor-shader-artist|Xor]]（GameMaker + Shadertoy）在定位上很像：都是「短篇 + 代码先行」的 shader 教学，但 Ronja 更系统地绑定 Unity，而 Xor 更偏 Shadertoy / 艺术风格。
- 与 [Catlike Coding](https://catlikecoding.com/) 的 [[jasper-flick|Jasper Flick]] 相比，Ronja 的文章更轻量、更聚焦单个效果，而 Jasper 的系列更像长篇工程笔记。
- 与 [Inigo Quilez](https://iquilezles.org/) 的 SDF 文章互补——iq 偏向数学推导和优化，Ronja 更侧重「从零开始怎么把它塞进 Unity」。

## 对本 wiki 的贡献

| 文章 | 贡献的概念 |
|---|---|
| Planar Mapping | [[planar-mapping]] — 世界坐标生成 UV 的最简方式 |
| Texture Dissolve | [[texture-dissolve]] — 纹理驱动的 clip + 边缘发光 |
| 2D SDF Basics | [[sdf-2d-primitives]] — 2D SDF 基元、transform、可视化 |
| 2D SDF Shadows | [[sdf-ray-marched-shadows]] — 用 SDF 做 2D 软阴影 |
| Graphics.DrawProcedural | [[draw-procedural-gpu]] — GPU 持有 buffer 直接绘制 |

## 相关

- [[planar-mapping]]
- [[texture-dissolve]]
- [[sdf-2d-primitives]]
- [[sdf-ray-marched-shadows]]
- [[draw-procedural-gpu]]
- [[jump-flooding-algorithm]]
- [[fragment-shader]]
- [[linden-reid]] —— 同赛道的另一位 Unity shader 教程作者

## Sources

- [[sources/ronja-planar-mapping]]
- [[sources/ronja-texture-dissolve]]
- [[sources/ronja-2d-sdf-basics]]
- [[sources/ronja-2d-sdf-shadows]]
- [[sources/ronja-draw-procedural]]
