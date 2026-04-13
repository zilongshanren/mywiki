---
title: Graphics Programming weekly - Issue 346 - June 30th, 2024
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-346/
author: Jendrik Illner
published: '2024-06-30'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the paper introduces a real-time BRDF model addressing diffraction on rough surfaces
- shows the improved realism in Unity over the Cook–Torrance model
- presents a performance comparison against a base Cook–Torrance implementation

![](../../assets/631ba135403e05f0.png)


- the blog post presents how to profile WebGPU applications with Nsight, PIX, and Radeon GPU Profiler
- The presented solution takes advantage of context sharing and dll interception

![](../../assets/86e23a5be198ecea.png)


- the paper presents an approach for incremental re-rendering of scenes
- it formulates image differences as a residual path integral, solved with importance sampling and path mapping
- presents speed-ups over previous methods and independent frame rendering

![](../../assets/d8f8c2b389a19c4d.jpg)


Grinding Gear Games are seeking experienced C++ Gameplay and UI Programmers to join our incredibly talented team. We’re after programmers to help design and implement gameplay and UI elements for Path of Exile using modern C++.

![](../../assets/c0f5d7d121e31f1a.png)


- the conference program for the High-Performance Graphics has been released
- will take place between July 26 to 28 in Denver

![](../../assets/ce9730b8b4fe8a3b.png)


- the video shows an overview of Technical Papers to be presented at SIGGRAPH 2024
- shows a quick showcase of each trailer and a brief summary of the presented approaches

![](../../assets/26281f882f05f086.png)

- the paper presents a method for the efficient extraction of mesh contours
- it proposes a simple, flat data structure that is GPU-friendly and uses patches bounded by normal cones and sphere
- discusses how to generate these patches and improve bounding sphere calculations
- presents a performance comparison against CPU techniques

![](../../assets/9e85ee1481b0d84a.png)


- the next episode of the Vulkan tutorial series presents how to execute work to the GPU
- presents how to clear the image to a fixed color and integrate it with the presentation process

![](../../assets/de482d96a0db9c27.png)


- new video tutorial series that will cover how to generate procedural shapes and patterns from shaders
- implementation is shown using Unity and Unreal Engine
- this video focuses on the reasons why to use the approaches and how to create a pattern with antialiased edges

![](../../assets/91f6eec6bed82341.png)


- the video presents an approach to develop an ASCII art shader approach (converts 3D rendering to text)
- discusses methods, issues of the techniques, improvements and presents results on several different games
- presents how to map the techniques onto a compute shader execution model
- additionally presents other techniques that could be built upon

![](../../assets/73419bf4b1947e4a.png)


- the blog post presents a walkthrough on how to implement a raytracing classification shadow optimization using D3D12 work graphs
- first discuss an overview of the technique
- followed by a presentation on how to express this technique using HLSL and D3D12 work graphs

![](../../assets/64d8d6d12e30d41f.png)

Thanks to [Bruno Opsenica](https://bruop.github.io) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.