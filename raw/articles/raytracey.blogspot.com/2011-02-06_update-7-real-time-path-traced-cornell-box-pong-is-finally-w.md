---
title: 'Update 7: Real-time path traced Cornell Box Pong is finally working!!! Source
  and Exe available!'
url: http://raytracey.blogspot.com/2011/02/update-7-on-cornell-box-pong-its.html
author: Sam Lapere
published: '2011-02-06'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Major update!!! Thanks to the awesome help of Kerrash, a coder with OpenGL and CUDA experience, I can finally present a working version of Cornell Box Pong, which has now been renamed to "The once known as Pong" (Tokap for short as a tribute to

[tokaspt](http://code.google.com/p/tokaspt/), the fantastic GPU raytracer it's based upon).All of the changes to the tokaspt source code in Tokap are 100% the work of Kerrash, for which I'm eternally grateful. I just provided him with the scene. The Pong ball now bounces for real, and there is user interaction with both of the paddles, or with just one paddle while the other is controlled by a basic AI routine. The game also features motion blur, which can be disabled in the source code (In the 'tokaspt.cc' file search for a value called 'BLUR_AMOUNT'. This number tells the engine how many frames to wait before completely throwing away the previous pixels. Setting to '0' will cause a refresh for every frame, having no motion blur. Recompile)

**VIDEOS:**

A video of a WIP version of Tokap (where the ball is following a sine wave path, with and without motion blur), made by Kerrash on a Nvidia GTS 250:

[http://www.youtube.com/watch?v=pqUdOpJq4l0](http://www.youtube.com/watch?v=pqUdOpJq4l0)A video by Kerrash of Tokap with one AI controlled paddle, running on a Nvidia GTS 250:

[http://www.youtube.com/watch?v=9svQE79XAPI](http://www.youtube.com/watch?v=9svQE79XAPI)Youtube of the latest version running on my 8600M GT (this is the version with extremely slow ball speed, 4 samples per pixel motion blurred at 5 fps)

Youtube of tokap running on a GTX 570 (video by Anonymous from comments). Normal speed, no motion blur, 64 samples per pixel at 10 fps:

Scene interaction, 1 fps at 32 samples per pixel (motion blurred to 160 spp) on 8600M GT:

[http://www.youtube.com/embed/gYl-uYtTKSY](http://www.youtube.com/embed/gYl-uYtTKSY)

Check it out!

Replace the src folder from tokaspt with the new src folder and overwrite all files, then recompile.

You can stilll use the UI of the original tokaspt i.e. change number of samples per pixel, ray depth, size, color and emitter properties of spheres, add spheres...

32-bit Tokap AI version with 4 different ball speeds (normal, slow, very slow and extremely slow ball speed). Download this version if you don't have a very fast CUDA card.

A CUDA enabled GPU is required, Fermi is recommended but even a 8600M GT works ;-) If you have problems with compiling the code, there could be files missing from your CUDA SDK. Download

[this zip with missing CUDA files](http://www.2shared.com/file/8vJBbFfW/missing_files_from_CUDASDK.html). Try compiling with Visual Studio 2008, VS2010 was not tested. Win 64 could give problems as well. All credits for the code modifications to tokaspt go to Kerrash! The gameplay is still work in progress. I will try to integrate Box2D physics in the source code. In the meantime, enjoy!UPDATE: Anonymous posted the timings for tokap1_2_players on a GTX 580 in the comments:

8 spp: 60 fps (blurry tail)

12 spp: 44 fps (accumulator tail)

16 spp: 30 fps

20 spp: 28 fps

24 spp: 20 fps

28 spp: 20 fps

32 spp: 17 fps

"At lower spp's it seems like the motion blur is kind of working, but after 12 spp it becomes weird and looks like a poorly sampled accumulator buffer. It's playable, but noisy, at 4 spp. Still noisy at 64 spp (10 fps) but it could be mistaken for film grain (maybe). Although you can then see 5 copies of the ball trailing behind it (motion blur)"This means that the GTX580 is about 20 times faster than my 8600M GT and that Tokap is playable with high image quality at 10 fps on this card. Hopefully Nvidia or AMD will make a similar tech demo for their next-generation GPUs.

## 7 comments:

I've just had chance to capture a quick video. http://www.youtube.com/watch?v=9svQE79XAPI



I suppose the next logical step is to make 'Breakout' :) LOL

I guess I should save for a GTX580. :)

Timings for tokap1 2 players on 580 GTX. I assume spppp is some sort of 'samples per pixel' option




Default: 60 fps (blurry tail)

8 spp: 60 fps (blurry tail)

12 spp: 44 fps (accumulator tail)

16 spp: 30 fps

20 spp: 28 fps

24 spp: 20 fps

28 spp: 20 fps

32 spp: 17 fps

At lower spp's it seems like the motion blur is kind of working, but after 12 spp it becomes weird and looks like a poorly sampled accumulator buffer. It's playable, but noisy, at 4 spp.

Still noisy at 64 spp (10 fps) but it could be mistaken for film grain (maybe). Although you can then see 5 copies of the ball trailing behind it (motion blur)

Thanks for the video Kerrash!




"Breakout" has crossed my mind as well, but since tokaspt currently only supports spheres as primitives, you would have to hack the code to support AABBs or worse, triangles, which would degrade the performance.

Anonymous, thank you very much for those numbers, I was really very curious how it would perform on a 580 GTX. There is a way to disable the motion blur as described in my post. I will compile a motion-blurless version for testing.

I would have guessed that there would still be noise even at 64 spp. On the other hand, the fact that tokaspt only uses spheres for raytrace ensures very high path tracing performance.

Would you mind making a video (with the freeware fraps perhaps) at 64 spp on your GPU? You can upload it to a registration free hositng service like woofiles.com. I would very much appreciate it.

Here is a raw dump from FRAPS (lossless compression), at 64 SPP:



http://www.megaupload.com/?d=STQ0Y9K4

The accelerator card is GeForce GTX 570 @ 1650MHz shader clock-rate.

Thanks a lot Anonymous!



That's a capture of the version without motion blur right? I'll post some versions with differing speeds today, where the motion blur effect is not that prominent.

Do you mind if a post your video on youtube?

Go ahead! ;)

Anonymous, I've uploaded a zip file which contains 4 new versions with different ball speeds. The motion blur is looking less objectionable in the versions with slower ball speeds. Check it out at http://www.2shared.com/file/G-ZquSYe/tokap_different_speeds.html

Post a Comment