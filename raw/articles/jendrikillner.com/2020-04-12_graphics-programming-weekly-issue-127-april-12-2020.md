---
title: Graphics Programming weekly - Issue 127 — April 12, 2020
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-127/
author: Jendrik Illner
published: '2020-04-12'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the talk presents an overview of rendering features developed for Path of Exile
- showing what constraints the game provides and how it enables these implementations
- Point Light Shadows (Screenspace Hierarchical Variance shadow maps)
- Screenspace Global Illumination
- Subsurface refraction, a technique used for ice and water
- Water flow map generation on the CPU using Algebraic Multigrid
- grass and fur using pre-calculated raytracing
- an extensive collection of brief overviews of other techniques such as burning, fracturing, scalar field vectorization

![](../../assets/a13b66dbc8aff12f.png)


- A virtual machine that is written in C enables executing of a subset of SPIR-V shaders (only 2D texture operations, no 3D etc.)

![](../../assets/bfd6c00e7a861a53.png)


- presents operations that reduced the shading time required from 21.58ms to 13.52ms
- combination of scene-specific adjustments, implementation changes to noise generation and variance reduction

![](../../assets/d0d200066ddc3e36.jpg)


- A guide aimed at technical artists to preset best practices for geometry, texture, material and shader optimizations for mobile devices

![](../../assets/97e5e99f29933bf0.jpg)


- the article presents implementations optimizations to speedup trilinear filtering
- taking advantage of the representation of power floating-point number to speed up operations

![](../../assets/979d47cc6b980cc8.jpg)


- The database of articles included in this series has been updated with a new look
- this is the first step of a more extensive upgrade, and new functionality will be added soon. Stay tuned

![](../../assets/a3b1a28ded0ead8d.png)

Thanks to [Max R.R. Collada](https://twitter.com/maxandonuts) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.