---
title: Graphics Programming weekly - Issue 2 — August 6, 2017
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-2/
author: Jendrik Illner
published: '2017-08-06'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

this course we will discuss various radically different ways to rethink texture mapping that have been proposed over decades, each offering different advantages and trade-offs


Dolphin will use the already compiled Ubershaders to immediately render the effect without stuttering while still compiling the specialized shader in the background


interesting exercise of measuring the actual behavior of given index sequences on real hardware, and trying to model several possible approaches hardware could take to understand the behavior better


takes ideas from Metal and D3D11, plus a few ideas from D3D12/Vulkan, and wraps them into a simple C API


This course picks up where the last ones left off, explaining not only the basic theory underpinning these recent advances, but also presenting a detailed and concrete look at their implementations.


Mesh color textures convert the mesh color data to a format that can be efficiently used by the texture filtering hardware on current GPUs. Utilizing a novel 4D texture coordinate formulation, mesh color textures can provide correct filtering for all mipmap levels and eliminate artifacts due to seams.



- Allows a SPIR-V usage instead of GLSL
- KHR_parallel_shader_compile extension is about allowing multiple shader compile threads
- and many more things

This subgroup is tasked with developing specifications, open-source library code and tools, together with conformance tests to define and support the set of Vulkan capabilities that can be made universally available across all major platforms, including those not currently served by Vulkan


will present a practical implementation of the multilayered PBR material rendering system developed at Infinity Ward



- clustering data structures
- scalarization
- clusterng algorithmn
- rasterization based culling


- approximates the multiple-scattering effects missing from the microfacet lobe
- Thin Surface BSDF
- Subsurface Scattering
- Coatings


- classification of clouds
- improvements upon last years system, artistically authoring volumetric cloudscapes in less then 2 ms (PS4)
- density based model
- houdini noise generator:
[http://bit.ly/nubisnoisegen]- want them to appear to be changing without altering the larger structure of the cloudscape
- weather system
- Cloud Lighting Model
- ray march result post processing
- light shafts


- GGX spherical area light
- Height fog (merging artistic fog with bruneton based atmospheric scattering model)
- AA in 1080p (Temporal FXAA with sample tweaks)
- 2160p checkerboard on PS4 Pro (without any native-res hints, noval packing technique)

glTF 2.0 has given us a fantastic chance to standardize a smooth workflow between 3D modelling software and game engines



- points out many problems, and discusses possible ideas
- Next problem to solve is compute
- Want to take real-time graphics further
- Need to render “smarter”


- overview of the techniques
- challenges
- unsolved problens


- Definition of a physically based material
- Current and future real-time material model
- Need to render “smarter”

real-world techniques for intermediate and advanced WebGL developers by assembling contributions