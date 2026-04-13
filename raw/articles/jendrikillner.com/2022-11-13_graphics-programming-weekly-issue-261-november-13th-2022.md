---
title: Graphics Programming weekly - Issue 261 - November 13th, 2022
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-261/
author: Jendrik Illner
published: '2022-11-13'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the video tutorial explains how to create a metal material
- explains the effect of the metallic parameter, metal reflectance values as well as specular reflection
- shows the implementation with both Unity and Unreal Engine

![](../../assets/eb6b6cb6c03f9d89.png)

- the article describes how to compress high-quality BC1 images efficiently
- explains how the compression space is optimized
- in-depth explanation of the vectorization process and how to efficiently use SSE, AVX, … to optimize the implementation

![](../../assets/89e0823f2f2d82e4.png)


- the article presents an overview of GPU-based GDeflate compression
- shows the influence of staging buffer size on compression speed
- list several best practice recommendations

![](../../assets/2b356fbe487a4fc4.png)


- the article presents the API rules for casting between texture formats in both Vulkan and D3D12
- discussing sRGB, BC(Block Compression), Depth and generic color format rules
- additionally, it shows Sparse/Tiled resources can be used to alias textures

![](../../assets/1513f26fb464127e.png)


Marmoset, developer of the real-time rendering software, Marmoset Toolbag, is looking for an experienced developer to help build bigger and better software tools for 3D artists.

The responsibilities of a Tools Engineer on the Marmoset team will focus on technical design and implementation of UI systems, and refining the user experience for new and existing workflows in 3D art production.

![](../../assets/1fa0cc86fa39e72b.png)


- the presentation shows how submitting/recording commands lists from the API to the GPU affects performance
- shows how to use GPU View and Radeon GPU Profiler to understand the execution behavior
- presents different strategies and how they differ
- additionally presents insights into the driver behavior by discussing the Open Source Linux driver behavior

![](../../assets/f96d726472bccb81.png)


- the presentation explains what Half edges data structure is
- discusses use cases and issues
- presents how to overcome some of the issues by using an Implicit half edges structure

![](../../assets/19f3ad367c4f4e2f.png)


- the article provides an overview of the implementation of three different techniques for procedural texture mapping (Triplanar, Dithered Triplanar, and Biplanar Mapping)
- implementation is provided in UE5 visual shader code
- explains the trade-offs of the different solutions

![](../../assets/b683b83cca150ba3.png)


- the video provides an overview of a Physically Based shading model
- discusses the Cook-Torrance BRDF model, Schlick GGX, and Fresnel
- provides both the theoretical overview as well as the GLSL shader code implementation of the presented technique

![](../../assets/d768ed2c91218839.png)

- the blog post describes the design of a validation system for bindless shader resource access
- shows how the shader code is protected against invalid resource usage
- presents how shaders can report failures back to the CPU to be able to inform the user about the error

![](../../assets/86e1563c58b75c0a.png)


Double Fine Productions is looking for a full time graphics programmer to join its San Francisco based development studio. Having recently shipped the award winning Psychonauts 2, we are looking to expand our graphics and systems programming team to support the development of our future titles.

You will be responsible for developing rendering features, optimizing game performance and memory usage, and building low level systems on PC and Xbox.

Applicants should have a strong preference for working in a highly creative, innovative, and nimble development environment, where collaborating with design, audio, art, animation, tech, and other disciplines is standard.

![](../../assets/27034fe5c580ce80.png)


- recording of the Siggraph showcase of original, interactive projects of the year
- includes Horizon Forbidden West, Unity-based machine learning character posing, hybrid VR, desktop sculpting, the cavern UE5 demo from the coalition, Unity Digitial Humans facial capture system, and much more

![](../../assets/21f671425b7ab2fc.png)

- the slides for the Real-Time Volumetric Clouds of Horizon Zero West from SIGGRAPH have been released
- covers the cloud modeling, authoring, and improved lighting implementation
- additionally covers optimizations and presents performance numbers

![](../../assets/d1ae274153dde269.png)


- the video explains the implementation of a 2D deferred shading system
- shows a breakdown of the individual steps of the lighting pipeline
- presents how to render shadows using a stencil-based shadow approach
- shows how to generate shadow mask extension meshes, update stencil buffers and deal with shadows overlapping multiple objects

![](../../assets/6bef97b08f15d62b.png)

- the article explains how to generate Worley, Voronoi, and fractal noise in a GLSLS shader
- ShaderToy example is provided

![](../../assets/c4a7b55200559a58.png)

Thanks to [Jonathan Tinkham](https://zincfox.red) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.