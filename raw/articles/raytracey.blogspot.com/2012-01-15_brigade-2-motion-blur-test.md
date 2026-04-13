---
title: Brigade 2 motion blur test
url: http://raytracey.blogspot.com/2012/01/brigade-2-motion-blur-test.html
author: Sam Lapere
published: '2012-01-15'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Today I've added cheap camera motion blur to the Brigade 2 path tracer using the OpenGL accumulation buffer. The technique blends the pixels of one or more previous frames with the current frame and works very well for real-time path traced dynamic scenes, provided the framerate is sufficiently high (10+ fps). The difference in image quality is huge: path tracing noise is drastically reduced and since all calculations pertaining to the accumulation buffer are hardware accelerated on the GPU, there is zero impact on the rendering performance. Depending on the accumulation value, you essentially get two to ten times the amount of samples per pixel for free at the expense of slight blurring caused by the frame averaging (the blurring is actually not so bad because it adds a nice cinematic effect).

Below is a comparison image of a stress test of an indoor scene without and with motion blur applied (rendered on 8600M GT). The images were rendered with multiple importance sampling using

__only 1 sample per pixel__to better show the differences (converging is off):
Comparison of the scene with the rotating ogre from a previous demo (see

[http://raytracey.blogspot.com/2011/12/videos-and-executable-demo-of-brigade-2.html](http://raytracey.blogspot.com/2011/12/videos-and-executable-demo-of-brigade-2.html)) rendered at 1 sample per pixel (on a 8600M GT), with (right) and without motion blur:
The following image has nothing to do with frame averaging but it is an image from an earlier test of the MIS indoor scene with a highly detailed Alyx character (40k triangles) with a Blinn shader applied. It rendered very fast:

I'll upload some videos of the above tests soon.

## 8 comments:

Nice!

nice!

thank you for this blog!


I have a question: Is the averaging done after or before gamma correction? I read somewhere that it looks more realistic if the smoothing is done before gamma correction is applied.

I'm really not a fan of motion blur as for the most part it's overdone and makes me feel car sick but the results are stunning! Also the blinn looks amazing :) look forward to seeing the videos

@ Anonymous: the frame averaging happens after gamma correction, just before the buffers are swapped. At very low samplerates (1-4 spp), there is a slight reduction in brightness in interiors, because paths that don't hit a lightsource return a black pixel, which gets blended in subsequent frames. Doing some gammma correction afterwards could probably solve this.




Paul, for the time being the motion blur technique is a necessary evil to reduce the noise to acceptable levels when doing path tracing in real-time. It's not the best solution, but it certainly isn't the worst either. In motion it looks quite good and you can reuse lots of expensive samples from previous frames :-)

Also, the higher the framerate, the better it looks. You can go to extremes and render at very low samplerates (1-2 spp) to achieve a high framerate and it will still look like a 20 spp frame. There are some recent filtering techniques such as à-trous wavelet and random parameter filtering, which have the disadvantage of blurring fine geometric and texture details and being useful only for diffuse and moderately glossy surfaces (they are also quite expensive to compute). The camera motion blur however does not affect the performance at all and completely preserves all the details, which I think is very important.

Yep, the blinn is awesome :-)

Maybe figure out what part of the screen is updating and motion blur the almost static parts more? (And maybe prioritize the updating part with tracing).

I thought about this as well, it's in fact a well known technique called "adaptive sampling" which focuses more samples on regions that have the most variance (noise), but it's actually quite costly to determine those regions. You could also start caching indirect lighting but that defeats the purpose of a completely dynamic scene and would make dynamic lighting impossible. I could use a more sophisticated method of calculating motion blur, which includes motion vectors for each object. It is in fact used in Crysis ("object motion blur"), maybe it's worth exploring this idea.

Post a Comment