---
title: Graphics Programming weekly - Issue 61 — November 4, 2018
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-61/
author: Jendrik Illner
published: '2018-11-04'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- paper on BRDF measurement which proposes a new parameterization that adapts to the behavior of the material
- able to significantly reduce the number of samples required
- published a new large database of measured BRDFs that have been captured using this technique

![](../../assets/d4885521b2585100.jpg)


- presents an architecture overview of the engine
- render backends are implemented as DLLs that can be reloaded at runtime
- multiple backends can be loaded at the same time
- resource handle system that allows the same resource to point to physical instances on multiple GPUs
- GPU work is recorded into an abstract command stream that is later compiled into API specific format
- render graph system that manages resource transitions, lifetimes, and execution order
- showcase of shader binding model
- using HLSL spaces concept to separate between update frequencies
- explanation how the HLSL resource binding model was emulated with SPIR-V using shader patching


![](../../assets/5d2de5685dbbf7a7.png)


- discusses considerations when designing memory components for use with gfx-hal (rust graphics API abstraction)
- proposes not to use a general purpose allocator but instead to implement simple allocator components and combine them into context-aware allocators on a higher level

![](../../assets/0f94065db211a4d1.png)


- presents a technique for font rendering that operates on coverage instead of visibility
- this allows fonts to remain sharp when moving on the screen and at varying font sizes
- for each pixel in a glyph, a 4x4 sub-sample grid of visibility samples is calculated ahead of time
- explains how to use this coverage mask to implement font rendering
- covering how to sample the coverage mark correctly for axis-aligned font rendering

![](../../assets/475302ab4280c19e.png)


- new PIX version that supports the final DirectX Raytracing API version

![](../../assets/fb8426a495bda485.png)


- full Linux support for Vulkan and OpenGL 4.5
- support for final DirectX Raytracing API and new supports Vulkan extensions such as VK_NV_shading_rate_image, VK_NVX_raytracing

![](../../assets/4bc87883883f26d0.png)


- shows that BC7 encoders produce compression artifacts when the alpha channel is unrelated to the RGB channels
- presents a heuristic to decide what BC7 mode to use on a per-block basis to improve the compression

![](../../assets/2344d077da6036fa.png)


- case study of a performance regression in League of legends
- presents what performance data they collected
- shows what problems they had with the existing data and how a better aggregation of performance data into distinct buckets allows better detection of performance regressions

![](../../assets/08911ce7121d340a.png)


- provides best practices for applications that use the RTX API
- talks about acceleration structure creation and updating
- how to improve memory usage, improve performance and best practices for shader authoring and compiling

![](../../assets/843f34502833b4bc.png)


- presents how to reduce light leaks in a large scale global illumination system
- each geometry is associated with markup information about visibility zones
- GI light data is only applied if two pieces of geometry are in the same visibility zone or are visible through connected portals

![](../../assets/2946f7b91d138b78.png)


- comparison of two libraries to compress SPIR-V shaders SMOL-V MARK-V
- compares for compression ration, decompression speed, and library size
- MARK-V achieve great compression results, but the library has a large memory footprint and is slow at decompressing the data

![](../../assets/dcde2e2465575850.png)


- a tutorial that explains how to create a custom shader for use with the scriptable render pipeline in Unity
- teaches how to interact with constant buffers
- presents what is required for GPU instancing to be supported by a shader and how to pass custom per-material data to the instanced meshes

![](../../assets/d1597e2acdf522be.png)


- mesa gallium driver that implements partial support for OpenGL 2.1, and OpenGL ES 1.1 and 2.0 on top of Vulkan
- talks about why this project was started, and what is and is not supported at this point

![](../../assets/1278827fc54b5a8c.png)


- shows how the lighting system in the 2D game was implemented
- making heavy use of color remapping LUTs
- sprites have normal maps, lights move in 3D space with custom light falloffs for lights moving behind sprites
- discusses how shadows and fog are applied
- presents how a deformation shader is used to simulate wind

![](../../assets/8bfbe0e2ca7bffe7.png)


- optimizing mesh shading pipeline, can now reach >20B triangles/second (input triangles, before cone culling)

![](../../assets/612168173ad95810.png)


- adding per object transformation and depth buffer support
- switched to using multi-draw indirect for classical and mesh shader based pipeline

![](../../assets/02446a3bb58c5ac5.png)


If you are enjoying the series and getting value from it, please consider supporting this blog.

[Support this blog](https://donorbox.org/jendrikillner)