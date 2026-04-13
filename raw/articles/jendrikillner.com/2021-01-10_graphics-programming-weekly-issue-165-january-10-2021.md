---
title: Graphics Programming weekly - Issue 165 — January 10, 2021
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-165/
author: Jendrik Illner
published: '2021-01-10'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article explains in detail how to render a raytraced sphere that interacts with other parts of the Unity rendering pipeline
- covers how to use a billboard to render there sphere, explaining how to calculate an optimal camera facing quad and texture mapping
- extending to support shadow casting, receiving, and use of conservative depth output to enable early depth rejection

![](../../assets/8c173cb96176be94.png)


- beginner-focused tutorial that explains how 3D data is structured in computer graphics
- covers what shaders are, what type exists, and how they are used within Unity to define the look

![](../../assets/4de9590b54f67378.png)


- the video tutorial explains how to create interactive snow on terrain and objects using Godot
- interactive snow is implemented via a snow mask that is updated and blends between textures and modifies vertex positions
- snow on objects is world space projected snow textures that also is interactive

![](../../assets/b780eb68e1af717a.png)


- the article presents a walkthrough of a RayTracing abstraction layer that was implemented for D3D12 and Vulkan
- provides a walkthrough of how to combine the elements to a example scene
- shows what the different raytracing shaders are and what they contribute to the final image

![](../../assets/08095046b230625f.jpg)


- the updated tool allows an in-depth view into the raytracing details on AMD hardware
- reveals that the driver might inline all shaders into a single shader or keep shaders separate
- the new update provides a shader table view to see the relative cost of different stages
- additional shows all shaders with costs, call count, and ability to see ISA

![](../../assets/751dcb6695df0c10.jpg)


- the video explains the CUDA memory model
- covering the rules of how memory operations on shared memory from multiple threads are processed
- looking at loading, reordering, barriers, etc.. and explains with examples (source code published)

![](../../assets/54aa3a1fabae433d.png)


- Overview for the start of a new shader tutorial series for beginners
- starts by providing the motivation, approach, and topics that will be covered

![](../../assets/2fea1e75f8d63af5.png)


- the article focuses on providing a walkthrough of dithering techniques
- provides an overview of what dithering is, use cases
- showcase of different dithering patterns and what results they produce

![](../../assets/c4d2a14e77a60070.png)


- the article provides an overview of the CVTT compression techniques used (DirecXTex fork aims to be an experiment to improve state of the art)
- shows how the different formats are compressed, common themes across formats, and lists possible improvements

![](../../assets/ea8fbe4bf15a0e44.png)

Thanks to Michael Hazani for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.