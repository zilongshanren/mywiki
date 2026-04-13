---
title: Brigade path tracer comparison
url: http://raytracey.blogspot.com/2010/07/brigade-path-tracer-comparison.html
author: Sam Lapere
published: '2010-07-02'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[http://igad.nhtv.nl/~bikker/](http://igad.nhtv.nl/%7Ebikker/)

Rendered with CPU only at resolution 832x512

Images with 100 and 800 spp were taken without frame averaging (only 1 iteration)

Images with 2, 8, 16, 32 spp taken with frame averaging (averaging samples of several frames)

2 spp

![](../../assets/c6dcb420ad2072a0.jpg)


![](../../assets/c6dcb420ad2072a0.jpg)

8 spp

![](../../assets/512f3f4375aac243.jpg)


![](../../assets/512f3f4375aac243.jpg)

16 spp

![](../../assets/82011bec7969f9e4.jpg)


![](../../assets/82011bec7969f9e4.jpg)

32 spp

![](../../assets/768853adb4c25add.jpg)


![](../../assets/768853adb4c25add.jpg)

100 spp

![](../../assets/1e987f40c8c4f486.jpg)


![](../../assets/1e987f40c8c4f486.jpg)

800 spp

![](../../assets/576804ba06699ef5.jpg)


![](../../assets/576804ba06699ef5.jpg)

To top it off, one big image comparing 800, 8, 16 and 32 spp. It amazes me that the quality of just 8 samples is already great and with some filtering it could rival the quality of the 800 spp image:

![](../../assets/1fb2d44f11e6c606.png)


![](../../assets/1fb2d44f11e6c606.png)

## 2 comments:

I have tried the demo and it was really impressive!


Frame averaging however looks really ugly, especially with moving objects.

I wonderer if the authors are considering the use of reprojection cache: http://www.cs.princeton.edu/gfx/pubs/Nehab_2007_ARS/NehEtAl07.pdf . I thing that it could help.

Thanks for the paper, Seb. The reprojection technique could very well work here imo. But I think it's only good for diffuse materials (which is also a limit of the frame averaging technique)


Some time ago, I read a paper by Vlastimil Havran on exploiting interframe spatio-temporal coherency with bidirectional path tracing: http://www.mpi-inf.mpg.de/resources/anim/EGSR03/ . This might also work.

Post a Comment