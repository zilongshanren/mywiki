---
title: Graphics Programming weekly - Issue 66 — December 9, 2018
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-66/
author: Jendrik Illner
published: '2018-12-09'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the final part of the series
- presents how different GPUs are able to overlap the workload between
- different async and graphics queues
- work on the same graphics queue

- presents how split barriers influence the overlap
- additionally presents the ability of Windows to preempt GPU work when multiple applications are sharing the same GPU

![](../../assets/85a9fc861d6a3679.png)


- slides for the fluid simulation used in Shadow of the Tomb Raider have been released
- the content of the talk was discussed last week in
[issue 65](https://www.jendrikillner.com/post/graphics-programming-weekly-issue-65/)

![](../../assets/15421a0d32f51681.png)


- next part of the series about the development of a forward shading pipeline using the Unity scriptable render pipeline
- implements support for directional, point, and spotlights
- show how to interact with the Unity provided light culling system

![](../../assets/2b8d583551794ba4.jpg)


- object based shading approach designed for VR rendering
- splits rendering into client and server operations
- the server calculates visible geometry and object space shading
- the results are stored into a shading atlas
- the client receives a preprocessed vertex stream and the shading atlas
- the visible geometry is rendered from a single vertex buffer and shading is applied from the information cached in the shader atlas
- presents the memory management technique and mip-level selection

![](../../assets/819e519dca0c3835.png)


- user created index-page for the Apple Metal documentation
- contains links to samples, class documentation, best practices documents, tools and debugging helper

![](../../assets/0174da56b4f5c16e.png)


- shows how to validate using image comparison and using a furnace test
- how to implement a plastic and glass BSDF
- make the ray tracer less biased through changes to the way the number of bounces is determined

![](../../assets/825c99d83341e0ae.png)


- Khronos talks from Siggraph 2018 Asia
- talks about Vulkan
- memory management, subgroup operations and the design of a FrameGraph style engine architecture

- introduction to WebGL and overview of the latest updates to the GLTF format

![](../../assets/7089ba27a143516f.jpg)


- series of videos walking through the implementation of a software renderer written in multithreaded C++ using SIMD
- presenting the whole pipeline from vertex fetching, vertex processing, culling, projection, binning, rasterization, mipmapping and finally shading

![](../../assets/b98ce05711d109d8.png)


- explains why noise is significant in computer graphics and how to animate blue noise over time so that it retains its properties

![](../../assets/4a6e3697c6a7b782.png)


- video summary of variable rate shading
- presents a few approaches that are used to drive shading rate selection
- what options are exposed in Wolfenstein 2 and how they influence performance and quality

![](../../assets/7cdd20556216a0b8.png)


- new encoding model for Ambient Highlight Direction (AHD) lightmaps that eliminate common interpolation artifacts
- and how to fit AHD from spherical harmonics data

![](../../assets/822fae173e753886.png)


If you are enjoying the series and getting value from it, please consider supporting this blog.

[Support this blog](https://donorbox.org/jendrikillner)