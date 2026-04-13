---
title: Graphics Programming weekly - Issue 123 — March 15, 2020
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-123/
author: Jendrik Illner
published: '2020-03-15'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the post presents the fresnel equations that are used for smooth metals and surfaces such as water
- shows the Schlick approximations and compares them to the equations and where to retrieve the necessary parameter values

![](../../assets/1f7c83d5f86aa0ac.png)


- Reverse engineering the color grading solution used in “The Witcher 3”
- shows how the indexing into LUT works, including rounding mode handing
- the solution used by the game can use up to 3 different LUTs for the same scene

![](../../assets/01873ac243384807.jpg)


- the article aimed at beginners presents how to use ShaderToy to get started with shader development
- extends the example from simple colors to animated scenes
- shows how to implement a spinning octahedron

![](../../assets/8f75a0b1bf8492bf.png)


- the article presents an overview of aliasing in digital signal processing
- then applies the information and shows how the same understanding applies to computer graphics
- covering rasterization, texture and shading aliasing
- short on time? Only read the TL;DR at the end
- example code provided

![](../../assets/c0452a1723197328.png)


- the Unity tutorial shows how to create an outline effect for 2D sprites
- implemented by storing a signed distance field in the alpha channel and using that additional information that in the pixel shader

![](../../assets/8af5e4178869ef26.png)


- discusses buffer allocation, update and mapping strategies
- descriptor pools, texture transfer synchronization, fence signaling, memory alignment, and shader variations

![](../../assets/1aff5a637c751b14.jpg)


- the post discusses how to write a simple GPU Hash table implementation using CUDA
- uses 32-bit keys and values with open addressing and linear probing

![](../../assets/2e12ff2a894dc6cb.png)


- the article presents that combining signed distance fields of primitives using min and max operations can create incorrect SDFs
- this is especially noticeable on the interiors of objects
- offers 5 different ideas/solutions on how to solve the problem

![](../../assets/51e540aa6317a40f.jpg)


- part 4 of ray tracing series by Nvidia
- this episode focuses on the RayTracing APIs in D3D and Vulkan
- discusses the types of shaders and how they are interconnected

![](../../assets/8a953705827417a3.png)


- Video tutorial for Unity that shows how to present the Echo effect (a point-cloud based rendering overlay) from “The Division”
- covers how to generate the data, implement the rendering, interactions with the player and post-processing

![](../../assets/858f71fe12dec641.png)

- overview of what is new with DXR 1.1
- presents how to extend a depth pre-pass system for shader ray tracing using the DXR 1.1 RayQuery object

![](../../assets/239fffb0df3a9a9f.png)


- the document provides an overview of the ASTC texture compression format
- explains how end-point color compression works
- encoding strategies, block sizes and how the format allows the compressor to adapt the techniques for each block

![](../../assets/e13a22119454ff88.png)


- the article presents how to use new ARM tools to gather performance information (later versions will support Continues integration)
- provides an easy to read report that can be used by non-programmers to validate the performance of the game
- the tool allows performance budgets to be defined, will be shown in the UI
- Automated screenshot collection when frames take longer than a specified threshold to produce

![](../../assets/f08989a3aa0bfc5d.png)

Thanks to [Eric Haines](http://erichaines.com/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.