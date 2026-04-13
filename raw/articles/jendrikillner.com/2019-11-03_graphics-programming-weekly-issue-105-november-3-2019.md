---
title: Graphics Programming weekly - Issue 105 — November 3, 2019
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-105/
author: Jendrik Illner
published: '2019-11-03'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the post introduces new D3D12 features available with latest win10 preview version
- DirectX Raytracing Tier 1.1 introduces ExecuteIndirect, dynamic raytracing PSO additions and Inline Raytracing
- Inline Raytracing allows RayQuery to be called from every shader stage
- DirectX Mesh Shader are similar to nvidia mesh shaders, allowing more flexibily in the vertex processing pipeline
- DirectX Sampler Feedback allows the recording of which parts of textures have been accessed
- enabling more fine grained streaming and texture space shading scenarios

![](../../assets/a9876505c82e256d.png)


- the video explains the basic of shaders in Unity for beginners

![](../../assets/cfc058292174e9ca.png)


- the ARM developed sets of samples to showcase best practices for Vulkan on mobile is now open-source and part of Khronos
- article has list of samples and tutorials for a number of different areas

![](../../assets/b6d3f430ff71a1a8.jpg)


- Khronos published a unified Vulkan Samples Repository
- all samples are based on the same framework and have been reviewed and are maintained by Khronos

![](../../assets/cbb5c697ac99cba0.jpg)


- the article shows the Unity shader implementation for stylized and unlit grass
- a geometry shader is used to spawn a variable number of grass blades based on camera distance
- grass movement by wind is emulated with a displacement texture

![](../../assets/87821f0c1f82bda7.png)


- starts by showing how to create a small 2D world procedurally
- small overview of explicit vs implcit surface ray tracing
- then shows the steps used to render a procedural mini planet
- including ocean waves, mountains and clouds

![](../../assets/7349c1d83f97f37d.png)


- summary of SIGGRAPH 2019 for a hybrid solution between temporal anti-aliasing with adaptive ray tracing
- using heuristics to detect when adaptive ray tracing provides the best improvements

![](../../assets/d03f0fce2128dde1.png)

Thanks to [Michael Riegger](https://www.linkedin.com/in/michael-riegger-33b55a11/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.