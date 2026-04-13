---
title: Graphics Programming weekly - Issue 57 — October 7, 2018
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-57/
author: Jendrik Illner
published: '2018-10-07'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- Vulkan stream - part 3
- fixing validation layer errors, explanation of pipeline barriers
- implementation of swap chain resize
- shader compiler integration with Visual Studio

![](../../assets/dbd5593facbf27cb.png)

- Vulkan stream - part 4
- overview and integration of Vulkan extension loader
- loading an .obj and rendering a mesh using classical vertex pipeline and manual vertex pulling

![](../../assets/f992b650c02080c6.png)

- explanation of shader for diamond rendering in a forward rendering architecture
- uses a precalculated cubemap from the inside of the object to simulate internal bounces

![](../../assets/b48e20701c5a75b5.png)


- discussing many aspects of making a fractal-based game
- including cone tracing, lighting, shadows, ambient occlusion, volumetric lighting, and atmospheric effects

![](../../assets/4f116ac902c88ee7.png)


- presents the steps required to vectorize the Ray-AABB approach by
[Andrew Kensler](http://psgraphics.blogspot.com/2016/02/new-simple-ray-box-test-from-andrew.html) - results are very similar to the recent
[jcgt paper](http://jcgt.org/published/0007/03/04/)

![](../../assets/cf4f27ce5cf2d489.jpeg)


- derivation of the progressive spherical Gaussian encoding technique discussed in last week’s issue

![](../../assets/40fcc43381c3f560.png)


- explores changes to CUDA path tracer with Rust, what improved since the last post and what problems persists

- command line tool that allows cross compilation from GLSL to HLSL, GLES and MSL (Metal)
- implemented using a combination of Glslang and SPIRV-cross

- work in progress post comparing API concepts between D3D12, Vulkan, Metal, and OpenGL

![](../../assets/b66c803390514469.png)

- Windows raytracing support is available starting with Windows 10 October 2018 update

![](../../assets/9938e30da1d77dfa.png)


- breakdown of “Real-Time Ray Tracing for Interactive Global Illumination Workflows in Frostbite” into short sections
- key takeaways for each section is provided in the post

![](../../assets/6cc76c985a452a61.png)


- explains how to parse a shader file for includes using regex (implemented using Rust)

- visualization of floating point precision when a classical OpenGL projection matrix is used

![](../../assets/5c2c48789844d79d.png)


- explanation of Unity shader graph nodes
- walkthrough of example shaders that allow the creation of a small island scene

![](../../assets/b6a244c1cf7b1819.png)


- new PIX features are available with Windows 10 October 2018
- can capture D3D11 applications using Direct3D 11 on 12 translation layer and WinML workloads

![](../../assets/be123ca2af51fdd5.png)



If you are enjoying the series and getting value from it, please consider supporting this blog.

[Support this blog](https://donorbox.org/jendrikillner)