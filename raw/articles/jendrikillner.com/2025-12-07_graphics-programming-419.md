---
title: Graphics Programming 419
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-419/
author: Jendrik Illner
published: '2025-12-07'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- introduces CUDA Tile, a tile-based programming model launching with CUDA 13.1
- provides developers with cuTile Python for accessible GPU programming and CUDA Tile IR for building custom DSL or libraries

![](../../assets/136c0c3595243971.png)


- introduces VK_EXT_present_timing extension to enable precise frame pacing control in Vulkan
- provides timing feedback from previous frames and allows specifying target presentation times for future frames

![](../../assets/baf237a97b79104c.png)


- presents a low-quality ray tracing mode using ray queries and data stored in acceleration structures
- eliminates ray pipelines, shader binding tables, and texture access by storing average diffuse color in TLAS instanceCustomIndex
- uses VK_KHR_ray_tracing_position_fetch to compute face normals from triangle vertex positions

![](../../assets/3cada67c6bf9de2c.png)


- proposes a tile-based framework for synthesizing large-scale terrains from 3D Gaussian Splatting exemplars
- builds on Wang Tiles with boundary constraints to enable seamless tiling of Gaussian fields

![](../../assets/ad5c7bfb9075a665.png)


- presents a walkthrough of implementing a GPU debugger for AMD hardware
- explains how to use registers and trap handlers to pause GPU execution and inspect register state
- demonstrates stepping through shaders, examining variables, and integrating with SPIR-V compilation through RADV’s ACO compiler

![](../../assets/0eddbf6876caa23b.png)


- provides a machine-readable specification for Arm Mali GPU performance counters starting from Mali-G71
- offers Python wrappers that resolve symbolic counter references for any supported GPU
- enables structured iteration through counters based on various orders

![](../../assets/bb784310813705d4.png)


- shares techniques learned from creating four tiny GLSL demos constrained to 512 characters
- covers isometric projection setup, smooth minimum operations, and various domain warping techniques for procedural generation

![](../../assets/5b2d72facfde03b6.jpg)


- presentation covering improvements to Unreal Engine’s GPU profiler
- discusses the redesigned RHI submission pipeline architecture and implementation
- shows how to leverage these tools for performance analysis, optimization and crash debugging

![](../../assets/5b3729ffd9234032.png)


- video tutorial on techniques to reduce tiling artifacts in terrain textures
- demonstrates methods to break up repetitive patterns in large-scale terrain rendering
- part of an ongoing series on terrain shader development

![](../../assets/e583c983960e94dc.png)

Thanks to [Leonardo Etcheverry](https://www.linkedin.com/in/leonardoetcheverry/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.