---
title: Unbiased Truck with Bullet Physics!!
url: http://raytracey.blogspot.com/2011/08/unbiased-truck-with-bullet-physics.html
author: Sam Lapere
published: '2011-08-15'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

After lots of trial-and-error, I have finally implemented car physics in the real-time path traced Unbiased Truck demos. Bullet doesn't like it when physical objects are not placed according to Newtonian rules, which has caused some unexpected behaviour and crashes.


The Bullet SDK provides a vehicle physics example with parameters for wheel friction, suspension, chassis stiffness, etc. The "car" consists of a rigid chassis with four independent wheels. Matching the physics world with the rendered world took some time to get right: for example, since each of the four wheels can move independently from each other and from the car chassis, each "rim" had to match up perfectly with its respective wheel.


Crashing the car into the walls is just plain fun. When hitting a wall, the car seems to disintegrate at first, after which it pulls its wheels and chassis together again.


The video below was rendered on a 8600M GT at low resolution, spp and max path length to achieve a somewhat playable framerate (it should look much better on a high end Fermi GPU):


512x256 resolution, max path length=3, 4 samples per pixel/frame:




256x256 resolution, max path length=4, 4 samples per pixel/frame:




A better video with higher framerate and image quality will follow soon. The new executable demo "Unbiased Truck Bullet Physics" can be downloaded from:




This is all work in progress. I'm planning to port this to the GPU path tracer developed by Jacco Bikker (which was also used in the Futuristic Buildings demos), which has support for AABB acceleration structures, better shadows, and which generally runs faster. A camera will follow the car, not only by targeting the car's center, but by moving along with it behind the car. Some basic shooting mechanics will be included as well, and maybe also some ragdoll physics with one of these:




The Bullet SDK provides a vehicle physics example with parameters for wheel friction, suspension, chassis stiffness, etc. The "car" consists of a rigid chassis with four independent wheels. Matching the physics world with the rendered world took some time to get right: for example, since each of the four wheels can move independently from each other and from the car chassis, each "rim" had to match up perfectly with its respective wheel.

Crashing the car into the walls is just plain fun. When hitting a wall, the car seems to disintegrate at first, after which it pulls its wheels and chassis together again.

The video below was rendered on a 8600M GT at low resolution, spp and max path length to achieve a somewhat playable framerate (it should look much better on a high end Fermi GPU):

512x256 resolution, max path length=3, 4 samples per pixel/frame:

256x256 resolution, max path length=4, 4 samples per pixel/frame:

A better video with higher framerate and image quality will follow soon. The new executable demo "Unbiased Truck Bullet Physics" can be downloaded from:

[http://code.google.com/p/tokap-the-once-known-as-pong/downloads/list](http://code.google.com/p/tokap-the-once-known-as-pong/downloads/list)


This is all work in progress. I'm planning to port this to the GPU path tracer developed by Jacco Bikker (which was also used in the Futuristic Buildings demos), which has support for AABB acceleration structures, better shadows, and which generally runs faster. A camera will follow the car, not only by targeting the car's center, but by moving along with it behind the car. Some basic shooting mechanics will be included as well, and maybe also some ragdoll physics with one of these:

![](../../assets/4e09a351fe4ab71f.jpg)


![](../../assets/4e09a351fe4ab71f.jpg)

## No comments:

Post a Comment