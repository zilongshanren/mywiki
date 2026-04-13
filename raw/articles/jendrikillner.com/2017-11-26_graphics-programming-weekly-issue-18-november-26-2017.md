---
title: Graphics Programming weekly - Issue 18 — November 26, 2017
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-18/
author: Jendrik Illner
published: '2017-11-26'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

[Decima engine: visibility in horizon zero dawn](https://www.guerrilla-games.com/read/decima-engine-visibility-in-horizon-zero-dawn) [[wayback-archive]](https://web.archive.org/https://d1z4o56rleaq4j.cloudfront.net/downloads/assets/GCAP2017_DecimaVisibility.pdf?mtime=20171120133325)

- seperate system for statics and dynamics
- world broken into tiles
- sort key is used to define clusters
- lod ranges, filter masks
- morton numbers for spatial partioning

- tile/cluster culling on the CPU
- launch one GPU culling job for each visible tile/cluster

- gpu tasks use
[aggregated atomics](https://devblogs.nvidia.com/parallelforall/cuda-pro-tip-optimized-filtering-warp-aggregated-atomics)to write wavefront results- one atomic operation per wavefront instead of per thread

- description of batching strategies

[Vulkan: Command Buffer Management](http://ourmachinery.com/post/vulkan-command-buffer-management/) [[wayback-archive]](https://web.archive.org/web/20171121153639/http://ourmachinery.com/post/vulkan-command-buffer-management/)

- CommandBuffer used to record GPU work
- each worker thread has one CommandPool which owns the CommandBuffer allocations
- engine CommandBuffer
- packs completed fence, target queue
- Primary + secondary command buffers
- resource descriptors
- deleteted resources

- once the fence is reached
- resources are deleted
- descriptors and command buffers are marked for reuse


[Maximizing Unified Memory Performance in CUDA](https://devblogs.nvidia.com/parallelforall/maximizing-unified-memory-performance-cuda/) [[wayback-archive]](https://web.archive.org/web/20171121153825/https://devblogs.nvidia.com/parallelforall/maximizing-unified-memory-performance-cuda/)

- on-demand page migration from CPU to GPU memory
- linear arrays nearly 2x slower then manual pre-fetching of gpu data
- number of page faults influences performance significantly
- less page faults, better performance

- how to structure code to achieve better asynchronous memory copy overlap

[Stabel 1 pixel dithering](https://forums.tigsource.com/index.php?topic=40832.msg1363742#msg1363742) [[wayback-archive]](https://web.archive.org/web/20171123222517/https://forums.tigsource.com/index.php?topic=40832.msg1363742)

- image rendered in greyscale
- fullscreen pass applied to convert to 1-bit dithered image
- discussion of different experiments
- ended up using a dithering pattern mapped with 2x oversampling onto a sphere

[Demystifying Floating Point Precision](https://blog.demofox.org/2017/11/21/floating-point-precision/) [[wayback-archive]](http://web.archive.org/web/20171125072738/https://blog.demofox.org/2017/11/21/floating-point-precision/)

- how to calculate precision of floats
- table listing the precision for half/float/double in different ranges
- show precision loss problem with storing time as float

[Neural 3D Mesh Renderer](https://arxiv.org/pdf/1711.07566.pdf) [[wayback-archive]](http://web.archive.org/web/20171124190539/https://arxiv.org/pdf/1711.07566.pdf)

- 3D mesh reconstruction from a single image
- applying 2D stylization from image to the 3D Mesh

[Universal GPU texture format: DXT5 support](http://richg42.blogspot.ca/2017/11/universal-gpu-texture-format-dxt5.html?m=1) [[wayback-archive]](https://web.archive.org/web/20171127025754/http://richg42.blogspot.ca/2017/11/universal-gpu-texture-format-dxt5.html?m=1)

- ETC1 to DXT5A conversion using a lookup table
- discussion of results

- description and WebGL demo of the terrain system used in the game Comanche released in 1992

[A better depth buffer for raymarching](http://tuxedolabs.blogspot.ca/2017/11/a-better-depth-buffer-for-raymarching.html?m=1) [[wayback-archive]](https://web.archive.org/web/20171127025722/http://tuxedolabs.blogspot.ca/2017/11/a-better-depth-buffer-for-raymarching.html?m=1)

- single depth buffer value is not enough
- need to know the depth of objects for correct effects
- stores front and backface depth of objects in R and G channel and uses that to determine the thickness

- snow deformation, snow particles, animation adjustment
- in-engine visualtions for AI
- wireframe of character models
- breakdown of light passes

[Dissecting “Tiny Clouds”](https://blog.demofox.org/2017/11/26/dissecting-tiny-clouds/) [[wayback-archive]](http://web.archive.org/web/20171127010155/https://blog.demofox.org/2017/11/26/dissecting-tiny-clouds/)

- breakdown and explanation of the
[Tiny Cloud](https://www.shadertoy.com/view/lsBfDz)shadertoy

[Simple Curve Fitting with the Gauss-Newton Algorithm](https://erkaman.github.io/posts/gauss_newton.html) [[wayback-archive]](http://web.archive.org/web/20171126224646/https://erkaman.github.io/posts/gauss_newton.html)

- explanation of how to use the Gauss-Newton Algorithm to derive an approximation to the Schlick fresnel formula

[cr.h: A Simple C Hot Reload Header-only Library](https://fungos.github.io/blog/2017/11/20/cr.h-a-simple-c-hot-reload-header-only-library/) [[wayback-archive]](https://web.archive.org/web/20171121153503/https://fungos.github.io/blog/2017/11/20/cr.h-a-simple-c-hot-reload-header-only-library/)

- open source system for hot reloading c code (written in C++)
- supports rollback to old version if an error is detected
- rewrites the .exe to point to the copied .pdb
- uses a custom data segment to mark statics for copying
- code is on
[github](https://github.com/fungos/cr)