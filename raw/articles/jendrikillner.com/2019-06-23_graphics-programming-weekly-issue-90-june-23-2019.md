---
title: Graphics Programming weekly - Issue 90 — June 23, 2019
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-90/
author: Jendrik Illner
published: '2019-06-23'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- explains gamut mapping techniques
- difference perceptual and clipping techniques
- shows how gamut mappings are derived

![](../../assets/d146d7e1ddf347a3.png)

- shows how the fog in The Witcher 3 has been implemented
- combines aerial fog and an artist-controlled fog coloring based on a gradient from 3 colors (front to back)
- uses AO information to darken the fog in occluded areas

![](../../assets/d45ac7ba3041816b.jpg)


- list of sessions from SIGGRAPH 2019 that are related to ray tracing techniques

![](../../assets/5a3556100eb62d24.png)

- new extensions in AMD driver
- VK_EXT_full_screen_exclusive, allows application to enter fullscreen mode such as IDXGISwapChain::SetFullscreenState
- VK_EXT_separate_stencil_usage allows separate depth and stencil states
- VK_AMD_display_native_hdr, better HDR support for FreeSync 2 monitors without requiring AMD libraries

![](../../assets/4453e69e6218a86c.jpg)


- support for GPU timing data in the new timing capture view
- a lot of GPU capture improvements

![](../../assets/fbcaaf5d74f2870d.png)

- new glint integrator for specular surfaces using multiple-scattering patch-based BRDF
- addresses energy loss introduced from classical normal mapping
- uses normal maps and second moments of slopes as in
[LEADR mapping](https://hal.inria.fr/hal-00858220v1/document)

![](../../assets/6b38d91dfbaa5779.png)


- shows a new version of voxel-based path-tracing based graphics engine
- provides an overview of the implementation

![](../../assets/568fe780cc2fcc52.png)


- new path tracing sampler techniques
- distributed per-pixel samples so that errors are distributed as blue noise in screen space
- provides C++ source code
- comparison against other methods at various sample counts

![](../../assets/6858e8cea08df791.png)


- the paper builds on the techniques described in the previous article
- introduces a temporal algorithm that locally permutes the pixel sequences
- improves error distribution for a series of frames

![](../../assets/0f7dad88643f2bf8.png)


- describes how to support unbounded arrays of textures in Vulkan
- presents two techniques to solve validation errors
- first fills unused slots with a know valid texture descriptor
- second shows the required extensions to enable partially filled descriptor sets

![](../../assets/3ef4023446d1cf0a.png)


- shows how to implement raytracing against a Signed Distance Field (SDF)
- extends this to use sphere tracing

![](../../assets/9dddffe7caedf9a9.png)

- a master thesis that describes a progressively path-traced solution for indirect illumination lightmaps on the GPU
- covers parameterizing geometry into lightmaps, improving coherence in a path tracer, reducing variance and spherical basis functions
- presents a new way to store diffuse and specular irradiance using an Ambient Dice encoding scheme (additional post below)

![](../../assets/f986efd83720216d.png)


- explains how to extend the Ambient Dice basis function to store and evaluate both diffuse and specular irradiance

![](../../assets/ab615654a5ba7797.jpg)

- explains how branching on GPUs is commonly implemented
- explains what divergence is, impact on performance and how to reduce it
- GPUs use an execution mask to hide results from inactive threads
- shows how this looks in GCN ISA and AVX512

![](../../assets/5c82c3bdb0be4d2d.png)


- describes the surface gradient framework
- a framework for robust processing of height maps, height volumes, and normal maps
- explains the Preliminaries (Tangent Frame, Height Maps, and Volumes, Wrinkled Surfaces)

![](../../assets/0a11283b36992a11.png)

Thanks to [Jon Greenberg](https://twitter.com/Jontology) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.