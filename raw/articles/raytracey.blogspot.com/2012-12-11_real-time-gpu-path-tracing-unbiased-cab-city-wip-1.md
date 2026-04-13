---
title: 'Real-time GPU path tracing: Unbiased Cab City WIP 1'
url: http://raytracey.blogspot.com/2012/12/real-time-gpu-path-tracing-unbiased-cab.html
author: Sam Lapere
published: '2012-12-11'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Found some time to do another quick instancing test with OTOY's Brigade engine:

- 1024 dynamic instances of a car (materials can be customized per instance, not shown yet)

- car model contains about 23k triangles

- 400k triangle city scene (can be instanced tens of times without performance loss)

It's now also possible to have a complete city with hundreds of instanced city blocks containing thousands of (instanced) animated characters and cars, essentially a real-time path traced photorealistic GTA. It's mighty impressive. But that's for another video :)


UPDATE: Yes! Ich bin mit diesen Demo auf die grossen Deutschen website PC Games Hardware erschenen, das ist ja ganz toll! :D :

UPDATE: Yes! Ich bin mit diesen Demo auf die grossen Deutschen website PC Games Hardware erschenen, das ist ja ganz toll! :D :

## 5 comments:

Somehow the perfect reflections on the windows and the street always freak me out. I assume that they're simply that way because it's not a priority to make the materials, and the mesh data for what's behind them.


Or is it something else?

2 little things.



1) could you make the videos without the blurring, but stuttery instead? that kind of blurring makes me sick, stuttering would be less cool, but more "what we're used to"

2) blurring when only rotating the camera. on rotation, one could simply turn the existing image as a screen-quad around, and not require (much) samples there again. only focus on the edge that shows new stuff, then. that could make lookarounds much nicer and much faster (or simply when standing still begin to render a full cubemap around the head).

my little critic and suggestion on an absolutely stunning product.

RC-1290: you are right, this was a very quick test to show off massive dynamic instancing, I didn't really bother tweaking the materials. I should have made the car windows look like glass. Next time :)


davepermen: thanks, but the method you describe (recalculating only an edge of the screen when rotating) works only in perfectly static scenes and breaks in scenes with thousands of dynamic objects. Butwe're actually working on several techniques that will make the need for blurring obsolete.

Wonderful,, btw, i need some help, i send an email to you.. Thanks.


Farid,

Post a Comment