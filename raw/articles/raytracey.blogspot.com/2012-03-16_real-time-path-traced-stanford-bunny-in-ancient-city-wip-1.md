---
title: Real-time path traced Stanford Bunny in ancient city WIP 1
url: http://raytracey.blogspot.com/2012/03/real-time-path-traced-stanford-bunny-in.html
author: Sam Lapere
published: '2012-03-16'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Working on a new real-time path traced game scene (400k triangles) set in an ancient city and rendered with the Brigade path tracer. The scene is a freely available SketchUp scene created by LordGood. The bunny model is a 5k triangle version of the Stanford Bunny and is dynamic.

- 400k triangle scene

- dynamic objects, receiving the

__exact__same lighting as the game world
- real-time rendered lighting, fully dynamic

- sun/sky light

- artifact free soft shadows, which consume no memory at all

- real-time diffuse global illumination (path traced)

- GPU path tracing on 2 GTX 580 GPUs

Brigade essentially renders light map baking for games obsolete, including radiosity and VPL/LPV based GI methods. More videos with a greater diversity of materials (diffuse, refractive, glossy, reflective) will follow soon.

## 23 comments:

Is it possible to reduce the blurring when the camera and rabbit moves, in future Brigade release?

Wow, very nice..

Is it running on a new build of Brigade?

It looks smoother than before, or maybe it's the illusion by seeing more 'videogames' scenery.

anonymous: the blurring will eventually be toned down, but first I will try implementing a simple noise reducing optimization in the sampling. There are some other enhancements for this kind of outdoor scenes that should greatly reduce the noise (for example, as you can see in the video sunlit areas converge very fast, while parts in shadow converge slower. You could easily redistribute samples to shadowy areas instead of wasting them on the already converged sunlit regions).



FreDre: this is using the latest Brigade code and kernels, and without fraps it's even smoother :)

Ray Tracey: that's actually a nice idea that might help scenes like these, to send more rays to occluded areas. Unless there's some balancing however you may end up with slow frames when going indoor.

True, with this optimization the framerate will vary depending on the amount of direct light in the image, but you could optimize that case as well, e.g. stop tracing shadow rays after the first "pass" when the pixel is in shadow, except near shadow edges to avoid hard shadows.

@Ray Tracey




How do you change resolution in Brigade? I would like to render at 1280 X 720.

Also, how do you bring up the "console" like in your video(at the top)?

@Ray Tracey,


Forgot to ask one more question. How many triangles can Brigade support? I have a GTX 580 3GB card.

Brigade supports about 2M on a 32bit OS. It has recently be ported to 64bit; we haven't tested the new limits, but they will depend on VRAM alone.


- Jacco.

Sam, are you going to get the latest Kepler when it launches? It would be awesome to see the performances with the latest high-end GPU


Also I have a question to Jacco; Is Brigade going to use OpenCL? So it can be GPU agnostic. I heard that OpenCL now is mature, not as much as CUDA but it's getting there.

As it is it is not very usefull of course even on current high end hardware for realtime-game rendering.

This rendering could look much better if done in a different way.

Just render everyting with polygons, and use texture mapping to map the shaddows. The path tracing ould have some value in generating the shadow map on the fly, with for example level of detail. There would be no need to calculate them again for every frame, so they could be calculated in the background at high quality.

As the sun does not move very fast, moving outdour shadows are not really required.

@FreDre: we have an OpenCL version, but currently it is not available with the public distribution of Brigade. Performance is comparable to the CUDA version. On NVidia, the OpenCL version is 20% slower.


Anonymous: you are probably right that there are better ways to handle soft shadows from a slow moving light source. However: the use of path tracing aims to solve the rendering problem in a more elegant way than rasterization, for a broad range of scenes. Ideally, that includes rapid moving light sources, and specular / glossy surfaces, for which view-independent caching does not work.

I like too it! :D I have single GTX 480 and I want to interactive this demo (caustics included). I respect that please you put download this demo. but I don't worry that I will get slow. :)

@RayTracey


Since you are achieving 50+ fps in some scenarios, have you considered moving from a constant number of samples per frame, to a constant frame rate with a varying number of samples? It could boost the quality when you are already hitting interactive frame rates (~30 fps).

Would something like this be a part of your noise reducing optimization, i.e. sample for 33 ms and then start the next frame?

Anonymous (post 6): you can change the resolution at the top of the main file, look for int2 screenresolution and renderresolution. The debug info can be toggled by setting ShowHUD to true.





FreDre: I would love to test Kepler, but I just got 2 brand new GTX 580 GPUs last month. Nvidia may always send me a Kepler card though ;)

Anonymous (post 10): as Jacco said, scenes with highly specular and glossy surfaces need to be updated every frame. I'll show that in another video. There are of course scene specific optimizations possible.

nuninho: I won't release any executables right now, it might be playable from the cloud at some point though ;-)

anonymous: that's actually a good idea and something that could be implemented. The optimizations I have in mind are more low-level though (Sobol sampling is one of them)

I would love to test Kepler too, but GK104 is not the high end GPU, GK110 is with 2,304 Cuda Core and 3-6 GB VRAM, release date August/September...

Frostbite 2 engine in Battlefield 3 has realtime gi too (geomerics tech):

http://planetbattlefield.gamespy.com/screenshots/?ss=2023&page=5

Anonymous: I admit that Battlefield 3 looks great and I'm very glad that game developers are finally looking at real-time GI methods (Battlefield 3 has Geomeric's instant radiosity and CryEngine3 has cascaded light propagation volumes), but - if I'm not mistaken - Geomeric's solution requires precomputed light probes (like the ones in the screenshot you've posted) to light dynamic objects/characters, while Brigade doesn't require any precomputation and computes the lighting on dynamic objects in real-time with the same superb quality as their environments (no interpolation). Moreover, AFAIK Frostbite2 doesn't support perfectly specular (mirror-like) reflections on arbitrary surfaces, which are a piece of cake for Brigade. I'll show more diverse materials (mirrors, glass and glossy) in an upcoming video.

I agree that this path tracing can generate very realistic rendering. And as a nice side effect it is relatively easy to code this. The only down is that it is extremely brute force. With all this random ray tracing it is even strange that it works that well, as it is far away of how GPUs are supposed to be used.

If GPUs were 100-1000 times more powerfull (or build with this kind of rendering in mind) it would be the way to go. As long a this is not the case, a lot of hard work and clever thinking will be required to achieve similar quality.

I couldn't agree more with you. The beauty is that this tech already runs great even if it's very brute force.



Imagine when all sorts of clever optimizations will be implemented :-D.

We're actually very close to having high framerate, high resolution, real-time path traced graphics for games.

Cool, how about a Anisotropic material?:


http://www.youtube.com/watch?v=bKDzB2IUAXk

Anisotropic is not supported yet, the materials are still being worked on.

Hi to all!

Is it possible to reduce the noise by compressing on the fly the each frame ? (for example you have

frame with resolution 1280x720 but in the preview images

of your test in this page are with 400x234 - compressed in 3 times - without any noise and smooth.)

If Brigade can do frame 3840x2160 and compress it to 1280x720 - we have no noise

I hope you'll realize what I have asked )) .. P.s. sorry for my poor English ...

I think you mean downscaling right? That wouldn't be a good solution, because the rendertime increases linearly with the resolution. There are much better and computationally cheaper options to reduce the noise in indirectly lit regions.

Post a Comment