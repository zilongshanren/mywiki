---
title: 'GPU path tracing tutorial 4: Optimised BVH building, faster traversal and
  intersection kernels and HDR environment lighting'
url: http://raytracey.blogspot.com/2016/09/gpu-path-tracing-tutorial-4-optimised.html
author: Sam Lapere
published: '2016-09-20'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

For this tutorial, I've implemented a couple of improvements based on the high performance GPU ray tracing framework of Timo Aila, Samuli Laine and Tero Karras (Nvidia research) which is described in their 2009 paper


-


-


-

["Understanding the efficiency of ray traversal on GPUs"](https://mediatech.aalto.fi/~samuli/publications/aila2009hpg_paper.pdf)and the[2012 addendum to the original paper](https://research.nvidia.com/publication/understanding-efficiency-ray-traversal-gpus-kepler-and-fermi-addendum)which contains specifically hand tuned kernels for Fermi and Kepler GPUs (which also works on Maxwell). The code for this framework is open source and can be found at the[Google code repository](https://code.google.com/archive/p/understanding-the-efficiency-of-ray-traversal-on-gpus/)(which is about to be phased out) or on[GitHub](https://github.com/matt77hias/GPURayTraversal/tree/master/src). The ray tracing kernels are thoroughly optimised and deliver state-of-the-art performance (the code from this tutorial is 2-3 times faster than the previous one). For that reason, they are also used in the production grade CUDA path tracer Cycles:-

[wiki.blender.org/index.php/Dev:Source/Render/Cycles/BVH](https://wiki.blender.org/index.php/Dev:Source/Render/Cycles/BVH)-

[github.com/doug65536/blender/blob/master/intern/cycles/kernel/kernel_bvh.h](https://github.com/doug65536/blender/blob/master/intern/cycles/kernel/kernel_bvh.h)-

[github.com/doug65536/blender/blob/master/intern/cycles/kernel/kernel_bvh_traversal.h](https://github.com/doug65536/blender/blob/master/intern/cycles/kernel/kernel_bvh_traversal.h)
The major improvements from this framework are:

-

**Spatial split BVH**: this BVH building method is based on Nvidia's "[Spatial splits in bounding volume hierarchies](http://www.nvidia.com/docs/IO/77714/sbvh.pdf)" paper by Martin Stich. It aims to reduce BVH node overlap (a high amount of node overlap lowers ray tracing performance) by combining the object splitting strategy of regular BVH building (according to a surface area heuristic or SAH) with the space splitting method of kd-tree building. The algorithm determines for each triangle whether "splitting" it (by creating duplicate references to the triangle and storing them in its overlapping nodes) lowers the cost of ray/node intersections compared to the "unsplit" case. The result is a very high quality acceleration structure with ray traversal performance which on average is significantly higher than (or in the worst case equal to) a regular SAH BVH.
-

**Woop ray/triangle intersection**: this algorithm is explained in["Real-time ray tracing of dynamic scenes on an FPGA chip"](http://www.sven-woop.de/papers/2004-GH-SaarCOR.pdf). It basically transforms each triangle in the mesh to a unit triangle with vertices (0, 0, 0), (1, 0, 0) and (0, 1, 0). During rendering, a ray is transformed into "unit triangle space" using a triangle specific affine triangle transformation and intersected with the unit triangle, which is a much simpler computation.
-


UPDATE: an attentive reader (who knows what he's talking about) corrected a mistake in the above paragraph: "Persistent threading on the GPU was designed to work around the slow dynamic load balancing hardware of the time (GTX 260), not to address branch divergence (totally separate issue). Occupancy is again a different issue, related to how many registers your kernel needs versus how many are present in a SM to spawn threads for latency hiding."

**Hand optimised GPU ray traversal and intersection kernels**: these kernels use a number of specific tricks to minimise thread divergence within a warp (a warp is a group of 32 SIMD threads which operate in lockstep, i.e. all threads within a warp must execute the same instructions). Thread divergence occurs when one or more threads within a warp follow a different code execution branch, which (in the absolute worst case) could lead to a scenario where only one thread is active while the other 31 threads in the warp are idling, waiting for it to finish. Using "persistent threads" aims to mitigate this problem: when a predefined number of CUDA threads within a warp is idling, the GPU will dynamically fetch new work for these threads in order to increase compute occupancy. The persistent threads feature is used in the original framework. To keep things simple for this tutorial, it has not been implemented as it requires generating and buffering batches of rays, but it is relatively easy to add. Another optimisation to increase SIMD efficiency in a warp is postponing ray/triangle intersection tests until all threads in the same warp have found a leaf node. Robbin Marcus wrote[a very informative blogpost](http://robbinmarcus.blogspot.co.nz/2015/12/real-time-raytracing-part-31.html)about these specific optimisations. In addition to these tricks, the Kepler kernel also uses the GPUs video instructions to perform min/max operations (see "renderkernel.cu" at the top).UPDATE: an attentive reader (who knows what he's talking about) corrected a mistake in the above paragraph: "Persistent threading on the GPU was designed to work around the slow dynamic load balancing hardware of the time (GTX 260), not to address branch divergence (totally separate issue). Occupancy is again a different issue, related to how many registers your kernel needs versus how many are present in a SM to spawn threads for latency hiding."

Other new features:

- a basic OBJ loader which triangulates n-sided faces (n-gons, triangle fans)

- simple HDR environment map lighting, which for simplicity does not use any filtering (hence the blockiness) or importance sampling yet. The code is based on



[http://blog.hvidtfeldts.net/index.php/2012/10/image-based-lighting/](http://blog.hvidtfeldts.net/index.php/2012/10/image-based-lighting/)
Some renders with the code from this tutorial (the "Roman Settlement" city scene was created by LordGood and converted from

[a SketchUp model](https://3dwarehouse.sketchup.com/model.html?id=2bf8769ad745b52d6eae68c8785f7931), also used by Mitsuba Render. The HDR maps are available at the[HDR Labs website](http://www.hdrlabs.com/sibl/archive.html)):**Source code**


For clarity, I've tried to simplify the
code where possible, keeping the essential improvements provided by the
framework and cutting out the unnecessary parts. I have also added clarifying comments to the most difficult code parts where appropriate. There is quite a lot of new code, but the most important and interesting files are:






**- SplitBVHBuilder.cpp**contains the algorithm for building BVH with spatial splits**- CudaBVH.cpp**shows the particular layout in which the BVH nodes are stored and Woop's triangle transformation method**- renderkernel.cu**demonstrates two methods of ray/triangle intersection: a regular ray/triangle intersection algorithm similar to the one in[GPU path tracing tutorial 3](http://raytracey.blogspot.co.nz/2016/01/gpu-path-tracing-tutorial-3-take-your.html), denoted as DEBUGintersectBVHandTriangles() and a method using Woop's ray/triangle intersection named intersectBVHandTriangles()

**Demo**



A downloadable demo (which requires an Nvidia GPU) is available from




[github.com/straaljager/GPU-path-tracing-tutorial-4/releases](https://github.com/straaljager/GPU-path-tracing-tutorial-4/releases/)
Working with and learning this ray tracing framework was a lot of fun, head scratching and cursing (mostly the latter). It has given me a deeper appreciation for both the intricacies and strengths of GPUs and taught me a multitude of ways of how to optimise Cuda code to maximise performance (even to the level of assembly/PTX). I recommend anyone who wants to build a GPU renderer to sink their teeth in it (the source code in this tutorial should make it easier to digest the complexities). It keeps astounding me what GPUs are capable of and how much they have evolved in the last decade.

The next tutorial(s) will cover direct lighting, physical sky, area lights, textures and instancing. I've also had a few requests from people who are new to ray tracing for a more thorough explanation of the code from previous tutorials. At some point (when time permits), I hope to create tutorials with illustrations and pseudocode of all the concepts covered.

## 15 comments:

Awesome progress!





"I've also had a few requests from people who are new to ray tracing for a more thorough explanation of the code from previous tutorials. At some point (when time permits), I hope to create tutorials with illustrations and pseudocode of all the concepts covered."

It would be awesome to see these tutorials, but for all of you out there with questions, if you have any questions regarding raytracing or pathtracing you can always ask them on one of the subreddits for raytracing:

https://www.reddit.com/r/raytracing

https://www.reddit.com/r/pathtracing

There are plenty of people there willing to explain these questions with joy!

Awesome renders!





"I've also had a few requests from people who are new to ray tracing for a more thorough explanation of the code from previous tutorials. At some point (when time permits), I hope to create tutorials with illustrations and pseudocode of all the concepts covered."

It would be awesome to see these tutorials, but for all of you out there with questions, if you have any questions regarding raytracing or pathtracing you can always ask them on one of the subreddits for raytracing:

https://www.reddit.com/r/raytracing

https://www.reddit.com/r/pathtracing

There are plenty of people there willing to explain these questions with joy!

Great update Sam. I always look forward to your posts. What do you think can be done next to improve the path tracer - how about if we can store the rays that hit the camera and reuse them on the next frame (not sure if this would work with the current camera type). This would be similar to the way Doom does it's screen space reflections.

Thanks Robbin. There's also the OMPF forum (ompf2.com) for ray tracing related questions, frequented by ray tracing researchers. I learned heaps about ray/path tracing from the discussions there.


Anonymous: not sure what you mean by reusing rays that hit the camera. Rays are being shot from the camera here, the probability that they hit the lens/aperture is very small. I believe screen space reflections are just reflected view vectors (eye rays) around the normal of the surface point they hit. The reflected geometry must also be present in screen space for it to work, so it's quite limited. It sounds like Doom is only updating reflections every few frames.

There are standard techniques to reuse rays/samples like spatiotemporal reprojection, but it's difficult to avoid artifacts in scenes with highly random movement (from the camera or objects in the scene). I'm currently looking into a way to transform the scene geometry (and rays) into frequency space using 3D Fourier transforms, which promises to be a very powerful way to filter out high frequency geometric detail from distant objects. Making it fast and efficient is where it really becomes interesting.

I see that many Render Engines are moving from Race tracer to Path Tracing. So Does Path tracking prove better quality than Race Tracer ? Please answer for me! Thank you!

Houdine suppy: don't know if path tracking provides better quality than race tracing, but path tracing definitely yields higher quality images than ray tracing. See this link: http://home.lagoa.com/2014/04/ray-tracing-vs-path-tracing-in-plain-english/

Great to see an update, I too have just implemented this BVH construction paper! And thanks for responding to my e-mails when I'm clueless and confused.


You can read my blog here, it's not as verbose as yours but it shows some of my progress:

http://henrikdahlberg.portfoliobox.net/dh2323projectblog

Hi Henrik, great progress on your renderer. The most recent screenshots with subsurface scattering look fantastic.

Very great job! I have read your last three GPU path tracing tutorial and implemented my very first CUDA path tracer. I am looking forward to your next post about how to efficiently implement direct lighting, especially MIS, on CUDA!

Can we create compact bvh layout(woop tri buffer, nodes, and tri indices) parallel on gpu? Or it's can't be parallelized, and therefore can not be realized on the gpu?

Just awesome !!!

hello Sam! I'm a student that really want to learn "real-time path-tracing".

First, thanks for your work for beginners like me . Now I have a problem need your help.

when I try to build this code in visual studio 2015, In this part of code, asm("vmin.s32.s32.s32.min %0, %1, %2, %3;" : "=r"(v) : "r"(a), "r"(b) , line 96 to 99, I got error like "expected a ')'", I don't know how I need to do, thanks.

Thanks for this nice self-contained example!




I saw that your code did not yet use tex1Dfetch to fetch the BVH nodes, so I fixed that on a forked repository on Github and sent a pull request.

The trick for getting the tex1Dfetch to work is to use BVH_Compact2, which divides all node addresses by 16 (sizeof(float4)), so that they work as indices for tex1Dfetch.

I removed the global memory pointers from the intersection routing, since now everything is fetched from textures, as in the original kernels from NVidia.

Nice optimisation, thanks!


Storing the BVH in texture memory was on the todo list, but never got around implementing it.

Thanks alot for these awesome posts :)

Post a Comment