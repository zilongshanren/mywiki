---
title: Video of Octane Render rendering in real-time on 8x GTX580s
url: http://raytracey.blogspot.com/2011/09/video-of-octane-render-rendering-in.html
author: Sam Lapere
published: '2011-09-12'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I just saw a very impressive video on Youtube, showing real-time rendering of a complex interior scene with Octane Render using eight GTX 580s. Octane Render has very recently improved its "direct lighting/AO" kernel which includes a new ambient occlusion preset and a diffuse indirect lighting option (there are now separate sliders for specular, glossy and diffuse path depth and a slider for AO distance) so that it is now capable of rendering very realistic looking interior scenes extremely fast:

Screengrab from Youtube:

Some observations:

- in contrast to the type of scenes that is usually used to show off unbiased renderers (wide open outdoor scenes with shiny cars and lots of direct lighting from a skydome or sun/sky) this is an interior scene that is mostly lit by indirect lighting with many glossy surfaces

- the scene in the video contains more than 1.3 million triangles

- rendered at very high resolution (1500x1000 pixels)

- perfect scaling with number of GPUs (99-100% extra performance per additional GPU)

- while navigating through the scene, the image remains remarkably clear and recognizable without ever degenerating into a pixelated mess of big, blocky (and often black) pixels

- convergence to a noise-free image is extremely quick

It's not hard to imagine that this renderer will be truly real-time with the upcoming generation of GPUs (according to Nvidia, Kepler will be more than twice as fast at path tracing as Fermi, just like Fermi is 2-4x as fast as Tesla (GT200) thanks to caches and other improvements (see


UPDATE: another interior animation rendered on a Nvidia GTX 590 with Octane Render's new indirect diffuse lighting/AO kernel:

Rendertime per frame: ~1 minute, 1024 samples per pixel (see screenshot in


[http://www.youtube.com/watch?v=0IC2NIogWR4](http://www.youtube.com/watch?v=0IC2NIogWR4)) and AMD's Graphics Core Next will be much more focused on GPGPU computing than previous architectures). These graphics can be rendered noise-free in real-time at high resolution with techniques like adaptive sampling, image reconstruction,[compressed sensing](http://www.ece.unm.edu/%7Epsen/Papers/TVCG11_CompressiveRendering.pdf)(a hot topic in medical imaging currently), edge-aware filtering of indirect lighting (e.g. the a-trous wavelet noise filter), extraction of spatiotemporal coherence with reprojection, path regeneration, reusing samples with frame averaging and frameless rendering. Rendering complex, 100% photorealistic scenes in real-time is much closer than commonly believed and cloud rendering will play a key role in accelerating this process.UPDATE: another interior animation rendered on a Nvidia GTX 590 with Octane Render's new indirect diffuse lighting/AO kernel:

[http://www.youtube.com/watch?v=O2Aufjr44g4Hi](http://www.youtube.com/watch?v=O2Aufjr44g4Hi)Rendertime per frame: ~1 minute, 1024 samples per pixel (see screenshot in

## 3 comments:

Do you know about Octane Render Power Tools? It allows realtime animation in Octane, and with such a setup of GPUs it could be a blast! Check it on http://www.OctanePowerTools.com or the YouTube channel YouTube.com/OctanePowerTools

Yes, I know about Octane Power tools and something tells me you are the guy that created it right?


It looks very useful but a bit too expensive compared to the current price of Octane Render itself (62€ for the powertools vs 100€ for Octane)

Nope I'm not the creator, but I very much respect him and his work, one thing because of saving me and our company a lot of time on rendering using it. Another thing the great support we got from him.

Honestly I dint get any support like this for a software before. He might be doing so to get popularity? Maybe, but it doesn't matter to the client as long as he stays so.

The price thing s not an issue, if you think about it, we purchased GPUs and systems with hundreds and thousands of $ to make octane work, even so we only payed 100$ for octane itself!

So it should not be relative to the main software price, it's relative to the value of what you are paying for.

By the way, they have a light version for 20$ now, but I recommend the full version, we purchased 5 full versions and the cameras rendering list and light animation are so valuable for any project, which the light version lacks.

Post a Comment