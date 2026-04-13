---
title: 'Some details about the new PowerVR GPU with Caustic Graphics ray tracing hardware.
  UPDATE: Hoax! (see comments)'
url: http://raytracey.blogspot.com/2011/02/some-details-about-new-powervr-gpu-with.html
author: Sam Lapere
published: '2011-02-16'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[http://segaleaks.wordpress.com/2011/02/02/powervr-engineer-speaks/](http://segaleaks.wordpress.com/2011/02/02/powervr-engineer-speaks/)


“CPU ray tracing has received tremendous speed ups in the past decade, with works on acceleration structures, traversal algorithms, and packet (or frustum) traversal. While these advancements brought ray tracing into the real-time area, the speed is still generally not acceptable.

PowerVR presents a solution, which proposes to place a small dedicated hardware ray traversal engine (RTE) directly on the GPU die.

The RTE has been conﬁrmed to run at frequencies above 2GHz and can ﬁt into an area less than 15mm2, achieving performance of over 1000 million rays per second.”

**All the numbers in the hoax article (2 Ghz, 15 mm2, 1000 million rays/sec) are pulled straight from the paper by Tomas Davidovic entitled "Performance Considerations When Using a Dedicated Ray Traversal Engine" (**

[http://www.davidovic.cz/wiki/lib/exe/fetch.php/school/davidovic_wscg2011/davidovic_wscg2011.pdf](http://www.davidovic.cz/wiki/lib/exe/fetch.php/school/davidovic_wscg2011/davidovic_wscg2011.pdf))**except that the paper mentions 100 million rays/sec for the RTE instead of 1000 million rays/sec.**



**Very pathetic journalism, this article would fit much better at a site like semi-accurate where you know beforehand you're reading trash).**

## 8 comments:

Sorry to disappoint you , but that's essentially directly ripped off my recently presented paper (http://www.davidovic.cz/wiki/doku.php/school/davidovic_wscg2011/davidovic_wscg2011) and as such essentially unbelievable.


Tomas

PS: I am not affiliated with any of the companies mentioned.

Doesn't the idea of a dedicated hardware RTE smell like the idea of a PPU (Ageia)? :P

Well, it sure does.

But I know I am not producing any such thing. And unless PowerVR has a crystal ball to read my design, neither are they. (Which they might, they used my papers introduction for this announncement :-) )

I've had chance to read through the paper now.



Very interesting idea.

Do you think the concept is compatible with nVidia's plans to integrate ARM cores into their design?

i.e. Could the ARM CPU's work as an RTE?

Overall, I don't see too much of a problem. It is heterogenous and has very little pressure on bandwidth and latency between the two parts.




However, having a general purpose ARM act as RTE does not make much sense to me. The way I see it, it is as if you had GPU ray tracer that sent rays to CPU to be traced.

I can imagine RTE being connected via the same means as ARM is, but the whole idea is that there is something to be gained by moving ray tracing into dedicated HW. Moving it onto even more general purpose goes against that.

The most hopeful way I see is that some way to merge ray tracing and rasterization HW emerges. But I have yet to see some hints for the development going in this direction.

@tomas





"The most hopeful way I see is that some way to merge ray tracing and rasterization HW emerges. But I have yet to see some hints for the development going in this direction"

3D raserization uses a hybrid between raytracing and rasterization.

http://www.vis.uni-stuttgart.de/~engelhts/paper/3dr_techreport.pdf

From what i understand POWERVR already uses ray tracing to determine visibility against transformed triangles.

What are your thoughts of possible hardware direction for Powervr in the future.

I know of the techreport (being author and all that), and the biggest counterargument is that right now it would result in way too complicated hardware because it works in floating point.


As to future of PowerVR, I have no idea what it might be, know very little of the architecture. I only know that this "insider report" is a complete fabrication.

Thanks Tomas! I've added an update to the post. I had read your paper on RTE already, but not thorougly enough apparently ;). The numbers from the article sounded vaguely familiar to me though ;)

Post a Comment