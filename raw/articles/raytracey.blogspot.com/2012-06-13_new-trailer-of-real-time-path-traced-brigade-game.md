---
title: New trailer of real-time path traced Brigade game
url: http://raytracey.blogspot.com/2012/06/new-trailer-of-real-time-path-traced_13.html
author: Sam Lapere
published: '2012-06-13'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Quasi-random, more or less unbiased blog about real-time photorealistic GPU rendering

Wednesday, June 13, 2012

New trailer of real-time path traced Brigade game

There's a new trailer of "It's about time", a real-time path traced game running on Brigade, created by a team of eight IGAD students (International Game Architecture and Design) from the NHTV, the Netherlands:

mental ray is not unbiased, it uses irradiance caching, so from a quality standpoint, Brigade would be superior. Not that I have anything against biased renderers (pre-emptive damage control :)

>> To be honest, I prefer the Unreal Engine 4 demo.

The fact that you're comparing this video with Unreal Engine 4 is a fantastic compliment to Brigade :)

>> Everything that makes unbiased rendering superior visually to rasterization is lacking in this demo :\

That's a good point. Actually there are some things in this video that a rasterizer can't do or at least not with the same quality, e.g. the red light emitting sphere, real-time reflections on the water surface, the glossy reflecting parts in the skull, real 3D depth of field, color bleeding and diffuse interreflection. All these effects are in the video, but they're still a bit noisy.

The Unreal Engine Demo is the result of millions of dollars of influence, and this was put together by a handful of students. That it was demonstrated that a playable game is possible is the most impressive aspect (IMO).

Given the challenge of rendering the UE4 demo (assuming similar post processing, et. al.), I think Brigade would wipe the floor with it in fidelity -- albeit with an ample amount of noise. :p

I'm trying to get a feel for the quality of AO in Octane to get a feel for what Brigade will be capable of doing. Do you know of any good screen shots that show this off?

hmm... why is ambient occlusion being singled out here? Isn't that solved in the encompassing unbiased rendering equation? E.G. - one unbiased renderer has the same fidelity has any other unbiased renderer?

I also want to make clear that Brigade is not going to mimic Octane, both renderers are based on path tracing and strive for the highest possible quality and speed, but each is optimized for their own field of application.

Anonymous: ambient occlusion is indeed solved inherently by unbiased path tracing and is not physically correct. It's an approximation to real GI, which works very well in certain scenes and is much faster to compute. Having the option to render with raytraced AO or path tracing (and everything in between) in Brigade lets us choose the best quality and speed for each scene.

I'm really happy with the fxguide article. It's awesome to see Octane and Brigade - which are both still very young GPU renderers - in such an in-depth article amongst the big, established production renderers like Arnold and Renderman.

Hybrid rendering is probably not worth the hassle, because primary rays (which could as well be rasterized because they're coherent) are just a tiny fraction of all rays in path tracing. It would also cause some effects to break and introduces additional aliasing.

## 17 comments:

Very promising. What features does that lack in comparison with photorealistic renderers like mental ray?

Also, how big is the potential for optimization?

mental ray is not unbiased, it uses irradiance caching, so from a quality standpoint, Brigade would be superior. Not that I have anything against biased renderers (pre-emptive damage control :)

the potential for optimization is huge.

To be honest, I prefer the Unreal Engine 4 demo.

Everything that makes unbiased rendering superior visually to rasterization is lacking in this demo :\

>> To be honest, I prefer the Unreal Engine 4 demo.





The fact that you're comparing this video with Unreal Engine 4 is a fantastic compliment to Brigade :)

>> Everything that makes unbiased rendering superior visually to rasterization is lacking in this demo :\

That's a good point. Actually there are some things in this video that a rasterizer can't do or at least not with the same quality, e.g. the red light emitting sphere, real-time reflections on the water surface, the glossy reflecting parts in the skull, real 3D depth of field, color bleeding and diffuse interreflection. All these effects are in the video, but they're still a bit noisy.

The Unreal Engine Demo is the result of millions of dollars of influence, and this was put together by a handful of students. That it was demonstrated that a playable game is



possibleis the most impressive aspect (IMO).Given the challenge of rendering the UE4 demo (assuming similar post processing, et. al.), I think Brigade would wipe the floor with it in fidelity -- albeit with an ample amount of noise. :p

And things are only going to get better.

Exactly :)

Hey Sam,


I'm trying to get a feel for the quality of AO in Octane to get a feel for what Brigade will be capable of doing. Do you know of any good screen shots that show this off?

hmm... why is ambient occlusion being singled out here? Isn't that solved in the encompassing unbiased rendering equation? E.G. - one unbiased renderer has the same fidelity has any other unbiased renderer?

Sean, this was made with a very early version of Octane (2010) with AO:



http://ww.w.refractivesoftware.com/forum/download/file.php?id=2006&sid=7777155485a90d3b066afe8453a0c103&mode=view

I also want to make clear that Brigade is not going to mimic Octane, both renderers are based on path tracing and strive for the highest possible quality and speed, but each is optimized for their own field of application.

Anonymous: ambient occlusion is indeed solved inherently by unbiased path tracing and is not physically correct. It's an approximation to real GI, which works very well in certain scenes and is much faster to compute. Having the option to render with raytraced AO or path tracing (and everything in between) in Brigade lets us choose the best quality and speed for each scene.

This is awesome Sam! And of course, re: different implementations. :)



My last 2 posts didn't go through, so this may seem a little off topic:

You've been mentioned in an article!

http://www.fxguide.com/featured/the-art-of-rendering/

* at the end

Thanks Sean.


I'm really happy with the fxguide article. It's awesome to see Octane and Brigade - which are both still very young GPU renderers - in such an in-depth article amongst the big, established production renderers like Arnold and Renderman.

Does / will it use something like this:



First render the scene using rasterization. Then combine the noisy raytracer result with the rasterizer result.

I know very little about raytracing so this may be a stupid question :)

Hybrid rendering is probably not worth the hassle, because primary rays (which could as well be rasterized because they're coherent) are just a tiny fraction of all rays in path tracing. It would also cause some effects to break and introduces additional aliasing.

Post a Comment