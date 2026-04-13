---
title: 'Real-time photorealistic GPU path tracing: first exposure test'
url: http://raytracey.blogspot.com/2012/05/real-time-photorealistic-gpu-path_10.html
author: Sam Lapere
published: '2012-05-10'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Thanks to another recent speed boost, Brigade is now able to render real-time photorealistic animations of huge urban scenes with dynamic day/night cycle at 1280x720 resolution and 20+ fps on 2 GTX 580 GPUs, including all the physically based light effects you expect from a path tracer:










The coolest thing about Brigade is that all of these effects are virtually free and can be used aplenty. It's the magic of path tracing.

**- real raytraced depth-of-field****- perfect soft shadows****- true ambient occlusion****- indirect lighting with diffuse interreflection/color bleeding****- specular and glossy reflection****- refraction****- ... the whole shebang.**The coolest thing about Brigade is that all of these effects are virtually free and can be used aplenty. It's the magic of path tracing.

## 2 comments:

Very impressive. The convergence speed of the image, especially for brighter areas is simply outstanding.



Good to hear that post fx is starting to find its way into the renderer.

I was wondering if you plan to implement Photon Mapping for caustic and such?

Thanks.


Photon mapping is not planned anytime soon. I'm not sure if it's worth investigating, because from test with stochastic progressive photon mapping on the GPU, it's actually slower than pure path tracing in most cases. Caustics would benefit for sure, but those can be handled efficiently with bidirectional path tracing as well. We're not aiming to render the pathological cases in real-time (light bulbs behind glass and many SDS paths), PT/BDPT with MIS + some secret sauce should be able to render most of our target scenes in real-time.

Post a Comment