---
title: 'Unbiased Truck Soccer: Sunny sky with only a few traces of rayn!'
url: http://raytracey.blogspot.com/2011/03/unbiased-truck-soccer-sunny-sky-with.html
author: Sam Lapere
published: '2011-03-28'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Another test in the quest for faster convergence speed, this time using a skydome and sun.


![](../../assets/e792521abc1194d1.jpg)


![](../../assets/e792521abc1194d1.jpg)

![](../../assets/0c65bf18261440fa.jpg)


![](../../assets/0c65bf18261440fa.jpg)

One of the advantages of using a skydome to light the scene is that the difference between 2 and 3 bounces of indirect light is not as large as when using an area light:


max path length 1 (zero bounces)


max path length 1 (zero bounces)

![](../../assets/32896f5552ebb73f.jpg)


![](../../assets/32896f5552ebb73f.jpg)

max path length 2 (1 bounce)

![](../../assets/484c101fae896aa7.jpg)


![](../../assets/484c101fae896aa7.jpg)

2 bounces

![](../../assets/14ddfd0e11497a05.jpg)


![](../../assets/14ddfd0e11497a05.jpg)

3 bounces

![](../../assets/eab44602444061b3.jpg)


![](../../assets/eab44602444061b3.jpg)

Another advantage is the very fast convergence speed compared to using area lights due to the fact that almost every pixel can 'see' the skydome. Only the pixels that are occluded from the skydome (e.g. the ground patch under the car) clean up slower because they are indirectly lit. Using bidirectional path tracing would greatly increase the convergence speed of these pixels (edit: as pointed out by Iliyan in the comments, bidir path tracing would actually perform worse in this outdoor scene where standard path tracing shines).


An overcast sky can be simulated by using only the skydome for lighting (without an emitting sun sphere):



An overcast sky can be simulated by using only the skydome for lighting (without an emitting sun sphere):

![](../../assets/c150c1e41f353a16.jpg)


![](../../assets/c150c1e41f353a16.jpg)

![](../../assets/5edbcbbecc4b3237.jpg)


![](../../assets/5edbcbbecc4b3237.jpg)

In this case, the noise clears up very fast with just a few samples. This lighting setup will be used for the Unbiased Truck Soccer game.


Download the executable for this sky test at


To brighten/darken the sun, select the sun sphere by right-clicking it, click the 'emi' button on the top right of the screen and change the values at the bottom of the screen to e.g. 10, 10, 5. Overbrightening the sun will cause the shadows to look sharper and more pronounced, but will also increase the noise to unacceptable levels:


Download the executable for this sky test at

[http://code.google.com/p/tokap-the-once-known-as-pong/downloads/list](http://code.google.com/p/tokap-the-once-known-as-pong/downloads/list)(package updated with glass sphere for some nice caustics)To brighten/darken the sun, select the sun sphere by right-clicking it, click the 'emi' button on the top right of the screen and change the values at the bottom of the screen to e.g. 10, 10, 5. Overbrightening the sun will cause the shadows to look sharper and more pronounced, but will also increase the noise to unacceptable levels:

![](../../assets/da96f77966a096a2.jpg)


![](../../assets/da96f77966a096a2.jpg)

## 4 comments:

Nice images :) However, I think bidirectional path tracing will perform even worse than unidirectional on this scene. Such scenes are in fact the best case for classic path tracing.

Thanks! :-)



Thanks for the suggestion. Now that I think of it, this kind of open outdoor scenes does indeed work best with standard path tracing and bidirectional pt should be reserved for scenes with lots of indirect lighting.

I'll update my post :)

Actually, if you look at all the "real-time global illumination" renderers that are constantly popping up like mushrooms, they are all unidirectional path tracers and are always advertised on well-lit open scenes, ambient occlusion - all cases where the illumination "depth complexity" is very low :)

Yep, you're right. I do think that once bidirectional path tracing will become available in GPU path tracers, scenes with more complex lighting will converge almost as fast as well-lit, open scenes do now with unidirectional pt.







The ones that I know of:

- Dietger van Antwerpen made it work with the Brigade path tracer (and extended it to MLT),

- Simon Brown has developed some kind of hybrid between uni- and bidirectional path tracing in CUDA, called "two-way path tracing", http://www.sjbrown.co.uk/2011/01/03/two-way-path-tracing/. This approach might be very interesting because according to the author, it renders more efficiently on the GPU than pure bidir path tracing.

- Jan Novak has GPU bdpt working with path regeneration (CUDA as well), http://cg.ibds.kit.edu/novak/index.php

- Kaikai Wang also has a hybrid uni- and bidirectional path tracer working in CUDA: http://kaikaiwang.blogspot.com/2010/11/live-scene-editing-path-tracing-support.html)

I might make a new post on that actually :)

Post a Comment