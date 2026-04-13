---
title: Graphics Programming weekly - Issue 128 — April 19, 2020
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-128/
author: Jendrik Illner
published: '2020-04-19'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- provides an introducing into linear blending
- explaining that pixels are no signal but rather samples taken at a given location
- presents the star-shaped artifact of bilinear filtering
- discusses an alternative to bilinear filtering with links to papers and analyzes the frequency response of some filters

![](../../assets/a63fe50d3dfacaea.png)


- the article presents how to use the Mitsuba renderer to validate the results from a PBR renderer
- provides an overview of the file structure used by Mitsuba and how to convert units where required

![](../../assets/87e3225f98b449e4.png)


- the article presents that Godot has now 3 update frequencies for shader parameters global, per-material and instance
- provides a few video examples that show use cases of global parameters for vegetation interactions

![](../../assets/6a1fff6c5c65e6c2.png)


- collection of papers from the I3D 2020 conference

![](../../assets/94aa50c8284018a1.png)

- part 5 of Nvidia ray tracing series
- focuses on the presentation of different visual effects that are created through ray tracing
- such as depth of field, motion blur, atmospheric effects

![](../../assets/91d77ee2b7ac1ee5.png)


- Eric Haines will be giving a webinar on May 12
- explains concepts related to ray tracing, comparison of ray tracing and explain how specialized hardware can accelerate the workload
- additionally covering denoising and other techniques required to make interactive raytracing possible

![](../../assets/232c8fc6d513a712.png)


- part 3 of Rust gfx-hal intro series
- shows all the steps required including binary serialization of mesh data, shader changes and all other Rust changes needed to render a spinning 3D teapot

![](../../assets/c40b1c9d88d64e81.png)


- presentation from revision
- focuses on the physics of light interaction with matters
- overview of shading models and possible implementation techniques

![](../../assets/7ab8c0d6b917d947.png)


- Cuda introduces new memory management functionality
- allows developers to reserve virtual memory ranges and map these ranges to physical memory on demand

![](../../assets/612c75a41a544fb6.png)


- the article shows that the D3D12 alignment requirement rules have an exception for small textures that allows a reduction in alignment requirements
- this behavior needs to be explicitly requested and presents how to take advantage of it

![](../../assets/0aee8d61a660e9c0.png)


- the article presents 3 different techniques for Unity that allow the color of UI elements to be dynamically adjusted
- shows pro and cons for each technique and what good use cases are

![](../../assets/cc7cf60f142f6ac5.png)


- talks aimed at computer science students starting to get started with GPU technology
- present an overview of GPU hardware architecture
- how functional programming is a good fit for GPUs
- shows how to adjust 2D rendering algorithms to be better adapted for the architecture
- overview of the graphics infrastructure (compilers, APIs, shader languages )

![](../../assets/6de53b796f10e8ea.png)


- the article and video and present a high-level overview of the rendering passes of Overwatch

![](../../assets/41517b3af18c8eaf.jpg)

![](../../assets/e656f3c998298b16.png)

Thanks to [Deepak Surti](https://www.deepaksurti.com) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.