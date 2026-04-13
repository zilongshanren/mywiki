---
title: Incredible real-time GPU path tracer using WebGL
url: http://raytracey.blogspot.com/2011/04/real-time-path-tracing-for-webgl.html
author: Sam Lapere
published: '2011-04-19'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Yesterday I came across another awesome GPU renderer (made by Evan Wallace), it's a very neat and extremely fast path tracer using GLSL shaders running in the browser:

A WebGL-enabled browser is required to run this (I highly recommend the latest Chrome build from

[http://www.khronos.org/webg/wiki/Getting_a_WebGL_Implementation#Chrome.2FChromium](http://www.khronos.org/webgl/wiki/Getting_a_WebGL_Implementation#Chrome.2FChromium)(the Chrome Canary build works great if you're on Windows, Firefox 4.0 crashes and other Chrome versions didn't work for me, it just keeps loading).It's great fun to edit the scene: move the light or objects and see soft shadows being cast in real-time (60 fps) on the walls and other objects. You can also change materials and add extra objects. It renders blazingly fast even on very low end GPUs. Very impressive!

Source code for the path tracer:

There's also a GLSL version (Mac OS X):

With this technology, a path traced physics simulation like the one in

## 2 comments:

Hi,

I have extended his work to add refraction and more stuff check it our here http://mmmovania.blogspot.com

Nice, I will write a blogpost about your work later this week.

Post a Comment