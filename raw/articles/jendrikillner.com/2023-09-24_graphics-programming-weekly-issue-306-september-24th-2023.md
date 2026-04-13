---
title: Graphics Programming weekly - Issue 306 - September 24th, 2023
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-306/
author: Jendrik Illner
published: '2023-09-24'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the video explains BC texture compression
- covers how the compression format works and the differences that exist
- explains guidelines on which format to use for different use cases
- additionally also covers SRGB color space and explains when/how to use it

![](../../assets/3928fb2d9ea7835a.png)


- the paper introduces a new method for the triangle mesh reconstruction from an SDF representation
- The presented method is based on the insight that each SDF sample represents a spherical region
- generates an initial mesh and then shrinks the shell using a gradient flow approach

![](../../assets/c9f5eab47311f84a.jpg)


- the article presents improvements to using floating point atomic operations if all inputs have the same sign
- additionally discusses how half and double floating point numbers might be operated on with uint atomics

![](../../assets/fee011009590828b.png)


- the article presents how to implement Worley/Voronoi noise
- starts with Voronoi shapes and expands to noise
- additionally presents how to animate the noise

![](../../assets/74ceb389159bef9c.png)


- the article presents a set of differences between WebGL and WebGPU
- covers clip space, synchronization, mip-generation, canvas handling, and more

![](../../assets/4009bae7faca473d.png)


- the latest version of the raytracing analyzer adds support for visualizing the rays in the scene
- allows each ray to be visualized, heatmap information, and ray types
- presents how to analyze performance given the provided information

![](../../assets/a5420690e21e5f98.png)


- the latest edition of the Memory Visualizer adds improved support for resource aliasing
- additionally adds support for post-crash analysis

![](../../assets/6961bb16ec6e8c97.png)


- the article presents changes in the latest AMD GPU profiler update
- improved work graph, instruction search, output merger state visualization as well as shader hashes

![](../../assets/b5c72ba270791dc6.png)


- the blog post provides an introduction to the Gaussian Splatting rasterization technique
- discusses the technique, data collection, training as well as downsides of the technique

![](../../assets/4d03518c12474940.png)

Thanks to [Aras Pranckevičius](https://aras-p.info/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.