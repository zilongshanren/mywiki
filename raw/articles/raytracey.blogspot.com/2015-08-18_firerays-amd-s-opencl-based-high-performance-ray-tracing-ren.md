---
title: FireRays, AMD's OpenCL based high performance ray tracing renderer
url: http://raytracey.blogspot.com/2015/08/firerays-amds-opencl-based-high.html
author: Sam Lapere
published: '2015-08-18'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Pretty big news for GPU rendering: about 6 years after Nvidia released the source code of their

[high performance GPU ray tracing kernels](https://code.google.com/p/understanding-the-efficiency-of-ray-traversal-on-gpus/)and 4 years after Intel released[Embree](https://software.intel.com/en-us/articles/embree-photo-realistic-ray-tracing-kernels)(high performance CPU ray tracing kernels), last week at Siggraph AMD finally released their own GPU rendering framework in the form of FireRays, an OpenCL based ray tracing SDK, first shown in[prototype form at Siggraph 2014](http://www.develop3d.com/blog/2014/08/amd-previews-opencl-ray-trace-renderer-on-maya-FirePro-Autodesk)by Takahiro Harada (who also conducted research into foveated ray tracing for VR):
The FireRays, SDK can be downloaded from the AMD Developer site:

[http://developer.amd.com/tools-and-sdks/graphics-development/firepro-sdk/](http://developer.amd.com/tools-and-sdks/graphics-development/firepro-sdk/)
More details can be found at

[http://developer.amd.com/tools-and-sdks/graphics-development/firepro-sdk/firerays-sdk/](http://developer.amd.com/tools-and-sdks/graphics-development/firepro-sdk/firerays-sdk/). The acceleration structure is a BVH with spatial splits and the option to build the BVH with or without the surface area heuristic (SAH). For instances and motion blur, a two level BVH is used, which enables very efficient object transformations (translation, rotation, scaling) at virtually no cost.
AMD's own graphs show that their OpenCL renderer is roughly 10x faster running on 2 D700 FirePro GPUs than Embree running on the CPU:

There are already a few OpenCL based path tracers available today such as Blender's Cycles engine and LuxRays (even V-Ray RT GPU was OpenCL based at some point), but none of them have been able to challenge their CUDA based GPU rendering brethren. AMD's OpenCL dev tools have historically been lagging behind Nvidia's CUDA SDK tools which made compiling large and complex OpenCL kernels a nightmare (splitting the megakernel in smaller parts was the only option). Hopefully the OpenCL developer tools have gotten a makeover as well with the release of this SDK, but at least I'm happy to see AMD taking GPU ray tracing serious. This move could truly bring superfast GPU rendering to the masses and with the two big GPU vendors in the ray tracing race, there will hopefully be more ray tracing specific hardware improvements in future GPU architectures.

(thanks heaps to CPFUUU for pointing me to this)


UPDATE: Alex Evans from Media Molecule had a great talk at Siggraph 2015 about his research into raymarching signed distance fields for Dreams. Alex Evans is currently probably the biggest innovator in real-time game rendering since John Carmack (especially since Carmack spends all his time on VR now, which is a real shame). Alex's presentation can be downloaded from


For people interested in the real-world physics of light bouncing, there was also this very impressive video from Karoly Zsolnai about ultra high speed femto-photography cameras able to shoot images at the speed of light, demonstrating how light propagates and is transprorted as an electromagnetic wave through a scene, illuminating objects a fraction of a nanosecond before their mirror image becomes visible:






UPDATE: Alex Evans from Media Molecule had a great talk at Siggraph 2015 about his research into raymarching signed distance fields for Dreams. Alex Evans is currently probably the biggest innovator in real-time game rendering since John Carmack (especially since Carmack spends all his time on VR now, which is a real shame). Alex's presentation can be downloaded from

[http://www.mediamolecule.com/blog/article/siggraph_2015](http://www.mediamolecule.com/blog/article/siggraph_2015)and is well worth reading. It sums up a bunch of approaches to rendering voxels, signed distance fields and global illumination in real-time that ultimately were not as successful as hoped, but they came very close to real-time on the PS4 (and research is still ongoing).For people interested in the real-world physics of light bouncing, there was also this very impressive video from Karoly Zsolnai about ultra high speed femto-photography cameras able to shoot images at the speed of light, demonstrating how light propagates and is transprorted as an electromagnetic wave through a scene, illuminating objects a fraction of a nanosecond before their mirror image becomes visible:

## 58 comments:

Hi Mr Tracey

I think your blog posts are just so pretty. Thanks for drawing the lovely pictures.

Sasha

One company wrote that ECL is 25 times faster than CMOS, with the former at frequencies >20GHz.





To get rid totally of cache, superscalarity & other ILP-inspired useless features, the fastest operating memory [ECL SRAM] is required.

Just because of x86's CISC->RISC hardware translator, the pure RISC processor is more effective.

Multi-core architecture is slower than Single-core. The only case when multi-core is needed is when a program is developed on naked hardware in order to increase program's effectiveness.

The 16-bits used in CD audio format can be a great solution to floating point problem.

Oh cool, FireRays is worth a new blog post ;)



I would like to see how it performs against its CUDA counterparts.

Next year will be exciting if both companys unleash their 14/16 nm beasts.

Here´s a collection from Siggraph 2015 papers :

http://kesen.realtimerendering.com/sig2015.html

This is worth a look too. An artist from the Cryengine forum made

a voxel gi sponza scene. Everybody can download and try it out for free :

http://www.cryengine.com/community/viewtopic.php?f=309&t=131851

Great numbers ! 10x better than embree cpu path-tracing.



Ghats amazing. Imagine what you could do with 4 highend

AMD GPUs. The future is made of ray tracing...

As i am going deeper and deeper into path tracing i tend to think a lot about raytracing itself. It is a fascinating subject.

Could it be possible to create somehow( i dont know it myself...haha) a photonic/electronic hybrid chip that would much more efficiently render an image?

i am thinking of diffractive photonic elements and such fancy stuff.

A path tracing photonic processor?

Just to give some inspiration..... haha.....

I am starting to wonder which will have real time ray tracing first mobile or desktop. Right now it looks like mobile is going to pull ahead which is crazy. NVidia and AMD really need to get ahead on this or they will fall behind. Some of the mobile ray tracing designs at recent shows have been very impressive.

Is there any comparison chart that compare's nVIDIA optix and FireRays on GPU and Intel's Embree and FireRays on CPU?

Mobile is using the hardware accelerated ray-tracers because they have the same pixel density as current big screens but they are small. So, using raytracers on them make sense and aliasing and artifacts are harder to understand but when you are talking about pcs which have 8K Displays, then things become different. Because you need more computation power to ray trace an 8K image in real-time and also artifacts are easier to detect. So, still we are still not at that point to use real time raytracers for pc applications.

Mobile just lacks the necessary energy for full raytracing.

Imagination Tech has still not build one of their powervr raytracing chips.

In 3-5 years from now there won't be such things as displays anymore.

Only visual copies of real world assests. :P

I can see the future. The world will be a different place.

I don't think the mobile PowerVR ray tracing chip will ever take off. Caustic's Visualizer ray tracing software and hardware flopped pretty badly and several key people have left the company, including Caustic Graphics's founder James McCombe, who invented the hardware.

I'm not sure if fixed function hardware for ray traversal and ray/triangle intersections would make that much of a performance difference since a modern path tracer spends about 3/4 of rendering time on shading. What's needed are more MIMD like GPU architectures which are better at dealing with divergence.

“Mobile just lacks the necessary energy for full raytracing.”




What about in set top boxes or consoles . We could see it in new version of Apples TV or similar devices at some point.

“Imagination Tech has still not build one of their powervr raytracing chips.”

The chip tapped out in July and has an enthusiastic response from developers along with some impressive looking presentations at the recent GDC 2015. The chip is meant to be over 100x more efficient at ray tracing then desktop GPU’s compute. It seems like one to watch to me as it fixes a lot of problems the old chip had like adding a lot of hardware shading clusters to the new design.

"I don't think the mobile PowerVR ray tracing chip will ever take off. Caustic's Visualizer ray tracing software and hardware flopped pretty badly and several key people have left the company, including Caustic Graphics's founder James McCombe, who invented the hardware."




Visualizer didn’t flop it was incorporated into one of the biggest game development engines Unity and is used by a large amount of game developers. Unity are also working on building support for ray tracing and hybrid rendering directly in the Unity engine for end user apps/games. The early beta version has worked well and supports the PowerVR hardware chip.

A couple of staff leaving over a 10+ year project is normal. He spent 5 years building up a team to replace him. The team should have enough experience by now to carry on. Anyway I didn’t mean to cause any arguments, I just thought an experienced team working on real time Ray tracing focused graphic chip backed up by support from one of the main development engines was something to keep an eye on.

Sam, nVIDIA and AMD are able to make real MIMD chips. they just don't like to that, because then the CUDA and OpenCL should change a lot and they think the amount of performance we will gain is not that worth to change from current architectures to real MIMDs.

There is this corean start up called SiliconArts that claims to do at least whitted ray tracing on a mobile MIMD chip consuming only 1 watt.


But i don't know how whitted raytracing would compare roughly to a pathtracer powerwise.

http://www.eetimes.com/author.asp?doc_id=1323637

http://www.google.de/url?sa=t&rct=j&q=&esrc=s&source=web&cd=2&ved=0CCwQFjABahUKEwj2_--9yr_HAhVDtBoKHS5iDe4&url=http%3A%2F%2Fgamma.cs.unc.edu%2FSATO%2FRaycore%2Fraycore.pdf&ei=Cu_ZVfbSJsPoaq7EtfAO&usg=AFQjCNHiVZbzloNsk4GfdaEqa2Sw1OBPqw


Here a detailed description of the architecture.

I did something interesting now to compare the optix and firerays. So, I run the firerays with CornellBox Scene on my GTX 980. Optix also has a similar CornellBox scene. But the nvidia implementation gave me 37 fps but firerays gave me 16 fps which is far bellow what it should be. I dont know if this difference is due to opencl driver implementation performance or fireray is not well implemented.



FireRays

Optix

Firerays


Optix

Thanks for the comparison, but the FireRays image doesn't show up. It's interesting to see such a large difference in performance. OptiX should be more optimized since it has been around since 2010 and incorporates the latest Nvidia ray tracing research kernels (from Nvidia researchers Karras, Aila, Laine and Lehtinen).


On the MIMD subject, I've been reading some articles about SIMD/SIMT/SMT and how Nvidia's Kepler and Maxwell GPUs deal with massively parallel workloads and divergent threads. Considering the amount of cores, registers, streaming multiprocessors, concurrent warps and the availability of warp shuffling, SIMT works very well in most cases and MIMD like features are probably not worth the extra transistor counts. Pascal's mixed precision feature might possibly lessen the need for MIMD even further.

we were using power-vr for some time and belive me.


it is crap (really). so we replaced it. no investor

will jump on this train again.

To be fair, PowerVR is the only company putting real-time raytracing hardware in a mass market chip and believing in its potential. I'm curious to see how they will fare.

ImgTech I mean

Ray tracing based on opencl is pretty good when using gpus.

Whats is the fastest approach for cpus today ?

Definitely Embree is the fastet ray tracing library on CPU. The performance of Embree on CPU is much better than FireRays. Also, coding and debugging on Embree is much easier than FireRays. Also, FireRays is not as complete as Optix. It is just a couple of kernels and a lib file. I expect more than this from a ray-tracing library.


Also, the FireRays supports texturing. When I try the "Rungholt" scene with FireRays on CPU, it gets very slow and sometimes it crashes. I think it is due to using textures and handling textures on CPU is not as fast as GPU.

What is the future of computing?

After non-voltatile memory devices being introduced and stacked on top of processores things will get so dense and hot, that we are going to need new switching devices that would operate at the Landauer Limit, the theoretical thermodynamic energy limit for doing one calculation. Currently 1 Million times less than todays devices.

Luckily there is nanomagnetic logic. It has been already prooven that magnetic logic can operate at Ultra low power(0,6attoJ). Therefore it has been nominated by the international Technology roadmap of semiconductors as one of the most promising future technologies in 2009. (Research in Jülich and Berkeley is top edge)

Since semiconductor manufacturers are already stacking NAND(64layers) or DRAM(8) one might believe that in future all of these devices will converge into one high rise chip containing logic and memory at a reasonable cost. Or better, the logic becomes the memory since nanomagnetic devices or ReRAM Technologies can do non volatile logic. This may allow for trillions of devices being integrated in 3D.

My personal believe is that we will encounter unprecedented performance levels at ultra low power(1..10W) reaching up to a few PetaFLOPS or other types of speed nominations.

Future and nature still hold a lot of potential for computers to get better.

CG will be as it is today the main reason for high performant consumer electronics.

I have studied every future computer technology presently suggested and assume that unless mainstream semiconductor manufacturers switch to Bipolar Emitter-Coupled Logic, you will never get a real high-performance path-tracer, Sam. Good luck.

I dont think we need that level of exotict technology.





The research in filtering plus upcoming gpu features looks promising.

In my opinion it is much more likely that path tracing will take of

on a (7nm)NV/AMD GPU.

Remember the last noise free Brigade demo on 80 GTX680.

Lets say a good filter algorithm can cut down the workload by a factor of 10.

You end up with 8 (old) Kepler GPU´s, even one 14nm Pascal might replace them.

@jenson button. But future still. Holds a lot of unknown variables. That is why it is called future. ;)

Besides path tracing , i see fluid simulations with up to a billion particles as something that would be worthy to do in realtime. A whole ocean with breaking waves in mixed reality would be insanely awesome. there are still so goos reasons why pc would need petaflops.

Optalysys optical computer can do cfd. By 2017 they are going to deliver a desktop 9PFLOP computer.

Keep in mind, that noise-free brigade video was using scenes well suited for uni-directional PT with most contributing samples occurring with less than a bounce or two and most likely a "mega-material" which uses the same kernel for every material. No way can brigade handle indoor scenes with difficult light paths, or advanced materials, with the same efficiency. In my opinion this is what is required for us to say "hey, we can do real-time path tracing without noise", as nobody really cares about path tracing on a simple outdoor city. We want to see the indoor architectural renderings clearing up quickly, with layered materials and animated geometry. We're not there yet, and we're not even really close, but we will get there eventually.

Just stop writing bosh! Intel itself has recently claimed and stated your favourite 7nm is completely useless in terms of further raising computational power, so 10nm currently heralds the end of the anyway pointless game for silicon FETs! Now, Intel's sole hope should be InGaAs; in reality, this means they're planning to take advantage of, say, DCFL, which is nevertheless slower than ECL. For nVidia and Intel, however, misleading & deceiving is always easier than making real progress. Indeed, future holds too many unknown variables, that's why we so need happier presence. The 'optical processors' being demonstrated are Turing-incomplete. Besides that, the electrical signalling on digital circuits already occurs with the speed of light, if not faster.

when it comes to voxels.. ehh well that's still a dead-end technology for now.. polygons and hybrid solutions offer so many hacks and clever tricks to do visually impressive stuff that it's crazy.. I for one think that something as "simple" as smooth shading, texture mapping and texture filtering are the first big advantages over voxels.. atomontage and euclideon with their clever LOD data structures and rendering tricks are still lightyears away from what we can do with top of the line game engines of today.

"Besides that, the electrical signalling on digital circuits already occurs with the speed of light, if not faster."







What is faster than light ? :D

Iis about processing with photos vs electrons. Photons are 1000x faster.

"No way can brigade handle indoor scenes with difficult light paths, or advanced materials, with the same efficiency."

At least they had a night scene with multiple lightsources.

Here is something interesting about creating natural sunlight indoors :

(nanotechnology helps to simulate an atmosphere for scattering)

https://www.youtube.com/watch?v=aJ4TJ4-kkDw

"What is faster than light ?"






extremely weak electrical fields

"Iis about processing with photos vs electrons. Photons are 1000x faster."

))))))

