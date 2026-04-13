---
title: Comparing path tracing image quality
url: http://raytracey.blogspot.com/2010/04/comparing-path-tracing-image-quality.html
author: Sam Lapere
published: '2010-04-23'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Video 1: Porsche Carrera rendered with Octane](http://www.youtube.com/watch?v=xHqRLLbfQt0)

2 samples/pixel

![](../../assets/dbc8a4fabcd46cb2.jpg)


6 samples/pixel

![](../../assets/1165522155f5dc16.jpg)


12 samples/pixel

![](../../assets/85aea2bb6e30f389.jpg)


24 samples/pixel

![](../../assets/d64602b24cef438e.jpg)


36 samples/pixel

![](../../assets/bc982af4ae633cbf.jpg)


1 sample/pixel

![](../../assets/2304e29eaaa150c0.jpg)


8 samples/pixel

![](../../assets/644c0210cc4a0ec2.jpg)


16 samples/pixel

![](../../assets/5d2d039eea24e413.jpg)


24 samples/pixel

![](../../assets/241a2686a66a5604.jpg)


40 samples/pixel

![](../../assets/c0dabab7f4fcf0a7.jpg)


1 sample/pixel

![](../../assets/c435a15f5c94e4ab.jpg)


8 samples/pixel

![](../../assets/b9c6ef3454922237.jpg)


16 samples/pixel

![](../../assets/c734fc6c2610284e.jpg)


32 samples/pixel

![](../../assets/28db6020b261145c.jpg)


64 samples/pixel

![](../../assets/c92ac229341452c7.jpg)


96 samples/pixel

![](../../assets/05749b0f4b2c9c32.jpg)


[Video 2: Chalet/Hotel rendered with Octane](http://www.youtube.com/watch?v=iIGA32VOKWk)

1 sample/pixel

![](../../assets/f86604fcb3720ac0.jpg)


8 samples/pixel

![](../../assets/8bb88abc8e8dc35b.jpg)


16 samples/pixel

![](../../assets/aba5d813ecf8c8ad.jpg)


32 samples/pixel

![](../../assets/9f4e2e0256436a36.jpg)


As these pictures show, the noise clears very fast at the beginning, but the image converging slows down rather quickly, following a saturation curve

![](../../assets/8d44bfec16833b05.img)


![](../../assets/8d44bfec16833b05.img)

8 samples/pixels is too noisy to see fine details, at 16 samples/pixels details start to appear and 32 samples/pixel gives sufficient quality for a game imo (compared to the horribly lowres shadow maps and normal maps in some of today's AAA games, like Modern Warfare 2). Unfortunately, the youtube video and subsequent jpeg compression makes the difference between 64 and 96 samples/pixel indiscernible. More than 100 samples/pixel would be ideal, but for now 32 will do. Hopefully the Fermi GPU (or multiple) will get us there soon.




UPDATE: I made a shitload of screengrabs (way too much) from

UPDATE: I made a shitload of screengrabs (way too much) from

[this video](http://www.youtube.com/watch?v=c0bwcsWi_fw)(HD footage of the Brigade engine)1 spp

![](../../assets/05b12b6b000cad7f.jpg)


## No comments:

Post a Comment