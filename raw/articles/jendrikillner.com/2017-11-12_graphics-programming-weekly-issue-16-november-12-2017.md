---
title: Graphics Programming weekly - Issue 16 — November 12, 2017
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-16/
author: Jendrik Illner
published: '2017-11-12'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

[Announcing new DirectX 12 features](https://blogs.msdn.microsoft.com/directx/2017/11/07/announcing-new-directx-12-features/) [[wayback-archive]](http://web.archive.org/web/20171109190010/https://blogs.msdn.microsoft.com/directx/2017/11/07/announcing-new-directx-12-features/)

support for GPU heaps that persist a device removal

[MSDN](https://msdn.microsoft.com/en-us/library/windows/desktop/mt813612(v=vs.85).aspx)allow writing of U32 values directly from withing command lists

[MSDN](https://msdn.microsoft.com/en-us/library/windows/desktop/mt844818(v=vs.85).aspx)Depth Bounds Testing support

[MSDN](https://msdn.microsoft.com/en-us/library/windows/desktop/mt492658(v=vs.85).aspx)Programmable MSAA

[MSDN](https://msdn.microsoft.com/en-us/library/windows/desktop/mt492660(v=vs.85).aspx)

[World of Tanks: Graphical Update Technical Overview](https://80.lv/articles/world-of-tanks-graphical-update-technical-overview/) [[wayback-archive]](https://web.archive.org/web/20171112195718/https://80.lv/articles/world-of-tanks-graphical-update-technical-overview/)

- Stochastic Flakes for rough materials (snow, dust, sand)
- spherical harmonics grid for Global Illumination
- height deviation on terrain/objects to optimize probe placement

- breakdown of water system
- deformation particles
- allow geometry to be deformed
- bent grass, water deformation, shockwaves

- terrain system
- vegetation system

[Precomputed Atmospheric Scattering:a New Implementation](https://ebruneton.github.io/precomputed_atmospheric_scattering/) [[wayback-archive]](http://web.archive.org/web/20171025101157/https://ebruneton.github.io/precomputed_atmospheric_scattering/)

- new OpenGL implementation of bruneton scattering model
- a lot more documentation and implementation descriptions
- new features
- ozone layer
- support for extra-terrestrial solar spectrum
- density profiles for air molecules and aerosols


[Deringing Spherical Harmonics](http://www.ppsloan.org/publications/shdering.pdf) [[wayback-archive]](http://web.archive.org/web/20171110080604/http://www.ppsloan.org/publications/shdering.pdf)

- removing ringing artifacts using
[windowing functions](https://en.wikipedia.org/wiki/Window_function)(function that is zero-valued outside of some chosen interval) - how to determine how much windowing to apply

[GPU-based particle simulation](https://turanszkij.wordpress.com/2017/11/07/gpu-based-particle-simulation/amp/) [[wayback-archive]](https://web.archive.org/web/20171107181048/https://turanszkij.wordpress.com/2017/11/07/gpu-based-particle-simulation/amp/)

- D3D11 based
- implementation overview
- code is accessible on github


[Upscaling half resolution screen space effects](https://tuxedolabs.blogspot.ca/2017/11/upscaling-half-resolution-screen-space.html?m=1) [[wayback-archive]](https://web.archive.org/web/20171112195833/https://tuxedolabs.blogspot.ca/2017/11/upscaling-half-resolution-screen-space.html?m=1)

- render diffuse at half-resolution
- generate “retouching” vector field
- used during upscaling
- information where to fetch samples


[Amplify Shader Editor - Rendering Shaders Overview](http://wiki.amplify.pt/index.php?title=Unity_Products:Amplify_Shader_Editor/Tutorials/Rendering_Shaders_Overview) [[wayback-archive]](http://web.archive.org/web/20171111012416/http://wiki.amplify.pt/index.php?title=Unity_Products:Amplify_Shader_Editor/Tutorials/Rendering_Shaders_Overview)

- series of short beginner level videos about
- shaders
- physically based rendering
- 3d models
- materials
- textures


- talks about how caches are working on a hardware level
- cache protocol
- memory barriers


[Parallelizing the Gauss-Seidel Method using Graph Coloring](https://erkaman.github.io/posts/gauss_seidel_graph_coloring.html) [[wayback-archive]](https://web.archive.org/web/20171112200139/https://erkaman.github.io/posts/gauss_seidel_graph_coloring.html)

- detect partition of variables that can be solved indepedently
- variables within one parition can be solved in parrallel
- detect partitions with graph coloring

- sparse matrices result in low number of partitions
- common in game use cases


- Physical Shader Framework for unity, now open source