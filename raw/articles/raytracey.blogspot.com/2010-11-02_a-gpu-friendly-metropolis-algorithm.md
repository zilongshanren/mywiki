---
title: A GPU friendly Metropolis algorithm
url: http://raytracey.blogspot.com/2010/11/gpu-friendly-metropolis-algorithm.html
author: Sam Lapere
published: '2010-11-02'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Just came across this paper on parallelizing the Independent Metropolis Hastings (IMH) algorithm:


[http://xianblog.wordpress.com/2010/10/12/parallel-processing-of-independent-metropolis-hastings-algorithms/](http://xianblog.wordpress.com/2010/10/12/parallel-processing-of-independent-metropolis-hastings-algorithms/)The fundamental idea in the current paper is that one can take advantage of the parallel abilities of arbitrary computing machinery, from cloud computing to graphical cards (GPU), in the case of the generic IMH algorithm, producing an output that corresponds to a much improved Monte Carlo approximation machine at the same computational cost.This could be very interesting for all the GPU renderers out there.

## 4 comments:

That's interesting! Can this parallel algorithm be used for unbiased rendering too?

I don't see any reason why it couldn't. Though I don't know much about Monte Carlo rendering and its derivatives (like Markov chain Monte Carlo)

From what I know, Independent Metropolis–Hastings (IMH) means that the next sample in the Markov chain does NOT depend on the current sample. In Metropolis based unbiased rendering however, the next sample is usually constructed by applying small mutations to the current sample. Hence, the next sample is NOT sampled independent from the current sample. AFAICS, the GPU friendly metropolis algorithm is therefore not directly applicable to metropolis based rendering.

Thank you for your explanation Dietger, makes perfect sense now that I think of it.



By the way, your latest videos blew me away. The MLT scene in particular looks very realistic. You should really post links on different forums (e.g. Blender artist forum, cgtalk, ompf, reddit, octane render forum ...) to attract attention and are a must-see for anyone in the (gpu) rendering business. Maybe you could make a comparison video between Kelemen MLT and PT to better appreciate MLT's advantages?

Looking forward to see more of your work on GPU rendering and on Brigade of course! Goe bezig, zeggen we hier in Gent :-)

Post a Comment