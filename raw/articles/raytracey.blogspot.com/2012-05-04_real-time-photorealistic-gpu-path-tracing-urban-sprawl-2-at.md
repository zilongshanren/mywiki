---
title: 'Real-time photorealistic GPU path tracing: Urban Sprawl 2 at double speed!'
url: http://raytracey.blogspot.com/2012/05/real-time-photorealistic-gpu-path_04.html
author: Sam Lapere
published: '2012-05-04'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[As requested by a reader of this blog](http://raytracey.blogspot.com/2012/05/real-time-photorealistic-gpu-path.html?showComment=1336122398912#c1219792509321533222), I've tested the performance of the most recent Brigade code in the Urban Sprawl 2 scene with the same camera viewpoint as in the screenshot from the

[previous post](http://raytracey.blogspot.com/2012/05/real-time-photorealistic-gpu-path.html). As of yesterday, Brigade is now

__twice__as fast when converging (at no extra cost), thanks to moving a critical part of the rendering code to the GPU.

Short video of Urban Sprawl 2, rendered in real-time on 2 GTX 580 GPUs

__at 1280x720 resolution__**(highly recommended to watch in 720p)**:(Youtube seems to have messed up again by auto-correcting the contrast and color saturation, I'm trying to fix that.)

## 23 comments:

Are the wrong colors only in the Youtube? Because we did some experiments with gamma / exposure over the past weeks.


You mentioned moving code to the GPU. Did you move your own frame averaging code?

- Jacco.

Yes, I've compared my captured video and the Youtube one and while the colors are now quite vibrant in Brigade (a bit too much), Youtube messed up the contrast, e.g. at 0:25 the car is totally obscured in the Youtube video, while it isn't in the original.


The frame averaging runs in OpenGL and it's totally free.

@Sam



Another great video!

Previously you may have mentioned toning down the frame averaging during camera rotations; however, I think there may be a better, simple solution for improved frame averaging. If you are rendering a 1280x720 image with a 60 degree FOV and the camera rotates to the right 5 degrees for the next frame, then when applying the average, the previous frame should be shifted left (5/60)*1280 = 106.6 pixels, so it is more likely to line up with the new frame. This would leave some edge pixels un-averaged, but I think it would greatly improve the ghosting AND the quality of the averaging. It should be pretty easy to do.

try http://vimeo.com

save uncorrected video

You have lastest your projects/demos but on youtube only!?! Always videos! Unfortunately no executable demos yet... :S I want much executable its. :(

Anonymous: sounds a bit like temporal reprojection, I might like into that soon.


nuninho: there won't be any downloadable executables (you'd need a very powerful system + the 3d scenes are protected), but there might be something else soon ;)

So, Brigade is not 2 but 2.6 (1.3 * 2) times as fast :). Nice!!

Exactly :)

Wait a minute, that's only under very specific circumstances. Even the 30% is only 'semi-real', as it was essentially a bug fix. We did quite some work in terms of overhead reduction, but the path tracer itself didn't really get that much faster. There will be some developments later on, but not at the break-neck speed people seem to expect now. :) - J.

Any guess as to why youtube allows some videos to be played at various speeds (.5x,1.5x,2x,..) but other videos can't? Videos like this that are ~10fps would be perfect for 2x playback. I couldn't find an answer through google.

Jacco: the path tracer is indeed not that much faster when the camera or objects are moving (only about 25-30%), but when the image is left to converge, samples are now accumulated twice as fast as before, which makes it extremely useful for real-time walkthroughs of static scenes with dynamic day/night cycle (e.g. archviz or urban planning).


Anonymous: I have no idea why the 2x playback speed button is present with previous videos, but not on this one

awesome stuff!



tech question: i was recently playing around with octane and it has this (somewhat disappointing) limitation of "Maximum number of 32bpp RGBA Textures Reached", which is a pain for large urban environments. they argue it is a cuda limitation. how does brigade handle this? by async texture streaming in the background or something similar?

thanks.

@anonymous: Brigade probably has even more limitations; it's an engine that targets games. Octane is more generic. - J.

Brigade also has a hard limit on the number of textures (no streaming yet). I'm not sure it's a memory problem, could be CUDA related though.

Excellent work so far, but I'm curious how Brigade means to extend to more complex BRDFs, unless I'm missing something I have only seen Diffuse, Specular and Glossy (non-fresnel'd specular over diffuse). I would really like to see how the engine handles something like CookTorrence or a Fresnel'd BlinnPhong ...

colin: Brigade differs from other GPU path tracers in that it's main goal is true real-time rendering, there's no need to be as feature rich or complete in materials as for example Octane. Also, Brigade's current material system is already more than sufficient to create scenes with much higher visual fidelity than what you see in today's games. This doesn't mean however that additional materials won't be implemented in the (near) future.

I also forgot to mention that Brigade can do Blinn as well, which I haven't shown yet.

That's a fair point however I would contest that if fresnel were to be added it would greatly enhance the look of all of the materials that specularly reflect (glass, car paint etc) and make Brigade look even more impressive.

Alright, I'll pass it on to the developers, thanks.

fresnel would make it look better indeed, using it tastefully of course :). I noticed with normal maps add the scene "pop" out more too. Hopefully they can support alpha channel(for leaves and such) in the near future.


Idea for Sam, since youtube screw up the video you upload, maybe you can upload a uncompress AVI file to mediafire, to keep the file size small, make it a 10 second video. This will give everyone a true impression of Brigade rendering capabilities.

BTW Sam, what software do you use to capture the videos?

I'm using FRAPS

Post a Comment