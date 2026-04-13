---
title: Real-time physically based volume rendering with CUDA
url: http://raytracey.blogspot.com/2011/10/real-time-physically-based-volume.html
author: Sam Lapere
published: '2011-10-01'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Just saw a very impressive video of "Exposure Render", an open source CUDA based volumetric path tracer which will be presented at EuroGraphics 2012:

The video shows an eerily realistic representation of a person scanned with CT (computed tomography), where anatomical layers of skin, muscle, cartilage, connective tissue and bone can be peeled away and rendered with photorealistic quality global illumination in real-time. This could be an extremely useful training tool for medical students and aspiring surgeons. The physically based photorealistic 3D renders of skull, bones and soft tissue could also benefit radiologists in diagnostic decision making.

Most medical volume rendering software uses ray casting, which is fast but provides very unrealistic looking lighting. With volumetric path tracing finally being feasible in real-time thanks to the GPU, this will hopefully change soon. I think we will see an implementation of real-time path traced sparse voxel octrees pop up sometime in the very near future.

## 4 comments:

This is no MRI, it is CT.

Corrected, thanks.

btw, die dx11 vuursimulatie is zeer indrukwekkend

Great blog! It's really revealing; my most favorite part is:



>"Most medical volume rendering software uses ray casting, which is fast but provides very unrealistic looking lighting."

Good Luck...

StefanBanev

Post a Comment