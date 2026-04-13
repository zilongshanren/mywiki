---
title: Graphics Programming weekly - Issue 23 — January 21, 2018
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-23/
author: Jendrik Illner
published: '2018-01-21'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

[Experiments in GPU-based occlusion culling part 2: MultidrawIndirect and mesh lodding](https://interplayoflight.wordpress.com/2018/01/15/experiments-in-gpu-based-occlusion-culling-part-2-multidrawindirect-and-mesh-lodding/) [[wayback-archive]](https://web.archive.org/web/20180116195435/https://interplayoflight.wordpress.com/2018/01/15/experiments-in-gpu-based-occlusion-culling-part-2-multidrawindirect-and-mesh-lodding/)

- using DrawIndexedInstancedIndirect (on AMD and Nvidia with API extensions)
- all vertices in large buffers with manual vertex fetch in the vertex shader

- how to integrate level of detail for meshes

[Using CUDA Warp-Level Primitives](https://devblogs.nvidia.com/parallelforall/using-cuda-warp-level-primitives/) [[wayback-archive]](https://web.archive.org/web/20180116195523/https://devblogs.nvidia.com/parallelforall/using-cuda-warp-level-primitives/)

- explanation of SIMT (Single Instruction, Multiple Thread) of 32 threads = Wrap
- wrap-level primitives for
- exchange of data between threads
- active thread mask query
- synchronize all threads in a wrap + memory fence


[Easy Transparent Shadow Maps](https://turanszkij.wordpress.com/2018/01/18/easy-transparent-shadow-maps/amp/) [[wayback-archive]](https://web.archive.org/web/20180121165023/https://turanszkij.wordpress.com/2018/01/18/easy-transparent-shadow-maps/amp/)

- technqiue to allow transparent objects to cast colored shadows onto opaque objects
- render transparents into a color but rejecting pixels that are occluded by opaques

- extension of technique to allow transparent shadows on transparent objects
- showcase of some use-cases
- projectors
- underwater caustics


[Area Lights with LTCs](http://blog.magnum.graphics/guest-posts/area-lights-with-ltcs/) [[wayback-archive]](http://web.archive.org/web/20180115180135/http://blog.magnum.graphics/guest-posts/area-lights-with-ltcs/)

- high level overview of the “Real-Time Polygonal-Light Shading with Linearly Transformed Cosines” technique

[Adding depth to 2D with hand-drawn normal maps in The Siege and the Sandfox](https://www.gamasutra.com/view/news/312977/Adding_depth_to_2D_with_handdrawn_normal_maps_in_The_Siege_and_the_Sandfox.php) [[wayback-archive]](http://web.archive.org/web/20180116113505/https://www.gamasutra.com/view/news/312977/Adding_depth_to_2D_with_handdrawn_normal_maps_in_The_Siege_and_the_Sandfox.php)

- normal map used to strengthen the silhouettes instead of adding small surface detail
- how they create the normals maps

[Unity - 2018 and Graphics](https://blogs.unity3d.com/2018/01/18/2018-and-graphics/) [[wayback-archive]](https://web.archive.org/web/20180121165007/https://blogs.unity3d.com/2018/01/18/2018-and-graphics/)

- what graphics features will be coming to unity in 2018
- Scriptable Render Pipelines, will allow C# script to control the render pipeline logic
- Lightweight Rendering Pipeline aimed at low end hardware will be added
- improvements to post processing, HDR rendering and a built-in shader graph

[GPU atomic operations performance](https://twitter.com/g_truc/status/954899823710306305/photo/1) [[wayback-archive]](https://web.archive.org/web/20180121164934/https://twitter.com/g_truc/status/954899823710306305/photo/1)

- comparison of atomic instructions on different GPUs