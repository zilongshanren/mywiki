---
title: Graphics Programming weekly - Issue 119 — February 16, 2020
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-119/
author: Jendrik Illner
published: '2020-02-16'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article presents the problems with ray tracing in terms of divergence workflows
- Imagination GPUs are able to reorder rays in hardware to maintain better coherency

![](../../assets/056fb67de07d0a83.png)


- the blog posts presents how to use high quality volumetric fog in UE4 to simulate ground level rolling fog
- based on multiple layers of 3D texture based noise, and fake self shadowing

![](../../assets/6510c0fb68e695de.png)


- new Geometric Algebra designed for realtime graphics and animation applications
- including SSE optimizations

![](../../assets/d72250ee859cacf7.png)

- article presents how to use barycentric coordinates in a pixel shader to manually interpoliate values in a quad

![](../../assets/23363e5d713abe5c.png)


- the article presents a brief overview of what deferred shading is
- shows how to customize the deferred shading logic used by unity
- expose global tweakable settings that influence the whole scene

![](../../assets/c3b658c177a0c138.png)


- collection of gpu resources
- links to details about hardware, shader languages, and WebGPU

![](../../assets/8fbc4faae01cd7df.png)


- the Unity article describes how to generate a stylized procedualr skybox
- shows how to generate proper speherical UVs, generate a sky gradient, stars, moon, sun and clouds

![](../../assets/be215b3b1880b7a1.png)


- the Unity tutorials shows how to use Material Property Blocks
- this feature allows Unity to better batch draw calls even if multiple materials are used

![](../../assets/3cf0b39d68bcb3c5.png)


- beginner Unity shader tutorial that shows how to implement a gradient made from 4 colors forming a quad

![](../../assets/539bf9ada1673c4b.png)

- last part of Unity shader torial that shows how to add ripples into the sand dunes
- this is achieved using normal mapping

![](../../assets/77c8639bca2be724.png)


- Unity tutorial that shows how to calculate new normals from a vertex shader
- this is required because the vertex shader modifies the vertex positions
- normal is calcuded by transform neighboring points and adjusting the normal based on the relative change of the points

![](../../assets/d853853e3d9e9f86.png)

Thanks to [Warren Moore](http://metalbyexample.com/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.