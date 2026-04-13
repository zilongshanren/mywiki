---
title: Real-time volume rendering with path tracing
url: http://raytracey.blogspot.com/2012/03/real-time-volume-rendering-with-path.html
author: Sam Lapere
published: '2012-03-13'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

David Skyfall, a reader of this blog (Zelcious on Twitter), has sent me a link to a downright amazing video of something he's working on: a real-time procedural volume path tracer running on a GTX 480 in 720p (100-200 million samples/second):

He also sent me this direct feed image, which rendered for about 30 seconds:

The geometric detail in the picture is just nuts. In a polygonal version, this model would probably be several billions of polygons. The voxel representation allows efficient rendering with GI in real-time. You can see blue-ish lighting from the sky (on the left part) and proper occlusion of environment light on the hollow inside.

This is the second real-time volume path tracer that I know of. The other one, Exposure Render (

[http://raytracey.blogspot.com/2011/10/update-2-on-exposure-render.html](http://raytracey.blogspot.com/2011/10/update-2-on-exposure-render.html)), is a very impressive CUDA based real-time photorealistic volume renderer for volumes scanned with CT and MRI.

## 19 comments:

Real time would be at least 30 images per second at full image quality, at 720p resolution.

I guess it takes at least 3 seconds to reach reasonably good image quality per image.

So it is at least still 100 times too slow to call it real-time. With a single GPU we might be getting there in 16 years, assuming like last few years, GPUs only double in performance every 2 years.

Doing it now in real time would also be possible, with using 100 GPUs in parallel, to render a single frame, by example tiling the image in 100 squares, 1 per GPU. Then you would need to composit all tiles in one image. If OTOY, has a spare render server, this might be something interesting to try.

Correction above, 14 years instead of 16, 2^7 = 128

Jan, I think you should take into account that even if the GPU doubles it's performance every 2 years, there are also new architecture and optimizations each iteration, so I don't really think it's that far away.



Also, if I remember correctly, NVIDIA did a presentation this last SIGGRAPH talking about ray-tracing on the GPUs and I think they said something about that for each new architecture on their GPUs, they increase the performance for ray-tracing exponentially. I think it's in this video:

http://www.youtube.com/watch?v=0IC2NIogWR4

I'll say that in the next 4-6 years we could probably see it real time, maybe even less with cloud computing.

Jan: the video description mentions "pure path tracing", which I interpret as naive brute force path tracing without any filters or other optimizations such as light caching, adaptive sampling and reprojection techniques which exploit spatiotemporal coherence in animated sequences. With these, true real-time volume path tracing could be achieved much faster than 14 years. Also, the video was captured on a GTX 480, which is almost 2 years old now and Kepler is on the verge of launching with more than 3x the number of shaders as a GTX 480 (1536 vs 480), which should double or even triple the path tracing performance (or more if you take bigger caches and other architectural improvements into account, as FreDre suggested).

From the description I read this is rendering from a voxel representation.




I guess a procedural algorithm is used beforehand to calculate the voxels, only once.

With this type of volume rendering you have to keep in mind that usually shaders are not the bottleneck, but getting the data in the GPU is. And as you may know memory bandwidth is increasing slower as shader FLOPS. Caches help, but with the shear amount of voxel data they are easily overwhelmed. The type of optimizations used, if any, is not mentioned. How big is the voxel volume, 1 GB ?

(BTW doubling performance every few years is already exponentially.)

Would rendering a static cloud like this be useful in a game, for flight simulation it might, but then you would need to generate loads of them on the fly.

This cloud looks more like an explosion, so you want this cloud to be generated in real time as a volume animation, for which procedural would not do, but you need fluid / smoke simulation, basically physics, which could take as much time as the rendering and even more memory resources. Will we be getting there ? I think so, but it will take many years, or a big GPU cluster now (and some talented people).

Maybe there's a way to bake the explosion, so it doesn't need to be simulated with physics in real time, specially in video games, as they bake pretty much everything.


As for the bandwidth, yeah, that's a big problem. I don't see it solved any time soon. Unless they start making GPUs with 8gb VRAM or even more, but that's far away.

Still, as Sam said, this path-tracing technique needs further optimizations and its performance should be measured with the latest high-end card, such as the upcoming Kepler that is right around the corner.

Kepler highend should come in 3GB and 6GB version, so not that far off for a 8GB consumer GPU card. Also, if one really needs a 8GB GPU , get a Quadro card. Using voxel for clouds might be going about it the wrong way, surely there are cheaper ways to generate realistic looking clouds that react to wind and scatter light?



Thanks for the link , Sam! the explosions look lovely.

Also, do not forget about dual GK104 GPU(3072 cores) buy 2(SLI) of those should give Brigade 6,144 cuda cores to play with.

Kepler specs are known:

http://www.geeks3d.com/

1500 shaders, but only at about 1 Ghz, 256 bit bus.

Looks more like a 7870 than a 7970.

No mention yet of nr of texture units.

Definitely not the big iron as the GTX 480/580 used to be.

This wasn't really an atempt at something realtime. I just wanted a preview so I could find good camera angles. That said I think there is lot room of improvement, like ray tracey said, this is pretty dumb path tracing. I have so many ideas on how to optimize this, some that could potentially increase performance by 100x. A side note, fraps kills the performance by half for me, its a lot smoother locally.

please share your ideas, I could always use a 100x performance speedup ;)

The link below shows what multi-core CPU may do today.


www.youtube.com/watch?v=m0-kAndyamQ&list=UUeRE-DFhYF1b5gQktAT0AVQ&index=1&feature=plcp

Stefan, I've been working with these kind of CPU volume renderers for several years in my previous job, and I'm really sick of seeing the same flat and boring lighting and shading over and over.


What David has shown in his GPU volume path tracing demo is of a completely different level lightingwise and reconfirms my belief that GPU volume rendering is the way forward.

Ray, I agree with you about GPU future; as soon as it becomes a robust MIMD machine it will be an ultimate ray-tracing machine. The computational complexity may be reduced dramatically once you have MIMD flexibility and this example shows that modern flexible MIMD machine may beat badly mighty SIMD/GFLOP one. Currently, dual e5649 beats badly any CPU+GPU setup for high quality volume rendering of CT/MRI data. If you have different opinion pls provide the link to interactive volume rendering sample.

Of course I have a different opinion, but everyone's entitled to his own, so no point arguing here. If you think CPUs are better, best of luck to you :-)

Well, modern GPU is better for brute force algorithms - it is indisputable fact; however, if code path depends on local data (unique for each thread) then robust MIMD architecture is essential to master an efficient implementation. I prefer facts rather then opinions; I really would love to find GPU based volume tenderer to be competitive with best CPU one; so if you know one please provide the link rather then opinions. I would love to run side by side; frankly, the luck offers a little help for side-by-side arrangement ;o)


Sincerely Yours,

Stefan

Oh, no Fovia again.

Stefan, if you have the chance go to the ECR or RSNA booth of Agfa, ask for a demo of our (my) volume rendering engine.

We can show you either CPU or GPU, you will not see the quality difference, only the speed difference, (ask for 3MP or 6MP rendering, on Impax Agility). Though on close inspection you may see the usual downscaled rendering upscaled in case of CPU.

And because plain GPU volume is now so fast, it becomes overkill, on high end GPU. ( BTW DVR is nice, but MIP is harder to do fast and good)

I've seen AGFA's VR at the latest RSNA and I know the rendering quality it provides (GPU one); it would be great to have side-by-side; unfortunately such arrangement was rejected by AGFA. I really see no downside for AGFA to have such comparison - upon your request it may be covered by NDA. Still the invitation is open...


Regards,

Stefan

Post a Comment