---
title: Incoherent ray tracing without acceleration structures
url: http://raytracey.blogspot.com/2012/04/incoherent-ray-tracing-without.html
author: Sam Lapere
published: '2012-04-24'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Just stumbled upon a very interesting paper by the author of the

[Voxelium blog](http://voxelium.wordpress.com/), whose impressive research on hybrid voxel/triangle ray tracing I've blogged about in the past (see[http://raytracey.blogspot.com/2012/01/voxlod-interactive-ray-tracing-of.html](http://raytracey.blogspot.com/2012/01/voxlod-interactive-ray-tracing-of.html)and[http://raytracey.blogspot.com/2010/09/voxlod-interactive-ray-tracing-of.html](http://raytracey.blogspot.com/2010/09/voxlod-interactive-ray-tracing-of.html)).
This guy has invented a new algorithm for tracing incoherent rays that doesn't need an acceleration structure at all, which means no time consuming updates or rebuilds of the acceleration structure. This would also immediately solve the problem of ray tracing huge dynamic scenes. The research was inspired by a recent algorithm proposed by Keller and Wachter (toxie on ompf), which was in turn inspired by a method described in a patent of Caustic Graphics iirc.

Excerpt of the abstract:

We present a new ray traversal method based on this principle, which efﬁciently handles incoherent rays, and takes advantage of the SSE and AVX instruction sets of the CPU. Our algorithm offers notable performance improvements over similar existing solutions, and it is competitive with powerful static ray tracers

## 9 comments:

nice academic work but i must observe that the results (mrays/s) are a factor of 15x behind star methods (accl. structur rebuild included).


these scenes can be rebuild in a handful of ms + fast rt incoherent rays. the boeing would be a nice example but the io pressure will limit the approach again to 1-2 fps only.

What star methods are you referring to and are they cpu or gpu based?

I think he refers to the GPU ray tracer by Aila and Laine:


http://www.tml.tkk.fi/~timo/HPG2009/index.html

Those results are indeed very impressive. However, the gap is much narrower on the CPU, and I think that CPU ray tracing is still very important. I've compared the results to a highly optimized MBVH ray tracer, which is one of the fastest on the CPU (the AVX version is faster than Embree). The difference is not that big on one thread, but on multiple threads the bandwidth limitation sadly kicks in. In the worst case, it's about 4x slower.

Thanks Atilla. Do you have any plans to port your algorithm to the GPU or is it not that well suited for parallelization (as mentioned at the end of the paper)?

I will certainly think about it. :)

cool :)

Note that Aila and Laine sorts all rays on the CPU in order to increase coherence. This is not included in their Mrays/sec (I believe).

That's interesting. Do you happen to know how much speed gain there is on average when sorting rays?

I don't know the exact number but I think it does help a lot. Just think about all the coalesced memory accesses that wont happen otherwise, as well as the improved SIMD-efficiency. You can enable/disable it in their demo program. I may test it later :) This is from the README:



"The sorting of is performed by the CPU and is a quite heavy operation, taking roughly one second per batch. It is disabled in the interactive mode."

They wouldn't do that if there wasn't a good performance boost :)

Post a Comment