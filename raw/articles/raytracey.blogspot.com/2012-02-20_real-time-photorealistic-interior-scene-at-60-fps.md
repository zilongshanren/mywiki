---
title: Real-time photorealistic interior scene at 60 fps
url: http://raytracey.blogspot.com/2012/02/real-time-photorealistic-interior-scene_20.html
author: Sam Lapere
published: '2012-02-20'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

My last youtube video got 9 likes, which is three times the usual number, so I must be doing something right I guess. Some people also asked me to make a video without motion blur (frame averaging), to see how much this would affect the image quality. For your entertainment, I made a lower res video at 60 fps (it actually ran at 70 fps, but the FRAPS video capturing steals some frames and is capped at 60 fps), in which I'm toggling the blur on and off (see the yellow BLUR stat on the left):

As you can see, noise is more apparent in shadows, glass and glossy surfaces when there is no blurring.

Real-time image quality at

__:__**38-39 frames per second**
Without blur (16 spp):

With blur (16 spp with frame averaging and stationary camera):

Converged (after 2 seconds):

The last version of Brigade 2 that the developers sent me is so fast it's not even funny anymore. Below is a screenshot of a new demo that I'm working on called "Random City" showing Brigade 2 can easily break 60 fps at 16 spp on 2 high end GPUs (

__221 million random samples per second!__). Videos will follow soon after I've added some random stuff like cars and trees.
Random City WIP screenshot (rendered at 16 spp with frame averaging,



__64 fps__):
## 5 comments:

Thank you! Now i can see, even though blur is so annoying, its still better than without it.

64 fps!?! that's, wow.. It seems that you have full control of the frame averaging, can you try to switch it of if the camera moves more than 5 degrees, I'm thinking it might be the best of 2 worlds. I know I have seen a paper+video that has a post process that goes beyond frame averaging. Anyone know/remember it, that would be awesome to see in brigade :) keep up the nice videos, btw what are you working on currently? other than kick ass demos & videos

Vojtech: yep, the blur covers up a lot of noise. I will leave it in until better ways to reduce the noise without affecting performance are found.



PaulUsul, you know I was thinking the exact same thing today: use the blur only when the camera is stationary or moving forward/backwards and turn it down relative to camera rotation. I'll try that out tomorrow. There are a lot of demos that I'm working on simultaneously at the moment: an animated character demo, an archviz interior scene with very difficult lighting setup, an open world city, a quake3 like fps, a new GUI, ...

Everything else is a secret for now, I might eventually blog about it at some point ;-)

I'd say the motion blur is the only thing standing in the way of real-time jaw-dropping beauty.



One thing you could try is to offset the previous frame based on the camera rotation, so that it lines up with the current frame and doesn't cause "ghosting". Crytek does this for applying Temporal Anti-Aliasing to distant scenery in Crysis 2. Doesn't really help with moving objects unfortunately, unless you want to get a depth buffer and calculate a bunch of parabolic warps >_<

Also, dropping back to a spatial blur whenever there is no sample from the previous frame, or if the samples vary too much(e.g. when the car is moving) may help as well.

Thanks for the helpful suggestions. Making the blur less objectionable is on the do list, but first I want to try some new scenes/demos.

Post a Comment