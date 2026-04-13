---
title: Graphics Programming weekly - Issue 240 - June 19, 2022
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-240/
author: Jendrik Illner
published: '2022-06-19'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the last part of the series covers how to extend the ray-tracing onto the GPU using OpenCL
- presents the extensions necessary to render hundreds of Stanford Dragons with reflections and lighting

![](../../assets/10e9caa92006b607.jpg)


- the video discusses the importance of color transformations to final images
- shows how color shifts can make for very unnatural behavior
- shows how filming tone mapping can resolve these issues
- it additionally presents an overview of how filmic tone mapping curve controls in the darkroom tool

![](../../assets/9ac7349dbe95c6a7.png)


- the article presents work done to make GPU operations reactive, declarative, and composable and remove many of the tedious manual boilerplate work required
- presents the problems and motivation for the suggested solutions
- the code and demos using WebGPU are available

![](../../assets/40968a15e94e53b9.png)


We have several project openings for a Senior/Principal or Lead Rendering Engineer to work on new/all original IP’s, which are being developed in Unreal 5 and are true cross-play multiplayer games on PC, Console & Mobile.

You will work collaboratively with artists, designers and engineers to realize our beautiful, stylized visual target.

The ideal candidates are broadly experienced with optimization & profiling CPU/GPU on multiple platforms, creating content workflows/pipelines and experienced with both R&D and production systems/features.

![](../../assets/4d60b6dd5a25ef5d.png)


- the video explains how to implement a positional-based cloth simulation on the GPU
- presents how to use NVIDIA Warp to use Python to author the simulation code
- it mainly focuses on mapping the algorithm onto the GPU for efficient and valid execution

![](../../assets/17af4fe099c641e1.png)


- the video shows to create 3 types of fullscreen masks (square-edge, round-edge, and distance)
- then presents how to use them to mask off areas where an effect should not be applied
- it additionally presents how to apply a vignette effect
- implementation is shown using the visual shader authoring system in both Unity and Unreal

![](../../assets/7bfcd25cd8232b13.png)


- the article presents a method to pack individual power-of-two textures into a texture array
- discusses the placement rules and how to pack them
- it additionally includes a brief code sample implementation

![](../../assets/fb9bbd19d6bf19ae.png)


- the video tutorial explains how to use an orthographic projection to implement directional light shadows
- explains the mathematical understanding behind orthographic projections and how to create a matrix for the projection
- it additionally shows the difference between left/right-handed coordinate systems
- presents the C++ and OpenGL implementation code required

![](../../assets/0ce35d1e86cf7089.png)


- the Vulkan Memory Allocator is now included as an optional component in the Vulkan SDK
- can be installed directly from the SDK installer

![](../../assets/8786095e8147682d.jpg)

Thanks to [Erika](https://twitter.com/rrika9) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.