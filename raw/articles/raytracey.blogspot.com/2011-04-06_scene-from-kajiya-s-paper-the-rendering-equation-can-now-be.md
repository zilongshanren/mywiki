---
title: 'Scene from Kajiya''s paper ''The rendering equation'' can now be path traced
  in real-time on the GPU! UPDATE: exe available'
url: http://raytracey.blogspot.com/2011/04/kajiyas-scene-from-rendering-equation.html
author: Sam Lapere
published: '2011-04-06'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

This is just incredible, another milestone in the history of rendering! Jacco Bikker, the main developer behind the real-time path tracer Brigade, and Jeroen van Schijndel, an IGAD research assistant, have made a new simple but superb path tracer (similar to tokaspt) which can render the classic path tracing scene from the 1986 paper "The rendering equation" by Jim Kajiya in real-time on just one GTX 470! There is very little noise overall, there's just some in the glass spheres and in the shadowed caustics.


- 512x512 rendering resolution

- 8 bounces

- 64 samples per pixel

- 12 frames/second on 1 GTX470

The amazing path tracing speed is partly due to the fact that there are no triangle meshes but only geometric primitives (spheres and boxes) in this scene, which are computationally much cheaper to intersect than triangles. The scene in the video is not 100 % identical to the original one (the structure consisting of the revolved parabola with the oblate spheroid, 'mushroom' for short ;-), is missing), but they're working on it (UPDATE 2: the mushroom is finished, see link at the end of this post). This is the original scene from the

[1986 paper](http://www.google.be/url?sa=t&source=web&cd=6&ved=0CFUQFjAF&url=http%3A%2F%2Fciteseer.ist.psu.edu%2Fviewdoc%2Fdownload%3Bjsessionid%3D2EA69276E27FB5D0C6DDC25D9EEA55AF%3Fdoi%3D10.1.1.63.1402%26rep%3Drep1%26type%3Dpdf&rct=j&q=kajiya%20rendering%20equation&ei=arycTZ2UGo2XhQezruHRBg&usg=AFQjCNEIkNwCEIzqosfxGxdKMNAMreyujw&sig2=PdQitF-vzusnYXdNCJXWJQ):It's really mind-boggling when you realize that Kajiya needed 1221 minutes (20.35 hours) to render this image on a supercomputer from 1986 (

[an IBM 3081 mainframe](http://www-03.ibm.com/ibm/history/exhibits/mainframe/mainframe_PP3081.html)) and 25 years later it can be computed at the same resolution in 36 milliseconds on a GTX580! A speed up of 2 million times!! Sounds like a great 25th anniversary :D !I would love to see some animation in this scene, for example an animated light casting moving shadows or a collapse of the pile of green spheres, which would greatly accentuate the "real-timeness" of the path tracing.

UPDATE: Executable and source code for this demo are now available at the links


UPDATE 2: Like Jacco Bikker has promised in the comments, the mushroom-like structure is now done! Visit


[in this thread on the ompf forum](http://ompf.org/forum/viewtopic.php?f=6&t=3174&p=24166#p24152). It's awesome, I'm getting a frametime of 1900ms in the 64 spp version on my poor 8600M GT, which is 49x slower than a GTX580 in this demo (kajiya-perf, default view at 64 spp/frame needs 1759 ms/frame on my 8600M GT and only 36 ms/frame on a GTX580)! Time to upgrade :)UPDATE 2: Like Jacco Bikker has promised in the comments, the mushroom-like structure is now done! Visit

## 6 comments:

is it available somewhere?

Not yet, but hopefully it will be soon. You can always visit the thread on the ompf.org forum (http://ompf.org/forum/viewtopic.php?f=6&t=3174) to put some pressure ;)

Some remarks: I worked on this with Jeroen van Schijndel, who did at least 50% of the CUDA work. And: there's now a CUDA 3.2 compatible version available on the ompf forum.

And finally: the mushroom will be there tomorrow. Code is almost done.

Fantastic news! And I'll correct my post. Truly amazing job, and I'm excited to see the final result :D

A Linux version?


Cheers,

RE: Linux version, I think it's best if you email the developer (Jacco Bikker) for a Linux version. You can find his e-mail on http://igad.nhtv.nl/~bikker/

Post a Comment