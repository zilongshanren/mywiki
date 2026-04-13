---
title: 'Unbiased Truck Soccer: coming soon!'
url: http://raytracey.blogspot.com/2011/03/unbiased-truck-soccer-coming-soon.html
author: Sam Lapere
published: '2011-03-15'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

![](../../assets/908d1469df266d55.jpg)


![](../../assets/908d1469df266d55.jpg)

I had the idea for this game just yesterday. The goal is to push the ball against the moving goal (glowing paddle) of the opponent and score. Once it's finished and physics are actually working, you will be able to move the truck in every way, not just forward, backward and strafing left and right. Initially it will be a two player game, but hopefully I can make a single player game with an AI controlled truck.



In this particular case, path tracing provides very real and natural looking lighting and shadows. And it's still somewhat real-time on my poor laptop with 8600M GT (2.3 fps, with 4 samples per pixel , max path length 4, at default resolution), so I'm confident that it will look and play much better on a high end GPU. A GTX580, which is 20 times faster than my card (measured with Cornell Box Pong), should be able to reach 40 fps at 4 spp, default resolution. Image quality at 4 spp is very acceptable thanks to the frame averaging trick (reusing samples from previous frames to fake motion blur) by Kerrash. Hopefully I can get the Bullet physics engine working soon.


Download the exe for this WIP Tokap Unbiased Truck Soccer at

Download the exe for this WIP Tokap Unbiased Truck Soccer at

[http://code.google.com/p/tokap-the-once-known-as-pong/](http://code.google.com/p/tokap-the-once-known-as-pong/)

The following GIF (click on it to see the whole image) shows the effect of the max path length on the lighting in the scene. The difference in realism between the image with path length 1 (zero bounces = direct lighting only, no global illumination) and the image with path length 2 (1 bounce global illumination) is huge. Reflections and color bleeding (mostly visible on the surfaces facing downward and on the ceiling) are completely missing from the image with path length 1. Refractive objects need at least a path length of 3 to become (slightly) transparent. The effect on framerate is also interesting: rendering with path length 3 (1.08 fps) halves the framerate compared to rendering with direct light only (2.07 fps).


![](http://i53.tinypic.com/rap79s.gif)


![](http://i53.tinypic.com/rap79s.gif)

![](../../assets/25800ea0043bf9c2.jpg)


![](../../assets/25800ea0043bf9c2.jpg)

![](../../assets/be26f0719f7ffb67.jpg)


![](../../assets/be26f0719f7ffb67.jpg)

![](../../assets/db61d0981c973782.jpg)


![](../../assets/db61d0981c973782.jpg)

![](../../assets/3017a154c44382c2.jpg)


![](../../assets/3017a154c44382c2.jpg)

Below is a simple chart plotting max path length against framerate. The numbers are for the above scene at default resolution and 4 spp on a 8600M GT. The curve demonstrates that the framerate is less impacted at higher path lengths.


![](../../assets/25dbc664cb3abe1a.jpg)


![](../../assets/25dbc664cb3abe1a.jpg)

UPDATE: 2 more videos

Mapping the movement keys to the eye pupils gives this result:

Playing with the main light source (720p video):

Rocky's opinion about the current state of game graphics:


![](http://i53.tinypic.com/25hmh79.gif)


![](http://i53.tinypic.com/25hmh79.gif)

## No comments:

Post a Comment