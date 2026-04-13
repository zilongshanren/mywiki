---
title: Graphics Programming weekly - Issue 366 - November 17th, 2024
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-366/
author: Jendrik Illner
published: '2024-11-17'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the tool allows the visualization of Monte Carlo samplers
- many different methods can be selected
- allows the exploration of settings through interactive controls

![](../../assets/23f715de910ac2a3.png)

- the article provides an overview of Gaussian Splatting support in V-Ray
- explains the technique on a high level, advantages, and limitations
- presents an example of how objects can be added to scanned scenes and interact with the scene around them

![](../../assets/9f4bbdde7fafa64b.png)


- the paper presents a framework for volumetric scene prefiltering and level-of-detail rendering
- to improve geometric fit of voxel approximations, it introduces a truncated ellipsoid primitive
- shows how the technique allows accurate LoD rendering closely matching the ground truth at all scales.

![](../../assets/1e0a150d1eb7db83.png)


- keen games released a snapshot of their Vulkan Backend implementation
- code is not compiling as it depends on code that has not been published
- meant as a reference for others to see how concepts can be implemented

![](../../assets/b0660d3852277d54.jpg)


- the article explains the changes that have been made to the Nanite-like Virtual Geometry system for Bevy
- discusses software rasterization, improved LOD selection, memory reduction techniques, as well as performance optimizations
- provides links to the various PRs and explains these, making it easy to follow along

![](../../assets/a1cb8e0ef785778c.png)


- AMD released a shader toy-like application that allows exploration of D3D12 Work graphs
- the application is compatible with D3D WARP (aka CPU emulation of D3D12)
- provides tutorials of different complexity to showcase different capabilities
- documented source code for all tutorials is provided

![](../../assets/260ec7e9a724e8b1.png)


- the blog post provides a high-level overview of the hair rendering technique used in Dragon Age that uses strand-based rendering
- presents that 6.5ms (at 30fps mode) and 3ms for 60fps are reserved for hair rendering
- shows a demo video to present the technique results

![](../../assets/ef6b335554b413e1.jpg)


- the slides discuss the design of the C4 Engine
- present how the engine has been separated into separate components and what these components do

![](../../assets/9c3c415cf3e8529b.png)

- the presentation shows how to use HLSL Wave Intrinsics
- explains what Wave Intrinsics are, what they can be used for, and the limitations
- shows practical use-cases and how to implement example solutions
- presents the generated code on AMD hardware and discusses pitfalls

![](../../assets/be36f3254f355995.png)


- the Bluesky thread presents a detailed look at how to optimize a 3x3x3 blur
- shows different stages of the optimization process
- published performance numbers for the different optimized implementations
- additionally presents how to use voxels to visualize the algorithm implementation

![](../../assets/9f9fccca30ec9f3a.png)

Thanks to [Deepak Surti](https://deepaksurti.com) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.