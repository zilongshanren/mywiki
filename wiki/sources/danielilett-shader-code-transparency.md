---
tags: [source, shader, urp, hlsl, 透明, alpha-blend, alpha-clip, 教程]
date: 2026-04-19
sources: 1
---

# Transparency | Unity Shader Code Basics 03（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] *Shader Code Basics* 系列第 3 篇（URP + HLSL 手写版）。在 Part 2 的 `BasicTexturing` 基础上加透明度：**alpha-blended transparency**（传统半透明混合）和 **alpha clipping / alpha test**（阈值剔除）。本篇也第一次出现 shader 里**从 ShaderLab 传命令到 HLSL 之外**的用法——`Blend` 命令通过 `[_SrcBlend] [_DstBlend]` 引用 Property，完全不走 HLSL。

## 摘要

Forward rendering 先画不透明（front-to-back 排序，配合 depth test 早剔除），再画透明（back-to-front 排序以保证 blend 正确）。Alpha blending 公式 `输出 = 源·源因子 + 目标·目标因子`——最常见组合 `SrcAlpha` × `OneMinusSrcAlpha` 就是半透明。把这两个因子暴露成 Property 并用 `[Enum(UnityEngine.Rendering.BlendMode)]` 让 Inspector 出下拉，再写 `Blend [_SrcBlend] [_DstBlend]` 就得到"面板选 blend 模式"的通用透明 shader——相加（SrcAlpha + One）、相乘（DstColor + Zero）等。Alpha clipping 另一条路：用 `discard` 或 `clip(v)` 在 fragment 里剔除 alpha < 阈值的像素，常用来画草叶、树叶。Clipping 属于 `AlphaTest` 队列（opaque 之后、transparent 之前），排序仍 front-to-back、仍写深度。作者个人更喜欢 `discard` 的可读性，但猜测两者编译后等价。

## 关键要点

- **Forward rendering 两阶段排序**：opaque front-to-back + transparent back-to-front；深度缓冲支撑前者的早剔除。
- **`Blend` 命令在 Pass 块顶部**：`ZWrite Off` 是透明物体的默认搭档——避免排序错误时互相遮挡。
- **`BlendMode` enum 的 11 个值**：Zero/One/DstColor/SrcColor/OneMinusDstColor/SrcAlpha/OneMinusSrcColor/DstAlpha/OneMinusDstAlpha/SrcAlphaSaturate/OneMinusSrcAlpha——顺序没有规律，作者吐槽。
- **`[Enum(UnityEngine.Rendering.BlendMode)]` 属性**：ShaderLab property attribute；把 Integer property 展示为下拉。
- **`Blend [_Prop] [_Prop]` 语法**：方括号里放 Property 名，ShaderLab 直接引用，**不需要在 HLSL 里声明这个变量**——这是 Part 1 提过的"ShaderLab-only property"的例子。
- **Queue 三档**：`Geometry`（不透明）/ `AlphaTest`（clipping，仍 opaque 但排在 Geometry 后）/ `Transparent`（混合）。
- **`discard` vs `clip(x)`**：前者 C-like 显式语句，后者 HLSL 函数（参数 < 0 时丢弃）；等价，风格差异。
- **clipping 仍写深度**：alpha test shader 属于 opaque 路径，保持 front-to-back + depth write。

## 链接到的概念

- [[alpha-blending]]
- [[alpha-compositing]]
- [[dither-alpha-clipping]]
- [[shaderlab-hlsl-basics]]
- [[blend-modes-shaderlab]]

## 原文

- 链接：<https://danielilett.com/2026-01-01-tut10-03-transparency/>
- 本地：`raw/articles/danielilett.com/2026-01-01_transparency-unity-shader-code-basics-03.md`
