---
title: Graphics Programming weekly - Issue 55 — September 23, 2018
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-55/
author: Jendrik Illner
published: '2018-09-23'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- new shader stages on Turing that allows the generation of primitives for direct consumption by the rasterizer
- task shader: emits mesh shader workgroups
- allows work on larger clusters, the selection of mesh resolution, …

- mesh shader: generates primitives (index + vertex buffers)
- OpenGL shader implementation that uses the new shader stages to allow culling on a per-cluster basis and generation of efficient mesh data
[video recording](http://on-demand.gputechconf.com/siggraph/2018/video/sig1811-3-christoph-kubisch-mesh-shaders.html)

![](../../assets/3c8a6823928f6a0d.png)


- talks about the challenges of developing for open world games
- covers water rendering, physically based time of day model, nighttime rendering
- lighting, exposure, emissive effects, and tone mapping
- material blending

![](../../assets/0469c092aed5972e.png)


- a new algorithm to compute the intersection point and surface normal of an oriented 3D box without precomputations or spatial data structures
- uses rasterizer pipeline to generate screen-space AABB to limit tests to only potentially visible pixels
- provides GLSL shader implementation

![](../../assets/a4f339bfcd7e56bc.png)

- explains the evolution of the windows graphics driver model from win7 to win10
- how WDDM 2.0 enables the features of D3D12
- differences between D3D12 and Vulkan regarding queue submission design
- D3D12 fences are designed to enable the OS to control command buffer scheduling
- look at Nvidia and AMD hardware details

![](../../assets/c6ac659ceb960eea.png)


- explains optimizations done to the hybrid shadow raytracer
- change to the way the BVH layout is constructed (Surface Area Heuristic) and memory layout changes enable huge speedups (16ms to 0.8ms on the GTX970)

![](../../assets/f5047b85915cbf64.png)

- overview of the new Turing hardware architecture
- description of new hardware features, exposed shader features, and improvements to existing technologies

![](../../assets/3886f30fb730c906.jpg)

- an extensive list of OpenGL and Vulkan extensions that expose the new Turing hardware features
- with short descriptions of each feature

![](../../assets/a78eef928a76ce40.png)

- Vulkan extension that makes it possible to skip parts of command buffers based on the content of a GPU buffer
- the example uses this to pre-generate a single command buffer and controls visibility of mesh parts from the CPU

![](../../assets/9043f5c51123f8fd.png)

- overview of the interior mapping technique
- showcase of different implementations and links to further information

![](../../assets/5bd78539aa4ee810.png)

- discussing of a technique that tries to preserve normal map variation by generation MIPs that preserve the variance in the roughness map
- the comments contain links to further reading about this topic

![](../../assets/cc7d0f3b83b019fe.png)

- comparison of DXC (DirectX Shader Compiler) and FXC shader compiler in regards to performance and functional regressions
- provides a docker file that allows FXC to run successfully

![](../../assets/b79a081e889ef89d.png)

- provides a configuration that allows the DXC compiler to run within docker

- explains the process that enables DXIL shaders to be signed after they have been compiled
- provides code for detecting if a shader has already been signed and how to call the necessary libraries to sign the shader
- provides a command line utility that can be used to sign DXIL shaders

![](../../assets/5bbb4d6c834bd809.png)

- start of a series of posts that will describe the development of a ray tracer using Metal Performance Shaders

![](../../assets/747827eae92a5135.png)

- Khronos released provisional material on the memory model for Vulkan
- including the specification, extensions for SPIR-V, GLSL and conformance tests

![](../../assets/b5088156473115e2.png)


- presents a small cross-vendor library for D3D12 that allows collection of information to narrow down GPU hangs to specific draw call ranges

- looks at the state of integration of the Vulkan swap chain with different OS and GPU vendors
- explains the expected API, what is required for a good experience and how the implementations differ between platforms

- discusses challenges and possible solutions to undersampling artifacts on curved geometry

![](../../assets/464e4ec97e2d891a.png)

- links to the presentations from the machine learning and rendering course from Siggraph

- an interview that explains what Nvidias DLSS is (Deep Learning Super Sampling)
- a trained neural network that is able to infer a 64 sample per pixel supersampled image from a 1 sample per pixel source
- the model is trained on Nvidia GPU clusters before the release of the game

![](../../assets/85746be2377c67f1.png)

- extends the Perlin noise implementation from the previous tutorial to support mixing of multiple layers of Perlin noise
- uses this to generate a dynamic terrain in a vertex shader

![](../../assets/c0e7c1f8fa363167.png)

- explains how Unity command buffers enable the extension of the Unity graphics pipeline
- uses this to implement selective bloom on objects

![](../../assets/2f48912c989a72e5.png)

If you are enjoying the series and getting value from it, please consider supporting this blog.

[Support this blog](https://donorbox.org/jendrikillner)