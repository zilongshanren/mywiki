---
title: Graphics Programming weekly - Issue 203 - October 3, 2021
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-203/
author: Jendrik Illner
published: '2021-10-03'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the paper proposes a new technique to enable the temporal reuse of samples in scenarios where motion vectors are not enough / available
- core algorithm of the paper is patch-based correspondence detection within a hierarchical

![](../../assets/5248bf77623b71de.png)


- the paper provides an overview of Spectral Image Representation and Bi-spectral Reflectance
- explains what kind of materials require the information for correct representation
- proposes a way to store the data in the OpenEXR format

![](../../assets/fd9d4e9ac14a84b5.png)


- the video provides an overview of a GPU based fluid solver
- written with WebGPU and Rust
- primarily focusing on the implementation details of the simulation

![](../../assets/7a997940122fa299.png)


- the Unity tutorial shows how to implement a basic flow system in Unity
- implemented using a projection of 3D shapes into clip space
- flow is implemented using a double buffering approach using compute shaders

![](../../assets/749077c30c3f3392.png)


- the Unity tutorial explains how to implement a 2D effect where a mask controls the visibility of a line over time
- presents the code and unity setup necessary to implement the effect

![](../../assets/277c9d6d3e87921a.png)


- the video explains how to develop a mental model of 3D rotations
- based around the change of orientation from one coordinate space to another
- presents an overview of different ways to express rotations
- additionally shows how to use the techniques in Unity

![](../../assets/abd9fe2f13754bfa.png)


- Khronos released the texture format 2.0, which now supports Basis Universal compression
- additionally, the new gltf KHR_texture_basisu extension allows the usage in gltf models

![](../../assets/d70f10bcdfab0b16.png)


- the blog post describes the details about parsing DXIL (the output from the Microsoft Shader Compiler)
- shows how to parse various opcodes, details with SPIR-V
- provides an overview of the capabilities of the LLVM based encoding

![](../../assets/efe019a9e343d233.png)

Thanks to [Joakim Dahl](http://www.plane9.com) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.