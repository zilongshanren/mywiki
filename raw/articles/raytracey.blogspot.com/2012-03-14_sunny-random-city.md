---
title: Sunny Random City
url: http://raytracey.blogspot.com/2012/03/sunny-random-city.html
author: Sam Lapere
published: '2012-03-14'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

New test with the most recent Brigade 2 code, this time a scene with an animated sun over a moderately complex city scene (136k triangles), path traced at 24 spp per frame and 60 fps on 2 GTX 580s.

Video (running at 50 fps, 60fps without Fraps):

[http://www.youtube.com/watch?v=-p47t0IaT2o](http://www.youtube.com/watch?v=-p47t0IaT2o)

Screenshots:

It's not clear from the video, but seeing the diffuse color bleeding from the ground onto the buildings get stronger while the shadows are moving is a real joy to behold:

Brigade allows real-time dynamic global illumination in a scene with the quality of a precomputed lightmap on static

__and__dynamic objects and at the same time also does glossy and perfectly specular reflections. Even though I'm seeing it on my own machine, it's still hard for me to believe that this is possible today. And this is just the beginning, imagine an open world game like Riven with this tech.
## 3 comments:

Very cool! How are you doing the sun? It looks like an image but its moving...


I can totally see a Riven or Myst style game with Brigade. Though simple environmental level from that style of game would be enough to show that it works.

are these 100% lambertian diffuse surfaces?

anon1: the sun is not an image but a bunch of saturated "skysamples", which radius can be adjusted.



Riven in real-time with superb looking GI is totally doable. I'm working on a more complex game-like scene with moving sun as a proof of concept.

Anon2: Yes, buildings and floor are perfectly Lambertian (except for one small building which is partially glossy) and the windows are perfectly specular. Max path depth is 8.

Post a Comment