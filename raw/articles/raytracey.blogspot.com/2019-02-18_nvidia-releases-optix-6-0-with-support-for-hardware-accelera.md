---
title: Nvidia releases OptiX 6.0 with support for hardware accelerated ray tracing
url: http://raytracey.blogspot.com/2019/02/nvidia-release-optix-60-with-support.html
author: Sam Lapere
published: '2019-02-18'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Nvidia recently released a new version of Optix, which finally adds support for the much hyped RTX cores on the Turing GPUs (RTX 2080, Quadro RTX 8000 etc), which provide hardware acceleration for ray-BVH and ray-triangle intersections.

First results are quite promising. One user reports a speedup between 4x and 5x when using the RTX cores (compared to not using them). Another interesting revelation is that the speedup gets larger with higher scene complexity (geometry-wise, not shading-wise):

As a consequence, the Turing cards can render up to 10x faster in some scenes than the previous generation of Geforce cards, i.e. Pascal (GTX 1080), which is in fact two generations old if you take the Volta architecture into account (Volta was already a huge step up from Pascal in terms of rendering speed, so for Nvidia's sake it's better to compare Turing with Pascal).

This post will be updated with more Optix benchmark numbers as they become available.

## No comments:

Post a Comment