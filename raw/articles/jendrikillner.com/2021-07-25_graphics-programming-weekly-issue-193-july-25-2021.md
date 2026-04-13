---
title: Graphics Programming weekly - Issue 193 - July 25, 2021
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-193/
author: Jendrik Illner
published: '2021-07-25'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article discusses how Visibility Buffer can be combined with Variable Rate Shading (VRS) Techniques
- shows how careful selection of sample positions can archive convergence towards the reference non-VRS image
- presents the performance of VRS usage for forward, deferred, and visibility approaches. Comparing different pixel densities
- additionally discusses techniques how the sparse g-buffers might be integrated into other rendering passes

![](../../assets/05853605b5d14342.jpg)


- the article explains how to express SDFs in Unity and Unreal
- shows the basic steps for a circle SDF
- extends this to show how to animate, combine and blend shapes

![](../../assets/292b692e8cf7c138.png)


- the preprint from Ray Tracing Gems 2 covers two techniques for caustics
- One focuses on the caustics around metallic and transparent surfaces
- the second is for caustics cast by water surfaces

![](../../assets/23cbfa1b04db423c.png)


- the article presents the idea of compensating for shortcomings of an upsample technique in the downsampling step
- shows the development of an improved downsample filter to compensate for bilinear upsampling
- discusses how this is related to the typical sharpening of mipmaps done as part of game art pipelines

![](../../assets/7e1e69a37ca1443b.png)


Threedy is a young Fraunhofer spin-off with a considerable number of high-profile customers in the german automotive sector.

We develop the Visual-Computing-as-a-Service platform instant3Dhub to enable our customers to leverage the true value of their 3D data in industrial applications – any data, any device, any size.

instant3Dhub has a strong focus on CAD data visualization, from browser-based to mixed reality applications and delivers out-of-the-box collaboration and augmented reality features.

We are looking for graphics programming enthusiasts to support our core development team for the 3D streaming with a focus on the evolution of our web frontend build on WebGL.

![](../../assets/2365cbc531701a1a.png)


- the NVIDIA RTX Memory Utility is an open-source (MIT License) SDK designed for reducing the complexity of memory management for Raytracing on Vulkan and D3D12
- shows how to use the utility to integrate acceleration structure memory reduction techniques
- additionally presents how much memory can be saved on different scenes (very scene dependent)

![](../../assets/4399c75b1b11882b.jpg)


- the video discusses the rendering pipeline
- presents the geometry and pixel processing pipeline
- shows how mali hardware implements the API pipeline for more efficient execution

![](../../assets/34ee9c2dc2e9b7e4.png)

- explains how the rendering pipeline translates into GPU hardware
- comparing immediate-mode vs. tile-based GPUs
- presents the pros and cons of both models and why mobile GPUs are tile-based

![](../../assets/60e65c2c0c6c7571.png)

- the video discusses the hardware essentials
- presents how CPUs are designed
- followed by how the design for GPUs is adjusted to take advantage of the graphics workloads

![](../../assets/243163b1a93989f1.png)

- the article discusses tile-based and immediate-mode rendering GPUs in detail
- exploiting how they work
- discussing strengths/weaknesses
- additionally covers how these influence the efficiency of rendering algorithms such as shadow map rendering

![](../../assets/e854a10d3e0cacd7.png)


- whitepaper that discusses how to use printf in Vulkan shaders
- presents how to use shader printf from HLSL, GLSL, and SPIR-V shaders
- additionally covers RenderDoc and validation layer integration

![](../../assets/669db2ced2f118c5.png)


- a collection of Signed-distance field primitives (Cylinder, cubes, …) expressed in WebGPU Shading Language (WGSL)
- additionally contains Boolean operations, displacement, positioning, and rotations for SDFs

![](../../assets/ece48340c9655796.jpg)

- the video provides an overview explanation of Global Illumination
- presents an overview of the fundamental concepts
- covers several techniques that have been used to approximate it
- discussing advantages and disadvantages of the techniques

![](../../assets/102dc2fadf86a881.png)


- the article goes into detail on how to implement physically correct and affordable ray traced soft shadows for individual polygonal or linear lights
- presents an overview of the concept of ray queries (rays that can be inline at each shader stage)
- shows in-depth the steps required for area lights, including importance sampling, diffuse, specular, and texture integration

![](../../assets/7cd2145b5c9953c4.png)

Thanks to [Erika](https://twitter.com/rrika9) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.