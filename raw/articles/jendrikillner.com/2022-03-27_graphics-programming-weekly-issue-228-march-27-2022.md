---
title: Graphics Programming weekly - Issue 228 - March 27, 2022
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-228/
author: Jendrik Illner
published: '2022-03-27'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article provides an overview of a denoising solution for raytraced global illumination based on the findings of Metro: Exodus
- presents how to improve temporal accumulation through blue noise and geometry aware blurs
- it additionally sounds how the ambient occlusion term can be used for further improvement

![](../../assets/6b969fce8f89d1fd.png)


- the article discusses a method for a simple non-PBR method to implement underwater caustics
- implementation uses a projection volume for multiple tiling textures
- code examples are provided using Unity

![](../../assets/02208e841c5ca87b.png)


- the article presents a walkthrough of the implementation of a complete skybox model, including time of day, moon, sun, and stars
- it additionally shows how to integrate support for lunar and solar eclipses
- the implementation of the sky colors is implemented as a function of the sun position to sample multiple gradients

![](../../assets/19b7ac19e05e1d95.png)


- the article describes a large number of changes and improvements made to the AMD and Vulkan Memory allocator
- the changes include new allocation algorithms, improved statics, support for custom pools as well as support for defragmentation
- additionally, the allocator can now be used when sub-allocating from a single large buffers resource

![](../../assets/4961d5cae7b911db.jpg)


- a collection of slides and videos from AMDs talk at GDC 2020
- covering raytracing, FidelityFX Super Resolution 2.0, game rendering effects as well as CPU optimization advice

![](../../assets/dfba9c213c773f9e.jpg)


- Vulkan loader has been improved with more debugging capabilities and improved documentation
- additionally improved the testing framework to ensure more consistent behavior across layers

![](../../assets/07548c9c2d995325.jpg)


- podcast discussing the development and design of WebGPU
- talks about the restrictions, design goals, and how it fits into the broader graphics ecosystem

![](../../assets/3d14960193c5978b.png)


- the page contains links to the presentations (slides and video) to the talks given by Intel at GDC 2022
- covering upscaling, optimizations, VRS, machine learning as well as optimization advice

![](../../assets/2c5cc2f78d81be89.png)


- the article provides in-depth details about the new Hopper GPU architecture for data center usage
- shows performance numbers, new capabilities, improvements as well as new

![](../../assets/ff82555701c69d27.png)


- the video presents an overview of techniques to represent more geometric details without having to use high geometric tessellation levels
- explains the differences between the different techniques, how they are related explaining strengths and weakness

![](../../assets/40bc153214e16937.png)


- the blog explains the graphics foundations of Mach, a zig graphics foundation layer
- provides an overview of the unified API abstractions that use WebGPU and WGSL internally

![](../../assets/359ac9649e0dfe7d.png)


- the paper presents a derivation of a representation for rotation and non-uniform scaling in a compact representation
- HLSL code for the implementation is provided
- contains a performance comparison against quaternions and matrix operations on RDNA2 hardware instruction costs

![](../../assets/81507ff1946a42a8.png)

Thanks to Dirk Dörr for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.