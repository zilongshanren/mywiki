---
title: Graphics Programming weekly - Issue 309 - October 15th, 2023
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-309/
author: Jendrik Illner
published: '2023-10-15'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the paper introduces a level of detail technique for triangular meshes for use with ray tracing workloads
- proposes a data structure for hierarchically representing triangle meshes, allowing localized decisions for the desired mesh resolution per ray

![](../../assets/9f70e57ec220b5c8.jpg)


- the blog post shows how to implement a scan-line rasterizer using D3D12 work graphs
- presents how to implement the rasterization using D3D12 work graphs, showing the C++ and HLSL implementation
- shows how to split work between GPU threads and how it affects performance

![](../../assets/9d587fcd5772f640.png)


- the article discusses the author’s development of a real-time voxel rendering and authoring system in Unreal Engine
- covers the data structure usage, compute shader implementation as well as issues transition between UE4 and UE5

![](../../assets/718d6c7c33643673.png)


- the blog post discusses advice to help debug issues with GPU workloads
- covers how to track GPU progress, get debugging information from shaders, available tools, etc
- additionally provides a list of steps to follow when tracking down issues

![](../../assets/5d6e6aca05fe9d0f.jpg)


- the article covers how to generate a 4D hypersphere
- discusses multiple generation techniques
- presents how to sample 4D noise uniformly

![](../../assets/bb69db65f5b69fdd.png)


- the article discusses ten implementation details to consider when working on a Dynamic Resolution Scaling (DRS) solution
- covering memory handling, resolution choices, effects on frame timing, debugging advice, as well as UI rendering

![](../../assets/de515743a78b09d2.png)


- the blog post introduces the updated Vulkan documentation website
- it combines the spec, proposals, samples, shader language information, etc., into one place
- the blog post provides the reasoning and an overview of where to find the information

![](../../assets/82c8c87f2b910e06.jpg)


- the video tutorial presents how to implement a material effect that simulates an old LCD screen effect
- the effect combines scan lines, vignette fading, flickering, half-tone shading, and flipbook animations
- implementation is shown in Unreal and Unity Visual Scripting

![](../../assets/e934e5f833b85ae6.png)


- The master thesis provides an overview of the different trade-offs of volume data structures
- introduces a method for storing density data in block-compressed textures combined with deduplicating homogeneous nodes
- shows how this enables efficient flipbook animations

![](../../assets/08534a3c018a34f3.png)

Thanks to [Matt Pharr](https://pharr.org/matt) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.