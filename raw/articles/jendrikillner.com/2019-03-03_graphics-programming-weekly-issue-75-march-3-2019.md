---
title: Graphics Programming weekly - Issue 75 — March 3, 2019
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-75/
author: Jendrik Illner
published: '2019-03-03'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

Missed the content for Feburary? Don’t worry. The summary is now availbale on my patreon: [https://www.patreon.com/jendrikillner](https://www.patreon.com/jendrikillner)

- the chapter describes the hybrid rendering pipeline used in the PICA PICA demo
- uses a mix of rasterization and raytracing techniques to generate the final image
- talks about opaque and transparent shadows, reflections, ambient occlusion, transparency, translucency, and GI techniques

![](../../assets/c8b40d9d50748f10.png)


- Ray Tracing Gems is now available as open access book
- the whole book is available as single pdf, but individual chapters can be downloaded too

![](../../assets/ce161faf579f9625.jpg)


- presents a method to distribute sampling points within a triangle taking advantage of sub-triangles to guide the distribution
- able to reduce variance in the test scene by 2.17x

![](../../assets/5cc50579a3e205a8.png)

- collection of different sampling patterns
- explains the patterns and the characteristic of each
- provides C++ implementations

![](../../assets/5dc723bd32ca1f46.png)


- presents a new algorithm that allows to efficiently and incrementally generate stratified sample points

![](../../assets/753b6e5dd7d5d46f.png)


- shows how to implement a fluid like movement inside an object, tri-planar mapping and a animated waterfall shader using the Unity Shader Graph

![](../../assets/52b00d3cfe48bdb7.png)

- shows how to implement halftone toon shading with Unity
- a technique that uses a binary lighting style that is modified by sampling screenspace signed distance fields to customize the edge between lit and unlit area

![](../../assets/893ede1ac9223566.png)

- documents the experiments with HDR support using all 3 different hardware vendors
- shows what HDR information is reported from DXGI and compares against manufacture APIs
- all vendors seem to indicate very different information about the same monitor connected

![](../../assets/5ee1ed6c06fc58eb.png)


- presents how FreeSync2 supports HDR and variable refresh rate
- explains what variable refresh is and what is required to use it
- FreeSync HDR allows the game to collect capabilities from the monitor to adjust the tone mapping accordingly
- shows how to use the AMD library to create and request the device

![](../../assets/c2d7db60f44abc29.jpg)


- shows the method used to abstract pixel formats between OpenGL and Vulkan using an external enum format
- using C++ preprocessor to provide abstraction and testing support

![](../../assets/d9974e4e085cfeed.png)

- explains the design of the new Unity batching system
- designed to enable better matching in situations where many materials are used, but they are using a small number of shader variations

![](../../assets/74e02069931d694e.jpg)

Thanks to Steven Cannavan [@PedanticCoder](https://twitter.com/pedanticcoder) for support of this series.

You would like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.