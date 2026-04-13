---
title: Graphics Programming weekly - Issue 169 — February 7, 2021
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-169/
author: Jendrik Illner
published: '2021-02-07'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- Shows how to sort data on the GPU using Bitonic Merge Sort networks using GLSL/Vulkan compute
- Derives how to non-recursively calculate per-thread index pairs for sorting networks
- Explains how to orchestrate compute-shader dispatches for large input data
- provides example implementation that sorts pixel by the brightness

![](../../assets/0a9e84aafbd33c91.png)


- the article presents how to implement ice shading
- uses an approximate for ice refraction controlled by textures and fresnel shading
- effect is implemented using Unity Shader Graph

![](../../assets/1b4a8ef1ba60f6bf.png)


- the video shows how to implement fireworks using fullscreen shader using Shadertoy

![](../../assets/990f1f16931cb76a.png)

Ubisoft RedLynx is a multiplatform game development studio located in Helsinki. Along with the hugely popular Trials series, we have developed and published more than 100 games and we are a passionate team of over 140 people of 21 different nationalities. We are seeking an experienced Graphics Programmer to join our core technology team in creating impactful game experiences

![](../../assets/4cfddfae173473e2.png)


- the paper presents a method that maps spacial search in a fixed radius into a ray tracing paradigm
- this allows the ways to take advantage of ray tracing hardware to speed up the operations
- presents an application for GI with progressive photon mapping and point-cloud registration of partial surface scans

![](../../assets/8039ba5ca1722066.png)


- the article presents a walkthrough of a stylized crystal shader implemented using Unity Shader Graph
- effect is implemented as an unlit effect based on color gradient and uses a copy of the scene to implement a refraction approximation

![](../../assets/24db202757f1e2b2.jpg)


- the article provides an overview of a GPU voxel renderer using raytracing
- shows the data structure layout, how GPU and CPU updates are overlapped
- presents a technique to archive interactive world updates by using incremental parallel updates
- additionally offers advice to improve the performance of the multi-threaded implementation

![](../../assets/8941f0b924d8249f.png)


- the article presents a comparison of DLSS 2.0 and the default TAA implementation of UE 4.26
- comparing performance and quality

![](../../assets/91214003cdd785d0.png)


- the Twitter thread presents an overview of the stylized g-buffer based rendering pipeline implemented using Unity
- presents how each material ID written into the g-buffer is later used to adjust post effects based on the affected materials
- lighting is applied in two stages with a second pass to toon ramp combined lights as well

![](../../assets/d695c84521a4692d.jpg)


- the post presents an overview of optimizations done for Godot 4.0
- list contains but CPU and GPU optimizations
- offers a good starting point for everyone looking into optimizing their own renderers

![](../../assets/63bd5bad152e5246.png)


- the article presents an overview of a simple GPU based path tracer written in Zig
- shows how to have two data layouts for changing scenes vs. static scenes
- presents how to implement spectral rendering and how it affects objects made from glass

![](../../assets/46c46ccd76f5c629.png)

Thanks to [Jonathan Tinkham](https://zincfox.red) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.