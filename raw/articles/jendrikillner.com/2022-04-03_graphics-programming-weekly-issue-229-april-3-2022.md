---
title: Graphics Programming weekly - Issue 229 - April 3, 2022
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-229/
author: Jendrik Illner
published: '2022-04-03'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the blog post describes the functionality of the new pipeline library extension and how to use it to reduce draw-time shader compilation stalls
- the extension breaks up PSO compilation into four distinct areas Vertex Input Interface, Pre-Rasterization Shaders, Fragment Shader, Fragment Output Interface
- these separate aspects can then be linked together to create the PSO
- link-time optimizations are optional to trade compilation time for runtime performance

![](../../assets/2b0ecc4dd566aa63.png)


- the paper presents an improvement of compute shader-based point cloud rasterization
- presents LoD structures for point clouds
- introduces the concept of per-batch Adaptive Vertex Precision that allows each batch to use three different position precisions relative to the center of the batch

![](../../assets/986a7b4e60bdb0cb.png)


- the blog post details the changes in the new PIX version
- enables exporting captures into C++ so that users can simplify or experiment with making changes to the generated code

![](../../assets/72c82d2c8cc444f7.png)


- the GDC talk presents the Mali Offline Compiler and how to use it to analyze shader performance at authoring time
- discusses the importance of understanding your target hardware to make informed decisions
- presents how much instruction costs might vary between different hardware generations
- highlights the importance of choosing the correct variable precision

![](../../assets/9ce2565391c5800a.jpg)


- the video lecture explains the concepts of compute shaders
- covering how to bind resources, compile and use shaders from OpenGL
- it also covers the execution model covering execution groups, threads, and how it matches onto hardware cores
- it additionally covers how mesh shaders fit into the graphics pipeline
- covering the high-level concepts and presenting demos of mesh shaders

![](../../assets/78a6a6250c3b59cb.png)


- the video tutorial shows how to implement specular highlights for a toon shader
- extends the shaders from the previous part of the series
- implementation is shown in both Unity and UE4 visual shader editor

![](../../assets/845ef8da3fe03b94.png)


- the video lecture presents deferred shading, discussing the problems of forward shading and how deferred can help to overcome them
- it also covers a brief overview of anti-aliasing techniques
- it additionally covers how Variable Rate shading can be used to reduce the shading rate for a group of pixels to reduce shading cost further
- it additionally presents an overview of Deferred Adaptive Compute Shading

![](../../assets/f7bd229a5141ace6.png)


- the article provides a collection of performance advice to consider with texture sampling
- discusses how helper lanes are required for MIP selection
- presents different ways that can allow reduced energy consumption on Mali GPUs

![](../../assets/397955fae473b0d9.png)


- the video explains how to use render-to-texture to enable object selection
- draws out an object id and primitive ID to a texture
- this texture is read back to the CPU to allow the detection of which object has been selected

![](../../assets/78c5f31e53409dff.png)


- the talk provides an overview of different LOD concepts
- how different Level of Details modes can be used to achieve improved performance

![](../../assets/2796bd2d3b6ef543.png)

Thanks to [Leonardo Etcheverry](https://www.linkedin.com/in/leonardoetcheverry/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.