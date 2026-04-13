---
title: Chaos Group (V-Ray) announces real-time path tracer Lavina (+ Nvidia's really
  real-time path traced global illumination)
url: http://raytracey.blogspot.com/2018/08/chaos-group-v-ray-announces-real-time.html
author: Sam Lapere
published: '2018-08-28'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

(See update at the bottom of this post to see something even more mindblowing)


The Chaos Group blog features quite an interesting article about the speed increase which can be expected by using Nvidia's recently announced RTX cards:

The Chaos Group blog features quite an interesting article about the speed increase which can be expected by using Nvidia's recently announced RTX cards:

[https://www.chaosgroup.com/blog/what-does-the-new-nvidia-rtx-hardware-mean-for-ray-tracing-gpu-rendering-v-ray](https://www.chaosgroup.com/blog/what-does-the-new-nvidia-rtx-hardware-mean-for-ray-tracing-gpu-rendering-v-ray)

Excerpt:

"Specialized hardware for ray casting has been attempted in the past, but has been largely unsuccessful — partly because the shading and ray casting calculations are usually closely related and having them run on completely different hardware devices is not efficient. Having both processes running inside the same GPU is what makes the RTX architecture interesting. We expect that in the coming years the RTX series of GPUs will have a large impact on rendering and will firmly establish GPU ray tracing as a technique for producing computer generated images both for off-line and real-time rendering."

The article features a new research project, called Lavina, which is essentially doing real-time ray tracing and path tracing (with reflections, refractions and one GI bounce). The video below gets seriously impressive towards the end:

Chaos Group have always been a frontrunner in real-time photorealistic ray tracing research on GPUs, even as far back as Siggraph 2009 where they showed off the first version of V-Ray RT GPU rendering on CUDA (see

[http://raytracey.blogspot.com/2009/08/race-for-real-time-ray-tracing.html](http://raytracey.blogspot.com/2009/08/race-for-real-time-ray-tracing.html)or[https://www.youtube.com/watch?v=DJLCpS107jg](https://www.youtube.com/watch?v=DJLCpS107jg)).
I have to admit that I'm both stoked, but also a bit jealous when I see what Chaos Group has achieved with project Lavina, as it is exactly what I hoped Brigade would turn into one day (Brigade was a premature

[real-time path tracing engine developed by Jacco Bikker in 2010](https://raytracey.blogspot.com/2010/04/real-time-pathtracing-demo-shows-future.html), which I experimented with and blogged about quite extensively, see e.g.[http://raytracey.blogspot.com/2012/09/real-time-path-tracing-racing-game.html](http://raytracey.blogspot.com/2012/09/real-time-path-tracing-racing-game.html)).
Then again, thanks to noob-friendly ray tracing API's like Nvidia's RTX and Optix, soon everyone's grandmother and their dog will be able to write a real-time path tracer, so all is well in the end.






This is just mindblowing stuff. Can't wait to get my hands on it. This probably deserves its own blogpost.

**UPDATE**: this talk by Nvidia researcher Jacopo Pantaleoni (famous from[VoxelPipe and Weta's Pantaray](http://raytracey.blogspot.com/2011/07/voxelpipe-paper-and-preview-of-real.html)engine) "Real-time ray tracing for real-time gloabl illumination" totally trounces the Lavina project, both in quality and in terms of dynamic scenes:[http://on-demand.gputechconf.com/siggraph/2018/video/sig1813-4-jacopo-pantalenoni-real-time-global-illumination.html](http://on-demand.gputechconf.com/siggraph/2018/video/sig1813-4-jacopo-pantalenoni-real-time-global-illumination.html)This is just mindblowing stuff. Can't wait to get my hands on it. This probably deserves its own blogpost.

## No comments:

Post a Comment