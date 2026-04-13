---
title: Graphics Programming weekly - Issue 211 - November 28, 2021
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-211/
author: Jendrik Illner
published: '2021-11-28'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article presents the noise issues encountered when rendering out animated camera tracks
- shows result comparisons between different sample counts and supersampling
- presents how the noise issue was solved by projecting static rendering onto proxy geometry

![](../../assets/52b5bb898d56a086.jpg)


- the video shows a visualization of reflection and refraction vectors
- shows how to combine reflection and refraction into a single effect
- presents how to use these vectors for effects within Unity and UE4

![](../../assets/604db92843fd1b97.png)


- the article presents the overview of a small and simple lossless image compression
- benchmark against libpng and stbi are available here:
[benchmark](https://phoboslab.org/files/qoibench/)

![](../../assets/d93d4376eb3680e4.png)


- the article presents an overview of fp16 (16-bit floating-point data types)
- shows what range and precision is available
- discusses 7 tricks to keep in mind when working with fp16 numbers in shaders

![](../../assets/f1a8a89a20f059ca.jpg)


- the paper presents a new approach that decouples displacement from the tessellation of the base mesh
- a displacement-specific acceleration structure is mapped onto the mesh, and tesselation factors are encoded seperate
- the BVH for the displaced geometry is computed instead of loaded from memory

![](../../assets/de57956c440583a9.png)


- provides a rundown of the different stages of a WIP experiment combing surfels and ReSTIR for rendering
- shows images of the different passes, what they contribute and how they form the final result

![](../../assets/24d4e8ac2287af9c.png)


- the article presents a look at the RDNA2 assembly generated from a simple pixel shader that outputs a color from a constant buffer
- compares D3D12_ROOT_PARAMETER_TYPE_DESCRIPTOR_TABLE, D3D12_ROOT_PARAMETER_TYPE_CBV, D3D12_ROOT_PARAMETER_TYPE_32BIT_CONSTANTS
- presents pros/cons of each technique

![](../../assets/78d4fa9b0e96add8.png)


- the article presents a starting point for developing unit tests for rendering algorithms
- shows the importance of small test cases
- additionally presents two real examples from pbrt-v4 and how unit tests helped to solve them

![](../../assets/65e6f2d1ae6c0999.png)

Thanks to [Unai Landa](https://twitter.com/unai_landa) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.