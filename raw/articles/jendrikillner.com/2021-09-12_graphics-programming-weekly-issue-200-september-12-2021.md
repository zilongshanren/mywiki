---
title: Graphics Programming weekly - Issue 200 - September 12, 2021
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-200/
author: Jendrik Illner
published: '2021-09-12'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the paper proposes a formal model to describe how surfaces/media respond to incident radiation
- introduces a hybrid matter model for a locally stationary stochastic process

![](../../assets/1cf0a4f2c53770e2.png)


- the Vulkan tutorial shows how to use the Vulkan VK_NV_ray_tracing_motion_blur extension (exposed by Nvidia)
- shows how to extend a static ray tracer implementation with the necessary information to support motion(blur)
- contains API extensions for time-dependent tracing, motion support in acceleration structures, and support for changing vertex positions

![](../../assets/5ab95ee3a8b14c38.png)


- the article presents a derivation of new color spaces designed for more uniform color picker behavior
- discusses the different tradeoffs and how a perfect solution is not possible
- presents an overview of existing methods (HSV, HSL, HSLuv), discussing the tradeoffs, weaknesses, and strengths
- additionally provides an interactive implementation of all the color pickers

![](../../assets/bf13f5488187b31f.png)


- the article presents a method for the rendering of static Constructive solid geometry SDFs
- breaks down an SDF into several sub-trees, with shader specialization for each
- requires a static source SDF; however, it could still change positions

![](../../assets/a639c274c6ac3dbb.png)


- article introduces a prototyping system aimed at making multi-pass shader experiments easier
- implemented using Rust and GLSL
- presents how to implement several systems such as a path tracer, the game of life using the system

![](../../assets/cbe82a86a192fd8c.png)


- signup and schedule for the Vulkanised conference has been published
- combination of talks and Vulkan layer authoring tutorials

![](../../assets/578e69dc9cb76719.jpg)


- the article presents a look at the making of the fog lost in random
- shows how the visual style was achieved
- based on volumetric or screenspace fog based on the platform capabilities

![](../../assets/40500e0046b9a31d.jpg)


- the paper introduces a new metric, CaMoJAB
- this considers how the judder, aliasing, and blur artifacts introduced by VRS are masked by the sensitivity limits of the visual system
- presents how to use the metric to derive VRS shading rate as well as required refresh rates

![](../../assets/aee4931d3e6937d3.png)

Thanks to [Warren Moore](http://metalbyexample.com/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.