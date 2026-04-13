---
title: Video of Unbiased FPS + a new video of Brigade!
url: http://raytracey.blogspot.com/2011/09/video-of-unbiased-fps-new-video-of.html
author: Sam Lapere
published: '2011-09-24'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

The following two videos of "Unbiased FPS" were rendered on a GTS 450 and demonstrate mouse look, shooting mechanics and how adjusting the number of averaged frames affects the amount of noise and blurring. Youtube has a terrible video compression algorithm for videos containing fine-grained noise (such as Monte Carlo noise), so these came out much worse than expected:

The frame averaging technique (implemented by Kerrash) significantly reduces the amount of noise without affecting the framerate, but the resulting blurring of fast moving objects is of course less than ideal. At the upcoming Siggraph Asia 2011, a paper entitled "Image-space bidirectional scene reprojection" will be presented which could potentially solve the blurring issue by reconstructing additional frames without distracting blurry artefacts (there are two versions, a raster based version and an image-based one). The video accompanying the paper shows a lot of promise and is definitely worth checking out:

[http://research.microsoft.com/en-us/um/people/hoppe/proj/bireproj/](http://research.microsoft.com/en-us/um/people/hoppe/proj/bireproj/)On a sidenote, I found a new, short video of the Brigade path tracer, showing a real-time pathtraced animated character:

[http://www.youtube.com/watch?v=RbxoZK6Apj8](http://www.youtube.com/watch?v=RbxoZK6Apj8)(no details on the hardware used)The video shows very nice soft shadows and path traced ambient light coming from the skydome (calculated in real-time contrary to the constant ambient term which is used by many games to approximate indirect lighting).

## No comments:

Post a Comment