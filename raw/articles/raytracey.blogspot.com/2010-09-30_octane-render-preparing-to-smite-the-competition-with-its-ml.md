---
title: Octane Render preparing to smite the competition with its MLT equivalent
url: http://raytracey.blogspot.com/2010/09/octane-render-preparing-to-smite.html
author: Sam Lapere
published: '2010-09-30'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Octane Render, the ultra-fast unbiased GPU renderer (made in Belgium just like me :-)) is soon going to introduce a new MLT-(Metropolis light transport)-like algorithm, which will make the rendering of certain difficult scenes with small light sources much more efficient: the scene will converge much faster, with less noise and will kill fireflies (bright pixels as a consequence of long paths from reflective caustics).

MLT is the base rendering algorithm used by unbiased CPU renderers like LuxRender, Maxwell Render, Fryrender, Indigo Renderer and Kerkythea.

Making Metropolis light transport (or an equivalent) work on current GPUs was thought by many to be impossible and it was one of the main criticisms from GPU rendering skeptics such as Luxology (Modo) and Next Limit (Maxwell Render), who believe that GPUs can only do dumb, inefficient path tracing and nothing more. Luckily there's Octane Render to prove them wrong. The fact that it has taken the developer such a long time to make it work shows that it's quite tricky to develop. Octane Render is currently also the only renderer (to my knowledge) that will utilise a more sophisticated rendering algorithm.

On a sidenote, ERPT (energy redistribution path tracing) is also possible on the GPU, as described in

[one of my previous posts](http://raytracey.blogspot.com/2010/07/energy-redistribution-path-tracing-in.html). It combines the advantages of Monte Carlo path tracing and Metropolis light transport to allow faster convergence with less noise and can achieve fantastic results, which look indistinguishable from the path traced reference (see

[http://raytracey.blogspot.com/2010/09/small-update-on-brigade-real-time-path.html](http://raytracey.blogspot.com/2010/09/small-update-on-brigade-real-time-path.html)) Timo Aila, a graphics researcher at Nvidia and GPU ray tracing genius, is also working on real-time Metropolis light transport (

[http://research.nvidia.com/users/timo-aila](http://research.nvidia.com/users/timo-aila)).

Octane's MLT-like algorithm has been hinted at by its developer since the unveiling of the software in January 2010, and it should be here very soon (within a couple of weeks, post will be updated when that happens). I'm very curious to see the first results.

Future GPU architectures, like Kepler and Maxwell, should make the implementation of MLT-like algorithms on the GPU much easier, but it's nice to see at least one developer trying to squeeze the maximum out of current GPUs, bending their compute capability until it breaks.

## 3 comments:

Refractive Soft should make a game engine with their Octane Render. That would rule!

Heh, you're reading my mind! ;-D

Neither fryrender nor Maxwell render use MLT. Neither does Octane. People tend to confuse MLT with (Bi-Directional) Path Tracing. Thank you.

Post a Comment