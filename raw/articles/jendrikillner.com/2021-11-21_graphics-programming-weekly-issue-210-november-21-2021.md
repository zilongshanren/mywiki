---
title: Graphics Programming weekly - Issue 210 - November 21, 2021
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-210/
author: Jendrik Illner
published: '2021-11-21'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article presents an overview of the implementation for various techniques found to mix raytracing and rasterization
- discussed the implementation of Spatiotemporal Variance-Guided Filtering for Denoising
- show how to apply this for Soft Shadows, Ambient Occlusion, Reflections, Indirect Lighting as well as a probe-based Global Illumination
- presents optimization and quality improvement steps

![](../../assets/72294cd29416b52e.jpg)


- the article presents the quickest way to implement fully bindless shaders using Vulkan
- shows how to implement the whole process from querying support, descriptor management as well as the shader side

![](../../assets/7769f6a5e56b5d92.png)


- the article shows how Pixel Local Storage can be used on ARM GPUs to implement Translucency and Order Independent Transparency
- additionally presents the Shader Frame Buffer Fetch to allow access to the render target color and depth stencil from within an active pixel shaders

![](../../assets/4409879b3ab8ab83.png)


- the article presents the official C++ interface for Metal
- shows how to integrate it into an application
- additionally offers how to generate a single header version

![](../../assets/f0354721f72ee7a4.png)


- the article describes the RenderDoc fork for use with Oculus devices
- presents what effects on performance the tool has
- shows how to visualize tile usage and collect performance counters for application optimizations

![](../../assets/fd2d02e3771068fe.png)


- the author presents his experience trying to run a prefix sum sorting algorithms portably using WebGPU
- discusses the limitations and issues encountered
- explains what synchronization primitives are missing to allow the most efficient variation using WebGPU

![](../../assets/251308f0d69a07a0.png)


- update on Nvidia scaling solutions
- the NVIDIA Image Scaling SDK now provides an open-source spatial upscaler
- can be used on hardware where Nvidia DLSS is not available
- presents the Image Comparison & Analysis Tool that allows comparison of up to 4 images and videos

![](../../assets/d7d24719affea0fe.jpg)


- the article shows an example of implementing a flood filling algorithm using the BGFX abstraction library
- provides a brief discussion of issues encountered in getting started with the library

![](../../assets/c181642e1ab53084.png)


- the article presents how to implement GPU particles with movement tails without CPU interaction
- all particle simulations happen in pixel shaders, and results are copied into ring buffers expressed as rows of textures
- implementation is provided using WebGL (regl)

![](../../assets/5ccfc05bcd9b4f13.png)


- the article presents how to render rectangles with rounded edges
- shows the distance field based shader implementation using Metal
- additionally covers anti-aliasing and gradient rendering

![](../../assets/e0e13de5f3f8889c.png)


- the Vulkan SDK has been repackaged and now separates between core and optional components

![](../../assets/382563bcc478e3e5.png)

Thanks to [Manish Mathai](https://github.com/goodbadwolf/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.