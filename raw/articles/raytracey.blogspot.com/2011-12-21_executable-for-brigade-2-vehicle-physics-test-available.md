---
title: Executable for Brigade 2 vehicle physics test available
url: http://raytracey.blogspot.com/2011/12/executable-for-brigade-2-vehicle.html
author: Sam Lapere
published: '2011-12-21'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

An executable demo of the scene in the previous post is available at




I've recompiled the cuda binaries on my laptop for every possible CUDA GPU architecture (compute capability 1.0, 1.1, 1.2, 1.3, 2.0 and 2.1). Since the binaries were not natively compiled on their respective architecture and use a fixed maxregistercount of 63, higher end GPUs like the GTX 560 and up are not used to their fullest potential (


UPDATE: Roeny (one of Brigade's developers) has posted an explanation of why the GPU is not fully loaded here:


UPDATE 2: szczyglo74 has posted a

[http://code.google.com/p/tokap-the-once-known-as-pong/downloads/list](http://code.google.com/p/tokap-the-once-known-as-pong/downloads/list)I've recompiled the cuda binaries on my laptop for every possible CUDA GPU architecture (compute capability 1.0, 1.1, 1.2, 1.3, 2.0 and 2.1). Since the binaries were not natively compiled on their respective architecture and use a fixed maxregistercount of 63, higher end GPUs like the GTX 560 and up are not used to their fullest potential (

[a member of the Beyond3D forum reports only 35% GPU load on a GTX 460 with this demo](http://forum.beyond3d.com/showpost.php?p=1607810&postcount=72)). But at least it works on all CUDA architectures :-)UPDATE: Roeny (one of Brigade's developers) has posted an explanation of why the GPU is not fully loaded here:

[http://forum.beyond3d.com/showpost.php?p=1608008&postcount=86](http://forum.beyond3d.com/showpost.php?p=1608008&postcount=86)UPDATE 2: szczyglo74 has posted a

## 6 comments:

Looks like it's sitting idle for long periods between each frame - major timing issue?


I'm not sure what you mean. What resolution are you running at? The frames only refresh when 4 samples per pixel are calculated. Depending on your GPU, this could result in framerates from 0.3 to 5 fps for 720p resolution. When nothing moves and physics are toggled off, the image converges (accumulated spp increases on the top of the screen)

Yep, got 30-40% GPU load (on any exe-file): http://img543.imageshack.us/img543/5561/runtest.jpg


But it works :)

It's hard to extract every bit of efficiency with ray tracing on a device that was build for rasterization. Hopefully some hardware ray tracing support will appear in the near future. In fact, Imagination Technologies is coming with a PowerVR GPU with Caustic ray tracing hardware in 2012 according to this: http://futuremark.yougamers.com/forum/showthread.php?t=159528


It's also in this official doc: http://www.imgtec.com/corporate/presentations/interim11/Interims-final-13-12-11.pdf

I've tested it on my workstation, res 480p 320x200

http://www.youtube.com/watch?v=0jVAwz-RGj4&feature=plcp&context=C3430684UDOEgsToPDskJT_exlHx9XQjZ6vGomixsL

Nice video, thanks!

Post a Comment