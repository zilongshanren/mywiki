---
title: Graphics Programming Weekly - Issue 393
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-393/
author: Jendrik Illner
published: '2025-05-25'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- introductory video tutorial on using Slang shader language to render a basic Gaussian splat
- provides a beginner-friendly walkthrough from setup, to convering the Slang language essential and application iintegration
- takes these concepts to explain how to render a basic Gaussian splat training process from python

![](../../assets/e665bb923e5ae22e.png)


- tutorial on Vulkan’s dynamic rendering feature that simplifies rendering without framebuffers
- explains how to transition from traditional render passes to the more streamlined dynamic rendering approach

![](../../assets/bf23806d5a145e5f.png)


- demonstrates the implementation of a GPU driven renderer
- explains GPU-based culling, draw call generation using indirect drawing as well as buffer compaction
- details implementation of clustered forward shading with optimized light assignment using subgroup operations

![](../../assets/fb818331916653e5.png)


- introduces Skewed Oriented Bounding Boxes (SOBB) for ray tracing acceleration
- presents an efficient algorithm for transforming standard AABB BVHs into SOBB representations
- demonstrates performance improvements of 1.0-11.0x over AABB BVH and 1.1x over OBB BVH for secondary rays, with similar memory requirements to AABBs

![](../../assets/bdcf5c7fb4ee4a3a.png)


- implements a WebGPU-based particle simulation that creates emergent life-like behaviors through asymmetric attraction/repulsion forces
- describes optimization techniques like spatial binning and parallel prefix sum for computing inter-particle forces efficiently
- discusses rendering approaches with anti-aliasing for both large and sub-pixel particles with glow effects

![](../../assets/1f85d3a22375b1ff.png)


- explains techniques for animating grass through wind effects by simulating gusts using noise textures
- details how to implement player interaction with grass, making it bend away from objects and characters
- also covers an approach for cutting grass dynamically

![](../../assets/f4f61bc12c4d5968.png)


- continues the custom lighting model series with techniques to simulate colored pencil art style
- presents shader methods for recreating the grainy texture and stroke patterns of traditional colored pencil drawings
- demonstrates implementation in both Unity and Unreal Engine using the visual shading language

![](../../assets/f437e9aa110ef3df.png)

Thanks to [Jasper Bekkers](https://x.com/JasperBekkers/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.