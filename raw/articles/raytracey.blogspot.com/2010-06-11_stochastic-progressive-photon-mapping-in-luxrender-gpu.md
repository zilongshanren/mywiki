---
title: Stochastic progressive photon mapping in Luxrender GPU
url: http://raytracey.blogspot.com/2010/06/stochastic-progressive-photon-mapping.html
author: Sam Lapere
published: '2010-06-11'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[http://www.luxrender.net/forum/viewtopic.php?f=34&t=4024](http://www.luxrender.net/forum/viewtopic.php?f=34&t=4024)(registration is needed)

The next step for the GPU renderers which rely on brute force path tracing is to investigate more efficient and faster algorithms such as bidirectional path tracing and Metropolis light transport running entirely on the GPU. There is already research going on in this area e.g. "Path Regeneration for Interactive Path Tracing" by Novak, Havran and Dachsbacher describes an efficient bidirectional path tracer running on the GPU (

[http://www.vis.uni-stuttgart.de/~novakjn/paper/eg2010_pt.pdf](http://www.vis.uni-stuttgart.de/%7Enovakjn/paper/eg2010_pt.pdf)).

Another logical evolution is getting biased algorithms (photon mapping, irradiance cache) to work efficiently on the GPU. This seems to be a much more difficult (but not impossible) task than having unbiased rendering on the GPU because these biased algo's are much more difficult to parallellize. Some recent papers in this area:

Morgan McGuire and David Luebke: Hardware-Accelerated Global Illumination by Image Space Photon Mapping

Bartosz Fabianowski and John Dingliana: Compact BVH Storage for Ray Tracing and Photon Mapping

Rui Wang et al.: An Efficient GPU-based Approach for Interactive Global Illumination

Maybe Chaos Group will stun us again at Siggraph 2010 with a biased GPU renderer, which renders 10 times faster than V-Ray GPU :-). Lots of interesting approaches to be explored and more exciting times ahead!

## 1 comment:

Great stuff, your thoughts resonate well with me :D

Post a Comment