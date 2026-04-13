---
title: V-Ray GPU news
url: http://raytracey.blogspot.com/2010/05/v-ray-gpu-news.html
author: Sam Lapere
published: '2010-05-20'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Yesterday a new video of V-Ray's GPU renderer surfaced on the net:


The rendering speed and interactivity look phenomenal, but then again it's being rendered on 3 GTX480's so no real surprise there. It's also using OpenCL and Chaos Group is the first to deliver a working commercial GPU renderer that is not CUDA-only (LuxRender's smallLuxGPU was actually first with OpenCL but is open source).


Chaos Group started the whole GPU rendering revolution 9 months ago at Siggraph 2009 (mental images probably had a working implementation first with iray, but it was not shown in public until GTC 2009). Not only did they prove that path traced rendering with high-quality global illumination was possible on GPUs, but also that the GPU was an order of magnitude faster at this kind of rendering than the CPU. Both of these amazing feats were utterly unbelievable just 10 months ago for every one but the lucky few at Nvidia, Chaos Group and mental images.


The V-Ray GPU presentation on a simple affordable PC (quad core i7 with gtx285) has inspired many other developers to start working on a GPU renderer (in contrast to iray's GTC demonstration on a uber render server consisting of 15 Teslas). If it wasn't for Chaos Group, most people probably still wouldn't have the ability to render on the GPU or even know that it was actually possible.

[http://www.spot3d.com/vray/images/rt_movies/20100514_VRayRTGPU.wmv](http://www.spot3d.com/vray/images/rt_movies/20100514_VRayRTGPU.wmv)The rendering speed and interactivity look phenomenal, but then again it's being rendered on 3 GTX480's so no real surprise there. It's also using OpenCL and Chaos Group is the first to deliver a working commercial GPU renderer that is not CUDA-only (LuxRender's smallLuxGPU was actually first with OpenCL but is open source).

Chaos Group started the whole GPU rendering revolution 9 months ago at Siggraph 2009 (mental images probably had a working implementation first with iray, but it was not shown in public until GTC 2009). Not only did they prove that path traced rendering with high-quality global illumination was possible on GPUs, but also that the GPU was an order of magnitude faster at this kind of rendering than the CPU. Both of these amazing feats were utterly unbelievable just 10 months ago for every one but the lucky few at Nvidia, Chaos Group and mental images.

The V-Ray GPU presentation on a simple affordable PC (quad core i7 with gtx285) has inspired many other developers to start working on a GPU renderer (in contrast to iray's GTC demonstration on a uber render server consisting of 15 Teslas). If it wasn't for Chaos Group, most people probably still wouldn't have the ability to render on the GPU or even know that it was actually possible.

## No comments:

Post a Comment