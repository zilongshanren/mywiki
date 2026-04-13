---
title: Paper on accelerating path tracing using eye path reprojection available
url: http://raytracey.blogspot.com/2011/07/paper-on-accelerating-path-tracing.html
author: Sam Lapere
published: '2011-07-25'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Quasi-random, more or less unbiased blog about real-time photorealistic GPU rendering

Monday, July 25, 2011

Paper on accelerating path tracing using eye path reprojection available

The paper "Accelerating path tracing by eye path reprojection" by Niklas Henrich et al., which I blogged about earlier is available from http://www.rendering.ovgu.de/publikationen.html. The algorithm achieves similar quality as regular path tracing in half the time and can easily be ported to the GPU. The authors also plan to incorporate their technique into a real-time raytracer.

1 comment:

Anonymous
said...

Huh. From the scant preliminary information, I thought they were using random vertices as virtual point sources. Using onscreen bounces as free samples is much more interesting - even if it doesn't always add much light.

## 1 comment:

Huh. From the scant preliminary information, I thought they were using random vertices as virtual point sources. Using onscreen bounces as free samples is much more interesting - even if it doesn't always add much light.

Post a Comment