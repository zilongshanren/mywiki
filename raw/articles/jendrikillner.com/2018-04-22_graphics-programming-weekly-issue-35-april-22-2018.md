---
title: Graphics Programming weekly - Issue 35 — April 22, 2018
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-35/
author: Jendrik Illner
published: '2018-04-22'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

#
Graphics Programming weekly - Issue 35 — April 22, 2018

- April 30th, Vulkan Developer Day in Montreal, hosted by Ubisoft


- UVs map into a gradient texture
- to change the colors the UVs are adjusted to point to other sections in gradient texture


- overview of the shader authoring format
- shader input parameters are defined without thinking about how they are bound
- passing data between shader stages is abstracted
- giving the system flexibility to pack as required



- microarchitectural details of the NVIDIA Volta architecture
- registers are divided into two 64 bit banks
- reduction of bank conflicts with register remapping can improve performance by 15%

- shorter latency for shared memory atomics


- MatCap texture contains lighting information for all camera space normals
- needs to be recalculated when camera direction changes


- uses a texture based and camera facing quad approach instead of a post-processing bloom
- lighting for terrain rendered into a low-res light map, sampled per-fragment
- terrain is rendered at 720p, up-scaled to 1080p


- algorithm to sum regions from arrays or grids in constant time
- need larger storage format, increase depends on largest range that needs to be summed
- compatible with bilinear filtering for sub-pixel values


- unity graphics team is looking to gather feedback to improve the roadmap

- performance numbers for all implementations with latest changes

- current approach recursively processes a single ray until it terminates
- new approach calculates each step for all rays in seperate passes
- memory read seems to be limiting factor, shows a few optimizations for that


- available with AMD vega architecture
- pack two FP16 into FP32 register
- reduce ALU instructions count, reduce VGPR usage

- how to detect FP16 code generation in FXC disassembly and GCN ISA output
- discussion of pitfalls and common use-cases
- how to deal with FP16 constants


- combination of ripples and streaking effect
- blending between the two effects based on surface orientation
- this post covers the implementation of the streaking effect


- many BC7 encoders compress all channels equally
- for color textures, errors in red and blue are less noticeable
- YCbCr color space allows better compression by reducing the number of bits used for chroma


- discusses issue with the ispc implementation
- compression has quality problems with grayscale textures


- survey of methods utilizing Monte Carlo for light transport in participating media


- list of resources for beginners aimed at shader toy like graphics programming


- A C++14/C++17 header-only library for simple, efficient, and robust serialization/deserialization of glTF 2.0

- library that allows access to GPU performance data on intel GPUs