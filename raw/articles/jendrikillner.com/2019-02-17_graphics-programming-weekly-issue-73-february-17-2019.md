---
title: Graphics Programming weekly - Issue 73 — February 17, 2019
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-73/
author: Jendrik Illner
published: '2019-02-17'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

This series can now be supported on [Patreon](https://www.patreon.com/jendrikillner).
Vote on the roadmap and monthly summaries for December and January are available as reward tier.

- chapter from the
[Ray Tracing Gems](http://www.realtimerendering.com/raytracinggems/)book - describes the real-time GI preview system developed for the Frostbite engine, runs on the GPU asynchronously to the editor
- uses an irradiance cache light map approach with denoising applied
- presents performance and results of different acceleration techniques

![](../../assets/e7005b25756dd1ea.png)


- shows the frame breakdown of Shadow Fight 3
- rendering approach designed to reduce the number of draw calls
- explains how the rendering system was designed to take advantage of the game design constraints to find very cheap solutions for lighting, shadows, and reflections

![](../../assets/aaa6a7740884daa7.png)

- presents performance optimizations done for the 2D rendering system
- reducing overdraw for blended objects
- discussion of texture compression formats for detailed 2D pixel art
- using
[YCoCg-DXT compression](https://www.nvidia.com/object/real-time-ycocg-dxt-compression.html)to split luma and chrominance - requires two textures instead of 1 but still a performance win for the game

![](../../assets/c83524458854f3b7.png)

- shows how to set up full-screen quad geometry data so that attribute interpolation can be used to generate the camera rays in a vertex and pixel shader with few instructions

![](../../assets/f882621dcc199751.png)

- card deck that introduces visual shapes and GLSL code required to create them
- combined with
[The Book of Shaders](https://thebookofshaders.com)(by the same author) it provides a good starting point for artistic shader projects

![](../../assets/d7b65c27ab9ba65a.png)

- presents a brief look at the performance of emulating a custom command buffer format on top of OpenGL
- notices a 7% overhead from the command buffer parsing

![](../../assets/a417475a0b733709.png)

- explains how to create a pulsating vertex effect using Unity Shader Graph and the lightweight rendering pipeline
- shows how to set up the shader node graph and control parameters it from C# scripts

![](../../assets/78ca8235e56841a6.png)

- shows how debug compute shaders when using BGFX
- a brief introduction into what is necessary to compile the project
- explains how to compile shaders so that debug information is available and can be used with RenderDoc and the Visual Studio Graphics Debugger

![](../../assets/e180cd7468532c24.jpg)

- open-source AMD Linux driver adds support to use async compute to cull primitives before the vertex shader stage

![](../../assets/05ebe6b259ec86d7.jpg)

- added support for ray and path tracing for the D3D12 backend
- low-level abstractions and high levels features have been implemented
- includes GI path-tracer to generate reference images directly in the editor
- preview for render graph API

![](../../assets/3697e0b74222d9d4.png)

![](../../assets/16b7ee866fe920ce.png)


- list of Unreal events/talks/presentations that will take place at GDC

![](../../assets/27088486c95c3fd8.jpg)

- presents a brief history of the development of WebGL and it’s adoption

![](../../assets/583e6a385c50fc7d.jpg)

- presents the equations necessary to express point- and directional lights when only area lights are supported

Thanks to Angel Ortiz [@aortizelguero](https://twitter.com/aortizelguero) for support of this series.

You would like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.