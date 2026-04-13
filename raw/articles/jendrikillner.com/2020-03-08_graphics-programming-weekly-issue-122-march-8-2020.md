---
title: Graphics Programming weekly - Issue 122 — March 8, 2020
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-122/
author: Jendrik Illner
published: '2020-03-08'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article explains how exposure used to work in Unreal Engine 4.24
- what problems the behavior caused and how the new implementation solves these problems
- looking at grey-point targeting, physical exposure units, lens values, and perceptual brightness
- additionally provides an overview of the debug modes available

![](../../assets/aa02352cd3600dac.png)


- the article shows how the milky way rendering from the Witcher 3 - Blood & Wine DLC was implemented
- including a brief look at the star rendering

![](../../assets/c177e720e6460a89.jpg)


- A Unity tutorial that focuses on the deformation of a plane to create a crumbled paper look
- implemented using a vertex shader

![](../../assets/6f730c46f8b7a6f0.png)


- the post provides an overview of an algorithm for boolean operations on geometry
- this allows for runtime slicing of meshes such as for dynamic destructions systems
- the idea is based around finding the overlap of two meshes to generate new vertices along the interception to create the cut

![](../../assets/3d68942eb817385f.png)


- part 3 of Nvidia ray tracing series
- this part focuses on the history of ray tracing hardware and presents how Nvidia changed its design approach
- Turing has dedicated hardware for Raytracing and machine learning tasks. the previous architecture contained only general-purpose compute

![](../../assets/09e0e6cc81ff252d.png)


- the article discusses techniques to compress data for skeletal animation data used for game runtimes
- presents an overview of standard terms
- followed by a look at data quantization, quaternion compression, and track compression

![](../../assets/1ae739029dae5206.png)


- a very brief high-level overview of mesh shaders and necessary OpenGL extension
- provides a condensed OpenGL example that renders a fullscreen quad

![](../../assets/5b6067cd16900c07.png)


- the article presents multiple scenarios in D3D12 where manual barrier synchronization is required
- followed by a back-to-back copy into buffers that cannot be synchronized by barriers and shows the behavior observed on actual hardware

![](../../assets/119ca2ad4f8690c8.png)


- the post focuses on efficient and high-quality grid rendering for “The Machinery” editor
- implementation is done in a pixel shader on world space quad created by two triangles
- shaders deals with LOD selection, anti-aliased line rendering, falloff for gracing angles and grid extends

![](../../assets/c1a56e6278e4b601.png)

Thanks to [Lesley Lai](https://lesleylai.info) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.