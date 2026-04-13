---
title: Vehicle test in Brigade 2
url: http://raytracey.blogspot.com/2011/12/brigade-2-path-tracer-vehicle-test.html
author: Sam Lapere
published: '2011-12-09'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Another test with the Brigade 2 path tracer: this time I've added a user-controllable vehicle (included in Brigade) to the scene from the previous post. The truck consists of 1953 triangles and uses a dynamic BVH which is updated (BVH refitting as there are only translations and rotations) every frame when the truck moves.

There is also some variation in the materials (all objects are no longer diffuse): the horse has a glass material applied to it (no Beer's law, although the engine supports it), the green sphere is glossy and the truck's trailer is perfectly specular. The following video and screenshots were rendered at 320x240 with 12 spp per frame on a low-end GPU (GeForce GTS 450):

The shadows and refraction are awesome:

## 2 comments:

Good job! Keep it up!

Thanks, I will. I'm already working on a scene with skydome lighting resulting in much less noise. A video will be up soon.

Post a Comment