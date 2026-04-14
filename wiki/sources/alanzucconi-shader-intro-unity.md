---
tags: [source, shader, unity, 入门, built-in-rp]
date: 2026-04-14
sources: 1
---

# A Gentle Introduction to Shaders in Unity（Alan Zucconi）

[[alan-zucconi]] 发表于 2015 年 6 月的 Unity Shader 教程系列第 1 篇，面向"几乎没接触过 shader"的读者，梳理 Unity 内建渲染管线时代 shader 的基本骨架与两种写法的取舍。

## 摘要

文章首先把渲染流水线拆成三个角色：3D 模型（带顶点、法线、UV 的顶点集合）、材质（shader + 参数的包装）、shader（GPU 上为每个像素跑的程序）。随后给出 ShaderLab 的最小结构：`Shader { Properties { ... } SubShader { ... } }`，Properties 对应 material Inspector 中的公共字段（Texture 2D、Int、Float、Range、Color、Vector 七种基本类型），而 SubShader 内部用 Cg / HLSL 声明同名变量并写实际计算逻辑——ShaderLab 只是 UI 绑定层，HLSL 才是 GPU 跑的代码。作者特别强调 `Queue` tag（Background/Geometry/Transparent/Overlay）控制渲染顺序，以及 ZTest（深度缓冲）在透明物体上的陷阱。最后对比了 Surface Shader（填 `surf` 函数，自动接入 Lambert/BlinnPhong 等 [[physically-based-shading|光照模型]]，适合贴近真实光照的材质）和手写 Vertex/Fragment Shader（`vert` 把顶点从对象空间经 `UNITY_MATRIX_MVP` 变换到裁剪空间，`frag` 返回最终像素颜色，适合 2D / 后处理 / 复杂特效），为后续 4 篇教程（Surface / PBR 光照 / Vertex & Fragment / Screen 后处理）铺垫入口。

## 关键要点

- Unity shader 是 **ShaderLab 外壳 + Cg/HLSL 内核**的两层结构；Properties 必须在 SubShader 里**再声明一次**变量，因为 ShaderLab 只做 Inspector 绑定。
- Properties 七种基本类型：`2D`（纹理，可初始化为 white/black/gray/bump）、`Int`、`Float`、`Range(min,max)`、`Color`（RGBA，`half4`）、`Vector`（XYZW，`float4`）。
- `Queue` tag 按整数控制渲染顺序（Background 1000 / Geometry 2000 / Transparent 3000 / Overlay 4000），可以写 `Background+2` 这种相对偏移。
- **ZTest 与 Queue 是两件事**：Queue 决定绘制顺序，ZTest 决定绘制时是否因为更远被深度缓冲剔除；不透明物体通常靠 ZTest 就能正确遮挡，透明物体才依赖 Queue。
- **Surface Shader vs Vertex/Fragment**：前者把光照循环藏起来，开发者只填 `surf` 函数写 Albedo 等表面属性；后者完全手写，`vert` 负责坐标变换（`UNITY_MATRIX_MVP` 封装了 MVP 乘法）、`frag` 负责着色。光照相关用 Surface，2D / 后处理 / 特效用 Vertex/Fragment。
- 手写 Vertex/Fragment 必须包在 `Pass { CGPROGRAM ... ENDCG }` 内；Surface Shader 则可省略 `Pass`。

## 语境与局限

这篇教程写于 2015 年，当时 Unity 还是**内建渲染管线（Built-in RP）** 的天下，Surface Shader 被推崇为"避免重复样板"的主力写法。到了 URP / HDRP 时代，Unity **放弃了 Surface Shader 模板生成**——所有 shader 都必须手写 `HLSLPROGRAM` 代码块，并 include URP 的 `Core.hlsl`、使用 `TransformObjectToHClip` 代替 `UNITY_MATRIX_MVP`。因此这篇文章对理解 shader 骨架仍然非常有价值，但具体 API 和推荐的写法已经过时；更现代的等价内容见 [[shaderlab-hlsl-basics]]（Daniel Ilett 的 URP 版）和 [[unity-surface-shaders]]（Surface Shader 的回顾与局限）。

## 链接到的概念

- [[shaderlab-hlsl-basics]]
- [[unity-surface-shaders]]
- [[fragment-shader]]
- [[physically-based-shading]]

## 原文

- 链接：https://www.alanzucconi.com/2015/06/10/a-gentle-introduction-to-shaders-in-unity3d/
- 本地：`raw/articles/alanzucconi.com/2015-06-10_a-gentle-introduction-to-shaders-in-unity-shader-tutorial.md`
