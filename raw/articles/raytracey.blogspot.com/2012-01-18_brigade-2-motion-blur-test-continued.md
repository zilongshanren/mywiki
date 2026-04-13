---
title: Brigade 2 motion blur test continued
url: http://raytracey.blogspot.com/2012/01/brigade-2-motion-blur-test-continued.html
author: Sam Lapere
published: '2012-01-18'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I made some side-by-side comparisons from the Utah teapot scene (

[http://www.youtube.com/watch?v=KxELvSK3Gl0](http://www.youtube.com/watch?v=KxELvSK3Gl0)) to show the difference that the motion blur technique makes in areas that are partially lit with indirect lighting. Both sides in the comparison screens use only 4 samples per pixel. The low samplerate is required to achieve playable framerates. Motion blur (frame averaging) is disabled in the left image, while the right image averages the pixels of the current frame with those of the previous 7 frames (equivalent to 32 samples per pixel). The difference in obscured regions is enormous. This is the quality that can be achieved in real-time (+10 fps) using one current high end GPU (GTX 570 or better):
Edges and shadows become much more clearly defined:

Video (low framerate, rendered at 640x480 on a GTS 450):

It's amazing what such a simple trick can do to the quality of the image, without losing any detail. My next test will involve a 3rd person car camera like the one in

## No comments:

Post a Comment