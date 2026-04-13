---
title: '"Futuristic Buildings" a new real-time path traced demo'
url: http://raytracey.blogspot.com/2011/07/futuristic-buildings-new-real-time-path.html
author: Sam Lapere
published: '2011-07-17'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

![](../../assets/1f7250062ffd1af7.png)


![](../../assets/1f7250062ffd1af7.png)

I've decided to put my freshly learned C++ skills to the test, and what better way is there than modifying the source code of an already awesome program, in this case the recently released real-time path tracer


The purpose of this demo was to emphasize the extraordinary capabilities of this path tracer, in particular the ultra-high-quality global illumination with color bleeding and dynamic soft shadows at real-time framerates. The demo renders almost noise-free images at 16 samples per pixel and should render them very fast when you have a high end GPU (>30 fps I guess, I only tested it with a 8600 M GT).


Some images:










Download "Futuristic Buildings" at




A CUDA enabled GPU is required as the path tracing happens entirely on the GPU.


This is work in progress of course, I'm planning to add another building and a user-controllable character (the truck from Unbiased Truck Soccer :) . A video should follow soon.



["Simplex Paternitas" by Jacco Bikker](http://raytracey.blogspot.com/2011/07/simplex-paternitas-real-time-path.html). For "Futuristic Buildings" I modified some of the animation from Simplex Paternitas, added some new animations and also a new "skyscraper" building with moving spheres.The purpose of this demo was to emphasize the extraordinary capabilities of this path tracer, in particular the ultra-high-quality global illumination with color bleeding and dynamic soft shadows at real-time framerates. The demo renders almost noise-free images at 16 samples per pixel and should render them very fast when you have a high end GPU (>30 fps I guess, I only tested it with a 8600 M GT).

Some images:

![](../../assets/9c0a2b7ee2c10490.img)

![](../../assets/9c0a2b7ee2c10490.img)

![](../../assets/e1f3e71b844db5a9.img)

![](../../assets/e1f3e71b844db5a9.img)

![](../../assets/26bceb93da6d3ca2.img)

![](../../assets/26bceb93da6d3ca2.img)

![](../../assets/bdb9b02e9c720d84.png)

![](../../assets/bdb9b02e9c720d84.png)

![](../../assets/be7c07a534c99255.png)

![](../../assets/be7c07a534c99255.png)

![](../../assets/37cbedbce1480fb1.img)

![](../../assets/37cbedbce1480fb1.img)

Download "Futuristic Buildings" at

[http://code.google.com/p/tokap-the-once-known-as-pong/downloads/list](http://code.google.com/p/tokap-the-once-known-as-pong/downloads/list)A CUDA enabled GPU is required as the path tracing happens entirely on the GPU.

This is work in progress of course, I'm planning to add another building and a user-controllable character (the truck from Unbiased Truck Soccer :) . A video should follow soon.

## 2 comments:

Hi, is there a Linux version?


It doesn't work with wine unfortunately :-(

Cheers,

Hello,


I don't have Linux installed, but I will upload the source code so you can compile your own version.

Post a Comment