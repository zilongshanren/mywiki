---
title: Graphics Programming weekly - Issue 348 - July 14th, 2024
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-348/
author: Jendrik Illner
published: '2024-07-14'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the blog post provides insights into the Vulkan variant for safety-critical applications
- shows the differences between stock Vulkan
- presents a detailed look at the architecture and how the variant is maintained

![](../../assets/d5aef7b20c9b258e.png)


- the paper discusses the implementation of a compute-shader-based rasterizer specialized for order-independent transparency
- explains the implementation and choices made
- presents performance comparison against other solutions
- additional explains the limitations of the current implementation

![](../../assets/531e8874e177d126.png)


- the blog post introduces the new AMD library that aims to improve GPU hang debugging
- allows developers to insert information into the command buffer
- in case of crashes, it allows to figure out which part of the frame has finished execution and what is still outstanding
- supports both Vulkan and D3D12

![](../../assets/70e13eb1b05cbae6.png)


- the blog post presents an overview of using Brixelizer for Ambient Occlusion and soft shadows
- shows performance number and discusses what aspects influence performance
- concludes with a summary of best-practices to consider when eveluating Brixelizer

![](../../assets/931f38705a9aeb51.png)


- the blog post introduces Arm Accuracy Super Resolution
- this upscaler is based upon AMD FSR 2.0 and optimized mobile GPUs
- shows performance numbers as well as quality comparison against other solutions

![](../../assets/4a5d7ecb84d550c3.png)


- the video provides a comparison to present the improvements done with FSR 3.1
- presents a comparison against other upscaling solutions

![](../../assets/bc1c2f2c9a427f75.png)

- the video tutorial presents how to combine multiple SDFs in shaders
- this information is used to implement a lava lamp effect
- implementation is shown using Unreal and Unity visual shading languages

![](../../assets/cd3d270567228e96.png)


- the video provides an overview of the concept of image barriers
- explains what kind of hardware-defined memory layout changes might be associated with image layouts
- presents how to implement the barriers in Vulkan required to solve the Vulkan validator messages for the swap chain presentation

![](../../assets/f50a007016e49fc8.png)


- the GDC presentation explains how the toon rendering effect was achieved
- the game uses a customized UE4 version, and the talk shows which stages need to be modified
- covers the lighting, cross-hatching, and halftone patterns, as well as how the outlines are applied

![](../../assets/88f576af1c1aa84b.png)


- the blog post announces the intent to open source DXIL shader validation as well as to support a mode to skip hash validation
- explains what hash validation is, what the current state is, and what issues arise because of it

![](../../assets/1d0c09206253e431.png)


- The survey paper presents a very detailed look at the state of font rendering
- discusses a high-level overview of font rendering systems, implementation, and limitations
- lists a long list of available solutions with brief summaries, as well as what solutions well-known software projects use
- showing performance tests of different solutions

![](../../assets/32bead996e10af5f.png)


- a new graphics programming-focused conference in Breda, Netherlands
- The call for speakers is still open till July 31st

![](../../assets/e2390562ba5d5d7e.png)

Thanks to [Leonardo Etcheverry](https://www.linkedin.com/in/leonardoetcheverry/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.