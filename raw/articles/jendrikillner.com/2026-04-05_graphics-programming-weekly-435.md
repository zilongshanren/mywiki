---
title: Graphics Programming Weekly 435
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-435/
author: Jendrik Illner
published: '2026-04-05'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- announces v1.1 of meshoptimizer, introducing two major new features, meshlet compression and opacity micromap rasterization
- The new method compresses meshlet topology, exploiting spatial locality, and provides an example compute shader decoder
- The opacity micromap support generates hardware-ready OMM data from mesh UVs and a texture alpha channel for direct use with VK_EXT_opacity_micromap or DXR 1.2

![](../../assets/b0d2b87909e42ff9.png)


- presents a single-pass, GPU-friendly terrain erosion filter that produces branching gullies and ridges, making it suitable for infinite or chunked terrain generation
- the technique uses gradient-aligned sine wave stripes subdivided into Voronoi cells to form gullies;
- Several refinements are described to preserve crisp peaks and valleys
- The Shadertoy example is provided

![](../../assets/e56265718ae63581.png)


- explains a three-control approach to color low-poly terrain driven entirely by geometry: a slope gradient, a height gradient, and a blend curve that determines which of the two governs each elevation band
- demonstrates the approach in Unity “Polaris” terrain tool

![](../../assets/bd384bc34a83cbe2.jpg)


- describes how to extend the Slug algorithm’s GPU implementation to render vector color emojis at arbitrary scale with no prerendered bitmaps
- covers how to deal with COLRv0 (flat color) and COLRv1 (gradient)

![](../../assets/8de383a255037c72.png)


- presents a framework that decomposes a single static anime illustration into a manipulatable model
- discussed as a starting point for artists to eliminate manual segmentation work
- uses a diffusion-based transparent layer generation model combined with a fine-tuned depth estimator

![](../../assets/5feef73d87874523.jpg)


- interview with Ignacio Castaño covering the development of Spark, a real-time GPU-based texture encoder for block-compressed formats
- explains why GPU-native formats require random per-block access and therefore cannot use entropy-coded formats like JPEG
- details the challenges of encoding ASTC on mobile GPUs
- discusses the main practical use cases that emerged for Spark

![](../../assets/32d90895862f8b6f.png)


- GDC 2026 session showing how Slang modernizes graphics development through generics, interfaces, and first-class differentiable programming
- presents a demo of Slang-compiled shaders running on current-gen console devkits
- deconstructs how Slang’s intermediate representation maps to console APIs
- providing a blueprint for extending the language to other systems

![](../../assets/8249365197baa0fa.png)


- covering the current state of real-time path tracing, includingShader Execution Reordering, RTX Mega Geometry, DLSS, and RTX Neural Shading
- presents best practices, optimization strategies
- previews techniques envisioned for next-generation path-traced visuals

![](../../assets/0105be7bc3767886.png)


- presents how NVIDIA uses Nsight in daily validation systems to analyze many game titles across a wide matrix of environments, catching performance regressions and identifying optimization opportunities at scale
- walks through concrete examples of real game optimization problems
- provides a deeper look at the NVIDIA hardware capabilities behind ray tracing and other RTX features

![](../../assets/f50f64653b0aa2cf.png)


- an April 1st experiment exploring whether a Vulkan image can be filled per-pixel using only CPU-recorded commands
- achieves this by aliasing a VkBuffer and a VkImage to the same VkDeviceMemory allocation and writing through vkCmdFillBuffer

![](../../assets/5ba87e88f66e37db.jpg)


- a small Win32 command-line tool for tracking GPU memory usage and demoted memory across all running processes on Windows
- visualizes how much VRAM has been demoted to system RAM

![](../../assets/1051c79266866d40.jpg)

Thanks to Stephen Hill for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.