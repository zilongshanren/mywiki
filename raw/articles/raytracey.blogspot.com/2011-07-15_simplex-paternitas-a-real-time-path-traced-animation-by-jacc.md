---
title: Simplex Paternitas, a real-time path traced animation by Jacco Bikker
url: http://raytracey.blogspot.com/2011/07/simplex-paternitas-real-time-path.html
author: Sam Lapere
published: '2011-07-15'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Jacco Bikker (developer of the Brigade path tracer and Arauna ray tracer) has released a cool video and executable demo of a real-time path traced animation called "Simplex Paternitas" created for iGathering 2011 (a demoscene festival organised at IGAD):




The demo in the video runs smoothly on just one GTX 470. Links to the executable demo and source code can be found in the video description. I've tried the 32 spp demo on my laptop with 8600M GT and got around 2 fps! :)



Soft shadows, refraction and caustics



Accurate color bleeding from the blue and red walls is clearly visible in the shadows of the characters and reflective sphere


The animation reminds me of vintage CG from the eighties (like


[http://www.youtube.com/watch?v=PaTz9tJ7_KY](http://www.youtube.com/watch?v=PaTz9tJ7_KY)The demo in the video runs smoothly on just one GTX 470. Links to the executable demo and source code can be found in the video description. I've tried the 32 spp demo on my laptop with 8600M GT and got around 2 fps! :)

![](../../assets/5dabb95fd5437eae.png)

![](../../assets/5dabb95fd5437eae.png)

Soft shadows, refraction and caustics

![](../../assets/06b0d887f8db60ac.png)

![](../../assets/06b0d887f8db60ac.png)

Accurate color bleeding from the blue and red walls is clearly visible in the shadows of the characters and reflective sphere

The animation reminds me of vintage CG from the eighties (like

[this](http://www.youtube.com/watch?v=k-GZ0PogVLw)one) which was rendered with either rasterization or Whitted-style ray tracing and needed several CPU hours per frame, while this is path traced in just a few milliseconds per frame.UPDATE: I tinkered a bit with the scene parameters (different colors and materials and brighter sky). The image is taken at 28 samples per pixel. There is some slight greenish color bleeding from the ground onto the bottom half of the spheres and the character (not Kirby :) I will upload a video very soon. Even at 16 spp, there is almost no noise in the outdoor scene except for refractive spheres.

![](../../assets/22027748f0d148a6.png)


![](../../assets/22027748f0d148a6.png)

![](../../assets/765b22701196b4f0.png)


![](../../assets/765b22701196b4f0.png)

## 3 comments:

could you please rehost the video somewhere else or without music?


because all i got is this:

Unfortunately, this UMG-music-content is not available in Germany because GEMA has not granted the respective music publishing rights.

Hi,


unfortunately I did not make this video (Jacco Bikker did). I might upload a video of this demo tomorrow but it won't run as smoothly (I have a GTS 450 vs the GTX 470 that was used for the video).

Links to source code failed.

Can you supply the source code?

Post a Comment