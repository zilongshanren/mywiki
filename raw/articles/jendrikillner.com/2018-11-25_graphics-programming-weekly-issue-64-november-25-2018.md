---
title: Graphics Programming weekly - Issue 64 — November 25, 2018
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-64/
author: Jendrik Illner
published: '2018-11-25'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- a brief overview of the concepts of the ray tracing extension
- started integration with replacing screenspace AO and shadow map implementations
- how to implement ray trace reflections, techniques to reduce noise and optimizations
- best optimization advice is to split ray casting and shading
- export ray hit information from raycasting shader, and shade samples later using a conventional compute shader
- overview of the indirect diffuse voxel solution used in Quantum Break and how ray tracing can be used to improve the results

![](../../assets/15403e852209aa86.png)


- overview of the Navier-stokes equation, look at each step of the implementation and how it was integrated into the engine
- scrollable grid, only run simulation near the player character, a static map for the rest of the world
- obstacle injection uses capsule vs. water plane collision checks
- algae implementation uses virtual particles that convert density to particles, applies simulations, and turns back to densities

![](../../assets/b26ce651b558b5da.png)


- Nvidia sample for mesh shaders using Vulkan and OpenGL
- presents performance comparison for different meshes and a varying number of vertex attributes

![](../../assets/09a95a40bf8ba3a3.png)


- explains the GPU programming model, how shaders are executed
- showcases the differences between CPU and GPU design

![](../../assets/0c682f9d00f2571c.png)

- explains how to implement a shader that simulates a foggy window effect applied to a plane in 3D space
- allows the user to clean parts of the window. Foggy state returns after some time has passed

![](../../assets/9ef1d3bb6327f352.png)


- explains how to integrate the DirectX shader compiler (DXC) into the Visual Studio build system (msbuild)
- integration of dependency tracking
- detecting headers
- shows how to provide a regex to integrate with the Visual Studio error window

![](../../assets/c73912031840a873.png)


- beginner level overview about consideration for modeling techniques related to performance and minimizing z-fighting artifacts

![](../../assets/da088e01ea27cc6d.png)


- article with interactive and live tweakable examples
- presents a technique that allows constant time conversion from a position on or above a sphere to the nearest triangle index using an octahedron subdivision model

![](../../assets/161ba788cd6371ca.png)


If you are enjoying the series and getting value from it, please consider supporting this blog.

[Support this blog](https://donorbox.org/jendrikillner)

- explains how to use new D3D12 API additions to precompile shaders for DirectX raytracing in parallel into a native hardware format

![](../../assets/b07277723b1f64c3.png)


- performance comparison of OpenGL, D3D9, D3D11, and Vulkan in Dota 2

![](../../assets/810ab9a361bd7325.png)

- frame breakdown of an interior scene in Ni No Kuni 2
- uses a light pre-pass architecture
- the cartoon edge line is using FXAA for smoother lines, and the final render result uses SMAA

![](../../assets/d504e934a8d67850.jpg)

- C++ header only implementation to generate 2D blue noise sample points

![](../../assets/59da053fbd913897.png)

- part 1 of the series on writing a software rasterizer in C++
- explains the concept of barycentric coordinates, edge functions and how they are combined to rasterize a 2D triangle

![](../../assets/a91647df8cf515b9.png)


- overview of the synchronization primitives of the Vulkan API
- explains concepts of barriers, access masks, semaphores, and queue transitions

![](../../assets/9444578e4c63846e.png)


- the distinction between memory and execution barrier
- explains render passes including sub-region dependencies
- look at GPU → CPU synchronization

![](../../assets/4c01acea0c5d2229.png)


If you are enjoying the series and getting value from it, please consider supporting this blog.

[Support this blog](https://donorbox.org/jendrikillner)