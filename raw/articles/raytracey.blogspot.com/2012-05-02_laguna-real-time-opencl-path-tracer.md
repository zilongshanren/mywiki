---
title: 'Laguna: real-time OpenCL path tracer'
url: http://raytracey.blogspot.com/2012/05/laguna-real-time-opencl-path-tracer.html
author: Sam Lapere
published: '2012-05-02'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Arjan van Wijnen created a new real-time experimental OpenCL path tracer, called Laguna. It runs surprisingly fast and uses a seemingly new kind of grid-like acceleration structure (which the author calls a "precalculated blocks structure"). Something to keep an eye on.

Screenshots and executable demo at



## 15 comments:

Is there a paper published about that new data structure?

Nope, but you can look at the ocl kernel code when you download the executable

Hi Sam! Can you add some interesting cars like at this picture to your scene of city ?

Sure. I've currently added an animated character, a first-person weapon and a simple user-controlled car (will post some videos of that soon).

Unfortunately it does not work with all the other scenes I have try (Sponza by example). But, for sure it is a good start...



It will be also interesting to see "how" he build the grid :-)

Nice work...

the grid is built with optimal non-cubical voxels

"optimal non-cubical voxels" !


Looks interesting ! I've never play with this ! Does the code of the builder can be published too ?

Will be curious to try it against SBVH & RSBVH (Fast Ray Sorting and Breadth-First Packet Traversal for GPU Ray Tracing) with different scenes :-P

maybe you should aks the author himself :)

Sure :-)

What about the grid build and rebuild time? Is there any information?

From what I can tell by trying the demo, building the grid is pretty slow (several minutes for the 1.3M triangle Mercedes model). Grid building is done on the CPU at the moment, but could be near real-time when done on the GPU.

I haven't checked CPU usage but it seems alot of the "build time" is infact spent loading the model itself (over 100mb)...so maybe it is reasonably fast...also of note increasing the spp seems to increase efficiency (atleast on my 7 AMD 970). It's nice to see HTC 680 and AMD 7970 putting out similar decent performance...that's what we need! -antzrhere

If you try loading a different model than the one that came with the demo, you'll notice that it takes quite some time to build the optimized grid, much longer than the loading of the model itself. The performance on AMD cards is indeed very nice.

that'll teach me to post on my phone on the bus...I meant GTX 680 and AMD 7970! It'd be nice if you could do a side-by-side video comparison of Brigade and this engine using the same scene and the same target fps (however many SPP that ends up being on each engine). The advantage Bridage is having a seperate acceleration struct for dynamic objects....I've looked at the code and and can't see anything like this on Laguna...whatever bounding heirarchy it's using...



Out of interest...how well does Brigade OpenCL perform on AMD's 7970...?have you any information on how it compares to the GTX 580 and 680?

-Antzrhere

Making comparisons with Brigade would be unfair, because Brigade is so damn optimized for real-time that it would completely crush every other path tracer that tries to defy it.



Seriously, samples are calculated differently in Brigade (with a very efficient Russian roulette like scheme), so a direct comparison with the same number of spp is not possible.

Regarding performance on GTX 580/ GTX 680/ HD 7970: Brigade's performance has been tested on all these cards, it's too early to give any numbers, because they change every couple of days.

Post a Comment