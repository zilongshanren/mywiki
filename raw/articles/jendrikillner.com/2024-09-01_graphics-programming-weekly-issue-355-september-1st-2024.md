---
title: Graphics Programming weekly - Issue 355 - September 1st, 2024
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-355/
author: Jendrik Illner
published: '2024-09-01'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the blog post provides an overview of the new VK_KHR_pipeline_binary that allows direct retrieval of binary data associated with individual pipelines
- this extension allows applications to write custom caching, pre-compilation as well as loading mechanisms
- The article explains what the extension allows, how it’s exposed, and considerations when designing a caching system

![](../../assets/2a66208258d59887.png)


- the paper introduces a new method for precomputing indirect lighting into a novel form of Irradiance Volume
- It discusses how two approaches, one neural net and one parametric function based on ReLU fields
- presents performance and memory usage information and presents comparisons against existing solutions
- additionally discusses the limitations of the technique

![](../../assets/241c9abd1dac65b6.png)


- the author presents a discussion of how to apply software rasterizing to the problem of hair rendering
- technique is based on the Frostbite technique from the presentation “Every Strand Counts: Physics and Rendering Behind Frostbite’s Hair”
- discusses the implementation of the steps that make up the technique, such as spline projection, rasterization using edge functions, as well as interpolation information along the strands
- WebGPU demo and implementation is available

![](../../assets/cbafaafd641e87c7.jpg)


General Arcade, a porting and co-development studio that has worked with a wide range of clients, from indies to AAA developers and publishers, including Larian, From Software, Capcom, Devolver Digital, TinyBuild, and others, is seeking a Software Engineer with a rendering emphasis.

This is a great opportunity to work with a passionate engineering team on cutting-edge industry technologies.

![](../../assets/c3ef79290c0765d3.png)


- the blog post describes the reasoning why SDL GPU doesn’t require a single portable high-level shader language
- focuses on the complexity of the shader ecosystem, how different formats are converted and required to be across platforms

![](../../assets/bd716468de0e4b51.png)


- the video explains how to implement a perspective-animated grid with a color gradient
- presents how to implement perspective wrap in UV space
- combines with other nodes to create the effect
- implementation is shown in Unity and Unreal visual shading languages

![](../../assets/ab851ddbc713666d.png)


- SDL GPU abstraction has been merged into the main branch
- provides a D3D11, D3D12, Metal and Vulkan implementation layer

![](../../assets/cf1d27d42fdafa1e.png)


- the article presents the effects of applying ML upscaling algorithms repeatedly to the same image
- compares against the effect of repeatedly scaling an image using a Lanczos filter

![](../../assets/87000c346cf19354.jpg)

Thanks to [Yuwen Wu](http://atyuwen.github.io/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.