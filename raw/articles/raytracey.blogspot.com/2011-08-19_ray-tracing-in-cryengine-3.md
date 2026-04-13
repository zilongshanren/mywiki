---
title: Ray tracing in CryEngine 3!
url: http://raytracey.blogspot.com/2011/08/ray-tracing-in-cryengine-3.html
author: Sam Lapere
published: '2011-08-19'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Crytek has pioneered a lot of well known rendering techniques like screen space ambient occlusion and light propagation volumes for real-time dynamic global illumination. Proving that they're still at the forefront of real-time rendering, Crytek revealed at Siggraph that they are using a limited form of ray tracing in CryEngine 3 to enable real-time local reflections. The technique involves screen space ray marching along the direction of the reflection vector. More info about this method and lots of other interesting details in their Siggraph presentation at


It's nice to see that ray tracing is finally being used by a leading game developer (without a doubt the most talented PC game engine developer of the moment), albeit in a limited form. If SSAO is any indication, we'll be seeing ray tracing based reflections in all of the other major game engines within the next year. From there, it's only a small step to use full ray tracing for reflections, shadows, refractions and ultimately global illumination. :)


[http://advances.realtimerendering.com/s2011/index.html](http://advances.realtimerendering.com/s2011/index.html)It's nice to see that ray tracing is finally being used by a leading game developer (without a doubt the most talented PC game engine developer of the moment), albeit in a limited form. If SSAO is any indication, we'll be seeing ray tracing based reflections in all of the other major game engines within the next year. From there, it's only a small step to use full ray tracing for reflections, shadows, refractions and ultimately global illumination. :)

## 5 comments:

I believe that the Unreal Engine 3 uses a form of ray tracing to render reflections of complex light sources (i.e. neon signs...) in their Samaritan demo. As I recall, they render each light source into a billboard, and then raytrace the reflection ray against those, while doing screen space ray marching to properly occlude the billboard reflection.

I looked it up and you are right. I found a technical powerpoint presentation from Epic about the Samaritan demo (http://www.nvidia.com/content/PDF/GDC2011/Epic.pdf) Epic does ray tracing for "billboard reflections" in a similar way as Crytek's solution . Thanks for this. That makes two top level game engines using ray tracing :)

In fact this kind of ray-tracing is quite common : Refractive object (ray marching in depth buffer), relief mapping (ray marching in height texture), ... and all those techniques are implemented in several games :)

Interesting, thanks. I didn't know how refraction was performed in a rasterization context. But I did know that relief mapping (or parallax mapping) uses raymarching.


This new local reflection technique just shows that ray tracing will be used more and more in games. I think shadows and ambient occlusion will be next, they are perfect candidates.

Thanks for sharing your info. I really appreciate your efforts and I will be waiting for your further write ups thanks once again.

html5 converter

Post a Comment