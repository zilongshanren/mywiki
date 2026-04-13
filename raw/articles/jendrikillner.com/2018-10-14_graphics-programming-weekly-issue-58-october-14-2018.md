---
title: Graphics Programming weekly - Issue 58 — October 14, 2018
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-58/
author: Jendrik Illner
published: '2018-10-14'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- explains an O(n) algorithm that calculates 2D distance fields by operating on rows and treating samples as overlapping quadratic parabolas
- shows ideas to visualize distance fields, generate tiling noise and some use-cases of distance field functions

![](../../assets/f04a327f476de42b.png)


- slides from XDC (
[X.Org](http://x.org/)Developer’s Conference) - Vulkan timeline semaphores
- allow increasing a 64-bit value on signal and wait on “greater than” a target value
- unified system for CPU and GPU waits
- look at how to implement them in the drivers

- many more talks about OS-level graphic topics

![](../../assets/8b657eda76b5beb4.png)


- compute shader based adaptive GPU tessellation technique using Mesh Shaders on Turing
- up to ~25% rendering time reduction at high tesselation rates

![](../../assets/8bbb2bd2e6888713.png)


- explains the Vulkan ray-tracing extension
- contains an overview of the ray tracing pipeline, the new shader types and how to interact with the API
- shows how to generate the acceleration structure, update and compact it as required

![](../../assets/1c5fac7c48be4b5b.png)


- explains the mathematical foundation behind deep composition that allows compositing of volumetric effects such as fog

![](../../assets/9b1dc0c779f62b2c.png)


- walkthrough of the steps required to render the Moana scene in the authors custom path tracer
- uses a binning scheme on rays combined with on-demand geometry loading to be able to render the scene on a 32 GB RAM machine

![](../../assets/bc91a45561f3551f.png)


- discusses a change to the SDL render back-end that will batch CPU rendering commands to reduce the number of draw calls required
- this will improve performance significantly

![](../../assets/a1057483cd697de1.png)


- next part of the series on gfx-hal usage (low-level graphics API for Rust)
- adds support for loading and using vertex buffers

![](../../assets/46341986c6169836.png)


- explains a water ripple system implementation that uses a top-down projection of ripples onto the water surface in a separate rendering pass

![](../../assets/9d2c1e2754336631.jpg)



If you are enjoying the series and getting value from it, please consider supporting this blog.

[Support this blog](https://donorbox.org/jendrikillner)