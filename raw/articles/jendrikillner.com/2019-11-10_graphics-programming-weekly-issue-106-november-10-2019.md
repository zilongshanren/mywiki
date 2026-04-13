---
title: Graphics Programming weekly - Issue 106 — November 10, 2019
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-106/
author: Jendrik Illner
published: '2019-11-10'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the paper presents a modification of histogram-preserving tiling algorithm discussed in
[issue 45](https://www.jendrikillner.com/post/graphics-programming-weekly-issue-45/) - it removes the lengthy 3D optimal transport preprocessing step and replaces it with per-channel lookup tables
- aims to reduce clipping and ghosting artifacts
- provides multiple blend modes that treat quality for performance

![](../../assets/9d0a71a39fdd47b7.png)


- the article explains the problem with the classic GPU geometry pipeline
- mesh shaders allow kernels to execute on sub-parts of meshes and output per-vertex and per-primitive attributes
- amplification shaders are run before, and output decide how many mesh shaders to launch
- shows code examples on how to use the feature in both HLSL and C++ API
- ExecuteIndirect also supports launch mesh shaders from the GPU

![](../../assets/6222ab48b7b80d18.png)


- the article explains what has been added with DXR tier 1.1
- it doesn’t require new hardware features but needs a new windows version and driver support
- provides an alternative to that doesn’t use separate dynamic shaders or shader tables
- inline shaders allow all shader stages to trace rays
- additionally added features are DispatchRays generated on the GPU
- growing state objects, GeometryIndex() in ray shaders, flags to skip triangles / procedural geometry

![](../../assets/5283128c582f9a4e.png)


- new Vulkan guide by Khronos
- a crucial starting point for getting started with Vulkan
- provides an overview of the ecosystem, components of Vulkan, tools, …
- additionally contains links to specific usage patterns and further information

![](../../assets/f7cf1bf6c3e6045c.png)


- the article presents the use-case of the streaming system and texture space shading
- sampler feedback is a hardware feature that allows D3D12 shaders to write to a texture which MIPS has been accessed
- FeedbackTexture2D is a new HLSL resource type to express it
- the granularity of the feedback map is user-controlled

![](../../assets/c02d29e208d34958.png)


- Twitter thread about possibilities of texture-space shading
- Sampler Feedback addition in D3D12 can improve the implementations

![](../../assets/7a03db40ceb413ff.png)


- the paper introduces a technique for improving the computation time required for lightmap baking
- based on guided sampling and minimum variance-based estimator combination
- the method has a fixed memory footprint and is independent of scene complexity

![](../../assets/32287ff716b5d5b1.png)


- the paper introduces a technique for translation of materials between different renderers
- using an image-based metric for uniform and texture based paramterization

![](../../assets/e2793ad965063a0c.png)


- the video shows how to modify the SDF of any geometrical shape to make its edges more rounded

![](../../assets/d864474b3861b005.png)

Thanks to [Jasper Bekkers](https://twitter.com/JasperBekkers/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.