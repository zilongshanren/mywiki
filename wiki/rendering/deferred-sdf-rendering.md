---
tags: [渲染, sdf, 延迟渲染, raymarching, unity, 混合管线]
date: 2026-04-14
sources: 1
---

# 延迟管线里渲染 SDF

[[kostas-anagnostou|Kostas Anagnostou]] 2017 年在 Unity 上做的一个小实验：**把解析 SDF 的 raymarching 结果写进 G-Buffer**，让 SDF 与多边形几何共存在同一条 [[deferred-rendering|延迟渲染]]管线里。灵感来自 *Claybook* 与 *Dreams* 这类完全基于 SDF 的游戏，但它们是自研从头到尾的 SDF pipeline；这里的问题反过来：**能否让 SDF 只是 deferred shader 里的一种几何源，其余照常？**

## 关键 trick：renderer 写 G-Buffer + depth

整条管线很简单，但关键是它没有绕过 Unity 的光照与后处理：

1. **一个 full-screen triangle** 在 g-prepass 阶段提交，Vertex shader 是 pass-through。
2. **Fragment shader 里构造 ray**：用远平面深度 1.0 从 clip space 反解 world position，再与 camera pos 相减得到 world-space ray direction——这样 raymarching 用的是和主场景一模一样的相机。
3. **标准 sphere-traced raymarch**，调用 iq 风格的 SDF 基元（见 [[sdf-2d-primitives]] 的 3D 对应）与组合算子。
4. **命中时写 G-Buffer**：albedo / normal / roughness / metalness 都按 Unity 的 *standard* shader 惯例填；这一步让它可以完整继承 Unity 的 PBR 光照。
5. **最关键：输出 depth**。把命中点投到 NDC，写 `clipPos.z / clipPos.w` 到 `SV_Depth`——这样 SDF 与多边形几何在 z-buffer 上**正确互相排序**，可以互相遮挡、互相穿插。

没有这一步，SDF 就只是一张后处理图层。有了它，Unity 的 SSAO、SSR、bloom 这类屏幕空间后处理对 SDF 和多边形**完全无差别地生效**——这是本文最有意思的地方。

## 和 SDF-native 管线的取舍

Anagnostou 自己点出了这个方案的局限。把光照从 SDF 渲染里剥离意味着：

- **丢失高质量反射和阴影**。原生 SDF pipeline 可以利用距离场直接做 [[sdf-ray-marched-shadows|soft shadow]]、cone-traced AO 和反射——这些都是 SDF 特有的便宜操作。放进 G-Buffer 之后光照只剩 deferred shader 算的那一套。
- **但换回来的是**：shader 更短、loop/branch 带来的寄存器压力更低，而且可以直接复用既有引擎的全部光照和后处理基础设施。不是「更好」，是「更工程友好」。

他也提到 shadow map pass 理论上可以同样魔改（让 SDF 也参与光源视角的深度渲染），但代价会显著增加。

## 材质系统的痛点

Unity 的 material 系统允许对 SDF 调 roughness / emissive 等参数——但这些参数对 pass 内所有 SDF 一起生效，因为只有一个 material。想要**单个 SDF 有独立材质**就得自己在 shader 里分发——这暴露了「把 SDF 套进传统 draw-call + material 模型」的根本摩擦：一个 full-screen triangle 里可能包含任意数量的 SDF，但 Unity 的 material 是按 draw 分配的。

## 为什么值得记一笔

这个 experiment 本身「not very useful yet」（作者原话），但它是一个干净的**范式混合样本**：

- **SDF 用得上但不想改整条管线**时，写 depth + G-Buffer 是最低摩擦的入口。
- 和 [[hybrid-raytracing-pipeline]] 类似，这是「rasterization 提供几何骨架，其他技术只填内容」的一种子情况——不同的只是替代物是 SDF raymarch 而不是 ray-traced secondary ray。
- 也顺带回答了一个常见疑问：**后处理需要 depth buffer**，只要你老老实实写了 SV_Depth，SDF 也能白嫖 SSR / SSAO / bloom。

## 相关

- [[deferred-rendering]] —— 本 trick 依附的管线形态
- [[raymarching-intro]] —— sphere tracing 基础
- [[sdf-ray-marched-shadows]] —— 解析 SDF 的软阴影
- [[sdf-2d-primitives]] —— SDF 基元与组合
- [[hybrid-raytracing-pipeline]] —— 另一种「光栅+非光栅几何」混合
- [[volumetric-raymarching-intro]]
- [[kostas-anagnostou]]

## Sources

- [[sources/interplay-deferred-sdf-rendering]]
