---
title: Graphics Programming weekly - Issue 354 - August 25th, 2024
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-354/
author: Jendrik Illner
published: '2024-08-25'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the paper presents an overview of the performance characteristics of synchronization primitives
- discusses what factors affect performance and presents performance results for these factors
- presents an open-source testing framework to measure these effects

![](../../assets/0a599287ccc3d361.png)


- this proposal discusses an alternative approach to Pipeline caching in Vulkan
- explains limitations of the existing Vulkan methods
- presents how the proposed solutions suggest solving limitations and giving application developers more control

![](../../assets/f10e5ecea1040b60.png)


- the author presents how Geometric Algebra concepts are often defined in the literature and what better definitions look like
- discusses different concepts such as Inner Products, Contractions, and duals
- additionally ensures comparing the best possible GA implementation against the best possible matrix implementations for a more fair comparison of the implementations

![](../../assets/4ed5b84c99d8017c.png)


- the D3D12 tutorial presents how to get started with compute shader usage
- explains the steps required to setup shaders, create the necessary API objects, and execute the shader
- source code is available

![](../../assets/d82f51e81c41d412.png)


General Arcade, a porting and co-development studio that has worked with a wide range of clients, from indies to AAA developers and publishers, including Larian, From Software, Capcom, Devolver Digital, TinyBuild, and others, is seeking a Software Engineer with a rendering emphasis.

This is a great opportunity to work with a passionate engineering team on cutting-edge industry technologies.

![](../../assets/c3ef79290c0765d3.png)


- the blog post explains how HLSL shaders compiled for mesh shader usage with Vulkan require special annotations
- default shader behavior doesn’t handle it correctly, and it only fails on AMD without any validation errors

![](../../assets/4e0c168374d6cf77.png)


- the article discusses a method to allow virtual geometry to be represented in ray-tracing scenes
- explains issues related to BVH construction and LOD selection
- shows how to integrate generation logic into loading and runtime frames

![](../../assets/50856803fede9423.png)


- the video develops a mental model for 4-dimensional space
- explores where the space is located and what it represents
- starts exploring the space via generalization of concepts from 2D to 3D and finally to 4D

![](../../assets/c63f547152ff39d5.png)

- the short blog post presents how to use human-readable ISA documentation to decode one CDNA instruction

![](../../assets/ac6e5ae5ea803ce8.jpg)

- AMD released ISA documentation for RDNA2 and CDNA ISA
- additionally, it presents a small example application that presents how to use the released data

![](../../assets/16e2d7994ff49a8f.jpg)


- the blog post introduces a prototyping programming platform for shader development
- exposes a way to use a visual node graph editor and HLSL shader nodes for the development of shader techniques
- allows the export of the developed solution into D3D12 code (more targets will be supported later)
- the video tutorial presents how to use the system and the debug tools available to implement a box blur technique

![](../../assets/70d4cd9ea18d9a69.png)


- the video tutorial explains how to load vertex information from within a Vertex Shader instead of relying on fixed function hardware
- provides an overview of the concepts of Programmable Vertex Pulling and use cases that are enabled through it
- implementation is shown using OpenGL

![](../../assets/380e47b8f9669e0f.png)

Thanks to [Lesley Lai](https://lesleylai.info) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.