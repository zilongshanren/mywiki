---
title: Real-time path tracing on a 40 megapixel screen
url: http://raytracey.blogspot.com/2018/06/real-time-path-tracing-on-40-megapixel.html
author: Sam Lapere
published: '2018-06-01'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

The

[Blue Brain Project](https://bluebrain.epfl.ch/)is a Switzerland based computational neuroscience project which aims to demystify how the brain works by simulating a biologically accurate brain using a state-of-the-art supercomputer. The simulation runs at multiple scales and goes from the whole brain level down to the tiny molecules which transport signals from one cell to another (neurotransmitters). The knowledge gathered from such an ultra-detailed simulation can be applied to advance neuroengineering and medical fields.
To visualize these detailed brain simulations, we have been working on a high performance rendering engine, aptly named "Brayns".

[Brayns](https://github.com/BlueBrain/Brayns)uses raytracing to render massively complex scenes comprised of trillions of molecules interacting in real-time on a supercomputer. The core ray tracing intersection kernels in Brayns are based on Intel's[Embree](https://embree.github.io/)and[Ospray](https://www.ospray.org/)high performance ray tracing libraries, which are optimised to render on recent Intel CPUs (such as the Skylake architecture). These CPUs basically are a GPU in CPU disguise (as they are based on Intel's defunct[Larrabee GPU](https://en.wikipedia.org/wiki/Larrabee_(microarchitecture))project), but can render massive scientific scenes in real-time as they can address over a terabyte of RAM. What makes these CPUs ultrafast at ray tracing is a neat feature called[AVX-512 extensions](https://en.wikipedia.org/wiki/AVX-512), which can run several ray tracing calculations in parallel (in combination with[ispc](http://pharr.org/matt/blog/2018/04/18/ispc-origins.html)), resulting in blazingly fast CPU ray tracing performance which rivals that of a GPU and even beats it when the scene becomes very complex.
Besides using Intel's superfast ray tracing kernels, Brayns has lots of custom code optimisations which allows it to render a fully path traced scene in real-time. These are some of the features of Brayns:


- hand optimised BVH traversal and geometry intersection kernels
- real-time path traced diffuse global illumination
- Optix real-time AI accelerated denoising
- HDR environment map lighting
- explicit direct lighting (next event estimation)
- quasi-Monte Carlo sampling
- volume rendering
- procedural geometry
- signed distance fields raymarching
- instancing, allowing to visualize billions of dynamic molecules in real-time
- stereoscopic omnidirectional 3D rendering
- efficient loading and rendering of multi-terabyte datasets
- linear scaling across many nodes
- optimised for real-time distributed rendering on a cluster with high speed network interconnection
- ultra-low latency streaming to high resolution display walls and VR caves
- modular architecture which makes it ideal for experimenting with new rendering techniques
- optional noise and gluten free rendering

![]() |

powered by seven 4K projectors (40 megapixels in total)

###
**Technical/Medical/Scientific 3D artists wanted **



We are currently looking for technical 3D artists to join our team to produce immersive neuroscientific 3D content. If this sounds interesting to you, get in touch by emailing me at sam.lapere@live.be

## 3 comments:

Wow Sam, that looks awesome! We're one step closer to a Holodeck. ;) Best of luck to you and your team!

Why only a screenshot?

Awesome work. I bet it's stunning to see this in motion :-)


What (and how many!) CPUs are you running this with?

Post a Comment