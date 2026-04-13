---
title: Graphics Programming weekly - Issue 157 — November 15, 2020
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-157/
author: Jendrik Illner
published: '2020-11-15'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

Daniel Jones has made a video summary of the articles included in this article available on [Youtube](https://www.youtube.com/watch?v=9ugxkpAm2lY)

- brief article that shows how to create a D3D11 device without a window
- presents that the FXC compiler can export compiled shader to a C compatible header

![](../../assets/3cc9d511da494101.jpg)


- the article presents techniques to improve Subsurface Scattering (SSS) implementation based on the model used in
[PBRT](https://www.pbrt.org) - presents a basic overview, how to importance sample the model
- shows several improvements that aim to reduce Fireflies, optimize the implementation
- additionally covers the material system that allows blending between materials that have SSS influence and not

![](../../assets/070671bcc1a67edb.png)


- the Unity explains how to implement a heat map view to visualize the temperatures in Buildings
- this effect is based on Frostpunk, the shader implemented as compute shader

![](../../assets/153338b6b5aacd15.png)


- the article provides a brief overview of different kinds of array indexing types in shaders
- presents Vulkan caps required for a bindless access pattern
- shows when extra annotations are needed for correct results and how these interact on different hardware

![](../../assets/08deca9dacea1ef2.png)


- the blog post explains what shader occupancy is and how it connects to vector registers usage
- provides a brief overview of GCN hardware details showing how shader compilers deal with data loading

![](../../assets/110385b1550f8dea.jpg)


- the article explains how to implement a CRT rendering effect using GLSL
- implements screen curvature, scanlines, and edge darkening

![](../../assets/a1828d9eead1324d.png)


- the article explains how the 2D VFX effect has been integrated int the 3D world of Blightbound

![](../../assets/5f3dc4f4bdd2c087.png)


- article introduces OWL, an abstraction build on OptiX 7
- presents the difference abstraction difference between OptiX 6 and 7
- shows several projects using it and samples on how to use it

![](../../assets/87f9e0f24cd606ac.png)


- the article presents the difference between baked, screen-space rasterization and Ray-traced GI of unity
- shows how many visual influences can be expected from the different techniques
- brief look at the performance of the other techniques

![](../../assets/0c217643515ccc8a.png)

Thanks to [Mike Turitzin](https://miketuritzin.com) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.