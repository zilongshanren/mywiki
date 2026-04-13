---
title: Graphics Programming weekly - Issue 124 — March 22, 2020
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-124/
author: Jendrik Illner
published: '2020-03-22'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- post containing an overview of the new D3D12 Feature level 12_2 now called DirectX 12 Ultimate
- covers Variable Rate Shading, Mesh Shaders, DirectX Raytracing 1.1 and Sampler Feedback
- fully supported on PC and Xbox Series X

![](../../assets/9f5bc4eebba701ee.png)


- the Unity tutorial shows how to use color masks to apply runtime coloring with smooth blending to sprites in a 2D scene
- explains masking, blending over time and using a sin function to achieve effect looping over time

![](../../assets/e7fc18ec322657e0.png)


- the post provides an overview of the new Vulkan raytracing extensions
- using similar concepts as DirectX Raytracing
- the acceleration structure can be built on the CPU or GPU
- the article explains how CPU scheduling is exposed to the application
- adds support for DXR 1.1 features such as inline raytracing
- additionally provides a few code examples

![](../../assets/1c2b00e0df0568a3.jpg)


- the presentation provides an overview of mesh shaders
- explains the problem with the classical geometry pipeline and how the mesh shader pipeline is an improvement
- provides a walkthrough of code demonstrating how mesh shaders are implemented and what needs to be considered to achieve excellent performance
- explains the meshlet data structure and how to use this as a base for a mesh shader pipeline
- how to implement instancing, and using per-primitive attributes

![](../../assets/8daa33bc7e61639e.png)


- build upon the @Reinventing the Geometry Pipeline: Mesh Shaders in DirectX 12” talks summarized above
- provides more hardware details and how to design mesh shader implementation to give excellent performance
- extending the meshlet pipeline with more advanced culling and mesh data compression
- providing performance numbers for different techniques

![](../../assets/4aa76d38ba4c6046.png)


- the video provides an overview of the new Sampler Feedback feature added to D3D12
- shows how to use compile sampler feedback and reserved resources to improve texture streaming
- overview of texture space shading and how sampler feedback can be used to guide the system
- closing with an API overview

![](../../assets/6df08a7f41a0f6c3.png)


- overview articles by Nvidia for D3D12 Ray Tracing, Mesh shading, Variable Rate Shading, and Sampler Feedback

![](../../assets/7dc35ee1f3ca419f.png)


- the article describes the VK_NV_device_generated_commands extension for Vulkan
- it allows partial command buffers to be generated on the GPU
- more flexible then D3D12 ExecuteIndirect
- main functional addition is the support of changing of shaders between commands

![](../../assets/62ec2b5e63530053.png)


- the article presents an overview of a BVH structure for GPU raytracing
- this is not using any raytracing APIs and focuses on the data structure design
- how to structure the tree, handle animated meshes and refit the structure for changes

![](../../assets/5191232e29d24540.png)

Thanks to [Ken Russell](https://twitter.com/gfxprogrammer) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.