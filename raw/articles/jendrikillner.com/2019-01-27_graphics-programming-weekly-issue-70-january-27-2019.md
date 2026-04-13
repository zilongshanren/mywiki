---
title: Graphics Programming weekly - Issue 70 — January 27, 2019
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-70/
author: Jendrik Illner
published: '2019-01-27'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

Thanks for everyone who filled out the survey. I closed the survey. I am analyzing the results and will post them later this week.

- D3D12 adds support for DRED (device removed extended data) in the latest windows insider preview build
- writes an auto-incrementing counter after each render-operation into memory that is persistent across device removed events
- this allows the GPU progress to be inspected during post-mortem analysis
- the overhead is around 2 to 5 % for a frame of a AAA game, therefore defaults to off and needs to be enabled explicitly
- additionally allows better tracking of page faults
- tries to detect access to recently deleted objects
- shows the API to enable and how to use it to enable and inspect provided data

![](../../assets/d3dd2d7945d210ef.jpg)


- extension to real-time image based lighting models
- adding support for multi-scattering shading using the precomputed integrals from single scattering models
- accomplishes energy conversation
- the paper derives the GGX approximation for 3 classes of objects (perfect reflectors, generic metals, and dielectrics)
- presents comparisons against single scattering models in a furnace test

![](../../assets/2ef4a9fb6e7b4a39.png)


- explains the PBR shading model
- a combination of 3 BSDFs that allow expressing a large number of materials
- including the derived formulas and illustrates the exposed parameters
- user guide describes how to use the system and provides examples of the different effects that can be achieved

![](../../assets/f51eb49fb8461e50.png)


- shader workshop that uses Shadertoy to teach raymarching techniques
- the workshop starts with basic 2D shape marching
- in the end explains how to define 3D scenes with support for lighting, gamma correction, shadows and materials with tri-planar texture mapping

![](../../assets/66bbf3cf76c75cc6.png)


- latest Vulkan SDK version (1.1.97.0) adds GPU assisted validation
- validates at runtime that shaders are not accessing any descriptors out of bounds
- this is achieved by adding instrumentation into the SPIR-V
- the document explains the constraints of the layer, known issues and an overview of the implementation details

![](../../assets/30e952a7a3da3e4b.png)


- the article discusses his favorite chapters and insights when looking back at the original “An Introduction to Ray Tracing” (book is now free) from today’s perspective
- mentions which chapter are still relevant today and which information has not aged as well

![](../../assets/4a033ee3e88f87ff.jpg)


- list of common problems encountered when using Shadertoy and how to solve them
- texel center issue, loading texture data, resolution changes, mipmap discontinuities

![](../../assets/57468bc0227a3451.png)


- list of sessions by Khronos and related talks that will be taking place during GDC this year

![](../../assets/c10b88ccf8448b98.jpg)