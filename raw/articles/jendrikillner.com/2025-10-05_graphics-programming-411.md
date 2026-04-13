---
title: Graphics Programming 411
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-411/
author: Jendrik Illner
published: '2025-10-05'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- proposes teaching GPU programming through compute shaders before graphics pipelines
- demonstrates starting from simple compute shaders in Vulkan, and using RenderDoc debugging as an essential teaching tool
- presents how to develop from this to understand the execution model, binding model, and how to integrate shader toy examples
- additionally presents next learning steps

![](../../assets/cf3f1db632321f35.png)


- details the theory and mathematics behind FFT-based ocean simulation
- covers oceanographic spectra including JONSWAP and TMA, directional spreading functions, and dispersion relationships
- presents implementation details for cascaded simulation and FFT using compute shaders

![](../../assets/5f449e475d379f6d.png)


- video analyzing DLSS image quality on Nintendo Switch 2
- compares different DLSS implementations and their visual quality

![](../../assets/10b8fc0afdc638a7.png)

- presentation covering the GPU rendering optimization process in Avowed using Unreal Engine
- shares insights from the development process and technical challenges encountered
- covers aspects from art authoring, material optimization, ray tracing, nanite tweaks, and much more

![](../../assets/fcd572c669c22d4a.png)


- presents an adaptive voxel-based approach for order-independent transparency rendering
- demonstrates performance and quality against other OIT methods

![](../../assets/c18aea98d438d7a8.png)


- video presentation on ray tracing implementation in Assassin’s Creed: Shadows
- focuses on the algorithms and implementations
- followed by the challenges specific to AC and a look at performance
- additionally discusses the limitations of the presented techniques

![](../../assets/09d1ed9485424aa2.png)


- tutorial covering GPU instancing for rendering of grass efficiently
- explains setup using Graphics.RenderMeshPrimitives and compute buffers for instance data
- includes GPU frustum culling implementation and optimization techniques for Unity

![](../../assets/02be37c1a4656432.png)


- presents the creation of a 448-character GLSL procedural demo featuring mountains, clouds, and fog
- explains techniques for generating noise using sine waves, rotation matrices, and FBM accumulation

![](../../assets/bd9c2d6d7fb1f491.png)


- XDC 2025 talk providing an overview of resource mapping from API and hardware perspectives
- discusses the differences in approaches to descriptors and how varios drivers map it onto the hardware
- additionally presents a preview of the new descriptor model coming to Vulkan

![](../../assets/5d0ea76095f691c6.png)


- details optimization work improving meshoptimizer’s hierarchical clustered LOD generation
- achieves 3.5x speedup through addressing memory sparsity, thread balancing, and SIMD optimizations
- demonstrates processing NVIDIA’s 1.64 billion-triangle Zorah scene in under 3 minutes, down from 30 at the start of the article

![](../../assets/83b240c8eab21b5c.jpg)


- comprehensive guide covering GPU architecture fundamentals, including memory hierarchies and compute pipelines
- explains PTX/SASS assembly languages and analyzes compiler-generated code from CUDA kernels
- progresses from warp-tiling synchronous kernels to SOTA Hopper asynchronous implementations using TMA and tensor cores

![](../../assets/19610fc28c1faa70.png)


- video summarizing the Game Optimization series of video tutorials
- recaps key optimization techniques covered throughout the series
- discusses future content directions and advanced optimization topics

![](../../assets/f8156128f4e14b18.png)

- video from 3Blue1Brown explaining the mathematical foundations of complex exponents
- connects dynamics and Euler’s formula through visualization

![](../../assets/649531d7f8b481b2.png)

Thanks to [Nathan Reed](https://www.reedbeta.com) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.