---
tags: [人物, 作者, 引擎作者]
date: 2026-04-19
sources: 5
---

# Panagiotis Christopoulos Charitos

希腊图形程序员，开源引擎 [AnKi 3D Engine](https://github.com/godlikepanos/anki-3d-engine) 的作者与长期维护者（2006 年立项至今）。在 anki3d.org 博客上以工程师视角记录引擎每一次大改：Vulkan 移植、bindless 化、GLSL→HLSL 切换、GPU-driven 管线、光追化简、pipeline barrier 抽象等。

文字风格一致：承认"这是一个 compromise"、把"nVidia 会吞错、AMD 会暴露、Vulkan validation 不会警告"这种硬件差异写进正文，适合作为"现实里工程师怎么规避 API 边角坑"的参考样本。

## 相关

- [[spirv-parsing-rewriting]] —— 自己啃 SPIR-V 二进制而不依赖 SPIRV-Cross
- [[mesh-shader-vulkan-hlsl-per-primitive]] —— HLSL + Vulkan mesh shader 的 PerPrimitiveEXT 坑
- [[simplified-pipeline-barriers]] —— 把 25 个 stage + 30 个 access flag 压成 2 个 enum
- [[minimalist-rt-acceleration-structures]] —— 只用 ray query + TLAS instanceCustomIndex 的"土豆级"光追

## Sources

- [[sources/anki-spirv-parsing-rewriting]]
- [[sources/anki-mesh-shader-vulkan-hlsl]]
- [[sources/anki-gpu-driven-rendering-video]]
- [[sources/anki-simplified-pipeline-barriers]]
- [[sources/anki-minimalist-ray-tracing]]
