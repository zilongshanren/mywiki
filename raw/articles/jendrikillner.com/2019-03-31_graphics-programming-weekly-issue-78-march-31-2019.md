---
title: Graphics Programming weekly - Issue 78 — March 31, 2019
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-78/
author: Jendrik Illner
published: '2019-03-31'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

Missed the content for March? Don’t worry. The summary is now availbale on my patreon: [https://www.patreon.com/jendrikillner](https://www.patreon.com/jendrikillner)

- part 3 of tutorial series in building a path tracer in Unity
- shows how to trace a ray against a triangle and extends this by integration of Unity mesh interactions from the scene

![](../../assets/4cad81ae69ff7b6c.jpg)

- new Nsight graphics release adds improved DXR support, D3D12 fence visualization and Vulkan support for the range profiler

![](../../assets/513b0ce4e64758e5.png)

- whitepaper presenting the Autodesk uber surface shader based on the Arnold shading model
- based on ten components that are layered and mixed hierarchical to form the final surface appearance
- defines a “preview” model that simplifies the shading model for real-time use
- shows the effect of the individual components and exposed parameters
- partial Open Shading Language implementation is provided

![](../../assets/ab6463c665fdb742.png)


- presents how to render maps using WebGL
- shows how to convert color maps to elevation
- generate normal maps from a height map
- apply soft shadows, ambient lighting and combine with color map information

![](../../assets/fb97394971ebc44d.png)

- collection of resources aimed at helping beginners get started with graphics programming

- overview of Variable Rate Shading which is starting to become part of the D3D12 API
- will have a two-tier hardware support level
- tier 1: per draw shading rate changes
- tier 2: can vary shading rate within a draw, with a screenspace image or per-primitive

![](../../assets/3bd6ad2299a16c73.png)

- next Windows update will add support for library subobjects
- these allow configuring raytracing pipeline state from HLSL, removing the need for boilerplate C++ code

![](../../assets/640aa29062edb9b4.jpg)

- the author presents his thoughts on the current state of raytracing in games
- where it can bring an advantage, weaknesses and the need for hybrid solutions
- how it might influence art direction

![](../../assets/49f460f59eae174a.png)

- explores a stable filter further
- presents a new test that can be used to validate the filter quality better
- performs experiments to find a filter that is stable and introduces less blurring than the filter discussed in part 1

![](../../assets/d076e3b5188d862c.png)

- ARM released a best practice guide for Vulkan
- consists of runnable samples that show best-practices and shows common performance pitfalls
- on-screen information visualizes the performance impact of different methods

![](../../assets/0a76315a56bc1979.jpg)

- look at the disassembly for parts of the skydome, sun, and stars shader from The Witcher

![](../../assets/4949ce07974980e8.jpg)

- covers overview of color theory, color spaces, and encoding
- presents what problems FreeSync 2 solves and what guidelines it requires hardware manufacturers to follow

![](../../assets/6efff5cdeca91efd.jpg)

- list of best practices for ray tracing
- how to manage the acceleration structure construction and building efficiently
- how to manage pipeline objects, shaders, and resources
- denoisers and memory budget

![](../../assets/edad20477462781a.png)

- occupancy graph is now supported on Turing GPUs too
- Variable Rate Shading is supported

![](../../assets/41e9bf8da7b8e973.png)

- a small article explaining the difference in the viewport coordinate system when using Vulkan compared to OpenGL
- shows how to flip the viewport to match OpenGL convention

![](../../assets/9d53884266fee819.png)

- presents how to precalculate an energy preserving microfacet BRDF with a diffuse-like lobe

![](../../assets/e4175b47d5ea5d6b.png)

- presents the authors’ views on “do”’s “do not”’s for the future use of raytracing in games
- how RTX gives new opportunities and also challenges
- performance vs. quality tradeoffs will still be required, and raytracing will not make this simpler

![](../../assets/6143ee294baee7fe.jpg)

- unreal tech talks from GDC 2019 are available

![](../../assets/59cd6e16dbf62732.jpg)

Thanks to [Warren Moore](http://metalbyexample.com/) for support of this series.

You would like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.