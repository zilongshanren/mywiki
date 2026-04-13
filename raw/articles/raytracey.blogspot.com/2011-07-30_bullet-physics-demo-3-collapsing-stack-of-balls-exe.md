---
title: 'Bullet Physics demo 3: Collapsing stack of balls + EXE'
url: http://raytracey.blogspot.com/2011/07/bullet-physics-demo-3-collapsing-stack.html
author: Sam Lapere
published: '2011-07-30'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

![](../../assets/35cc489afd2760a5.png)


![](../../assets/35cc489afd2760a5.png)

![](../../assets/9449c747a7735db6.png)


![](../../assets/9449c747a7735db6.png)

![](../../assets/7ec988ae8e18ca59.png)


![](../../assets/7ec988ae8e18ca59.png)

Yesterday I got a new idea for a real-time path traced Bullet physics animation: a collapsing stack of spheres. The plan:

![](../../assets/2f9741986d5fb88f.jpg)


![](../../assets/2f9741986d5fb88f.jpg)

I've implemented the scene and physics in both the tokaspt and the Simplex Paternitas path tracers to see the difference in framerate and realism.

Picture from Tokap (some circular artefacts which look kinda cool :) :

![](../../assets/ec6d72c859ae94c3.png)


![](../../assets/ec6d72c859ae94c3.png)

Picture from the Futuristic Buildings (Simplex Paternitas) path tracer:

![](../../assets/99ae1187ee9b9c32.png)


![](../../assets/99ae1187ee9b9c32.png)

All videos below were rendered in real-time on my poor little 8600M GT, probably one of the weakest CUDA-enabled cards in existence. Every animation below should run smoothly and at much higher quality on a GTX 260 or higher:


Tokap with Bullet 4 spp:

Futuristic Buildings with Bullet 12 spp:

Futuristic Buildings with Bullet 24 spp:

Futuristic Buildings with Bullet 4 spp, Eagle's view:

Download the executable for "TOKAP Bullet Sphere Stack" at


[http://code.google.com/p/tokap-the-once-known-as-pong/downloads/list](http://code.google.com/p/tokap-the-once-known-as-pong/downloads/list)UPDATE: Some people have reported that the Bullet demos don't work on their systems, receiving the following message:





This error is due to the fact that the demos were compiled with the Bullet library in debug mode and are dependent on the Visual C++ 2008 runtime library. Downloading the Microsoft Visual C++ 2008 Redistributable Package (x86) from

## 1 comment:

<3

Post a Comment