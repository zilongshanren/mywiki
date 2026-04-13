---
title: Graphics Programming weekly - Issue 150 — September 20, 2020
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-150/
author: Jendrik Illner
published: '2020-09-20'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the video tutorial explains how to implement a rust effect on objects that intersect with a water plane
- describes how to calculate the distance between a point and a plane
- implemented using the Godot engine

![](../../assets/d7d172840e5ed001.png)

- the article explains the sorting, rendering layer design for a 2D game
- implemented using Unity
- sorting layers also interact with how the dynamic 2D lights interact with the sprites

![](../../assets/906524bc939f16c4.png)


- the talk provides an overview of WebGPU and provides an overview of the implementation using Rust
- this implementation is used by Firefox
- shows the design considerations for the API, how to use it, and implementation discussions

![](../../assets/ce5ef4e2fcc00d84.png)

- the blog post explains how to implement a simple Toon Lighting shader using the Amplify Shader Editor inside of Unity
- shows how to configure the effect and use the idea to archive different looks

![](../../assets/5382570876e12a23.png)


- the Unity tutorial shows how to generate mesh data on compute shaders and draw them from the GPU without a CPU roundtrip

![](../../assets/054a233c6c037c88.png)

- this guide explains how to use the Vulkan Synchronization Validation layer
- shows what kind of problems it can detect, how to debug these issues, and explain how to understand the messages

![](../../assets/7aed8a187d363c15.png)


- the blog posts explains how PIX for windows captures work
- provides insights into how the focus has shifted from API focused recording to GPU work recording

![](../../assets/0ee2a405a74b9f90.png)

- the article explains how to implement a heat haze screenspace effect for a 2D game using Unity
- implementation is done using Shader Graph
- a video version of the tutorial is available too

![](../../assets/4a7c8f8eafc89a27.png)

- article shows the new Instruction Timing, Theoretical occupancy, and UI improvements in the latest version

![](../../assets/4960a6ce3f1d214f.png)

- new release adds support for NVIDIA Ampere microarchitecture
- support for the Vulkan added to the Shader Profiler (including raytracing)

![](../../assets/4ceaf4023cc75e12.png)

- Vulkan validation layer has been updated to include additional and improved validation messages

![](../../assets/4afa3cdfba6caf1a.jpg)

- the paper presents a physically-based model for the realtime rendering of sparkling materials
- the implementation uses a pre-computed BRDF dictionary of ~390KB size
- precomputation is independent of smoothness, so runtime variations are possible

![](../../assets/3586b317ddb5f15d.png)

Thanks to [Michael Riegger](https://www.linkedin.com/in/michael-riegger-33b55a11/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.