If something like this even exists...



It is irrelevant for todays silicon transistors ;)

Here is some free physics education about electrons and photons :

https://www.youtube.com/watch?v=eFhgb5CqAy8

@cpfuuu that natural light looks interesting....


i wondered one day myself, it should be possible to simulate heaven on the ceiling somehow...

Now someone finally realized it... Nice! Took him 15 years.....wow....

MAgic Leaps technology should be able to do this anyways.....

Sunlight in wintertimes and in the not so far future path traced mixed reality.

Reshading your apartment with summertime lighting in the winter. Yes! :)

A palm that shadows on yourself in realtime.

Fluid simulation at a beach..... Ahhh...why are our computers so slow....XD

Thumbs up guys your doing a really good job. gaming tutorials


Here is a a small update to this Optalysys stuff:



https://www.youtube.com/watch?v=OZenWL44jS4

The interesting part is when he talks about optalysys as a coprocessor

on top of an NV card.

Im asking myself if this can help calculating raytracing and physics data ?

In some way it is like using raytracing to calculate raytracing.

@cpfuuu



they claim to have a computer with 17EFLOops by 2020 by using 50k x50k pixels.

i assume they are talking about sub pixels.

Currently microdisplays with highest ppi have something on the order of 8kx4k at(Jasper) .7inch.

