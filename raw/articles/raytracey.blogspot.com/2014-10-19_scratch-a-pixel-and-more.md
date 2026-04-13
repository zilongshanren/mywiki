---
title: Scratch-a-pixel and more
url: http://raytracey.blogspot.com/2014/10/scratch-pixel-and-more.html
author: Sam Lapere
published: '2014-10-19'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Having left Otoy some time ago and after enjoying a sweet as holiday, it's time for things new and exciting. Lots of interesting rendering related stuff happened in the past months, below are some of the most fascinating developments in my opinion:

- starting off, there's an excellent online tutorial series on computer graphics (mostly ray tracing) for both beginners and experts called

[Scratch-a-Pixel](http://scratchapixel.com/). The authors are veterans from the VFX, animation and game industry and have years of experience writing production rendering code like Renderman. The tutorials deal with all the features that are expected from a production renderer and contains a lot of background and insights into the science of light and tips and tricks on how to write performant and well optimized ray tracing code. Rendering concepts like CIE xyY colorspace and esoteric mathematical subjects like discrete Fourier transforms, harmonics and integration of orthonormal polynomials are explained in an easy-to-digest manner. Most tutorials also come with C++ source code. At the moment some sections are missing or incomplete, but the author told me there's a revamp of the website coming very soon...
- hybrid rendering (rasterization mixed with ray tracing) for games has finally arrived with the recent release of Unreal Engine 4.5 which supports ray traced soft shadows and ambient occlusion via signed distance fields (which can be faster to compute than traditional shadow mapping, but works only for static geometry):

[https://docs.unrealengine.com/latest/INT/Engine/Rendering/LightingAndShadows/RayTracedDistanceFieldShadowing/index.html](https://docs.unrealengine.com/latest/INT/Engine/Rendering/LightingAndShadows/RayTracedDistanceFieldShadowing/index.html)
Like voxels or triangles, distance fields are another way to represent scene geometry. Just like voxels, distance fields approximate the scene geometry and are more efficient to trace than triangles to create low frequency effects like soft shadows, ambient occlusion and global illumination that don't require 100% geometric accuracy (and because they have inherent multiresolution characteristics by approximating the scene geometry). Inigo Quilez wrote a few interesting articles on rendering with distance fields (in 2008):

[Free penumbra shadows for raymarching distance fields](http://www.iquilezles.org/www/articles/rmshadows/rmshadows.htm)

More on distance fields:

[Distance fields in Unreal Engine](http://www.tomlooman.com/distance-fields-unreal-engine/)

There's also a very recent paper about speeding up sphere tracing for rendering of signed distance fields or path tracing:

[Enhanced sphere tracing](http://erleuchtet.org/~cupe/permanent/enhanced_sphere_tracing.pdf)
- one of the most interesting Siggraph 2014 surprises, must be the announcement from Weta (the New Zealand based visual effects studio that created the CG effects for blockbusters like the Lord of the Rings, King Kong, Avatar, Tintin and the Hobbit movies) that they are developing their own production path tracer called Manuka (the Maori name for New Zealand's healing tea tree) in conjunction with Gazebo, a physically plausible realtime GPU renderer. While Manuka has been used to render just a couple of shots in "The Hobbit: the Desolation of Smaug", it will be the main renderer for the next Hobbit film. More details are provided in this extensive fxguide article:

[http://www.fxguide.com/featured/manuka-weta-digitals-new-renderer/](http://www.fxguide.com/featured/manuka-weta-digitals-new-renderer/)Another surprise was Solid Angle (creators of Arnold) unveiling of an OpenCL accelerated renderer prototype running on the GPU. There's not much info to be found apart from a comment on BlenderArtists.org by Solid Angle's Mike Farnsworth ("*This is a prototype written by another Solid Angle employee (not Brecht), and it is not Arnold core itself. It's pretty obvious we're experimenting, though. We've been keeping a close eye on GPUs and have active communication with both AMD and Nvidia (and also obviously Intel)*.*I wouldn't speculate on what the prototype is, or what Brecht is up to, because you're almost certainly going to be wrong.*")
- Alex St John, ex-Microsoft and one of the creators of DirectX API, has recently moved to New Zealand and aims to create the next standard API for real-time graphics rendering using CUDA GPGPU technology. More details on his blog

[http://www.alexstjohn.com/WP/blog/](http://www.alexstjohn.com/WP/blog/). His post on his[visit to Weta](http://www.alexstjohn.com/WP/2014/02/15/cuda-6-0-rc/)contains some great insights into the CUDA accelerated CG effects created for The Desolation of Smaug.
- Magic Leap, an augmented reality company founded by a biomedical engineer, recently got an enormous investment from Google and is working with a team at Weta in New Zealand to create imaginative experiences. Info available on the net suggests they are developing a wearable device that directly projects 3d images onto the viewer's retina that seemlessly integrate with the real-life scene via projecting multiple images with a depth offset. Combined with Google Glass it could create games that are grounded in the real world like this:

[http://vimeo.com/109214393](http://vimeo.com/109214393)(augmented reality objects are rendered with Octane Render).
- the Lab for Animate Technologies at the University of Auckland in New Zealand is doing cutting edge research into the first real-time autonomously animated AI avatar:

[http://vimeo.com/97186687](http://vimeo.com/97186687)
The facial animation is driven in real-time by artificial intelligence using concepts from computational neuroscience and is based on a physiological simulation of the human brain which is incredibly deep and complex (I was lucky to get a behind the scenes look): it includes the information exchange pathways between the retina, the thalamic nuclei and the visual cortex including all the feedback loops and also mimics low level single neuron phenomena such as the release of neurotransmitters and hormones like dopamine, epinephrine and cortisol. All of these neurobiological processes together drive the avatar's thoughts, reactions and facial animation through a very detailed facial muscle system, which is probably the best in the industry (Mark Sagar, the person behind this project, was one of the original creators of the USC Lightstage and pioneered facial capturing and rendering for Weta in King Kong and Avatar). More info on

## 15 comments:

That Baby X project is incredible!

Yep, it's even more impressive if you see all the simulations happening under the hood. It's AI model is based on computational cell biology (among others) and is much closer to true biological intelligence than IBM's Blue Brain project. I'm convinced this is the way to achieve self thinking and learning machines with affective behaviour.

Awesome.

Will be cool if someday this tech will be implemented in VR games.

Shiver!

How much computation resources would it take to simulate somewhat emotional intelligent characters.

Hard to say. There's an entire research field called affective computing that deals with recreating emotion in machines. Ray Kurzweil estimates it will take 15 years (in 2029) to achieve computers with human-like emotional intelligence: http://www.cnbc.com/id/101751468

So if you consider that pets can think and show feelings, we should be able to build machines with animal-level intelligence and emotions well before 2029.

Self-thinking is an inherent quality of Matter {should not be confused with infinite Initial Matter which is the basis of all forms of existence, thinkable & unthinkable} if it is being in so-called substantional {astral} form solely.



Fixed matter is incapable of thinking; in fluid & organic forms it can only be a conductor of thinking process, but, yet again, at legislative role of substantional form of it.

Thus, a human does think by means of micro energetic space spheres that are situated right near the head aura.

Good morning Sam,


Could you tell me if it will be integrated in the UE4(5) as a render layer in the next year? (for realtime games)

Are they planning to make an opencl version and some kind of demo with that? (if its not a super secret)

Why dreaming of nothing, instead of just formulating that already is existing ?



















On laboratory solely level the such device can be presently created {apparently, american soldiers will be playing a graphically most advanced Call of Duty game ever}:

* (Tl5Pb2)Ba2MgCu10O20+ room-temperature superconductor ‘Dayem bridge on purest Teflon’ monopolar transistors

* Emitter-Coupled Logic

* Explicit Data Graph Execution

* Ternary — dynamic combinational & asynchronous sequential — logic

* Static random-access memory

* Unified core with Belt Machine Architecture

* Hyper-large-scale tridimensional integrated circuit with (Tl5Pb2)Ba2MgCu10O20+ room-temperature superconductor wiring

* Mercury programming language

* No operating system

For everyday use (including writing-playing real-time 3D-graphics games), an all-in-one (that is without either external video card and RAM) all-purpose processing unit may be produced henceforth:

* 3-nanometre 3D-FinFETs

* Microthreading

* SRAM

* Ultraconductor™

* RISC

* SPIN OS (modified under current Windows programs)

Thence, there is not any other reasonable way to building a computer.

You leaving OTOY means you're not working on Brigade anymore right? Is anybody at this point? It sucks because I really thought it would become a full fledged engine.

1} Will NASA's 80-petaflops 20-watts ZISC processor be sufficient for the project ?


2} Path-tracing was never the ultimate, and couldn't be that by definition: lower computational resources inevitably means lower visual quality. That's that.

Sam is back! Yayyy!

So, are you back at Otoy? I hope so. Brigade needs some help it seems.

Seeker

Hi Seeker, no I'm not at Otoy anymore, check the first sentence of this post ;)

Sam - did you sign a non-compete before you left?

The Scratch-a-pixel tutorial is a true goldmine. Explains many things much clearer than elsewhere on the net.

Good to have you back!

anyone ever heard of VRDisplays?

sounds crazy

Post a Comment