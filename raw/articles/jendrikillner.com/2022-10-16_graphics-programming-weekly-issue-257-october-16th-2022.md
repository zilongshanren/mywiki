---
title: Graphics Programming weekly - Issue 257 - October 16th, 2022
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-257/
author: Jendrik Illner
published: '2022-10-16'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article presents how to improve an outline rendering technique by using surface IDs instead of normals
- discusses which issues the use of normals can cause and how surface Ids can improve
- presents what kind of data issues can occur and how to pre-process the data

![](../../assets/29ae28cad6810202.png)


- the article presents how the Nvidia hardware feature Shader Execution Reordering (SER) can be leveraged in D3D12 ray tracing workloads
- shows how to integrate the API and the necessary Root signature and shader changes
- presents how the new feature was integrated into UE5 Path Tracing and Lumen
- additionally mentions when the feature should be used and what kind of speedups can be expected

![](../../assets/1247766df06a7d80.png)


- the article (and video) explains how to author and integrate shaders with transparency support for use in Unity
- covers Alpha Blending, Alpha Cutouts, sorting as well as shadow integrations
- presents code examples for all stages with detailed explanations

![](../../assets/2b4cdaa5137174fb.png)


As a 3D Engineer at Threedy, you develop our core system’s algorithms and data structures, always optimizing data representations for efficient and cutting-edge 3D data streaming and visual computing.

![](../../assets/2365cbc531701a1a.png)


- the article presents that the next DirectStorage release will start to support GPU-based GDeflate decompression
- drivers can provide optimized implementation, but a generic DirectCompute fallback will be provided
- lists what hardware and software will support the feature

![](../../assets/383e96d485bba9e1.png)


- the video tutorial series covers how to build a complex rock shader
- this episode shows the implementation of a snow shader in both UE and Unity with view-dependent sparkles
- presents how to analyze source texture data and separate information so that smaller texture resolutions can be used without quality loss
- shows how to pack textures and manually unpack them from the shader

![](../../assets/33418bbb28b0e96a.png)


- the Developer Guide provides a functional description of Intel’s hardware ray-tracing implementation
- additionally provides a list of guidelines for developers to allow them to maximize performance

![](../../assets/83526bb4afd63de3.png)


- the blog post provides a comparison of DLSS 2.4, FSR 2.1.1, and Intel XeSS upscaling techniques
- provides uncompressed images of different scenes for better comparison

![](../../assets/46317f5b37bf11eb.png)

Double Fine Productions is looking for a full time graphics programmer to join its San Francisco based development studio. Having recently shipped the award winning Psychonauts 2, we are looking to expand our graphics and systems programming team to support the development of our future titles.

You will be responsible for developing rendering features, optimizing game performance and memory usage, and building low level systems on PC and Xbox.

Applicants should have a strong preference for working in a highly creative, innovative, and nimble development environment, where collaborating with design, audio, art, animation, tech, and other disciplines is standard.

![](../../assets/27034fe5c580ce80.png)


- the video provides a high-level explanation of the DLSS 3 system
- covering the hardware and system components required for the functionality
- presents how motion vectors and optical flow are combined to generate intermediate frames

![](../../assets/6581063dbc1a5eca.png)

- a collection of simple test scenes for light conditions in UE5 and NVIDIA Falcor 5.2 Mogwai path tracer
- contains Perfect Lambert Plane, Perfect Mirror Plane, Perfect Mirror Weak White Plane, as well as a Glossy Plane

![](../../assets/12e1fbc4b641c008.jpg)


- the article presents how to implement a compute shader that can be used to paint on vertex meshes in realtime
- explains the fundamentals of compute shaders
- shows how to integrate the system with code examples in Unity

![](../../assets/ae21b458041604cc.png)


- the video explains how to implement blending between two skeletal animations
- shows what information the ASSIMP library provides and how the data is structured
- additionally presents how to update the OpenGL implementation to allow blending

![](../../assets/49bf08ca0926dad5.png)

- the article provides examples of different camera distortion effects (with code examples)
- presents distortion, expansion/contraction, longitudinal/horizontal stretch as well as extrusion effects

![](../../assets/a1a02821de7c2457.png)


- PIX adds a separate preview branch of the tool that supports the Preview Agility SDKs
- supports Enhanced Barriers, Independent Front/Back Stencil Refs and Masks, Triangle Fans
- lists known limitations and considerations when starting to use the preview tool

![](../../assets/a1d509ba97ebfefe.png)

Thanks to [Keith O’Conor](https://twitter.com/keithoconor) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.