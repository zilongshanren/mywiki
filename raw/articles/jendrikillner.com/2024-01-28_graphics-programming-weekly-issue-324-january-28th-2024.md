---
title: Graphics Programming weekly - Issue 324 - January 28th, 2024
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-324/
author: Jendrik Illner
published: '2024-01-28'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the new Vulkan extension allows developers to express local dependencies between sub-passes so that drivers can stay on-chip memory for tiled hardware
- blog post explains the extensions, how to post existing applications to use the new extension

![](../../assets/989865581f5894fa.jpg)


- Khronos released two new SPIR-V extensions
- the first extension guarantees reconvergence behavior to require the behavior many programmers’ intuition assumed to work
- additionally, a new extension allows correct divergence handling within a quad
- the blog post explains the previous issues and how the extension solves them

![](../../assets/966f015ae017784d.png)


- the blog post describes the history of Portals and BSP trees
- expands the ideas to more modern concepts and suggests the applicability of GPU based solutions

![](../../assets/cb5632bc7f9adfec.png)


- the article presents issues with moving averages and suggests using binomial averages instead
- shows data examples to highlight the issues and explain in frequency domain why they happen

![](../../assets/eccd96610549a0bd.png)


- the article shows how PIX can be used to debug WebGPU applications
- shows what is required to attach PIX, get debug-marker output, as well as frequent issues

![](../../assets/00abd41c37f47d7f.png)


- the author discusses a method to use indirect drawing to draw a dynamic number of instances of each type on the GPU
- The article provides an overview of the implementation (with code examples)
- additionally provides a couple of optimizations and future development steps

![](../../assets/c67ae0fcfa98d631.png)


- the blog post provides a detailed walkthrough of the implementation of a caustics effect using WebGL
- shows the different elements the effect is made up of and how to simulate the different phenomena
- intermediate samples are presented as interactive WebGL examples

![](../../assets/e7101a30b2019212.png)

Thanks to [Giuseppe Modarelli](https://twitter.com/gmodarelli) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.