That is a pixel pitch of 3.74µm. Or 1.2 for subpixels.

At that density you could have 50kx50k subpixels with the display measuring only 50x50xmm(well for 1µm). That is only 2 inches x 2 inches worth of microdisplays.

I am really curious how this thing will evolve. This technology could be particularly interesting for VR physics like ocean sim or weather.

I don't know if anyone has seen this yet but you can now try out Euclideon's unlimited detail engine online in the browser now. See the link below:



http://udserver.euclideon.com/demo/html5_viewer.html

For anyone who has never heard of it - it is a massive point rendering engine. Can you imagine this integrated with the latest cuda kernels for path tracing - we would be able to bake the ambient lighting and render the reflected voxels on the fly, producing ultra realistic level detail.

it is an old update. They still owe us the final proof.

THey wanted to release games in may.

https://www.youtube.com/watch?v=7upriqpcKOQ


Yes they can do static. I think that is now a fact.

But no serious animations shown yet which is essential for games.

Not Euclideon again, i dont see this going anywhere.




The only usefull approach in volumetric or voxel data ist Atomage :

http://www.atomontage.com/

It can do animations, destruction and even softbody deformation.

In contrast to polygons, voxel objects are not hollow. If you crack them open

there are still voxels inside, like atoms in the real world.

But i dont know how rendering would be done in this case.

