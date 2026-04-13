---
title: 'CentiLeo: a brand new interactive out-of-core CUDA path tracer for massive
  models'
url: http://raytracey.blogspot.com/2011/04/centileo-brand-new-interactive-out-of.html
author: Sam Lapere
published: '2011-04-12'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[http://www.youtube.com/watch?v=mxx9dyPO0js](http://www.youtube.com/watch?v=mxx9dyPO0js)

Some screengrabs of the video with more info:

![](../../assets/ee367bd30a3facd7.jpg)


![](../../assets/ee367bd30a3facd7.jpg)

![](../../assets/381efa4741b6309a.jpg)


![](../../assets/381efa4741b6309a.jpg)

![](../../assets/0f1b532b7941391b.jpg)


![](../../assets/0f1b532b7941391b.jpg)

![](../../assets/38f0c68eb32f3d7b.jpg)


![](../../assets/38f0c68eb32f3d7b.jpg)

![](../../assets/82de6527bfbfe9f4.jpg)


![](../../assets/82de6527bfbfe9f4.jpg)

![](../../assets/b6974b943b418d3b.jpg)


![](../../assets/b6974b943b418d3b.jpg)

![](../../assets/8124cc627741f0ef.jpg)


![](../../assets/8124cc627741f0ef.jpg)

![](../../assets/50721171f1528db5.jpg)


![](../../assets/50721171f1528db5.jpg)

"the target is CUDA implementation because it is fast and flexible enough. BDPT, MLT, tesselation, displacement mapping, hair/fur, texture filtering - sure, will be CUDA-based.Programmable materials can be done in CUDA. But an additional idea would be to port some existing CPU/C++ material shaders to work with our GPU compute building blocks. Voxels are not yet planned. But they can be potentially implemented.

Our goal is to finish the TODO feature list by September 2011. The concepts are pretty simple, but all the devil is in details. The future work is engineering. Almost all research was already done.

The website will be created this or next week. This demo shows what we can do now."

![](../../assets/d0857e73633a1e20.jpg)


![](../../assets/d0857e73633a1e20.jpg)

![](../../assets/9e6185792109fdfa.jpg)


![](../../assets/9e6185792109fdfa.jpg)

## 9 comments:

Bad russians, bad-bad russians...

??? I know it's made by a Russian developer, but what does that have to do with it? Unless of course the KGB is involved somehow, stealing Boeing 777 blueprints while pretending to make a GPU path tracer ;)

Damn, that's a pretty awesome demo. Didn't know a GTX480 was capable of this.

They promise a lot of cool features. And the one, they published, is very promising!


Bichugan

Indeed! I'm very curious to see how they're going to handle raytraced displacement mapping on the GPU. Could be something like in "Micropolygon Ray Tracing With Defocus and Motion Blur" (http://www.kunzhou.net/2010/mptracing.pdf).

apparently programming the MLT algorithms is a total bitch to implement in GPU ray tracey, it slows the speed down and such.

@Anonymous: implementing MLT on GPU doesn't have to be a total bitch per se, look at what Dietger van Antwerpen did (search for "Kelemen-style Metropolis Light Transport on the GPU" on Youtube) or more recently Dade from the Luxrender team with MLT implemented in PathGPU. It's certainly not impossible, and I'm sure that it will appear in other GPU renderers soon.

Even what they have done is a bitch, but this bitch works great

Yup, it does work great and it looks fantastic.

Post a Comment