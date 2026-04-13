---
title: 'Real-time path tracing of animated meshes on the GPU (2): OGRE'
url: http://raytracey.blogspot.com/2011/10/real-time-path-tracing-of-animated.html
author: Sam Lapere
published: '2011-10-18'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

![](../../assets/c540f3ae8fa98b1f.png)


![](../../assets/c540f3ae8fa98b1f.png)

Another test in my never relenting quest for real-time photorealistic graphics. This time I was inspired by one of the first animations rendered with unbiased Monte Carlo path tracing. The animation was made by Daniel Martinez Lara from [Pepeland](http://www.pepeland.com/) in 1999 and can be seen here:

It’s one of the first animations that uses Arnold, the Monte Carlo path tracing based production renderer developed by Marcos Fajardo, that is currently taking Hollywood VFX by storm: it was used in e.g. Cloudy with a Chance of Meatballs, 2012, Alice in Wonderland and the Assassin’s Creed: Brotherhood and Revelations CG trailers and is giving PRMan and mental ray a run for their money (probably making them obsolete soon, mainly because of ease of use and huge artist time savings). The animation shows a very lifelike clay figure coming to life. Despite the simplicity of the scene, the whole looks very believable thanks to physically accurate global illumination and materials and an extensive use of depth-of-field and camera shake.

In an attempt to reproduce that particular scene, I’ve used the animated Ogre model from a ray tracing demo developed by Javor Kalojanov which can be found at [http://javor.tech.officelive.com/tmp.aspx](http://javor.tech.officelive.com/tmp.aspx). The Ogre model (which was created by William Vaughan) consists of 50,855 triangles and was also used in the excellent paper “[Two-level grids for ray tracing on GPUs](http://www.intel-vci.uni-saarland.de/fileadmin/grafik_uploads/publications/59.pdf)” by Javor Kalojanov and Philipp Slusallek (really great people btw, whom I've had the pleasure to meet in person recently. The conversations I've had with them inspired me to finally try triangles as primitive for my real-time path tracing experiments (instead of just spheres), which led to this Ogre demo. To my surprise, triangle meshes are not that much slower to intersect compared to spheres. I think this is due to the fact that the cost of primitive intersection is becoming increasingly smaller compared to the cost of shading).

The following videos show an animated Ogre path traced in real-time with real-time, per frame update of the acceleration structure of the Ogre’s 50k triangle mesh (watch in 480p):

[http://www.youtube.com/watch?v=u0a0mPR8jdM](http://www.youtube.com/watch?v=u0a0mPR8jdM)

Path tracing is performed entirely on the GPU, in this case a GTS 450 (a low-end GPU by today’s standards). The framerate of the walk animation is about 4 fps max on my card but should be around 15-20 fps on a GTX 580. The image converges extremely fast to a very high quality result (in about 1-2 seconds). The movement of the Ogre (translation, rotation, animation) is actually much more fluid in real life without Fraps, the overhead of the video capturing software almost halfs performance.

The images below were each rendered at 20 samples per pixel in under 2 seconds on a GTS 450 (it would take less then 0.5 seconds on a GTX 580):

Note the very subtle color bleeding from the ground plane onto the Ogre:![](../../assets/049eb33496b19800.png)

![](../../assets/4598e611f243520a.png)


If you’re interested in trying this scene out yourself, send me an e-mail at sam [dot] lapere [at] live [dot] be. A CUDA enabled GPU is required (minimum compute capability 1.1).

I’m planning to build a (very) simple game with this tech. The possibilities are really endless. We're on the cusp of having truly photorealistic games.

## No comments:

Post a Comment