---
title: Graphics Programming weekly - Issue 226 - March 13, 2022
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-226/
author: Jendrik Illner
published: '2022-03-13'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article present how to derive a downsampling filter that uses eight bilinear samples
- shows the process how to create the desired response and optimize the weights
- includes a shadertoy implementation

![](../../assets/342f04359835cb85.png)


- the article presents an overview of sRGB, Linear, and Oklab gradient interpolation
- shows how to optimize the linear and Oklab calculations to get a lot closer in terms of performance compared to direct sRGB interpolation

![](../../assets/ca6aa187b43426f9.png)


- the article discusses the authors’ decision for a home renderer abstraction layer
- focusing on ease-of-use for experimentation over performance

![](../../assets/03227bf4a775684f.png)


- the article presents the implementation of a bindless binding model using D3D12 and Vulkan
- discusses the decisions, trade-offset as well (API) implementation-specific details
- code examples are provided in Rust

![](../../assets/8b71ab1f1d440bc9.png)


- the article presents a compiler approach that takes an SDF representation and generates shaders for cheaper execution on parts of the mesh
- lists several recommendations to consider when implementing
- additionally provides a few use cases for the SDF Evaluator

![](../../assets/5e82f3d0981f8f25.png)


- the paper extends the ideas of Stochastic Light Culling to compute single scattering in a homogeneous media
- presents how combining reservoir sampling with the introduced technique can improve performance

![](../../assets/21fb150c87b5766c.png)


- the paper introduces a technique to lower the cost of ray tracing by using approximated geometry for shadow rays
- additionally proposes a stochastic material sampling for material blending
- presents how to combine the techniques in a path-tracer implementation

![](../../assets/2beed47524b1ed55.png)


- the article presents hardware and shader compiler improvements for the new Malig G710 GPU
- provides details into how the improvements compared to previous generations
- additionally provides updated best-practices for best performance

![](../../assets/011784374d423d8f.png)


- the forum post presents the proposal to integrate HLSL and DXIL support into clang/LLVM
- discussion presents insights into the tradeoffs in the compiler backend and difficulty with GPU architectures

![](../../assets/5ec2114651516352.jpg)


- the article provides an introduction to WebGPU for compute shader workloads
- starts from the basics and walks through all steps required to implement a simple 2D ball physics simulation
- shows how to upload readback data from the GPU

![](../../assets/c145d1743ff0a4f6.png)


- the page contains information and links to all the talks that AMD will present at GDC22
- lists what new tools and libraries are going to be announced
- number of talks will be freely accessible on GPUOpen

![](../../assets/ba3b863115511f4a.jpg)

Thanks to [Robert Wallis](https://github.com/robert-wallis) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.