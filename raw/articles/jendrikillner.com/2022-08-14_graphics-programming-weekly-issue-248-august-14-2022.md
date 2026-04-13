---
title: Graphics Programming weekly - Issue 248 - August 14, 2022
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-248/
author: Jendrik Illner
published: '2022-08-14'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- Nvidia open-sources MDL distiller and the GLSL backend
- MDL distiller is a system for automated shader simplifications
- the GLSL backend enables the usage of MDL for Vulkan applications

![](../../assets/ed74f20fbe341cb2.png)


- A database of physically based values for CG artists (materials, Light Sources, Cameras)
- contains material information of familiar materials in a unified interface
- materialX, unity, and unreal shader graphs are available for the different materials

![](../../assets/2c3dac8f5bebc982.jpg)


- new PIX release allows profiling to target different GPU clock rates (controlled by the hardware manufacturer)
- added the ability to export metrics to CSV
- additionally, added support trimming of captures

![](../../assets/b2ce3de63134d536.png)


- the post explains how to set up budgets for pix metrics
- can be defined for the user or system metrics

![](../../assets/b2204dc0c4677be6.png)


- the article explains the theory of a Gaussian blur algorithm
- shows how the filter is defined, sample weights calculated
- it additionally presents how to implement the technique using a Unity Pixel Shader

![](../../assets/2202339023411d49.png)


- the article presents a description of the texture/buffer/sampler binding model supported by different hardware manufacturers
- discusses how Vulkan and D3D12 models map onto the hardware
- additionally discusses problems arising from the differences

![](../../assets/cbe8512cf41c8f39.png)


- the presentation provides a brief overview of the implementation details for the Nvidia path tracer and the level of optimizations required to archive the performance
- presents open problems in data authoring, scene description, and material complexity
- shows ideas on how techniques can be developed together to deliver improved results

![](../../assets/0efdb7e7eacb5b6f.png)


- a growing collection of content from SIGGRAPH 2022
- presentations, slides, videos, and posters

![](../../assets/e27720451ad0c205.png)


- discusses the limitations of linear perspective and how classical artists rarely used it
- present non-linear projection techniques and how they can be used
- starts a discussion on how to computationally model and apply these methods

![](../../assets/ac03d3ce391357f7.jpeg)


- the article presents a technique to generate explosion decals aimed at a 3D topdown game
- based around forward shading, a projected 3D sphere with procedural noise

![](../../assets/596af515b5af4ec3.jpg)


- video tutorial shows how to implement a bloom effect using Unreal and Unity shader graphs
- starts by showing visually how the effect works using photoshop before implementing the code
- followed by presenting a walkthrough of the total effect

![](../../assets/2ef83160290f68fb.png)

Thanks to [Keith O’Conor](https://twitter.com/keithoconor) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.