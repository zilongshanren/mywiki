---
title: Graphics Programming weekly - Issue 318 - December 17th, 2023
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-318/
author: Jendrik Illner
published: '2023-12-17'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the blog post aims to introduce and explain the ReSTIR technique with a focus on implementation and intuition instead of the underlying theory
- shows how to start with a first implementation and expand it to implement shadows
- additionally shows how to take advantage of temporal and spatial data to reduce noise

![](../../assets/08312fb88c590515.png)


- the article presents a breakdown of the primary render passes of the Knockout City frame
- provides a high-level overview of the rendering techniques used, what existing techniques they are based on, and how they modified the techniques to fit the requirements of the game

![](../../assets/64bd0a2b6b7e8f5a.png)


- the blog post collects advice on how to achieve the most stable presentation results when using DXGI
- presents what flags to set, how to size the queues, and how to make sure the results stay consistent after window/resolution resizes

![](../../assets/49ec979edfeee4dd.jpg)


- the blog post presents an overview of the FSR3 SDK improvements
- shows the debug display modes to help during implementation
- additionally shows how it’s possible to run workloads on one queue to make initial implementation easier

![](../../assets/4a514c53cc39c64f.png)


- the article discusses several ways to query the driver version and how to interpret the results
- presents how to query the information with AMD, and Nvidia-specific API
- and the API standard way exposed by D3D12 and Vulkan


- the interview between DigitialFoundry and some of the developers of the developers from Massive provides insights into the implementation of the game
- discussing raytracing, GI, GPU rendering pipeline, and many more topics
- also provides into the CPU side structure as well as PSO management

![](../../assets/a9c80c07cf9011e0.jpg)


- the article presents how to use Simplygon to generate micro-meshes (base structure + displacement information)
- shows examples of what kind of results can be expected from different settings and how it affects memory usage and quality
- presents how the way a model has been created can affect the base resolution vs. tesselation amount to achieve high-quality results

![](../../assets/22ac1ac2431b8e33.png)


- the blog provides an introduction to fluid dynamics and rendering
- the implementation is explained with the growing sophistication of the simulation
- an interactive WebGL demo of each stage is provided
- closes with how to apply temperature to color space conversion to enable a first completed fire simulation

![](../../assets/070fd7cd1aa06a1b.png)


- the video tutorial explains how to sample textures from a vertex shader
- explaining the quality difference and how the mesh vertex distribution and the texture content can significantly affect the quality of the result
- additionally presents the different strategies that are available for the selection of varying texture MIP levels

![](../../assets/82c9ae720ba4588a.png)

Thanks to [Jasper Bekkers](https://twitter.com/JasperBekkers/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.