---
title: Doom 3 path traced with OptiX
url: http://raytracey.blogspot.com/2011/02/doom-3-path-traced-with-optix.html
author: Sam Lapere
published: '2011-02-28'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[http://developer.nvidia.com/forums/index.php?showtopic=5892](http://developer.nvidia.com/forums/index.php?showtopic=5892)

Seems like a nice idea, but currently it's far from real-time and it doesn't look very spectacular. Imo, it should use the Brigade path tracer for better performance and quality.

UPDATE: the guys working on this have posted a new screenshot, showing much improved global illumination by using Russian roulette:

Everything looks much brighter now and actually starts to have that path traced look. Unfortunetly textures and geometry are pretty low resolution. And it's still way too slow for real-time (30 minutes for this 2048x2048 image on GTX480 + Tesla C2050).

## 2 comments:

Hmm, that looks really weird for path tracing. I don't really see any of the "GI-ish" look :/

I agree. The first screenshots don't seem to have GI in them, but the last one (that I posted in the update) definitely looks much better and lit with GI.

Post a Comment