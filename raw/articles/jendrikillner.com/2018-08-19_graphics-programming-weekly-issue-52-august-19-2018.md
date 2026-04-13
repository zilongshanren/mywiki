---
title: Graphics Programming weekly - Issue 52 — August 19, 2018
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-52/
author: Jendrik Illner
published: '2018-08-19'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- slides for the layered real-time shading model discussed in
[issue 38](https://www.jendrikillner.com/post/graphics-programming-weekly-issue-38/) - using a statistical analysis of light transport in layered structures
- a visual explanation of the statistical analysis framework
- presentation of results, comparison against stochastic references and discussion of limitations of the technique

![](../../assets/3572f0da7c5bb5d8.png)


- slides for the technique discussed in
[issue 45](https://www.jendrikillner.com/post/graphics-programming-weekly-issue-45/) - explanation of problems with linear blending
- how contrast-preserving blending is able to mitigate some of these problems
- presents a histogram-preserving blending algorithm that has many use cases besides the introduced procedural texturing technique
- whenever you blend
- weighted data: use premultiplied blending
- data chosen randomly: use histogram-preserving blending


![](../../assets/429daa78f42ff339.png)


- video discussing a fully automated UV unwrapping tool
- explains all steps of the pipeline that tries to find the best projection technique for local parts of the model
- tool available for licensing

![](../../assets/c2d11995d9149ac5.png)

- added pixel history view for D3D12 and added support for support for Vulkan ray trace extension
- new GPU trace activity view visualizes the GPU utilization in more detail
- provides a breakdown of wrap level activity, connected to events and performance markers

![](../../assets/6dc1620561659e3e.jpg)


![](../../assets/4807ac9110f9a16d.png)


- comparison of 3 techniques to generate blue noise
- visual quality comparison of three methods to generate blue noise
- the void and cluster technique produces the best results in the test

![](../../assets/f7e35d94dc9b9998.png)


- integration of spherical harmonics over spherical polygons
- using a closed form expression with linear cost
- shows applications for area lights and approximating shadows from area lights

![](../../assets/e1f94438f947a733.png)


- Nvidia open sourced the MDL SDK (Material Definition Language)
- set of tools that allow materials to be shared between different renderers
- can generate texturing functions for multiple backends; however the GLSL backend is NOT part of the open source release

![](../../assets/9edd98be3b07145f.jpg)


slides and [video](https://youtu.be/Q1cuuepVNoY?t=310) for the “Introduction to DirectX RayTracing” track from Siggraph 2018 have been released

![](../../assets/9fba2055e950da9b.png)


- the pdf version of the Ray Tracing Minibooks series has been released for free

![](../../assets/5497e8dd7a5dc73b.png)

- new GPU architecture from Nvidia
- dedicated ray tracing hardware
- volta cores have int8 and int4 support
- support for variable rate shading

![](../../assets/9d362948b6ca1c1c.jpg)


- list of author’s favorite papers with a brief summary of the content

![](../../assets/5a4418ab02acd7bd.png)


- slides for the Siggraph course about the fundamentals of color science and color management for games and film

![](../../assets/71f65b8dcf615cf3.jpg)


- slides for the Siggraph course
- provides an overview of all API interfaces required to render 3D meshes

![](../../assets/5c1d4359e931cca9.png)


- fully vulkan 1.1 compatible
- support for VK_EXT_conditional_rendering, VK_KHR_8bit_storage

![](../../assets/5c1d4359e931cca9.png)

If you are enjoying the series and getting value from it, please consider supporting this blog.

[Support this blog](https://donorbox.org/jendrikillner)