---
title: Graphics Programming weekly - Issue 125 — March 29, 2020
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-125/
author: Jendrik Illner
published: '2020-03-29'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article presents what Hierarchical depth buffers are, what they are used for and how to generate them
- two different techniques for calculating these buffers are presented
- one pixel shader based method and a compute shader variation
- the compute shader variation is designed to only generate a single MIP level, not a full MIP chain
- presents a performance comparison between the two techniques

![](../../assets/b696845b497058e9.png)


- the Unity tutorial explains how to implement a cone of sight that is occluded by objects
- intersection with the primary scene depth buffer allows constraining the effect to the surface of the terrain
- a secondary “shadow map” from the position of the player is used to detect occlusion in the cone

![](../../assets/72fdae5c728f927f.png)


- collection of link resources from GDC, GTC
- additional resources from Google, Intel, Ubisoft and Khronos

![](../../assets/ca61f407ae9ddf74.png)


- new Pix for Windows release with support for DXR 1.1, Mesh shaders and sampler feedback
- also includes updated timeline news with the correlation between CPU and GPU work
- additionally adds support for DXIL source-level debugging

![](../../assets/b77a10fa1173374c.jpeg)


- GPU Trace and Nsight Aftermath now supports Vulkan
- Advanced mode for GPU Trace collects more in-depth information over several continues frames

![](../../assets/79eda86ff7c30929.png)


- the author presents his domain-specific language and how it’s used to extend shaders
- allows all state required for pipeline objects to be encoded as part of the shader code

![](../../assets/20091190a01bf2ad.png)


- the article presents best practices for multithreaded command recording with Vulkan
- show performance comparisons of different methods and discusses common mistakes

![](../../assets/2c8b34cb5d081fda.png)


- the article contains many best practices for WebGL applications
- discussing a large number of topics including memory estimation, performance guidelines, GLSL tips, texture performance, and constraints
- additionally covers some WebGL 2.0 and Canvas related advice

![](../../assets/1175c94d29ea9ced.png)


- Microsoft and Collabora are working together to implement an OpenCL and OpenGL layer for Mesa that is running on D3D12
- provides a summary of what Mesa 3D is and why API translation is important
- also provides an overview of the implementation

![](../../assets/6ee2340cb85525ae.png)


- presentation from Intel that presents how to use multiple adapters with D3D12
- techniques for work-sharing and dealing with synchronization
- offers performance numbers for the presented methods, best practices, and possible problems

![](../../assets/08b6eb3681f085d0.png)


- the presentation provides an overview of Variable Rate Shading (VRS), explaining what shading and rasterization rate are
- shows what settings implicitly disable VRS on Tier 1 intel hardware
- presents how VRS is integrated into Unreal Engine 4, Chivalry II
- gives performance and quality examples for both

![](../../assets/b4dc7438be369c69.png)


- Nvidia released the RTX Global Illumination (RTXGI) SDK v1.0
- SDK provides a framework for realtime GI for games, it offers full source code
- post contains a video overview of the techniques from GDC 2019

![](../../assets/46694a0f63ea9b35.png)


- Nvidia released a new version of the DDS exporter
- improved mathematically correct filtering for mipmap generation adjusted to the content of the image
- support for high-quality BC7 and HDR formats

![](../../assets/80c82a7b5dc47021.png)

Thanks to [Graham Wihlidal](https://www.wihlidal.com) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.