---
title: 'Update 11 on real-time path traced Tokap: Pimped out, chromed out truck!'
url: http://raytracey.blogspot.com/2011/03/update-11-on-real-time-path-traced.html
author: Sam Lapere
published: '2011-03-13'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

![](../../assets/e56b441dd402d06d.jpg)


![](../../assets/e56b441dd402d06d.jpg)

Since Tokap can (currently) only ray trace spheres, I've decided to build a funny looking car out of spheres: the body of the car consists of 3 merged diffuse spheres, the top sphere is a blue refractive sphere, the wheels are grey diffuse spheres with reflective spheres inside them representing the rims. The headlight is a reflective chrome like sphere with an emitting sphere inside. The car can currently only move forward, backward, and strafe sideways.

Image with motion blur, 20 spp (reusing samples from previous frames), 0.84 fps on 8600M GT

![](../../assets/3458659b767a407a.jpg)


![](../../assets/3458659b767a407a.jpg)

Image without motion blur, 20 spp, 0.84 fps (on 8600M GT):

![](../../assets/a476e9b207b635ab.jpg)


![](../../assets/a476e9b207b635ab.jpg)

This is an image where the main light source is turned off and the scene is only lit by the emitting white spheres in the headlights:

Some videos:

Notice the soft shadows and ambient occlusion under the car, and color bleeding from the floor onto the body of the car. Photorealism becomes a piece of cake with path tracing :-).

Everything is still rendered on my humble laptop with a 8600M GT, maybe it's time to upgrade ;-) Even on such low end hardware, the amount of noise is quite acceptable in this particular scene (where everything is mostly directly lit).

**Download this 'tokap truck' executable (CUDA enabled GPU required) at**


**http://code.google.com/p/tokap-the-once-known-as-pong/**Stay tuned for more tests with hopefully some physics so the truck can drive up a slope, push a ball, collide with another truck, ...

![](../../assets/726f911140368349.jpg)


![](../../assets/726f911140368349.jpg)

**UPDATE:**more videos!

If anyone has a better CUDA GPU than mine (which is not unlikely ;-), I would really appreciate it if you could capture a short video and upload it somewhere.

## No comments:

Post a Comment