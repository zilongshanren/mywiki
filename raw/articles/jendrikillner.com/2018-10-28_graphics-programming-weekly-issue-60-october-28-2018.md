---
title: Graphics Programming weekly - Issue 60 — October 28, 2018
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-60/
author: Jendrik Illner
published: '2018-10-28'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- brief overview about what mips are and how to calculate mip selection in a rasterizer
- explains ray differentials, a technique that can be used for mip selecttion on primary rays
- discussion of problems with ray differentials on other ray types, possible solutions and look at what other production renderers use
- solution using a distance to camera metric and presenting the results by comparing against other techniques

![](../../assets/bad59ca8e135fbc5.jpg)


- explains the plugin architecture that enables efficient implementation of high-level graphical features
- how to interact with the scene, culling, scheduling, and GPU execution

![](../../assets/5d094df9e58f03b7.png)


- SPIR-V shaders can only access global resources
- HLSL is very flexible with resource usage
- this post shows what usage pattern DXC is able to transform into legal SPIR-V and what patterns cannot be expressed in SPIR-V

![](../../assets/99112646cb9adcd9.png)


- walkthrough of the development of real-time GPU based water simulation
- discusses simulation experiments and algorithms used
- a brief look at the lighting of the water

![](../../assets/a7ac6b233959161a.png)


- post that provides links to talks with summaries about ray tracing on Nvidia RTX hardware
- difference between rasterization and ray tracing
- the structure of a real-time ray-tracing application and the components required
- how to extend the raster-based application with ray-tracing

![](../../assets/fc4a1a438d33ce79.png)


- overview of texture space shading
- technique decouples shading from rasterization rate
- Turing hardware provides support for computing derivatives in compute shaders and exposes texels that need to be shaded
- linked video explains the implementation of a texel space shading pipeline

![](../../assets/be3950771831a08d.png)


- look at how to adjust mip selection to favor noise over more detail at acute angels

![](../../assets/ed4965c239c9de80.png)


- visual and interactive explanation of quaternions and stereographic projection

![](../../assets/c21d27b34a2d1661.png)


- cone culling in task shaders
- two implementations, one using shared memory atomics and one with other subgroup operations

![](../../assets/763b9f34bc6a8822.png)


- collection of HLSL functions to use spherical harmonics
- Mathematica notebook to verify and visualize SH functions

![](../../assets/2cad0825fa48a1bc.jpg)


- all content from the SIGGRAPH 2018 course has been published


If you are enjoying the series and getting value from it, please consider supporting this blog.

[Support this blog](https://donorbox.org/jendrikillner)