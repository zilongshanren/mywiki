---
title: 'Real-time path tracing: Bunny, Dragon and Teapots Medieval meeting'
url: http://raytracey.blogspot.com/2012/03/real-time-path-tracing-bunny-dragon-and.html
author: Sam Lapere
published: '2012-03-20'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I've added a few classic 3D objects to the scene from the previous post, the Stanford Dragon and the Utah teapot. The following screens and video show off the materials that are currently supported the Brigade path tracer and were rendered in real-time on 2 GTX 580 GPUs:

Screens:

Caustics:

The realism you can achieve with this tech in real-time is utterly insane. These are some of the features you won't find in any real-time game engine:

**- global illumination with 100% accurate diffuse interreflections**



**- raytraced reflections and refractions on arbitrary shaped surfaces**



**- physically based glossy reflections**



**- caustics (under the glass dragon)**



**- perfect raytraced soft shadows, that don't eat any GPU memory**



**- raytraced ambient occlusion (e.g. the darker spots under the teapots)**



**- combinations of multiple reflections, refractions, soft shadows and diffuse GI**

**(e.g. a reflection of a shadow of a glass object)**

**are automatically and robustly rendered without any artist intervention**

I will be using this scene for a simple game, probably a survival horror or a puzzle/adventure game.

WIP update: just an idea for my survival horror game:

**this jolly character will chase the player through the streets:**
## 21 comments:

Some fluids(water ???) might be nice.

Sure, but it's not high on the priority list right now.

Won't a general purpose particle system be more important then fluids? Unless your game is base around fluids xD





Looking forward to the video!

two questions.

1. are alpha maps supported in TGA file for Brigade? It would be handy to fake things like hair,plants - the typical stuff you see in modern video games. It would be a waste to model it hair or leaf of a plant.

2. Is animation supported,if so what format?

I'm not sure about the alpha maps, I'll check that out.


Animation is supported and works very well. It's in the md5 (Doom3) format.

very cool video! Is there a way to turn on transparency for a mesh

Thanks! I've coded my own key bindings in this demo to enable transparency. If you're using the public binaries, you can try putting 'transparency 1.0' for the mesh material in the mtl file. If that doesn't work, export the mesh with Maya and change the mtl file.

opps alpha maps, should be alpha channel.

Sam, are you going to start using OTOY's cloud technology very soon with brigade or you will still work on it at a local level?

FreDre: I can't say much about that, sorry

Hey sam,



When will there be some exes to mess around with, my 590 is pretty hungry :D.

~Radiant || Micheal

Hi radiant, great to hear from you again. There won't be any exes for a while, because Brigade is closed source and under heavy development right now.



It was different with my early path traced demos with spheres and boxes (such as Unbiased Truck), which were built with open source code.

I think you will be amazed once it's finally ready for release.

GTX 680 is out and with 1536 shaders it performs worse than GTX 580 in compute:

http://www.anandtech.com/show/5699/nvidia-geforce-gtx-680-review/17

Damn, that's a major disappointment. I expected Kepler to be at least 2x faster in compute benchmarks than the 580. I'm glad I have a dual 580 setup for doing path tracing :)

Apparently GTX 680 compute poor performance comes from unoptimized drivers, NVIDIA stated that they focused more on the gaming side. So we'll have to wait a little bit to see if they'll release a new driver with optimized performances.

I really hope that's the case.

So GTX680 didn't turn out to be the expected ray tracing monster, big number sometimes can be deceptive.

Why would that be compared to GTX580 ?

- L2 cache shrunk from 768 to 512 KB.

- L1 cache the same, but 4 times the number of execution units (running at half speed)

- Number of registers doubled, execution units quadrupled.

- Got rid of a lot of smart, but power hungry scheduling logic.

- Same memory bandwidth

Clearly this is a chip aimed less at compute, but more at console and traditional graphics.

Another bigger chip will surely follow, targeted at compute, and most of all double precision FLOPS, probably more bandwidth too. This will be sold as Tesla, and I doubt we will see a consumer version of it.

The good news is that there is a 7970 with all the features for fast path tracing. Any news yet on how fast Brigade runs on it as there already is a OpenCL version a was told ?

We haven't seen any CUDA ray/path tracing benchmarks with the GTX 680 yet, but if it keeps performing worse or just slightly better than the GTX 580 (while costing more), than that would be extremely disappointing.


I haven't tested the 7970 with Brigade yet, I don't know how it performs, but Jacco said in a comment on a previous post that the OpenCL performance on high end AMD cards was comparable to CUDA and that Nvidia OpenCL ran 10% slower than CUDA.

There was the SmallLux benchmark, but this probably has been tuned towards AMD GPUs.


With all those GPU architectures, there is a lot of careful tuning needed to get the best out of each, (as we found out with ComputeMark.)

Jan

I found some more promising cuda benchmarks on the octane render forum:



SiSoft Sandra 2012

gtx 560 ti @ default: 1065mpix/sec

gtx 570 @ default: 1520mpix/sec

gtx 580 @ default: 1680mpix/sec

gtx 580 @ 850mhz: 1850mpix/sec

gtx 680 @ default: 2750mpix/sec = 1.64 times a gtx 580 or 2.58 times a gtx 560 ti at default clocks

gtx 680 + 165mhz: 3020mpix/sec (+10%)

If you want a deep technical analysis read http://www.realworldtech.com/page.cfm?ArticleID=RWT032212172023&p=2

"The catch is that the Kepler core is a poor fit for compute applications. The excellent efficiency for graphics has undoubtedly come at the cost of general purpose workloads. As our analysis showed, Nvidia’s architects made a conscious choice to quadruple the FLOPs for each core, but only double the bandwidth for shared data. The result is that the older Fermi generation is substantially better suited to general purpose workloads and will continue to be preferred for many applications."

thanks for this. So Kepler's focus is less on general purpose computing performance than Fermi, very weird. Not really happy with this as path tracing crucially depends on it.

Post a Comment