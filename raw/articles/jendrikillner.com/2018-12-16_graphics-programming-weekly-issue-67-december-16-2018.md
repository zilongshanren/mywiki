---
title: Graphics Programming weekly - Issue 67 — December 16, 2018
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-67/
author: Jendrik Illner
published: '2018-12-16'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

Thank you everyone for the support in 2018, this is the last post of the series for this year, the next post will be released on January 14, 2019.

I wish you happy holidays and a great start into 2019.

- explains the state management system implemented for the Diligent Engine
- resources states are exposed on D3D12 style semantic for barriers
- allows mixing of automatic and manual explicit state management
- the developer can choose to disable automatic transitions on a per resource basis
- can switch on a per-resource basis at any time during the frame


![](../../assets/e461c61c00bf14d1.png)


- course notes for the Siggraph Asia 2019 course
- presenting the newest developments and techniques used during The Incredibles 2
- talking about Simulation & FX, Rendering & Compositing and Real-time Tools to allow quicker iteration time
- overview of subdivision surface representations for use with OpenSubdiv

![](../../assets/f50d2b7d1f3878c2.png)


- explains the parallax mapping technique used to represent the interiors of buildings as seen through windows
- broken into multiple layers to separate window frames, curtains and interior of the room
- baked separate light texture to allow night time for interiors

![](../../assets/7bb6b8cd81b5213b.jpg)


- explains sparse binding and residency
- sparse binding lifts the requirement that resource memory needs to be fully continuous in memory. Instead, memory is managed with pages that can be mapped at non-continues offsets
- sparse residency lifts the requirement that the complete resource needs to mapped. For example, only parts of a texture atlas could be mapped

![](../../assets/54d93592431cb34c.png)


- describes how the histogram of pixel brightness is collected using a compute shader in The Witcher 3
- the system allows a dynamic weighting of pixels that origin from the sky

![](../../assets/b1fb3683ab7e691e.png)


- explains how to use D3D12 to calculate a histogram of pixel brightness in a compute shader
- shows how to use a per-bin weight to calculate the luminance for the exposure step

![](../../assets/c63beffc06983557.png)


- part two of rasterization implementation article series with C++
- shows how to extend the rasterizer into 3D
- now implements the necessary pipeline to project vertices from object space into clip space for rasterizations
- adds support for depth testing and index buffers

![](../../assets/40a1abeb7775e089.png)


- RenderDoc survey looking to gather information about the user experience, stability, development experience, API and platform coverage
- help to set the direction for future developments

![](../../assets/e2faf755f7b64d24.png)

- presenting an overview of next-generation Intel architecture
- will support adaptive sync, tile-based rendering, coarse pixel shading

![](../../assets/166d4538777a60cb.jpg)


- acceleration structure visualization for DXR (DirectX Raytracing) and Vulkan
- serialize DXR application to a C++ capture is now supported
- added Vulkan pixel history support

![](../../assets/6ae6b45c7a37abc6.png)


- new AMD driver adds support for VK_EXT_inline_uniform_block, VK_KHR_swapchain_mutable_format, VK_EXT_scalar_block_layout and sparse extensions


If you are enjoying the series and getting value from it, please consider supporting this blog.

[Support this blog](https://donorbox.org/jendrikillner)