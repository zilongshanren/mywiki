---
title: Graphics Programming weekly - Issue 54 — September 2, 2018
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-54/
author: Jendrik Illner
published: '2018-09-02'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

I am going to be on vacation for the next two weeks so this series will take a small break and will return on September 24th.

- presents a filtering approach for a pixel art style in a 3D environment
- discussion of filtering theory and derivation of a filter for real-time use
- provides GLSL implementation of the filter

![](../../assets/cef803c85fe2a53f.png)


- in-depth documentation for Unity
- explains the most common terms, the difference between the rendering pipelines with strengths and weaknesses
- explains the difference between global illumination systems and light modes
- provides 4 example scenarios that show how the desired game influences the decisions

![](../../assets/14d669bf7824c14d.png)


- shows how to reformulate the rendering equation so that stochastic shadows can be combined with non-stochastic shading
- explains how to denoise the stochastic shadows
- shows results and discusses the performance of the approach

![](../../assets/beb6a4da1faf330e.jpg)


- start of a new Intel series about Vulkan
- the focus is on the high-level usage and will be comparing different approaches to common problems
- walkthrough of the structure of the series and how the sample code will be structured

![](../../assets/a0d70f1e4a5a3c44.png)


- investigates the performance effect of different acquire → render → present approaches
- shows visually why two sets of frame resources are required to utilize the available hardware efficiently
- the sample allows experimentations with different scene complexities and CPU workloads

![](../../assets/40629dc4f43ab668.png)


- explains the strategy how GPU memory is currently managed and what allocation strategy is used
- shows a visual representation of allocator usage and discusses the weaknesses of the current approach, pointing to possible future improvements

![](../../assets/89a1c2b15c704bbc.png)

- tutorial on how to implement a candle flame using 3 separate texture channels and noise distortion using Unity

![](../../assets/7503312abc10c2d5.jpg)

- discusses how the drunk effect in “The Witcher 3” was implemented based on reverse engineering the D3D11 shader disassembly
- provides the reverse engineered HLSL source code

![](../../assets/f645b46658555637.png)


- reusing a generic ray-triangle intersection for other calculations such as calculating the distance from a ray to a curve segment

![](../../assets/c38cd495dfbbd035.png)

- Unity tutorial that extends water with flow map (previous part of the series) to support transparent water rendering
- apply underwater fog and approximation of refractions

![](../../assets/7e8bb00cc3bce948.jpg)

- overview how the large-scale ambient occlusion data is baked for Homefront: The Revolution
- implemented using rasterization with an orthographic projection and per-pixel linked lists
- runtime information stored in regularly spaced cells

![](../../assets/61b57cd41f1f7209.jpg)

- article discussing what is required to achieve high-quality lightmaps
- UV space rasterization, using a UV G-buffer to collect necessary information to trace rays
- dealing with shadow leaks and UV seams
- an algorithm to enable mipmap generation for lightmaps

![](../../assets/4b07b80850a4664e.jpg)


- explains why clipping happens in 4D clip space before the perspective divide is applied

![](../../assets/600c22a99f9c7a5e.png)

- blender developers view of the technologies shown at Siggraph
- talking about USD / Hydra, MaterialX / ShaderX / OSL / Gaffer and OpenColorIO

![](../../assets/1265861cb1001433.png)

- overview of the open shading language in 3ds Max
- how OSL was implemented into the 3ds max architecture
- discusses problems encountered and improvement possibilities for OSL

![](../../assets/01bd0d530e268d48.png)

- explains what contact-hardening shadows are
- presents one technique that can be used to implement them and deal with artifacts
- discussions of a method to optimize the process by splitting the shadow mask generation into two passes
- the first pass generates the penumbra mask at a quarter resolution and the second pass generates the soft shadows, sampling from the quarter resolution penumbra mask

![](../../assets/30ebdd8a533f5378.jpg)


- the slides for all talks from the High-Performance Graphics 2018 conference have been uploaded

![](../../assets/e48c003cc491ac87.jpg)

- can now show register and LDS (Local data share) usage as well as theoretical occupancy
- new render target overview table, provides information about all render targets in the frame in one location
- more robust handling for applications that create multiple device contexts

![](../../assets/0a7563bd2dfbe80b.jpg)

- explains how to pack an integer and a floating point number into a single unsigned render target channel
- provides source code for packing and unpacking into a variable number of available bits

If you are enjoying the series and getting value from it, please consider supporting this blog.

[Support this blog](https://donorbox.org/jendrikillner)