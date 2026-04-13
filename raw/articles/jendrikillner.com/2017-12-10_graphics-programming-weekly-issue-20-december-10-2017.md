---
title: Graphics Programming weekly - Issue 20 — December 10, 2017
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-20/
author: Jendrik Illner
published: '2017-12-10'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

[White Paper: Foveated Rendering](https://community.arm.com/graphics/b/blog/posts/white-paper-foveated-rendering) [[wayback-archive]](https://web.archive.org/web/20171205192618/https://community.arm.com/graphics/b/blog/posts/white-paper-foveated-rendering)

- overview of typical VR rendering pipeline
- lens distortion causes pixels towards the edges to be distorted more
- Foveated takes advantage of this and uses a variable quality across the screen
- how to implement it using the opengl multiview extension

[Introducing a New Foveation Pipeline for Virtual/Mixed Reality](https://research.googleblog.com/2017/12/introducing-new-foveation-pipeline-for.html?m=1) [[wayback-archive]](https://web.archive.org/web/20171209055646/https://research.googleblog.com/2017/12/introducing-new-foveation-pipeline-for.html?m=1)

- Foveated rendering
- rendering the scene with more resolution in the center then in the peripheral vision

- Conformal Rendering
- using vertex distortion based on fixation point to better match desired resolution

- Foveated Image Processing
- applying the same ideas to post processing


[ADAM: The evolution of Alembic support in Unity](https://blogs.unity3d.com/2017/12/04/adam-the-evolution-of-alembic-support-in-unity/) [[wayback-archive]](https://web.archive.org/web/20171205192714/https://blogs.unity3d.com/2017/12/04/adam-the-evolution-of-alembic-support-in-unity/)

- added timeline support
- vertex sharing for constant topology
- vertex interpolation

[They are what they wear: Clothing simulation in ADAM](https://blogs.unity3d.com/2017/12/05/they-are-what-they-wear-clothing-simulation-in-adam/) [[wayback-archive]](https://web.archive.org/web/20171209062649/https://blogs.unity3d.com/2017/12/05/they-are-what-they-wear-clothing-simulation-in-adam/)

- costumes are built in real-life
- scanned using photogrammetry
- using alembic to import cloth simulations into unity

[CUTLASS: Fast Linear Algebra in CUDA C++](https://devblogs.nvidia.com/parallelforall/cutlass-linear-algebra-cuda/) [[wayback-archive]](http://web.archive.org/web/20171208035012/https://devblogs.nvidia.com/parallelforall/cutlass-linear-algebra-cuda/)

- use accumulating matrix products
- overview of how the computation is decomposed into a hierarchy of thread block tiles, warp tiles, and thread tiles

[Thoughts on light culling for clustered shading](https://www.sebastiansylvan.com/post/light_culling/) [[wayback-archive]](https://web.archive.org/web/20171209053652/https://www.sebastiansylvan.com/post/light_culling/)

- list a few ideas for different culling changes
- Split X and Y visibility as well
- Go beyond 1D visibility for Z
- Use a more flexible primary “sort axis”
- use visible lights to find principal axis dynamically and use that for sorting

- Remove the view dependence entirely

[Lazy spectral rendering](https://psgraphics.blogspot.ca/2017/12/lazy-spectral-rendering.html?m=1) [[wayback-archive]](https://web.archive.org/web/20171209055042/https://psgraphics.blogspot.ca/2017/12/lazy-spectral-rendering.html?m=1)

- a simplification of spectral rendering

[Lighting tips & tricks in the ADAM films](https://blogs.unity3d.com/2017/12/07/lighting-tips-tricks-in-the-adam-films/) [[wayback-archive]](https://web.archive.org/web/20171211032851/https://blogs.unity3d.com/2017/12/07/lighting-tips-tricks-in-the-adam-films/)

- light setup (linear, deferred, ACES tone mapping)
- shadows
- cascades are tweaked per shot
- smoke and fire particles
- baked from Houdini into texture atlas + flow maps


[Animation Compression Library: Paragon Results](https://nfrechette.github.io/2017/12/05/acl_paragon/) [[wayback-archive]](http://web.archive.org/web/20171205173128/https://nfrechette.github.io/2017/12/05/acl_paragon/)

- how does it perform on the animation data from the game Paragon