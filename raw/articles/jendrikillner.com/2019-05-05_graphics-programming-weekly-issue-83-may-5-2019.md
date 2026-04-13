---
title: Graphics Programming weekly - Issue 83 — May 5, 2019
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-83/
author: Jendrik Illner
published: '2019-05-05'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- presents how Granite deals with vkPipeline management
- API designed for user convenience
- hashmaps used for control of the different state combinations
- pre-warmed with information from previous runs using
[Fossilize](https://github.com/ValveSoftware/Fossilize)

![](../../assets/e37cf8254661667b.png)


- explains a code generation method to generate helper functions to make indexing into unbounded resource tables more convenient
- uses glslang symbol information to auto-generate accessor functions

![](../../assets/1faddecd7a55249d.png)


- explains the BHH (Bounding Half-Space Hierarchy) data-structure
- allows sorting of 3D objects with sublinear search

![](../../assets/1ff0a4bc93f92315.png)

- bibliography file containing 2000+ entries, in computer graphics, rendering, transport theory, and statistics

![](../../assets/54bad73a367cc9f2.png)


- part 3 of the volumetric cloud rendering series
- the code has been released on
[github](https://github.com/sergeneren/Volumetric-Path-Tracer) - Open VDB is used to store volumetric data

![](../../assets/d28b27361e4beef1.png)


- a twitter thread that provides an overview about how games, especially in regards to texturing, have changed since the 90s

![](../../assets/839dad65f98d1560.jpg)


- presents the rendering architecture used for the raytracing demo
- uses nearby pixels to fill in missing lighting information
- temporal reprojection is used to gather extra information from the last 6 frames

![](../../assets/07c6b1f976528d8a.png)


- overview of the state of graphics API wrappers and libraries for rust

![](../../assets/f8bffa094a10ec61.png)


- explains 3D camera projections
- shows the influence of the camera FoV and how it changes the perceived image
- presents how to calculate a perspective and orthographic projection matrix

![](../../assets/7942d7e40d7ded29.png)


- shows how to convert effects from unity shader code to use the ShaderGraph system

![](../../assets/943eeb0976a8b3f6.png)

Thanks to [Eric Haines](http://erichaines.com/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.