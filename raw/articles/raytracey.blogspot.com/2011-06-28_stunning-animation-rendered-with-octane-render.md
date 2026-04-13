---
title: Stunning animation rendered with Octane Render
url: http://raytracey.blogspot.com/2011/06/stunning-animation-rendered-with-octane.html
author: Sam Lapere
published: '2011-06-28'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Just saw this very impressive video on the




The whole scene is 3D. Rendertime was two minutes per frame on average on a single GTX480, so eight of these GPUs rendering simultaneously would reduce the rendertime to just 15 seconds per frame (rendertimes in Octane scale almost linearly with the number of GPUs), which is just completely nuts considering the quality.


[Octane forum](http://www.octanerender.com/forum/viewtopic.php?f=5&t=7077)today and thought it deserved its own post (the level of realism is otherworldly):[http://vimeo.com/25686881](http://vimeo.com/25686881)The whole scene is 3D. Rendertime was two minutes per frame on average on a single GTX480, so eight of these GPUs rendering simultaneously would reduce the rendertime to just 15 seconds per frame (rendertimes in Octane scale almost linearly with the number of GPUs), which is just completely nuts considering the quality.

## 4 comments:

It is not a real time? Is it possible with particular hardware in real time?

If by "real-time" you mean 25 frames per second at the quality and resolution in this video, I don't think that's possible yet, unless you have a huge GPU renderfarm with 3000 GTX480s. But I think that sub-second rendertimes at preview quality (f.e. 100 samples/frame) and at 1/4 the resolution of this video are entirely possible on a server with 8 high-end GPUs.

Thank you for your answer. Do you know any research project for high resolution real time (25 fps) ray tracer? It is very interesting!

If you're looking for research projects that only do basic ray tracing (Whitted-style ray tracing), there are plenty: google Arauna (from Jacco Bikker) and the games that are made with it (such as "Let there be Light" and "Outbound"), Daniel Pohl from Intel has made some raytraced versions of famous id games (Quake 3, Quake Wars, Wolfenstein, ...), there's also AntiPlanet Reflections, Elite Force raytraced (search "stereo1984" on Youtube). They all run on the CPU only (except AntiPlanet) at pretty high resolutions and framerates. Shading is still very basic though and cannot rival today's rasterized games.



If you mean 'path tracing' (highly incoherent ray tracing with advanced effects like high quality global illumination), that's a totally different story: the GPU has dramatically evolved over the past few years (unified shaders, massive parallelism and general programming APIs like CUDA) so that it now greatly outperforms the CPU at path tracing, but we are still not at the point where you can have 25 fps at decent image quality and decent resolution on a single GPU, except my own path tracing demos of course ;-) which use simple geometric primitives for faster intersection and optimized path tracer code (from tbp's tokaspt in the case of "Tokap Arcade Madness" http://www.youtube.com/watch?v=NcyEXBXYwUY, and from Jacco Bikker and Jeroen van Schijndel in the case of "Kajiya Unbiased Truck" http://www.youtube.com/watch?v=kddh26mKZHc (original path tracer: http://www.youtube.com/watch?v=OHWxsUUataw)).

The closest is probably the Brigade path tracer (also from Jacco Bikker), which is aimed at real-time games (search for "Minecraft Brigade path tracing"). Then you also have the really high quality GPU renderers like Octane, iray, Cycles, Arion, SmallLuxGPU, V-Ray GPU from which Octane easily beats the others in speed, quality and features. They are not real-time yet (i.e. sufficiently converged image quality at 25 fps), but you should definitely check out some videos like this one: http://www.youtube.com/watch?v=6QNyI_ZMZjI

Post a Comment