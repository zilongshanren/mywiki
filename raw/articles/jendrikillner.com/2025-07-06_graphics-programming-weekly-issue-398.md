---
title: Graphics Programming Weekly - Issue 398
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-398/
author: Jendrik Illner
published: '2025-07-06'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- Explains the concept and motivation behind virtual textures for efficient GPU memory use
- Compares software and hardware implementations, highlighting current hardware limitations
- benchmarks sampling and tile updating performance between different hardware and driver versions
- shows that Intel’s drivers are the only ones with tile update performance that appears viable for real-time applications

![](../../assets/067f61f29798ce67.png)


- Proposes a real-time method for rendering glints using image-based lighting
- Introduces a fast environment map filtering technique for dynamic materials and lighting

![](../../assets/56dd46d9e8571893.png)


- the developers’ vlog discusses the implementation process of screen space global illumination
- presents various techniques and stages of the implementation process
- shows performance and quality differences between the various parts of the implementation

![](../../assets/857c193c5c22d991.png)


- The video introduces the REAC 2025 conference
- discusses the underlying idea and philosophy of the conferences
- provides an overview of the content and presents the schedule
- All videos are available on the channel now

![](../../assets/c1ee57c59f72413e.png)


- The video provides a visual explanation for shadowing terms such as umbra and penumbra
- shows how bokeh and lights for near and far objects interact to create the appearance that light and shadows are attracted by each other

![](../../assets/ef76f110283428cf.png)


- The video provides a high-level overview of how to implement a terrain generation vertex shader
- discusses how to further develop this basic technique in various aspects
- Additionally, announces a coding jam based on the project

![](../../assets/3a17a3d0e1a91064.png)


- covers the Overwatch team’s journey to modernize their global illumination (GI) solution
- discusses tradeoffs in quality, performance, and workflow for GI in a large-scale game
- Details the transition to a new approach that improves artist workflow while maintaining visual quality
- shares challenges and solutions for supporting a wide range of hardware

![](../../assets/0ab1e6a2f731b863.png)


- explains the meshlet rendering pipeline used in Dragon’s Dogma 2 and Monster Hunter Wilds
- addresses challenges of rendering vast, dynamic environments with stable performance
- Details the transition to meshlets across shared engine technology
- compares early and current meshlet implementations and shares optimization results

![](../../assets/9911951b8cafdc70.png)


- Details the geometry rendering pipeline and data management in Swarm Engine for Space Marine 2
- addresses challenges of rendering dense architecture, procedural vegetation, and many interactive entities
- Discusses system organization for future optimizations and features
- Explains shader infrastructure and managing the complexity of Uber shader permutations
- shares lessons learned in balancing scalability, performance, and visual complexity

![](../../assets/70ce97ec986164b7.png)


- presents Anvil’s evolution into a centralized engine powering multiple productions from a monorepo
- discusses technical and organizational challenges: modularization, shader complexity, code divergence
- details the rendering architecture as well as the GPU-driven mesh pipeline and frame graph
- covers performance optimization, profiling tools, and data-driven tuning via a centralized platform manager

![](../../assets/da4965d46707cd15.png)


- presents architectural challenges and decisions for GI, ray tracing, and character creator in Dragon Age: The Veilguard
- covers probe baking system, team size, and asset constraints
- discusses ray tracing implementation choices and support for a wide range of GPUs
- details the technical and practical aspects of the character creator tool

![](../../assets/e5e4030c6c3ab3aa.png)

Thanks to Peter Kohaut for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.