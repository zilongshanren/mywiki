---
title: Graphics Programming weekly - Issue 323 - January 21st, 2024
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-323/
author: Jendrik Illner
published: '2024-01-21'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article presents an overview of mesh shaders and amplification shaders
- shows the considerations and constraints on RDNA2/3 hardware
- showcases the tools available to profile the different stages and identify bottlenecks

![](../../assets/e2581b454c140cbb.png)


- the article presents a detailed look at implementing a mesh shader based rendering pipeline
- each step is accompanied by performance numbers on Nvidia and AMD
- shader code samples are provided

![](../../assets/83e2d6656c68b398.png)


- the author presents an alternative method to calculate the previous frame screen space position given a world space position
- this technique doesn’t rely on projection matrices

![](../../assets/1f1bf97063a7367e.png)


- the blog post introduces a new GPU-based debugging tool to make finding shader issues easier
- allows the detection of out-of-bounds access, resource-bound validation, NAN detection, concurrency validation, and more
- works with Vulkan and D3D12 on both AMD and Nvidia GPUs

![](../../assets/c7ad77945c6dfe78.png)


- the video provides an overview and introduction to machine learning from a game development perspective
- explaining the standard terms, intuition, building an example network, and finally running the example network using D3D12
- the example code is provided

![](../../assets/b9a40a7ff02032ae.png)


- the article presents a method to construct rhombic dodecahedral honeycomb elements from an integer grid
- shows an example of an SDF represented using the method
- presents how to generate the mesh surfaces
- additionally presents some ideas on what the method might be used for

![](../../assets/480b2acac59725dc.png)


- the article explains the packing rules for Constant buffers when used with D3D11/D3D12
- provides examples of different structures
- shows visually how the different members are packed into memory

![](../../assets/b68cd9341a5441c5.png)


- the article provides an overview of GPU sorting algorithms
- provides high-level comparisons between the techniques
- links to papers and implementations of the techniques are provided

![](../../assets/e1dbbde3b19c4f2c.png)

Thanks to [atyuwen](http://atyuwen.github.io/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.