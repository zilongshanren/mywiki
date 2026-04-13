---
title: GPU-accelerated biased and unbiased rendering
url: http://raytracey.blogspot.com/2010/12/gpu-accelerated-biased-and-unbiased.html
author: Sam Lapere
published: '2010-12-19'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Since I've seen


- unidirectional (standard) path tracing: used by Octane, Arion, V-Ray RT GPU, iray, SmallLuxGPU, OptiX, Brigade, Indigo Render, a bunch of renderers integrating iray, etc. Jan Novak is one of the first to report a working implementation of path tracing on the GPU (implemented with CUDA on a GTX 285,

- bidirectional path tracing (BDPT):

- Metropolis Light Transport (MLT)+BDPT:

- energy redistribution path tracing (ERPT):

- (stochastic) progressive photon mapping (SPPM): used by SmallLuxGPU, there's also a GPU-optimised parallellised version on Toshiya Hachisuka's website,


Octane, my fav unbiased GPU renderer, will also implement an MLT-like rendering algorithm in the next verion (beta 2.3 version 6), which is "coming soon". I gathered some interesting quotes from radiance (Octane's main developer) regarding MLT in Octane:



[the facemeltingly awesome youtube video of Kelemen-style MLT+bidirectional path tracing running on a GPU](http://www.youtube.com/watch?v=70uNjjplYzA), I'm quite convinced that most (if not all) unbiased rendering algorithms can be accelerated on the GPU. Here's a list of the most common unbiased algorithms which have been ported successfully to the GPU:- unidirectional (standard) path tracing: used by Octane, Arion, V-Ray RT GPU, iray, SmallLuxGPU, OptiX, Brigade, Indigo Render, a bunch of renderers integrating iray, etc. Jan Novak is one of the first to report a working implementation of path tracing on the GPU (implemented with CUDA on a GTX 285,

[https://dip.felk.cvut.cz/browse/pdfcache/novakj8_2009dipl.pdf](https://dip.felk.cvut.cz/browse/pdfcache/novakj8_2009dipl.pdf)). The very first paper reporting GPU path tracing is "St**" from 2008 by Huwe and Hemmerling (implemented in GLSL).****ochastic path tracing on consumer graphics cards**- bidirectional path tracing (BDPT):

[http://www.youtube.com/watch?v=70uNjjplYzA](http://www.youtube.com/watch?v=70uNjjplYzA), I think Jan Novak, Vlastimil Havran and Carsten Dachsbacher made this work as well in their paper "Path regeneration for interactive path tracing"- Metropolis Light Transport (MLT)+BDPT:

[http://www.youtube.com/watch?v=70uNjjplYzA](http://www.youtube.com/watch?v=70uNjjplYzA)- energy redistribution path tracing (ERPT):

[http://www.youtube.com/watch?v=c7wTaW46gzA](http://www.youtube.com/watch?v=c7wTaW46gzA),[http://www.youtube.com/watch?v=d9X_PhFIL1o](http://www.youtube.com/watch?v=d9X_PhFIL1o)- (stochastic) progressive photon mapping (SPPM): used by SmallLuxGPU, there's also a GPU-optimised parallellised version on Toshiya Hachisuka's website,

[CUDA http://www.youtube.com/watch?v=zg9NcCw53iA](http://www.youtube.com/watch?v=zg9NcCw53iA),[OpenCL http://www.youtube.com/watch?v=O5WvidnhC-8](http://www.youtube.com/watch?v=O5WvidnhC-8)Octane, my fav unbiased GPU renderer, will also implement an MLT-like rendering algorithm in the next verion (beta 2.3 version 6), which is "coming soon". I gathered some interesting quotes from radiance (Octane's main developer) regarding MLT in Octane:

“We are working on a firefly/caustic capable and efficient rendering algorithm, it's not strictly MLT but a heavily modified version of it. Trust me, this is the last big feature we need to implement to have a capable renderer, so it's our highest priority feature to finish.”

“MLT is an algorithm that's much more efficient at rendering complex scenes, not so efficient at simple, directly lit scenes (eg objects in the open). However MLT does sample away the fireflies.”

“The fireflies are a normal side effect of unbiased rendering, they are reflective or refractive caustics. We're working on new algorithms in the next version that will solve this as it will compute these caustics better.”

“they are caustics, long paths with a high contribution, a side effect of unbiased path tracing. MLT will solve this problem which is in development and slated for beta 2.3”

“the pathtracing kernel already does caustics, it's just not very efficient without MLT, which will be in the next 2.3 release.”

“lights (mesh emitters) are hard to find with our current algorithms, rendertimes will severely improve with the new MLT replacement that's coming soon.”

“it will render more efficiently [once] we have portals/MLT/bidir.”

“All exteriors render in a few minutes clean in octane currently. (if you have a decent GPU like a medium range GTX260 or better). Interiors is more difficult, requires MLT and ultimately bidir path tracing. However, with plain brute force pathtracing octane is the same or slightly faster than a MLT/Bidir complex/heavily matured [CPU] engine, which gives good promise for the future, as we're working on those features asap.”

With all unbiased rendering techniques soon possible and greatly accelerated on the GPU, what about GPU acceleration for biased production rendering techniques (such as photon mapping and irradiance caching)? There have been a lot of academic research papers on this subject (e.g. Purcell, Rui Wang and Kun Zhou, Fabianowski and Dingliani, McGuire and Luebke, ...), but since it's a lot trickier to parallellize photon mapping and irradiance caching than unbiased algorithms while still obtaining production quality, it's still not quite ready for integration in commercial software. But this will change very soon imo: on the ompf forum I've found a link to a very impressive video showing very high-quality CUDA-accelerated photon mapping


This is a render of Sponza, 800x800 resolution, rendered in 11.5 seconds on 1 GTX 470! (image taken from


[http://www.youtube.com/watch?v=ZTuos2lzQpM](http://www.youtube.com/watch?v=ZTuos2lzQpM).This is a render of Sponza, 800x800 resolution, rendered in 11.5 seconds on 1 GTX 470! (image taken from

[http://kaikaiwang.blogspot.com/](http://kaikaiwang.blogspot.com/)):![](../../assets/e75bc21f8ff6cccd.jpg)


11 seconds for this quality and resolution on just one GPU is pretty amazing if you ask me. I'm sure that further optimizations could bring the rendertime down to 1 second. The video also shows real-time interaction (scale, rotate, move, delete) with objects from the scenery (something that could be extended to support many dynamic objects via HLBVH). I could see this being very useful for real-time production quality global illumination using a hybrid of path tracing for exteriors and photon mapping for interiors, caustics, point lights.


Just like 2010 was the year of GPU-accelerated unbiased rendering, I think 2011 will become the year of heavily GPU-accelerated biased rendering (photon mapping in particular).

Just like 2010 was the year of GPU-accelerated unbiased rendering, I think 2011 will become the year of heavily GPU-accelerated biased rendering (photon mapping in particular).

## 5 comments:

article that i was looking for.

I am just curious..

why doesnt chaosgroup just develope GPU based VRAY?? not a lame VRAY RT? All they need to do is keep VRAY and use GPU instead of CPU. Seems to be very easy job..

but they tend to wait? why?

Nice article btwy. Thanks

They actually have made a GPU version of V-Ray RT based on OpenCL. The "real" V-Ray renderer (not the RT version) will also be accelerated by GPUs in a few years IMO, when Nvidia Denver comes out (Maxwell GPU generation in 2013).

I agree...nvidia denver will be the killer..but i still dont understand why dont they just use CUDA for accelerating the "real" vray not the vray RT.

Good question, I think GPUs need some necessary CPU-like features before that will happen (probably with Maxwell), but as said earlier I'm sure that the "real" V-ray eventually will become fully GPGPU-accelerated in a few years, whether with CUDA or OpenCL.

what s diff and meaning cpu and gpu?

Post a Comment