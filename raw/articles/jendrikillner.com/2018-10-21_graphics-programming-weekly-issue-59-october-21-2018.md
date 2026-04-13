---
title: Graphics Programming weekly - Issue 59 — October 21, 2018
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-59/
author: Jendrik Illner
published: '2018-10-21'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the complete 3rd edition of Physically Based Rendering is now online for free
- the post explains the history of the book and decisions that led to making the book available for free
- authors can be supported on
[https://www.patreon.com/pbrbook](https://www.patreon.com/pbrbook)

![](../../assets/09badc539167ad45.jpg)


- summarizes voxel ray tracing implementation, memory and performance optimizations
- show the different artifacts that can be encountered and their solutions

![](../../assets/6afb39cf7880967d.png)


- next part in the Metal ray tracer series that adds support for multiple bounces to simulate global illumination
- implements importance sampling for diffuse BSDF

![](../../assets/15249f6914ea92da.png)


- extending the material system of the Metal raytracer so that multiple materials can be expressed and importance sampled correctly
- changes sampling heuristic to support multiple importance sampling. This enables both rough and mirror-like surfaces

![](../../assets/46697eb22cfd9620.png)

- 2-minute video summary of the “Position-Free Monte Carlo Simulation for Arbitrary Layered BSDFs” paper

![](../../assets/eacbed9ff5412847.jpg)


- overview of the strengths and weaknesses of different sampling techniques in ray tracing
- presents links to papers that present methods that are aimed at creating better-stratified sampling results

![](../../assets/72815530ce21fb29.png)


- stream that adds support for rendering meshes using Nvidia mesh shader extensions

![](../../assets/90c3671dd86536f5.png)


- during the stream, the mesh shader pipeline is optimized
- performance parity with the classical rasterization pipeline is achieved without GPU culling

![](../../assets/c9ec2426accfbd49.png)


- shows how to implement interior mapping using the Unity reflection probe system
- explains how to set up the model and environment to generate the required probes and how to apply the reflections to the windows

![](../../assets/61b437395c2f5248.png)


- rust version of the
[meshoptimizer](https://github.com/zeux/meshoptimizer)library is now available - the post explains how to setup Rust code to be able to compile, link and use existing C code from Rust

![](../../assets/0d03c0bd4e50e87e.png)


- the presentation explains how Global illumination has been implemented in the Godot engine
- talking about GI probe generation, deterministic light baking and the interacting with the shading pipeline

![](../../assets/d07cb38dfbbbabf9.png)


- walkthrough of a Godot shader that uses particles to spawn vegetation meshes based on height map and feature (biomes) map data

![](../../assets/632ff13f274476cc.png)


- a brief summary of the usage of premultiplied alpha using Vulkan
- pre-multiplication is done in the pixel shader, no texture pre-processing is used

![](../../assets/22972a3f52dfa367.png)


If you are enjoying the series and getting value from it, please consider supporting this blog.

[Support this blog](https://donorbox.org/jendrikillner)