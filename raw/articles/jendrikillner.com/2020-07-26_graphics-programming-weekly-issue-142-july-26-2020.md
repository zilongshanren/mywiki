---
title: Graphics Programming weekly - Issue 142 — July 26, 2020
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-142/
author: Jendrik Illner
published: '2020-07-26'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article presents an overview of Vulkan barriers and shows how different barriers influence a PowerVR chip’s ability to overlap work

![](../../assets/09baefbe3d076995.png)


- the second part of the series presents how to overlap work from two consecutive frames by submitting each frame to its own queue

![](../../assets/26365f09d7727e03.png)


- the blog post presents how to use the Intel Embree library to generate a BVH tree for use with a GPU raytracer
- offers performance and memory comparisons for the different quality modes available

![](../../assets/4f5ce5c91d197966.png)


- the article present how the food in ‘Ratatouille’ was shaded based on the skin model
- using a subsurface scattering approximation on a voxel grid
- artists were given much control over the final more stylized appearance

![](../../assets/3b090030e6c2b019.jpg)


- the Unity tutorial explains how to add an outline to a 2D sprite
- implemented using 8 extra texture samples around the shading point
- additional presents a way to make the outline size independent of the sprite size

![](../../assets/27150c3153a5fd34.png)



- the Unity tutorial explains how to create basic compute shaders
- shows how to use a compute shade to generate random positions in a sphere and use these position from the CPU to render meshes

![](../../assets/e8c680d746aef5ec.png)


- This Unity tutorial shows how to pass data from the Shuriken Particle System to the particle shader

![](../../assets/e7e1f2eccba4ad55.png)


- the article provides a high-level explanation of the Vulkan API concepts required to render a single triangle on the screen
- contains well-documented example implementations to clarify some ideas through code examples

![](../../assets/dfa53fafc4aa993c.jpg)


- open source D3D11 implementation of the paper presented at EGSR 2020
[“A Scalable and Production Ready Sky and Atmosphere Rendering Technique”](https://www.youtube.com/watch?v=y-oBGzDCZKI)

![](../../assets/d2c14ef4c365d275.png)


- the blog posts list a few possible drawbacks that need to be considered if a mix of dedicated GPU and integrated GPU is supposed to be used in a single application


- a small shader example that shows that texture channels can be reserved to allow objects to change color dynamically at runtime

![](../../assets/bfcedffaec7e365d.png)

Thanks to [Erika](https://twitter.com/rrika9) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.