---
title: Optix 2.5 released
url: http://raytracey.blogspot.com/2012/01/optix-25-released.html
author: Sam Lapere
published: '2012-01-22'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

A few days ago, Nvidia has released

[OptiX SDK 2.5 RC1](http://developer.nvidia.com/optix)which stands out compared to prior releases due to a number of major improvements:
- out-of-core GPU ray tracing: scenes can now exceed the amount of available GPU RAM (up to 3 times)

- HLBVH2 support (


This will greatly benefit real-time GPU path traced games and animations as it not only reduces the BVH build times by several orders of magnitude compared to CPU builders, but also eliminates costly per-frame CPU-to-GPU transfers of the updated BVH (when built on the cpu)

[Garanzha and Pantaleoni](http://www.google.be/url?sa=t&rct=j&q=hlbvh+garanzha&source=web&cd=2&ved=0CCwQFjAB&url=http%3A%2F%2Fgaranzha.com%2FDocuments%2Fhlbvh.pdf&ei=XWQcT9DjDpGd-wabs4G1Cg&usg=AFQjCNG4i9sNZHlDuiTM0cuD1BtQrL5G1A&sig2=vyTmZT2sPFBAOvOxeGEVZA)): replaces the previous LBVH builder and is able to build the BVH acceleration structure on the GPU at a fraction of the time it would take a CPU, which allows for completely dynamic scenes by rebuilding the acceleration structure each frame in real-time (e.g. the HLBVH2 paper reports building times of 10.5 ms on a GTX480 for a model consisting of 1.76M fully dynamic polygons). HLBVH2 traversal speed is said to be comparable to a CPU built BVHThis will greatly benefit real-time GPU path traced games and animations as it not only reduces the BVH build times by several orders of magnitude compared to CPU builders, but also eliminates costly per-frame CPU-to-GPU transfers of the updated BVH (when built on the cpu)

- the SDK path tracing sample is enhanced with multiple importance sampling

## 2 comments:

Hi Raytracey,



OptiX 2.5 doesn't use any out-of-core things from CentiLeo. They are different projects and use differnt out-of-core staff. And I am only working on CentiLeo ;)

Kirill Garanzha.

Ok, I will correct my post then. Thanks Kirill.


And nice to know you're reading my blog.

Post a Comment