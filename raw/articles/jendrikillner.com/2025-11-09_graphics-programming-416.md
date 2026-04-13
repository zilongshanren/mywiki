---
title: Graphics Programming 416
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-416/
author: Jendrik Illner
published: '2025-11-09'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- major release adding threaded shader debugging support for D3D11, D3D12, and Vulkan
- correctly simulates wave/subgroup operations, group-shared memory, and whole-workgroup interactions
- includes numerous bugfixes for pixel history, descriptor buffers, and multi-GPU scenarios

![](../../assets/57831dd4c8eaab94.png)


- presents a multi-agent workflow for automatic CUDA kernel generation and optimization
- uses LLM agents to iteratively generate, correct, and optimize kernels while integrating Nsight Compute metrics

![](../../assets/6a1d83552e0ee89b.png)


- introduces spectral rendering for more accurate color reproduction
- explains how to obtain illuminant spectra from databases and convert RGB textures to reflectance spectra using Fourier sRGB
- presents the mathematical foundations of spectral upsampling that enable working with existing assets

![](../../assets/09d1623f77b82e7e.png)


- technical post-mortem of graphics techniques used in the “This is Us” demo presented at Revision 2025
- describes real-time path tracing implementation using radiance caching with spatial hashing and ReSTIR GI
- presents SPH fluid simulation using tiled approach with LDS pre-fetching and marching cubes meshing

![](../../assets/447b05692e2c13f1.jpg)


- compares inline and pipeline ray tracing approaches with detailed explanations
- benchmarks both methods on AMD, NVIDIA, and Intel Arc
- shows AMD achieves significantly better performance with pipeline ray tracing, while NVIDIA and Intel perform similarly with both approaches

![](../../assets/824501df3f38b44b.png)


- investigates how animation affects the visibility of LOD transitions in 3D models
- finds that animated models can switch LODs much closer to the camera compared to static models
- demonstrates that animation effectively masks geometry changes, potentially eliminating the need for cross-fade transitions

![](../../assets/37173153e6f375fa.png)


- Registration for the Shading Languages Symposium 2026 is open
- The program has been published and features keynotes and sessions covering Slang, SPIR-V, HLSL, GLSL, WGSL, Gigi, WESL, and more
- aimed at attending work on shader languages, compilers, tools, or rendering pipelines

![](../../assets/ac03d8d1b159f88f.jpg)


- The video discusses additional shader hints that the author would like to see expressed in shader code
- explains the reasoning and advantages of the various requests
- demonstrates suggested shader code syntax

![](../../assets/028d0e863c2f7976.png)

- third episode in a series on terrain shader development
- explains how to extend a single-layer material into a 4-layer blend setup
- presents a height-based blending approach between layers

![](../../assets/ea97b15f6f3c4658.png)


- explains how to use vertex shaders to animate a simple wave
- shows that vertex density affects the quality of the effect
- provides a detailed walkthrough on how to set up the mesh tessellation pipeline using Unity

![](../../assets/e5b7ba5fa81a239c.png)


- announces open source release of Tellusim Core SDK for cross-platform graphics and compute development
- provides unified C++ API with bindings for C#, Rust, Swift, Python, Java, and JavaScript
- includes comprehensive examples covering meshlets, ray tracing, UI, and more

![](../../assets/8b3912670898e120.png)

Thanks to [Eric Haines](http://erichaines.com/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.