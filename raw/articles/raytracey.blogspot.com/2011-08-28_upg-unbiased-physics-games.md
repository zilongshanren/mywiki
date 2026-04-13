---
title: 'UPG: Unbiased Physics Games!'
url: http://raytracey.blogspot.com/2011/08/upg-unbiased-physics-games.html
author: Sam Lapere
published: '2011-08-28'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

![](../../assets/8ae3ab517b3d3998.png)


![](../../assets/8ae3ab517b3d3998.png)

I've been working on some new real-time path traced demos during the past week involving physics, driving and shooting, three popular ingredients in action games. The demos will be bundled under a new 3 letter acronym, i.e. UPG (GPU in reverse), which stands for Unbiased Physics Games.

I've created two new small games:

- a simple driving game where you can pull some driving stunts with lighting effects (the camera follows the car):

- a simple shooter game where you can hit the car and a robot-like character which will respond to the impact of a cannonball:

Both games use the GPU path tracer developed by Jacco Bikker for the Simplex Paternitas demo. The videos were recorded on a GTS450 with 16 samples per pixel (which already offers very good image quality with little noise) at a resolution of 640x480.

The robot and car in the second demo are both encapsulated by a "hitbox" (an axis aligned bounding box to maximize the path tracing performance), which position is updated every frame.

I'm going to implement a movable and "shootable" light hanging from a chain, which should create dramatic shadow effects. Some basic AI path finding code so the robot starts chasing and shooting the user-controlled car might also be an option. Still thinking about implementing oriented bounding boxes which would enable some cool collapsing structures. Plenty of ideas still and new ones are coming every day, there's just not enough time to execute all of them :) On the rendering side, I think I'll shift the geometric focus of the demos to triangle meshes and two-level BVH or grid, because there's only so much you can do with spheres and boxes - even though they're relatively cheap to intersect.


I've also tried porting the code to OpenCL with the recently released OpenCL1.1 drivers from Nvidia but the OpenCL kernel refuses to build for some reason and there's no easy way to find out what's causing the error. It will take some time to get this right.


Download the executables at


Download the executables at

## 4 comments:

nice!

Good to see some opencl efforts here, I bought an nvidia card just to get in on the cuda party, but not everyone can afford to, Actually I'm starting to think perhaps I didn't either! :S

compiling Opencl code on Nvidia doesn't seem to work quite as easily as it does for amd, but perhaps that was just my lack of experience.

Hi, my thoughts exactly. It just doesn't compile on Nvidia, and Google doesn't help much either...

The first demo points to a good goal for a path-traced game worth shipping. When polygonal rasterization was new (i.e., dog slow) there were a slew of low-framerate racers ported to underpowered microcomputers, and those proved fun despite their limitations. You've got a goofy cartoon car that rolls around those sort of low-detail environments with wacky physics.


You should make Unbiased Stunt Racer FX.

Hi anonymous,



I was just thinking about the same thing yesterday. I remember playing 3D rasterized racers in 1997, which looked incredibly rough, but they were fun. I've go a lot of ideas that I want to implement, but the geometric limitations (only spheres and boxes) require a lot of creativity to work around :) I may have to switch to an entirely different renderer, f.e. Brigade, to realize everything I 've got in mind.

But thanks for the suggestion and the name :-)!

Post a Comment