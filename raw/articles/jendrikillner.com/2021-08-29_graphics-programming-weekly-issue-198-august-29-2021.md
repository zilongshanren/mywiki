---
title: Graphics Programming weekly - Issue 198 - August 29, 2021
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-198/
author: Jendrik Illner
published: '2021-08-29'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- in-depth frame analysis of a nighttime scene in Mafia, a d3d11 based deferred rendering engine
- covers g-buffer, occlusion culling, decal blending, GI
- cars use a precalculated shadow texture to cast AO
- heavy use of stencil usage for volumetrics, sky, as well as the minimap rendering

![](../../assets/1a4f375ed22128ad.jpg)


- the article presents optimizations to the FidelityFX Super-Resolution by AMD
- shows multiple steps, what gains got achieved and hints at what quality reductions can be expected

![](../../assets/47c65f12a9562a42.jpg)


- the article presents how to implement a shader-based ASTC decoder
- shows what different modes are supported, how to encode parts
- pointing out the complexities and special cases of the format

![](../../assets/f8237323cf7d1a3e.png)


- the article contains a brief summary of the content presented at the WebGPU meetup
- covers WebGPU performance advice, new glTF extensions
- additionally shows how batching and multi-draw techniques can improve performance

![](../../assets/9c0d30b18273c5bb.png)


- the shader tutorial presents how to implement a grass shader using the Universal Render Pipeline in Unity
- using Geometry Shaders to generate blade meshes and tessellation shader to control the grass density
- presents how to deal with a nonplanar surface, supporting rotation and bending
- additionally shows how to control grass painting onto the world, wind and shadow integration

![](../../assets/fe126476c5bbdd74.jpg)


- collection of tweets covering an extensive range of technical art topics
- VFX, breakdown of scenes, showcases of visual effects, …

![](../../assets/f25b8ceba0e1db03.png)


- article presents a project that emulates a Linux in a pixel shader running in VRChat
- emulates a RISC-V CPU in an HLSL pixel shader
- shows how the emulation was implemented
- a few pointers on performance improvements made throughout the process

![](../../assets/288d210561181fe1.jpg)

Thanks to [Deepak Surti](https://www.deepaksurti.com) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.