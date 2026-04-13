---
title: Graphics Programming Weekly - Issue 394
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-394/
author: Jendrik Illner
published: '2025-06-09'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- details the rendering techniques used in the latest Assassin’s Creed game
- explores the GPU-driven rendering pipeline, micro polygon rasterization, global illumination implementation
- presents how the weather system was implemented in a deferred pipeline fashion
- additionally presents a brief look at how the team manages platform differences and performance tracking

![](../../assets/5fb45e3b5f14ff13.png)


- talk from Nordic Game Jam 2025 providing an intuitive explanation of quaternion mathematics
- breaks down quaternion concepts using visual examples and practical applications in game development
- demonstrates techniques for visualizing rotations
- additionally presents how rotation order/axis orders vary between different popular game engines

![](../../assets/85339bfa708ca9f2.png)


- presents a mathematical derivation for efficiently transforming direction vectors from camera space to screen space
- reduces computation from 32 multiplies, 24 additions/subtractions, and four divides to just six multiplies and two subtractions

![](../../assets/75ff694de838df1d.png)


- walks through the implementation of a CPU-based software rasterizer
- covers techniques for triangle rasterization, projections, depth buffering, basic lighting
- explains the underlying theory with visual explanations before presenting the implementation

![](../../assets/bcc78f27970c749e.png)


- investigates techniques to improve Bounding Volume Hierarchy (BVH) quality
- challenges common assumptions about binned vs. full-sweep SAH building and demonstrates that bin count significantly impacts performance
- introduces Representative Ray Sets (RRS) for BVH quality assessment and optimization, showing that significant performance improvements ( >50% ) are possible
- opening the discussion that offline builds of optimized static geometry BVHs might be worthwhile to explore

![](../../assets/c291dc0529fe4b42.jpg)


- explores asynchronous compute techniques to improve GPU utilization by executing compute and graphics workloads in parallel
- explains the implementation details of scheduling work on separate command queues and synchronizing between them using fences
- provides practical examples of work pairing that benefits from async compute and how to measure performance gains

![](../../assets/b8d057532fae4f5e.png)


- introduces Shader Execution Reordering feature for Shader Model 6.9
- explains how SER allows application developers to provide hints that will enable drivers to optimize execution patterns for DXR workloads
- provides example code that presents the feature in shader code and how to use it from the D3D12 API
- additionally discusses the state of driver support

![](../../assets/04bf9983e5c664d5.jpg)


- introduces Opacity Micromaps (OMMs) for DirectX 12 ray tracing to accelerate alpha-tested geometry
- details how OMMs encode alpha mask information at different resolutions to skip unnecessary ray-triangle tests
- provides implementation explanations, first example implementations, and performance data for foliage scenes

![](../../assets/4ab925cd77d39523.png)


- presents DirectX 12’s new cooperative vector instructions
- discusses how these instructions allow developers to take advantage of additional hardware features (such as Nvidia Tensor Cores)
- shows how to check for the availability of support and how the API allows developers to encode the data into the hardware-required formats

![](../../assets/cad5e5f8205c49db.png)


- the video tutorial implements a physics-based cloth simulation on the GPU using compute shaders
- discusses how to structure the mesh for connectivity as well as how to handle constraints solving to simulate springs
- covers both the theory as well as the implementation

![](../../assets/700dfe4c21a5bc43.png)


- announces the addition of Slang shader language support for the Vulkan samples repository
- discusses the experience of using Slang for shader development

![](../../assets/e920ea9687228b69.png)

Thanks to [Robert Wallis](https://github.com/robert-wallis) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.