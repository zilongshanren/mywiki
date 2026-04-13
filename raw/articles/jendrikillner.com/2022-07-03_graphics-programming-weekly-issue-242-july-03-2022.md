---
title: Graphics Programming weekly - Issue 242 - July 03, 2022
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-242/
author: Jendrik Illner
published: '2022-07-03'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the second part of the blog series that talks about order independence transparency
- this week focuses on techniques that aim at solving transmittance contribution first and then applying the factors while shading
- shows how Rasteriser Order Views (ROVs) can be used to implement custom blending operations
- presents performance implications of the proposed techniques

![](../../assets/fcf359a98104874e.png)


- the Twitter thread discusses the terminology that applies to meshes
- presents the difference between static, dynamic, deformable, and procedural meshes

![](../../assets/30ded9028888d0c7.png)


- the Xfest presentation discusses the portal implementation for Psychonauts 2
- covers how portals are represented in the world, how to render the portal world, discusses issues encountered and how they have been overcome
- it also presents essential performance optimizations
- it additionally covers how to calculate the required transformations and solve system interaction problems

![](../../assets/aaa17087d01c9d80.png)


Double Fine Productions is looking for a full time graphics programmer to join its San Francisco based development studio. Having recently shipped the award winning Psychonauts 2, we are looking to expand our graphics and systems programming team to support the development of our future titles.

You will be responsible for developing rendering features, optimizing game performance and memory usage, and building low level systems on PC and Xbox.

Applicants should have a strong preference for working in a highly creative, innovative, and nimble development environment, where collaborating with design, audio, art, animation, tech, and other disciplines is standard.

![](../../assets/27034fe5c580ce80.png)


- the paper presents a new method for stratified resampling
- shows a single pass solution to inverse CDF sampling (similar to reservoir sampling)
- extends the presented solution to other domains and compares it against existing techniques

![](../../assets/43ecc0f310310ad7.png)


- the video presents how to use second-order systems to allow dynamic motion control in procedural animation scenarios
- presents the mathematics and an example implementation in Unity

![](../../assets/1bb5aba2dc0f9a7c.png)

- the article presents how to combine multiple tricks to create the appearance of volumetric fog
- combines a height map-based mesh with depth & translucency fading to create the illusion
- discusses the steps required and provides examples in C++ / Unreal visual script

![](../../assets/1748b1c8785842cb.jpg)


We have several project openings for a Senior/Principal or Lead Rendering Engineer to work on new/all original IP’s, which are being developed in Unreal 5 and are true cross-play multiplayer games on PC, Console & Mobile.

You will work collaboratively with artists, designers and engineers to realize our beautiful, stylized visual target.

The ideal candidates are broadly experienced with optimization & profiling CPU/GPU on multiple platforms, creating content workflows/pipelines and experienced with both R&D and production systems/features.

![](../../assets/4d60b6dd5a25ef5d.png)


- overview of the talks that will be presented at the Advances course as part of Siggraph 2022

![](../../assets/ce9a5acd7515640d.png)


- the article presents Nvidia’s best practices for clearing textures and depth buffers
- clarifies what methods are preferred and how clear values can influence performance
- it additionally presents the tradeoffs between the different presentation modes

![](../../assets/a44058142dcabd17.jpg)


- the video tutorial presents how to create a post-processing effect that simulates an underwater look
- covers depth-fog, distortion, lens distortion, and caustics
- presented using Unity and Unreal visual shading system

![](../../assets/499b1d0f0749d960.png)


- the article presents how to generate a procedural Icosahedron mesh
- shows and discusses the differences in point distribution compared to other sphere mesh structures

![](../../assets/0943c507ae6f4ea4.jpg)


- the article presents how to improve compute shader performance when workloads are memory limited
- presents how to detect if a CUDA shader runs into register limits
- it additionally shows how CUDA launch bounds (promises on work sizes) can give the compiler more information for more aggressive optimizations

![](../../assets/f6751f88f080cb33.jpg)

Thanks to [Vivitsu Maharaja](https://twitter.com/vivitsum) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.