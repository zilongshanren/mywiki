---
title: Graphics Programming weekly - Issue 317 - December 10th, 2023
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-317/
author: Jendrik Illner
published: '2023-12-10'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the blog presents a walkthrough of the author’s R&D process when approaching the issue of generation of a scene approximation
- shows how to analyze the constraints, develop a high-level intuition for the problem, and use this to explore the problem space
- discusses the different solutions’ pros & cons and shows how to start prototyping and iterating through the process

![](../../assets/b0c931ee542106c6.png)


- the blog post provides an overview of GPU programming concepts for non-graphics programmers
- discusses GPU architecture, how to author shaders, how to read/write data, and basics of synchronization
- For example, d3d11 code for an image converter is provided

![](../../assets/106d937fe2682240.png)


- the research paper presents the performance impact of different vertex clustering (meshlets) on the efficiency of mesh shaders
- discusses hardware design/limitations that affect considerations when deciding on cluster sizes
- discusses different algorithms, providing an overview of the technique, implementation considerations, as well as performance differences
- source code for the meshlet generation is provided

![](../../assets/d61257871f07da7f.png)


- the presentation shows the complexity of debugging issues that cause crashes that originate from GPU issues
- provides an overview of available techniques and tools and how to combine them to track down issues
- explains the steps required to track down example crashes from The Witcher

![](../../assets/cc62e37bdfaec590.png)


- a small website that allows the authoring of GLSL shaders and running them on a virtual “The Sphere” located in Las Vegas
- contains a couple of examples as starting points

![](../../assets/60403867bd2bc573.png)


- the article provides best practices to follow when comparing WebGL and WebGPU workloads
- It presents how to verify the underlying API, output configuration, blend modes, and other aspects that can affect performance
- additionally presents how to report issues after confirming the aspects are identical

![](../../assets/c49877064c24799d.png)


- the video provides an explanation of techniques used by rendering systems to reduce the number of objects that need to be drawn to the screen
- shows how frustum culling is only the first step, expand upon the idea by introducing occlusion culling
- explains how to use the depth buffer to improve culling further and take advantage of temporal information to further enhance culling results

![](../../assets/8e4d5d0604fb9d70.png)


- brief example blog post that presents how it’s possible to use DXVK to build a native Linux elf that uses the D3D11 API
- shows how to integrate the necessary steps into Cmake with a SDL based application

![](../../assets/174e6c7c2210df4a.png)


- the video tutorial shows how to move computations from a pixel shader into a vertex shader
- presents two examples and uses them to show the change in visual results when moving from pixel to vertex shading frequency
- code examples are shown in unity and unreal visual scripting

![](../../assets/320769f2a4d5dac1.png)


- the blog post shows the release of the new version of the AMD GPU profiler
- presents the updated UI and how divergence raytracing pipelines can be visualized better

![](../../assets/c2ac87d9eef6eaf2.png)


- AMD released a sample for DirectStorage that was presented during GDC 2023
- the code shows how to use the API and how to compress assets to be able to take advantage of the API patterns

![](../../assets/699a59aa803c2e6d.png)

Thanks to [Eric Haines](http://erichaines.com/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.