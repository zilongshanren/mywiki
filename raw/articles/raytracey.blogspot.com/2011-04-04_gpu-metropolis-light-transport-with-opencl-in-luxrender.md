---
title: GPU Metropolis light transport with OpenCL in LuxRender!
url: http://raytracey.blogspot.com/2011/04/gpu-metropolis-light-transport-on-gpu.html
author: Sam Lapere
published: '2011-04-04'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

This is very neat: after Dietger van Antwerpen successfully implemented Metropolis light transport (MLT) on the GPU using CUDA and the Brigade path tracer framework, one of the LuxRender developers now has succeeded at making MLT work on the GPU with OpenCL.




Unlike Luxrender's SmallLuxGPU, which is a hybrid CPU+GPU renderer that only uses the GPU for ray intersections, this MLT algorithm is running entirely on the GPU using OpenCL, offering a vast speed boost over the hybrid approach. Fireflies (bright pixels produced by caustics) are sampled away much more efficiently than when using the standard path tracing integrator. Very complex lighting situations (e.g. light passing through a keyhole) should benefit as well.


It's great to see a smart and efficient rendering algorithm like MLT (which many believed to be impossible on current GPUs) is now popping up in several GPU renderers. Hopefully bidirectional path tracing running entirely on the GPU (with MLT on top, something that has already been done by Dietger van Antwerpen) will become widespread soon as well.


[http://www.luxrender.net/forum/viewtopic.php?f=34&t=5795](http://www.luxrender.net/forum/viewtopic.php?f=34&t=5795)(registration required)Unlike Luxrender's SmallLuxGPU, which is a hybrid CPU+GPU renderer that only uses the GPU for ray intersections, this MLT algorithm is running entirely on the GPU using OpenCL, offering a vast speed boost over the hybrid approach. Fireflies (bright pixels produced by caustics) are sampled away much more efficiently than when using the standard path tracing integrator. Very complex lighting situations (e.g. light passing through a keyhole) should benefit as well.

It's great to see a smart and efficient rendering algorithm like MLT (which many believed to be impossible on current GPUs) is now popping up in several GPU renderers. Hopefully bidirectional path tracing running entirely on the GPU (with MLT on top, something that has already been done by Dietger van Antwerpen) will become widespread soon as well.

## No comments:

Post a Comment