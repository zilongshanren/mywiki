---
title: Sfera, the first real-time path traced game based on OpenCL!
url: http://raytracey.blogspot.com/2011/12/sfera-first-real-time-path-trace-game.html
author: Sam Lapere
published: '2011-12-10'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

![](../../assets/910451418648a1d9.png)


![](../../assets/910451418648a1d9.png)

This is very cool: there is a new game called Sfera, it's using only spheres and is rendered with real-time path tracing on the GPU and CPU using OpenCL. The developer of the game, Dade (David Bucciarelli), is a LuxRender developer who is the first to make a working implementation of OpenCL-based unbiased path tracing on ATI cards. He created SmallptGPU, SmallLuxGPU and LuxRays.

The demo features HDR image based lighting, bump mapping, multiple physically accurate materials, Bullet physics and multi-GPU support. I think it is absolutely awesome to see more developers using the power of the GPU (I'm glad that this time OpenCL and GPUs from ATI are used) to create amazing looking simple games with real-time photorealistic lighting. This game is a very nice proof-of-concept to show that real-time photorealism is very close. I hope this is the beginning of a paradigm shift for game graphics from rasterization to real-time ray tracing. The code is also open source and can be found at

[http://code.google.com/p/sfera/](http://code.google.com/p/sfera/)(includes executables for Windows and Linux).More info about the game Sfera can be found at

## 6 comments:

Very cool video.



I was wondering, does anyone have any papers that talk about the accumulation of pixels over time? I was wondering if instead of a rendering a frame at a certain spp, could rays just be accumulated intelligently to do away with discreet frames altogether for scenes in motion? I picture some accumulation/motion blur system that would be tied to the physics/geometry update engine instead of a certain frame rate.

I haven’t been able to find anything on this subject. Thanks!

Mmm, too bruteforce; even we have 10x more processing power (10x GTX470)and 2x algoritm speed optimizations - we will still have only 1920x1080 render with same noize, on same simplest scene, with same low fps...


Can someone find less bruteforce ways of use path-tracing? In my imagunation its something like uisal DirectX11/OGL4x game render plus realtime raytracing that used not for full scene lighting/texturing but for creating render tasks for DirectX11/OGL4x render? E.g. we do some raytracing for define what game renderer need to do.

Anyway, this game - its like small miracle in my hands :) ^_^

@Anonymous,I think you are referring to something called "frameless rendering". There is a video on this technique at http://video.google.com/videoplay?docid=-8018915362682031037


Lex4art: I agree with your analysis, but you should not forget that if Nvidia or AMD or IMGTec would decide to add fixed function ray tracing hardware to their GPUs (for ray/primitive intersection and traversal), ray tracing would suddenly become an order of magnitude faster. But before that could happen, the advantages of real-time ray tracing must be clearly proven and ready for mainstream use. This is one of the main reasons that I am developing prototype games with real-time path tracing.

@Ray Tracey, Thanks! Exactly what I was thinking of! It would be interesting to see something like that on today's real-time ray tracers.

Post a Comment