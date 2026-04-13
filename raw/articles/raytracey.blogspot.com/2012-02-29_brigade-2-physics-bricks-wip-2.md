---
title: Brigade 2 Physics Bricks WIP 2
url: http://raytracey.blogspot.com/2012/02/brigade-2-physics-bricks-wip-2.html
author: Sam Lapere
published: '2012-02-29'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I've altered some things in the scene to look more like the original video (

[http://www.youtube.com/watch?v=bSQoJW9ajmU](http://www.youtube.com/watch?v=bSQoJW9ajmU)), such as materials, floor texture, and lighting. The scene is now lit by the sky and by an area light floating above the brick tower. I've also implemented shooting physics for the orange ball, which can be shot from any camera view.Real-time rendered recreation of the scene in Brigade 2:

The number of dynamic bricks is reduced to maintain a high framerate and because the physics become increasingly twitchy with more moving objects. I'm quite happy with the result so far, as it shows that in simple scenes Brigade 2 can achieve the same photorealistic quality in materials and lighting as an offline unbiased renderer (in this case LuxRender's SmallLuxGPU), but in real-time and with real-time physics and moving objects.

I've also made a fly-through video of Random City, which is another real-time path traced WIP demo that I'm working on:

[http://www.youtube.com/watch?v=VUoXmsu-7bg](http://www.youtube.com/watch?v=VUoXmsu-7bg)

## 2 comments:

Beautiful! Is it safe to assume that a noise free image @ 30fps will be possible once Jacco implements bidirectional path tracing and noise filtering?




The first brigade video doesn't suffer from camera blur as the city video, is this because of frame averaging was used or the case of slow frame rate?

Keep releasing the videos, they are inspiring!

Thanks for the comment!



Noise filtering will certainly help, bidir PT on the other hand will not do much in open well-lit scenes (where it would actually make performance worse), but it might make a big difference in indoors with lots of indirect lighting. With filtering and other optimizations, a noisefree image at 30 fps is attainable.

The second video looks more blurry because of the lower framerate and because I also used a higher amount of blur. The framerate is currently also heavily dependent on the number of dynamic objects, e.g. I'm getting 80 fps with 20 physically animated bricks (which contain only 12 triangles/brick), but just 25 fps with 120 bricks.

Post a Comment