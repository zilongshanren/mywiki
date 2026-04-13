---
title: Graphics Programming weekly - Issue 343 - June 9th, 2024
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-343/
author: Jendrik Illner
published: '2024-06-09'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the video recordings for the Rendering Engine Architecture Conference have been released
- covering a large number of topics from resource management, GPU-based mesh pipeline, testing approaches, and much more

![](../../assets/c37ee116b1764807.png)


- the blog post provides a detailed discussion of implementing meshlet-based virtual geometry rendering into Bevvy
- discusses how meshlet LODs are calculated, how meshlet culling has been implemented, and how they are rendered without mesh shader support
- presents findings from different approaches and discusses the pros/cons of the various approaches
- Additionally, it shows the integration work for supporting systems (depth pyramid generation, material shading, etc.).

![](../../assets/d3cb56087913ee93.png)


- the blog post discusses the author’s experience learning Vulkan through the development of a small 3d engine
- presents the approach for keeping things focused and decisions leading to using Vulkan
- explains the API concepts and how they are used in the engine (shaders, pipelines, queues, etc.)
- additionally presents how higher-level techniques are implemented inside the engine

![](../../assets/15b4b6a660cc92ae.png)


- the short paper presents how to reformat bezier interpolation using cheaper functions
- shows the implementation of quadratic, cubic, and higher-order polynomials
- additionally shows how a GPU implementation could take advantage of hardware linear interpolation

![](../../assets/107a4d82bc555752.png)


- the article presents a geometric and statistical analysis of the PCG2D hash function
- explains the terminology of random number generators and how they can be mapped onto GPUs
- visualization of provided using shader toys

![](../../assets/cf0587a2629fb83c.png)


- the blog post provides a high-level view that explains machine learning concepts for practical usage by graphics programmers
- presents the individual concepts and how DirectML maps them into compute shaders
- additionally presents an overview of the different passes that make up the Open Image Denoise implementation

![](../../assets/63974a7e2d36b4e3.jpg)


- the blog post introduces the release of the first stable release of OpenPBR
- discusses the importance of the standard and the history of its development
- MaterialX now contains a reference implementation of the model

![](../../assets/6bd8898822977ecc.jpg)


- the article presents how a rasterizer calculates intermediate values on a triangle
- explains barycentric Interpolation and explains the cause for common artifacts on PS1-level hardware
- then derives perspective-correct Interpolation that resolves the artifacts

![](../../assets/b88af66c3d40056c.png)


- The videos for I3D paper presentations have been released
- covering Reducing the Memory Footprint of 3D Gaussian Splatting, SimLOD: Simultaneous LOD Generation and Rendering for Point Clouds
- additional Deblur-GS: 3D Gaussian Splatting from Camera Motion Blurred Images as well as Light Field Display Point Rendering

![](../../assets/bc647145747dc220.png)


- the video provides an overview of the OpenGL Ecosystem
- explains the history of OpenGL and how OS integration compares to Direct3D
- presents what software layers are involved and which software components enable easier cross-platform development

![](../../assets/950797f555c0725c.png)

Thanks to [Cort Stratton](https://mastodon.gamedev.place/@cort) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.