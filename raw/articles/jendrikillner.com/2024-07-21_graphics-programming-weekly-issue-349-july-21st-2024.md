---
title: Graphics Programming weekly - Issue 349 - July 21st, 2024
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-349/
author: Jendrik Illner
published: '2024-07-21'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the 2-part article series explains how Brixelizer GI (a sparse distance field backed GI solution) limitations affect Foliage geometry
- part 1 explains the limitations, and Part 2 covers how to extend the system to support Foliage (alpha-tested) geometry
- the implementation of an additional Alpha cache helps to resolve the problem
- additionally, it discusses how the system deals with animations

![](../../assets/741160cc1d7cac0c.png)


- the video presents how to create an SDF for a rectangle using Unity and Unreal
- effect allows the modification of many parameters, including size, edge thickness, corner radius, and stroke thickness

![](../../assets/fc8d5d33a3053316.png)


- the article explains how images are represented
- covers the build-up from single binary images to grayscale and, finally, color images
- a brief discussion of the concept of resolution, human vision as well as DPI

![](../../assets/d987b3eeb6857757.png)


- the paper presents a detailed look at how to use D3D12 work graphs to generate a procedural world
- shows how multiple generation phases are combined with GPU ray-tracing to create a world
- discusses how the BVH structure is used to place markers, generate Ivy, marketplace arrangements, as well as ground clutter
- presents results with performance information

![](../../assets/27196a353f7ce8d1.png)


- the series of articles discusses how work graphs are now allowed to execute mesh rendering work
- part 1 how presents the getting started guide through the code sample on basic setup
- the second part focuses on best practices for performance
- finally, the last part discusses how to use work graphs to procedurally generate and render a whole game world

![](../../assets/229b942341323c82.png)


- A brief blog post discusses what aspects of the new mesh nodes preview for d3d12 can be debugged using Pix

![](../../assets/895147f4ee7ef7d7.jpg)


- SCALE is a GPGPU toolchain allowing CUDA programs to be natively run on AMD GPUs
- discusses what hardware is currently supported and how it’s achieved
- documentation provides examples of how to get started

![](../../assets/f7d707c0bd938f7f.png)


- the article discusses a solution to allow GPU instanced and animated models using Vulkan
- presented solution pre-calculates all bone transformations for all frames of the animations and calculates the sample index during the vertex shader stage

![](../../assets/e6ca02d5d0cec58e.png)


- the paper to be presented at SIGGRAPH 2024 presents a technique for rasterizing hair from hair strands
- since it’s based on Hair meshes (which are protected by patents), I did not read it and can’t provide a summary
- ensure to contact your legal team before proceeding to read

![](../../assets/c8f73be5bc570c40.jpg)

Thanks to [Vivitsu Maharaja](https://twitter.com/vivitsum) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.