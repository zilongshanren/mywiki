---
title: Graphics Programming weekly - Issue 120 — February 23, 2020
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-120/
author: Jendrik Illner
published: '2020-02-23'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- a 3 part series that provides an overview of the backend implementations of sokol_gfx for the OpenGL, D3D11 and Metal implementation

![](../../assets/a8c77f13eb8faa38.png)


- Nvidia added support to the DirectX Shader Compiler (DXR) to generate SPIR-V that is valid to be used with the Vulkan SPV_NV_ray_tracing extension
- the article shows an example and explains how concepts are mapped to SPIR-V

![](../../assets/249aef8391924b8d.png)


- the article presents an overview of techniques to optimize pixel shaders
- starting with techniques to make sure that pixel shaders are only run if necessary and offers several methods to reduce the cost of pixel shaders afterward

![](../../assets/2591439fd91c8a75.png)


- the author presents how shooting stars in the Witcher 3 are implemented
- show the vertex and pixel shader implementation

![](../../assets/549a6d3892a4ed38.png)


- the in-depth article presents the physical models and approximations of participating media (such as fog, water)
- presents constant, linear and exponential fog implementations
- extends these solutions to express atmospheres and provides approximations for numerical approaches

![](../../assets/8972a1339a70dfed.png)


- the newest part in article series about defining a data-driven rendering pipeline
- focusing on the definition of a render pipeline
- a simplified version of a RenderGraph/FrameGraph system
- build around render targets as central primitive

![](../../assets/ef16f3b354f68e20.png)


- the Unity tutorial explains how to implement a stylized Eyeball Shader using Unity Shader Graph

![](../../assets/e755cb735d06de39.png)


- presents an approach to render particle effects using compute shaders
- the primary focus is optimization for tiny, pixel-sized particles that are additively blended
- lacking support of atomic on floats requires float->int->float conversions in the shader and how this influences the final implementation

![](../../assets/560882213ee5d4c5.jpg)


- the results from the Vulkan survey have been released
- contains comments, and what are the next steps that are taken to address the feedback

![](../../assets/8846969b920e98c3.png)


- the article presents how to implement a Path Tracer using the Unity Data-Oriented Technology Stack (DOTS)

![](../../assets/d53414723d5371dd.png)


- the article describes how to deal with device orientation changes in a Vulkan application efficiently
- describes how to query the information from the system, recreate Vulkan objects and necessary modifications to shader code

![](../../assets/de02e1a62882ba44.png)

Thanks to [Cort Stratton](https://twitter.com/postgoodism) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.