---
title: Bullet Physics! It works!!!
url: http://raytracey.blogspot.com/2011/07/bullet-physics-it-works.html
author: Sam Lapere
published: '2011-07-20'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

![](../../assets/a702209a43807654.jpg)


![](../../assets/a702209a43807654.jpg)

I've been wanting to integrate the Bullet Physics library in the real-time path tracing demo's like Tokap and Unbiased Truck Soccer for a while now (since February actually), but I lacked the programming knowledge and experience to make it work back then. Today I've finally made it work, which will open up lots of new gameplay ideas for future demo's.

I retrofitted TOKAP (the real-time path traced 3D Pong) with the Bullet physics library and the results are awesome, even though I have only tested it on a very low-end 8600M GT.

Below is a very low-res video captured in real-time on a 8600M GT at 256x256 resolution and 4spp (I will soon make a higher quality video with a GTS450):

The physics simulation can be stepped and paused by holding down the UP key. You can walk around the scene during simulation or when the simulation is paused as shown in the video. The simulation is deterministic, so it will produce the exact same result every time it runs.

Now that I've passed this hurdle, the possibilities are endless and I will finally be able to implement proper car physics (see

[http://raytracey.blogspot.com/2011/03/unbiased-truck-soccer-first-physics.html](http://raytracey.blogspot.com/2011/03/unbiased-truck-soccer-first-physics.html)).**The new demo can be downloaded from**

[http://code.google.com/p/tokap-the-once-known-as-pong/downloads/list](http://code.google.com/p/tokap-the-once-known-as-pong/downloads/list)**UPDATE:**The source code is also available at

[http://code.google.com/p/tokap-the-once-known-as-pong/downloads/list](http://code.google.com/p/tokap-the-once-known-as-pong/downloads/list)

## 8 comments:

Congratulations!

That is an epic step forward.

Nice one!


I will try this at home with my gtx580.

Thanks Kerrash!


@ r0ots: can you tell me at what framerate the simulation runs on your 580?

Your last exe don't work on my computer :(




I' might be Win7 64 compatibility problems.

I've tested with Futuristic_Buildings_v2_no_aabb_8spp,I'm arround 50-52 FPS

32spp : 8-10

GTX580, i7 2600k

Wow, those are great numbers :D




50 fps on Futuristic_Buildings_v2 noAAB_8spp? Damn, the 580 is fast! I'm getting only 0.99 fps with the 8spp version and 0.18 fps with the 32 spp version on my 8600M GT :)

It's a shame that the latest exe doesn't work, it could also be an issue with being dependent on the Bullet library.

I've uploaded the source code of my last demo to the google code website, so hopefully you can compile a working version on your system.

I got 22-29 FPS in the:




Futuristic_Buildings_Drivable_Car_noAABB_4spp

The dip occurs mainly when the move light emerges.

But only have a Corei7-920 + GTS250 in this machine.

I've got some old source code around for vehicle physics for a game I wrote in college, you're welcome to?

Sure, I would be very grateful if you send the vehicle physics code. I'm currently basing my vehicle code on an example demo that comes with the Bullet Physics source, but it's quite complicated.



I'm getting 2-5fps in the FutBuildings 4spp version. Still much worse than the GTS250 :)

From looking at the CUDA code, I think that when the 'sun' (sphere[0] in 'Tracer.cu') appears, shadow rays are traced from every primary ray hitpoint, which could explain the framerate dip.

Post a Comment