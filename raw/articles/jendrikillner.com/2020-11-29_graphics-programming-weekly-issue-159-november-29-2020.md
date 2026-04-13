---
title: Graphics Programming weekly - Issue 159 — November 29, 2020
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-159/
author: Jendrik Illner
published: '2020-11-29'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

Daniel Jones has made a video summary of the articles included in this article available on [Youtube](https://www.youtube.com/watch?v=EwN7yVcXJe8)

- the video presents an in-depth walkthrough that shows how to use signed distance fields (SDF) to create an animated girl
- explains all used primitives as SDW, how they are combined, and the lighting implementation
- implementation is done in shadertoy

![](../../assets/1ed12429f75ce2e4.png)

- the article shows how The Witcher 3 implements a fullscreen effect that gives the world a painterly look
- presents a step-by-step walkthrough, showing all components that define the noise generation
- author provides a
[shadertoy](https://www.shadertoy.com/view/3stBD2)implementation of the effect

![](../../assets/f9089cf3bb24807d.jpg)


- the post presents a bi-planar mapping as an alternative to tri-planar mapping using only two texture fetches
- starts by giving an overview of the tri-planar mapping
- followed by an explanation of the bi-planar mapping technique, presenting strategies to improve the quality and how the quality compares

![](../../assets/01e621419c51f09d.jpg)


- a very detailed article about depth buffers
- focusing on Unity, but most of the information is engine agnostic
- explains the different spaces, storage formats, and precision considerations
- additionally shows how to calculate world space positions from the depth buffer

![](../../assets/08cbfc98d5f0117b.png)

- A Unity video tutorial that explains how to generate grass meshes using Compute shaders
- covers the setup, mesh generation, and LOD selection

![](../../assets/92fb7889457c0240.png)

- the article shows how Multiple Importance Sampling in 1D is used to improve the convergence of stochastic algorithms
- presents multiple experiments and shows how different techniques can reduce the sampling error

![](../../assets/da0a977113d224e9.png)


- a collection of resources (books, talks, websites) the author recommends for beginners to get started with graphics programming

![](../../assets/68bd1b81b8703d15.png)


- the presentation provides an overview of Variable Rate Shading (VRS), the different features levels
- provides insights into VRS performance, features that disable VRS, and what bottlenecks will cause VRS to not offer performance improvements
- additionally shows how to integrate the AMD helper library to generate the VRS screenspace map

![](../../assets/85f8ab4dc64bc642.png)


- the presentation explains the ray tracing denoising technique developed by AMD
- shows what inputs are used, how the algorithm uses these to decide ray count, and how to use temporal reprojection to further reduce sample counts
- the code for the technique is provided, and the
[website](https://gpuopen.com/fidelityfx-denoiser/)includes comparison pictures and images of the intermediate results

![](../../assets/0d5860818792d6d4.png)


- the post explains what changes have been made to the Vulkan raytracing extension since the preview specification
- extension has been split into 3 layers (acceleration structure, raytracing shaders states, and ray queries)
- walkthrough of each stage of the extensions
- in contrast to DXR, Vulkan offers the ability to generate acceleration structures on the CPU

![](../../assets/c23c0dd7261a3dc7.png)


- the article presents an overview of how Vulkan raytracing has been implemented into Wolfenstein
- provides a brief overview of the different API concepts and how they are used

![](../../assets/cfb55243ca42f84e.png)


- the article contains an overview of the new features that will be included in shader model 6.6
- 64-bit Integer Atomic Operations, Dynamic Resource Binding, Compute Shader Derivatives and Samples, Packed 8-Bit Operations and variable Wave Size

![](../../assets/ac522ed0eaa77713.jpg)

Thanks to [atyuwen](http://atyuwen.github.io/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.