---
title: Instancing Limits
url: http://hacksoflife.blogspot.com/2011/05/instancing-limits.html
author: Benjamin Supnik
published: '2011-05-24'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[instancing numbers](http://hacksoflife.blogspot.com/2011/03/instancing-numbers.html)a while ago. As we keep bashing on things, we've found that the upper limit for instanced meshes on a modern Mac with an ATI card appears to be about 100k instanced batches.

There is definitely a trade-off between the number of "actual" batches (e.g. the number of actual draw calls into the driver) and the number of instanced meshes. So we're looking at how to best trade off larger clumps of meshes (fewer driver calls) with smaller ones (less extra drawing when most of the clump is off screen and could have been culled.

There is also a point at which it's not worth using instancing: if the number of objects in the instanced batch is really low, it's quicker to use immediate mode instancing and call draw multiple times. We're not precisely sure where that line is, but it's low - maybe 2 or 3 batches.

(Note that using client arrays to draw an instanced batch where the instancing data is in system memory appears to be a non-accelerated case on 10.6.x - if the instance data isn't in a VBO we see performance fall over and die.)

## No comments:

## Post a Comment