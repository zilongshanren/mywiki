---
title: Graphics Programming weekly - Issue 33 — April 8, 2018
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-33/
author: Jendrik Illner
published: '2018-04-08'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

[Breaking down barriers – part 2: Synchronizing GPU threads](https://mynameismjp.wordpress.com/2018/04/01/breaking-down-barriers-part-2-synchronizing-gpu-threads/) [[wayback-archive]](https://web.archive.org/web/20180408164108/https://mynameismjp.wordpress.com/2018/04/01/breaking-down-barriers-part-2-synchronizing-gpu-threads/)

- explanations of barrier behaviour on a simplified GPU model
- how split barriers help to increase GPU utilization

[Color: From Hexcodes to Eyeballs](http://jamie-wong.com/post/color/) [[wayback-archive]](http://web.archive.org/web/20180408122501/http://jamie-wong.com/post/color/)

- in-depth introduction into light theory, human perception, color spaces and gamma correction

[One Mesh To Rule Them All](https://www.unrealengine.com/en-US/blog/one-mesh-to-rule-them-all) [[wayback-archive]](https://web.archive.org/web/20180408164138/https://www.unrealengine.com/en-US/blog/one-mesh-to-rule-them-all)

- same assets used on PC/mobile/consoles
- limits the LODs based on the target platform
- creates clusters of nearby objects, generate proxy geometry from these clusters

[Improved Lerp Smoothing](https://www.gamasutra.com/blogs/ScottLembcke/20180404/316046/Improved_Lerp_Smoothing.php) [[wayback-archive]](http://web.archive.org/web/20180407224633/https://www.gamasutra.com/blogs/ScottLembcke/20180404/316046/Improved_Lerp_Smoothing.php)

- classical lerp is frame rate dependent, hard to tweak
- improved version that solves these problems: value = lerp(target, value, exp2(-rate*deltaTime))
- how to convert from classical lerp

[Normals and the Inverse Transpose, Part 1: Grassmann Algebra](http://reedbeta.com/blog/normals-inverse-transpose-part-1/) [[wayback-archive]](https://web.archive.org/web/20180408165324/http://reedbeta.com/blog/normals-inverse-transpose-part-1/)

- introduction into grassmann algebra
- explanation of vector, bivector, trivector and wedge product
- derivation of a more geometric understanding about the behaviour under transformation

[Combining Analytic Direct Illumination and Stochastic Shadows](https://eheitzresearch.wordpress.com/705-2/) [[wayback-archive]](https://web.archive.org/web/20180408164303/https://eheitzresearch.wordpress.com/705-2/)

- split into unshadowed illumination and illumination-weighted shadow
- unshadowed areas are noise free, only shadowed areas use stochastic ray tracing and need denoising

- discussions of denoising techniques

[Memory Mapping on Windows (including Benchmark)](https://arvid.io/2018/04/02/memory-mapping-on-windows/) [[wayback-archive]](https://web.archive.org/web/20180408164849/https://arvid.io/2018/04/02/memory-mapping-on-windows/)

- overview of memory mapping on windows
- benchmark of different techniques
- using MEM_RESET allows the OS to lazily unmap pages

[Rendering in the DirectX Shader Compiler Editor](https://blogs.msdn.microsoft.com/marcelolr/2018/04/05/rendering-in-the-directx-shader-compiler-editor/) [[wayback-archive]](https://web.archive.org/web/20180408165038/https://blogs.msdn.microsoft.com/marcelolr/2018/04/05/rendering-in-the-directx-shader-compiler-editor/)

- tool to allow compilation of shaders, inspection of AST and disassembly
- renderView allows execution of draw/dispatch, could be useful for prototyping

[Viewing Optimization Passes in the DirectX Shader Compiler Editor](https://blogs.msdn.microsoft.com/marcelolr/2018/04/06/viewing-optimization-passes-in-the-directx-shader-compiler-editor/) [[wayback-archive]](http://web.archive.org/web/20180408165400/https://blogs.msdn.microsoft.com/marcelolr/2018/04/06/viewing-optimization-passes-in-the-directx-shader-compiler-editor/)

- allows display of optimisation passes
- change setup of used passes, ordering and parameters

[Barycentrics](https://github.com/kayru/Barycentrics) [[wayback-archive]](https://web.archive.org/web/20180408165100/https://github.com/kayru/Barycentrics)

- demo application that shows 5 ways to get Barycentric coordinates
- large variation in performance between the different approaches

[Ray Tracing with the DirectX Ray Tracing API (DXR)](http://diaryofagraphicsprogrammer.blogspot.ca/2018/04/ray-tracing-with-directx-ray-tracing.html?m=1) [[wayback-archive]](https://web.archive.org/web/20180408165147/http://diaryofagraphicsprogrammer.blogspot.ca/2018/04/ray-tracing-with-directx-ray-tracing.html?m=1)

- concerns about a blackbox raytracing API and the quality of drivers

[Vulkan bindless extensions](https://www.khronos.org/registry/vulkan/specs/1.1-extensions/html/vkspec.html#VK_EXT_descriptor_indexing) [[wayback-archive]](https://web.archive.org/web/20180408165205/https://www.khronos.org/registry/vulkan/specs/1.1-extensions/html/vkspec.html)

- descriptors can be updated after they are bound to a command buffer
- relax requirement so that descriptors that are not accessed can be invalid
- allow variable size bindings in descriptor set layout
[GL_EXT_nonuniform_qualifier](https://github.com/KhronosGroup/GLSL/blob/master/extensions/ext/GL_EXT_nonuniform_qualifier.txt)allows indexing into resource arrays which differ within the same draw call

[GDC Retrospective and Additional Thoughts on Real-Time Raytracing](https://colinbarrebrisebois.com/2018/04/07/some-thoughts-on-real-time-raytracing/) [[wayback-archive]](http://web.archive.org/web/20180408052448/https://colinbarrebrisebois.com/2018/04/07/some-thoughts-on-real-time-raytracing/)

- quick overview about the content of the SEED raytracing presentation at GDC
- sees the future to be about trade-offs between noise, ghosting and performance
- allows comparison against ground truth
- allows researchers to implement techniques using a common API

- library that provides a C reflection API for SPIR-V shader bytecode

[Why every gfx/CV/robotics programmer should love SymPy (Part 1)](https://mzucker.github.io/2018/04/06/why-every-gfx-cv-robotics-programmer-should-love-sympy.html) [[wayback-archive]](https://web.archive.org/web/20180408165237/https://mzucker.github.io/2018/04/06/why-every-gfx-cv-robotics-programmer-should-love-sympy.html)

- 2 case studies of how to use SymPy

[Daily Pathtracer Part 5: Metal GPU!](https://aras-p.info/blog/2018/04/03/Daily-Pathtracer-Part-5-Metal-GPU/) [[wayback-archive]](http://web.archive.org/web/20180404033138/http://aras-p.info/blog/2018/04/03/Daily-Pathtracer-Part-5-Metal-GPU/)

- experience of porting the pathtracer to metal with performance numbers and problems encountered

[(Demoscene) Revision 2018](http://www.geeks3d.com/20180402/demoscene-revision-2018/) [[wayback-archive]](http://web.archive.org/web/20180403032337/http://www.geeks3d.com/20180402/demoscene-revision-2018/)

- videos of the demos shown at revision 2018