---
title: 480p and 720p videos of Brigade 2 physics and UI tests on the GTS 450
url: http://raytracey.blogspot.com/2011/12/480p-and-720p-videos-of-brigade-2.html
author: Sam Lapere
published: '2011-12-18'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

The following videos demonstrate some Bullet physics tests that I've been working on and which were rendered in real-time with the Brigade 2 path tracer on a GeForce GTS 450. All the rendering is pure GPU path tracing with CUDA, the CPU doesn't take part in the rendering process except for recalculating the dynamic BVH of the car and the boxes every frame. All the light in the scene is coming from a skydome. The code for the car physics is essentially the same as what was used in the "Unbiased Stunt Racer" demo. The physics simulation can be paused and resumed and the image converges (extremely fast) when nothing moves (physics simulation paused + stationary camera). There is also a short demo of a work-in-progress material UI (only diffuse to glossy/specular for now, the final version will have sliders for transparency, specularity, diffuse color and emissive color).

480p physics test (640x480 screen resolution, 320x240 render resolution):

## 2 comments:

We have some new stuff for you this week that will significantly enhance frame rates.


- Jacco.

Cool, can't wait! :)

Post a Comment