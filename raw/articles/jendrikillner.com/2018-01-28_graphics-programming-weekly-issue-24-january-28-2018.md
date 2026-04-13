---
title: Graphics Programming weekly - Issue 24 — January 28, 2018
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-24/
author: Jendrik Illner
published: '2018-01-28'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- aimed at beginners in graphics programming
- overview of common problems and causes
- renderdoc explanation
- feature and interface overview
- how to use it to detect problems

- GPU perf studio and how to profile your application
- common GPU performance problems

[Rendering and shading in ADAM: Episode 3](https://blogs.unity3d.com/2018/01/24/rendering-and-shading-in-adam-episode-3/) [[wayback-archive]](http://web.archive.org/web/20180126094714/https://blogs.unity3d.com/2018/01/24/rendering-and-shading-in-adam-episode-3/)

- frame breakdown
- deferred shading pipeline
- extra g-buffer channels used to store subsurface scattering profiles
- spot lights used to light the main characters
- for subsurface scattering diffuse and specular are applied separately
- diffuse component gets blurred to approximate scattering outside of a single pixel
- recombined with specular afterwards

- running two g-buffer passes
- once for the main scene and once for the visor (rendered as opaque)
- visor is recomposited using the visor alpha


- proposal of a new unit of time ( 1 flick =
1⁄705600000second ) - can represent most common frame duration in integer quantitates

[Explicit Multi-GPU Programming](http://ourmachinery.com/post/explicit-multi-gpu-programming/) [[wayback-archive]](http://web.archive.org/web/20180122204035/http://ourmachinery.com/post/explicit-multi-gpu-programming/)

- aimed not just at games but also other industries
- creating and updating of resources take a bitmask to specify on which device to operate on
- when binding a render pass or binding a queue the target device mask is specified
- new sync primitive to specify what fences to wait on and what fences to signal
- signal uses the device mask


[Using Arrays of Textures in Vulkan Shaders](http://kylehalladay.com/blog/tutorial/vulkan/2018/01/28/Textue-Arrays-Vulkan.html) [[wayback-archive]](https://web.archive.org/web/20180128174350/http://kylehalladay.com/blog/tutorial/vulkan/2018/01/28/Textue-Arrays-Vulkan.html)

- use a single descriptor set to store all textures
- push constant to index into the array
- how to create, fill and use the descriptor set
- deal with GlslangValidator warnings

[A Simple, and Trivially Parallelizable Triangle Rasterization Approach](https://erkaman.github.io/posts/fast_triangle_rasterization.html) [[wayback-archive]](https://web.archive.org/web/20180128174406/https://erkaman.github.io/posts/fast_triangle_rasterization.html)

- description of how the cross product can be used to detect if a point is inside a triangle

[Art Design Deep Dive: Using a 3D pipeline for 2D animation in Dead Cells](https://www.gamasutra.com/view/news/313026/Art_Design_Deep_Dive_Using_a_3D_pipeline_for_2D_animation_in_Dead_Cells.php) [[wayback-archive]](http://web.archive.org/web/20180125124237/https://www.gamasutra.com/view/news/313026/Art_Design_Deep_Dive_Using_a_3D_pipeline_for_2D_animation_in_Dead_Cells.php)

- simple 3D model used
- rendered into a small texture without anti aliasing to create the 2D sprite + normal map

[Google and Qualcomm: Pixel-Perfect?](https://medium.com/@afd_icl/google-and-qualcomm-pixel-perfect-e8ecefaf5968) [[wayback-archive]](http://web.archive.org/web/20180125194945/https://medium.com/@afd_icl/google-and-qualcomm-pixel-perfect-e8ecefaf5968)

- look at driver quality between Google Pixel 2 and Samsung Galaxy S8

[GPU Zen 2 - Call for Authors](https://gpuzen.blogspot.ca/?m=1) [[wayback-archive]](https://web.archive.org/web/20180128174555/https://gpuzen.blogspot.ca/?m=1)

- next edition of the book is looking for proposals, due March 30th

- open source
- supports PC D2D12, vulkan, iOS, Android, PS4, Xbox One