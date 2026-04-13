---
title: Graphics Programming weekly - Issue 21 — December 17, 2017
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-21/
author: Jendrik Illner
published: '2017-12-17'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

[Unreal Engine 4 Rendering Part 1: Introduction](https://medium.com/@lordned/unreal-engine-4-rendering-overview-part-1-c47f2da65346) [[wayback-archive]](https://web.archive.org/web/20171212191025/https://medium.com/@lordned/unreal-engine-4-rendering-overview-part-1-c47f2da65346)

- focus on the deferred shading pipeline
- settings required for good development experience
- how data is passed from updated thread -> engine thread -> gpu
- how shader system is structured
- binding between HLSLS and C++
- how the correct shader variation is picked

[Deferred Signed Distance Field rendering](https://interplayoflight.wordpress.com/2017/12/12/deferred-signed-distance-field-rendering/) [[wayback-archive]](http://web.archive.org/web/20171212191132/https://interplayoflight.wordpress.com/2017/12/12/deferred-signed-distance-field-rendering/)

- using a fullscreen pass, render the SDF into the g-buffer
- outputting custom depth for correct depth sorting

[State of Roblox graphics API across all platforms - December 2017](https://gist.github.com/zeux/f09ec9d0effae8f6904e7dead226fb58) [[wayback-archive]](https://web.archive.org/web/20171212191219/https://gist.github.com/zeux/f09ec9d0effae8f6904e7dead226fb58)

- on windows 77% can use D3D 11+, still 3% on D3D39
- windows store, 10% for D3D10
- 52% can run metal on mac and 86 on iOS
- android very fragmented across ES 3.X and 2.0, vulkan

[Vulkan: Pipelines and Render States](http://ourmachinery.com/post/vulkan-pipelines-and-render-states/) [[wayback-archive]](https://web.archive.org/web/20171217234837/http://ourmachinery.com/post/vulkan-pipelines-and-render-states/)

- support on-demand, VkPipeline creation at runtime only as fallback option
- most should be created offline

- how to handle this with multithreaded rendering
- Render State Override Blocks
- allow changes to some dynamic states at runtime


[A Simple Device Memory Allocator For Vulkan](http://kylehalladay.com/blog/tutorial/2017/12/13/Custom-Allocators-Vulkan.html) [[wayback-archive]](http://web.archive.org/web/20171213153149/http://kylehalladay.com/blog/tutorial/2017/12/13/Custom-Allocators-Vulkan.html)

- memory heaps and types
- can’t mix different types into one heap

- vkAllocateMemory overview
- guaranteed to return memory aligned to the largest required alignment for any resource
- allocation sizes differ depending on hardware
- driver specifies maximum number of allocations that can be done

- when sub-allocating

- need to respect Buffer-Image Granularity to avoid aliasing
- need separate pool for each allocation type
- only allowed to map allocation once, even when sub-allocating different objects within


[Deferred Path Tracing By Enscape](https://gpuopen.com/deferred-path-tracing-enscape/) [[wayback-archive]](http://web.archive.org/web/20171217094718/https://gpuopen.com/deferred-path-tracing-enscape/)

- path traced real time global illumination that can converge to offline quality
- using Radeon Rays for BVH construction and traversal
- using g-buffer as replacement for primary rays
- try to cast the diffuse rays in screen space, only if no hit is found trace using the BVH
- ray bundling based on direction
- BVH is streamed based on estimated visual importance weighted against their BVH cost
- bake lighting into BVH per-vertex
- sun is evaluated during traversal

- filtering with temporal accumulation buffers

presentation here: [Real-time path tracing using a hybrid deferred approach](https://enscape3d.com/wp-content/uploads/2017/12/23026-real-time-path-tracing-using-a-hybrid-deferred.pdf) [[wayback-archive]](https://web.archive.org/web/20171214171616/https://enscape3d.com/wp-content/uploads/2017/12/23026-real-time-path-tracing-using-a-hybrid-deferred.pdf)

[Learning DirectX 12 – Lesson 1](https://www.3dgep.com/learning-directx12-1/) [[wayback-archive]](https://web.archive.org/web/20171215184631/https://www.3dgep.com/learning-directx12-1/)

- very in-depth tutorial about D3D12
- win32 window creation
- Query the GPU adapters
- Create in d3d12 device, command queue, swap chain, command allocator and command lists
- Handle GPU synchronization
- Handle resizing
- Handle full-screen toggling


[Crunch compression of ETC textures](https://blogs.unity3d.com/2017/12/15/crunch-compression-of-etc-textures/) [[wayback-archive]](https://web.archive.org/web/20171215202838/https://blogs.unity3d.com/2017/12/15/crunch-compression-of-etc-textures/)

- explanation of DXT1 compression
- detailed explanation how crunch compression works
- and what improvements have been done

[Metal Gear Solid V - Graphics Study](http://www.adriancourreges.com/blog/2017/12/15/mgs-v-graphics-study/) [[wayback-archive]](http://web.archive.org/web/20171215175959/http://www.adriancourreges.com/blog/2017/12/15/mgs-v-graphics-study/)

- SSAO is done with two passes
- Line Integral SSAO + Scalable Ambient Obscurance

- uses local irradiance spherical maps for global illumination

- one bounding-box-shaped mesh representing the volume of influence of the zone
- additively blends the irradiance from all zones

- does tone-mapping early, right after g buffer lighting
- depth of field
- done using a sprite scattering approach
- on near-field and far field separately
- results blended together


- this was discussed in
[Issue 18](https://jendrikillner.bitbucket.io/post/graphics-programming-weekly-issue-18/) - now the video has been released

- import / export GLTF 2.0

- open source showing the implementation of the Spherical Harmonic Lighting: The Gritty Details paper
- shader toy
[https://www.shadertoy.com/view/XtlBzs](https://www.shadertoy.com/view/XtlBzs)

- now supports pix markers
- barriers and transitions now show reason why they are executed