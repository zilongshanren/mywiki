---
title: 'Real-time path tracing: Babylonian city test'
url: http://raytracey.blogspot.com/2012/03/real-time-path-tracing-babylonian-city.html
author: Sam Lapere
published: '2012-03-26'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Real-time video,

__rendered at 1280x720 resolution__on 2 GTX 580s at ~10 fps:

[http://www.youtube.com/watch?v=Wvsnk1DewAg](http://www.youtube.com/watch?v=Wvsnk1DewAg)(watch in 720p)

UPDATE: 30 fps video with "variable" blur

UPDATE 2: At the request of my Aussie mate Radiant, I've uploaded a real-time video in 1080p Full HD (1920x1080):

[http://www.youtube.com/watch?v=1SIhLNjerNs](http://www.youtube.com/watch?v=1SIhLNjerNs)- lit by sky + sun

- 30 fps at 640x480, 10 fps at 1280x720 on 2 GPUs (faster without sun)

- brute force path tracing with max path depth 8 (maximum 7 diffuse light bounces, which is rarely attained, because most rays "escape" to the sky)

Sun disabled:

Textures disabled:

True cinema-quality lighting in real-time :-). More outdoor scenes soon.

## 11 comments:

Why the bright white lines in the "No sun" version?

Those are due to a reversed normal in the original model. The SketchUp model contained some surfaces with normals that were facing the wrong way, I cleaned up most of them, but apparently missed one. I saw it after exporting it to obj and loading it into Brigade.

How is the blur being varied?

The blur depends on the amount of rotation of the camera, it's smoothly toned down according to the delta of the mouse motion relative to the previous frame. So if the camera turns fast or strafes sideways, there is less blur and when it is stationary, moving forward or backwards there's more. This is a bit counterintuitive, but it works well for path tracing.

That 'variable blur' is a very nice idea. - Jacco.

Thanks Jacco, it's an idea that I had for quite some time (finally implemented it yesterday).

WOW, this blur technique is magnificent.




~Is it possible to post a 1980x1080 version?

~Is there any record of it running at 30 or 20 FPS?

~Is your team ;) looking into out of the core methods, there was a paper back called centilo i think which uses the computer ram (as big as 32 gigs) but still utilizing the GPU for rendering???

Cheers,

Michael ~Radiant

Hi radiant,




- 1080p is possible, but the upload will take a while. The blurring will be more noticeable, because the framerate is about 5 fps.

- I've uploade a 30 fps video here: http://www.youtube.com/watch?v=EeQvfBL6A4k

- the focus is on in-core scenes currently, but out-of-core rendering is very interesting indeed ;) CentiLeo is a fantastic example

radiant, I updated my post with a 1080p video :)

Wow cheers sam :D.

The video looks even better.

Cant wait to see what this baby can do, once it tackles a crysis like level.

It should do really well on Crysis levels, in fact I'm searching for a highly detailed outdoor game level (in the range of 1 - 2 M polygons), I'm convinced that Brigade can pull it off.

Post a Comment