---
title: Unbiased Stunt Racer in HD!
url: http://raytracey.blogspot.com/2011/09/unbiased-stunt-racer-in-hd.html
author: Sam Lapere
published: '2011-09-07'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I've changed the

['Unbiased Stunt Racer' demo](http://raytracey.blogspot.com/2011/09/unbiased-stunt-racer.html)a little bit: I've added the buildings from my Futuristic Buildings demo to the scene and also added a function to adjust the speed of the physics simulation at runtime with the N and M keys. The platform and sphere are also moving at a speed that's independent of the framerate, so the game is still playable on high-end cards like the GTX 480 and higher. The new executable contains 480p and 720p executables. I find it mindblowing that real-time path tracing is feasable today at HD resolutions using only one GPU.Below is a 720p image of the new demo, rendered on a 8600M GT at 8 samples per pixel:






A video will follow soon and the source code will also be uploaded. The code is very messy with lots of obsolete comments and there are heaps of global variables, which isn't good programming practice but it does the job. :)

**The executable "Unbiased Stunt Racer HD Final" is available at**

[http://code.google.com/p/tokap-the-once-known-as-pong/downloads/list](http://code.google.com/p/tokap-the-once-known-as-pong/downloads/list)This will be one of my last demos involving only spheres and boxes as primitives. The limitations on the number of objects and shapes are starting to outweigh the benefits of these cheap-to-intersect primitives, so I'm moving to the wonderful world of triangles and BVHs soon.

![](../../assets/3ae88e74fd93d38f.jpg)


![](../../assets/3ae88e74fd93d38f.jpg)

UPDATE 3: Finally found some time to make an HD video of Unbiased Stunt Racer HD:

720p "fly-through":

480p gameplay:

Executable and source can be found at





There is also a new paper and video on reducing Monte Carlo rendering noise called "Random parameter filtering" with amazing results (thanks to ompf.org forum):


[http://code.google.com/p/tokap-the-once-known-as-pong/downloads/list](http://code.google.com/p/tokap-the-once-known-as-pong/downloads/list)![](../../assets/ae4b49e9677b370d.png)

![](../../assets/ae4b49e9677b370d.png)

![](../../assets/f657ddd6b77364a9.png)

![](../../assets/f657ddd6b77364a9.png)

There is also a new paper and video on reducing Monte Carlo rendering noise called "Random parameter filtering" with amazing results (thanks to ompf.org forum):

## No comments:

Post a Comment