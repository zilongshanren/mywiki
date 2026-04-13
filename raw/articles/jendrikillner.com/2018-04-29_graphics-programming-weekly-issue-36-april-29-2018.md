---
title: Graphics Programming weekly - Issue 36 — April 29, 2018
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-36/
author: Jendrik Illner
published: '2018-04-29'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

#
Graphics Programming weekly - Issue 36 — April 29, 2018

- summary of
- cloud modeling and authoring system
- lighting model

- high level overview of the implementation


- environment lighting is using several distributed area lights
- distribution / strength is adapted to the environment
- implementation of importance sampling using varying step sizes for ray marching steps


- investigation of relation between linear interpolation and curve representations


- D3D11 extensions to simplify use of Lens Matched Shading and Multi-Res Shading
- short overview of the concepts and how the API works


- vulkan function calls pass through several layers until the actual function is executed
- looks at the disassembly to evaluate the cost of this (between 1-5%)
- and how to bypass many layers to reduce the overhead


- 100% dynamic lights, 16 shadow maps in 4kx4k atlas
- gbuffer breakdown
- stores material index in gbuffer, indexing into structured buffer for material information

- deferred decals have problems with depth discontinuities because of wrong mip selections
- use mip0 when depth discontinues are found around the pixel

- object decals, blending arbitrary meshes into the gbuffer
- working on bindless decals, follow the same pattern as clustered deferred lighting


- implementation of a buffer based (breadth first) approach for the raytracer
- looking at synchronization issues, performance
- brief look at the NVidia nsight tool


- overview of what error metric he uses when working/comparing encoders


- shows effect of different ray marching step sizes for screen space reflections
- diffuse reflections approximation with mip selection vs reference implementation with many samples


- comparison of backface culling efficiency for cluster cone, 64-triangle clusters


- discusses 3 different approaches for implementing thermal erosion on a height field based terrain


- supports perceptual metric for compression
- designed for opaque textures


- descriptor types in vulkan vs D3D12
- how to specify resource bindings for vulkan in HLSL
- memory layout rules