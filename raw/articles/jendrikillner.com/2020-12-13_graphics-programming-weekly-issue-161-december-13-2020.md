---
title: Graphics Programming weekly - Issue 161 — December 13, 2020
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-161/
author: Jendrik Illner
published: '2020-12-13'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article gives an understanding of how different types of camera and lenses work
- provides many interactive examples that explain the various elements, aspects and how they interact

![](../../assets/0311a31c12cd1597.png)

- the video tutorial provides an overview of signed distance fields
- explains how to use SDFs for font rendering
- provides an example implementation of multiple font effects (thickness, feather, outline color)

![](../../assets/6bff42d25e6cd324.png)

- video recording from all talks in the Siggraph 2020 course in a single video
- covering Intro to Moving Mobile Graphics, Mobile Graphics 101, Vulkan on Mobile Done Right, Deferred Shading in Unity URP,
- Large Voxel Landscapes on Mobile, High Quality, High-Performance Graphics in Filament are covered below in more detail

![](../../assets/22b8e422420ab125.png)

- introductory slides for physically based rendering course
- provides an overview of fundamental terms and concepts
- explaining how the different ideas fit together to create a basic physically based shading implementation

![](../../assets/ff915c57adf699e7.png)

- the video tutorial shows how to generate grass blades that swing in the wind
- LODs are supported, reducing the number of segments for each blade of grass when it’s further away from the camera
- implemented as compute shaders using Unity

![](../../assets/502a425e15f17254.png)

- the video tutorial explains how to implement a ripple effect
- first implements a sprite-based effect, extends this afterward to support 3D mesh deformation
- implemented using Unity shader graph

![](../../assets/e280eb2fe3982ea9.png)

- short blog post that provides advice on how to debug refraction in a raytracer
- provides what values to expect when debugging refraction on a glass sphere

![](../../assets/28a8517046e8eba0.png)

- the article presents an overview of different compression formats and libraries
- comparing quality and compression speed for several texture types

![](../../assets/6197c0acc4fb8e7f.png)

- the article explains the implementation of Caustics using a photon mapping technique that takes advantage of DXR capabilities
- the first part focuses on caustics from meshes (such as bottles, glasses)
- additional provides a performance comparison between Nvidia GPUs
- part 2 focuses on water-based caustics

![](../../assets/9f5999e50618e70f.png)


- the article shows examples of how to use mesh shaders (code examples in GLSL)
- show how different data types and models influence the performance
- gives advice on best-practices when designing a solution for Nvidia hardware
- additionally provides pointers on what might be different on other hardware

![](../../assets/666bbdcc720e5f18.png)


- the RDNA 2 Instruction Set has been released
- shows that RDNA 2 supports dedicated instructions for BVH intersection to accelerate ray tracing workloads

![](../../assets/af64d74a4498d433.jpg)

- AMD released the source code for the Memory Visualizer
- tools support Vulkan and D3D12 to provide insights into memory usage

![](../../assets/07f6a57fb1e7292d.png)

- the article shows how fading our transparent objects when getting close to an intersection helps them to appear more volumetric
- technique presented in the article uses the depth buffer information from opaque objects to fade out the transparent

![](../../assets/f7f85d8fb179dd0b.png)


- the paper presents the results of research into using the RTX raytracing hardware for unstructured point rendering
- presents multiple iterations from a reference CUDA implementation to more complex RTX solutions
- comparing performance for the different approaches

![](../../assets/0dac40e2743a4d6b.jpg)


- video for the talk has been released, was covered in the week
[147](https://www.jendrikillner.com/post/graphics-programming-weekly-issue-147/) - how to take advantage of tiling GPU architecture and enable the use of fp16 math
- cloth shading, reduction of energy loss for rough metals, multi-bounce AO

![](../../assets/97b52725873c116d.png)

- the talk explains the Voxel-based terrain system used in Roblox
- voxels store material id and material occupancy (0,1) range
- how to generate meshes from the sparse voxel representation
- texture mapping, tiling reduction, water considerations, and various performance advice

![](../../assets/00ae72624bba9f33.png)

Thanks to [Robert Wallis](https://github.com/robert-wallis) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.