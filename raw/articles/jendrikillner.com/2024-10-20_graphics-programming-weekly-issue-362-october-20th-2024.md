---
title: Graphics Programming weekly - Issue 362 - October 20th, 2024
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-362/
author: Jendrik Illner
published: '2024-10-20'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the video continues meshlet implementation and looks at task shader performance on AMD hardware
- starts with an overview of the technique implementation and presents the performance problem encountered using the AMD profiler
- explains how the driver implements task shaders and what causes the performance issue by patching the Linux drivers
- From there, implement a solution that uses compute shaders to cull meshlets instead of using task shaders
- presents performance and memory comparison against the native task shader solution

![](../../assets/2b018532784796e4.png)


- the document explains how vkd3d-proton decides to emulate Vulkan Workgraphs using ExecuteIndirect
- discusses different trade-offs and design decisions made
- presents how the implementation compares against native implementations on both Nvidia and AMD
- many workloads are currently more efficient using this emulation code path than the native driver version


- the article describes how to use the native Metal rendering API for Apple Vision devices
- explains how to interact with the OS for Variable Rate Rasterization based on eye positions, interact with projection matrix
- shows different techniques exposed to render meshes to the two-eye views
- presents how to structure the rendering frame architecture to reduce latency

![](../../assets/c7921e4512fc073a.png)


- the article announces the release of Work Graphs as experimental Vulkan extensions
- provides links to the headers, spec, and code samples, as well as compiler support
- additionally provides a list of current limitations

![](../../assets/dfc82468ccee64c4.jpg)


- the article introduces the new features in Reshape, a tool for instrumentation of GPU operations with instruction level validation of potentially undefined behavior
- explains in detail what AMD Waterfall’ing is, how the tool can detect NonUniformResourceIndex usage
- updates to per-byte and pixel resource usage, as well as placed resource initialization

![](../../assets/4cfa3a5343751885.png)


- the blog post presents two mathematical methods to scale points along a direction
- the first method uses matrix operations, and the second uses dot products

![](../../assets/bd9913ba732611ba.png)


- the tutorial series on Vulkan continues by implementing Graphics Pipeline objects
- presents the C++ code changes and Vulkan changes required
- closes with a first triangle being drawn to the screen

![](../../assets/ff8c2185441301ca.png)


- the video provides a comparison of different upscaling techniques for Ratchet and Clank Rift Apart
- tries to match the PC and PS5 Pro rendering quality as closely as possible
- compares the PS5 Pro upscaler technique against the AMD and Nvidia upscalers on PC

![](../../assets/3c5b5df2e644db2e.png)

Thanks to [Eric Haines](http://erichaines.com/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.