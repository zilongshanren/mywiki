---
title: Real-time rendered animation previews with Octane Render
url: http://raytracey.blogspot.com/2012/07/real-time-rendered-animation-previews.html
author: Sam Lapere
published: '2012-07-27'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

This is a major breakthrough in rendering: the last version of Octane Render can now render complex animatable objects completely in real-time with path tracing. This has never been done before and is a game changer for animation previsualisation.

Real-time ray tracing of scenes with highly detailed dynamic objects has always been considered as a near impossible feat and has held ray tracing back as a rendering method for interactive applications such as games. Until now: we have adapted Octane in such a way that


The following video was made with the Octane plug-in for 3ds Max and demonstrates that the acceleration structure of the animated robot



__it can handle dynamic scenes effortlessly and in real-time without compromising the ultrafast GPU path tracing performance.__The following video was made with the Octane plug-in for 3ds Max and demonstrates that the acceleration structure of the animated robot

**can be updated instantly while rendering an instant preview of the lighting**. The transformer in the animation was used before in a demo that I've made with Brigade some time ago ([http://raytracey.blogspot.co.nz/2012/04/real-time-photorealistic-path-tracing.html](http://raytracey.blogspot.co.nz/2012/04/real-time-photorealistic-path-tracing.html)) and I always wanted to see it animated and rendered in real-time with path tracing, which can now be done with Octane and will be shown in another video :
This is the final render, with motion blur using subframes in 3ds Max:

[https://www.youtube.com/watch?v=3NkN7JNbmnQ](https://www.youtube.com/watch?v=3NkN7JNbmnQ)

Some screens from an early render:

UPDATE: a video of the same animation with materials

Another video, showing a real-time deforming hand, rendered with real-time path tracing:

You'll be able to follow the progress of Octane Render and all of our tests on a dedicated blog soon (this post will also be moved to the new blog).

## 20 comments:

Ups, the bold claims again :) Which part of these videos have been impossible and never seen before? What exactly is the game changer?

The game changer is that this workflow makes everything vastly more intuitive. You can now render an animation with highly detailed moving characters and objects, fully path traced and and in real-time if you throw enough GPUs at it. This is what I have been dreaming of doing for over ten years: real-time animation rendering with photoreal quality.




When I'm playing with Octane and seeing these beautiful animated scenes rendering before my eyes, I'm smiling like a retard, it's a dream come true.

People have been talking about rendering Toy Story in real-time for over ten years, but this is so much better and much more fun. It's as if you are watching a movie and you can interact with it. No other software can do this, the key here is that runs in real-time and you can literally have a GPU renderfarm in a PC box, rendering your animation before your eyes in full detail.

I'm telling you, playing with Octane and Brigade is the most fun and exciting thing I've experienced in years graphicswise. And I'm convinced that we can push this tech even further to the point that even the most demanding scenes can be rendered in full photorealistic detail in real-time. :D

Very very nice!!

Have you covered CentiLeo (CentiLeo.com) also? Also quite interesting stuff...

Hmm..CentiLeo does look very impressive...the 1280x720 render converges nicely within a few seconds using a setup that is approximately 4.5x slower than Sam's setup, whilst using an additional +2 ray bounces (10 total) plus the added benefit of out of core geometry/texture management. Brigade has competition!

I know Sam keeps talking about Brigade as revolutionary, and Indeed it probably is, but without a comparison video between different path tracers (such as CentiLeo & Octane) using a standard test scene, how do we know it is?



A few people in the past have mentioned doing something similar (I asked for a comparison with Laguna GPU tracer) but the answer has always been that Brigade is so well optimised to real time path tracing it would destroy the competition. I really welcome this and hope it is true, but we need proof, not reassurance.

keep up the good work!

@Anonymous and Centileo does just use one GeForce GTX 485M (how does it compare to two GTX 580s in the brigade setup)?

(I think that makes the Brigade setup maybe 4-5 times as fast).

Taking the 3DMark score as an indication of how these two GPUs perform relative to each another (probably not wildly unfair as based on same architecture), a single 485M scores 3370 and the GTX 580 scores 6560 ...roughly double.


So GTX580SLI is roughly 4x more powerful than a single 485M

I've seen the recent videos of CentiLeo, looks neat and I might write a blogpost on it.

Viewing raytraced animations real-time in viewport is not new. Here's how it's done in Blender/Cycles (freeware):


http://www.youtube.com/watch?v=PxrMQi-XoLQ&feature=player_detailpage#t=209s

I guess that Octane is probably quite abit faster than Cycles, but your point is valid in that, while Octane will look better, (let's say for arguements sake) a 2-3x performance increase would only have marginal impact on workflow efficiency, if any.



Sure you can throw more GPUs at Octane, but this feature could be quite easily added to any path tracer. And for Blender's audience, anything more than one high performance GPU is beyond most.

I guess the appeal of Octane is it is faster and likely supports more physically correct visual effects than Cycles with more focus on professional grade features. And for professional use where you're rendering thousands, if not tens of thousands of frames, a 2-3x decrease in rendering time is alot of time and money. But then Blender/Cycles is free.

I think what is a missed opportunity is that the video examples Sam posted don't really demonstrate any advantages to using realtime path traced viewports over the standard view as no complex lighting/caustics or reflections are utilised. Sure people here appreciate it, but it is not anymore intuitive than the standard view, and certainly rasterization with SSAO would have produced better results. I think there was abit too much of a tradeoff between performance and more complex (but demanding) lighting in order to highlight the realtime selling point.



However, when more realistic lighting effects are deployed I'm sure Octane would shine in this regard, and show some improvement over say, Cycles which may struggle (only a guess mind you).

@antzrhere




Octane & Cycles both got selling points. Octane's probably more like 10x faster for any complex lightning situation because there's custom MLT implementation. Cycles currently is just pure path tracing. For professionals who want speed today it's probably worth the price for speed alone.

On the other hand, cycles is free, node system is truly great, and every parameter fully animatable in blender.

When I was little I examined the world and tried to understand soft shadows, ambient lightning and suff. Now I can create new worlds by playing with the rules of light, in my home without expensive software, without waiting... much. We live interesting times!

From my experience, octane is much faster than cycles and higher quality because it is a spectral renderer.


Cycles is nice to quickly set up the lighting in your scene, but I use octane for the beauty renders. I hope blender will get an octane plug-in soon, this real-time animation rendering looks pretty useful 0_o

I think Cycles is awesome. In fact I'm a fan of all fast GPU path tracers, whether that be Octane, Brigade, Cycles, CentiLeo, SmallLuxGPU, etc. I like them all because they will all bring us closer to the ultimate goal in rendering, creating images that are indistinguishable from real life.



The embarrassingly parallel nature of path tracing and the massive parallellism of GPUs are a match made in heaven.

I'm starting to think that GPUs are actually much better suited to path tracing than rasterization, because it scales so much better than rasterization over multiple GPUs. Octane for example scales perfectly with the number of cores/GPUs, whereas a rasterizer gets only about 50% better performance from an additional GPU.

Sam,


any video of the Brigade demo at siggraph 2012?

It's nearly impossible to make a decent video of the Siggraph demo, I've tried several screen recording tools (Fraps, Camtasia, BlueBerry, Jing) but the framerate completely sinks when they're capturing.


I'm uploading a video to youtube now (rendered at 720p), but I'm not sure if the result will be presentable at all.

Sam,


arigatou!

Hi Sam. I hope for video or at least some screens. I kind a miss brigade stuff :-)

Anonymous, expect a new post with video and screens soon, it will not be exactly the same as what was shown at siggraph though.

Post a Comment