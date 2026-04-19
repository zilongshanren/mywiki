---
title: Erfan Ahmadi Projects
url: https://erfan-ahmadi.github.io/blog/Portfolio
author: Erfan Ahmadi
published: '2015-01-01'
source_blog: Redirecting…
source_site: https://erfan-ahmadi.github.io/
category: graphics
fetched: '2026-04-19'
---

Here are my Graphics Projects sorted from latest to oldest.

# 1. Bokeh Depth Of Field

It’s been a month since I decided to challenge my self with implementing **Bokeh Depth of Field** effect
and began learning complex postfx pipelines.

I’ve learned a lot about post processing and I’m a lot more comfortable with Scatter-as-Gather thinking

There are 3 methods used to create Depth of Field Effect described briefly in [this blog post](https://erfan-ahmadi.github.io/Bokeh/)

- Circular Depth of Field (paper by Kleber Garcia at Frostbite) used in FIFA, NHS, Need For Speed Heat, Anthem, Mass Effect: Andromeda
- Practical Gather-Based Bokeh (GPU Zen Book)
- Depth of Field in Single Pass (Dennis Gustafsson)

![](../../assets/1cacf2b7986f20e2.jpg)

![](../../assets/2db3c4695918fd40.jpg)

![](../../assets/6f0dfc3b0c05d45e.jpg)


# 2. Graphics Projects

Motivations for these Projects were to get comfortable with TheForge API and gain more experience with some Graphics Techniques I’m interested in.

- Bloom
- Tessellation
- Toon Shading
- Deffered Lighting
- Instancing

### Bloom

Bloom gives noticeable visual cues about the brightness of objects as bloom tends to give the illusion objects are really bright.

The technique used is to render the bloom-affected objects to a 256x256 FBO and then blurred and added to the final scene.
Technique based on **GPU Pro 2 : Post-Processing Effects on Mobile Devices** and [SachaWilliens Vulkan Example](https://github.com/SaschaWillems/Vulkan/tree/master/examples/bloom)

The Final pass is **ToneMapping / Exposure Control** and Gamma Correction and all the frame buffers before that are rendered as HDR (R16G16B16A16)

![](../../assets/83dd9f48d7966e8d.gif)


### Tessellation

Tessellation using Hull/Control and Domain/Evaluation Shader in HLSL and GLSL. PN-Triangles is a method using **Bezier Triangles** and does not require a heightmap to improve quality of the geometry unlike the first technique which is simple and passthrough tessellation

![](../../assets/8d475f0fb1944daf.gif)


### Toon Shading

Simple Toon Shading with outlining. It uses **Stencil Buffers** to draw the cool outlines.

![](../../assets/6dc004b4ba1c9f98.gif)


### Deffered Lighting

Blinn-Phong Deferred Rendering. It writes to normal/position/color map in the 1st Pass, Then uses the Lights Data Passed to GPU as Uniform and Structured Buffers to calculate the colors using these textures.

Deferred Rendering doesn’t work too well on High Resolution (**2K**/**4K**) devices such as consoles due to it’s memory and It’s suggested to use [Visibility Buffers](http://jcgt.org/published/0002/02/04/) instead.

Also on Mobile devices it’s good to uses subpasses for tile-based rendering instead of Render Passes, again because of high memory size.

![](../../assets/60aea71f427b7f23.gif)


# 3. SIMD and GPGPU Collision Detection

Implementing Different Methods of Circle to Circle Collision with **Spatial Partitioning** Techniques and Vulkan Graphics Compute and SIMD AVX2 Technologies

Resources and More Details and Charts are on Github Page.

[[GitHub](https://github.com/Erfan-Ahmadi/CircleCollision)]

### Motivation

This Project Is For Learning Purposes of Following Topics

- SIMD/Vectorization using
**AVX**/**AVX2** - Vulkan Compute Shaders and GPGPU Programming
- Data Oriented Programming

**Circles** were chosen to focus more on [ Broad-Phase](https://developer.nvidia.com/gpugems/GPUGems3/gpugems3_ch32.html) algorithms of the Collision Detection Pipeline.

![](../../assets/8125208b3ab35eb8.gif)

![](https://raw.githubusercontent.com/Erfan-Ahmadi/circle_collision/master/docs/explode_fun.gif)


**Broad-Phase**- Brute Force ( O(n^2) )
- Spatial Partitioning
- Grid
- K-D Tree
- Quadtrees
- BSP

- Sort and sweep
- Simplex-Based : GJK

**Narrow-Phase**- We Have Circles Here and Math/Physics Calculations are easy.

**Technologies/API’s****CPU**- Simple Sequential
- Multi-Threaded
- SIMD
- AVX2
- AVX-512


**GPU**- Vulkan Compute Shaders
- OpenCL