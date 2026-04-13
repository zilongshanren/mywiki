---
title: New version of Brigade path tracer
url: http://raytracey.blogspot.com/2010/07/new-version-of-brigade-path-tracer.html
author: Sam Lapere
published: '2010-07-07'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[this post](http://ompf.org/forum/viewtopic.php?f=8&t=1775&p=19649#p19638)to download. There's some new features + performance increase. Rename cudart.dll to cudart32_31_9.dll to make it work.

The next image demonstrates some of the exceptional strenghts of using path tracing:

- indirect lighting with color bleeding: notice that every surface facing down (yellow arrows) picks up a slightly greenish glow from the floor plane, due to indirect light bouncing off (this picture uses path trace depth 6)

- soft shadows

- indirect shadows

- contact shadows (ambient occlusion)

- superb anti-aliasing

- depth of field

- natural looking light with gradual changes

all of these contribute to the photorealistic look and it's all interactive (on high end cpu+gpu)!

![](../../assets/0dcd5e45badb44be.jpg)


![](../../assets/0dcd5e45badb44be.jpg)

## No comments:

Post a Comment