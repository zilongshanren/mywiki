---
title: Graphics Programming weekly - Issue 102 — October 13, 2019
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-102/
author: Jendrik Illner
published: '2019-10-13'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- a mathematical framework for more consistent layering of bump/normal maps using linear surface gradients
- shows the problems with reliance on vertex level tangent space in existing techniques
- how to express existing methods in the new framework
- including source code

![](../../assets/5c9c8532c7d1f7c5.png)


- high-level system discussion of a retro GPU emulation implemented in Vulak compute shaders
- implementation details are discussed in the presentation
- using Subgroup and async compute for further optimizations

![](../../assets/b11e7cd965d675dd.png)


- new RenderDoc version allows explicit GPU playback selection
- improved SPIR-V reflection, performance improvements
- more extensions and feature levels supported for Vulkan and D3D12

![](../../assets/fe814cf60d2ebb1d.png)


- proposal of approach for rendering layered materials
- layers are defined by anisotropic NDFs on varying tangent vector fields

![](../../assets/099018974ef93676.png)


- the post describes the perspective from Stardock on D3D12/Vulkan vs. D3D11
- new possibilities but also many more problems
- performance improvements with D3D12 need to be balanced against the higher QA costs compared to D3D11

![](../../assets/bdf7fca159374e15.png)


- proposes a real-time solution to rendering unstructured point clouds
- combination of temporal reprojection, random point selection, and GPU vertex buffer shuffling

![](../../assets/6692131ea24f0d34.jpg)


- provides an overview of the foundations of denoising techniques
- expands pon the basics to explain how more complex schemes are constructed
- how to consider denoising as a building block for several different problems

![](../../assets/bff5e0aa17d2105c.png)

Thanks to [Graham Wihlidal](https://www.wihlidal.com) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.