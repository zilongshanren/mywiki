---
title: Graphics Programming weekly - Issue 365 - November 10th, 2024
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-365/
author: Jendrik Illner
published: '2024-11-10'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article presents a technique for Order-Independent Transparency
- the presented technique uses multiple passes over the geometry to generate transmittance coefficients
- discusses how this turns the problem into an additive shading problem
- presents the implementation details step-by-step, limitations and possible optimizations

![](../../assets/55f83693dc4f50ff.png)


- the article discusses the concept of coordinate systems and how it relates to column vs row-major matrices
- provides into how the misconception is based on old fixed function style OpenGL concepts
- overview of how matrix and vector convention are disconnected from memory layout
- additionally shows how the Odin language supports these concepts on the language level

![](../../assets/4701bd9ea4be8ad6.jpg)


- the blog post provides an overview of the process of how procedural vegetation was implemented in COD Black Ops 4
- discusses the design process and how different developments across the teams influenced the design of the system
- provides insights into the noise generation process, placement logic as well as storage considerations

![](../../assets/93a9d1bdbc7fa582.png)


- the article goes into detail how to implement a floating point (0 to 1) conversion to 8bit and back without relying on division support
- first presents the simple division method and then derives how to implement the same without division support
- goes into detail about how floating point precision and ranges

![](../../assets/914720b15459251c.png)


- the blog post provides insight into the BC7 texture compression format
- explains how to best express constant color blocks within the constraint of the format

![](../../assets/b5ec3fc0575d3f5b.png)


- the article series about the implementation of a CPU rasterizer C++ continues
- part 4 to 6 are released and add support for 3d transformations, projections, clipping, depth buffer, and perspective correct interpolation

![](../../assets/3e29664c1b465070.png)


- the blog post presents a beginner-focused introduction to shader programming
- provides an overview of how shaders allow access to GPU resources, execution model, and restrictions
- shows how classical rendering pipelines with vertex & pixel shaders are used

![](../../assets/ca5b6ed965d58c05.png)


- single header HLSL library for spherical harmonics
- implements support for L1 (2 bands, 4 coefficients) and L2 (3 bands, 9 coefficients) SH (spherical harmonics)

![](../../assets/04c7039737eea242.png)

Thanks to [Aras Pranckevičius](https://aras-p.info/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.