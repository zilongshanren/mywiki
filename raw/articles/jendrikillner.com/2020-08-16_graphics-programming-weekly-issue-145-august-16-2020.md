---
title: Graphics Programming weekly - Issue 145 — August 16, 2020
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-145/
author: Jendrik Illner
published: '2020-08-16'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article provides an extensive list of best practices for DXR usage
- covers acceleration structures, GPU utilization, memory allocations, handling of non-opaque geometries, binding, performance and pipeline state best practices

![](../../assets/cd358fbafc209964.png)


- the blog post explains what the bindless model is
- shows how to use for Textures and how to replace Vertex Layouts
- examples are for D3D12, but links to information for Vulkan is provided

![](../../assets/6802db238492e483.jpg)


- the article provides a basic overview of how the OpenGL ES based engine was ported to Vulkan
- lists performance issues encountered such as Sparse Indexing, vkQueuePresent blocking and barrier usage for improved throughput
- provides a comparison of CPU, GPU usage with OpenGL and Vulkan

![](../../assets/d37704faa3912e67.png)


- the blog post explains how the author implemented a precural painting logic using compute shaders
- explains how the algithmn was structrued, discussiong ecoutnered problems and solutions implemented

![](../../assets/99e31fc4e9d2d813.jpeg)


- the article presents an overview of the DXT and ETC compression formats
- shows how information is compressed and how to decode these formats from a compute shader

![](../../assets/bd107582ae3e04bc.png)


- short post presenting how to setup VSCode to allow GLSL shader iteration

![](../../assets/6d560afeb8402887.png)


- the article explains primary surface replacement (PSR) and checkerboarded split frame rendering (CSFR)
- these techniques are presented as a possible solution for high-quality reflections and refractions in a mixed hybrid renderer design that relies on GBuffers for primary rays

![](../../assets/299c2e99b7edb8a2.png)


- A video tutorial that explains how to implement a shader to render a torus knot using ShaderToy
- starts by explaining the foundational math followed by the shader implementation

![](../../assets/7e352bd6739fb9bd.png)


- the article discusses the different render target requirements for D3D12 and Vulkan and presents 4 alternative solutions to design an abstraction

![](../../assets/71bee12917a3c764.png)

Thanks to [Manish Mathai](https://github.com/goodbadwolf/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.