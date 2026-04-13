---
title: 'Sci-fi interior WIP 2: video'
url: http://raytracey.blogspot.com/2012/05/sci-fi-interior-wip-2-video.html
author: Sam Lapere
published: '2012-05-21'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I really love playing around with this thing, the graphics are so utterly insane. I'm not easily impressed, but every time I fire up Brigade, my jaw falls to the floor. You can't believe how many times I had to visit a maxillofacial surgeon for that. But it's worth it.

## 11 comments:

as before nice but really noisy.

realtime is maybe the wrong term here. you have realtime updates but it takes around 4s until details show up and the quality is anyhow acceptable. so to get 20fps a factor around 80x is still missing.

Agreed. The videos, although entirely amazing, do exhibit the work left to be done. Huge steps are being made, but the hardest will probably be those final steps that take it from 0.25 FPS to 30 FPS. A frame being an actual acceptably converged frame, not just a fragment of one. Only then would the word realtime be used in a meaningful context.

Well, this interior scene was actually a stress test for Brigade. It's already running at very acceptable quality at 30 fps. Outdoor scenes render with 4x less noise at 30 fps, and Brigade is getting faster every day.



Keep in mind that Brigade is still a very brute-force path tracer. When all the optimizations on our to do list will be implemented, it will be orders of magnitude faster.

And if you factor in the rendering power of the cloud, this will be completely noisefree at 60 fps/1080p :)

I don't know about those first two, but I'm already very impressed. But please keep at it Sam! as 4seconds is really too long for me to wait! ;)


Nicholas

Which are the differences between this engine and other "real time" path tracer? I can't get it.



You speak about real time but it isn't. And those shaders are so simple, what about sss, caustics and fur.

Cheers

Don't get me wrong, as I said before this is completely impressive and exciting. And of course it will get better. Just pointing out the loose use of the term "realtime" because although technically it might be casting rays and updating in realtime, we aren't actually seeing 30 frames per second. We're seeing 30 updates per second, with an acceptable converged frame after 2+ seconds which would be an effective <0.5 fps in my book.

Both sss and fur had not shown up in computer graphics for 20-25 years from the first publicly available tools like 3dstudio DOS. No one has expectations of the tools presented here to do better.






(Although it probably will).

Technology such as Brigade and what is has to offer have a definite place in computer graphics and is a welcomed technology. All Technology have development/embryonic stages, and go through many cycles of design, Brigade is walking that beat.

All technology have different and multiple purposes, one of those is being tried out with Brigade.

As for the definition of Real-Time, all I can say is this:

Never judge incomplete work until it's done (loosely quoting someone famous).

Nicholas

Also it will be interesting to see how a dynamic particle engine would find its way through the path tracer.

Anonymous: As I've said in my previous post, we're just scratching the surface with Brigade. The awesome part is that even in its current brute force state, it already runs with stellar performance and well above our own expectations. I mean, the fact that we can do Monte Carlo path tracing in real-time is still boggling my mind every day. I never thought we could do this one year ago, when I was making real-time path tracing demos with only spheres and boxes. With all the ideas and experience we have now, I'm convinced that in six months time we'll be able to render very demanding scenes truly in real-time. Just wait ;)

100x more processing power might seem a lot but it is actually 5 to 7 years from now. This is really exciting even without taking into account the software breakthroughs.

You won't have to wait that long. 5 to 7 months from now is more likely.

Post a Comment