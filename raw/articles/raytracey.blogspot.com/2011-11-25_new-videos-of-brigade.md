---
title: New videos of Brigade!
url: http://raytracey.blogspot.com/2011/11/new-videos-of-brigade.html
author: Sam Lapere
published: '2011-11-25'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

The developers behind the Brigade path tracer (Jacco Bikker and Jeroen van Schijndel) have released two very impressive videos on Youtube and the jump in quality and performance is quite huge. The scene in the video runs smoothly on just one GTX 470 at 8spp and 640x360 render resolution (1280x720 display resolution) with very little noise:

This latest version of the Brigade path tracer contains at least two major improvements compared to previous versions: multiple importance sampling and a Blinn shader for glossy materials (e.g. the floor) which greatly enhances the realism of the scene (and seems to converge very fast). The kernel now runs on the GPU only.

Very impressive what they have achieved so far. With an extra GPU, the noise should almost vanish and become imperceptible after playing a while. And with Nvidia's Kepler and AMD's compute-focused GCN (HD7000) on the horizon, this path tracer is going to become very interesting (when the code will be ported to OpenCL in AMD's case). Something like real-time photorealistic chess rendered on the GPU is very close now. Jacco also mentions in the comments under the video that a new game is in the works with support for animated objects (including skeletal animation).

The mere thought of having truly real-time, photoreal global illumination in games is the most exciting thing that has happened in computer graphics over the past ten years. The last time I was this excited was with the introduction of real-time lighting and shadowing with normal mapping in Doom 3,

[first shown to the world on the MacWorld Expo 2001](http://www.youtube.com/watch?v=Qj3dPyk7hPI):I can't wait to get my hands dirty and experiment with the new Brigade code.

## 5 comments:

awesome :D will it be released as open source or remain proprietary?

btw: what's up with ompf.org?

About open sourcing the code: I can't tell you, it's up to Jacco to decide this.


ompf.org has indeed been down since last weekend. I think only tbp (admin) can fix that.

Ompf is down for the moment, and there's not much we can do about that without tbp. We will probably setup a temporary replacement this week. Can't really live without ompf. :(


- Jacco.

Note that the scene with the colored chess piece runs on two GPUs (dual GTX470s). The other video is 1 GPU (also GTX470). Also note that doubling performance only slightly reduces noise; there's no linear link between noise and performance.


That being said: one more generation of GPU should get us pretty far. Not sure if it will be enough for path traced games, but we're getting close, and I do believe the moving target of ray tracing will stop moving. ;)

- Jacco.

Totally agree, from my own experience with messing around with several GPU path tracers, I'm also convinced that we're very close to practically usable real-time path tracing. Things like adaptive sampling, multiple importance sampling, QMC and bidirectional path tracing will help a lot (and of course faster GPUs).

Post a Comment