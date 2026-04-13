---
title: Graphics Programming weekly - Issue 255 - October 2nd, 2022
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-255/
author: Jendrik Illner
published: '2022-10-02'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article provides an overview of the implementation underlying AMDs’ FidelityFx screen space reflection technique
- discusses how the decision is made if to trace a screen space ray or to fallback to cubemap reflections
- presents performance optimizations done across the different stages

![](../../assets/1719050b5d59617c.png)


- the video provides an introduction to the AMD raytracing tool
- shows how to use the tools to gather performance information about the raytracing passes
- video explanation of the
[Improving raytracing performance with the Radeon™ Raytracing Analyzer (RRA)](https://gpuopen.com/learn/improving-rt-perf-with-rra/)that was covered in the week[253](https://www.jendrikillner.com/post/graphics-programming-weekly-issue-253/)

![](../../assets/4dcb1a7e4d9d8474.png)


- the article provides a summary of two plots for the existence of gamma space related to CRT and human perception
- presents how the workflows are integrated into Unity and Unreal
- it additionally presents how rendering results are incorrect when done in the wrong space

![](../../assets/3fc84057bbdb88fb.png)


Double Fine Productions is looking for a full time graphics programmer to join its San Francisco based development studio. Having recently shipped the award winning Psychonauts 2, we are looking to expand our graphics and systems programming team to support the development of our future titles.

You will be responsible for developing rendering features, optimizing game performance and memory usage, and building low level systems on PC and Xbox.

Applicants should have a strong preference for working in a highly creative, innovative, and nimble development environment, where collaborating with design, audio, art, animation, tech, and other disciplines is standard.

![](../../assets/27034fe5c580ce80.png)


- the article discusses the RGB and HSV color spaces
- presents how to convert between the two spaces
- it additionally shows how to use the HSV model to implement fullscreen color adjustments effects such as desaturation

![](../../assets/5b0f0ad68fabafc0.png)


- the video presents visual explanations of lerp (linear interpolation)
- takes the knowledge to extend how to visualize and shape the curve for different effects
- presents standard functions and presents different use-cases
- it additionally shows cases where linear interpolation is not enough (camera movement, rotations, ..) and how to resolve them

![](../../assets/a5093e4b38128a7b.png)


- the blog post provides an introduction level guide to using the D3D12 bindless model
- shows how RenderDoc and Nsight show the accessed resources for debugging purposes

![](../../assets/4d2a6a7cecfd106f.png)


- the article presents how to calculate the intersection between axis-aligned rectangles
- extends the methods to cover rotated and more generic polygon shapes
- interactive code samples provided in javascript

![](../../assets/db294ce6f6859bb2.png)


- the video explains how DLSS uses motion vectors and optical flow fields to implement AI Frame Generation
- presents performance and quality comparison
- discusses the upsides and downsides of the new AI frame generation technique

![](../../assets/67eea1aa5194f7fa.png)


- the 2023 Vulkanised conference has been announced for in-person in Munich in February
- organizes are currently looking for speakers for the event

![](../../assets/e2ae7de23b49da64.jpg)


- Intel has released the SDK for the XeSS upscaler
- closed source release that exposes the API for D3D12-based applications

![](../../assets/28f06145fea9870a.png)

Thanks to Stephen Hill for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.