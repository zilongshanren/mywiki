---
title: HPG paper and video of "Improving SIMD Efficiency for Parallel Monte Carlo
  Light Transport on the GPU"!
url: http://raytracey.blogspot.com/2011/06/hpg-paper-and-video-of-improving-simd.html
author: Sam Lapere
published: '2011-06-21'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Another post on the work of Dietger van Antwerpen, but that's because his research efforts for GPU path tracing are so damn amazing and groundbreaking. I can't stop imagining what the possibilities could be when implemented in a real-time path tracer for games. His HPG2011 paper "Improving SIMD Efficiency for Parallel Monte Carlo Light Transport on the GPU" and an accompanying video are available here:




The video shows a side-by-side comparison between standard path tracing (PT), bidirectional path tracing (BDPT) and Metropolis light transport (MLT) in a number of scenes with complex lighting. The difference in efficiency of the MLT and BDPT algorithms compared to regular path tracing is huge: for example, the kitchen scene (indirect lighting, actually it's lit by light passing through a lens, essentially a caustic) converges extremely slowly with PT and is still mostly pitch black (because the probability of a random path hitting a small light source behind a lens is very low), while BDPT (paths starting simultaneously from the camera and the light source, "meeting each other half way") and MLT (paths starting randomly, but once an important light contributing path is found, nearby paths are explored) both do a much better job and show a recognizable scene in a matter of milliseconds. All these algorithms are running completely on the GPU with almost zero CPU load. The end of the video shows a flooded Cornell box scene rendered with MLT at interactive rates, showing that the caustic light pattern on the floor converges very fast (something that would take a very long time for a regular path tracer). The last page of the


An often recurring criticism of using the GPU for rendering is that for scenes with complex lighting and materials, the CPU outperforms the GPU because the CPU is able to use smarter and more efficient algorithms (like MLT and BDPT) while the GPU is only efficient at regular, "dumb" path tracing. This is no longer true as proven by this paper: not only can GPUs use more efficient rendering algorithms like BDPT and MLT, they can also do it an order of magnitude faster than the CPU! The table comparing performance between GPU rendering and CPU rendering (GTX 480 vs Core i7 920) demonstrates that, depending on the scene, PT is 10-18x, BDPT 8-15x and MLT 9-15x faster on the GPU than on the CPU!!


It's amazing to see that the still very young field of physically based GPU rendering has made such tremendous advancements in just a couple of months (thanks to guys like Dietger among others). I can't wait to see where this field is going to head during the next year with better hardware (Nvidia Kepler, AMD Graphics Core Next) and even more optimized and efficient algorithms. It really is mind-boggling...


[http://graphics.tudelft.nl/~dietger/HPG2011/index.html](http://graphics.tudelft.nl/%7Edietger/HPG2011/index.html).![](../../assets/16687f1b774de18a.png)

![](../../assets/16687f1b774de18a.png)

The video shows a side-by-side comparison between standard path tracing (PT), bidirectional path tracing (BDPT) and Metropolis light transport (MLT) in a number of scenes with complex lighting. The difference in efficiency of the MLT and BDPT algorithms compared to regular path tracing is huge: for example, the kitchen scene (indirect lighting, actually it's lit by light passing through a lens, essentially a caustic) converges extremely slowly with PT and is still mostly pitch black (because the probability of a random path hitting a small light source behind a lens is very low), while BDPT (paths starting simultaneously from the camera and the light source, "meeting each other half way") and MLT (paths starting randomly, but once an important light contributing path is found, nearby paths are explored) both do a much better job and show a recognizable scene in a matter of milliseconds. All these algorithms are running completely on the GPU with almost zero CPU load. The end of the video shows a flooded Cornell box scene rendered with MLT at interactive rates, showing that the caustic light pattern on the floor converges very fast (something that would take a very long time for a regular path tracer). The last page of the

[HPG 2011 paper](http://graphics.tudelft.nl/%7Edietger/HPG2011/paper.pdf)contains a very interesting comparison between a fully converged reference image and a PT, BDPT and MLT image after just 30 seconds on a GTX 480.An often recurring criticism of using the GPU for rendering is that for scenes with complex lighting and materials, the CPU outperforms the GPU because the CPU is able to use smarter and more efficient algorithms (like MLT and BDPT) while the GPU is only efficient at regular, "dumb" path tracing. This is no longer true as proven by this paper: not only can GPUs use more efficient rendering algorithms like BDPT and MLT, they can also do it an order of magnitude faster than the CPU! The table comparing performance between GPU rendering and CPU rendering (GTX 480 vs Core i7 920) demonstrates that, depending on the scene, PT is 10-18x, BDPT 8-15x and MLT 9-15x faster on the GPU than on the CPU!!

It's amazing to see that the still very young field of physically based GPU rendering has made such tremendous advancements in just a couple of months (thanks to guys like Dietger among others). I can't wait to see where this field is going to head during the next year with better hardware (Nvidia Kepler, AMD Graphics Core Next) and even more optimized and efficient algorithms. It really is mind-boggling...

## 3 comments:

Hello,



Please contact me at aron@foundthefuture.com. I am interested in speaking with you and gaining some of your industry incites.

Aron

Do these papers have any impact on the competition? I mean it is all good in theory and such but doesn’t it really come down to how it is coded, such as the acceleration structures and data handling?

I'm sure this paper is going to have an impact in advancing the field of GPU rendering, even though some GPU renderers already have something similar to MLT, like Octane (see http://raytracey.blogspot.com/2010/09/octane-render-preparing-to-smite.html), Luxrender SLG2.0 and OptiX.



I think this research is going to be very useful for developers who are struggling with getting advanced physically based rendering algorithms to work on the GPU or who are looking to optimizing their existing implementation.

There's also going to be another paper about optimized GPU path tracing at HPG, by Ingo Wald (an expert in real-time ray tracing), so this is moving really fast.

Post a Comment