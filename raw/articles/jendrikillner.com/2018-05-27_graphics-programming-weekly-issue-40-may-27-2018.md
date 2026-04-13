---
title: Graphics Programming weekly - Issue 40 — May 27, 2018
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-40/
author: Jendrik Illner
published: '2018-05-27'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

#
Graphics Programming weekly - Issue 40 — May 27, 2018

- many optimization lessons learned for mobile
- how to deal with shader preloading
- discussion of error detection in automated image comparison tests
- increased game brightness to reduce the use of display backlights to save battery and reduce heat
- using raytracing to remove aliasing in special cases
- improvements to blue noise algorithm


- discussions of problems with old occlusion culling systems
- renders occluders in a pre-pass, uses the depth information to cull instances
- how to implement culling against the depth buffer, remove culled instance from the stream
- stream compaction implementation
- extend the system to handle LOD, materials and manual vertex fetching
- performance results on Nvidia and Intel


- overview of how to generate a SDF in unity
- per object SDF at build time
- global SDF aggregation at runtime


- introduction to shaders workshop in Montreal
- focused on the node-based shader pipeline of Unreal


- discussion of characteristics of different ways to pass CPU generated data to the GPU using OpenGL
- persistent memory (GL_ARB_buffer_storage)
- client arrays
- vertex buffer object (VBO)



- overview of SPH (Smooth Particle Hydrodynamics)
- how it’s implemented in a compute shader
- explanation of a sorted grid acceleration structure


- how the fractal raytracer was implemented on the GPU
- evaluating the fractal, ray marching and photon simulation


- discussion of a unique art style rendering technique
- the character is represented from axis aligned voxels
- voxels are created/destroyed on a quantized world space grid as the character moves through the world


- adds supports for a basic material system with lambert diffuse + phong specular
- explanation of importance sampling


- list of resource for beginners into graphics programming


- implementation details for reflections, translucency, transparency, shadows
- global illumination uses surfels with world space accumulation


- explanations of how to get started with shader programming with unity
- takes the unity toon shader as the starting point to explain concepts and provide a gentle introduction into making modifications to it


- adds support for GPU tracking system that allows to enable/disable features based on the GPU used

- now includes present events in the system activity view
- explanations for why the driver had to insert barriers