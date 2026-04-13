---
title: Graphics Programming weekly - Issue 56 — September 30, 2018
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-56/
author: Jendrik Illner
published: '2018-09-30'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- explains what variable rate shading is and what use cases it enables
- a control texture allows varying of the shading rate on a 16x16 pixel grid

![](../../assets/ae4f5953e54a628b.png)


- explains the recent developments in VR headsets and how Turing offers new hardware solutions
- extensions that allow rendering up to 4 different views, with view-dependent attributes using a single invocation

![](../../assets/26533842ef47dcb8.png)


- a new encoding method for Spherical Gaussians that improves quality from previous encoding methods

![](../../assets/108f19f7dc66469b.png)


- presents a high-level overview of how to implement interior mapping
- comments have much information about the timeline of games that used similar techniques

![](../../assets/0c96193793455884.jpg)


- discusses a technique to generate instanced geometry procedurally on the GPU using OpenGL compute shaders
- aimed at filling vast streaming worlds that are broken down into tiles

![](../../assets/7ecf129a5a59e4a0.png)


- new stream coding series about the creation of a Vulkan renderer from scratch
- the first two episodes implement rendering of a single triangle on screen

![](../../assets/5245b6154b56407e.png)

- pre-print of an article that will appear in GPU Zen 2
- implements adaptive tessellation using OpenGL 4.5 compute shaders
- source code:
[https://github.com/jadkhoury/TessellationDemo](https://github.com/jadkhoury/TessellationDemo)

![](../../assets/64aba96109ad2d3e.png)


- Twitter thread discussing Raw vs. Typed buffer performance on Claybook
- suggest using raw buffers if supported

![](../../assets/8c0fed3e8f21ec1d.png)


- overview of new features included in CUDA 10
- Multi-Precision Tensor Cores are exposed on Turing
- CUDA Graphs allow the specification and recording of an execution graph that can be executed multiple times, this reduces overhead and allows the compiler to apply further optimizations
- interoperability with Vulkan and D3D12 is supported

![](../../assets/9a2e5efcfed49963.png)



- extends the Metal raytracer with obj model loading
- a simple diffuse BRDF implementation, including frame accumulation and shadows
- provides a Mitsuba test scene

![](../../assets/b64266824bd90c81.png)


- walkthrough of the geometry pipeline on current GPU architectures and how mesh shaders fit into it
- description of an upgrade path to mesh shaders
- look at possibilities of future use cases


![](../../assets/300c4b99dbc4f947.png)


- summary of resources for graphics programmers to study and keep up-to-date with the graphics programming community


- a tutorial that shows how to implement a custom rendering pipeline in Unity
- implements skybox rendering, culling filtering, sorting and rendering of unlit objects
- how to improve memory usage and better integration with the Unity frame debugger

![](../../assets/fba96468c6be8f37.jpg)


- Unreal released the tech talks from SIGGRAPH 2018
- Virtual Production in Unreal Engine 4.20, Mixed Reality Production with Unreal Engine, Fortnite: Advancing the Animation Pipeline, Real-Time Motion Capture in Unreal Engine

![](../../assets/d86a1d6f110fc241.jpg)


If you are enjoying the series and getting value from it, please consider supporting this blog.

[Support this blog](https://donorbox.org/jendrikillner)