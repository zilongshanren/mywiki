---
title: Graphics Programming 427
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-427/
author: Jendrik Illner
published: '2026-02-08'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- details the development journey of Adobe’s Substance Modeler from its origins as Oculus Medium to a professional desktop sculpting tool
- describes the sculpting engine’s voxel-based SDF architecture with marching cubes tessellation and the rendering engine’s COW-based deduplication for handling billions of polygons
- discusses the challenges of supporting both VR and desktop workflows

![](../../assets/af4fa0c493a85ff8.png)


- tutorial showing how to blend between two terrain layers based on height
- covers practical remapping and smoothing to avoid hard transitions
- part of a longer series of terrain shading

![](../../assets/88af3fbf7c8216ac.png)


- introduces the Khronos Working Group’s new strategy to combat API complexity through complete subsystem replacements
- presents VK_EXT_descriptor_heap as the first implementation of this approach, fully replacing the descriptor set subsystem with a simpler memory-based model where descriptors are just data
- emphasizes broad industry collaboration across the working group and invites feedback before finalizing as a KHR extension

![](../../assets/31ef79209c1b4ec4.png)


- concise guide to investigating performance problems: start with profiling and measurement to find real hotspots rather than guessing
- surveys practical techniques (data-oriented layouts, instancing, background workers, frame spreading, cache-friendly changes) and gives small, actionable examples
- emphasizes pragmatic trade-offs, verifiable wins and beware optimizations that appear to help for the wrong reasons

![](../../assets/42996a018e02c00c.png)


- release candidate for KHR_gaussian_splatting to store 3D Gaussian splats in glTF
- describes Gaussian splatting (sparse, optimized 3D points with position/scale/orientation/color/opacity) as a fast, scalable format suited to geospatial capture, digital twins and photoreal 3D capture workflows
- designed to be extensible and compression-friendly

![](../../assets/20a69ad58d9d2b1d.png)


- traces the evolution from SIMD to SIMT execution models, starting with NVIDIA’s G80 architecture in 2006
- explains how SIMT preserves SIMD efficiency while managing divergent control flow through hardware-controlled serialization and masking of inactive threads within warps
- shows how AMD, Intel, and newer GPU vendors adopted similar thread-based execution models
- modern APIs like Vulkan, DirectX 12, and Metal provide subgroup abstractions that map to underlying SIMT hardware

![](../../assets/f4cf06154fea8d47.png)


- introduces Nanite Tessellation as a system for dynamically tessellating and displacing meshes using shader graphs, extending Nanite’s virtualized geometry capabilities
- discusses the motivation for geometry amplification including data compression advantages of displacement maps and improved artist workflows for procedural content
- explains how displacement is particularly valuable for film-style workflows as well as games requiring scalability across platforms

![](../../assets/5da4abf386944756.png)


- presents a talk challenging the perception that Vulkan is overly complex and not worth engaging with as an indie developer
- argues that proper GPU abstraction design matters more than the choice of API
- demonstrates how to build fast, flexible, and simple rendering systems in Vulkan

![](../../assets/2d182aaf46484fe0.png)


- examines practical aspects of normal map compression, including the evolution from DXT5/BC3 swizzled encodings to BC5’s capabilities
- discusses Z reconstruction methods and tangent space discontinuities
- presenting solutions for UNORM encoding offsets to represent flat normals at UV seams properly
- explains the tradeoffs between UNORM and SNORM formats

![](../../assets/94e7132d1a0cdb01.png)


- investigates how decoder implementations and chroma upsampling post-processing affect perceived image quality beyond encoder efficiency alone
- tests various decoders, including FFmpeg, jpegli, ImageMagick, dwebp, and dav1d, with different chroma handling strategies
- demonstrates that filtered FFmpeg decoding with Lanczos scaling and accurate chroma interpolation achieves efficiency improvements compared to baseline approaches

![](../../assets/3755a6f63586689b.png)


- analyzes and replicates the Shadowglass technique for achieving stable first-person pixel art without shimmer by rendering to low-resolution cubemaps from fixed positions
- implements reprojection using cubemap depth buffers to raymarch and offset samples based on camera movement, creating parallax effects while maintaining pixel stability
- describes optimizations including different cubemaps for varying distances and resolutions
- presents how to handle transitions between the cubemaps

![](../../assets/eedf6abbc43d0157.png)


- AMD technical report introducing ray tracing fundamentals and a HIP-based GPU implementation
- highlights Orochi for runtime HIP/CUDA backend switching
- explains core algorithms (ray-triangle intersection, BVH construction and traversal, ambient occlusion, path tracing and next-event estimation) and performance considerations
- provides code examples

![](../../assets/5606d9fb7f3e6af7.png)

Thanks to [Nathan Reed](https://www.reedbeta.com) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.