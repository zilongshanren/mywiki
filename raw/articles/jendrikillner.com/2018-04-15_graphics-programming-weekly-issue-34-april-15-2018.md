---
title: Graphics Programming weekly - Issue 34 — April 15, 2018
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-34/
author: Jendrik Illner
published: '2018-04-15'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

[Exploring scriptable render pipelines in unity 2018.1](http://colourmath.com/2018/tutorials/exploring-scriptable-render-pipelines-in-unity-2018-1/) [[wayback-archive]](https://web.archive.org/web/20180416005143/http://colourmath.com/2018/tutorials/exploring-scriptable-render-pipelines-in-unity-2018-1/)

- overview of the scriptable render pipeline
- walkthrough of the development of a pipeline for mobile VR, code on
[github](https://github.com/colourmath/ScriptableRenderPipeline) - lighting, fog, lightmaps, shadows, light/reflection probes, transparency

[SymPy case studies, part 2: derivatives](https://mzucker.github.io/2018/04/11/sympy-case-studies-part-2-derivatives.html) [[wayback-archive]](https://web.archive.org/web/20180416005317/https://mzucker.github.io/2018/04/11/sympy-case-studies-part-2-derivatives.html)

- calculation of partial derivatives, function gradients
- able to eliminate common subexpressions

[SymPy part 3: moar derivatives!](https://mzucker.github.io/2018/04/12/sympy-part-3-moar-derivatives.html) [[wayback-archive]](https://web.archive.org/web/20180416005350/https://mzucker.github.io/2018/04/12/sympy-part-3-moar-derivatives.html)

- longer example combining all elements of previous posts of the series to calculate area elements on the unit sphere

[Daily Pathtracer Part 7: Initial SIMD](https://aras-p.info/blog/2018/04/10/Daily-Pathtracer-Part-7-Initial-SIMD/) [[wayback-archive]](https://web.archive.org/web/20180416005411/https://aras-p.info/blog/2018/04/10/Daily-Pathtracer-Part-7-Initial-SIMD/)

[Daily Pathtracer 8: SSE HitSpheres](https://aras-p.info/blog/2018/04/11/Daily-Pathtracer-8-SSE-HitSpheres/) [[wayback-archive]](https://web.archive.org/web/20180416005430/https://aras-p.info/blog/2018/04/11/Daily-Pathtracer-8-SSE-HitSpheres/)

[Daily Pathtracer 9: A wild ryg appears](https://aras-p.info/blog/2018/04/13/Daily-Pathtracer-9-A-wild-ryg-appears/) [[wayback-archive]](https://web.archive.org/web/20180416005443/https://aras-p.info/blog/2018/04/13/Daily-Pathtracer-9-A-wild-ryg-appears/)

- new parts about the pathracer, discussing SSE implementation approaches, performance and optimizations

[Coarse Pixel Shading with Temporal Supersampling](https://software.intel.com/en-us/articles/coarse-pixel-shading-with-temporal-supersampling) [[wayback-archive]](https://web.archive.org/web/20180416005252/https://software.intel.com/en-us/articles/coarse-pixel-shading-with-temporal-supersampling)

- coarse pixel shading lowers shading rate
- temporally reconstructs shading samples and full visibility information
[pdf preprint](https://software.intel.com/sites/default/files/managed/3b/2b/CPST_preprint.pdf)

[GPU Emitter Graph System in Star Wars Battlefront 2](https://www.ea.com/frostbite/news/frostbite-gpu-emitter-graph-system) [[wayback-archive]](https://web.archive.org/web/20180416005556/https://media.contentapi.ea.com/content/dam/eacom/frostbite/files/gdc2018-frostbitediceemittergraph.pptx)

- workflow overview
- runtime design
- frame organisation
- data management
- particle sorting
- performance

- walkthrough of different use cases (sparks, snow, rain, leaves, … , crowds)

- website allows the compilation of HLSL using the old fxc and the new dxc shader compiler

[Fast & beautiful 2D lighting in Unity](https://medium.com/@tidyui/fast-beautiful-2d-lighting-in-unity-47b76b10447c) [[wayback-archive]](https://web.archive.org/web/20180416005655/https://medium.com/@tidyui/fast-beautiful-2d-lighting-in-unity-47b76b10447c)

- breakdown of how the 2D lighting system was implemented
- using 3D objects to cast and receive shadows
- rendering shadows and lighting into a render target, blend the result into the main output

[Interactive Editor for the DirectX Shader Compiler](https://blogs.msdn.microsoft.com/marcelolr/2018/04/09/interactive-editor-for-the-directx-shader-compiler/) [[wayback-archive]](https://web.archive.org/web/20180416005719/https://blogs.msdn.microsoft.com/marcelolr/2018/04/09/interactive-editor-for-the-directx-shader-compiler/)

- Interactive editor mode allows to show changes introduced by each pass
- changes to disassembly can be made and will be propagated to following changes

[For best performance, use DXGI flip model](https://blogs.msdn.microsoft.com/directx/2018/04/09/dxgi-flip-model/) [[wayback-archive]](http://web.archive.org/web/20180416005736/https://blogs.msdn.microsoft.com/directx/2018/04/09/dxgi-flip-model/)

- Spring Creators Update brings new features
- discussion of scenarios when the windows compositor can be bypassed with the flip model to allow best performance
- hardware can scale back buffers when they don’t match the screen resolution

[Epic at GDC 2018](https://www.unrealengine.com/en-US/events/gdc2018/) [[wayback-archive]](http://web.archive.org/web/20180310045337/https://www.unrealengine.com/en-US/events/gdc2018/)

- list of all Epic content presented at GDC 2018