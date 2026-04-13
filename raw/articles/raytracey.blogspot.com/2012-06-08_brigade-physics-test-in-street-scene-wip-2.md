---
title: Brigade physics test in street scene WIP 2
url: http://raytracey.blogspot.com/2012/06/brigade-physics-test-in-street-scene_08.html
author: Sam Lapere
published: '2012-06-08'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Another test with the ray traced AO kernel in Brigade. This kernel holds the middle between distributed ray tracing [Cook] and full path tracing [Kajiya] and provides soft shadows, refraction, reflection (glossy and perfectly specular), depth of field and ambient occlusion with adjustable ray length, all raytraced in real-time and without screen space limitations or other hacks.

The best thing about this kernel is that the image converges so insanely fast that I've decided to tone down the frame averaging (blur) almost to zero. The little noise that still remains is mostly visible around shadow edges and on reflecting surfaces, but it's almost negligible compared to the amount of noise when using the path tracing kernel. Brigade is now extremely close to real-time noise-free rendering and this is still without any fancy noise filters.

If the current rate of development continues, you might expect to see the Brigade engine at E3 next year (disclaimer: kidding)

Real-time rendered test at 800x480 resolution with 6 samples per pixel on 2x GTX 580:

**UPDATE:**According to

[this article](http://www.geforce.com/whats-new/articles/stunning-videos-show-unreal-engine-4s-next-gen-gtx-680-powered-real-time-graphics/), Unreal Engine 4 uses a form of GPU based real-time ray tracing for global illumination called voxel cone tracing in a sparse voxel octree (SVOGI). The technique was pioneered by

[Cyril Crassin](http://blog.icare3d.org/2012/05/gtc-2012-talk-octree-based-sparse.html)and was presented at Siggraph last year (sparse voxel octrees were all the hype in 2008 thanks to Jon Olick's Siggraph demo, which was researched further independently by Cyril Crassin and Samuli Laine). The future of real-time ray tracing on the GPU looks bright with one of the largest game companies starting to use it on a large scale :)

**UPDATE 2:**A reader of this blog just sent me a screenshot of an awesome stress test with the public Brigade version: a giant cube containing 729k (90x90x90) tiny cubes, a total of 8.75 million triangles, consuming ~ 2 GB of video memory. Thanks Nicholas!

## 31 comments:

Any plans on implementing a sky system?

Holy crap! That is seriously impressive performance!

Absolutely, a physical sun/sky + animated clouds are on the to-do list.

Thanks Sean. tbh, I was actually very surprised when I tried out the new kernel.

You and me both! It's getting so good that it perhaps deserves a spotlight at the next SIGGRAPH (real time graphics portion of the show).


Using AO, and distributed ray tracing, I would be interested in the rendering differences vs a purely path traced image.

Sean, I think it's safe by now to say that Brigade is conditionally accepted for the Real-Time Live session on Siggraph this year :D

:D

Are you allowed to show side-by-side comparisons pics between both kernels ?

Sure, but I prefer to wait a bit. It's still a work in progress, it should get faster and look even better than it does now.

Wow just wow..



Just to finish up my testing I was able to load 90^3 cubes in brigade.

that just fit under 6 gig, and 3 gig GTX 580.

What about the first bounce lighting you mentioned earlier? Do you know already how to do that?

Nicholas, thanks for the awesome stress tests but how do you fit 6 GB of geometry into a 3GB GPU?

Sorry for the confusion. 6Gig PC memory. actually I didn't look at how much memory it used on the card.


anyway I would love to post an image , is that possible with the "img" html tag in blogger?

I think so. If not, upload your image to something like tinypic and I will post it on my blog.

Anonymous ^^: it's not in yet

Yeah I can see it's not built in at the moment. My question was whether you already know how to do it or not.

I don't work on the rendering core, so I have no idea. The other people working on Brigade have much more insight in how to make it work

I show most of the width and depth, but I didn't bother with the height because you loose all detail.




correction: It uses about 2+ gig of the card memory.

img tags doesn't work here is a direct link:

http://i48.tinypic.com/2e1ggia.png

Cool, will update the post

AO rays are highly coherent. So you

should consider to run your kernel on cpus with frustum/packets. This gives you a magnitude more thruput (mrays/s) compared to current gpu architectures.

AO rays are highly incoherent, so CPUs are out of the question as they are an order of magnitude slower than current GPUs for tracing incoherent rays, which make up 80-90% of all rays. For this reason packet/frustum tracing is not relevant anymore in modern rendering engines.

AO rays are pretty coherent in comparison with pathtracing after the primary rays.

for ao you need a lot of rays distributed over the hemisphere. they can be easily grouped together (octant/quadrant) and the ray length is short => ao rays in common are coherent and yes: cpus outperform gpus in this area that is for shure !

if you say so :)

I was wondering if you could have an access to an nvidia 680 card to make performance comparisons with 580. I suspect that even with two 680 cards the difference will be zero, since the problem is mostly memory bound and the bandiwdth of both the 580 and 680 is the same ( around 192GB/sec ).


p.s. brigade uses cuda or opencl?

I don't have access to a 680 myself, so I can't say much about the 680. But I do know that it's not as good as I hoped.


Brigade uses both CUDA and OpenCL.

by both you mean you can choose ? so on an ATI card you can choose to use opencl?


p.s. i downloaded the latest version from here http://igad.nhtv.nl/~bikker/ which is revision 2017 but it has no precompiled demo/benchmark in any folder. i guess it's just an API and we have to make our own examples ?

Brigade can run on OpenCL but this is not in the public version. There are some samples in the package, but you have to build them first with VS2008 or VS2010. There are some executables in the Jan 27 post on the same page.


The public Brigade version also lacks many features and optimizations that I've been showing in recent demos.

Will all those features and optimizations be added in a future release? what is the plan? will it be a commercial version ?

Can't say anything about that.

Post a Comment