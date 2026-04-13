---
title: 'GPU path tracing tutorial 2: interactive triangle mesh path tracing'
url: http://raytracey.blogspot.com/2015/12/gpu-path-tracing-tutorial-2-interactive.html
author: Sam Lapere
published: '2015-12-01'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

While the tutorial from the previous post was about path tracing simple scenes made of spheres, this tutorial will focus on how to build a very simple path tracer with support for loading and rendering triangle meshes. Instead of rendering the entire image in the background and saving it to a file as was done in the last tutorial, this path tracer displays an interactive viewport which shows progressively rendered updates. This way we can see the rendered image from the first pass and watch it converge to a noise free result (which can take some time in the case of path tracing triangle meshes without using acceleration structures).

For this tutorial I decided to modify the code of a real-time CUDA ray tracer developed by Peter Trier from the Alexandra Institute in 2009 (described in



[this blog post](http://cg.alexandra.dk/?p=278)), because it's very compact, does not use any external libraries (except for CUDA-OpenGL interoperability) and provides a simple obj loader for triangle meshes. I modified the ray tracing kernel to handle path tracing (without recursion) using the path tracing code from the previous tutorial, added support for perfectly reflective and refractive materials (like glass) based on the code of smallpt. The random number generator from the previous post has been replaced with CUDA's own random number generation library provided by curand(), which is less prone to patterns at low sample rates and has more uniform distribution properties. The seed calculation is based on a trick described in a post on[RichieSam's blog](http://richiesams.blogspot.co.nz/2015/03/creating-randomness-and-acummulating.html).**Features of this path tracer**

- primitive types: supports spheres, boxes and triangles/triangle meshes

- material types: support for perfectly diffuse, perfectly reflective and perfectly refractive materials

- progressive rendering

- interactive viewport displaying intermediate rendering results

Scratch-a-Pixel has some excellent lessons on ray tracing triangles and triangle meshes, which discuss barycentric coordinates, backface culling and the fast Muller-Trumbore ray/triangle intersection algorithm that is also used in the code for this tutorial:


- ray tracing triangles:


- ray tracing polygon meshes:



- ray tracing triangles:

[http://www.scratchapixel.com/lessons/3d-basic-rendering/ray-tracing-rendering-a-triangle](http://www.scratchapixel.com/lessons/3d-basic-rendering/ray-tracing-rendering-a-triangle)- ray tracing polygon meshes:

[http://www.scratchapixel.com/lessons/3d-basic-rendering/ray-tracing-polygon-mesh](http://www.scratchapixel.com/lessons/3d-basic-rendering/ray-tracing-polygon-mesh)


**Some screenshots**



**Performance optimisations**

- triangle edges are precomputed to speed up ray intersection computation and triangles are stored as (first vertex, edge1, edge2)

- ray/triangle intersection uses the fast Muller-Trumbore technique

- triangle data is stored in the GPU's texture memory which is cached and is a bit faster than global memory because fetching data from textures is accelerated in hardware. The texture cache is also optimized for 2D spatial locality, so threads that access addresses in texture memory that are close together in 2D will achieve best performance.

- triangle data is aligned in float4s (128 bits) for coalesced memory access, maximising memory throughput, (see

[https://docs.nvidia.com/cuda/cuda-c-programming-guide/#device-memory-accesses](https://docs.nvidia.com/cuda/cuda-c-programming-guide/#device-memory-accesses)and[http://blog.spectralstudios.net/raytracing/realtime-raytracing-part-3/#more-573](http://blog.spectralstudios.net/raytracing/realtime-raytracing-part-3/#more-573))
- for expensive functions (such as sin() and sqrt()), compute fast approximations using single precision intrinsic math functions such as __sinf(), __powf(), __fdividef(): these functions are performed in hardware by the special function units (SFU) on the GPU and are much faster than the standard divide and sin/cos functions at the cost of precision and robustness in corner cases (see

[https://docs.nvidia.com/cuda/cuda-c-programming-guide/#intrinsic-functions](https://docs.nvidia.com/cuda/cuda-c-programming-guide/#intrinsic-functions)
- to speed up the ray tracing an axis aligned bounding box is created around the triangle mesh. Only rays hitting this box are intersected with the mesh. Without this box, all rays would have to be tested against every triangle for intersection, which is unbearably slow.

In the next tutorial, we'll have a look at implementing an acceleration structure, which speeds up the rendering by several orders of magnitude. This

[blog post](http://robbinmarcus.blogspot.co.nz/2015/10/real-time-raytracing-part-2.html)provides a good overview of the most recent research in ray tracing acceleration structures for the GPU. There will also be an interactive camera to allow real-time navigation through the scene with depth of field and supersampled anti-aliasing (and there are still lots of optimisations).
References

## 46 comments:

Amazing tutorials! Thanks Sam :)



-Juanjo

I always look forward to your blog posts Sam. Though I am a newb at CUDA and can never seem to get the demos running - I have them compiling and linked to the 64bit libs but my display driver always crashes (GTX770) I have ran the CUDA 7.5 samples fine, use VS2013 and have compiled numerous other related graphics demos. I really want to get it working. Some things I think will be awesome - interpolating the triangle normals based on vertex normals for fake smooth surface). I also have an idea for an optimal acceleration structure in mind (balanced hybrid BVH/Octree, split on AABB dimension mid-points).

Muchos gracias Juanjo! And great to see you're following my blog. I think you will like the next tutorial even more.





Anon: no worries, getting code compiled with CUDA can be quite hairy sometimes. I've been using the CUDA 6.5 toolkit (can't use any older version because of my Maxwell card) and VS2013 Community Edition (free version with 64-bit support) which comes with native NSight support for CUDA performance profiling, but the VS2013 Express should work just as well.

Some steps that might help:

- install the CUDA 6.5/7/7.5 toolkit and choose integration with Visual Studio

- open VS2013 (Express or any other version)

- click New Project...

- select Visual C++, then General, then Empty Project

- right click on the project, select Build Dependies > Build Customizations

- select the CUDA 6.5 (or 7 or 7.5) checkbox, click OK

- in the project explorer window, right click on Source Files, select Add, C++ file, then change the name from "Source.cpp" to "Source.cu"

- in the project explorer window, right click on the newly created Source.cu file, select CUDA C++

- paste all the code from the tutorial in the file

- right click on the project name, select Properties

- under Linker > Input, add "cudart.lib" (without the quotes) to Additional Dependencies

- select Build > Rebuild Solution

Let me know if you still have trouble compiling the code.

Btw, I had a similar idea for a hybrid BVH/Octree that I'd like to try. I'm also working on a technique that could theoretically provide truly noiseless global illumination without the need for screen space filtering (inspired by a research paper from Weta Digital, but with a twist).

Thanks for the help Sam, I think I tried everything on your list but I will start again with a fresh install and make sure nothing else is interfering. The noiseless global illumination sounds interesting, I assume it based on the paper Importance Sampling Microfacet-Based BSDFs using the Distribution of Visible Normals. Do you think you will be able to achieve a high enough sample to remove the noise?


I have also thought about the noise problem and think the noise could be minimised by performing the collision test (after the first bounce) on a low resolution model of the scene , approximating the surrounding light (similar to sampling used with voxel cone tracing, described in The Technology of Tomorrows Children).

Anon, interesting paper, but the one I had in mind is related to the Pantaray engine developed by Pantaleoni.


The voxel cone tracing from the Tomorrow Children is really impressive and the GI approximation seems to work quite well. It's probably the first game that actually uses voxels for real-time global illumination. I think multiresolution geometry representations (multiple levels of detail) that are independent of the scene's complexity such as voxels, surfels or signed distance fields are key for real-time GI that doesn't require UV parameterisation (unlike Enlighten in Unity, which they confusingly call Precomputed Realtime GI: http://blogs.unity3d.com/2015/11/05/awesome-realtime-gi-on-desktops-and-consoles/).

Btw, CryEngine supports real-time sparse voxel octree GI as well:



http://docs.cryengine.com/display/SDKDOC2/Voxel-Based+Global+Illumination

Video: https://www.youtube.com/watch?v=-7U6JgbFCVM

Hey Sam!



Nice post and good to see your path tracer is progressing! Do you have any statistics on how fast it's currently running?

I'm currently moving my blog (spectral studio) to my own blog, because the site is going to be discontinued. You can find a nice overview with new links here: http://robbinmarcus.blogspot.com/p/tutorials.html.

Thanks Robbin. I haven't bothered doing any time measurements with this code, because each ray hitting the bounding box around the triangle meshes is tested against all triangles. The path tracer in the next tutorial will use an acceleration structure, I'll post some stats then.

Some videos leaked out of the PowerVR PC hardware ray tracing GPU have you seen them? What do you think?




The translations are poor and I would have preferred higher quality video but it looks like they did 4 x GR6500 cards to get 30fps @ 1080p and 1 card to get 30fps at 1280×720

https://translate.google.co.uk/translate?sl=ja&tl=en&js=y&prev=_t&hl=en&ie=UTF-8&u=http%3A%2F%2Fwww.4gamer.net%2Fgames%2F144%2FG014402%2F20151117095%2F&edit-text=

https://www.youtube.com/watch?v=VE5bpQgpKQA

https://www.youtube.com/watch?v=A0keJiuEKdg

https://www.youtube.com/watch?v=NGWKcpJOdLk

https://www.youtube.com/watch?v=hsOuj3V4Adw

Thanks for the links, I had seen some of them before. Funny that they're using the same Stonemason scene that I've used for my ray tracing experiments from 2012 (http://raytracey.blogspot.co.nz/2012/05/real-time-path-tracing-urban.html). What's shown in these videos still looks like Whitted ray tracing (no global illumination) to me. The level of realism that can be achieved with traditional game engines like CryEngine, Frostbite, Unreal Engine, id Tech 6 etc looks miles better than this and doesn't require any special RT hardware. But you have to start somewhere.

Just a couple of sentences, as quoted: «In my opinion, the main advantage of fast hardware is not that the graphics get rendered quicker, but that clever algorithms are not that necessary anymore, meaning that straight away approaches (those which are actually the most intuitive of all) can be directly coded and a result can be expected in a reasonable amount of time. 20 years ago expensive techniques required the implementation of clever, complex and obscure algorithms, making the entry level for the computer graphcis hobbyist much higher. But thanks to new hardware that's not true anymore - today, writing a global illumination renderer takes one hour at most.»


Now, if you really consider path tracing {as opposed to Brute-Force rendering that is better} the shortest way towards faithful real-time rendering presentation, then why the hell don't you resort to all available means?! Thus, it comes that the faster the hardware the mangier the work done by a lousy programmer! Don't get yourselves down on the level of Windows inventors! More of that: with ECL, we could already have been on the very top of computational possibilities!

Jenson, simple path tracing is already being "augmented" with more clever sampling schemes to some extent. Look for example at Arnold, one of the very first production path tracers, which predominantly uses unidirectional path tracing (although they are also working on bidirectional PT and vertex connection and merging (VCM), which unifies photon mapping and bidirectional pt). Unidirectional PT is easier to extend with more sophisticated variance reducing sampling strategies like QMC (quasi Monte Carlo). Some optimisation tricks that work for unidirectional PT don't work with bidirectional PT or Metropolis Light Transport. MLT is highly overrated. It can be very useful in some scenes with very difficult indirect lighting (small light sources, light coming through a keyhole or light splitting through a prism), but for most everyday scenes it performs much worse than a well-implemented path tracer. This is because MLT cannot take advantage of any sort of sample ordering (e.g. quasi-Monte Carlo sampling). An MLT renderer must fall back to pure random numbers which greatly increases the noise for many simple scenes (like an open skylight scene).

“Thanks for the links, I had seen some of them before. Funny that they're using the same Stonemason scene that I've used for my ray tracing experiments from 2012 (http://raytracey.blogspot.co.nz/2012/05/real-time-path-tracing-urban.html). What's shown in these videos still looks like Whitted ray tracing (no global illumination) to me. The level of realism that can be achieved with traditional game engines like CryEngine, Frostbite, Unreal Engine, id Tech 6 etc looks miles better than this and doesn't require any special RT hardware. But you have to start somewhere.”






It can do global illumination as it was one of the things talked about at the graphics show GDC. I have no idea if they are using global illumination in those demos as the quality of the videos isn’t good enough for me to tell either way. It looks to me as the hardware is very capable it’s a choice of the demo coders and the type of demo/app being created.

Each demo was design to show off a different thing the Stonemason style demo was meant to demonstrate how Ray Tracing can be used in a hybrid rasterized GPU engine to provide a number of benefits. Which is a reduction in development time for the map, 50% reduction in memory bandwidth and doubling of the performance for the entire frame while improving the shadow quality by using RT for lights and shadows over cascaded shadow maps on a traditional rasterized GPU.

Its unsurprising considering the company’s background, they seem to be pushing RT for its speed, bandwidth and power consumption benefits over a rasterized method. I think there goal is to get the devs used to a hybrid approach before moving over to a full RT approach in a few generations.

Getting back to being more related to your blog. Assuming the hardware is better at RT then NVidia GPU’s which I am not saying it is as I haven’t seen a good enough comparison. Could it be worthwhile getting your hands on one of the PC cards and running your path tracing demos on it? Is it doable without too much work to port your code over? Would there be any benefits coding for this RT card over NVidia cards?

RayTracingFan, you're starting to sound like a viral marketeer for Imagination Technologies, but that's alright.



Anyway, from what I've read and remember of the Caustic hardware, I'm not really interested in trying it out as it's not flexible enough for my purpose. I read Caustic's OpenRL spec a few years ago and it looked like you're forced to use the primitive types, intersection routines and acceleration structure that come with the package, which is why a prefer CUDA/OpenCL where you've got a lot more flexibility. I'd love to be wrong though, as I haven't looked too deep in what the PowerVR Wizard GPU and the new ray tracing API is capable of. So if I can get my hands on a ray tracing PC card, I would definitely try out some ideas (assuming that by PC card you mean a PC version of the mobile Wizard GPU and not the Caustic One or Two which lacked shading hardware and was therefor slower than GPU based ray tracing).

On a sidenote, one thing I believe being worth accelerating in dedicated fixed function hardware is noise filtering. The recent high quality denoisers take up several seconds to minutes to denoise an image (see for example https://corona-renderer.com/forum/index.php/topic,10073.0.html), which is way too slow. If some of those computations could be offloaded and accelerated in dedicated hardware (like texture filtering is currently done), it would allow simultaneous rendering and filtering in pretty much real-time.

Just looked in more detail at the PowerVR GR6500 specs ("24 billion node tests per second and 100 million dynamic triangles per second", impressive if true) and API. I've got some ideas to speed up the computation of noise free indirect lighting to real-time speeds (involving Delaunay triangulation), which is reasonably easy to do in CUDA. There might actually be a way to trick the PowerVR hardware into doing something it wasn't intended for, but is absolutely necessary for my idea to work.

Did anyone see those images? IMO at two indirect bounces VXGI is starting to look Very interesting.


https://www.reddit.com/r/pcgaming/comments/35dqd8/workinprogress_vxgi_multibounce/

This one also has two indirect bounces. https://www.youtube.com/watch?v=eqvDdBbvoFk

Interesting times ahead, definiteley.

All techniques are converging towards the holy grail of realtime CG. XD

Also, precomputed realtime GI (what?,lol) in Unity 5 can look awesome. https://www.youtube.com/watch?v=4OjoADLPfbI

I'm not a fan of voxel based GI, just seems a rough means to an end. It's very "hacky" like most other rasterizer techniques. You have to voxelize and mipmap all properties of dynamic geometry every frame which is excessively costly for both construction and memory, and it still has a very "biased" look in motion from the filtered blockiness of the voxelization resolution. VXGI will likely just be a passing thing until we get pathtracing where it needs to be.

@CHris


you are right. Converging was a wrong term i used.

how far away is path tracing really?

who really knows.

Sam, there you're pondering over additional techniques that may better path tracing, not over improved optimization of written code.


Meanwhile, Nvidia and Intel are the worst that could befall to computer industry.

@Retina: yep, I think voxel based GI is a sensible intermediary solution for real-time GI until voxels become small enough that regular path tracing can take over. There are actually better ways than voxels to approximate geometry, so they might become obsolete sooner than you think.


Jenson: there are also plenty of techniques to optimise GPGPU code like stream compaction, data prefetching, loop unrolling, using intrinsics and shared memory, etc.

Presently, curve modelling & tracing every photon in a scene are to be considered the future. These techniques, in tandem with several others, can be possible with ultra-modern Emitter-Coupled Logic solely. But if current manufacturers are all set to keep on fooling around with their hardware trash, then nothing good for real-time tridimensional computer graphics should be expected anytime soon.

@Sam Lapere


i really hope so. Currently i am drunk of the Enlighten GI implemented in Unity 5.

The Courtyard demo is so breathtakingly beautiful. (modified it also with a blue sky.)

Sth completely different.

My God i wish i could be there now in VR. XD

Sam: language choice does not influence in terms of program performance on the final result ?

@Jenson Button


The host language does not matter so much, but for the best performance you're looking to work in a language that works on the GPU. This could be CUDA, OpenCL or even compute shaders from DirectX or openGL.

@ Robbin Marcus


As understood: language level & its declared advantages cannot gain performance ?

@Jenson Button



If you take perspective of consumer hardware in the form of a PC with a CPU and GPU, there are some hard limits on calculation speed and memory bandwidth. Theoretically, with any provided framework you should be able to achieve speeds up to this limit. Of course, this task is not trivial. Every language has its own interface to communicate with the hardware.

There are advantages over one language in comparison to others, but this is more a personal preference I would say.

The language level can increase your performance: if you write code and cross reference the compiled code (low level) with the intended workings, you may notice some redundant work. However, writing the complete algorithm in this compiled form would cost more valuable time than it would increase performance eventually.

@ Robbin Marcus


Then, what would you say about declarative languages being intrinsically better than imperative ones?

@Jenson Button


Declarative is shorter to write down what you actually want, but you lose control of the workings itself. I'd say you can't really have one without the other. I think over some time the solution is to have a basic functional or declarative basis with an imperative core you can tweak when necessary. Much like existing ray tracing frameworks like Optix or FireRays offer these functional solutions to global illumination, however still not open source.

That meaning: you lose control of the workings itself, even when the declarative language is based on solving problems using constraints given to the program, rather than using an algorithm written by a programmer?

> there are some hard limits on calculation speed


Yes, limitless is only the greediness of the top management of the computer hardware companies. Hopefully, somewhere around 2130, Intel/Nvidia might have finally achieved today's level of computer technology. We shall be waiting impatiently.

Intel/Nvidia/AMD have bottom-lines like any company, I'm sure they could create something better suited for pathtracing, but the money doesn't point there right now. Nvidia is happy to support software that doesn't break the hardware cycle (like Optix or VXGI), but a hardware-cycle-breaking change is very very unlikely.


The only thing we can do is create better software to compliment Moore's law and expedite the time until pathtracing is "here". The good news is we are nowhere near the apex of software's contribution; new intersection and sampling routines are constantly improving with new research. Keep your ears to the wall ;)

Now, let's briefly summarize the situation:


of about 23000 races that inhabit our galaxy {located in the 17th of currently almost 47 Creations each accommodating hundreds and thousands of Universes}, the humankind is one of the least advanced, i.e. still being Low-End. Of course, there are High-End Civilizations that used to live in the centre of Milky Way, but their main value is Cosmic Love {comprises eight true virtues; shouldn't be confused with Goodness, which is just the anti-Evil active/defensive energies kit of the Lord} & they act strictly together with the Creator, a complex of multiple Monadic arrays which were born by the infinite ocean of Primary Matter that had always existed, and, apart from the Greatest Tibetan Teachers, there were also Christ & Lenin, the two famous Genii of Earth called for to crusade against Cosmic Evil, a very mighty formation off Space-Time deviation, that totally rules on Earth. And there are Middle Civilizations that actively use the so-called Continuous Logic of Cognition, otherwise simply known as 'integrated thinking'. And what I had to say is that the latter is the only thing by means of which the earthly hardware can be fabulously improved.

I just created a subreddit for realtime pathtracing if anyone wants to have discussions there instead of spamming Sam's blog:



/r/pathtracing

@Sam Lapere - would love to see ya there :)

Good idea, Chris. I'll join the discussion when I find some time.

With ECL hardware I already now am looking absolutely not towards, but straight beyond any sampled rendering techniques, currently being deified, that are inevitably flawed. This is in contrast to the senseless view of the dreamers that have started /r/pathtracing which I shouldn't haunt.

Ironically, you cannot even make perfect digital 3D models, but yet dreaming of a highly computer performance intensive rendering technique.


Intel/Nvidia hamper, who will finally begin with producing extremely fast computer hardware required for graphics?

Athbhliain faoi mhaise daoibh !

WTF???



https://www.youtube.com/watch?v=EgMy5dqAl_U

https://www.youtube.com/watch?v=MnIlpoamQYc

Nice find Jenson! I almost lol'ed :D. This must be your most on topic comment so far.

Have you run path tracing stuff on one Nvidia GeForce GTX Titan X piece of shit ?


How is the overall performance ?

Brochure iBrouchure with numerous exceptional capacity to make your undertaking intriguing. It tells the story and interactive.


Hey Sam, I couldn't get it to work either and seem to have the same problem as Anon on Dec 2. It appears to compile fine, although there are some warnings, but when I run it I just get a display driver crash. I'm also using cuda 7.5 so maybe there's an incompatibility there.



Any advice?

Cheers, Tristan.

Hi Tristan, thanks for letting me know. I fixed it and updated the code on github. The problem was in the way the VBO got created. It should run fine now.

Appreciate it! Thanks.

Hi Sam! There are two questions I want to ask:

1. When the material is "Diffuse", you wrote "mask *= f", shouldn't it be "mask *= f * dot(d, nl) * 2"?(considered the inverse pdf, ρ and cosine coefficent)

2. When the material is "Refractive", the incoming ray should split into two rays: reflected ray and refracted ray(ignore total internal reflect). But in your code, you randomly choose one kind of ray, is it reasonable? I know it's hard to deal with this in a non-recursive function:(

Hi Berry,



1. you're right, I forgot to multiply the colour with a cosine factor, thanks for pointing that out. The "2" factor could be anything really, it's just a fudge factor to make the scene look brighter

2. that's how it works for Whitted ray tracing, path tracing on the other hand doesn't split rays, but randomly chooses one type of ray according to some probability distribution function. It's how path tracing works (both on CPU and GPU) and is not a limitation of non-recursive tracing on the GPU (every recursive algorithm can be converted to an iterative one by keeping a stack).

Post a Comment