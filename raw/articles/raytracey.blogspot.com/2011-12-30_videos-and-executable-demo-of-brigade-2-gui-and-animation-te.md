---
title: Videos and executable demo of Brigade 2 GUI and animation test
url: http://raytracey.blogspot.com/2011/12/videos-and-executable-demo-of-brigade-2.html
author: Sam Lapere
published: '2011-12-30'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Some videos of the GUI that I developed for Brigade 2, showing real-time changing of materials with simultaneous animation and physics simulation. The GUI is still a work in progress, but being able to tweak any material on the fly is so much more easy to get the look right.

480p (320x240 render res, 4 spp, max depth 4)

480p (640x480 render res, 4 spp, max depth 4)

The Ogre (model from

[here](http://javor.tech.officelive.com/tmp.aspx)) is just simply rotating for now. The mesh consists of 51k triangles of which the BVH is dynamically updated every frame (as are the BVHs of the car and the stack of blocks which are physics driven).
The executable demo is available at

[http://code.google.com/p/tokap-the-once-known-as-pong/downloads/list](http://code.google.com/p/tokap-the-once-known-as-pong/downloads/list)

(all CUDA architectures supported)

Further experiments will include:

- skeletal animation

- first person camera and gun

- cam following the vehicle

- architecture

## No comments:

Post a Comment