---
title: Bullet Physics in Simplex Paternitas path tracer
url: http://raytracey.blogspot.com/2011/07/bullet-physics-in-simplex-paternitas.html
author: Sam Lapere
published: '2011-07-29'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

![](../../assets/23d2c7381f33fc19.png)


![](../../assets/23d2c7381f33fc19.png)

Someone on youtube suggested to make a version of the physics animation from my previous post where the scene is only lit by the small white ball on top. For this purpose I've incorporated the Bullet library to the Simplex Paternitas path tracer of Jacco Bikker. The results are pretty wicked:



![](../../assets/e32c46144ab3eca3.png)


![](../../assets/e32c46144ab3eca3.png)

This video was rendered on a 8600M GT, 12 spp, 480x360 resolution:

Without caustic noise (only reflective and diffuse balls, 12 spp, 640x480 resolution on 8600M GT):

The new executable and source code are available at

[http://code.google.com/p/tokap-the-once-known-as-pong/downloads/list](http://code.google.com/p/tokap-the-once-known-as-pong/downloads/list)

Damn this stuff is really addictive!

## 5 comments:

hey mate,


Can you compile a 64 bit [64spp] exe

i dont have the 64 bit cudart64.dll or something like that

Sure, but I don't have access to a 64-bit system right now (maybe in a few days I will).

I've got a 64bit environment, let me see what I can do

Thanks Kerrash. If you need any help with compiling the source code, I've been through the process a couple of times already :)

Anyone compiled something for Linux?


Cheers,

Post a Comment