---
title: Graphics Programming weekly - Issue 166 — January 17, 2021
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-166/
author: Jendrik Illner
published: '2021-01-17'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the post shows how aliased resources can cause problems when doing render doc captures
- aliased textures that are captured might need barrier transitions, which can corrupt other textures in the same memory range

![](../../assets/0a786dafe2818e3e.jpg)


- collection of articles/ blog post written by John Carmack on a variety of topics

![](../../assets/1c5a8128e75e159f.png)


- the video tutorial shows how to implement a shader for freezing objects
- this includes blending ice material on top of existing objects, tessellation shaders to extend meshes to form icicles, and mesh normal generation

![](../../assets/2dda067f2f90857a.png)


- the blog post shows the interactive particle implementation used in Ghost of Tsushima
- particles are controllable through expressions and can react to runtime information
- shows different use cases such as interactive leaves, candles, and crabs

![](../../assets/52058975fc5fcecf.png)


- the tutorial shows how to implement Temporal Anti-Aliasing using an example OpenGL implementation
- provides a walkthrough of all steps required
- shows how to calculate velocity vectors, use history buffers, calculate jittering matrix
- additionally shows how dithering can be used to create alpha-blended looks

![](../../assets/bbe94bcaeb8b456a.png)


- the Rust tutorial provides an extensive walkthrough of the steps required to use OpenGL using native rust
- explains all the necessary interop to load OpenGL, initialize a swap chain, and start presenting

![](../../assets/e4f19872df253d92.png)


- the article presents how VRS tier 2 shading was integrated into Gears
- uses the previous frame color buffer results to run a Sobel edge detection compute shader to detect the shading rate
- a conservative VRS allows systems to opt-in for special quality if required
- contains advice on optimizations for VRS tile texture generation
- additionally provides guidance on how to estimate performance using Tier 1
- provides performance numbers for the savings from different render passes

![](../../assets/3f048e21badb1db8.png)


- the article contains a list of common graphics programming terms and how to pronounce them

![](../../assets/40b291f7dc57dd47.png)


- the article provides a guide for porting from the original VK_NV_raytracing extension to official VK_KHR_raytracing extensions
- show what changes are required for device creation, memory management, acceleration structure build, pipeline management

![](../../assets/04760b4d178fdc84.png)


- the article presents an overview of Creation Graphs and what it enables the user to create in The Machinery
- an extensible node-based system that allows the flexible combination of data from different kinds of data to create new combinations

![](../../assets/a4c4409739923577.jpeg)


- the video tutorial explains how to create stylized grass in the Unreal engine
- shows how to create the meshes in Houdini, textures in Unreal and integrate them into the rendering pipeline

![](../../assets/20f9b43885ac6c1a.png)

Thanks to [Angel Ortiz](https://twitter.com/aortizelguero) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.