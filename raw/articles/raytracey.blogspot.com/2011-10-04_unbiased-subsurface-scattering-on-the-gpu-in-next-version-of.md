---
title: Unbiased subsurface scattering on the GPU in next version of Octane Render
url: http://raytracey.blogspot.com/2011/10/unbiased-subsurface-scattering-on-gpu.html
author: Sam Lapere
published: '2011-10-04'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Wow, the developers behind Octane render never cease to amaze. After being the first GPU renderer to implement Population Monte Carlo (a more complex rendering method than plain path tracing which borrows concepts from Metropolis light transport and energy redistribution path tracing to handle scenes with difficult lighting more efficiently), Octane render is now adding unbiased subsurface scattering along with other features such as instancing. Here's the announcement post from radiance (Octane's main developer) over at the


[Octane forum](http://octanerender.com/forum/viewtopic.php?f=5&t=8777&start=0&sid=21ebe6a88652ef9a4100174f9c55dcb0):"We have fully working and VERY fast SSS ready for release in the next test version. It renders about as fast (a tiny bit slower) as a glossy specular material. And, it's unbiased/bruteforce SSS, eg no bias introducing photon grids or other precomputed approximations.

[...]

This is the prime new feature in the next test release, along with instancing support and FAST voxelisation, and another suprise feature, aswell as the soon to be publically released first of a series of new products, OctaneRender for 3DS Max."

Surprise feature? Refractive Software knows how to keep their audience hyped ;-)


Some screenshots with the new SSS method can be seen in


I think it will eventually be possible to implement every feature found in traditional CPU renderers on the GPU and make it an order of magnitude faster. For example, Radiance



Some screenshots with the new SSS method can be seen in

[this thread](http://octanerender.com/forum/viewtopic.php?f=5&t=8777&sid=21ebe6a88652ef9a4100174f9c55dcb0).I think it will eventually be possible to implement every feature found in traditional CPU renderers on the GPU and make it an order of magnitude faster. For example, Radiance

[hinted at bidirectional path tracing + PMC](http://octanerender.com/forum/viewtopic.php?p=55695&sid=ab27583386a7f277739bf42c8ab1d461#p55695):"Bidirectional pathtracing (and PMC) should make renders like this one converge MUCH faster and bidirectional pathtracing + PMC is something we will be starting work on next, after 2.5 is out.GPU rendering is going to redefine every area of rendering from movies, animation, visualization and design to games, simulation and virtual reality. Truly the most exciting time for rendering in decades. I'm very happy that this paradigm shift is in full swing and that things are evolving at nauseating speed :-)

PMC + bidirectional will be ideal, it will be as efficient as the popular standard in CPU based unbiased engines (MLT+bidir), and this combined with the power of GPUs should really take things to a new level."

## No comments:

Post a Comment