The hardest part are reflections and smooth surfaces.

I think the real-time CG community should work more together in order to find the most efficient raytracing algorithm.


Pathtracing should run on mobile device one good day.

It's not really about the algorithms anymore... we're largely bound by bandwidth when it comes to tracing rays (shading is a different, complex story), so keep your eyes on the new memory and connectivity technologies.

Anonymous: There is actually still plenty that can be done on the algorithm side to speed up path tracing. I'm working on an algorithm, inspired by a technique used by Weta for rendering the CG scenery in Avatar and drawing from my experiments with path tracing spheres (https://code.google.com/p/tokap-the-once-known-as-pong/) that could potentially speed up the calculation of global illumination by several orders of magnitude. Pascal's HBM will certainly help in making path tracing faster, but I think novel algorithms will still provide the biggest boost by far.

@SamLapere: that is awesome to here. :)

@CPFUU: concerning the Optalysys machine: since 'next gen' VR displays like the one from Magic Leap will be holographic, thus computationally_intensive and Optalysys can compute fourier transforms i think it would be a nice combination because CG hologramms are created by a fourier transform method.

New computer architectures anyone?

Max Shulaker explains how it would be possible to achieve a 1000x performance gain if we only conquered the 3rd dimesion via ultra dense CNT interconnects.

