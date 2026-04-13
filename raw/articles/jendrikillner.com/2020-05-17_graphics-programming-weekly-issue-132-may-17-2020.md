---
title: Graphics Programming weekly - Issue 132 — May 17, 2020
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-132/
author: Jendrik Illner
published: '2020-05-17'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the paper presents a new technique that allows a massive number of dynamic lights to be rendered in real-time
- the presented implementation shows 3.4 million dynamic, emissive triangles in under 50 ms
- this is archived by reusing information from spatially and temporally adjacent pixels to filter probabilities to guide rays

![](../../assets/2b7c0c59c3ceda4b.png)


- AMD virtual event that contains talks about
- Ryzen™ Processor Software Optimization
- optimizing for Radeon™ RDNA Architecture
- From Source to ISA: A Trip Down the Shader Compiler Pipeline
- A Review of GPUOpen Effects
- Curing Amnesia and Other GPU Maladies With AMD Developer Tools
- Radeon™ ProRender Full Spectrum Rendering 2.0: The Universal Rendering API


![](../../assets/8d285f5543c07c19.png)



- overview of what Constructive Solid Geometry (CSG) is and workflows
- presents the algorithm that allows for iterative updates including how to calculate intersections and mesh generation

![](../../assets/0a72229c31660aa9.png)


- the post provides an overview of the new AMD memory profiler for Vulkan and D3D12
- this tool allows gaining a deeper understanding of memory usage
- shows all allocations, tracked on a timeline, will enable comparisons of snapshots and gives warnings about possible problems

![](../../assets/80f53764f291f132.png)


- the article shows how to calculate the shadows from the sun
- presents the results of the shadow quality with white and blue noise
- the implementation is then extended to Spherical Positional and spotlights

![](../../assets/1972b11800c0974b.png)


- the article presents how using blue noise can improve ray marching results
- provides a shadertoy that compares against white noise

![](../../assets/2bc45d1c21b5f961.png)


- the author presents his ideas about how the Nanite technology in the UE5 tech demo might be implemented

![](../../assets/99e845943803e818.jpg)


- the article that discusses possible ideas on how the UE5 nanite technology might be implemented
- contains links to exciting techniques that might be related, or inspired the development

![](../../assets/04d886706ac5fbbb.jpg)


- an overview of the new Nvidia Ampere Architecture aimed at compute workloads
- new tensor cores for f32 data, IEE compliant fp64, and BF16 throughput improvements
- adds the ability to run multiple processes on the same GPU with error isolation

![](../../assets/0d04221760ce1064.png)


- overview of new features in CUDA 11 and how the NVIDIA Ampere GPU hardware features are exposed

![](../../assets/7b8e748040b9b3e7.jpg)

Thanks to [Aras Pranckevičius](https://aras-p.info/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.