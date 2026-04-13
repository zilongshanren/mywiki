---
title: Graphics Programming weekly - Issue 160 — December 6, 2020
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-160/
author: Jendrik Illner
published: '2020-12-06'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- The article presents how important reflectivity of Black skin is for believable results
- it shows how to adjust textures and the Unity PBR shaders (specular workflow) to decouple specular color from the glossiness

![](../../assets/98ec8d46f00bd1d7.png)


- the talk from Digital Dragons looks at open questions in rendering
- walkthrough of the various assumptions and approximations and raises the question of the most significant source of error in modern rendering pipeline?
- presenting a look at the higher-level view at how are rendering and production pipeline might evolve
- discussing tradeoffs and how a more holistic view of rendering might lead to more productivity and better results

![](../../assets/f4350955c69cfe8b.png)


- the talk provides an overview of Roblox and how the philosophy creates an environment with very different technical challenges
- a tech that favors scalable over optimal and how it’s been able to evolve existing data to take advantage of new device abilities
- provides an overview of the engine architecture and a walkthrough of a large number of rendering systems (clustering, lighting, shading)

![](../../assets/7c11891f557e763a.png)


- part of tutorial series about the Unity scriptable rendering pipeline (SRP)
- covers how to support soft and distortion particles
- determining depth for orthographic and perspective projections

![](../../assets/64442a29efef6ce4.jpg)


- presentation shows the in-progress state of the new Frostbite hair rendering system in the context of FIFA
- covering both the strand simulation and rendering
- rendering is done using a custom line rasterize, order-independent transparency, and strand space shading (texture space shading)

![](../../assets/8a2bb943aad13594.png)


- the articles discusses how the voxel rendering in teardown uses an 8-bit color palette for voxel materials and still allows coloring
- this is archived by precalculating multiple color variations for each material
- if not enough slots are available similar materials will be merged

![](../../assets/901c558535659d89.png)


- the Bachelor thesis introduces Linearly Transformed Spherical Harmonics
- A technique for computing specular shading from to polygonal area lights
- compares the method against linearly transformed cosines, and it’s able to produce higher quality results

![](../../assets/431ef79981c5af89.jpg)


- the article explains a different kind of memory that exists
- how AMDs Smart Access Memory fits into the picture
- additionally covers considering of performance when using a device or host-local memory

![](../../assets/8fd0d1f7f86d60e8.png)


- the article presents how the effect was implemented that allows objects to be colorized/silhouetted to make them pop out of the scene
- this is implemented by rendering AABB with per-object depth into a separate render target, marking tagged objects via stencil
- and using post-processing to apply the outline effect

![](../../assets/596c566827111b3a.jpg)


- video recording of the talk covered in
[week 154](https://www.jendrikillner.com/post/graphics-programming-weekly-issue-154/) - the presentation explains how the raytracing for shadows has been implemented into Call of Duty
- covering acceleration structure separation, performance, denoising implementation, and supporting multiple local area lights

![](../../assets/18eb58f358bc9ce7.png)

Thanks to Peter Kohaut for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.