---
title: Real-time path traced Unbiased Truck Soccer moved to Kajiya-engine
url: http://raytracey.blogspot.com/2011/05/real-time-path-traced-unbiased-trucker.html
author: Sam Lapere
published: '2011-05-04'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

![](../../assets/d7d94df6bf99fe0c.png)


![](../../assets/d7d94df6bf99fe0c.png)

It has been a while since the last update on Unbiased Truck Soccer, the real-time path traced game featuring a truck made of spheres. Two major changes happened since last time: I've upgraded from my laptop with 8600M GT to a desktop with GTS 450, not a high end card but a fair bit better than the ultra-low end 8600M GT (I'm still using the latter for developing and testing new ideas, because if it looks and runs OK on crappy hardware, you can be sure that it will look great on a real GPU). I've also started porting the Unbiased Truck game to the brand new and recently released Kajiya scene path tracer from Jacco Bikker and Jeroen van Schijndel. This decision was made for several reasons:

- when comparing path tracing performance on the 8600M GT and the GTS450, TOKAP runs only 5x faster while the Kajiya path tracer runs 11x faster. It's also optimized for Fermi cards and uses CUDA 3.2, while tokaspt (TOKAP's framework) was developed for CUDA 2.0 and pre-Fermi cards. The path tracing performance of tokaspt was already extremely fast, but this new path tracer is just in a league of its own.


- it's going to be fairly easy to port this to OpenCL, since the CUDA-specific code is very small and there's also an OpenCL port of the Kajiya demo available at

[http://code.google.com/p/kajiya-gpu/](http://code.google.com/p/kajiya-gpu/)Still waiting for working OpenCL 1.1 drivers from Nvidia.- more primitives to choose from: not only spheres (as in Tokap), but also cubes (axis aligned bounding boxes actually) and ellipsoids, so there will be less restrictions on game ideas. An example of a physics game: drive the truck into a building made of boxes and make the whole structure collapse like in

[this video](http://www.youtube.com/watch?v=yPU6xNNCE68). This would require additional support for oriented bounding boxes.- the Kajiya path tracer uses "hitboxes", a kind of acceleration structure, improving performance. Tokaspt doesn't have built-in acceleration structures, hence the path tracing performance went down very quickly when adding more spheres (or a second truck).

- proper support for skydome and sunlight with much better looking shadows and much reduced noise levels

Some pictures and videos (screenshots rendered with 8600M GT, videos with GTS450):

![](../../assets/69ce158f44a00844.jpg)


![](../../assets/69ce158f44a00844.jpg)

The next two images show all the advantages of rendering with path tracing: reflection, refraction, soft shadows, ambient occlusion and colour bleeding. Surpassing Pixar quality graphics in real-time! :D

![](../../assets/82fc40fb47820930.jpg)


![](../../assets/82fc40fb47820930.jpg)

Nice refraction + color bleeding and gradual light fall-off on the car's rear:



An "overcast" sky (no sunlight):




Night scene, only illuminated with a spotlight. Notice the indirect light bounced from the floor onto the cuboids:








![](../../assets/4e294c9b4e140d86.jpg)

![](../../assets/4e294c9b4e140d86.jpg)

An "overcast" sky (no sunlight):

![](../../assets/367526303ebbc4ba.jpg)

![](../../assets/367526303ebbc4ba.jpg)

![](../../assets/62e3636f1128e113.jpg)

![](../../assets/62e3636f1128e113.jpg)

Night scene, only illuminated with a spotlight. Notice the indirect light bounced from the floor onto the cuboids:

![](../../assets/97902baadb337fad.jpg)

![](../../assets/97902baadb337fad.jpg)

Convergence in this simple scene is extremely fast. While moving, frames are displayed at 8 spp and the scene runs with great quality at 50-60 fps (512x512 resolution) on my GTS 450. When the camera is stationary, 32 spp are accumulated.

I hope I will soon be able to animate the truck and incorporate some CPU physics.

Download executable (Win32) and source code at

[http://code.google.com/p/tokap-the-once-known-as-pong/downloads/list](http://code.google.com/p/tokap-the-once-known-as-pong/downloads/list)-

## No comments:

Post a Comment