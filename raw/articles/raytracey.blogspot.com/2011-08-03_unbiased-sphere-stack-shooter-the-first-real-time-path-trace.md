---
title: Unbiased Sphere Stack Shooter, the first real-time path traced shooter
url: http://raytracey.blogspot.com/2011/08/first-real-time-path-traced-shooter.html
author: Sam Lapere
published: '2011-08-03'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

![](../../assets/dcb3d63e2a7b0ce0.png)


![](../../assets/dcb3d63e2a7b0ce0.png)

![](../../assets/270d70f736d19329.png)


![](../../assets/270d70f736d19329.png)

![](../../assets/06d64a06ecf491f9.png)


![](../../assets/06d64a06ecf491f9.png)

![](../../assets/1409dcd060a7365f.png)


![](../../assets/1409dcd060a7365f.png)

**Features:**

-

**real-time path traced graphics on the GPU:**produces ultra-high quality physically accurate global illumination, soft shadows and reflections-

**integration of the Bullet physics engine:**start/pause the physics simulation by pressing 'm'-

**first person camera:**move forward, backwards and sideways with the arrow keys-

**mouse look:**click and hold the left mouse button to look around the scene (already working, but needs a bit more work to make it more robust)-

**shooting mechanics:**fire a ball into the stack or try hitting a bouncing sphere by pressing 'Enter'. The ball is shot from the current camera position at the current view target in the center of the screen. Due to performance reasons, only one ball is shot at a time (the same ball is 'recycled' with every shot).Make the physics go berserk!

Video rendered on 8600M GT (a better quality video on GTS 450 will follow soon):

## 10 comments:

cant believe i spend 15 minutes on this XD.


It would be uber awesome if you could have unlimited or x amount of firing balls :D

Well spent 15 minutes! :D


I have tried implementing more firing balls, but the performance crawls to a slow on my tiny laptop after firing 20 balls or so (both because of GPU path tracing and CPU physics calculations). So there's only one ball to keep the framerate constant. Maybe I will make a version where you can fire 8 consecutive balls, it should still run pretty fast on a GTX580.

I am using a 8600M GT too. But don't know why my framerate is so much lower than your video :(

That's because in order to get an acceptable framerate (~17 fps) for making the video, I have resized the window from 768x512 to 512x256 (just drag the lower right corner with the mouse) and the max path length was set to 3.

Isn't that sci-fi FPS demo from a few months back the first real-time path traced shooter?

I think you mean the Reflect game that is running on the Brigade engine? It's not really a shooter afaik. Even if it has laser guns and a portal gun, it doesn't fire projectiles. I haven't played it (still waiting on a binary release), so I can't tell for sure.

I see. Thanks. Will try to run at lower resolution.




By the way, I just discovered your blog recently. I am really amazed at how you got into graphics rendering. A complete non-programmer spending 6 months learning C++ and global illumination theory in order to enjoy the beauty of photo-realism. I guess you must come from a Math/Science/Engineering background at least.

I really share your enthusiasm for this field, as I was also how I became addicted to it.

Keep posting. I will visit this place often. :)

Thanks for the great comment!




I actually really started learning C++ programming just two months ago. I'm learning mostly by analyzing open source code and by trial and error.

My background is actually in the medical field, but I have always had a very strong interest in computer graphics (it all started with Toy Story 1, Jurassic Park, Terminator 2 and the Matrix movies) and I wanted to see that same photoreal quality in a video game. Hence my fascination with real-time path tracing :)

I have been interested in ray tracing and real-time global illumination since 2004 and I have read almost every relevant paper in the field of real-time ray tracing and real-time GI, instant radiosity, GPU photon mapping and path tracing (Siggraph, HPG, EGSR, Pacific Graphics)out of pure interest.

I have quite some C++ experience, how can I compile it for Linux?



Cheers,

Ps. I got a 470 GTX

You need to download the CUDA toolkit and developer drivers for Linux at http://developer.nvidia.com/cuda-toolkit-40 before you can compile the code. Mail me if you have any problems compiling the code.

Post a Comment