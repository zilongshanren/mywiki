---
title: Physics tests in Brigade 2
url: http://raytracey.blogspot.com/2011/12/physics-tests-in-brigade-2.html
author: Sam Lapere
published: '2011-12-14'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Jeroen van Schijndel, one of the developers of the Brigade path tracer, has posted a cool video showing off the physics inside Brigade:

During the last several days, I have been working on implementing vehicle physics in a new simple demo that uses the Brigade 2 path tracer. The scene in the demo is only lit by a sky texture and consists of a vehicle with mass, a few perfectly specular containers and a stack of boxes (more than 2800 triangles in total). The maximum path depth is 4 to make the reflections more interesting.

The following screenshots and videos were all rendered in real-time on a mobile GPU, the 8600M GT, which is extremely low-end by today's standards and is about 30 times slower than a GTX 580. Nevertheless, despite its very low "CUDA core" count and clocks, it can still produce some pretty amazing footage, path-traced in real-time at 4 samples per pixel and a max path depth of 4 (allowing for reflections of reflections). Better videos with much higher framerate (captured on a GTS 450) will follow soon.

Somewhat better quality, but lower framerate



Glossy floor, 4 spp

Some ideas that I want to work on next:

- frame averaging, which greatly reduces the noise at the expense of slight blurring

- a camera that follows the vehicle automatically

- a first-person gun which can shoot projectiles with physical mass

- (low-poly) animated enemies (with cheap-to-update BVH)

- investigate the use of bump mapping to further increase realism (Dade's

[Sfera](http://www.youtube.com/watch?v=Dh9uWYaiP3s)demo has shown that bump mapped surfaces converge almost as fast as non-bump mapped ones)- more interesting scenes, using a greater variety of materials (Brigade supports diffuse, glass, glossy and perfectly specular) and textures. I'm still aiming to replicate

[this path traced animation](http://www.youtube.com/watch?v=yPU6xNNCE68)in real-timeThe Brigade 2 path tracer is just great fun to play with and the speed and quality in a well-lit environment (on a high end GPU) are truly amazing. Seeing a real-time animated character with perfectly photoreal lighting while orbiting the camera around it is so damn rewarding...

## No comments:

Post a Comment