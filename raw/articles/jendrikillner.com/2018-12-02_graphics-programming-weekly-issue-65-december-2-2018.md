---
title: Graphics Programming weekly - Issue 65 — December 2, 2018
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-65/
author: Jendrik Illner
published: '2018-12-02'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- review of problems with classical APIs (OpenGL) and motivations for the creation of WebGPU
- presentation about Dawn, WebGPU implementation from Google
- splits into render passes that insert resource transitions between passes automatically
- how numerical fences are implemented (Monotonically increasing values indicate a timestamp in GPU execution history)
- considerations for implementations using cross-process communication

![](../../assets/c76d83c09e658867.png)


- part 2 of Vulkan raytracing series
- extends the application with multiple 3D meshes, texturing, simple shading, shadows, reflections, and ice shading model

![](../../assets/2390aa556a903b4b.png)


- development of a new rendering framework for transmittance for participating media that enables non-exponential media types to be represented
- archived by splitting transmittance into 4 transport functions
- discussion of how to express this new model so that it is intuitive to use and still creates physically correct results

![](../../assets/d325be8575712e53.png)


- walkthrough of the implementation of a rain material using the Unreal Engine 4 shader graph

![](../../assets/83a3d89cfa162a43.jpg)


- a short summary of what spherical harmonics are and what they are used for
- proposes a sanity check for SH projection code, by passing a function with a constant of 1, should result in a first coefficient close to 2√π

![](../../assets/b23d99a754ead7fe.png)


- article series about procedural routines for color generation
- talks about some techniques to generate procedural color variations
- explains HSB color space and the effect of changing each component
- convert from RYB hues to HSB hues
- generation of monochrome color schemes
- how the difference in colors influences human perception

![](../../assets/5b9b21e30b3b1991.jpeg)


- a sample that explains how to use Metal to generate render commands on the GPU
- implements GPU culling only to issue rendering commands for visible meshes and remove empty draws
- the final command buffer submission is controlled from the CPU

![](../../assets/1f9ca7bb2368a280.png)


- explains a new model for sampling visible normals of the GGX distribution
- summarizes the properties of GGX and how sampling a 2D projection of the truncated ellipsoid is equivalent to sampling the visible normals of the GGX distribution
- the method is more precise and quicker than previous methods
- provides a GLSL implementation

![](../../assets/4ef53c21bd698e8f.png)


- twitter thread that discusses what a BRDF is and how they are formed
- links to sources with more in-depth information

![](../../assets/f09ddebb43377bb3.jpg)


![](../../assets/eff8bfc8efb0f16b.jpg)


- the walkthrough explains how to use GLSL-reduce to simplify a GLSL shader and preserve certain conditions such as a crash or invalid output
- this is achieved with an interestingness test script
- the script expresses what is considered to be interesting, such as specific compiler crash, high memory usage, long compile time, etc
- presents the problem of bug slippage, this happens when a reduced shader generates a problem, but it’s not the same problem as in the original shader


- a tutorial explains how to implement ray traced shadows when using a signed distance field to represent the scene geometry using Unity

![](../../assets/e61adddf9701f4f9.png)


- interactive WebGL demo for the paper describing a technique to reduce firefly artifacts from path tracer outputs

![](../../assets/365190788f4314e4.png)


If you are enjoying the series and getting value from it, please consider supporting this blog.

[Support this blog](https://donorbox.org/jendrikillner)