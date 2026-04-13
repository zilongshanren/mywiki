---
title: Graphics Programming weekly - Issue 74 — February 24, 2019
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-74/
author: Jendrik Illner
published: '2019-02-24'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- in-depth discussion of color spaces
- shows how the color response curve influences which color absolute values are referring to
- explains how to match colors between different color spaces
- how to represent color spaces visually
- what negative color values represent
- defines the standard CIE XYZ and RGB color space and how they have been defined relative to human perception capabilities
- look at the sRGB color space related to all the information covered in the article

![](../../assets/033580c3db058930.png)


- whitepaper explains how to enable GPU assisted validation
- how it is implemented, performance implicatications
- what issues it is a ble to detect and known problems

![](../../assets/a8a6643ca503f7cd.png)


- walkthrough of two algorithms for forward culling techniques
- stream compaction and flat bit arrays
- presents how to implement scalarazation to reduce atomics overhead and achieve higher occupancy
- presents performance comparisions of the approaches with lights and decals

![](../../assets/b0a245e0c46a8aef.png)


- presents multiple approaches to calculate MIP mapping textures when using raytracing
- includes performance comparisons for the different methods
- DXR shader implementation of the RayCones mip selection algorithm

![](../../assets/499f7716bc31288c.png)


- explains how to use GPU instancing
- to render health bars for individual objects

![](../../assets/51172a15c6b7a80d.png)


- implementation walkthrough of the OpenGL Scalable Ambient Obscurance (SAO) algorithm

![](../../assets/b39d8cb2063cbce3.jpg)


- shows how to implement a parallax effect in the pixel shader
- allows the appearance of depth in materials that is not backed by actual geoemtry

![](../../assets/bfc641cfd2447fae.png)


- Vulkan extension that exposes NVIDIA Tensor Cores on Turing GPUs

![](../../assets/7c22883745a5ce32.jpg)

- video, author presents his approach to reducing of tiling artifacts in terrain textures using a height based approach

![](../../assets/1dbd5ca4127a1600.png)

- great visual explanation of Convolution Integrals
- many examples that allow to gain a visual understanding of filters commonly used in computer graphics

![](../../assets/f761017e534d435a.png)

Thanks to Vivitsu Maharaja [@vivitsum](https://twitter.com/vivitsum) for support of this series.

You would like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.