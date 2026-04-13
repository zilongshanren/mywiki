---
title: Graphics Programming 422
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-422/
author: Jendrik Illner
published: '2026-01-04'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- companion document to the OpenPBR specification providing deeper implementation guidance for the standardized uber-shader
- covers slab-based layering, statistical mixing, and microfacet theory with mathematical derivations and code examples
- discusses physical components including metallic, dielectric, subsurface substrates, thin-film iridescence, and planned extensions like hazy specular reflection

![](../../assets/0b59b46a3d8aaa53.jpg)


- analysis of GPU market share and D3D12 feature support using Steam Hardware Survey and D3d12infoDB
- examines adoption rates for DXR, Shader Model 6.6-6.8, Mesh Shaders, Enhanced Barriers, VRS, and Work Graphs across GPU architectures

![](../../assets/f4e7e8a37fcc0978.png)


- announces ACM’s transition to fully open access publishing model
- makes all ACM research content freely available

![](../../assets/f274deda16c31ac6.jpg)

- advocates for bindless rendering as an accessible gateway to GPU-driven rendering with lowered complexity
- demonstrates how bindless resources enable event-driven draw management with reduced CPU involvement
- proposes treating GPU data as database tables with compute shaders only modifying tables for simplified renderer architecture

![](../../assets/e6be7139bfd60cb0.png)


- extensive tutorial demonstrating modern Vulkan 1.3 programming with simplified features like dynamic rendering and buffer device address
- creates functional 3D rendering application with textured meshes, lighting, and user interaction in single-file example
- leverages recent API improvements including descriptor indexing, synchronization2, and Slang shader language to reduce verbosity

![](../../assets/641e2a8f687bc71a.png)


- presents practical techniques for working with axis-aligned bounding boxes including slab-based min/max representation for simpler merging operations
- demonstrates an approach to extract individual vertex coordinates from AABB using vertex index without floating-point math
- explains efficient ray-AABB intersection test

![](../../assets/260aa2e83451ce6c.png)


- educational course implementing differentiable triangle rasterization from scratch inspired by tiny renderer
- teaches inverse rendering techniques allowing 3D scene parameters to be learned from 2D images through gradient-based optimization
- covers automatic differentiation, discontinuity handling, and practical applications including optimizing geometry, materials, lighting, and camera parameters

![](../../assets/825404b6b6f25dd7.png)


- analyzes limitations of traditional micro-occlusion texture baking for material-level direct lighting occlusion
- compares micro-shadowing approaches from Naughty Dog and Activision with analytical formulas and visual results
- proposes improved analytical alternative using cone angle calculations with better handling of full occlusion and roughness variation

![](../../assets/a1c0d629ad82d36a.jpg)


- proposes alternative diffuse lighting formula that avoids completely black unlit areas
- provides simple one-liner solution for test projects that preserves geometric detail without complex lighting setups

![](../../assets/60236444d0d4abe9.png)


- presents a prototype implementation of printf debugging for HLSL shaders
- uses compile-time string table extraction and builtin functions to convert format strings into buffer offsets
- implemented entirely in HLSL using variadic templates

![](../../assets/02b14bcefb8c7f7e.png)

- conference program has been released
- Combined passes for the Shading Languages Symposium + Vulkanised are available
- Early bird ticket sales are still available

![](../../assets/97978ce65cf6b79e.jpg)


- presentation detailing the path-traced global illumination system in idTech8
- discusses optimizations for dynamic lighting, material complexity, and scene complexity

![](../../assets/4b349ad1d6cd8cfc.png)

- video tutorial series introducing BGFX, a cross-platform graphics rendering library
- covers setup, basic rendering concepts, and how to create simple graphics applications

![](../../assets/857bfb1e6691de61.png)

- video tutorial showing how to create holes or cutouts in terrain geometry
- demonstrates shader techniques for masking and clipping terrain based on texture data
- covers practical applications like caves, tunnels, or dynamic terrain destruction

![](../../assets/e162e26977659695.png)

- details improvements to Bevy’s dynamic raytraced lighting system in version 0.18
- adds specular material support with GGX BRDF including importance sampling and proper handling for mirror surfaces
- fixes energy loss bugs, reduces ReSTIR resampling correlations, and improves world cache performance with adaptive blend factors and lifetime management

![](../../assets/d277ef5bb2f4b3ea.png)

Thanks to [Aras Pranckevicius](https://aras-p.info/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.