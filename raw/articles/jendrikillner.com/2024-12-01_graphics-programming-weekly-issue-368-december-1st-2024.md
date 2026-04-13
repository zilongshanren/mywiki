---
title: Graphics Programming weekly - Issue 368 - December 1st, 2024
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-368/
author: Jendrik Illner
published: '2024-12-01'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article provides a very detailed look at how a frame in Detroit Become Human is being drawn
- presents insights into how the shading pipeline is implemented, details into implementation for the various resource passes, vertex formats, interactions with animations, effects implementation, etc
- additionally shows a flow graph of how a full frame is structured with images of the resources involved in each pass

![](../../assets/527b2d022ad16a7a.png)


- the example project presents an example of how to use Slang with WebGPU
- shows how to use CMake integration to compile shaders from slang to WGSL (WebGPU shading language)
- additionally shows how to use the reflection API to generate binding helpers

![](../../assets/68775d0331524932.png)


- In the working document, Timothy Lottes records and suggests solutions for GPU programming issues in a compute shader context
- covers many problematic areas, from performance hints over shader compiler improvements, caching related, buffer access patterns, and much more
- provides example cases that offer insights into current shortcomings, performance issues, and shader compiler bugs

![](../../assets/8623d2efae7823ba.png)


- the article presents how to use RustGPU to compile a compute kernel
- discusses the implementation details and interactions with the ecosystem
- additionally presents how RustGPU enables shader logic to be run on the CPU

![](../../assets/236188022f840bc9.png)


- the article discusses the efficient implementation of Sparse Voxel Octrees
- presents how to build the required tree structures and traverse the created trees
- additionally provides advice to improve debuggability, performance, and robustness of the initial implementation

![](../../assets/f1432f4fada87738.png)


- The article presents the new Fragment Pre-pass hardware implementation available in upcoming Arm GPUs
- explains how the technique works, what it enables, and what are the limitations
- additionally, it discusses best practices for performance and shows some performance numbers

![](../../assets/9c1caa06b9e0509e.png)


- My list of recommendations for books
- Covering Computer graphics, engine design, algorithms, collision detection, as well as knowledge management
- contains resources for beginners as well as advanced programmers

![](../../assets/a0c70814bff40659.jpg)


- A summary of the chapter Differentiable Graphics with Slang.D for Appearance-Based Optimization included in GPU Zen 3
- the article focuses on the practical usage of stochastic gradient descent and optimization from beginning to a working minification system for materials

![](../../assets/379fef96d7e0eb87.jpg)


- the article presents insights into how to upscale retro pixel art games for higher resolutions than the source material
- The suggested solution is using nearest for vertical and linear for horizontal

![](../../assets/904667e035256cb8.png)


- the Vulkan code example presents how to use various modern Vulkan concepts to create compact sample applications
- presents how to use descriptor management, specialization constants, timeline semaphores, ImGui integration, etc.

![](../../assets/25784ccc141be247.png)

Thanks to [Aras Pranckevičius](https://aras-p.info/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.