---
title: Graphics Programming weekly - Issue 41 — June 3, 2018
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-41/
author: Jendrik Illner
published: '2018-06-06'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- shader authors can define variations of shaders with a number of systems
- each system can inject code/resources/constants into the shader
- a material allows specifications of which shaders belong together, which systems they use and allows to insert command at the correct time in the Frame
- all of the resulting shaders get a shared resource binder and constant buffer to reduce

![](../../assets/4241200b17532f8e.png)


explanations how ray tracing shaders in OpenGL can access the necessary textures for all objects in the world using GL_ARB_bindless_texture

![](../../assets/663430625a7fd273.jpg)


- moving the scene information into group shared memory to speed up the ray tracing code a lot
- problems on metal, slower unless passing data by value instead of by const reference


- look at the iOS implementation with an overview of performance tools for CPU and GPU

![](../../assets/bab0992de4d75b2a.jpg)


- now using Logarithmic depth buffer when available
- writes custom depth in a pixel shader, this does disable early depth optimizations but still a performance win for their use-case

![](../../assets/6b61c8d25d2a4ecb.jpg)


- look at the implementation of Witcher 3 rendering from an outside perspective using RenderDoc
- breakdown of rendering Frame structure
- how normals are stored in the g-buffer
- explanation of a number of techniques from the d3d disassembly
- sun rendering
- blinking stars
- eye adaptation
- tonemapping
- vignette


![](../../assets/5f097ddba70cbc07.png)


- discussion of tradeoffs for the basis file format
- comparison of different images formats transcoded from the same source format

![](../../assets/bdc6efcce8aa261d.png)


- extending previous work in CNN(Convolutional neural network) based denoising
- using a modular architecture that improves temporal stability and detail preservation

![](../../assets/13ca8e674acc5a56.png)



- the longer the CPU/GPU can idle, the less power is needed
- optimizing a CPU bound game might cause more frames to be rendered (hitting 60 fps instead of 30). causing less GPU idle time and increasing power consumption
- kernel heuristics might trigger higher frequency mode which increases battery usage significantly


- Tutorial about the implementation of water surface movement of using a flow map in unity
- how to deal with deformation of normals using derivative maps

![](../../assets/4822d8fa11502a8e.jpg)


- NVIDIA Nsight Systems visualizes system-wide application interactions across CPU and GPU
- Nsight
- Volta, Vulkan 1.1 and Cuda 9.2, are supported
- user configurable memory view


![](../../assets/5befafe3d15a0a39.png)


-how to investigate GPU starvation and detect CPU/GPU synchronizations and overview of other tools

![](../../assets/652d802be5121905.png)