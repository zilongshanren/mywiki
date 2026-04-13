---
title: 'Design Garage: stunning Nvidia tech demo using raytracing ;-)'
url: http://raytracey.blogspot.com/2010/04/design-garage-stunning-nvidia-tech-demo.html
author: Sam Lapere
published: '2010-04-10'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[http://www.youtube.com/watch?v=nEXeTXmCfdE](http://www.youtube.com/watch?v=nEXeTXmCfdE&feature=related)

The OptiX team did a really great job with this. I hope they will build upon it, using more advanced algorithms like bidirectional pathtracing, Metropolis light transport or even stochastic progressive photon mapping, a combination of these three would probably be the ideal solution, which could handle 99.9% of lighting situations in a robust and efficient manner. The stochastic progressive photon mapping algorithm (SPPM), invented by Toshiya Hachisuka and Henrik Wann Jensen is ideally suited for GPU adaptation: it's progressive, consumes very little memory compared to normal photon mapping and can render effects like DOF and motion blur (and of course caustics). In fact there already is a working downloadable GPU version of it (not CUDA, but GLSL): available at http://graphics.ucsd.edu/~toshiya/gpusppm.zip, which hits 40 million photons per second on a HD4870. SPPM is also not biased in the way that photon mapping is, but it's more similar to unbiased algorithms: because SPPM is progressive, it will "eventually" converge to the correct solution (just like path tracing, bidirectional path tracing and Metropolis light transport).

Returning to the Design Garage demo, I can't wait to see what they're cooking for Fermi2/GTX500.

## No comments:

Post a Comment