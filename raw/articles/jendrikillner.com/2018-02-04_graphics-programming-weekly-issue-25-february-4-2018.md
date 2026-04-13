---
title: Graphics Programming weekly - Issue 25 — February 4, 2018
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-25/
author: Jendrik Illner
published: '2018-02-04'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

[Optimized Swapchain in Vulkan](https://timothylottes.github.io/20180202.html) [[wayback-archive]](http://web.archive.org/web/20180203060107/https://timothylottes.github.io/20180202.html)

- discussion of different approaches, overview of strengths and weaknesses
- recommends splitting command buffers into two groups
- pre-acquire (everything that doesn’t write into the swapchain)
- post-acquire (everything that writes into the swapchain)

- allows better GPU utilization, execution of pre-acquire workload doesn’t need to stall waiting for the present

[Optimized Swapchain in Vulkan II](https://timothylottes.github.io/20180203.html) [[wayback-archive]](https://web.archive.org/web/20180205004221/https://timothylottes.github.io/20180203.html)

- how to reduce input -> present latency further
- theoretical model to find a better method for dynamically adaptive workloads while minimizing input latency

[A “Bind Once” Approach to Uniform Data](http://kylehalladay.com/blog/tutorial/vulkan/2018/02/05/Bind-Once-Uniform-Data-Vulkan.html) [[wayback-archive]](https://web.archive.org/web/20180205000102/http://kylehalladay.com/blog/tutorial/vulkan/2018/02/05/Bind-Once-Uniform-Data-Vulkan.html)

- how to use a single descriptor set for all uniform data
- uses a single uniform buffer object
- with fixed size uniform blocks, indexed using a per object push constant

[Thoughts on Skinning and LDS](https://turanszkij.wordpress.com/2018/02/03/thoughts-on-skinning-and-lds/) [[wayback-archive]](https://web.archive.org/web/20180205002142/https://turanszkij.wordpress.com/2018/02/03/thoughts-on-skinning-and-lds/)

- each thread loads one skinning matrix into LDS (local data share)
- all further loads of skinning matrices are done from LDS instead
- discussion of LDS limits for thread occupancy

[Unity and Unreal Engine: Real-time Rendering VS Traditional 3DCG Rendering Approach](http://cgicoffee.com/blog/2018/01/unity-real-time-rendering-vs-offline-cgi) [[wayback-archive]](https://web.archive.org/web/20180202195729/http://cgicoffee.com/blog/2018/01/unity-real-time-rendering-vs-offline-cgi)

- show what rendering techniques are available in unity / unreal
- how engines can be integrated into the art pipeline
- and be used to render the final movie

- full range of Disney’s principled BSDF for physically-based rendering
- Global illumination
- new postprocessing options
- gpu based particles

[2D Reflective Water Shader in Unity](https://lindseyreidblog.wordpress.com/2018/01/31/2d-reflective-water-shader-in-unity/) [[wayback-archive]](https://web.archive.org/web/20180202195957/https://lindseyreidblog.wordpress.com/2018/01/31/2d-reflective-water-shader-in-unity/)

- how the water reflection effect was setup in The Endless River (2018 Global Game Jam)
- using a second camera to render the scene
- shader effect that uses noise to offset the vertex position to create the movement in the water

[Scriptable Render Pipeline Overview](https://blogs.unity3d.com/2018/01/31/srp-overview/) [[wayback-archive]](https://web.archive.org/web/20180202205816/https://blogs.unity3d.com/2018/01/31/srp-overview/)

- short overview of the concepts and how to cull and render opaque objects using the scriptable render pipeline

[What the Heck is Blue Noise?](https://blog.demofox.org/2018/01/30/what-the-heck-is-blue-noise/amp/) [[wayback-archive]](https://web.archive.org/web/20180205015353/https://blog.demofox.org/2018/01/30/what-the-heck-is-blue-noise/amp/)

- what are the characteristics of blue noise
- more evenly distributed samples then white noise
- allows fewer samples to cover more space
- helps to reduce aliasing when compared to grid samples

[Portable Graphics Abstraction in Rust](https://fosdem.org/2018/schedule/event/rust_vulkan_gfx_rs/) [[wayback-archive]](https://web.archive.org/web/20180205005929/https://fosdem.org/2018/schedule/event/rust_vulkan_gfx_rs/)

- the slides are missing the .pdf extension (rename them)
- single RUST API with many backends (D3D12, vulkan, metal, … )
- aim is to implement the vulkan portability layer on top of the hardware abstraction layer

[THE AMD LINUX GRAPHICS STACK – 2018 EDITION](https://fosdem.org/2018/schedule/event/amd_graphics/attachments/slides/2251/export/events/attachments/amd_graphics/slides/2251/fosdem2018_amdstack.pdf) [[wayback-archive]](https://web.archive.org/web/20180205010016/https://fosdem.org/2018/schedule/event/amd_graphics/attachments/slides/2251/export/events/attachments/amd_graphics/slides/2251/fosdem2018_amdstack.pdf)

- overview of the AMD open source driver for linux
- architecture of the platform abstraction layer (PAL)