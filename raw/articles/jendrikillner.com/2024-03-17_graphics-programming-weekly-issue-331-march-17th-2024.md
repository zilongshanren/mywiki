---
title: Graphics Programming weekly - Issue 331 - March 17th, 2024
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-331/
author: Jendrik Illner
published: '2024-03-17'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the video provides a walkthrough of the steps when optimizing a voxel renderer
- each step is explained and visualized to make it very easy to understand
- covers a large number of optimizations and, for each, discusses the effect on performance and memory usage

![](../../assets/063ae907238bebb2.png)


- the article provides an overview of the different models available to describe the appearance of a mesh using OpenUSD
- Explain the advantages and the disadvantages of the available methods

![](../../assets/e7a4a0124cede658.jpg)


- the article provides an overview of all new features available in the D3D12 Agility SDK update
- covers work graphs, new shader model, accessible memory for CPU/GPU, as well as unifications on shader creation

![](../../assets/53918f2f9e885444.png)


- an overview from Microsft into what work graphs are
- what possibility it enables, a brief summary of the spec
- additionally points out the changes since the preview version last year

![](../../assets/82f1a21540d9f370.png)


- the article provides an overview of how a G-Buffer classification system for BRDF selection can be authored using work graphs
- provides performance numbers for the work graph and an Uber shader approach
- discusses lessons learned, pitfalls, and performance considerations
- It additionally discusses the open challenges and future developments

![](../../assets/de95000a3784d08c.jpg)


- AMD provides a list of talks they will be presenting at GDC (starting today)
- each talk is given a small summary and where it’s taking place

![](../../assets/9ae72b2ad9e1130c.png)


- the article provides a detailed walkthrough of how to implement Loop’s and Blinn’s font rendering approach from Siggraph 2005
- provides an overview of the approach with many visualizations
- shows how to implement the algorithm using D3D12 mesh shaders
- source code is provided

![](../../assets/bc716296610dad03.png)


- the blog post discusses a method for generating uniformly distributed quaternions
- explains the theory of quaternion and the proposed method to generate random rotations
- provides an implementation without using trigonometric in C++ SIMD as well as GLSL

![](../../assets/ca686756cda16325.png)


- the whitepaper presents which tools and optimizations passes in spirv-cross and glslang are available to optimize shaders, taking advantage of knowledge from multiple shader stages
- shows an example of how vertex outputs can be eliminated if the connected pixel shader doesn’t read the attribute

![](../../assets/968b57d381d2cca9.jpg)


- second part in an article series about creating a LODing system that allows per-cluster LOD selection
- focuses on performance and quality fixes for the proposed solution from part 1

![](../../assets/32dad0e5a1842f4c.png)


- the video provides an explanation of Gaussian Splatting and how it connects to point clouds and nerfs
- presents the base idea and optimizations that have been applied to speed up the technique

![](../../assets/25bd92b2f448a5cf.png)

- the blog post provides an overview of new features and improvements in PIX
- additionally presents at which state of support the new D3D12 features, such as shader graph, shader model 6.8, etc.

![](../../assets/0418e9b78d8749d1.png)

Thanks to [Erika](https://twitter.com/rrika9) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.