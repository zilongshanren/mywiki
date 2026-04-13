---
title: Graphics Programming Weekly - Issue 410
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-410/
author: Jendrik Illner
published: '2025-09-28'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- details Figma’s migration from WebGL to WebGPU
- presents challenges in modernizing the graphics interface, including shader processing, uniform buffer management, and cross-platform deployment
- discusses the rollout strategy with dynamic fallback systems and device compatibility testing

![](../../assets/2e97eceb81eefd9f.png)


- step-by-step tutorial series on implementing Vulkan ray tracing with KHR extensions
- guides readers through acceleration structures, ray generation, and shader binding with practical code examples
- highlights recent improvements: Vulkan 1.4 support, VMA integration, Slang shader compilation, glTF 2.0 asset loading, and a cleaner codebase

![](../../assets/8152f5a8d1d4b4ee.png)


- announces new DirectX Agility SDK release featuring the advanced shader delivery system
- presents the various steps of the process
- talks about pipeline data collection, offline compilers, as well as new APIs

![](../../assets/128e109f502c1bc3.png)


- PIX tool update with support for tracking driver & application combination specific state
- supports recreation of resource at specific virtual addresses for improved playback
- additionally contains various other fixes

![](../../assets/ec0ecab3187ef996.jpg)


- introduces animation capabilities for AMD’s Dense Geometry Format (DGF) with linear vertex blending techniques
- demonstrates the animation pipeline that overwrites vertex positions within DGF blocks each frame
- shows quantization approaches and the effects on performance

![](../../assets/cbd102d84f462ae2.png)


- research paper introduces high-level GPU programming abstractions in Rust using procedural macros for automatic code generation
- presents linear pipeline parallel patterns for simplified GPU execution
- benchmarks against manual OpenCL implementations

![](../../assets/1e68fae35b36a566.png)


- clarifies common misconceptions about rejection sampling techniques in statistical computing and graphics
- explains the mathematical foundations and implementation considerations
- showing how to combine multiple sample distributions to improve sample efficiency

![](../../assets/cf9402ce0797074b.png)


- The blog post discusses performance issues related to Anisotropic samples found on Indiana Jones and the Great Circle, as well as DOOM
- presents an algorithm that can be used to vary AnisotropicSampleCount in a dynamic resolution scenario
- additionally brings up the option of using the same technique for values where infrequent change, particularly with a moving camera, may go unnoticed

![](../../assets/a9f9ea8207e0ddff.jpg)


- announces the schedule for the Graphics Programming Conference in Breda, Netherlands, later this year
- covers a large variety of topics

![](../../assets/017049ae062bf864.png)


- video tutorial focusing on GPU shader optimization techniques
- covers common shader bottlenecks, how to identify performance issues, and possible solutions
- presents optimization scenarios in both Unreal and Unity

![](../../assets/26622ebd6b6da89b.png)


- comprehensive tutorial implementing physically based rendering (PBR) in OpenGL using the GLTF 2.0 format
- covers material property handling, including albedo, metallic, roughness, and normal mapping
- demonstrates proper lighting calculations and implementation of the PBR shading model

![](../../assets/87c308c3c6ba80f4.png)


- starts by providing an overview of the current landscape of upscaling techniques and associated performance and quality effects
- explores CRT display emulation techniques, focusing on spatial scaling algorithms
- demonstrates methods for accurately reproducing retro gaming visuals on modern high-resolution displays

![](../../assets/7a4a89e28b739120.png)

Thanks to Stephen Hill for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.