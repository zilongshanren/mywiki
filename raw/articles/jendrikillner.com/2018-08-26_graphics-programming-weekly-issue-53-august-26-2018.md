---
title: Graphics Programming weekly - Issue 53 — August 26, 2018
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-53/
author: Jendrik Illner
published: '2018-08-26'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- video for the talk that was discussed in
[issue 42](https://www.jendrikillner.com/post/graphics-programming-weekly-issue-42/) - an in-depth overview of color, color spaces, and color transformations
- discussion of HDR standards
- ACES pipeline overview
- implementation of HDR pipeline covering:
- tone curve, display mapping, UI rendering
- universal CLUT and color grading


![](../../assets/a85e3123b7235c84.png)

- normal and gloss mipmapping
- using a shortened normals technique
- normals are shortened based on the glossiness
- how to combine different textures to add detail to a base texture

- material surface occlusion
- reformulation of Ambient Occlusion that adds indirect lighting in the occluded parts of the material
- adds micro-shadowing from material occlusion into the direct-lighting component
- indirect specular occlusion, using 3D Environment BrdfLut, 3rd dimension is cone angle

- multi-scattering diffuse BRDF utilizing an approximation stored in a 2D LUT

![](../../assets/0e619119c3a75641.jpg)


- present HLSL code snippets that implement different kinds of dithering and an example application
- comparison of quality and performance of the different dithering techniques

![](../../assets/955f2ffaabda3f55.png)

- an in-depth walkthrough of the new Depth of Field implementation in Unreal Engine 4
- discussing problems encountered, solutions and optimizations
- includes many small code snippets
- better results and better performance than the old UE4 implementation

![](../../assets/3140cf55739fc400.jpg)

- discusses architecture, light culling, clustered lighting implemetation
- how feature parity between deferred and forward pipeline is achieved
- implementation of decal system using a D-buffer (similar to g-buffer but for decals only)
- details about material types, lighting features, volumetric systems

![](../../assets/0bc3a0bcb89b3093.jpg)


- presentation of a screen space subsurface scattering model, they call it the Disney SSS
- model is using a single tweakable parameter that makes it easy to use for artists
- implementation details for a thick and thin object model and optimizations to the implementation

![](../../assets/27a1b6f20197a6f2.jpg)


- start tracing rays where rasterizer has shortcomings
- explains how to tune Monte Carlo estimators to converge quicker by minimizing variance using different AO and spherical lights as examples
- shows the weakness of uniform random numbers and provides techniques to generate better distributions
- variance-driven sampling focus taking more samples where variance is high

![](../../assets/571d0f845c9c45a2.jpg)


- presents two techniques that improve on existing Fibonacci lattice methods
- one version to achieve better packing distribution
- other to optimize volume and surface area of the convex hull

![](../../assets/bdea8343179bb7df.png)

- overview of differentiable rendering
- a technique gaining traction in machine learning
- the idea is to provide a way to inverse the rendering process so that changes in the output can be traced back through the pipeline to map changes from output state into changes in the input state

![](../../assets/068991d8f0597829.png)

- slides for the Moving Mobile Graphics 2018 course from SIGGRAPH 2018

![](../../assets/ecd6bd150686b4e2.jpg)

- an in-depth explanation WIP document about Monte Carlo integration
- how it’s able to approximate the shape of the function from taking independent samples
- how importance sampling helps to converge quicker
- extend technique to support Multiple Importance Sampling

![](../../assets/164c354449218909.png)

- slides from the SIGGRAPH course
- characteristics of an idealized display
- discussion of real hardware considerations
- tone reproduction, tone characteristics, dynamic range
- color primaries, gamut, calibration & characterization
- viewing environment, adaptive displays, observer differences

![](../../assets/d558815acb7e8186.png)


- video tutorial on how to implement a subsurface scattering approximation with unity

![](../../assets/2a051520971a8ed7.png)

- a tutorial that explains how to use the stencil buffer with Unity
- shows how to read/write the stencil mask so that only parts of models will be visible on the screen

![](../../assets/59d88a44d99b2b9f.png)

- a tutorial explains how to create an Overwatch style x-ray effect in Unity
- implemented using stencil buffer and multiple shader passes

![](../../assets/037223a45dc5ddf5.png)

- abstraction layer from AMD on-top of Vulkan has been released as open source
- implements automatic render barrier management, descriptor pools/sets, memory management, render passes, etc

![](../../assets/d1b7a500e1e8bd65.png)

- collection of observations and nuggets of information from different SIGGRAPH 2018 sessions

![](../../assets/a76092591cd50b0c.jpg)

- a visual explanation of foundational linear algebra concepts that are required for shader programming

![](../../assets/411d1d2f77e6830d.jpg)

- video of the demoscene session at SIGGRAPH 2018
[Clouds in Wande](https://youtu.be/yqA71-HHY2Q?t=585)[Making an animation in 18 bytes at a time](https://youtu.be/yqA71-HHY2Q?t=1555)[Building World in 64KB](https://youtu.be/yqA71-HHY2Q?t=2722)[Demo Party in Japan](https://youtu.be/yqA71-HHY2Q?t=3918)

![](../../assets/55036fad5edb8268.jpg)


- next part of the series about developing a path tracer using Cuda
- discussing how to move ray generation code from the CPU to the GPU
- speedup of 11x is achieved compared to single threaded CPU implementation

- thoughts on open questions in regards to raytracing dynamic, open world type environments

- brief discussion of difference between
[Moment Transparency](https://dl.acm.org/citation.cfm?id=3231585)and[Moment-Based Order-Independent Transparency](http://momentsingraphics.de/?page_id=210)approaches - small code samples to help to integrate the trigonometric Moment-Based Order-Independent Transparency technique

- look at different ray tracing scenarios and how they influence coherency between neighboring rays
- references to papers that investigate the issue in further details

If you are enjoying the series and getting value from it, please consider supporting this blog.

[Support this blog](https://donorbox.org/jendrikillner)