---
title: Graphics Programming 415
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-415/
author: Jendrik Illner
published: '2025-11-02'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- explains how dithering techniques trick spatial averaging in human vision to perceive more colors than are actually present
- covers ordered dithering using Bayer matrices and error diffusion methods like the Floyd-Steinberg algorithm
- discusses how dithering was historically necessary for limited color palettes but has now become primarily a retro aesthetic choice

![](../../assets/c5c2668b02f96ea0.png)


- comprehensive guide to installing and setting up GFXReconstruct for capturing and replaying Vulkan and DirectX 12 API calls
- covers both prebuilt binaries from the Vulkan SDK and building from source for custom configurations
- provides detailed troubleshooting steps and verification tests for both Vulkan and DirectX 12 workflows

![](../../assets/6bfd893e76ab0e5c.jpg)


- demonstrates how to build native inference pipelines on AMD GPUs using ONNX Runtime with DirectML execution provider
- explains sharing the DirectX 12 context between DirectML and user code to avoid CPU-GPU data transfers
- shows how to map resources directly into ONNX Runtime tensors for efficient preprocessing and postprocessing

![](../../assets/6592c107ffa5f428.png)


- introduces Simplygon’s clustered meshlet optimizer for dividing models into independently cullable parts with continuous LOD
- explains that streaming levels contain partial data requiring a combination of all lower levels for full detail
- provides complete implementation examples, including Python generation scripts and Unity C# visualization code

![](../../assets/1dd387f14acb091a.png)


- Pacific Graphics 2025 paper presenting an iterative algorithm to update lightmaps when objects are inserted or removed efficiently
- focuses on updating only the paths affected by scene changes rather than full recomputation
- implements an importance sampling scheme on a GPU suitable for interactive scene editing scenarios

![](../../assets/7c74e1da3550987f.png)


- SIGGRAPH Asia 2025 paper introducing a biased transmittance estimator with significantly reduced bias compared to naive ray marching
- applies the UMVU estimator based on nearly normally distributed optical depth estimates from stratified jittered sampling
- extends the theory to estimate MIS weights and proposes two new integrators combining MIS with improved transmittance estimation

![](../../assets/34f1994641870a0e.jpg)


- SIGGRAPH Asia 2025 paper presenting a method for rendering glint effects from microfacet geometry in constant time
- represents faceted geometry as a 4D point process on a multiscale grid to find highlight-causing facets efficiently
- supports various appearances, including anisotropic materials and individually colored particles, while converging to standard NDFs like GGX

![](../../assets/58f9c8b15d511bf5.png)


- video tutorial explaining how to work with depth information in Unity shaders
- covers fundamental concepts like the depth buffer, depth textures, and their use in effects
- provides practical examples and shader code for implementing depth-based visual effects

![](../../assets/2d65bd7254e74c2b.png)


- tutorial on implementing a transparent coat layer for physically based rendering (PBR) materials
- explains the principles behind simulating a transparent coating over a base material
- demonstrates the shader implementation and shows how it enhances the realism of surfaces like car paint or polished wood

![](../../assets/c0e29f93d08f655f.png)


- presents a BSC 2025 talk on Foliated Distance Fields for representing and rendering complex geometry
- discusses how this technique can be used for high-quality, real-time rendering of intricate surfaces
- explores the implementation details and performance characteristics of the approach

![](../../assets/4ffda3379942e682.png)

Thanks to [Eric Heines](http://erichaines.com/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.