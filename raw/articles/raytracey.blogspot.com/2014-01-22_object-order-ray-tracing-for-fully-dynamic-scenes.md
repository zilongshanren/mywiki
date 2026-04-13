---
title: Object-order ray tracing for fully dynamic scenes
url: http://raytracey.blogspot.com/2014/01/object-order-ray-tracing-for-fully.html
author: Sam Lapere
published: '2014-01-22'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Today, the

[GPU Pro blog](http://gpupro.blogspot.co.nz/2014/01/gpu-pro-5-object-order-ray-tracing-for.html)posted a very interesting article about a novel technique which seamlessly unifies rasterization and ray tracing based rendering for fully dynamic scenes. The technique entitled "**" will be described in the upcoming GPU Pro 5 book (to be released on March 25, 2014 during the GDC conference) and was developed by Tobias Zirr, Hauke Rehfeld and Carsten Dachsbacher .**[Object-order Ray Tracing for Fully Dynamic Scenes](http://gpupro.blogspot.co.nz/2014/01/gpu-pro-5-object-order-ray-tracing-for.html)This article presents a method for tracing incoherent secondary rays that integrates well with existing rasterization-based real-time rendering engines. In particular, it requires only linear scene access andsupports fully dynamic scene geometry. All parts of the method that work with scene geometry are implemented in the standard graphics pipeline. Thus, the ability to generate, transform and animate geometry via shaders is fully retained. Our method does not distinguish between static and dynamic geometry. Moreover, shading can share the same material system that is used in a deferred shading rasterizer. Consequently, our method allows fora unified rendering architecture that supports both rasterization and ray tracing. The more expensive ray tracing can easily be restricted to complex phenomena that require it, such as reflections and refractions on arbitrarily shaped scene geometry. Steps in rendering that do not require the tracing of incoherent rays with arbitrary origins can be dealt with using rasterization as usual.

This is to my knowledge the first practical implementation of the so-called hybrid rendering technique which mixes ray tracing and rasterization by plugging a ray tracer in an existing rasterization based rendering framework and sharing the traditional graphics pipeline. Since no game developer in his right mind will switch to pure ray tracing overnight, this seems to be the most sensible and commercially viable approach to introduce real ray traced high quality reflections of dynamic objects into game engines in the short term, without having to resort to complicated hacks like screen space raytracing for reflections (as seen in e.g. Killzone Shadow Fall, UE4 tech demos and CryEngine) or cubemap arrays, which never really look right and come with a lot of limitations and artifacts. For example, in this screenshot of the new technique you can see the reflection of the sky, which would simply be impossible with screen space reflections from this camera angle:

Probably the best thing about this technique is that it works with fully dynamic geometry (accelerating ray intersections by coarsely voxelizing the scene) and - judging from the abstract - with dynamically tesselated geometry as well, which is a huge advantage for DX11 based game engines. It's very likely that the PS4 is capable of real-time raytraced reflections using this technique and when optimized, it could not only be used for rendering reflections and refractions, but for very high quality soft shadows and ambient occlusion as well.

The ultimate next step would be global illumination with path tracing for dynamic scenes, which is a definite possibility on very high end hardware, especially when combined with another technique from a very freshly released paper (by Ulbrich, Novak, Rehfeld and Dachsbacher) entitled

**which promises a 5x speedup for real-time progressively path traced GI by cleverly caching diffuse and glossy interreflections (a video can be found**
## 62 comments:

Modern rasterization pipelines are already disgustingly complicated... Now we are excited to rough voxelize our scene and add another shading stage? Wake me up in 5 years, i dont want to work with this nonsense

we implemented the voxel approximation for a some effects

two years ago. there are a lot of special cases where you easily run into huge problems. conclusion: forget it, its crap.

I think the addition of ray tracing will simplify game engines by gradually replacing "hacks" like shadow mapping, cube environment mapping, order independent transparency, SSAO, SSGI, postprocessed depth of field and motion blur, etc. John Carmack also thinks ray tracing will gradually be introduced in game engines, according to this

Will you make use of progressive visibility caching... for Brigade?


Sounds like you are one step closer to 99,5% noise free PTed images. :)

i thought next-gen engines made already use of some kind of object ordered ray tracing, hehe.

Are you aware of this work by Matt Swoboda?




http://directtovideo.wordpress.com/2013/05/07/real-time-ray-tracing/

http://directtovideo.wordpress.com/2013/05/08/real-time-ray-tracing-part-2/

( demo http://www.pouet.net/prod.php?which=61211 )

Just FYI Matt Swoboda made a talk at DevStation 2013 in London about real time raytracing (The sony PS4 developer conference). Unfortunately I can't share the slides. (NDA)

This is really exciting stuff, I hope this is the tipping point I have be predicting.


I agree that a single unified technique would be ideal, but likewise if this can be used to factor away all the ugly hacks; then bring it on.

Hi Sam. Give us something please.

we need more stuff...more videos please

http://derunov.narod.ru/Experiment_en.htm

There's not much more to show, more videos of outdoor scenes are meaningless at this point. We are compute bound now and it's a waiting game until we get meaningful videos again (indirect light dominant scenes), maybe a few years

The sixth-generation 3D graphics computer :










{A.S. No cooling is required at all !}

* Room-temperature superconductor {pioneered by Derunov V.L. [2x off-Bednorz-Müller Nobel Prize pendant], Soviet Union, 1978; proved at Cambridge University, United Kingdom, in 2010} ‘bipolar’ {can as well utilize only one type of charge carriers which should make the even faster} transistors {Dayem bridge Josephson junction on purest Teflon isolator} & room-temperature superconducting wire

* Emitter-Coupled Logic

* Explicit Data Graph Execution {non von Neumann}

* Combinational ternary logic

* Single 8-threaded core with machine belt architecture

* Multilayered integrated circuit

* 100-exabyte Hyper CD-ROM

* Mercury programming language

> We are compute bound now and it's a waiting game until we get meaningful videos again (indirect light dominant scenes), maybe a few years



~ Sam, just order 4 nVidia Quadro K6000s and show them what they are demanding the day after tomorrow...

* Nonetheless, gaming industry is already moving gradually onto Linux-driven IBM Power 740 Express server.

Sam,


Will we see more of Brigade at GDC 2014?

On the Otoy blog (http://render.otoy.com/newsblog/) it is mentioned that Brigade is being used by some top game studios for AAA franchises. Exciting! Any hints on this?

Yo Sam, it's been almost 2 months now and on GDC Crytek, Unity and Epic have announced their new pricing models and engine features.





Also Imagination Technologies has announced PowerVR as their hardware ray tracing solution.

I also read the Announcment on the otoy blog about launching Brigade on the Amazon EC2 cloud.

So, on the development side, what's currently going on ? Mind giving us an update on what you guys are working on right now? I also wonder what you think about the Hardware Solution for Ray Tracing. Would Path tracing also benefit from something similar?

The Iray VCA demo from Nvidia @ GTC2014 was utterly disappointing.


Please, show us what you could do with such a massive piece of hardware!

Why no update yet? There's a new video out here https://www.youtube.com/watch?v=BpT6MkCeP7Y

Holy shit, just saw a video of live texture painting with Octane inside Photoshop: http://vimeo.com/89520368


Is this coming to Brigade as well? That would be a dream come true!!

Analogue Light Modelling might give a much higher picture quality than it could ever be possible with path-tracing

Really awesome GTC presentation which reminded me of Brigade: Blur Studio using real-time path tracing with vray rt in Motion Builder for live motion captured performances: http://nvidia.fullviewmedia.com/gtc2014/S4855.html (starts at 14:00 mark)



Pixar also showed real-time path tracing in Katana at GTC. I predict that next year every studio will be doing RTPT :)

A.S. No cooling system is required anymore !














The current-generation 4D-graphics {superphenomenally advanced doxel engine + hyperrealistic direct light modelling + highly accurate physics engine + character motion capture by means of an exceptionally fast room-temperature superconducting camera} video game console :

* Room-temperature superconductor {pioneered by Derunov V.L., Soviet Union, 1978 (if not earlier); proved at Cambridge University, United Kingdom, in 2010} ‘bipolar’ {can as well utilize only one type of charge carriers which should make the even faster} transistors {Dayem bridge Josephson junction on purest Teflon isolator} & room-temperature superconducting wire

* Emitter-Coupled Logic

* Explicit Data Graph Execution {non- von Neumann ‘tile’ architecture}

* Ternary logic {combinational solely or with pulse-driven sequential}

* Unified 8-threaded core with machine belt architecture

* Multilayered integrated circuit

* 100-exabyte Hyper CD-ROM

* Mercury programming language

** 100-inch very high-resolution Nanotube Emissive Display

** Carbyne fibre diaphragm single magnetic-levitationally-hung open-baffle full-range loudspeaker

** Room-temperature single-electron superconductor extremely low noise transistor {developed at the Moscow State University} single-ended purest Class-A no-negative-feedback signal amplifier with room-temperature superconducting accumulator

** Single bendable nanotube Teflon-isolated cable

Sam, you should take a look at this: http://www.youtube.com/watch?v=nnaz8q6FLCk

I bet Brigade can do the same with almost no noise

Brigade in UE4 would be epic! it's possible the source code is open to subscribers.

The only thing that would be epic with current technology is Carbon physics engine from Numerion Software .

Don't want to spam, but I'm working on something similiar : https://www.youtube.com/watch?v=dL_SxY2Njq4


Can't provide a lot of details, as I applied to present it at SIGGRAPH, but I can say it's really simple to implement, and can be extended a lot

Presently, room-temperature S-S-S Josephson heterostructure should reach 10 THz while remaining cool.







How to accelerate existing hardware right now:

~ Microthreads

~ 3-nanometre 3D-FinFETs [Korea, 2006]

~ SRAM

~ graphene wiring

# IBM POWER processor must be single-core and take advantage of super-threading's lowering memory latencies by utilizing all suitable kinds of instruction-level parallelism.

A.S. No cooling system is required anymore !














The current-generation 4D-graphics {superphenomenally advanced doxel engine + hyperrealistic direct light modelling + highly accurate physics engine + character motion capture by means of the fastest room-temperature superconducting camera} video game console :

* Room-temperature superconductor {pioneered by Derunov V.L., Soviet Union, 1978 (if not earlier); proved at Cambridge University, United Kingdom, in 2010} ‘bipolar’ {can as well utilize only one type of charge carriers which should make the even faster} transistors {Dayem bridge Josephson junction on purest Teflon isolator / S—S—S heterostructure} & room-temperature superconducting wire

* Emitter-Coupled Logic

* Explicit Data Graph Execution {non- von Neumann}

* Ternary logic {dynamic combinational in tandem with pulse-driven sequential}

* Unified 8-threaded core with machine belt architecture

* Multilayered integrated circuit

* 100-exabyte Hyper CD-ROM

* Mercury programming language

** 100-inch very high-resolution Nanotube Emissive Display

** Carbyne fibre diaphragm single magnetic-levitationally-hung open-baffle full-range loudspeaker

** Room-temperature single-electron superconductor extremely low noise transistor {developped at the Moscow State University} single-ended purest Class-A no-negative-feedback signal amplifier with room-temperature superconducting accumulator

** Single bendable carbon nanotube Teflon-isolated wire

The new game engine from Silicon Studio looks very photoreal, on par with path traced images but without noise: https://www.youtube.com/watch?v=ErWicf6yuDo


I remember reading somewhere that OTOY integrated Brigade in the Yebis engine, which is made by these same guys. Does this new engine have Brigade tech under the hood?

Instead of just trying to implement the lossy lighting schemes, one of which is definitely path tracing, one could quite easily increase the amount of textures and overall quantity of shaders as soon as the modern hardware adopts all of the abovementioned improvements, and especially with the newish physics engine this might already be hard on it. So that you're sailing a wrong direction..

The 400 petabyte per second Internet connection possible nowadays will transmit a full Hyper CD-ROM game in only 25 seconds which will aid to spread such applications very easily across the net !!!

* >4 minutes, to be correct

In the brand-new console, room-temperature superconductor pure combinational ternary ECL SRAM will apparently be used for registers.

Just another trick to have seriously improved upon modern hardware: Source-coupled logic .

A.S. Presently, room-temperature S-s-S Josephson heterostructure reaches 10 THz pure frequency while remaining ideally cool at any computational load.













So, to substantially increase the performance of either currently existing CPUs and GPUs, manufacturers should only resort to:

* Source-coupled logic

* 3-nanometre 3D-FinFETs for the first time created in Korea yet in 2006

* Microthreads

* SRAM

* Graphene wiring

* Super-Threading (requires single core but reduces memory latencies)

That's it! As you can see, none of these items does anyhow notably increase TDP, provided, several modern techs typically found in hardware is fairly to no avail has been avoided and overridden (Intel's RISCiness, for instance).

Overall performance increase may first of all be measured without coolers, etc., at +19°C 100% humidity as it is room temperature as well and dew drops are known to cause cool-effect on electronics and machinery.

All-in-all, the preliminary increase measure hardly gives way to correct digits since a decent Linux server from IBM has already up to 1 TB operating memories, hence, their devices, albeit incredibly expensive {the console which is clearly the fastest specifically computer in all the history could freely sell for only 500$}, offers a great potential for game developers (indies, in particular) to right today deliver all the best modern technology is capable of!

A.S. No cooling system at all is required anymore !










The current-generation 4D-graphics {superphenomenally advanced doxel engine + hyperrealistic direct light modelling + highly accurate physics engine + character motion capture by means of the fastest room-temperature superconducting camera} video game console :

* Room-temperature superconductor {pioneered by Derunov V.L., Soviet Union, 1978 (if not earlier); proved at Cambridge University, United Kingdom, in 2010} ‘bipolar’ {can as well utilize only one type of charge carriers which might have made the still faster} transistors {Dayem bridge Josephson junction on purest Teflon isolator / S—s—S heterostructure} & room-temperature superconducting wire

* Emitter-Coupled Logic

* Explicit Data Graph Execution {non- von Neumann}

* Ternary logic {dynamic combinational & asynchronous sequential}

* Unified core with ECL SRAM & machine belt architecture

* 3D integrated circuit

* 100-exabyte Hyper CD-ROM

* Mercury programming language solely oriented hardware

Derunov's multilayered superconductor has NO electrical resistance at all within the temperature range of from -196°C to +346°C .

Obviously, an Intel Pentium IV would lack speed due to its core's inherent CISC nature.

How to finally implement a decent operating system, to replace, particularly, the Microsoft's crap once and for all:




* SPIN Operating System {NO-KERNEL}

* Modular Megalithic Kernel

* Retrieve BeOS 5 Pro complete source code from Access Inc.

Hi! I have just tried out this Adaptive Manifold Filter and it's awesome! You can avoid texture blurring if you supply texture information to the filter. But it works poorly with glass material. It might be better with more info like secondary bounce colors or something.

Success in operation of transistor with channel length of 3 nm :


it was verified that scattering effects are repressed inside the 3 nm-long channel, resulting in a quasi-ballistic flow of electrons. This suggests that an electric current can flow without energy loss. Consequently, reduction in power consumption of integrated circuits is expected.

IBM POWER9 processor might be based on the following :








* 770 GHz {at the room-temperature} heterojunction bipolar transistors

* Emitter-Coupled Logic

* Microthreading

* SRAM {made up of the aforementioned transistors}

* graphene wiring

** SPIN OS {a nearly ‹lossless› operating system}

*** Mercury programming language provides excellent optimizations capability

Just one american university is all set to present an integrated circuit consisting of millions of superconducting Josephson junctions .

Thus, any graphics card could be made out of 770-gigahertz bipolar transistors {still fastest in the world}, Emitter-Coupled Logic {fastest ever}, ECL SRAM {currently the most efficient}, graphene wire {which is more conductive and reliable compared to copper and silver}, thereby have nearly the highest performance.

Dubbed "nano emissive display" (NED), the new technology




developed by Motorola, Inc. enables manufacturers to design

large flat panel displays that exceed the image quality

characteristics of plasma and LCD screens at a lower cost.

Motorola currently (2005) is in discussions with electronics

manufacturers in Europe and Asia to license the technology for

commercialization.

NED technology is potentially the cheapest and best alternative

to CRT and LCD screens and is easily scalable. The technology

could be used by ad agencies erecting monolithic 100-inch

roadside billboards. With technology like this being available,

who in their right mind would purchase a plasma display.

"Motorola is ready to deliver this technology to manufacturers today" "We estimate that this technology can be commercialized in the very near term, depending on the aggressiveness of the licensees."

"Motorola's NED technology is demonstrating full colour video with good response time," said Barry Young, the CFO of DisplaySearch. "According to a detailed cost model analysis conducted by our firm, we estimate the manufactured cost for a 40-inch NED panel could be under $400."

So, a NED display can be realized in room-temperature superconducting single-electron transistors with the lowest shot/flicker noise digits plus carbon nanotube wire with reduced skin effect and thermal noise.

Bipolar Transistor Scaling Roadmap still reads that the devices should break 1.4 THz cutoff frequency barrier yet at 32 nm die shrink

By the way, NED displays have no scanning at all !!!

yes, i agree. NED displays are more alive than this blog. so go ahead,

the hype is over...

The ultimate no-operating-system voxel-based Direct-Light-Modelling 3D-graphics gaming solution being completely possible already today and requiring no cooling thanks to Vladimir Leonidovich Derunov from the glorious Soviet Union !








* Room-temperature superconductor ‘monopolar’ transistors on S—graphene—S heterostructure on purest Teflon isolator

* Emitter-coupled logic

* Explicit Data Graph Execution

* Ternary dynamic combinational / asynchronous sequential logics

* Unified core with machine belt architecture

* Tridimensional integrated circuit with room-temperature superconducting wiring

* Mercury programming language

I want whatever the dude making up half of the comments on this post is smoking...

(Tl5Pb2)Ba2MgCu10O20+ superconducts at about +18.5°C





















so now a fantastically powerful supercomputer can already be built exclusively for gaming utilizing solely the following

* The superconductor ‘monopolar’ transistors based on S—graphene—S heterostructure on purest Teflon isolator

* Emitter-coupled logic

* Explicit Data Graph Execution

* Ternary dynamic combinational / asynchronous sequential logics

* Unified core with fattest lots of ECL SRAM & belt machine architecture

* Tridimensional integrated circuit with the superconductive wiring

* Mercury programming language

_ _ _ _ _ _ _

Meanwhile, for ordinary mortals' needs a quite advanced "all-in-one" RISC-based non-silicon computing device could be created, just take a look:

* 770 GHz heterojunction bipolar transistors

* Emitter-Coupled Logic

* Microthreading {should not be confused with Micro-Threading}

* SRAM

* Ultraconductor wiring

* SPIN OS

* Mercury programming language

_ _ _ _ _ _ _

Thus, the abovementioned superconducting supercomputer will be capable of real-time handling as purely voxel 3D graphics as Direct Light Modelling technique, plus the sound might be provided by Linear LTC2380-16.

Superconducting single-electron transistors in a NED dispaly can be interconnected via superconductive wire .

@Sam,


any update on Brigade? Is it feasible to implement Brigade into Unreal Engine 4?

everything is dead and sam

got fired ! lets go back to real

stuff...

Probably Oculus VR bought the Brigade team for a virtual retinal scanned foveated real-time ray traced SUPER AWESOME VR simulation.

I wonder which new display tech Palmer Luckey that would make the thing significantly lighter was talking about

in a recent interview.

Sam, what's your take on the "Ray Histogram Fusion" paper?


It looks like it would solve the noise problem of path tracing.

Look at that: http://dev.ipol.im/~mdelbra/rhf/

Is this blog extincted? ;)

Hoping your on the cusp of another cool blog post, understanding if you're not.

We want to see more stuff....what is going on? I really hope brigade is going to see the light some day...




By the way: did anyone think about this chip ? it could help

http://www.wired.com/2014/08/ibm-unveils-a-brain-like-chip-with-4000-processor-cores/

“The chip is designed for real-time power efficiency.” Nobody else, he claims, “can deliver this in real time at the vast scales we’re talking about.”

Maybe the silence has sth to do with

an aqcuisition by a larger company.

Looks like a sudden NDA death.

Brigade team is now sitting in LA,

40 miles from Oculus.

I could imagine sth like a VR gold rush. ;)

We could always hope, but this engine is pretty heavy to drive as it is and VR needs good framerates to be an enjoyable experience, so I doubt it..

Very useful and helpful post you are.

Post a Comment