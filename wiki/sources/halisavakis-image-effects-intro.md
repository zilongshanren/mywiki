---
tags: [source, rendering, shader, unity, tutorial]
date: 2026-04-14
sources: 1
---

# My take on shaders: Introduction to image effects（Harry Alisavakis / Technically Art）

[[harry-alisavakis]] 于 2017 年 4 月发表的「My take on shaders」系列第一篇，面向完全没写过着色器的 Unity 初学者，用 Unity 自带的 InvertColor 模板讲清楚 image effect（全屏后处理）着色器是怎么拼起来的。

## 摘要

作者从 Unity 菜单 `Shader > Image Effect` 生成的默认反色模板切入，按块讲解 ShaderLab 文件的组成：最顶层的 `Shader "Custom/..."` 定义名字和菜单路径；`Properties` 块声明外部可调的参数（名字、编辑器标签、类型、默认值），image effect 的 `_MainTex` 会自动被运行时赋值为相机输出；`SubShader` 里的 `Cull Off ZWrite Off ZTest Always` 表示全屏四边形不需要深度剔除；`appdata` 和 `v2f` 结构体负责从顶点到片元传递位置和 UV；顶点着色器只做坐标变换、UV 透传；[[fragment-shader]] 里 `tex2D(_MainTex, i.uv)` 取相机颜色再做一次 `col = 1 - col` 就完成反色。作者特别点破一个新手卡点：Properties 里声明过的变量必须在 CGPROGRAM 段里**同名再声明一次**，因为 CG 代码是真正喂给 GPU 的，而 Properties 块只负责 Unity 编辑器侧的绑定。最后给出一段十行的 `OnRenderImage` MonoBehaviour，用 `Graphics.Blit(src, dest, material)` 把 image effect 挂到相机上。

## 关键要点

- Unity image effect 本质是一次相机输出到目标的 blit，shader 的 `_MainTex` 被自动设为相机渲染结果
- `Cull Off ZWrite Off ZTest Always` 是全屏后处理 pass 的标准三件套，避免深度/剔除干扰
- Properties 块只是编辑器端的绑定接口，真正的 HLSL/CG 代码里必须把同名变量再声明一次才能被 GPU 读到
- `fixed4`/`float4`/`half4` 的语义一致，只在精度和性能上有差别，`col.rgba` 就是当前像素的颜色通道
- `OnRenderImage(src, dest)` + `Graphics.Blit(src, dest, material)` 是挂接自定义后处理到 Unity 主相机的标准模式（注：这是 built-in 管线时代的做法，URP/HDRP 下要走 [[blit-render-feature]]）
- Alisavakis 写这篇时自认还是 shader 新手，文章语气是「把自己当初被卡住的点翻译出来给初学者」，后来这一视角发展成了完整的 ShaderQuest 系列

## 链接到的概念

- [[unity-image-effect-basics]]
- [[fragment-shader]]
- [[shaderlab-hlsl-basics]]
- [[blit-render-feature]]

## 原文

- 链接：<https://halisavakis.com/my-take-on-shaders-introduction-to-image-effects/>
- 本地：`raw/articles/halisavakis.com/2017-04-12_my-take-on-shaders-introduction-to-image-effects.md`
