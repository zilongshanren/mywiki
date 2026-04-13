---
title: Graphics Programming weekly - Issue 12 — October 15, 2017
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-12/
author: Jendrik Illner
published: '2017-10-15'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

[Forward+ decal rendering](https://turanszkij.wordpress.com/2017/10/12/forward-decal-rendering/amp/) [[wayback-archive]](https://web.archive.org/web/20171016024515/https://turanszkij.wordpress.com/2017/10/12/forward-decal-rendering/amp/)

- goals: avoid additional geometry, and don’t increase draw call count
- extend the light structure to also support decals
- cull the decals, sort them and apply them in the object shader just as lights
- still has a few open problems, for example mip selection
- possible solution: calculate the UV gradients manually as in
[this example](https://github.com/TheRealMJP/DeferredTexturing/blob/master/BindlessDeferred/Shading.hlsl#L193)

- possible solution: calculate the UV gradients manually as in

[Depth proxy transparency rendering](https://eidosmontreal.com/en/news/depth-proxy-transparency-rendering) [[wayback-archive]](https://web.archive.org/web/20171016024418/https://eidosmontreal.com/en/news/depth-proxy-transparency-rendering)

- Depth proxy: 2 channel textures that contains min and max of transparent entity
- using this structure for various applications
- Particles Self-Shadowing
- Volumetric Effects-Particles Sorting
- Particles-Transparent Meshes Sorting


[Little Lightmap Tricks](http://www.codersnotes.com/notes/lightmap-tricks/) [[wayback-archive]](http://web.archive.org/web/20171011044941/http://www.codersnotes.com/notes/lightmap-tricks/)

- no pixel gaps are required between charts, if they are required then the UV calculation is wrong
- if all pixels in a chart are similar, can squash them down to a single pixel and point the UVs to it
- deduplicate nearly identical charts
- store similar colors for unused pixels, increase DXT quality
- explanation of the scheme used for the wii version of Call Of Duty: Modern Warfare

[It’s All About The Data](http://ourmachinery.com/post/its-all-about-the-data/) [[wayback-archive]](http://web.archive.org/web/20171010022458/http://ourmachinery.com/post/its-all-about-the-data/)

- how to optimize data transformation from API agnostic command buffers to API specific calls
- think about data layout
- combine state settings into few and bigger commands

[Unreal Dev Day Montreal Presentations Released](https://www.unrealengine.com/en-US/blog/unreal-dev-day-montreal-presentations-released) [[wayback-archive]](https://web.archive.org/web/20171016025424/https://www.unrealengine.com/en-US/blog/unreal-dev-day-montreal-presentations-released)

[UE4 Performance and Profiling](https://www.youtube.com/watch?v=hcxetY8g_fs)[Paragon Character Texturing Pipeline](https://www.youtube.com/watch?v=nVes6OUyzdw)[Creating Complex In-Game Effects](https://www.youtube.com/watch?v=Vhsllsv53K0)[Lighting with Unreal Engine Masterclass](https://www.youtube.com/watch?v=ihg4uirMcec)[Fortnite Trailer Pipeline](https://www.youtube.com/watch?v=LS0VsMMTaQA)

[Aftermath 1.3 Update](https://developer.nvidia.com/aftermath-update) [[wayback-archive]](https://web.archive.org/web/20171016025409/https://developer.nvidia.com/aftermath-update)

- no need to rename the .exe anymore
- can return resource information
- reduced overhead (memory and CPU performance)

- samples released by the Xbox Advanced Technology Group
- this includes source code for Xbox One samples

- API to supersede WebGL
- abstraction on Vulkan, Metal, D3D12 but embracing web constraints
- comparison of similar concepts in all 3 APIs

- was discussed in
[Issue 10](https://jendrikillner.bitbucket.io/post/graphics-programming-weekly-issue-10/). Now the video is released

[Register Cache: Caching for Warp-Centric CUDA Programs](https://devblogs.nvidia.com/parallelforall/register-cache-warp-cuda) [[wayback-archive]](https://web.archive.org/web/20171016024240/https://devblogs.nvidia.com/parallelforall/register-cache-warp-cuda/)

- software abstraction that uses inter-thread shuffling to replace shared memory with thread register usage
- use case: replace shared memory with registers to cache kernel inputs

[Dealing with geometry in Vulkan](https://sopyer.github.io/b/post/static-dynamic-geometry-vulkan/) [[wayback-archive]](https://web.archive.org/web/20171016025341/https://sopyer.github.io/b/post/static-dynamic-geometry-vulkan/)

- how to upload data into buffers for dynamic and static cases