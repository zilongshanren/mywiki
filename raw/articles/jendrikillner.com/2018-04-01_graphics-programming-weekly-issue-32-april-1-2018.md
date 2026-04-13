---
title: Graphics Programming weekly - Issue 32 — April 1, 2018
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-32/
author: Jendrik Illner
published: '2018-04-01'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

[Triangle Visibility Buffer](http://diaryofagraphicsprogrammer.blogspot.ca/2018/03/triangle-visibility-buffer.html?m=1) [[wayback-archive]](https://web.archive.org/web/20180402192008/http://diaryofagraphicsprogrammer.blogspot.ca/2018/03/triangle-visibility-buffer.html?m=1)

- in-depth walkthrough of the GPU triangle culling pipeline
- render into a single render RGBA8 render target, storing drawID + triangle ID
- memory usage comparison with deferred shading
- at shading time
- lookup the triangle ID from the render target
- interpolate vertex attributes at pixel position
- apply shading

- advantages of the technique
- less memory bandwidth required
- better memory coherence during shading
- more material variety, no need to store material data in gbuffers


[Re-Testing Vulkan Transform Data Handling Strategies](http://kylehalladay.com/blog/tutorial/vulkan/2018/03/28/SSBO-VS-Uniform-Buffer-2.html) [[wayback-archive]](https://web.archive.org/web/20180402192024/http://kylehalladay.com/blog/tutorial/vulkan/2018/03/28/SSBO-VS-Uniform-Buffer-2.html)

- performance comparison of constant buffer data stored in
- push-constants
- large UBO (device / host memory)
- large SSBO (device / host memory)

- on Nvidia UBO performs significantly better

[Octahedral Impostors](http://www.shaderbits.com/blog/octahedral-impostors) [[wayback-archive]](https://web.archive.org/web/20180402192049/http://www.shaderbits.com/blog/octahedral-impostors)

- better usage of texture space, workflow improvements
- overview of billboard techniques
- using either Hemi-Octahedron or full Octahedron
- how to blend between the different baked directions
- integration into UE pipeline

[substance PBR guide](https://www.allegorithmic.com/blog/pbr-guide-revised-and-expanded) [[wayback-archive]](http://web.archive.org/web/20180320130812/https://www.allegorithmic.com/blog/pbr-guide-revised-and-expanded)

[Improving the compression of block-compressed textures Revisited](http://cbloomrants.blogspot.ca/2018/03/improving-compression-of-block.html?m=1) [[wayback-archive]](https://web.archive.org/web/20180402191459/http://cbloomrants.blogspot.ca/2018/03/improving-compression-of-block.html?m=1)

- comparison of crunch (unity improved version) with DDS + general purpose compressors

[V-EZ brings “Easy Mode” to Vulkan](https://gpuopen.com/v-ez-brings-easy-mode-vulkan/) [[wayback-archive]](http://web.archive.org/web/20180331153811/https://gpuopen.com/v-ez-brings-easy-mode-vulkan/)

- abstraction layer on-top of vulkan
- implements automatic render barrier management, descriptor pools/sets, memory management, render passes, etc.
- aimed at CAD software, not games
- not open source at this point

- set of lessons explaining shader basics with unity
- how shaders are integrated into the unity pipeline

[Ray Tracing at GDC](http://www.realtimerendering.com/blog/ray-tracing-at-gdc/) [[wayback-archive]](https://web.archive.org/web/20180402191547/http://www.realtimerendering.com/blog/ray-tracing-at-gdc/)

- summary of available ray tracing articles

[Announcing Microsoft DirectX Raytracing!](https://blogs.msdn.microsoft.com/directx/2018/03/19/announcing-microsoft-directx-raytracing/) [[wayback-archive]](http://web.archive.org/web/20180325225149/https://blogs.msdn.microsoft.com/directx/2018/03/19/announcing-microsoft-directx-raytracing/)

- overview of DirectX raytracing api
- discussion of design decisions
- future direction

[PIX 1803.16-raytracing – DirectX Raytracing support](https://blogs.msdn.microsoft.com/pix/2018/03/19/pix-1803-16-raytracing-directx-raytracing-support/) [[wayback-archive]](http://web.archive.org/web/20180319230100/https://blogs.msdn.microsoft.com/pix/2018/03/19/pix-1803-16-raytracing-directx-raytracing-support/)

- pix supports DirectX Raytracing (DXR) API calls
- shows details about resources
- visualization of acceleration structure
- showcase of demos that support DXR

[Introduction to NVIDIA RTX and DirectX Raytracing](https://devblogs.nvidia.com/introduction-nvidia-rtx-directx-raytracing/) [[wayback-archive]](http://web.archive.org/web/20180330072238/https://devblogs.nvidia.com/introduction-nvidia-rtx-directx-raytracing/)

- more in-depth explanation of how the DXR API work
- ray generation -> intersection / any hit -> closest hit / miss

[An Idea: Raytracing Lookup Tables](https://blog.demofox.org/2018/03/24/an-idea-raytracing-lookup-tables/) [[wayback-archive]](http://web.archive.org/web/20180324230707/https://blog.demofox.org/2018/03/24/an-idea-raytracing-lookup-tables/)

- instead of using textures use adaptive-meshes to represent data where required, raytrace against that mesh to get the lookup value

[PIX 1803.25 – GPU Occupancy, CPU sampling, automatic shader PDB resolution, and more](https://blogs.msdn.microsoft.com/pix/2018/03/27/pix-1803-25/) [[wayback-archive]](https://web.archive.org/web/20180402191708/https://blogs.msdn.microsoft.com/pix/2018/03/27/pix-1803-25/)

- allows to see occupancy broken down into different render pipeline stages (NVidia only for now)
- improved CPU profiling
- more memory usage information (command allocators, PSO, descriptor heaps)
- geometry shader and DXR debug support

[Daily Pathtracer Part 0: Intro](http://aras-p.info/blog/2018/03/28/Daily-Pathtracer-Part-0-Intro/) [[wayback-archive]](https://web.archive.org/web/20180402191726/http://aras-p.info/blog/2018/03/28/Daily-Pathtracer-Part-0-Intro/)

- series about small path tracing experiment with C++, C# and unity C# burst

[GPU Ray Tracing in One Weekend](https://medium.com/@jcowles/gpu-ray-tracing-in-one-weekend-3e7d874b3b0f) [[wayback-archive]](http://web.archive.org/web/20180331230152/https://medium.com/@jcowles/gpu-ray-tracing-in-one-weekend-3e7d874b3b0f)

- unity implementation of a compute shader ray tracer
- random points on sphere stored in texture
- ray scheduler, store persistent ray state in gpu buffer and iterate, no recursion
- depth of field
- scene change handling

[Hello World: OctaneRender 4 is here](https://render.otoy.com/forum/viewtopic.php?f=33&t=66013) [[wayback-archive]](https://web.archive.org/web/20180402191756/https://render.otoy.com/forum/viewtopic.php?f=33&t=66013)

- free option for single PC available
- Brigade Engine integration (real time path tracing engine)
- many speed improvements

[“Ray Tracing Gems” Book Call for Participation](http://www.realtimerendering.com/blog/ray-tracing-gems-book-call-for-participation/) [[wayback-archive]](https://web.archive.org/web/20180402191756/https://render.otoy.com/forum/viewtopic.php?f=33&t=66013)

- new book, call for authors
- small overview of raytracing history