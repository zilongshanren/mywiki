---
title: 'Real-time Metropolis Light Transport on the GPU: it works!!!!'
url: http://raytracey.blogspot.com/2010/12/real-time-metropolis-light-transport-on.html
author: Sam Lapere
published: '2010-12-15'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

This is probably the most significant news since the introduction of real-time path tracing on the GPU. I've been wondering for quite a while if MLT (Metropolis Light Transport) would be able to run on current GPU architectures. MLT is a more efficient and more complex algorithm than path tracing for rendering certain scenes which are predominantly indirectly lit (e.g. light coming through a narrow opening, such as a half-closed door, and illuminating a room), a case in which path tracing has much difficulty to find "important" contributing light paths. For this reason, it is the rendering method of choice for professional unbiased renderers like Maxwell Render, Fryrender, Luxrender, Indigo Render and Kerkythea Render.

Dietger van Antwerpen, an IGAD student who co-developed the Brigade path tracer and who also managed to make ERPT (energy distribution ray tracing) run in real-time on a Fermi GPU, has posted two utterly stunning and quite unbelievable videos of his latest progress:

-

[video 1 showing a comparison between real-time ERPT and path tracing on the GPU](http://www.youtube.com/watch?v=c7wTaW46gzA):

![](../../assets/419f2d7f88cf5d71.png)


![](../../assets/419f2d7f88cf5d71.png)

ERPT on the left, standard path tracing (PT) on the right. Light is coming in from a narrow opening, a scenario in which PT has a hard time to find light paths and converge, because it randomly samples the environment. ERPT shares properties with MLT: once it finds an important light path, it will sample nearby paths via small mutations of the found light path, so convergence is much faster.

-

[video 2 showing Kelemen-style MLT (an improvement on the original MLT algorithm) running in real-time on the GPU](http://www.youtube.com/watch?v=70uNjjplYzA). The video description mentions Kelemen-style MLT on top of bidirectional path tracing (BDPT) with multiple importance sampling, pretty amazing.

![](../../assets/790955aeb1f385c8.png)


![](../../assets/790955aeb1f385c8.png)

Kelemen-MLT after 10 seconds of rendering at 1280x720 on a single GTX 470. The beautiful caustics are possible due to bidirectional path tracing+MLT and are much more difficult to obtain with standard path tracing.

These videos are ultimate proof that current GPUs are capable of more complex rendering algorithms than brute-force standard path tracing and can potentially accelerate the very same algorithms used in the major unbiased CPU renderers. This bodes very well for GPU renderers like Octane (which has its own MLT-like algorithm), V-Ray RT GPU, SmallLuxGPU and iray.

If Dietger decides to implement these in the Brigade path tracer we could be seeing (quasi) noise-free, real-time path traced (or better "real-time BDPT with MLT" traced) games much sooner than expected. Verrrry exciting stuff!! I think some rendering companies would hire this guy instantly.

## 4 comments:

Nice find, that's incredibly fast rendering. I didn't think a gpu could do this stuff, call me impressed. Shame it's Nvidia only.

Imagination to acquire Caustic Graphics, developer of real-time ray-tracing graphics technology


http://www.imgtec.com/corporate/newsdetail.asp?NewsID=602

Not really, I know that SLG (SmallLuxGPU) is OpenCL and runs very fast on my 5850 :)adn its in the process of being integrated into LuxRender, so you can get dispersive caustics )ie rainbow effect) with GPU acceleration.

This is pretty awesome. As for Nvidia cards... I love them, but it seems they went backwards in terms of GPU compute abilities from the 5xx line to the 6xx and maybe 7 as well. I believe that currently the gtx 580 is still far ahead of any of the later lines of graphics cards on the luxrender leaderboards. Hopefully they will introduce better optimized cards for GPGPU since that's been a pretty big area of research for many people and companies.

Post a Comment