---
title: Graphics Programming weekly - Issue 315 - November 26th, 2023
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-315/
author: Jendrik Illner
published: '2023-11-26'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article discusses a system to compute shader rasterize large point cloud datasets at interactive rates
- the detailed blog presents how they solved problems along the whole pipeline
- covering point reordering, point rejection and hole filling, level of detail selection and calculation, as well as memory usage optimizations
- additionally presents how the data is expressed and used from the Unity implementation

![](../../assets/2bc8c73c9840c6d4.png)


- the article gives some advice on how to get started with graphics programming
- discusses the complexity of different graphics APIs
- additionally provides a list of tutorials/blogs and courses that provide a good starting point

![](../../assets/bd9abf91085506e4.png)


- a start of a collection of books and resources for (graphics) engine programmers that I recommend
- covering mathematics, engine architecture, graphics programming, collision detection, software design, as well as knowledge organization

![](../../assets/4c9bf9013d03dc49.jpg)


- the article presents Phi and the Golden Angle
- shows how to use these numbers for a point distribution in a rectangle as well as a disk
- provides a shader toy example to present the effect when using blur kernels

![](../../assets/a538f073123fdf5d.png)


Studio Elevation are re-establishing the boundaries of VR. We’re looking for a talented Principal Graphics Programmer to help us explore, create, and deliver world-leading innovation in software and VR hardware. Become a key member of Elevation, pioneering AAA, remote first process and crafting a new generation of VR development to bring core VR games to fruition.

![](../../assets/dce70758dae65d6c.png)


- the article provides a visual explanation of what an optimal transport problem is
- presents how the problem can be solved a lot simpler in 1D
- extends on this insight to present how a multi-dimensional problem can be sliced and approximated in multiple 1D steps

![](../../assets/0eb495ef274f5c36.png)


- the article describes the concept of render-bundles and how they can be used to reduce CPU overhead
- presents what changes are backed into the bundle and how updating referenced resources enables flexibility beyond static scenes
- code examples and internals are discussed in WebGPU terms but apply to other APIs as well

![](../../assets/e9b191d1effd8cf3.png)


- The author updated his library for spherical harmonics and zonal harmonics
- added GLSL shader variation and shader toy
- additionally, the update fixed several bugs and made improvements

![](../../assets/982b3248599dcaa0.jpg)


- the article presents a look into the internals of the gfx-rs wgpu implementation
- demonstrates the limitations of the implementation in terms of multithreaded uses
- shows what changes were made to reduce lock-contention and how the implementation might change in the future further

![](../../assets/949accfd3c5d7cfa.png)


- short blog post lists a couple of tricks to use when writing shaders for higher performance
- additionally provides a small trick on how to reuse data between iterations when using shaderToy

![](../../assets/f9f4341ffe86133e.png)


- the blog post shows how to use Nvidia-specific intrinsics with D3D11 and D3D12
- how to use them from shaders and how to verify that the hardware supports it

![](../../assets/94ff0e4aaf0411ea.jpg)

Thanks to [Denis Gladkiy](https://play.google.com/store/apps/developer?id=Piggybank+Software) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.