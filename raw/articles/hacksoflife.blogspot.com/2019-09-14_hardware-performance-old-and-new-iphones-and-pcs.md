---
title: 'Hardware Performance: Old and New iPhones and PCs'
url: http://hacksoflife.blogspot.com/2019/09/hardware-performance-old-and-new.html
author: Benjamin Supnik
published: '2019-09-14'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I am looking at performance on our latest revision of X-Plane Mobile, and I've noticed that the performance bottlenecks have changed from past versions.








In the past, we have been limited by some of everything - vertex count, CPU-side costs (mostly in the non-graphics code, which is ported from desktop), and fill rate/shading costs. This time around, something has changed - performance is pretty much about shading costs, and that's the whole ballgame.

This is a huge relief! Reducing shading costs is a problem for which real-time graphics has a lot of good solutions. It's normally

*the*problem, so pretty much all rendering techniques find ways to address it.
How did this shift happen? I think part of it is that Apple's mobile CPUs have just gotten really, really good. The iPhone X has a single-core GeekBench 4 score of 4245. By comparison, the 2019 iMac with an i5-8500 at 3 ghz gets 5187. That's just not a huge gap between a full-size gaming mid-range desktop computer and...a phone.

In particular, we've noticed that bottlenecks that used to show up only on mobile have more or less gone away. My take on this is that Apple's mobile chips can now cope with not-hand-tuned code as well Intel's can, e.g. less than perfect memory access patterns, data dependencies, etc. (A few years ago, code that used to be good enough that hand tuning wouldn't be a big win would need some TLC for mobile. It's a huge dev time win to have that not be the case anymore.)

If I can summarize performance advice for today's mobile devices in a single item, it would be: "don't blend." The devices easily have enough ALU and texture bandwidth to run complex algorithms (like full PBR) at high res as long as you're not shading the full screen multiple times. Because the GPUs are tiling, the GPU will eliminate virtually any triangles that are not visible in the final product as long as

**blending is off**.
By comparison, on desktop GPUs we find that

*utilization*is often the biggest problem - that is, the GPU has the physical ALU and bandwidth to over-draw the scene multiple times if blending is left on, but the frame is made up of multiple smaller draw calls, and the GPU can't keep the entire card fed given the higher frequency of small jobs.
(We did try simplifying the shading environment - a smaller number of shaders doing more work by moving what used to be shader changes into conditional logic on the GPU. It was not a win! I think the problem is that if

*any*part of a batch is changed, it's hard for the GPU to keep a lot of work in flight, even if the batch is "less different" than before optimization. Since we couldn't get down to "these batches are identical, merge them" we ended up with similarly poor utilization and higher ALU costs while shading.)
## No comments:

## Post a Comment