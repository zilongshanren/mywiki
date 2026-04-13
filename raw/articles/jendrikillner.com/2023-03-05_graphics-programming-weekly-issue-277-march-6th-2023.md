---
title: Graphics Programming weekly - Issue 277 - March 6th, 2023
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-277/
author: Jendrik Illner
published: '2023-03-05'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article continues the series on float compression topics
- presents how to optimize the process by redesigning the system to take advantage of SIMD instruction sets
- shows how much of a performance difference the usage can make

![](../../assets/62fd87bd6716200c.png)


- new release of PIX contains a vast list of new developments
- some examples are RayGen debugging, the ability to show selected draw objects, pix capture diffs, improved memory allocation view, and much more

![](../../assets/896981af3204357c.png)


- the article explains the alignment requirements of buffer loads from VK_KHR_buffer_device_address
- provides a walkthrough of the generated SPIR-V and explains why the issue occurs by explaining the spec requirements

![](../../assets/bca8dc6890ccb265.png)


- the presentation covers a real-time cluster-based path-tracing renderer
- discusses how the architecture was designed to allow linearly scaling with the number of GPUs

![](../../assets/1175fda5c16e632c.png)


- the video tutorial presents a simple lighting model that uses sprites to define light effects
- this is done by defining lights as one render target and combining it with the base world
- implementation using Defold is presented (using GLSL shaders)

![](../../assets/ab43313915ae4edc.png)


- the paper explains the experience of transitioning university classes to be taught using Vulkan instead of OpenGL
- discusses difficulties and advantages encountered
- shows how it affects student learning, grades, and project results

![](../../assets/4d6c9f56c932951b.jpg)


- the video discusses the problem of non-uniform constant loads within a single wrap
- shows how to use Nvidia NSight to identify the problem
- discusses in detail how to correlate counters, latency, and instruction traces
- using Structured Buffers instead of Constant Buffers will be able to resolve the problem once identified

![](../../assets/fcc426de7cc8c415.png)


- the paper presents how to use GPU-based techniques to implement LOD construction of point clouds
- discusses the different implementation approaches’ impact on performance and quality

![](../../assets/cf12d172b91de0ba.png)


- the latest part of the video tutorial discusses how to apply lighting to a terrain using OpenGL
- discusses standard diffuse lighting and Slope Lighting
- provides a high-level overview of each technique and discusses the implementation

![](../../assets/ac7c51fc2ca42200.png)

Thanks to [Matt Pharr](https://pharr.org/matt) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.