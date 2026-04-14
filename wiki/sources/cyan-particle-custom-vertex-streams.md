---
tags: [source, unity, 粒子系统, shader, shadergraph]
date: 2026-04-14
sources: 1
---

# Passing Particle System Data into Shadergraph（Cyan）

[[cyanilux|Cyan]] 2020 年 7 月发表的教程，讲解如何通过 Unity 粒子系统（Shuriken）的 **Custom Vertex Streams** 和 **Custom Data** 模块，把 per-particle 的数据传进 Shader Graph 做更细的 VFX 控制。

## 摘要

文章先提醒粒子系统的 **Vertex Color** 通道默认就会把 Start Color + Color over Lifetime + Color by Speed 的合成结果送进 shader——Shader Graph 里对应 `Vertex Color` 节点。但只有一个颜色远远不够做精致的 VFX，于是粒子系统提供 **Custom Vertex Streams** 机制：在 Renderer 模块下添加任意数量的 per-particle 数据源（Lifetime → AgePercent、Random → StableRandom.x、Position、Velocity 等），Unity 会把它们按顺序塞进 TEXCOORD 通道的闲置分量——TEXCOORD0 的 xy 已被纹理 UV 占用，剩下的 zw 就给到这些额外数据，再不够就溢出到 TEXCOORD1。列表顺序直接决定 shader 读哪个分量，顺序错了就得在 shader 里跨通道拼数据。

**Custom Data** 模块是另一条路径——它提供两个槽（Custom1/Custom2），可以绑定 Color 或 Vector。Color 支持 HDR（超出 1 的亮度），对搭配 Bloom 后处理很有用；Vector 可以每个分量独立设为 Constant/Curve/Random Between Constants/Random Between Curves——Curve 尤其强大，允许任意形状的生命期曲线，比 AgePercent + Lerp 的线性组合表达力更强。

文章举的例子是烟雾粒子：StableRandom.x 喂给 Flipbook 从 3×3 云朵 sheet 里抽一格、同时 Lerp 到 `[0.9, 1.1]` 做颜色抖动；AgePercent 和纹理 Step 对比做 [[texture-dissolve|dissolve]] 效果。

顺带提到 **VFX Graph**（GPU 粒子）作为替代路径：适合高粒子量，但在 URP 上早期是 Experimental，集成 Shader Graph 需要额外开启 Experimental Operators/Blocks。

## 关键要点

- Custom Vertex Streams 把 per-particle 数据塞进 TEXCOORD 的闲置分量，Shader Graph 里通过 `UV` 节点选通道 + `Split` 拿出。
- 常用源：**AgePercent**（归一化生命 `[0,1]`）、**StableRandom.x**（每粒子一个固定随机数）。
- 列表顺序硬编码分量位置——调整顺序能让跨通道溢出更整齐。
- Vertex Streams 的列表必须和 shader 的 attribute 需求完全匹配，否则 Unity 报 "Vertex Streams do not match the shader inputs" 警告。
- Custom Data 的 Color 支持 HDR（Intensity），这是普通 Start Color 做不到的；Vector 的 Curve 表达力远胜 Vertex Color 的线性演化。
- VFX Graph 是另一条 GPU 粒子路径，适合高粒子量，但和 Shader Graph 的集成早期很繁琐。

## 链接到的概念

- [[particle-custom-vertex-streams]]
- [[uv-manipulation-nodes]]
- [[texture-dissolve]]

## 原文

- 链接：https://cyangamedev.wordpress.com/2020/07/19/custom-vertex-streams/
- 本地：`raw/articles/cyangamedev.wordpress.com/2020-07-19_passing-particle-system-data-into-shadergraph-custom-vertex.md`
