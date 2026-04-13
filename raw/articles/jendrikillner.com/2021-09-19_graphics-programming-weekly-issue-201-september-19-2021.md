---
title: Graphics Programming weekly - Issue 201 - September 19, 2021
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-201/
author: Jendrik Illner
published: '2021-09-19'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the video presents what is new with the A15 GPU
- added support for lossy compression
- in addition to bandwidth, it also saves 50% memory usage (quality will be dropped to fit)
- improved sparse texture support with support for depth/stencil
- as well as support for SIMD shuffle operations

![](../../assets/4657bd8668357de2.png)


- the article presents a comparison of triangle throughput for indexed buffer rendering, mesh shader usage, MultiDrawIndirect, and custom compute shader rasterization
- comparison is made for depth-only rendering
- results are presented on Nvidia, AMD, Intel, Qualcomm, and Apple GPU

![](../../assets/0157ef6b5819cfc1.jpg)


- the whitepaper explains how to use DevSim to simulate lower spec devices on higher-end devices
- the Vulkan device simulation layer will adjust the return values of capabilities queries
- the paper shows how to use the tool, how it fits into the architecture, and what settings can be adjusted

![](../../assets/dfd6fe108bf26282.jpg)


- the frame breakdown covers the flight simulator scenes
- presents how the gbuffer by a texture array with MSAA enabled
- how reflections, environment maps, and shadows are drawn
- covers how transparent elements in the cockpit are drawn
- additionally contains a brief look at post-processing and volumetric clouds

![](../../assets/be79dc7d6bd339f9.png)


- the article discusses lessons learned by ARM’s approach for developing raytracing support for Mali GPUs
- implemented as software implementation that can be loaded as Vulkan layer
- presents best practices for mobile performance and battery usage

![](../../assets/a805306ac46dc60d.png)


- the video shows the smoothstep node in UE5 and Unity3D
- covering the math, and examples of how it is used

![](../../assets/51a33d6bc1fbe232.png)

- video in-depth interview with VP of developer ecosystems at Nvidia
- discussing Khronos technologies such as Vulkan, upcoming standards
- as well as how gaming graphics might be developing with new techniques and hardware capabilities

![](../../assets/07348a98e5b17cfa.png)


- the in-depth article shows how to implement a custom physically based lens flare effect as post-process
- presents what lens flares are, how they are used in games and movies
- finally shows how to implement them into the UE4 pipeline and replace the build-in effect

![](../../assets/b086c9800f5b91fb.jpg)


- the paper presents how to extend spatiotemporal reservoir resampling to multi-dimensional path space such as volumetric media
- combines cheap approximations for transmittance with unbiased methods for per-pixel evaluations

![](../../assets/4a12175366beb8e0.png)


- the author suggests a method D3D12 state transition system for multithreaded command recording
- based around per-resource tokens that use CPU side fences to synchronize access to previous state transitions

![](../../assets/c41622cd8d0b16bb.png)

Thanks to [Max R.R. Collada](https://twitter.com/maxandonuts) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.