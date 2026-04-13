---
title: Graphics Programming weekly - Issue 86 — May 26, 2019
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-86/
author: Jendrik Illner
published: '2019-05-26'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- database with articles that were previously covered in Graphics Programming Weekly
- central location that aims to make it easier to discover/rediscover graphics programming information

![](../../assets/0896d97322ea89d6.jpg)


- open source release of the Basis Universal texture codec
- similar compression as .jpeg but allows textures to stay compressed on the GPU
- transcode from a common format into compressed GPU formats at runtime

![](../../assets/9561f1fd4d95f587.png)


- collection of VFX tweets of the week
- tutorials, demos, and showcases of great looking effects

![](../../assets/c6f7de5b4f233c57.png)


- presents the GPU based light mapper implemented in Unity, based on Radeon Rays
- how to design for GPU occupancy and efficient cache usage

![](../../assets/4eb9017c8603903e.jpg)


- overview videos of the hair rendering in Frostbite
- later parts will contain details about the implementation

![](../../assets/84990947b3bc9bdd.png)


- master thesis trying to answer if raytraced real-time ambient occlusion is a viable option for games
- providing path tracing theory, an overview of implementation (Vulkan)
- presents the theory behind ambient occlusion
- comparison for performance and quality with existing real-time techniques

![](../../assets/285a042168173678.png)


- proposed antialiasing technique combines rasterization with ray tracing
- uses ray tracing to collect extra samples when information from previous frames is not available
- run FXAA on the fast moving parts on the edges of the screen to reduce cost


- Microsoft GDC 2019 presentation about variable rate shading (VRS)
- presents the history of techniques and what problems VRS is designed to solve
- how VRS works
- introduction into the API
- how it performs on Intel hardware
- results by Firaxis in Civilization

![](../../assets/a1f39fb5fb0ffb36.png)


- presentation video recordings have been released
- a large variety of topics are covered
- VFX, modern rendering features for 2D games, layer materials, raytracing, color management, Vulkan and many more

![](../../assets/496e4275b3796e0c.png)


- a new skinning algorithm that removes the need for iterative calculations from delta mush skinnings
- the algorithm aims to reduce the manual skinning requirements
- quality comparison against existing skinning techniques

![](../../assets/50d2d12b61077714.png)


- a master thesis that demonstrates how to use multiple GPUs with Vulkan
- comparison of sharing work by dividing the screen or recomposition of rendering results

![](../../assets/7bd5843536613b0a.png)

Thanks to Jhon Adams for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.