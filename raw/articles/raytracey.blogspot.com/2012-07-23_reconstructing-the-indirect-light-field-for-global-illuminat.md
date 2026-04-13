---
title: '"Reconstructing the indirect light field for global illumination" paper finally
  available'
url: http://raytracey.blogspot.com/2012/07/reconstructing-indirect-light-field-for.html
author: Sam Lapere
published: '2012-07-23'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[http://groups.csail.mit.edu/graphics/ilfr/ilfr_preprint.pdf](http://groups.csail.mit.edu/graphics/ilfr/ilfr_preprint.pdf)

Aila and Laine (Nvidia research) are both geniuses when it comes to GPU path tracing, image reconstruction, SVO and GI in general and their papers are guaranteed to contain exciting (and reproducible) results. The paper includes some interesting comparisons between the new algorithm, the a-trous wavelet filter and random parameter filtering. Good stuff!

## 6 comments:

Lovely paper (can't say I followed all of it as this is not my expertise). From what I can see though even a simple adaptation of this is probably not suited to game-friendly PT (i.e. Brigade) and is very memory intensive. Am I assuming they use a GTX 480 rather than 580 due to how long this paper has been in the works?

This is a group of very clever techniques! It is similar to Adaptive Field Manifolds (perhaps just that they are both screen-space filters), but uses additional sample characteristics for the final construction. The final construction has INCREDIBLE fidelity especially given the low sampling rates in some of the example pictures -- the 1 spp Cornell box blew my mind!



I would

loveto get an idea of the per-frame penalties of using such techniques on modern hardware.Do you have any additional insight, Sam? I'm still learning and would love to get your feedback on what you like most!

Gah! I just was reading the Test Results section further and it has the information I was looking for!


It's still expensive, but those costs will drop with optimization, and the forward march of technology!

Just noticed odd test result. Pg 6/10 para 2, 8SPP took 36.6sec, whereas 512 SPP took 3910.5sec.




If things scale linearly 512SPP should take 2342.4sec.

I realise they might want to break up the long computation stages to prevent GPU timeout but if anything 512 SPP should still carry less overhead than 8SPP render frames, and if anything scale better.

Am i missing something?

It's probably not very useful for real-time path tracing as it takes several minutes to filter a 720p image on the GPU with this technique.

@Sam - How this approach is computed? I mean, is it a "tile/bucket pass" after the render samples, or is it calculated concurrently?

Post a Comment