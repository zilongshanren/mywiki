---
title: Graphics Programming weekly - Issue 292 - June 18th, 2023
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-292/
author: Jendrik Illner
published: '2023-06-18'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the talk discusses the design of the Task Graph architecture used by Activision
- covers how to author tasks, design iterations, interactions with the memory allocation systems
- additionally presents how it interacts with multi-threaded command recording

![](../../assets/d725ef3c43c01176.png)


- the presentation slides explain the improvements done to decoupled shading
- discusses how decoupled shading enables improved visual stability
- presents how the technique has been implemented by using Shadels that reduces the limitations of overshading of previous iterations of the technique
- show how to generate a PrimiteID texture from rasterization as a replacement for position texture maps
- additionally shows how the material system has been designed to enable utilization of the new shading method

![](../../assets/f026269eecb1bc8a.png)


- the paper presents a new method to render glittery materials
- introduces a new statistical method to calculate the number of glints for each pixel
- source code and a Unity implementation demo are available

![](../../assets/862359730a793756.png)


- the article presents an overview of line extraction techniques
- discusses line theory and types
- presents Screen-Space Extraction as well as Geometry-Based (Mesh Contours)
- discusses limitations and considerations of each technique
- additionally gives recommendations on when each technique should be used

![](../../assets/c822e774bc451d11.png)


- the article presents a discussion of the limitations of metal hardware related to barriers across thread groups
- also discusses the complexity of the current compute ecosystem across platforms

![](../../assets/2a2f51aeab87d0f9.jpg)


- the paper introduces a novel importance sampling algorithm for the GGX microfacet BRDF
- presents an explanation of the method and how it compares to the Heitz method
- code implementation is provided

![](../../assets/4bf222b8e3a6b550.png)

Thanks to [Trevor Black](https://trevord.black) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.