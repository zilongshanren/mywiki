---
title: Real-time photorealistic interior scene with Brigade 2
url: http://raytracey.blogspot.com/2012/02/real-time-photorealistic-interior-scene.html
author: Sam Lapere
published: '2012-02-17'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Just a simple test to show how well the latest version of Brigade runs on a system with 2 GTX 580s. The scene uses multiple importance sampling and renders extremely fast, regardless of the materials being used (Blinn, diffuse, glass and specular) or the number of reflections. The new engine is truly a joy to play with, I've tested a number of complex 3D models containing over half a million triangles and Brigade doesn't break a sweat.

The following video was rendered at 640x360 (720p screen resolution) with 16 spp per frame (15-25 fps):

Some 720p screens:

Depth of field:

Yep, path tracing has come a long way and it's finally ready for primetime!! Time for some hardcore testing :-) Stay tuned next week for a real-time path traced fly-through of Random City.

## 8 comments:

holy crap!

Hi Ray. Its awesome! Can you make a video without "motionblur"? Cant wait for city scene.

It must be the high frame rate but the motion blur really does not bother me at all in this video. Great show case!

Are you using the code drop Jeroen sent you? Looks like it, performance is as it should be now. :) Great work! The mirror room is awesome!

Amazing

It surprise me how fluid it looks.

Sure, it's rendered with two GPUs, but still.

Thanks guys.



Jacco: yep, I'm using the latest code Jeroen sent me. It's unbelievably speedy, even at higher sampling rates. Two high end GPUs are enough for a highly detailed outdoor scene at 720p/30fps.

Vojtech: without motion blur, the variance (noise) is more outspoken and jarring and it's more unpleasant to look at than a blurred image. So the blur will stay for now, until something better can replace it.

Ok. I just want to compare raw output with blured one.

Vojtech, I will post a 60 fps video of this scene tomorrow with and without blur.

Post a Comment