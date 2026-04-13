---
title: 720p video of Unbiased Truck Soccer Sunny Sky with caustics!
url: http://raytracey.blogspot.com/2011/03/720p-video-of-unbiased-truck-soccer.html
author: Sam Lapere
published: '2011-03-29'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[http://www.youtube.com/watch?v=ymo57ElhHvY](http://www.youtube.com/watch?v=ymo57ElhHvY)

Rendered with my 8600M GT, it's still doing a pretty good job despite its age :) The caustics from the glass sphere are not reflected in the mirror ball because max path length is set to 3 for performance reasons. Setting max path length to 4 will show the reflection of the caustic light pattern.


Download executable:

[http://code.google.com/p/tokap-the-once-known-as-pong/downloads/list](http://code.google.com/p/tokap-the-once-known-as-pong/downloads/list)

![](../../assets/2fb24828724fa405.jpg)


![](../../assets/2fb24828724fa405.jpg)

Increasing the emission values (RGB) of the "sun" to 4, 4, 2 makes the caustics more obvious:

![](../../assets/2b3e2d5027405ed9.jpg)


![](../../assets/2b3e2d5027405ed9.jpg)

## 4 comments:

Very impressive, good work!! And can you tell me what acceleration structure did you use on the GPU side?

Thanks!




There is no acceleration structure actually. The scene only consists of spheres (about 30 of them). So every ray is tested for intersection with each of the 30 spheres, which is not very efficient. The ray tracing performance decreases with ~50% with every 15 extra spheres. Using a BVH or octree would increase performance, but then you would also have the overhead of the acceleration structure which is not worth it in a simple scene as this one.

But I'm hoping to implement an acc structure soon though. First I want to make the Bullet physics work, which is trickier than I thought.

Btw, just to be clear, I did not write the path tracer myself, I am using the open source code from tokaspt.

if you choose a specific bounce depth for the tracer it is no longer unbiased (a word that is quite unappropriate for any kind of tracer).

I realize that it's not unbiased in the strict sense, but the term is thrown around liberally by so many commercial ray tracers without statistical proof that their renderer is really unbiased. Whether it's unbiased or consistent is a rather academic discussion, and I deliberately chose to name the game "Unbiased Truck Soccer" for the irony of it.

Post a Comment