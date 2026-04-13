---
title: Sunny real-time path traced Sponza!
url: http://raytracey.blogspot.com/2012/03/sunny-real-time-path-traced-sponza.html
author: Sam Lapere
published: '2012-03-15'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Another real-time Brigade test with the sun on Sponza, a more challenging scene with lots of areas with indirect lighting.

Video (32 spp per frame):

The toad was modeled by Son Kim. The video is pretty dark in some areas, so to see all the details, I advise to watch it without too much environment light.

This scene is the gold standard to test how well a newly developed GI algorithm handles indirect lighting scenarios. With Brigade it is possible to render this scene at photorealistic quality in real-time on just two GTX580 GPUs (one Kepler GPU should easily surpass surpass this).

Beautiful diffuse colour bleeding on the toad:

I've decided to work on a real game-like outdoor city scene, something like the open world city in Assassin's Creed, but with photoreal quality real-time path traced global illumination. I'm currently working on an ancient city scene (400k triangles, model from SketchUp). Expect a video with this model soon, showing dynamic sunlight and real-time updated GI (it renders effortlessly at 10-20 fps).

## 5 comments:

Simply amazing.


Five years ago if you told me you'd be path tracing hundreds of thousands of polygons in realtime within the near future I would have looked at you funny and walked away.

yay, seeing my model in Brigade is inspiring! I'm working on some new stuff(environments) specifically for Brigade.


-SK

Anonymous: that's the reaction I got from almost everyone that I spoke to about path tracing, so I just gave up and started coding to prove it :-)


Son Kim: cool, keep me updated on your progress

Btw, can you light up one moment: any plans about "Brigade Free SDK" (like "UDK" or "Cryengine3 Free SDK") - e.g. public avalible toolset, that can be used for commercy (with 20-30% royality to toolset owners) and so on?

Lex4art, I can't say for sure at this point, the details for Brigade licensing have yet to be determined.

Post a Comment