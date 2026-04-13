---
title: Graphics Programming Weekly - Issue 407
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-407/
author: Jendrik Illner
published: '2025-09-07'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- provides a comprehensive introduction to physically based rendering, starting by explaining the physical concepts
- explains the bidirectional reflectance distribution function (BRDF) and how light interacts with surfaces
- demonstrates the mathematical foundations behind microfacet theory and importance sampling techniques

![](../../assets/4d0ea8d39904dfd5.png)


- provides a comprehensive explanation of color spaces, color models, and gamuts in digital imaging
- covers the mathematical foundations of how colors are represented and transformed between different systems
- explains practical implications for developers working with color-accurate workflows and display technologies

![](../../assets/ad97a80ad3cd3d55.png)


- a detailed article that covers the various steps that are required to understand blurs
- provides interactive examples for the various components
- analyzes different blur algorithms and their performance characteristics
- closes with a discussion of Kawase blur technique and how it achieves high-quality blur effects with fewer texture samples than traditional methods

![](../../assets/48b1dc3ca249bac2.png)


- explores modern techniques for achieving order-independent transparency in real-time rendering
- discusses the challenges of transparent object rendering and various solutions to depth sorting issues
- presents advances in per-pixel linked lists and weighted blended transparency methods
- covers applications in virtual production workflows where accurate transparency is critical

![](../../assets/6e80f8bbd5b6ef86.png)


- demonstrates the benefits of GPU-compatible texture compression for storage size, VRAM usage, and sampling performance
- provides practical guidance on texture format conversion tools and automation workflows for game development

![](../../assets/b81cd7b0991730c6.png)


- demonstrates how to overlap CPU and GPU work by having multiple command buffers and synchronization objects
- covers the synchronization challenges and resource management needed when multiple frames are being processed simultaneously

![](../../assets/28ee655cd8e93d3d.png)


- demonstrates how to use profiling data and performance analysis to guide optimization decisions
- covers systematic approaches to identifying bottlenecks in game performance
- explains the importance of measuring before optimizing to avoid premature optimization pitfalls

![](../../assets/fba2d5d1879dd7db.png)


- argues that often UE5 performance issues stem from a poor user experience design rather than just technical limitations
- discusses how hidden system dependencies and lack of performance visibility make optimization difficult for teams
- proposes better profiling tools and feature-level cost indicators to help developers understand what systems are active

![](../../assets/5a651a2fd47cdbf2.png)


- presents updates and developments in the MaterialX open standard
- discusses community contributions and adoption across different software and studios

![](../../assets/40c71216e57ac47f.png)

- retrospectively examines the evolution of Direct3D 12 over its first decade since release
- details the significant API additions, including ray tracing, mesh shaders, work graphs, and enhanced barriers
- covers new shader features like wave operations, bindless resources, and HLSL language improvements
- reflects on how development workflows and programming patterns have changed with modern D3D12 features

![](../../assets/6a8b1c77fb6a4dd2.jpg)

Thanks to [Angel Ortiz](https://x.com/aortizelguero) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.