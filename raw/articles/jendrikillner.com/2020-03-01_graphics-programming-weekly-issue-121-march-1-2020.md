---
title: Graphics Programming weekly - Issue 121 — March 1, 2020
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-121/
author: Jendrik Illner
published: '2020-03-01'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- copy of an article that was published in GPU Zen 2, updated for changes introduced with Vulkan 1.1 and 1.2
- covering memory management, Descriptor sets, command buffers, pipeline barriers, render passes and pipeline management

![](../../assets/68ccb0053937686c.png)


- video comparing rasterization and ray-tracing algorithm
- analyzing the strengths and weaknesses of both techniques and how they complement each other

![](../../assets/a0a2eb1bdecbb0b7.png)


- the paper presents an overview of Temporal Antialiasing (TAA) techniques, the history, different implementation techniques
- follows up with a presentation of open challenges and discussion of possibilities for improvements

![](../../assets/86455725bc1d85bf.jpg)


- presents findings from compressing PBR material information into a single texture
- developed for terrain-like materials
- shows a comparison of memory usage and performance improvements

![](../../assets/ca02e18fee161f3c.png)


- A FAQ for Vulkan best practices guide by ARM
- swap chain acquisition, image transitions, device lost debugging, and transient attachments

![](../../assets/a48b04510a1ea69f.jpg)


- the 7-min video provides a walk through the history of light transport research
- showing numerous techniques, how multi importance sampling can be used to combine multiple techniques
- closes with the presentation of the “Unifying points, beams, and paths in volumetric light transport simulation” (UPBP) paper

![](../../assets/a081192255c07e51.png)


- the article presents an approximation to the GLSL trisect function
- trisect splits an angle into three equal parts, playing the same role as square root in quadratics

![](../../assets/2dc1c84fd46f73ca.png)


- the tutorial shows how to implement a skeletal animation system using Geometric Algebra (GA)
- additionally introduces the required GA concepts along the way

![](../../assets/5e327b995537311b.png)


- the article presents how to pack UV and gradients (ddx, ddy) into 32-bit gbuffer channels
- this is used for deferred materials where the results of texture samples are not stored in the gbuffer

![](../../assets/c985b90c3ba2a111.png)


- the Unity tutorial shows how to implement a checkerboard pattern if a 2D player is behind another object
- this is achieved using the stencil buffer

![](../../assets/05712e0c53435c9c.png)

Thanks to [Aras Pranckevičius](https://aras-p.info/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.