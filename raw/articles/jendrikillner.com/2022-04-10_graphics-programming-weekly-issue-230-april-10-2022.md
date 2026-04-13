---
title: Graphics Programming weekly - Issue 230 - April 10, 2022
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-230/
author: Jendrik Illner
published: '2022-04-10'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the video provides a complete walkthrough of the creation of a large outdoor environment using shadertoy
- presents how to implement a terrain using fractal surfaces, sun lighting, atmospheric scattering, clouds, grass, and trees
- it additionally shows how to apply color adjustments for artistic expression

![](../../assets/2f53f7437ed9df75.png)


- the article presents a retrospective of raytracing experiments done using compute shader implementations
- shows an introduction for every experiment and how they present a continuous research space
- providing links to an article covering each experiment

![](../../assets/e6f1839922894d07.png)


- the article presents an abstraction system to allow shaders to author bindings without having to be aware of binding details in an abstracted method
- shows how to emulate Shader Model 6.6 ResourceDescriptorHeap functionality in Vulkan where it’s not yet available

![](../../assets/c6c4f30d84bc7b0f.png)


- the article provides an in-depth look at the core loop optimizations of the Oodle decoding step for AMD jaguar CPUs
- discussing hardware details of the CPU cores and how they define the decoder design

![](../../assets/fa0b43b67237f0ae.png)


- the 30min video provides a summary and examples of the new features in Unreal Engine 5 (UE5) to build an example scene
- covering things like Niagra particles, fluids, landscape modeling, object material blending, nanite, etc

![](../../assets/92862a3f7d092b57.png)


- the video tutorial shows how to implement ten different effects using UnityShader graphs
- covering outline, dithered transparency, and vertex waves

![](../../assets/9034c2b7cc9dd3cc.png)


- the video shader tutorial shows how to use tessellation and displacement to create dynamically detailed meshes
- presents how to control the displacement amount from a height texture
- it additionally shows how to control the amount of tessellation only to add extra detail when needed on the silhouettes

![](../../assets/17ef76d85d429dfa.png)


- a high-level overview of what Global Illumination is, the importance for the rendering results
- presents several techniques that exist for the calculation of GI
- these include radiometry, lightmapping, Path tracing, Voxel Cone Tracing as well, as Virtual Lights

![](../../assets/4ca2301ff50cdbf5.png)


- discusses what Ambient Occlusion is, provides how it fits into the rendering equation and what it cannot express
- presents a high-level overview of an existing screen space technique to calculate the effect
- it additionally covers why in most cases, soft shadows are expected and techniques to approximate the effect

![](../../assets/8ff8714c5152deee.png)


- the video tutorial shows how to generate a procedural hexagon shape mesh
- extends the generation to logic to support 3D hexagon shapes and combine them into a grid
- implementation is shown using Unity C# code

![](../../assets/9d6322d7ea544136.png)

Thanks to [Matt Pharr](https://pharr.org/matt) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.