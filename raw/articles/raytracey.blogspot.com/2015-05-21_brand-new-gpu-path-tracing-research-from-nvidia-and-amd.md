---
title: Brand new GPU path tracing research from Nvidia and AMD
url: http://raytracey.blogspot.com/2015/05/brandnew-gpu-path-tracing-research-from.html
author: Sam Lapere
published: '2015-05-21'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

A very interesting paper called "

[Gradient domain path tracing](https://mediatech.aalto.fi/publications/graphics/GPT/)" was just published by Nvidia researchers (coming from the same incredibly talented Helsinki university research group as Timo Aila, Samuli Laine and Tero Karras who developed highly optimized[open source CUDA ray tracing kernels](https://code.google.com/p/understanding-the-efficiency-of-ray-traversal-on-gpus/)for Tesla, Fermi and Kepler GPUs), describing a new technique derived from the ideas in the paper[Gradient domain Metropolis Light Transport](https://research.nvidia.com/publication/gradient-domain-metropolis-light-transport), which drastically reduces noise without blurring details.Abstract

We introduce gradient-domain rendering for Monte Carlo image synthesis. While previous gradient-domain Metropolis Light Transport sought to distribute more samples in areas of high gradients, we show, in contrast, that estimating image gradients is also possible using standard (non-Metropolis) Monte Carlo algorithms, and furthermore, that even without changing the sample distribution, this often leads to significant error reduction. This broadens the applicability of gradient rendering considerably. To gain insight into the conditions under which gradient-domain sampling is beneficial, we present a frequency analysis that compares Monte Carlo sampling of gradients followed by Poisson reconstruction to traditional Monte Carlo sampling. Finally, we describe Gradient-Domain Path Tracing (G-PT), a relatively simple modification of the standard path tracing algorithm that can yield far superior results.

This picture shows a noise comparison between gradient domain path tracing (GPT) and regular path tracing (PT). Computing a sample with the new technique is about 2.5x slower, but path tracing noise seems to clear up much faster, far outweighing the computational overhead:

More images and details of the technique can be found in

[https://mediatech.aalto.fi/publications/graphics/GPT/kettunen2015siggraph_paper.pdf](https://mediatech.aalto.fi/publications/graphics/GPT/kettunen2015siggraph_paper.pdf)
Related to the

[previous post](http://raytracey.blogspot.co.nz/2015/02/real-time-ray-traced-augmented-reality.html)about using real-time ray tracing for augmented reality, a brand new Nvidia paper titled "[Filtering Environment Illumination for Interactive Physically-Based Rendering in Mixed Reality](https://research.nvidia.com/publication/filtering-environment-illumination-interactive-physically-based-rendering-mixed-reality)" demonstrates the feasibility of real-time Monte Carlo path tracing for augmented or mixed reality:Abstract

Physically correct rendering of environment illumination has been a long-standing challenge in interactive graphics, since Monte-Carlo ray-tracing requires thousands of rays per pixel. We propose accurate filtering of a noisy Monte-Carlo image using Fourier analysis. Our novel analysis extends previous works by showing that the shape of illumination spectra is not always a line or wedge, as in previous approximations, but rather an ellipsoid. Our primary contribution is an axis-aligned filtering scheme that preserves the frequency content of the illumination. We also propose a novel application of our technique to mixed reality scenes, in which virtual objects are inserted into a real video stream so as to become indistinguishable from the real objects. The virtual objects must be shaded with the real lighting conditions, and the mutual illumination between real and virtual objects must also be determined. For this, we demonstrate a novel two-mode path tracing approach that allows ray-tracing a scene with image-based real geometry and mesh-based virtual geometry. Finally, we are able to de-noise a sparsely sampled image and render physically correct mixed reality scenes at over 5 fps on the GPU.

Paper and video can be found at

[https://research.nvidia.com/publication/filtering-environment-illumination-interactive-physically-based-rendering-mixed-reality](https://research.nvidia.com/publication/filtering-environment-illumination-interactive-physically-based-rendering-mixed-reality)
While Nvidia is certainly at the forefront of GPU path tracing research (with CUDA), AMD has recently begun venturing into GPU rendering as well and has previewed its own


Slides from



This video shows off the new technique, rendering in near-realtime on the GPU:

[OpenCL based path tracer](http://www.develop3d.com/blog/2014/08/amd-previews-opencl-ray-trace-renderer-on-maya-FirePro-Autodesk)at the Siggraph 2014 conference. The path tracer is developed by Takahiro Harada, who is a bit of an OpenCL rendering genius. He recently published an article in*GPU Pro 6*about rendering[on-the-fly vector displacement mapping with OpenCL based GPU path tracing](http://gpupro.blogspot.co.nz/2015/03/gpu-pro-6-rendering-vector-displacement.html). Vector displacement mapping differs from regular displacement mapping in that it allows the extrusion of overlapping geometry (eg a mushroom), which is not possible with the heightfield-like displacement provided by traditional displacement (the[Renderman vector displacement documentation](http://renderman.pixar.com/view/vector-displacements)explains this nicely with pictures).Slides from

[http://www.slideshare.net/takahiroharada/introduction-to-monte-carlo-ray-tracing-opencl-implementation-cedec-2014](http://www.slideshare.net/takahiroharada/introduction-to-monte-carlo-ray-tracing-opencl-implementation-cedec-2014):This video shows off the new technique, rendering in near-realtime on the GPU:

There's more info on


Foveated rendering has the potential to make high quality real-time raytraced imagery feasible on VR headsets that support eye tracking like the recently Kickstarted



Slides from


This video shows a working prototype of the FOVE VR headset with a tracking beam to control which parts of the scene are in focus, so this type of real-time ray traced (or path traced) foveated rendering should be possible right now, (which is pretty exciting):



[Takahiro's personal page](https://sites.google.com/site/takahiroharada/), along with some really interesting slideshow presentations about OpenCL based ray tracing. This guy also developed a new technique called "**Foveated real-time ray tracing for virtual reality devices**" ([paper](http://research.lighttransport.com/foveated-real-time-ray-tracing-for-virtual-reality-headset/)), progressively focusing more samples on the parts in the image where the eyes are looking (determined by eye/pupil tracking), "reducing the number of pixels to shade by 1/20, achieving 75 fps while preserving the same visual quality" (source:[http://research.lighttransport.com/foveated-real-time-ray-tracing-for-virtual-reality-headset/asset/abstract.pdf](http://research.lighttransport.com/foveated-real-time-ray-tracing-for-virtual-reality-headset/asset/abstract.pdf)). Foveated rendering takes advantage of the fact that the human retina is most sensitive in its center (the "fovea", which contains densely packed colour sensitive cones) where objects' contours and colours are sharply observed, while the periphery of the retina consists mostly of sparsely distributed, colour insensitive rods, which cause objects in the periphery of the visual field to be represented by the brain as blurry blobs (although we do not consciously perceive it like that, thinking that our entire visual field is sharply defined and has colour).
This graph shows that the resolution of the retina is highest at the fovea and drops off quickly with increasing distance from the center. This is due to the fact that the fovea contains only cones which each send individual inputs over the optic fibre (maximizing resolution), while the inputs from several rods in the periphery of the retina are merged by the retinal nerve cells before reaching the optic nerve (image from

[www.telescope-optics.net/eye.htm](http://www.telescope-optics.net/eye.htm)):[FOVE VR headset](http://techcrunch.com/2014/09/09/fove/). Using ray tracing for foveated rendering is also much more efficient than using rasterisation: ray tracing allows for sparse loading and sampling of the scene geometry in the periphery of the visual field, while rasterisation needs to load and project all geometry in the viewplane, whether it's sampled or not.[www.slideshare.net/takahiroharada/foveated-ray-tracing-for-vr-on-multiple-gpus](http://www.slideshare.net/takahiroharada/foveated-ray-tracing-for-vr-on-multiple-gpus)This video shows a working prototype of the FOVE VR headset with a tracking beam to control which parts of the scene are in focus, so this type of real-time ray traced (or path traced) foveated rendering should be possible right now, (which is pretty exciting):

It's good to finally see AMD stepping up its OpenCL game with its own GPU path tracer. Another example of this greater engagement is that

[AMD recently released a large patch](http://www.blendernation.com/2015/03/24/amd-patches-cycles-for-opencl/)to fix the OpenCL performance of Blender's Cycles renderer on AMD cards. Hopefully it will put some pressure on Nvidia and make GPU rendering as exciting as in 2010 with the release of the Fermi GPU, a GPGPU computing monster which effectively doubled the CUDA ray tracing performance compared to the previous generation.
Rendering stuff aside, today is a very important day: for the first time in their 115 year long existence, the Buffalo's from AA Gent, my hometown's football team, have won the title in the Belgian Premier League, giving them a direct ticket to the Champions League. This calls for a proper celebration!

## 46 comments:

The Gradient domain path tracing screenshots comparison is insane. I will dive in the papers, that looks promising.

"foveated rendering should be possible right now"

Unfortunately, we won’t see foveated rendering before a while, because the very, very fast (and yet not too expensive) eye trackers needed are still far from reality.

Samsung invests in FOVE: http://www.slashgear.com/samsung-invests-in-fove-eye-tracking-vr-headset-25390542/

That is indeed a real good thing. We will see how fast eye tracking will evolve. If every second generation hardware gets eye tracking, it will easily lead the path for raytracing for some indie games.

Yep, I believe ray tracing is ideally suited for foveated rendering due to its flexibility. It might also help create super high res images that are directly projected in the eye (sort of what Magic Leap claims to be doing). I don't think VR/AR has a chance of taking off as long as you're forced to look at a screen that's only a couple of centimeters away from your eyeballs. People will just not accept that.

Foveated rendering in Unity, so with a rasterizer: https://www.youtube.com/watch?v=GKR8tM28NnQ

Hey Sam, long time no see :)



I was just wonder about one key point in that article, specifically the 'vector displacement mapping'. Do you think that it would be a good technique for supporting complex character animation?

I just wonder if all animation could be compacted into the 2D texture and replayed as displacement 'frames'

Hi Kerrash, good to see you back! Can't believe you're still following my blog after all these years.

The idea of encoding character animation frames as vector displacement frames sounds really interesting. It's already possible to recalculate displacement acceleration structures and render on-the-fly displaced geometry in real-time on the GPU, so this might work. But depending on the length of the animation, the amount of texture memory you'll need to store a sufficiently high resolution displaced animated mesh might be too much to be practical, unless you can stream them in advance from system RAM. Rui Wang and Kun Zhou implemented something similar using tradition displacement on a coarse mesh for ray traced animations in "Real-time kd-tree construction on graphics hardware" (check the video and paper here: http://kunzhou.net/)

ECL is 3 times faster than CMOS

I had a dream last night.

I dreamt of noise free ray traced images.

XD. A prophecy?

Exciting dreams you've got! :) I take it you mean real-time raytraced noisefree images. That's already feasible with voxel cone tracing, although it lacks the versatility in materials of real ray tracing and the overall quality is not great compared to what you get with an offline path tracing engine. I think noisefree real-time rendering can be done properly with a slight modification to a BVH or kd-tree which gives much faster and less noisy renders and maps better to the GPU's architecture. I might write a post about it later.

Yeah i meant 60hz images. It felt like a longing. Entering a new world. Like a new born.

My life is fucked up. XD

Right the difference in quality is still significant.

Photogrammetry + raytracing will come as close to reality as it can possibly get.

The star wars gameplay images were quiet a burst as they scanned basically the whole desert. XD.

Is there a slight sign of hope on the horizon for an update on Brigade Engine. ?

I know you are not longer on the team. ;)

What about the new AMD cards. ? Any cookies on them to accelerate Brigade?

Retina: nope, no more Brigade news on this blog.


Photogrammetry is very useful for organic environments, rocky surfaces and so on, but not necessary for photorealism. Indirect lighting with color bleeding, image based lighting and soft shadows make the real difference in perceiving a scene as real. All materials can actually be diffuse, as long as you've got the lighting right.

Let's ultimately clarify the situation (which is quite frustrating).





ECL has propagation delay of 100 picoseconds, whereas CMOS is 1 nanosecond. This parameter is very important for the entire circuit to be as fast as the flip-flop allows to.

ECL 's power dissipation is always constant (same at any frequency) and little, whereas CMOS's increases exponentially(!) with increasing frequency, hence, requires ever better transistor shrinkage just to keep up with pre-defined TDP, thus, gaining nothing except some cost savings on smaller chip size. Meanwhile, Bi-Polar Transistors are already sufficiently small, low-voltage, and withstand operating temperatures up to 300°C.

It might have been known well that programs could be written & executed (games played) without OS, thereby saving computational resources, mainly operating memory. This can be done practically with no loss for multitasking if use multi-core processor that also won't require graphics co-processor, meaning that video DAC would be soldered on motherboard, and a game would be implemented directly in machine code, avoiding the notorious graphics APIs and even the graphics driver.

Mind that currently games are created using either nVidia or AMD cards, but not both at the same time. Then what's the reason in DirectX & OpenGL, be they even the lowest-level?

So, Intel, a company that most succeeds in development of omnifarious shit, has lastly found a solution to get beyond their current 'technology': it will be highly expensive InP/InGaAs substrate, on which extremely slow CMOS crap will be newly realized. Sincere congratulations, as the saying goes.






In the meantime, Bi-Polar ECL, implemented on InP/InGaAs, features propagation delay of 3.21 picoseconds, plus it might take advantage of the 770 GHz bipolar transistors, and it has been world's fastest electronic logic yet for twelve years & it remains so nowadays. Though, ECL is also fastest on silicon.

If you think that this is all, you are deeply wrong: Sn10SbTe4Ba2MnCu16O32+ is a freshly developed superconductor that features absolutely no electrical resistivity within the temperature range from 'absolute zero' right up to approx. +141ºC. Do you even if comprehend how fast a computer can get with this already today?..

On the other hand, there is as well no reason in increasing CPU/GPU's frequencies if the main memory is unable to keep up with them in terms of raw speed, that is not its own frequency.

Best operating system can be written from scratch in the Mercury programming language solely !

It is completely unimportant whether this comment will be published or rather not. The most important thing for you must be that you will inevitably lose, until some manufacturer has changed for fastest...

Interesting. It is true that Nvidia's GPU manufacturing process has been stuck on 28 nm since 2012 and the latest Maxwell GPUs from Nvidia are only 2-2.5x faster in CUDA applications than the five years old Fermi GPU (launched in 2010), far from the 10x increase expected by Moore's law and forecast by Nvidia in 2009. The enormous speed gains that GPU based ray tracing enjoyed five years ago have slowed to a crawl due to chip manufacturing problems. Intel seems to experience major problems in the transition to 10 nm, so it's an industry wide problem.

Anonymous, you are making a lot of claims. There certainly have been close circle monopolies in other domains which had led to slow down the technology democratization. One example I have is the french phone companies that repeatedly concerted to avoid risks and keep their margin at the highest. The main public company, France Telecom, that was also a public company at the time, also tried to repulse the adoption of Internet from France in favor of our horrible Minitel network. These repeated issues were attested by court or with official documents published.






However, even thinking about that kind of company strategies, I have a high doubt about your assertions. I guess ECL are used, they have advantages, I read the Wikipedia page to know more of it. But your comment is mostly a pamphlet against CMOS, we do not have the pondered disadvantages of ECL, and nothing to understand your point of view regarding the CMOS choice. You say that those companies are "bad", yeah it can be fun for us too to say that. But I am not a chip engineer, so I can't say why they would be bad. I don't have all the information to have an opinion on that subject.

I also can't trust you just because of few words, not much more if you gave me a dozen of arguments. But the more you give us, and the more we will be interested in that subject.

For me, giving the fact that you gave almost no argument at all to explain the industry choices. The only one is the slow memory that would nuke the ECL CPU/GPU advantages. Yes, why not, but that's not enough for me. It's mostly a sterile rant.

I hope you will understand my point of view.

Cheers.

Which is why we'll continue to scale out horizontally and work on improved interconnect. E.g. 8 gpus in SLI, and an omnipath interconnect.

Actually, the slow memory is currently being CMOS DRAM. ECL SRAM is the fastest: it typically has very low density, but its raw speed may be high in excess of that drawback.



As to Intel, they didn't care to have developed own RISC and now their CPUs still continue with CISC->RISC hardware translator that additionally dissipates power.

Blame on Nvidia for not using Explicit Data Graph Execution architecture which is fully non-von-Neumann. It is definitely unsuitable for CPU.

I think we will not see any gpgpu raytracer. The latest Brigade demo used 80 GTX 680



(720@30fps) to achieve a noise free image.

But there is hope !

http://blog.imgtec.com/multimedia/award-winning-powervr-gr6500-ray-tracing-gpu-tapes-out

Software raytracing is just too wastefull, so hardware needs to change.

I can only hope this technology will be licensed for next gen consoles and desktop.

The tech from Imagination looks very amateuristic, they're going to have a hard time convincing game developers to switch to ray tracing with that marketing. I don't think bringing dedicated ray tracing hardware to market is a good idea either, because fundamental research in ray tracing acceleration structures and traversal algorithms is still ongoing.

Yes their visualizer is not on par with the top path tracers.


I can only speak for myself, but i like the graphics a lot more than anything in todays games.

https://www.youtube.com/watch?v=ufbDH5qbRCE

These caustics cards were manufactured in 90nm and still used the cpu for shading and textures. So im kind of courious what a high end 14nm gpu + imagination tech could achieve ?

Maybe fixed function hardware lacks flexibility in regards to ongoing research.

But if i look back on the last five years of gpu path tracing, i am optimistic :)

The marketing of course could be a lot better.

But at least they promised some more demos for this year.

Where is it stated Brigade used 80 GPUs for that demo?

Its from one of the Octane devs in the Otoy forum.



"To get the quality we showed at GTC you will need roughly 80 amazon GPUs, so it is not cheap or for everyone, and is cloud only. We can use filtering to get it to work on 2-4 GPUs."

https://www.youtube.com/watch?v=FbGm66DCWok

I dont know how good filtering would work. But pure path tracing still needs a lot of

teraflops for calculation. Without dedicated ray tracing hardware we can wait another

decade to see this tech in games.

And we will also have to imagine what stuff we could do with 80 GPUs and triangle rasterizers.

Nothing about ray traced images. Rasterized images will always look fakish.


The Star Wars Battlefront demo from Dice really turned me on.

BUt after a week or so as i watched gameplay demos without all the TA TA star wars music

i realized that it doesnt look much better than battlefield 4. Only cookie is the photogrammetry. But shading is so wrong!

No way around ray tracing. Unfortunately it takes exponentially more power to get the last 10 percent of shaded pixels right. XD

By the way , Magic Leap bought its own semicondúctor facility for 38 million to produce their lightfield chip. https://www.youtube.com/watch?v=bmHSIEx69TQ

I have THE idea how to get Full Dive technology NOW. without nerve interfaces and such things..... just to let you know.....XD It involves proprioceptive illusions induced by vibrations and such things. electronic skin....etc.....Motoric output is possible without muscle tranquilizers. XD There is 1 path.

There is basically only one way to do full dive non invasively.

Retina, I don't agree with you. I'll give you this example: https://www.youtube.com/watch?v=DRqMbHgBIyY. This looks quite good. If you don't find it good, the average joe will. This is all about how the creative guys manage to create illusion. So this little video still looks much better than any Brigade video, even if it is theory a much more poor lighting result. When you'll have your path trace solution, amazing graphists and overall tech/production team will manage to put 80x your efforts in simple rasterization and will put to shame your first working path tracing sample. With time, it will certainly reverse at some point, because Monte Carlo path tracing and even simple tracing with few bounces still have some advantages.




So in my opinion that's not where Path tracing/ray tracing will shine. In my opinion, path tracing should help democratizing quality. Because it's very simple to just throw a set in there and change few parameters and make it look good. So indie games could look good, teams with poor taste will make it look good, and so on. I think that it is the real advantage of that technology. An other advantage is the seamless LOD. Either foveated rendering or spatial LOD, or any LOD. It's even easy to do it on a per frame basis. That could also help for the streaming part. With the rays, it's easier to know what to load, even for indirect bounces I guess.

About your idea of a "full dive" tech, I stand in my position, as a programmer, that if you have no prototype, an idea holds no clear value. Without confirmation, an idea is bound to fail most of the time. There are billions of "good ideas" that simply fail on first attempts. Also in our world the "idea" is not the end result. The end result is the product, so you have to have the idea and make it grow until it becomes a product. If you fail somewhere, your idea will have no real value. It might for another person though. Ideas are great, making things happen is what is expected. Even less cool ideas are shining just simply because they passed the whole filter of production. For example VR, the initial idea is simple: throw images into your eyes and capture movement. The correct result is not yet fully available after tons of money have been thrown at for years and years, and we still have to see if nausea will have a definitive solution or not.

As a simple note about your proprioception thing: I had about 100 people to test the Oculus DK1 back in time. All people reacted different and in that way, it was quite weird as we are used to have people in the same tone when playing on 2D screens. So I think maybe proprioception may have the same subjectivity issues as proprioception itself is a quite subjective sensor.

I agree with MrPapillon that some of the Unreal Engine 4 videos look fantastic, especially the architectural ones with baked lighting, but the amount of artist hours, effort and skill to achieve such a result is disproportionate compared to what you can do with path tracing, even if that means that you have to throw much more computational power at it. The baked lightmaps in the UE4 video also require your scene to be completely static, which is a huge drawback and shatters the illusion once you start moving around. Once you're over the initial appeal of a perfectly photorealistic (but static) scene, there's actually very little incentive to keep going back to it. The novelty wears off very fast and it gets boring incredibly quickly. A scene must be interactive to capture someone's attention for more than 30 seconds, and I believe a fully real-time realistic lighting solution is paramount for immersion or "suspension of disbelief".


Btw, @Retina: I think Magic Leap buying their own chip facility is a great idea, but I would actually like to see someone create dedicated hardware that can do high quality noise filtering in real-time, since path tracing is already possible at 8 samples per pixel at HD resolution in real-time.

Dedicated hardware?.. Then, you definitely should be longing for an ECL-based game console with no OS and no API, where you could do everything you wanted to. It is so simple, but no-one cares. 'tis a small talk, but you'll see who was right.

@MrPapillon: I like this demo too. It looks so realistic to us because the photogrammetric assests just match exactly what we've stored in our brains.





With enough artistic effort you can do sth amazing ,i agree.

I am doing right now sth in UE4 with scanned trees, rocks and such things.

Looks amazing! But as Sam pointed already out correctly, novelty wears off.

The amount of detail is also a very important aspect. The more geometric/pixel detail the more foregiving i am with wrong shading. It distracts my brain from the errors because it is so busy/overwhelmed recognizing objects. If then the objects are also of photogrammtric nature the illusion could be quiet perfect.

Right now it is all about error hiding. With path tracing your objects could always be of artificial/less realistic nature, wouldnt matter because lighting is correct.

Although this would also look unreal, but not because the lighting is wrong but because our brain is not used to artificially created objects. Experience.

Concerning FullDive: I know it could work, but question how good.

It is simple. Why are all people talking about it? Because there are two things missing. Motoric control and Sensation.

Strangely enough Vision and Audio turns out to be the 'easiest' part.

Interfacing nerves could be possibly in 20 years but there is actually a easier way

to do it with far more puclic acceptance.

You would be buried in a medium so you would rest immovable. Some how fixed.

You would wear a electronic skin that could measure very accurately pressure profiles(or stretching) once you would try to move a limb. Sounds odd but it would work. Try it yourself holding one hand on another.

Now with These commands you could control a virtual avatar. But , proprioception would be missing. KEy to move, you cant move without it.(there are few people on the world who have an illness where they can move but dont feel their limbs, bound to a wheelchair)

You can generate ghost movements by vibrating your muscle tendons.

Some guys even want to reproduce those movements induced by vibration to use it for

advanced prosthesis and virtual reality. https://www.youtube.com/watch?v=zTW5rq6jmuo

https://www.youtube.com/watch?v=CAOBdeqov6E

What i want to stress is. All sensitive cells in our skin, tendons, joints, inner ear(rotation,acceleration) are of pressure sensitive nature. Mecanoreceptors, which can be stimulated by force. Ultrasound. There was a time when neuroscientists wanted

to control the brain with ultrasound. I say: why not control our whole tactile/proprioceptive System via ultrasound. Those are a 1000x more sensitive to force than electric brain neurons are.

We need an electronic skin that could do that. https://www.youtube.com/watch?v=4oqf--GMNrA

@SamLapere: Maybe in 5y Nvidia and AMD will do that. 'Unfortunately' they are client no. 1 at Globalfroundries. All about the money.

We will see how the world will change once ML is going to sell DK1s next year.

They create visual worlds that are 100% neurologically true. They just dont do atoms......That is another company..... XD (Rony Abovitz)

@MrPapillon






These archviz demos are created with the lightmass tool. You cant create landscape with it,

all static, lots of errors in building process. Quality is not on par with path tracing.

Theres a reason why people hope for this as a better baking tool :

https://www.youtube.com/watch?v=RSpc3JBosF4

On the other hand, engine devs know that realtime raster graphics are at a dead end.

Unreal and Cryengine try to implement cone and distance field tracing.

But these hybrid solutions are very complex with a lot of limitations.

Anonymous , what do you think about Intel and Microns new 3D XPoint Technology?

Sounds like some sort of resistive cell tech.

Intel reckons that it will lead to even more new storage technolgies.

Hey Sam, quick question.


Do you think that it will be ever possible to render such a thing in real time?

https://www.youtube.com/watch?v=pHLjZkpdnyQ

It was rendered on the super computer Supermuc and contains half a million trees.

If not, then hybriding with Unlimited Detail would be an option?

I've seen it before on the Blender forum, it was rendered in Cycles. Crazy amounts of geometry are not a problem for ray tracers when using instancing, you don't need Unlimited Detail for that. The difficulty is making sure your rays don't get trapped in the dense foliage and keep bouncing around. There are ways to prevent that from happening or at least mitigate it.

Maybe a lot of stuff can be done on the LOD part too.



For example:

- from very near distance, you will have full unique trees;

- from halfway distance, you'll have a tree composed of instances;

- and at far distance, a full cloned tree instance.

The trick would probably be to make transitions smooth and to seek for a correlation algorithm between LODs to avoid morphing meshes too different.

LOD schemes would definitely work. Weta used this in their GPU accelerated PantaRay renderer to precompute geometry occlusion for the CG scenes in Avatar (and feeding the results to RenderMan): https://research.nvidia.com/publication/pantaray-fast-ray-traced-occlusion-caching-massive-scenes

With Manuka they've now got a full path tracer, which can be optimized quite aggressively to deal with massively instanced geometry.

I only ask because i found that the discrepancy between different render times were quiet high. The creator of the scence George Kim rendered 12 seconds in 7 hours with one high end GPU whereas on the supercomputer MUC which consists of 18,000 Intel Xeon E5 2680 octa cores and reaches 3 PetaFLop of performance it needed 1 hour for one frame to render.


My gaming dream is to find myself one day in a vast mountainous VR jungle sitting in a mech hiding from my opponents. haha

So that was my concern for the question. I just wanted to know if that was ever possible, or if i should stop dreaming forever.

That doesn't sound right. It might have been because the CPU version of Cycles doesn't scale well beyond 8 cores, and throwing 18000 octa cores at it won't make it any faster.

There's no reason why that sort of massive scenes wouldn't be possible in real-time some day, provided GPU technology crawls out of the slump it's been in for the past 5 years.

I suspected sth like that.



I suspect that many things will change in the next 5 years.

If Magic Leap is really what they say it is supposed to be then we will probably witness a tectonic shift in the whole consumer electronics industry/business.

Games or 3d graphics will no longer be a big niche , like it is today, it will become ubiquitous, like TV.

It will be the #1 driver for the CPU/GPU industry.

There is this teenager Thomas Sohmers who has designed a new CPU(rexcomputing)

that is 20x more efficient than a top Intel CPU.

http://www.theplatform.net/2015/03/12/the-little-chip-that-could-disrupt-exascale-computing/

That would mean that you could put a high end CPU into a Smartphone. :D

I dont know maybe it would be also possible to make a high end GPU much more efficient so it would fit also into a Smartphone what would be desirable because there is currently no high Speed wireless Connection(50+Gbit/s) available.

At 10 W TDP and with a 50 Whours battery (build by Sakti3/cheap high energy density solid state battery) the highend Desktop PC in a Smartphone could become a reality. I think everyone is going to demand/want that, even the financial managers of Nvidia and AMD.

I really hope that Magic Leap will disrupt the circuit designer world for a reincarnation of the PC.

Another thing that i find highly exciting are Unum numbers.



Invented by Johan Gustafson it is a super accurate way of performing mathematic calculations on the Computer with definite Solutions by using 29bit Unum numbers instead of floating numbers.

I have a strong feeling that you should watch his talk with Rich Report.

Path tracing makes use of monte carlo algorithm which is a guess.

Isnt this the reason for this annoying noise?

Unum numbers can find exact results to the Problem. So no more noise?

JOhan Gustafson mentioned ray tracing at the end of his talk. 47:50

https://www.youtube.com/watch?v=jN9L7TpMxeA

Rex computing is also thinking about implementing unums eventually on their chip.

There is a book about them called: The end of error : Unum Computing

I am going to read that one, highly exciting!!!

It is written from a non mathematician perspective. So i dont worry....haha.....

With unum computing valid Information/second will be measured, no longer FLOPS....

This Unum numbers could be a big hit.


I dont think they will reduce the number of rays directly in path tracing.

Seems more like they will reduce the compute cost per ray ?

Path tracing with 16 or 8 bit instead of 32.

Maybe it can accelerate filtering technique too.

@CPFUUU:


As John Gustafson,former CTO of AMD, pointed out it will. He's done tests on it.

Actually the number size can adapt. It would add more complexity on the circuit design, but in the end calculations would highly benefit of it.

In an interview with VRFocus he got asked if AMD was interested in it. They rejected. Maybe thats why he was only 1 year employed over there.

By the way.

Syoyo Fujita, a japanese raytracing enthusiast did some interesting tests on

the 16 core chip Epiphany from adapteva. https://www.youtube.com/watch?v=_t4p4Is0Z3E

Its 25x more efficient than a Intel Xeon. Adapteva wants to put up to 64,000 cores onto one chip in the future.

The sourcecode for aobench is available on github.

In this video Andreas Olofsson the creator of the epiphany chips shares some amazing insights on the future of chip design.

https://www.youtube.com/watch?v=9qPJdF_soFQ

Did you know that putting RAM onto the processor can make a chip 10-25x faster? :)

Nvidia's upcoming Pascal GPU architecture has a feature called "mixed precision" which enables it to use half precision floats (16-bits). This would make Pascal purportedly 10x faster than Maxwell in certain computations according to the marketing slides. This is hard to believe since Maxwell is only 25% faster than Kepler in CUDA tasks (both architectures are based on 28 nm and while Maxwell is more power efficient, it has also traded double precision for more single precision performance).

Being able to perform computations at half precision should be really interesting for ray tracing though.

I like the MIMD philosophy of Rex Computing and the Unum stuff looks nifty. Adaptiva seems to have stopped production of the Epiphany IV Parallela chips, I suppose there wasn't enough interest.

I wonder if this 10x speed up is real in the end. At least Pascal will






have 2x raw power over Maxwell.

http://wccftech.com/nvidia-pascal-gpu-17-billion-transistors-32-gb-hbm2-vram-arrives-in-2016/

This Rex Computing pulls out a very good gflop/w ratio.

If they scale it up to 200w@14nm, the chip could hit around 100tflop.

That is some serious compute power.

Seems like the research in filtering algorithm is increasing.

Even Disney is now in the path tracing business :D

http://www.disneyresearch.com/publication/adaptive-rendering-with-linear-predictions/

AMD published some informations about its new opencl renderer FireRays :

http://developer.amd.com/community/blog/2015/08/14/amd-firerays-library/

Pascal's specifications look really interesting indeed. I think the 10x faster than Maxwell number only applies when using half precision floats (vs Maxwell's single precision).



Path tracing has indeed taken over the entire movie industry (with Disney's Hyperion, Pixar's Renderman RIS renderer, Weta's Manuka, Arnold and Animal Logic's Glimpse) and has pretty much entirely displaced rasterization/REYES rendering (the last REYES movie was Good Dinosaur). It's just a matter of time before path tracing will take over real-time rendering as well.

Thanks for the link to AMD's FireRays renderer, that calls for a new blogpost :)

From the infos in the wccftech article you can derive that a high end 16nmFinFET+ GPU would only consume 100Watt. Compared to a gtx980 which consumes 165W.


The new finfets+ are said to consume 70% less than 28nm tech and that would mean 50WattTDP. But because you double the amount of transistors it goes again up to 100W. Would be cool to see.

What a world it would be if one day billions of smartphones containing the lightfield chip of Magic Leap and a 10Watt high end GPU are going to be sold.

No bulky desktop case no more!

AMD FireRays looks like it would a hell of a lot less work for me when i am going to

parallelize my path tracer.

Post a Comment