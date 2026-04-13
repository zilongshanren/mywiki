---
title: Graphics Programming weekly - Issue 11 — October 8, 2017
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-11/
author: Jendrik Illner
published: '2017-10-08'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

[Lightmap optimizations for iOS](http://www.ludicon.com/castano/blog/2017/10/lightmap-optimizations-ios/) [[wayback-archive]](http://web.archive.org/web/20171007053252/http://www.ludicon.com/castano/blog/2017/10/lightmap-optimizations-ios/)

- lightmpas too big for the memory budget on iOS
- using ETC2 as a replacement for DXT5 (same size, slightly less quality)
- switched to per-vertex lightmaps
- needed some art fixes
- but reduced disk size to 17 % and most expensive runtime location to 25 %


[Road to Anti-Aliasing in BRE: Aliasing and Anti-Aliasing](https://nbertoa.wordpress.com/2017/10/03/road-to-anti-aliasing-in-bre-aliasing-and-anti-aliasing/amp/) [[wayback-archive]](https://web.archive.org/web/20171009141454/https://nbertoa.wordpress.com/2017/10/03/road-to-anti-aliasing-in-bre-aliasing-and-anti-aliasing/amp/)

- what is the cause of aliasing
- overview of different techniques to reduce it
- Supersampling Antialiasing (SSAA)
- Multisampling AntiAliasing (MSAA)
- Coverage Sample AntiAliasing (CSAA)


[The Complexity of Simplicity: Rendering INVERSUS Deluxe](http://blog.hypersect.com/the-complexity-of-simplicity-rendering-inversus-deluxe/) [[wayback-archive]](https://web.archive.org/web/20171009141653/http://blog.hypersect.com/the-complexity-of-simplicity-rendering-inversus-deluxe/)

- Seamless wrapped worlds, on the screen multiple times
- breakdown of rendering
- rendering to off-screen buffer that is drawn to screen multiple times
- extra pixels for correct sub-pixel accuracy when panning the camera
- color pallets, pattern map, inversion buffer create the look
- fullscreen effects for wrapping space

[Calculating the Distance Between Points in “Wrap Around” (Toroidal) Space](https://blog.demofox.org/2017/10/01/calculating-the-distance-between-points-in-wrap-around-toroidal-space/) [[wayback-archive]](http://web.archive.org/web/20171006233233/https://blog.demofox.org/2017/10/01/calculating-the-distance-between-points-in-wrap-around-toroidal-space/)

- useful for use in tiling worlds, tileable textures, …

[Medium Under the Hood: Part 2 - Move Tool Implementation](https://developer.oculus.com/blog/medium-under-the-hood-part-2-move-tool-implementation/) [[wayback-archive]](http://web.archive.org/web/20171007090131/https://developer.oculus.com/blog/medium-under-the-hood-part-2-move-tool-implementation/)

- uses SDF and triangle mesh representation
- using both representations for different techniques
- how to convert triangle mesh to SDF

- hardware constraints dictate decisions
- C++ hardware abstractions
- memory model
- coherency model
- consistency model

- new execution model designed for C++
- more details in next link

[Cooperative Groups: Flexible CUDA Thread Programming](https://devblogs.nvidia.com/parallelforall/cooperative-groups/) [[wayback-archive]](https://web.archive.org/web/20171009142059/https://devblogs.nvidia.com/parallelforall/cooperative-groups/)

- Cooperative Groups describes synchronization within and across CUDA thread blocks
- abstraction level above explicit wrap level operations
- allow algorithms that can be more portable between different hardware

[Bringing Galaxy on Fire 3 to Vulkan: Handling Resources and Assets](https://www.gamasutra.com/blogs/JohannesKuhlmann/20171002/306839/Bringing_Galaxy_on_Fire_3_to_Vulkan_Handling_Resources_and_Assets.php) [[wayback-archive]](https://web.archive.org/web/20171009142136/https://www.gamasutra.com/blogs/JohannesKuhlmann/20171002/306839/Bringing_Galaxy_on_Fire_3_to_Vulkan_Handling_Resources_and_Assets.php)

- overview of vulkan implementation for android
- texture layout handling
- shader pipeline
- pipeline (PSO in D3D12)


[Animation Compression Library: Unreal 4 Integration](http://nfrechette.github.io/2017/10/05/acl_in_ue4/) [[wayback-archive]](https://web.archive.org/web/20171009142211/http://nfrechette.github.io/2017/10/05/acl_in_ue4/)

- first results of the ACL in UE4 Matinee scene
- 59.5% smaller in total
- big wins on moving character, more costly atm for mostly idle bones


[Data visualization in shader - twitter](https://twitter.com/mmalex/status/916313043767906304?s=09) [[wayback-archive]](http://web.archive.org/web/20171009142233/https://twitter.com/mmalex/status/916313043767906304?s=09)

- thread containing a number of small snippets to visualize data in shaders

[tinyspheremesh.h - generate geodesic sphere](https://github.com/RandyGaul/tinyheaders/blob/master/tinyspheremesh.h) [[wayback-archive]](https://web.archive.org/web/20171009142443/https://github.com/RandyGaul/tinyheaders/blob/master/tinyspheremesh.h)