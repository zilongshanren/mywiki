---
title: EGSR 2011 paper on real-time noise-free GPU path tracing
url: http://raytracey.blogspot.com/2011/07/egsr-2011-paper-on-noise-free-real-time.html
author: Sam Lapere
published: '2011-07-04'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Just read an interesting paper called "


[Guided Image Filtering for Interactive High-quality Global Illumination](http://graphics.tu-bs.de/publications/Bauszat2011GIF/)" by Bauszat, Eisemann and Magnor, which was accepted at EGSR 2011. The paper describes a novel method for edge-aware filtering of noisy path traced images using the normal and depth buffers instead of the noise image itself. The indirect lighting is filtered separately from the direct lighting and the whole pipeline (path tracing + filtering) is implemented on the GPU using CUDA (the numbers in the paper are obtained with a GTX 285). The new method is compared to cross bilateral filtering and the[edge-avoiding à-trous wavelet filter](http://www.uni-ulm.de/in/mi/graphics/atrous-filter.html)described in a HPG paper from last year and the results seem very promising.I very much agree with the introduction to the paper:

"...many approximations exist to reproduce certain effects of the real global illumination and try to incorporate it into a classic rasterizer. Unfortunately, in order to speed up the computation they are either aiming at simulating only a single effect, like soft shadows [ED08] or ambient occlusion [RGS09] or they are are limited to certain constraints, requiring low-frequency lighting environments [SKS02], static scenes [LSK07] or precise parameter adjustment for varying scenes [RGK08]. Code complexity increases tremendously for systems that simulate global illumination effects using rasterization because multiple approximations need to be combined to achieve a sufficient visual quality. On the other hand path tracing naturally incorporates all these effects with a very simple rendering algorithm.

Another drawback of approximative algorithms is that they not necessarily converge to the correct result. Therefore, they will only become faster with better hardware but do not necessarily produce a higher quality result. Instead of trying to incorporate global illumination effects into a rendering pipeline which is not capable of physically correct rendering, it is a much more promising design to take a physically valid rendering approach and implement approximative algorithms on top to speed up the rendering. Designing them in an adjustable way results in a very future-oriented rendering paradigm."

Research in fast interactive GPU path tracing with minimal noise has made enormous advancements over the past year and I'm confident that real-time high-quality path traced global illumination for games will be feasible soon.


## 3 comments:

I hope this info helps:


http://newsroom.intel.com/community/intel_newsroom/blog/2011/06/07/intel-labs-collaborative-efforts-speed-technological-breakthroughs-shape-future-of-computing

I've heard about it, but I'm not very impressed with Intel's latest ray tracing endeavours:






- Intel's Embree path tracer needs a 40-core CPU (a Quad Xeon server with 10 physical cores per CPU, see http://ompf.org/forum/viewtopic.php?f=8&t=5163) to rival the speed of an unbiased GPU path tracer using just one GPU. Embree's CPU code is no doubt extremely optimized and efficient (using SSE and AVX instructions), but the brute force performance of today's GPUs is just unbeatable, no matter how good the CPU code is. And this GPU/CPU performance ratio (currently ~10-40x) is only going to increase with future hardware generations.

- Pohl's raytraced version of Wolfenstein needs a server with 4 Knight's Ferry cards (each containing 32 cores)and it still looks worse than a PC game from 2001, because of the basic shading

- the Larrabee joke: the first (and also last) public demo of Larrabee at IDF 2009 was comedy gold. They showed a ray traced version of Quake wars (which looked much worse than the regular Quake Wars) with a static camera view and horrible framerates. I've never seen a traditional rasterized game run on Larrabee. The really sad news is that the biggest victim of Larrabee's failure was Offset Software (developer of the cancelled Project Offset). You should definitely read this article:

http://news.bigdownload.com/2010/12/15/interview-we-chat-with-sam-mcgrath-about-fractiv-what-happened/

I'm afraid that Knight's Ferry and Knight's Corner won't change much for high performance and high quality ray tracing and path tracing, which seem to be shifting entirely (BVH construction + ray traversal + shading) to the GPU.

Killing off Project Offset was indeed a very bad decision, such a waste of talent.

Post a Comment