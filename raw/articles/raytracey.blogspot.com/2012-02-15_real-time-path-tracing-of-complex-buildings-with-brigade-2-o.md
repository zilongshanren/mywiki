---
title: Real-time path tracing of complex buildings with Brigade 2 on 2 GTX 580s
url: http://raytracey.blogspot.com/2012/02/real-time-path-tracing-of-complex.html
author: Sam Lapere
published: '2012-02-15'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I finally got a new system specifically built to do some serious real-time path tracing tests. It contains 1 quad core Core-i7 and 2 GTX 580 GPUs and it just rips through the most complex scenes you throw at it. Brigade 2 doesn't use the CPU for rendering, but it is important for dynamic scenes that require multiple BVH updates/rebuilds, which is currently done on the CPU.

The Brigade 2 path tracer can really show its muscle on such a powerful system and regularly breaks 250 million rays per second as can be seen in the following video of a real-time path traced building containing

__(640x480 full render resolution, 8 spp per frame, motion blur with frame averaging):__**430k triangles**
Color bleeding from the floor on the overhanging structure:

Orange color bleeding on the disk shaped roof:

The building model is free and can be found on

## 5 comments:

Ow, you got your fast machine! That's great! I'm looking forward to what you will make it do. :)

I have some ideas that might make it crawl ;)

Oh wonderful! Look forward to seeing all the cool things to come :)

Awesome mate.

I was waiting that you upgraded your machine.

Now we'll see some serious stuff ;)

Good rig and video ^^

Post a Comment