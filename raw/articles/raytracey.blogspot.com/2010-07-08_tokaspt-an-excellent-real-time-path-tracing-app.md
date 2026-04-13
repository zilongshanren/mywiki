---
title: Tokaspt, an excellent real-time path tracing app
url: http://raytracey.blogspot.com/2010/07/tokaspt-excellent-real-time-path.html
author: Sam Lapere
published: '2010-07-08'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

![](../../assets/41229fe41ac4d0a9.jpg)


![](../../assets/41229fe41ac4d0a9.jpg)

Just stumbled upon this very impressive CUDA based path tracer:


Although the scenes are quite simple (spheres and planes only), it's extremely fast and it converges literally in a matter of milliseconds to a high quality image. Navigation is as close to real-time as it gets. There are 4 different scenes to choose from (load scene with F9) and they can be modified at will: parameters are sphere size, color, emitting properties, 3 material BRDFs (diffuse (matte), specular (mirror) and refractive (glass)) and sphere position. Path trace depth and spppp (samples per pixel per pass) can also be altered on the fly thanks to the very convenient GUI with sliders. When moving around and ghosting artefacts appear, press the "reset acc" button to clear the accumulation buffer and get a clean image. Definitely worth messing around with!

[http://code.google.com/p/tokaspt/](http://code.google.com/p/tokaspt/)for exe and source (The app itself has been available since January 2009)Although the scenes are quite simple (spheres and planes only), it's extremely fast and it converges literally in a matter of milliseconds to a high quality image. Navigation is as close to real-time as it gets. There are 4 different scenes to choose from (load scene with F9) and they can be modified at will: parameters are sphere size, color, emitting properties, 3 material BRDFs (diffuse (matte), specular (mirror) and refractive (glass)) and sphere position. Path trace depth and spppp (samples per pixel per pass) can also be altered on the fly thanks to the very convenient GUI with sliders. When moving around and ghosting artefacts appear, press the "reset acc" button to clear the accumulation buffer and get a clean image. Definitely worth messing around with!

## 6 comments:

Impressive indeed. The sliders are a great addition.

I hope these programs will soon be released in OpenCL. ATI folks need some lovin too :)

I'm glad you were fooled but there's no plane anywhere, only spheres (up to the local memory capacity); credits go to beason for that trick (a large enough sphere under the right conditions will look like plane, unless you're working with GPU and didn't sacrifice enough goats on the IEEE754 altar).




'Z' is the shortcut to clear that accumulation buffer. What was kind of nice on my then underpowered 8600GTS is quite annoying on faster hardware. Sorry for that.

If you ever make some funny scene, do not hesitate to share.

Anyways, i hope you were all amused.

Thanks tbp :-D! So the fact that it's only tracing spheres is where the speed comes from. I hope you will develop it further when you find some spare time.

Shhh, you're gonna blow my cover!




I maximized occupancy (execution unit usage) by minimizing registers & shared memory usage and going for 1 main pass (hence minimizing memory traffic); under such circumstances i couldn't shoehorn more features (beleive me, i tried).

It's a one trick pony.

My goal was uncompromised, real-time, dynamic, path tracing on

mycrappy hardware, not some hypothetic big iron from the future ;)You'd have to take another approach entirely to, say, add more primitives or simply throw an acceleration structure in there. Like multiple passes, trading gigantic amount of memory traffic to relieve each kernel for example.

GPU are weird beasts that come with weird bottlenecks.

I see. So not usable for more general scenes, but maybe useful for a pathtraced snooker or jeu de boules game played on a gigantic sphere ;-D!

Post a Comment