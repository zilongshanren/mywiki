---
title: Graphics Programming weekly - Issue 116 — January 26, 2020
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-116/
author: Jendrik Illner
published: '2020-01-26'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article presents how ordering mesh data can influence rendering performance
- compares different algorithms developed for this purpose
- the primary focus is on how to train these algorithms using machine learning techniques
- analyzes the results of different approaches and presents results

![](../../assets/0b2a69b63e76c677.png)

- the article shows how to enable AMD FreeSync using D3D12 and Vulkan
- presents how to use the library to encode color information into the desired HDR display format

![](../../assets/3321d5aef5aa206a.png)

- Vulkan 1.2 has been released
- this release promotes
[23 extensions](https://www.khronos.org/registry/vulkan/specs/1.2/html/chap38.html#versions-1.2)into core Vulkan - including extensions such as imageless_framebuffer, timeline semaphores, and better support for HLSL shaders

![](../../assets/ea31a943e0f48c40.png)

- Microsoft open-sourced two layers to help to port to D3D12
[D3D12 Translation Layer](https://github.com/microsoft/D3D12TranslationLayer)helps mapping from D3D11 style APIs to D3D12 style- Resource binding, renaming, sub-allocation, pooling, and deferred destruction
- Batching and threading
- Residency management

[D3D11On12](https://github.com/microsoft/D3D11On12)is implemented on top of the previous layer and contains the D3D11 specific aspects

![](../../assets/c136aac3baf7d99d.jpg)


- the paper examines k-d trees and bounding volume hierarchies
- comparing the approaches with varying cone sizes

![](../../assets/656bc513d0377bc2.png)

- the article discusses the new timeline semaphore synchronization API included in Vulkan 1.2
- superset VkSemaphore and VkFence allows synchronization between CPU and GPU using a single primitive
- additionally provides support for wait-before-signal submission and multiple waits per signal

![](../../assets/2c0e169fb0f0b5c3.png)

- the code snippet shows how to screenspace extends of a sphere from view space
- an optimized version of
[Clipped Perspective-Projected 3D Sphere](http://jcgt.org/published/0002/02/05/paper.pdf)

![](../../assets/b60416da80bc52f6.png)

- the article presents how Grassmann (Geometric) Algebra extends four-dimensional homogeneous coordinates into a larger algebraic structure

![](../../assets/855ab1ae8bca008f.png)

- the Unity tutorial shows to implement the stylized lava effect discussed in the previous article using Shader Graph

![](../../assets/f96f7ea1c3334f49.png)

- the author presents his opinions about how a rendering abstraction layer should be designed
- additionally offers his thoughts on Render Graphs, Meta Command Buffers, and meta shader languages

![](../../assets/506b97b40665730b.jpg)

- presents an improved precision method for normal reconstruction from depth buffers
- the technique uses 5 depth samples in each direction

![](../../assets/aad36050cd52c4de.png)

- the article presents a few approaches to skybox rendering
- introduces how to use the min/max depth of the D3D12 viewport to force skybox to a max depth
- the comments present other approaches

![](../../assets/e719a8715ee7c560.png)

- the paper introduces a technique for improving the computation time required for lightmap baking
- based on guided sampling and minimum variance-based estimator combination
- the method has a fixed memory footprint and is independent of scene complexity

![](../../assets/9b84f4c037a39772.png)

- the article shows how to use Node bindings to enable RTX support when using WebGPU
- provides a brief overview of the DXR API and presents how to use the API to set up the pipeline and render an animated mesh

![](../../assets/e14717bf5e563688.png)

- the article presents the shader nodes from Unity ShaderGraph system
- explains how to use the nodes, what options are available and how to combine them

![](../../assets/e91b0d66b2a3df7b.png)

- the article presents code and explains the logic behind correct dithering patterns that preserve the brightness

![](../../assets/aa023f491d6e86ca.png)

Thanks to [Jasper Bekkers](https://twitter.com/JasperBekkers/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.