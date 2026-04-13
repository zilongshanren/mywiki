---
title: Minecraft path traced in real-time with Brigade!
url: http://raytracey.blogspot.com/2010/10/minecraft-path-traced-in-real-time-with.html
author: Sam Lapere
published: '2010-10-18'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

![](../../assets/6327b46e866c4b12.jpg)


![](../../assets/6327b46e866c4b12.jpg)

Very nice work again from Bikker and co. A level from Minecraft, the current hype in indie games, that is path traced in near real-time using the Brigade path tracer! Enjoy:

[http://www.youtube.com/watch?v=7REP_FE0e98](http://www.youtube.com/watch?v=7REP_FE0e98)

The path traced lighting does look completely different from the lighting in the original Minecraft game, which isn't bad but not nearly as realistic.

UPDATE: here's another video with much improved importance sampling:

[http://www.youtube.com/watch?v=xZ62VwiLr3A](http://www.youtube.com/watch?v=xZ62VwiLr3A)

![](../../assets/659f24283f1e0e3e.jpg)


![](../../assets/659f24283f1e0e3e.jpg)

This new video shows that even with the current hardware, there is still a lot of potential left to reduce noise and improve the image quality of real-time path traced graphics through better algorithms (importance sampling, maybe ERPT or something similar to MLT) and filtering methods.

## 5 comments:

Is Minecraft a paradox in that it does with polygons what was meant for voxels? The only difference is that these cubes are textured where as voxels cannot be.

Yeah, I agree that voxels would suit this game much better and would be more efficient. The gameplay is practically begging to use voxels/octrees. And it would also speed up the path tracing quite considerably, because there's no triangle intersection anymore.

i actually assumed both were using sparse voxel octrees, that hot new technology from 2009.


again on ompf another jon (not the carmack) was posting about id's experiments with SVOs. around then these methods were quite popular, though the hype seems to have died down lately.

You are right lycium. SVOs were indeed "invented" by Jon Olick (I have made quite a few blog posts about it actually), but there hasn't been much news about it since. It was targeted at GPGPU. Minecraft isn't using SVO though, according to the wiki - "Minecraft uses a voxel system which is an incremental 3d grid in which each grid point holds a data for a single block." They are stored as voxels, but rendered as polygons. So a hybrid. http://www.minecraftwiki.net/wiki/Map

"the hype seems to have died down lately"


What?!

The Unreal Engine 4 "Elemental Demo" does cone tracing into a SVO pyramid...

Post a Comment