https://www.youtube.com/watch?v=wU0bEnQZAF4

Sam: I agree there is more work to be done on the algorithm side, I just think particularly there is a need to reduce bandwidth and latency, rather than a reduction in compute. Uncoalesced memory access and large acceleration structures that tend towards such accesses are not ideal at the moment, so there is more to be done there. After years of research though, I think new memory hardware would provide a more immediate leap.


Cool to hear you're working on something. I don't mean to prod, but what were your terms leaving otoy? Are you allowed to work on a competing technology?

I wonder if native neural network structures could accelerate the acceleration structure problem somehow. I have this strong intuition that neural structures would be very well suited

for this problem.

Knowm is doing some breakthrough stuff in this area.

@Retina: Who is Knowm? you mean the website? do you have any links regarding using neural network structures in acceleration structures?

@mmostajab https://www.youtube.com/watch?v=CFSrC7kjbJo



It is just my natural neural network intuition that i have inherently in my head that is trying to tell me that the building up of acceleration structures in raytracing would be well suited for that since it is somehow an AI problem, not?

knowm.org

But which neural network? and where do you want to use it? tree computation? or in traversal step? or you want to totally change the tree structure? For example, you want to use neural network to remember which path, it has already traversed? This is already called Mailboxing. There are many different techniques for doing that.



It worth to think about using neural networks for tree generation and travesing. a tree which learn from previous traversals and scenes and decide on the fly which rays should be packed and so on. I don't know. may be.

I am just thinking where can a neural network be used?

Yeah that kind of thinking. I don't know either how to implement it directly, i am so baby-new to path tracing. XD

I think a neural network would carry more overhead than it is worth compared to the very specificly written acceleration methods currently used. What pathtracing really needs is quantum computing, to solve the integrals.

Here is a paper about quantum algorithms that could be applied to raytracing.


http://www12.tuiasi.ro/users/103/f4_2012_2_Caraiman.pdf

Australian researchers claim to have the first quantum computer in 3 years.

But not yet at room temperature....XD

~ why are our computers so slow








because they rely on the slow digital logic (shan't point it once again)

~ where can a neural network be used?

Resynthesis

~ new memory and connectivity technologies

Let me guess: DRAM will remain as slow as it is used to be & the speed of light will be improved as well ?

~ quantum computing

Cosmic Signs are incomparably more powerful (if you tried to depict something in your childhood, that might be just they)

Post a Comment