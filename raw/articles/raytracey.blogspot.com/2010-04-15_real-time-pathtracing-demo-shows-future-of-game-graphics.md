---
title: Real-time pathtracing demo shows future of game graphics
url: http://raytracey.blogspot.com/2010/04/real-time-pathtracing-demo-shows-future.html
author: Sam Lapere
published: '2010-04-15'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Yessss!!! I've been anticipating this for a long time: real-time raytraced high-quality dynamic global illumination which is practical for games. Until now, the image quality of every real-time raytracing demo that I've seen in the context of a game was deeply disappointing:


- Quake 3 raytraced (

[http://www.youtube.com/watch?v=bpNZt3yDXno](http://www.youtube.com/watch?v=bpNZt3yDXno)),

- Quake 4 raytraced (

[http://www.youtube.com/watch?v=Y5GteH4q47s](http://www.youtube.com/watch?v=Y5GteH4q47s)),

- Quake Wars raytraced (

[http://www.youtube.com/watch?v=mtHDSG2wNho](http://www.youtube.com/watch?v=mtHDSG2wNho)) (there's a pattern in there somewhere),

- Outbound (http://igad.nhtv.nl/~bikker/projects.htm),

- Let there be light (

[http://www.youtube.com/watch?v=33yrCV25A14](http://www.youtube.com/watch?v=33yrCV25A14),

- the last Larrabee demo showing an extremely dull Quake Wars scene (a raytraced floating boat in a mountainous landscape, with some flying vehicles roaring over, Intel just showed a completely motionless scene, too afraid of revealing the low framerate when navigating)

[http://www.youtube.com/watch?v=b5TGA-IE85o](http://www.youtube.com/watch?v=b5TGA-IE85o),

- the Nvidia demo of the Bugatti at Siggraph 2008 (

[http://www.youtube.com/watch?v=BAZQlQ86IB4](http://www.youtube.com/watch?v=BAZQlQ86IB4))

All of these demo's lack one major feature: realtime dynamic global illumination. They just show Whitted raytracing, which makes the lighting look flat and dull and which quality-wise cannot seriously compete with rasterization (which uses many tricks to fake GI such as baked GI, SSAO, SSGI, instant radiosity, precomputed radiance transfer and sperical harmonics, Crytek's light propagation volumes, ...).


The above videos would make you believe that real-time high quality dynamic GI is still out for an undetermined amount of time. But as the following video shows, that time is much closer than you would think:


[http://www.youtube.com/watch?v=dKZIzcioKYQ](http://www.youtube.com/watch?v=dKZIzcioKYQ)![](../../assets/0b968dd135f6f617.img)


![](../../assets/0b968dd135f6f617.img)

![](../../assets/2c6b8253b5842f1e.img)


![](../../assets/2c6b8253b5842f1e.img)

The technology demonstrated in the video is developed by Jacco Bikker (Phantom on ompf.org, who also developed the Arauna game engine which uses realtime raytracing) and shows a glimpse of the future of graphics: real-time dynamic global illumination through pathtracing (probably bidirectional), computed on a hybrid architecture (CPU and GPU) achieving ~40 Mrays/sec on a Core i7 + GTX260. There's a dynamic floating object and each frame accumulates 8 samples/pixel before being displayed. There's caustics from the reflective ring, cube and cylinder as well as motion blur. The beauty of path tracing is that it inherently provides photorealistic graphics: there's no extra coding effort required to have soft shadows, reflections, refractions and indirect lighting, it all works automagically (it also handles caustics, but not very efficiently though). The photorealism is already there, now it's just a matter of speeding it up through code optimization, new algorithms (stochastic progressive photon mapping, Metropolis Light Transport, ...) and of course better hardware (CPU and GPU).


The video is imo a proof of concept of the feasibility of realtime pathtraced games: despite the low resolution, low framerate, low geometric complexity and the noise there is an undeniable beauty about the unified global lighting for static and dynamic objects. I like it very, very much. I think a Myst or Outbound-like game would be ideally suited to this technology: it's slow paced and you often hold still for inspecting the scene looking for clues (so it's very tolerant to low framerates) and it contains only a few dynamic objects. I can't wait to see the kind of games built with this technology. Photorealistic game graphics with dynamic high-quality global illumination for everything are just a major step closer to becoming reality.

The video is imo a proof of concept of the feasibility of realtime pathtraced games: despite the low resolution, low framerate, low geometric complexity and the noise there is an undeniable beauty about the unified global lighting for static and dynamic objects. I like it very, very much. I think a Myst or Outbound-like game would be ideally suited to this technology: it's slow paced and you often hold still for inspecting the scene looking for clues (so it's very tolerant to low framerates) and it contains only a few dynamic objects. I can't wait to see the kind of games built with this technology. Photorealistic game graphics with dynamic high-quality global illumination for everything are just a major step closer to becoming reality.

UPDATE: I've found a good mathematical explanation for the motion blur you're seeing in the video, that was achieved by averaging the samples of 4 frames (http://www.reddit.com/r/programming/comments/brsut/realtime_pathtracing_is_here/):

it is because there is too much variance in lighting in this scene for the numbers of samples the frames take to integrate the rendering equation (8; typically 'nice' results starts at 100+ samples/per pixel). Therefore you get noise which (if they implemented their pathtracer correctly) is unbiased. Which means in turn that the amount of noise is proportional to the inverse of the square of number of samples. By averaging over 4 frames, they half the noise as long as the camera is not moving.

UPDATE2: Jacco Bikker uploaded a new, even more amazing video to youtube showing a rotating light globally illuminating the scene with path tracing in real-time at 14-18 fps (frame time: 55-70 ms)!

[http://www.youtube.com/watch?v=Jm6hz2-gxZ0&playnext_from=TL&videos=ZkGZWOIKQV8](http://www.youtube.com/watch?v=Jm6hz2-gxZ0&playnext_from=TL&videos=ZkGZWOIKQV8)

![](../../assets/db01dbd2b85a9efb.jpg)


![](../../assets/db01dbd2b85a9efb.jpg)

![](../../assets/880ebdd2d25778b9.jpg)


![](../../assets/880ebdd2d25778b9.jpg)

The frame averaging trick must have been used here too, because 6 samples per pixel cannot possibly give such good quality.

## 6 comments:

Perhaps some of us know Jacco Bikker as the author of an raytracing tutorial from the good old days of flipcode. Nice to see that he is still working on computer graphics.

Yes, the guy certainly knows what he's doing and has a forward-looking vision on game graphics. He can afford it to experiment with exotic algorithms like path tracing, unlike the big game companies who are restricted by 30 fps/720p demands.

I'm curious what speedups can be gained by using new algorithms and will the scene still remain dynamic? I know in video games everything is moving towards realtime/dynamic everything. CryEngine 2 is an example of not prebaking anything.


If new GPUs can give a 10x gain in 10yrs and algorithms give a 2-5x gain then it seems like having this in games isn't that far off. Or am I missing something?

@ DIY-CNC





This technology is exactly doing what you said: real-time dynamic global illumination for everything: scene, objects, characters, lights can be moved and will cast soft shadows, nothing is precomputed. This algorithm delivers much higher quality than wat Crytek is doing: Crytek is using tricks and approximations with their Light Propagation Volumes, while path tracing is the de facto standard in GI, nothing can beat it's quality.

Researchers are looking to implement newer algorithms on the GPU which deliver the same or comparable quality as (bidirectional) path tracing, progressive photon mapping being one of them (in fact, the latest OptiX SDK has a sample implementation of this). "Regular" global photon mapping has also been adapted to the GPU by Rui Wang and Kun Zhou with great results. Irradiance caching is probably also possible on the GPU and could deliver some serious speed up at the expense of a little quality loss.

Your estimate of a 10x gain in GPU speed over 10 years is way too conservative imo: I think 100-200x is more accurate, so you probably won't have to wait that long before seeing these algorithms or variations of them in games :-)

Keep in mind that this pathtraced animation was done on one Core i7 (quad-core machine)+ one GTX260. Imagine what it will look like on a hexacore (six cores) + a GTX480! :-D

Looks sick! I want it.

Sjonnie, you'll have to wait a bit, the code and demo will be released in September (according to Phantom on ompf forum).

Post a Comment