---
title: Graphics Programming weekly - Issue 39 — May 20, 2018
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-39/
author: Jendrik Illner
published: '2018-05-20'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

#
Graphics Programming weekly - Issue 39 — May 20, 2018

- implements foveated rendering through usage of log-polar transformation
- gbuffer is written as normal, attributes transformed into sub-resolution textures using a log-polar transformation
- shading is done in log-polar space before the results are transformed back into Cartesian space



- Intro to sampling theory and how different sampling patterns influence the aliasing that can be observed
- explanation of why the default D3D11 MSAA has been chosen



- description of a shader effect that dissolves triangles outside of a spherical effect range



- slerp between two orientations takes the shortest path on a 4D hypersphere
- author wants the shortest arc in 3D instead
- decomposes rotation into swing and twist operations
- these are interpolated independently and concatenated to form the final rotation



- start of series that will look at lack of multi scattering in common analytical BSDFs and solution
- only modelling single scattering causes significant energy loss on rough surfaces
- post shows visual example that up to 60% of energy can be lost



- derivation of the multi-scattering GGX BRDF
- provides source code and precomputed lookup tables

- explains what shader variations are
- how to compute the amount of variations created for a shader
- how unity decides what variations to include
- Unity 2018.2 beta adds the possibility to control shader variation compilation from a C# script



- new image diff option allows visualization of pixel difference between compressed / uncompressed textures
- adds model optimizations (vertex cache, overdraw, vertex prefetch optimizations)
- draco compression support



- tool that allows to only include vulkan functionality that you need
- comparison of header sizes and influence on compile time, startup time



- introduction into vectors as functions and dual space
- how to transform dual vectors


- uses ShaderGen to write shaders in C# and compile them into the target shader language for D3D11, Metal, OpenGL and vulkan


- website that allows compilation of shaders with a multitude of shader compilers and inspect the available outputs
- possibility to chain compilers together



- tutorial how to use the VK_EXT_debug_utils extensions
- combines old debug extensions into a unified one and adds more possibilities
- allows more details to be reported from the validation layer and tools that support the extension



- technical details about the font rendering algorithm used in
[slug](http://sluglibrary.com/)



- presents one method to derive the slerp formula for quaternions



- discusses issues with composability, how complexity poses a problem of sharing research results
- list of frameworks for research
- how the scriptable render pipeline of unity allows more flexibility and still hides most of the complexity



- discusses problems with using a texture atlas
- set of scripts to help with the creation, management and usage of texture arrays in unity



- technique that helps to reduce problems of disappearing geometry for alpha tested geometry
- no runtime changes required, only changes the way mips are generated