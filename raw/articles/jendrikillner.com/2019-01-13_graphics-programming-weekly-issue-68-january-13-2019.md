---
title: Graphics Programming weekly - Issue 68 — January 13, 2019
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-68/
author: Jendrik Illner
published: '2019-01-13'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

I am running a small survey to be able to improve the series further this year.

If you have two minutes to spare, please fill out the survey [https://goo.gl/forms/nNPzrRpiMERIgtBl2](https://goo.gl/forms/nNPzrRpiMERIgtBl2)

This week also contains articles that have been published during my vacation since issue [67](https://www.jendrikillner.com/post/graphics-programming-weekly-issue-67/)

- start of series for programmers with D3D11 experience starting to learn D3D12
- explains what command queues are, how they express different GPU execution timelines and how fences allow synchronization between CPU and GPU

![](../../assets/09129ad38c8a7865.jpg)

- explains how to render water using WebGL, Rust, and WebAssembly
- water supports reflection and refraction
- reflections are rendered using a reflection plane technique, that mirrors the world and clips fragments if they are below the water plane

![](../../assets/a28be30f6fce1cd0.png)

- shows how to use screen space derivatives to create hard edges on a mesh in the pixel shader
- how to calculate greyscale from colors

![](../../assets/46a0d2901393b1de.png)

- video explaining the rendering equation in an easy to understand and visual way

![](../../assets/9223aa633e5fea98.png)

- list of common patterns for shadertoy programming
- included are: normalizing screen coordinates, color management (hue, sRGB), line drawing, antialiasing, blending, vector math, and random value generation

![](../../assets/66d9b289958faaaa.png)

- preprint of the article to appear in GPU Zen 2 talking about the implementation details (C++ and GLSL)
- replaces the 3D histogram transformation with three 1D histogram transformations
- improves quality of the result under mipmapping and shows how to generate correct results with compressed texture formats

![](../../assets/cd254c77fe6b2285.png)


- walkthrough of steps to learn graphics programming
- recommends starting that beginners start with a raytracer/rasterizer from scratch before starting to use any graphics API
- list of project ideas for beginners

![](../../assets/7a5809b183b2f504.jpg)

- explains how to rasterize the glyphs from a font into a texture. Providing the coverage information that is required by the technique discussed in part 1 and 2
- includes code for the OpenGL compute shader
- overview of typography terms and explain how to correctly position the glyphs to form the final text on the screen

![](../../assets/ce9e3f29fa6034bb.png)


- presents what vertex attributes are and how they are interpolated to deal with perspective distortions correctly
- uses this knowledge to interpolate normals and UV coordinates for the sponza model

![](../../assets/ef73454ba5b02efc.png)

Part 1 of the article:

- explains how classical forward/deferred pipelines work and how tiled and clustered algorithms can be used to extend these ideas
- includes animations to show the concepts in a more visual way
- presents strengths and weaknesses for each technique

Part 2 of the article:

- presents the clustered forward shading implementation
- how to subdivide the camera frustum into clusters and implement light culling
- provides links to further information sources

![](../../assets/6e20f605e82874e5.png)


- frame breakdown of the Rise of the Tomb Raider with D3D12 on PC
- uses a light pre-pass architecture
- lens flares don’t use a visibility query but instead use the depth buffer to calculate visibility
- talks about shadow mapping, ambient occlusion, depth-aware upscaling, reflections, hair rendering, volumetrics, and tone mapping

![](../../assets/50e14f9e0bde185e.jpg)


- explains how to apply an expanding color effect that converts the world from greyscale back to color as post-processing effect using Unity scriptable render pipeline
- presents how to reconstruct world space position from the depth buffer

![](../../assets/ae012b4dbbf00406.png)


- shows how to set up a Docker container image that is able to run shader compilers
- supported are: DXC, FXC, GLSLang, AMD Radeon Graphics Analyzer, DXIL signing, SMOL/V and Vulkan SDK

![](../../assets/5b1523386a29da22.png)

If you are enjoying the series and getting value from it, please consider supporting this blog.

[Support this blog](https://donorbox.org/jendrikillner)