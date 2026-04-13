---
title: Graphics Programming weekly - Issue 62 — November 11, 2018
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-62/
author: Jendrik Illner
published: '2018-11-11'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- overview of the compute shader execution and pipeline model
- explains how instructions are executed, what the difference between uniform and non-uniform work is and how it relates to SGPRs and VGPRs
- using the example of texture downsampling to present the performance profile of a pixel shader solution and why a compute shader solution can achieve better performance

![](../../assets/12f8628310a7caf7.png)


- overview of the GPU execution model, the difference between scalar and vector registers and instructions
- explains the concept of scalarization and how wave level instructions enable this process

![](../../assets/344c90862bf4e88a.png)


- walkthrough of two different strategies to scalarize the forward+ shading loop
- provides code, step by step analysis and links to more in-depth presentations

![](../../assets/b93c7ab616c9531e.png)


- overview of some of the technical papers that will be presented during SIGGRAPH Asia 2018, 4-7 December 2018 in Tokyo

![](../../assets/fd29e0e7219b900c.png)


- adding support for multiple meshes and GPU frustum culling and submission
- one Dispatch to execute culling and one ExecuteIndirect is used to draw the rest of the scene

![](../../assets/288709bf60014c18.png)


- improving culling performance through the removal of dummy draw calls
- implementation of LOD selection per mesh
- support querying of pipeline statistics to gather information about the number of triangles drawn

![](../../assets/1ef40f84405dece4.png)


- A walkthrough that explains all the concepts and shaders necessary to ray trace a single colored triangle using the Vulkan raytracing extension

![](../../assets/58b411fa8c17f26b.png)


- explains how to convert the code from the
[Ray Tracing in One Weekend](http://in1weekend.blogspot.com/2016/01/ray-tracing-in-one-weekend.html)book to use CUDA - the source code is available
[here](https://github.com/rogerallen/raytracinginoneweekendincuda), one branch for each chapter

![](../../assets/de0fe8d81bea6259.jpg)


- unity tutorial that explains how to create a signed distance field for a 2D circle and rectangle
- how to apply transformations (translation, rotation, scale) and how to visualize the distance field to aid debugging

![](../../assets/70646826d86f1424.png)


- explains how to implement 3D picking in a Metal application
- overview of coordinate spaces and how to convert between them
- hit-testing performed using a ray vs. bounding sphere test

![](../../assets/bcd5edbfc6f47a07.png)


- a tool, now open source, that allows the compilation of HLSL and shows the disassembly in DXBC and AMD GCN
- includes a small utility to visualize the effect of a fullscreen pixel shader effect


- list of image effects found in tools such as Photoshop with a small explanation and GLSL code snippets

![](../../assets/da22b06fb2d05134.jpg)


If you are enjoying the series and getting value from it, please consider supporting this blog.

[Support this blog](https://donorbox.org/jendrikillner)