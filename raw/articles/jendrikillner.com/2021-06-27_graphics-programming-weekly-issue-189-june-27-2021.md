---
title: Graphics Programming weekly - Issue 189 - June 27, 2021
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-189/
author: Jendrik Illner
published: '2021-06-27'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- in-depth analysis of the sources of variance in state-of-the-art unbiased volumetric transmittance estimators
- propose several new methods for improving the efficiency
- improving truncated power-series estimators based on U-statistics

![](../../assets/d95272277520824d.png)


- the paper presents a new BRDF for porous/dusty materials
- these surfaces exhibit back-scattering and saturation that is missing from other BRDFs
- based on a volumetric BRDF derivation based spherical Lambertian particles

![](../../assets/37e0330f079acda9.png)


- the article discusses how to implement gamut clipping into a render pipeline
- compares different methods and presents the results with different lighting setups

![](../../assets/f2c0c4f2f20bc2c8.png)


We are looking for a Senior Research Engineer to work on real-time rendering algorithms for visual effects, animation, and post-production software.

The role is about creating the next generation of artists and production tools, with a focus on virtual production. There is a focus on the role of improving, optimizing, and expanding the graphics capability within real-time renderers.

We are looking for people with a strong track record in graphics and real-time rendering with the desire to build real-world solutions for our artists.

![](../../assets/6172b637eae5ba5f.png)


- describes the state of raytracing in games
- presents a high-level overview of a Decoupled Real-Time Ray Tracing pipeline
- shows where raytracing is used in games and what new problems it introduces
- additionally presents 4 open problems in raytracing and how it interacts with other developments

![](../../assets/ba0c214e32251754.png)


- the paper introduces a neural radiance caching method for path-traced global illumination
- uses a self-training process to train the neural network at runtime

![](../../assets/373cde16928b83ed.png)


- the video tutorial explains how to draw Squares, boxes, and rounded rectangles as SDFs
- presents how to derive the SDFs and presents the extension into rotated shapes
- additionally shows how to use rectangle SDFs to implement a brick wall

![](../../assets/80e8627a2a432e87.png)


- discusses how to generate ocean displacement, buoyancy,
- rendering of the ocean as micro facets, how to calculate moments from the displacement
- reflections (specular and environment), masking/shadowing, and light scattering inside the water surface
- additionally covers interactions with the water, explosions, etc…

![](../../assets/3cd46384c9a04a8f.png)


- the article discusses local tile memory and mobile GPUs
- presents how different usage patterns affect the ability to achieve optimal bandwidth usage
- shows some OpenGL extensions that enable tile local memory usage
- additionally, it shows how Vulkan Subpasses allow the driver to optimize shaders transparently

![](../../assets/4a9825ab9483c1a1.png)


- a new Vulkan extension that adds vkCmdDrawMultiEXT vkCmdDrawMultiIndexedEXT
- these allow applications to provide an array of draw call arguments in CPU visible memory
- for uses cases where applications would call vkCmdDraw multiple times in a loop without changing state
- tests indicate that a doubling of draw call processing rate can be observed

![](../../assets/b1e223a1bbb23dc9.jpg)

Thanks to [Jasper Bekkers](https://twitter.com/JasperBekkers/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.