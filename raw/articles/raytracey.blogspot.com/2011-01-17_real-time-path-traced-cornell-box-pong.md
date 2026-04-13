---
title: Real-time path traced Cornell Box Pong
url: http://raytracey.blogspot.com/2011/01/real-time-path-traced-cornell-box-pong.html
author: Sam Lapere
published: '2011-01-17'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

![](../../assets/ab9d1d527722c949.jpg)


![](../../assets/ab9d1d527722c949.jpg)

I've started working on a real-time path traced version of Pong, the very first computer game ever. I'm planning to use a modified version of the Cornell box, using the framework of


[tokaspt](http://code.google.com/p/tokaspt/), the excellent real-time CUDA path tracer by Thierry Berger-Perrin which is based on smallpt by Kevin Beason. The tokaspt path tracer is extremely fast (much much faster than iray, Octane or Brigade) and converges to a noise free image in a matter of milliseconds, because a) scenes are very simple and only use spheres as primitives (there are no planes, even the walls of the Cornell box are just parts of huge spheres with very large radii) and b) because occupancy (execution unit usage) is maximized by minimizing registers and shared memory usage and going for 1 main pass (hence minimizing memory traffic). There are no acceleration structures used, so geometry should stay simple (very limited number of spheres) to ensure real-timeness. On the other hand, this allows for completely dynamic scenes, since no acceleration structure also means that no update of acceleration structure is required.The plan is as follows: use the Cornell box as the "playing area". The bouncing ball will be a diffuse or specular or light emitting sphere. The rectangular boxes cannot be made out of triangles (tokaspt only supports spheres as primitive) and should instead be made out of the intersection of two intersecting spheres, creating a lens-shaped object as in the picture below (grey part):

![](http://users.telenet.be/cool_things_with_fresnel_lenses/lens.gif)


![](http://users.telenet.be/cool_things_with_fresnel_lenses/lens.gif)

The "boxes" will thus have curved surfaces on which the ball can bounce off:

![](../../assets/307087b5b8ce856f.jpg)


![](../../assets/307087b5b8ce856f.jpg)

Potential problems:

- I have very little programming experience

- my development hardware is ancient (GT 8600), but even with this old card I can get very fast convergence in the scenes included in tokaspt

- making the gameplay code work and above all fun: 2D physics with collision detection of ball with the lens-shaped boxes (the ping pong bats), ceiling and floor and the ball bouncing back and forth between boxes at progressive speeds to steadily increase difficulty level (I found some opensource code for a basic Pong game

[here](http://www.planet-source-code.com/vb/scripts/ShowCode.asp?txtCodeId=1971&lngWId=1)so this part shouldn't be too difficult)

- all the code should be executed on the GPU

Let's see how far I can get this. Hopefully some screenshots will follow soon.

## 2 comments:

Not having a CUDA capable hardware, I can't try and use it, but seems interesting ...


Hope you'll have a usable gameplay...

Well I'm experiencing some difficulties with making the boxes appear right now and I haven't even started with the gameplay yet. I'll post an update soon.

Post a Comment