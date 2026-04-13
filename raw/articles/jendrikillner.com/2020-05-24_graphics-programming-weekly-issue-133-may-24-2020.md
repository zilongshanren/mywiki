---
title: Graphics Programming weekly - Issue 133 — May 24, 2020
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-133/
author: Jendrik Illner
published: '2020-05-24'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- detailed post presents the idea of “decorrelating” color channels to maximize information in texture channels and eliminate redundancy allowing data to be stored in fewer color channels
- introduction into Singular Value Decomposition SVD and how it can be used for channel decorrelation
- showing quality comparisons for a PBR texture set and discusses possible problems

![](../../assets/d4172a02a8b7760d.png)


- Version 2 of Windows Subsystem for Linux adds full support for D3D12 (not allows rendering to the screen yet)
- this is implemented as Linux kernel model driver to expose the GPU to user mode Linux applications
- DirectML and CUDA are implemented on top to allow machine learning on Linux guests

![](../../assets/82259dee4384ed3a.png)


- relaxed cone step mapping for relief mapping to add more details
- async compute based tesselation for interactive terrain
- the interactive deformations have been implemented using texture-atlas based technique
- running pixel bound post-processing in parallel with the pre-pass of the following frame
- advice for the reduction of d3d12 hitches

![](../../assets/958523dc198a579e.png)


- collection of concepts, macros, shader logics, that exists in unity build-in render pipeline and how they are represented in the new Universal Render Pipeline

![](../../assets/9f48c83b3637ebd5.png)


- Khronos questionary that presents a list of suggestion for possible vulkan helper libraries
- looking for feedback on which libraries would be of most interest from developers

![](../../assets/bafc3b2f6762927a.png)

- Unity tutorial that shows how to use a navmesh as a base for minimap rendering

![](../../assets/f70fd212596f5af1.png)

- the paper proposed a new method that aims to improve ray tracing by offsetting ray starting point aways from the originating leaf nodes of the acceleration structures
- the suggested proposal is generating an auxiliary data structure of hemispheres that make it robust to offset the ray starting point

![](../../assets/7f742632d9ebe735.png)


- A unity tutorial that shows how to blend multiple textures together and save them to disk using Unity

![](../../assets/eb8dc456c22b65a4.png)

- Eurographics & Eurovis 2020 conference will be virtual and streamed starting May 25-29, 2020

![](../../assets/b63d8407266eac54.png)

- brief overview and introduction into Mesh Shaders using OpenGL and Vulkan

![](../../assets/72027198ee677566.jpg)


- collection of notes about the content of the AMD talk presenting the AMD RDNA architecture and GPU optimizations
- presents a walkthrough of a MIP generation example

![](../../assets/933a4032ce470c92.png)


- A new newsletter with news and insight on volumetric filmmaking, virtual production, 3D rendering, and other emerging realities

![](../../assets/365b48f04e82d58e.jpeg)

Thanks to [Trevor Black](https://trevord.black) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.