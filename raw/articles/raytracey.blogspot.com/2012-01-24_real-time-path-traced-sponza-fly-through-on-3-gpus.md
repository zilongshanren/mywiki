---
title: Real-time path traced Sponza fly-through on 3 GPUs!
url: http://raytracey.blogspot.com/2012/01/real-time-path-traced-sponza-fly.html
author: Sam Lapere
published: '2012-01-24'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I've sent the executable of the teapot in Sponza scene to a friend, szczyglo74 on Youtube, who has a much more powerful rig than my own (a PC with 3 GPUs: 1 GTX 590 (dual gpu card) + 1 GTX 460) and who made some very cool real-time videos of the sponza scene. Many thanks szczyglo!

The maximum path depth in each of these videos is 4 (= 3 bounces max):

__32 spp per frame__(480x360, 1/4th render resolution,

__8 fps__):

[http://www.youtube.com/watch?v=fVAl-oKAL9I](http://www.youtube.com/watch?v=fVAl-oKAL9I):awesome video, shows real-time convergence in most parts of the scene

32 spp per frame (640x480, 1/4th render resolution, 4.7 fps):

8 spp per frame (480x360, 1/4th render resolution, ~21fps):

4 spp per frame (640x480, 1/4th render resolution, ~18fps):

The above videos clearly show the importance of the number of samples per pixel per frame in indirectly lit areas: despite the low max path depth of 4, it is still possible to discern some details in the corridors in the first two videos (32 spp per frame) during navigation, while the last two videos (8 and 4 spp per frame) are obviously too dark in these regions, but clear up very fast with a stationary camera. Note that these tests were made with a kernel that is not optimized for indirect lighting (no multiple importance sampling is used here).

I'm quite happy with the sense of photorealism in these videos, especially when you consider that this is just brute force path tracing (no caching, filtering or interpolation yet nor anything like image reconstruction, adaptive sampling, importance sampling, bidirectional pt, eye path reprojection, ... which are all interesting approaches). A textured version of Sponza will probably further increase the realism, which is something I will try in a next test.

## 10 comments:

Your frameblending has one big flaw: Even small rotation is causing a lot of blurring. But there is a simple fix, rotate previous frame by the delta rotation to the previous frame before blending and you will only have motionblur for translation and moving objects. Just calculating the dx,dy on the midpoint of the previous frame will be a huge improvement.

Thanks for the tip! The motion blur that I'm using is a really cheap hack (just three lines of OpenGL code). Can you point me to a tutorial on how to implement your method in OpenGL?

I dont know of any webpage but you could look at it this way. Store the 4 corner directions of the previous frame. If you let the originate from the current camera position they will each project to a single point in the framebuffer. Draw a quad between these points with the last frame as a texture for the quad. Done!


I think you will se a huge improvement from this. If you want to take it one step further then you could reproject each sample individually and compensate for the translation as well. Bit more work and more expensive as well. Assign a motion vector for each sample and you will take care of moving objects as well.

There is so much more you could do, for example adaptively distribute samples where there is more change.

Thanks! I was meaning to dive into more sophisticated motion blur techniques including motion vectors, and also to explore reprojection techniques to reuse pixels/samples in order to lazily update dynamically changing lighting over several frames. There are some good papers floating around, I'll see how far I'll get.

Adaptive sampling is something that could help, but I'm not sure if it's feasible in a real-time context. I read somewhere that it's quite expensive to determine the pixels that need more samples. But you never know until you try it yourself :)

Simple adaptive sampling: Pick a random point p in the framebuffer, calculate its value with x number of samples. Compare with previous frame, if enough difference spend y number of samples in the neighbourhood of p.

Stochastic noise is your enemy here, x needs to high enough to fight it.

Interesting and simple. It's obvious where I would like to spend more samples in the Sponza scene, but as you said, the initial number of samples must be high enough to decide if more sampling is required, which I doubt is doable in real-time. It's certainly worth trying though (need to read more on this and other noise reduction techniques).

Why wouldn't it be doable? You don't have to pick that many samples. What happens if you get an incorrect answer? If you distribute the samples intelligently you will pretty much end up with a worst case of what you started with.



Perhaps distribute samples something like this:

50% evenly over the screen

10% at a few places with perhaps 32 samples each to decide where to spend the last 40%

A very rough guess would be a worst case efficiency of 80% and an average of 200% over evenly distributed. Can't back it up, it's just an educated guess.

seems like a good sampling strategy. I have to learn more about CUDA and sampling before I can try this out :)



Just to be clear, I'm not developing Brigade, but just testing some ideas with it. Jacco Bikker and Jeroen van Schijndel are the main developers.

I'm interested in all sorts of noise reduction methods and more efficient sampling/tracing, but it is not something I'm able to actively contribute to in the very near term (in terms of programming). Currently I'm focussing on making something playable in real-time.

Post a Comment