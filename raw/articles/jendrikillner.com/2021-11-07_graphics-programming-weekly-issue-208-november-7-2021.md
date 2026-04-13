---
title: Graphics Programming weekly - Issue 208 - November 7, 2021
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-208/
author: Jendrik Illner
published: '2021-11-07'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- summary of Occlulus Quest 2 Application SpaceWarp technology
- technology that allows an application to render at half of the target frame rate and “upscale” to the target frame rate
- uses the application provided depth, image buffers, and motion vectors to generate in-between frames

![](../../assets/3438c5f5a5b64584.png)


- the Unity tutorial shows how to sample shadow maps and implement an edge detection filter
- extending the concepts to show how to apply outline shadows

![](../../assets/cfc1d7d93f40394c.jpg)


- the article explains how to implement a portal look into a separate world using stencil buffers for filtering
- shows why the technique was used and how rendering passes have been structured
- additionally covers other the aspects of the demo, such as the volumetric fog and candles

![](../../assets/d1b9c66eb4b1be4e.jpg)


- weekly round-up of tweets from a large variety of technical art and VFX topics

![](../../assets/0795999b457b3a47.png)


- the article presents the details of the D3D12 binding model and discusses the differences to Vulkan
- presents a detailed look at all the possible binding possibilities
- discussing problems, limitations, and how it maps to hardware

![](../../assets/c9aeb1ebd89bc70f.png)


- the article presents how constructor like functionality can be implemented in DXC HLSL
- relies on variadic macros support in the compiler frontend

![](../../assets/8cb9979e24497467.jpg)


- class in introduction to computer graphic series focusing on shadows
- explains the fundamental of shadow casting and presents practical implementation notes that are required for correct implementations
- covers ray tracing and rasterization based implementations
- shows the logic required for reflections and the derivations from the rendering equation
- additionally covers a small discussion of the different ray types, names, and usages

![](../../assets/0e0c2f20c9ae8e97.png)


- the video tutorial explains how to implement metaball rendering
- presents how to approach the approach to the problem and derive the final marching square solution
- focusing on how to transform a problem into solvable sub-problems

![](../../assets/f28627dd01eb050d.png)


- the video for the SIGGRAPH 2021 presentation about UE5 Nanite has been released
- will explain how the mesh-based data structure is built, streamed, decompressed, culled, rasterized, and shaded

![](../../assets/c4a6c967ce5e0008.png)


- Vulkan extension that allows the use of render passes in Vulkan using a D3D12 style objectless model
- already being reported as supported on first Nvidia drivers

![](../../assets/eaad27f109c1e915.jpg)


- video tutorial explains the concepts of spotlights and develops a mathematical model to describe the effect
- presents how to implement these concepts using GLSL and OpenGL

![](../../assets/899f3621578f7203.png)

Thanks to [Sondre Kongsgård](https://github.com/kongsgard) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.