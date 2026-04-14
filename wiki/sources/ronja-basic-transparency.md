---
tags: [source, rendering, shader, unity, 透明]
date: 2026-04-14
sources: 1
---

# Basic Transparency（Ronja's Shader Tutorials）

[[ronja-bohm|Ronja Böhm]] 2018 年 4 月发表的 Unity shader 入门系列第 006 篇，讲怎样把一个已有的纹理 shader 改成半透明版本。

## 摘要

文章从三件事讲透了 Unity 里的透明 shader 配置：一是 `Tags { "RenderType"="Transparent" "Queue"="Transparent" }` 把材质丢到透明渲染队列末尾，让它在不透明几何之后绘制，否则会被 Z-test 误杀；二是 `Blend SrcAlpha OneMinusSrcAlpha` 指定经典的 source-over 混合模式——新色乘 α、旧色乘 `1-α`、相加得到结果——并用两个数值例子（α=0.5 均等混合、α=0.9 几乎完全覆盖）帮读者直观理解；三是 `ZWrite Off` 必须关掉深度写入，因为半透明物体不应该遮挡它后面的其他半透明物体，Unity 会替你按深度排序重叠的透明物体。这篇是 Ronja 整个系列里 sprite、描边、溶解、UI 等一切透明效果的前置知识。

## 关键要点

- 透明 shader 的三件套：`Queue=Transparent` + `Blend SrcAlpha OneMinusSrcAlpha` + `ZWrite Off`。
- Blend 指令在 SubShader 或 Pass 块里定义，**必须在 HLSL/CG 块外**。
- Unity 自动为 `Queue=Transparent` 的物体做 back-to-front 排序（painter's algorithm），shader 作者无须处理。
- fragment shader 返回的 `col.a` 作为 source alpha 自然驱动混合——只要不在 shader 里覆盖它，Inspector 上 `_Color` 的 alpha 分量就直接生效。

## 链接到的概念

- [[alpha-blending]]
- [[fragment-shader]]
- [[z-buffer]]

## 原文

- 链接：<https://www.ronja-tutorials.com/post/006-simple-transparency/>
- 本地：`raw/articles/ronja-tutorials.com/2018-04-06_basic-transparency.md`
