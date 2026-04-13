---
title: Graphics Programming weekly - Issue 272 - January 29nd, 2023
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-272/
author: Jendrik Illner
published: '2023-01-29'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article presents a rendering analysis of the game Teardown
- shows a look at video captures of the game to develop an intuition before diving into RenderDoc
- shows that the game objects are drawn using a 3D Sprite concept
- the game uses a volumetric shadow map that is updated from the CPU
- additionally covers Lighting, Compositing as well as Post-Processing

![](../../assets/2acc51e438df8e9a.png)


- the paper presents how to take advantage of ray tracing hardware for progressive photon mapper
- shows how ray tracing–based collection outperforms hash-based GPU photon mapping algorithms
- additionally introduces Photon Culling, a technique to reduce the number of photons stored per iteration

![](../../assets/89b9e75038885b7d.png)


- the article explains updates required for Chapter 4 of Battle Royale
- shows how increasing triangle counts of the mesh tented is better than masked materials and techniques to preserve vegetation density
- discusses how to handle object animation and improve culling

![](../../assets/994e0e8b4dd7edb4.jpg)


- the new release introduces support for the Brotli-G lossless compression format
- additionally adds support for RGBA_10101002, R8 and 16-Bit PNG File support

![](../../assets/2efa749cfce5f57c.png)


- the video presents how to implement image-based lighting of the Cook-Torrance microfacet BRDF
- contains how to derive the Ground Truth Solution and shows how the Split Sum Approximation can simplify the equation
- presents how to implement the required shaders using GLSL

![](../../assets/8f8d2f8e9533c325.png)


- the article introduces the idea of expression quadtrees in terms of a collection of square grids
- this allows the space to grow indefinitely as the used spaces change (movement or zooms)

![](../../assets/73cb1f10ca0751ab.png)


- the WIP guide covers how to use the WebGPU graphics API from C++
- at this time, presents how to create a render a basic 3D mesh
- additionally shows how to load and apply textures

![](../../assets/c56cc7510b56db96.png)


- the article presents how to implement a camera look-at matrix
- visually shows how the components combine to form the result
- mentions the difference between rasterization and ray-tracing workloads

![](../../assets/483de8f647020e46.jpeg)


- the blog post describes what changes were required to make Lumen work in 60 FPS mode for the new season of Fortnite
- discusses how a reverse lookup structure is used to accelerate per-mesh surface cache information for sharper reflections and lighting when using software ray tracing at low resolutions
- shows how spatiotemporal blue noise was able to improve results from the same number of rays

![](../../assets/fa9f4e63ece127fa.jpg)


- the article explains the issue that needed to be solved for Virtual Shadow Maps at 60fps
- explains common issues that are often encountered when trying to cache sun shadow maps
- additionally explains a collection of techniques required to improve performance and quality for the Fortnite art style

![](../../assets/d25ca4205855d1c2.png)

Thanks to [Bruno Opsenica](https://bruop.github.io) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.