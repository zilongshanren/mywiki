---
title: Latest version of Futuristic Buildings with AABB
url: http://raytracey.blogspot.com/2011/07/latest-version-of-futuristic-buildings.html
author: Sam Lapere
published: '2011-07-27'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

![](../../assets/8d1a882ed8386840.png)


![](../../assets/8d1a882ed8386840.png)

I've implemented tight fitting AABB hitboxes around the car and the two buildings, which gives a nice performance boost of about 50-200%, depending on the viewpoint. Since the car can be moved (with the I, J, K, L keys), the AABB around the car is moving with it and its position is updated every frame.

**Download the executables and the source code for "Futuristic Buildings v2.9 with AABB" from**

[http://code.google.com/p/tokap-the-once-known-as-pong/downloads/list](http://code.google.com/p/tokap-the-once-known-as-pong/downloads/list)Real car physics are coming up next. After those are in, OBBs (oriented bounding boxes) or oriented cylinders (depending on which one's cheaper to intersect) are on the todo list for some crazy real-time path traced physics simulations.

## No comments:

Post a Comment