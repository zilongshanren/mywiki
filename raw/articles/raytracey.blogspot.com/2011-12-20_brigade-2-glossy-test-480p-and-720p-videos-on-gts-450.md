---
title: Brigade 2 Glossy test 480p and 720p videos on GTS 450
url: http://raytracey.blogspot.com/2011/12/brigade-2-glossy-test-480p-and-720p.html
author: Sam Lapere
published: '2011-12-20'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Stats:

- rendered on just one GTS 450, no CPUs involved (hybrid CPU/GPU rendering is actually slower than pure GPU rendering (due to synching) besides being more complex)

- 640x480 render resolution (first video)

- 1280x720 HD render resolution (second video)

- extremely fast convergence: great image quality with only 4 samples per pixel per frame (when the camera is non-stationary) which is sufficient for scenes with skydome lighting

- max path depth 4

- floor, blue boxes, vehicle wheels and chassis are partially glossy to create a plastic look

- containers, mirror ball and flat mirror are perfectly specular

- orange ball is perfectly refractive in first video

- walls are perfectly diffuse (Lambertian)

- almost 3800 triangles (not that many but it's a lot less restrictive than the spheres and boxes from TOKAP and actually not that much slower thanks to BVH acceleration)

The framerate would be a lot smoother on a GTX 580, or better yet a pair of them :-)

## 2 comments:

What's the chance of getting to play with that demo? I've got a GTX 570 I'd like to try that against.

I'll see what I can do.

Post a Comment