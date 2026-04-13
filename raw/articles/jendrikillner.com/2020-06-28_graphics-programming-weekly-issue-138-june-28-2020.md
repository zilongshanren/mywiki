---
title: Graphics Programming weekly - Issue 138 — June 28, 2020
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-138/
author: Jendrik Illner
published: '2020-06-28'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the Metal shader API now supports function pointers
- the talk provides an overview of the compilation models and performance considerations
- function tables can be passed via argument buffers t the GPU

![](../../assets/f62008ff846e1bb6.png)


- the Unity tutorial explains how to implement a moving scanline post-processing effect

![](../../assets/81f5e0a6813c013f.png)

- the video provides an overview of the D3D12 frame-level profiler
- walkthrough of an example capture of Wolfenstein scene and uses it to explain how to use it to identify performance issues

![](../../assets/b9e5999227c941a0.png)

- the article explains several different methods that can be used to manage shader constant data
- provides a brief overview of each technique and compares performance on Mali GPUs

![](../../assets/58ad3f396a2792f2.jpg)


- the article explains a method that stores shader instructions encoded into a texture and uses a runtime shader to interpret the data
- shows an experiment what happens if the texture is filled with random information

![](../../assets/64775bd93cd7d069.png)


- the program for the online conference taking place this week
- all videos are available on youtube and linked from this program

![](../../assets/d6fe3fa268f0ddcd.png)

- a twitter thread that lists new features Metal API features and provides links to documentation for each topic
- including Programmable Blending, Indirect Command Buffers for Compute and many more

![](../../assets/d4acc3c25cc621d7.png)


- the GDC talk discusses the voxel-based lighting and shadow system
- how to handle performance vs. quality tradeoffs in algorithms
- uses MSAA to increase the effective resolution on shadow maps on higher-end devices
- how to implement gaussian blur efficiently with async compute
- presents shader optimizations for PowerVR hardware

![](../../assets/9cfe3246b675f62a.png)


Foundry are looking for a seasoned software engineer specialising in Real-Time Rendering to join our existing team of rendering experts working on rendering technologies across our portfolio. We’re looking for a self-motivated developer with strong C++ and GPU graphics programming skills. Experience in software development lifecycle and knowledge of software engineering best practices are also required. As a Principal Software Engineer, you will help to ensure the quality, scalability, and extensibility of the code that we’re writing.

![](../../assets/6172b637eae5ba5f.png)


- the article presents a frame breakdown of the PC version of Red Dead Redemption 2
- covering g-buffer breakdown, environment map filtering, shadow pipeline, and more supporting systems

![](../../assets/f5e8e55fd6443222.jpg)


- NVidia driver update adds support for DXR 1.1, VRS Tier 2, mesh shaders and sampler feedback
- additionally now supports Vulkan 1.2

![](../../assets/0509ee037bec5538.jpg)


- a video from WWDC 20 provides an overview of the GPU pipeline, what hardware counters are available and how to use them understand application performance bottlenecks

![](../../assets/430a166aff7ed2f9.png)


- video from WWDC explains the basic building blocks of the Metal ray tracing API and how to support more complex materials

![](../../assets/a4e563137b4c082c.png)

- the article provides an overview of several problematic mesh characteristics that cause an issue for ray tracing and how to resolve them

![](../../assets/23f2cb09e16136e9.png)

Thanks to [Cliff Owen](http://swiftcreekgames.com) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.