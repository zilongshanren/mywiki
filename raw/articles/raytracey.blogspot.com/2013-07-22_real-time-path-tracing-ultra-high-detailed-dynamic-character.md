---
title: 'Real-time path tracing: ultra high detailed dynamic character test'
url: http://raytracey.blogspot.com/2013/07/real-time-path-tracing-125k-dynamic.html
author: Sam Lapere
published: '2013-07-22'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

To celebrate Siggraph, here's a new video of Brigade for your enjoyment, showing an


To give some background: one of the main reasons why ray tracing has not been considered a viable alternative for rasterization as a rendering technique for games is because ray tracing requires an acceleration structure to achieve real-time performance and dynamic scene support requires that acceleration structure to be rebuilt or updated every frame which has been a long standing and often revisited problem in the ray tracing research community.


Until a few weeks ago, Brigade was capable of handling about 50k (non-instanced) dynamic triangles at 30 frames per second. Recently however, the dynamic triangle budget was tripled and we can now do around 150k triangles at 30 frames per second (and this will soon increase further to a dazzling 1 milllion dynamic triangles at 30 fps), which allows for some extremely detailed deformable meshes like characters. VFX houses doing previs of real-time motion captured characters will love this.





**animated character mesh consisting of****125k dynamic triangles**rendered in real-time at 35 fps with path tracing (the static background contains 600k triangles).To give some background: one of the main reasons why ray tracing has not been considered a viable alternative for rasterization as a rendering technique for games is because ray tracing requires an acceleration structure to achieve real-time performance and dynamic scene support requires that acceleration structure to be rebuilt or updated every frame which has been a long standing and often revisited problem in the ray tracing research community.

Until a few weeks ago, Brigade was capable of handling about 50k (non-instanced) dynamic triangles at 30 frames per second. Recently however, the dynamic triangle budget was tripled and we can now do around 150k triangles at 30 frames per second (and this will soon increase further to a dazzling 1 milllion dynamic triangles at 30 fps), which allows for some extremely detailed deformable meshes like characters. VFX houses doing previs of real-time motion captured characters will love this.

**UPDATE:**Updated the post with a fresh batch of screenshots to show the extreme texture detail on the LightStage model.**HD video (rendered at 720p):**[http://www.youtube.com/watch?&v=EgMy5dqAl_U](http://www.youtube.com/watch?&v=EgMy5dqAl_U)**Note the huge difference diffuse color bleeding makes on the character's body when the floor is matte in the next two screenshots:**

The entire movie industry is going down the physically based rendering path with path tracers like Arnold. Recently even

[Pixar/Disney went with full path tracing for Monsters University](http://www.fxguide.com/featured/monsters-university-rendering-physically-based-monsters/)and completely reworked their old Renderman renderer by adding a path tracing mode. The benefits of progressive rendering with physically based global illumination and materials without having to rely on time consuming point cloud baking has entirely revolutionized the way artists work as it's a game changer for the creative process. Games will eventually follow this path as well as game developers keep striving for cinema quality graphics as they've been doing since the introduction of the first OpenGL accelerator boards. And if you're still not convinced of the undeniable superiority of path tracing after all this fluff, you can talk to this nicely textured hand:Btw, in case you haven't noticed yet, we dramatically improved the lighting quality and sky model in Brigade over the past months and it's now almost up to Octane standards.

More tests to come soon.

## 67 comments:

hhmm, come on, its an old hat !

very impressive.

Nice. You should license Euclideon's Unlimited Detail Engine

to overcome the RAM problem for objects. hehe

Looks good and the noise is low. But the shadows are to hard. Did you limit the number of bounces or why does it look like the parts in the shadow get very little indirect light?


Good work and best regards

also theres something very wrong with the scale of the human being!!!

^ It's done on purpose.

I'm also gonna post my comment on the video here, in hope that it raises my chances to get an answer :)



First of I'm happy that the project has not been abandoned. I've been following this blog for ages now and there hasn't been an update in months. So: YAY!

Would you mind uploading a bit of raw footage ? YouTube Compression really messes it all up. I bet the grain ist A LOT nicer without the aweful compression.

Also, is this real PT or RT with additional Stuff like AO?

What hardware are you running this on? And what is up with the leafs? Are alpha- channels not supported yet?

There must be some new AMD GPUs soon...

It should be wonderful to download this demo and run on my system. Any chance?

Anonymous: >> hhmm, come on, its an old hat !















Prepare yourself for more old hat next week then :)

Irakli: thanks

colocolo: thanks, I don't think Unlimited Detail will solve any long standing problems in graphics, the lighting still looks very poor + brigade can handle scenes with billions of polygons (both static and dynamic, we'll show that soon) so there's no immediate need for any exotic geo representation

Jeyhey: yes, the contrast is quite high because we're using a new kind of tonemapping. Parts in shadow are actually receiving more than enough light, it's just not very apparent in the vid

Anonymous: scale is not a concern, the more ridiculous the video the more people will remember it :)

Kevin: thanks for being a long time follower of my blog, I wished there were more. I'll see if we can upload the raw footage somewhere. It's rendered with path tracing, so you've got GI going on everywhere, I'll post some screenshots today. It was run on 1 Titan, the test was not so much about render quality, it was more about finding out how fast brigade can update an acc structure for a high detail mesh + render simultaneously.

alpha is not supported yet.

Anonymous: no demo yet, the scene and mesh cannot be distributed

I left two messages, but there seems to be an error as they didn't show up.


I will sum them up: Outstanding work and glad to hear that you are still putting about! :)

That's weird, some comments are not coming through, but I see them in my email. To answer your quation about the body segment movements, Brigade does a full rebuild of the character mesh. There's no special cleverness involved to detect segment movements.

Is Brigade renderer antialiased by default or you have to multisample each pixel? if so how many passes does it do?

updated the post with a few screenshots.


Radoslaw: the antialiasing in Brigade happens as a side effect of accumulating samples per pixel. In the video it's rendering at 4 spp

Ah thanks Sam for your fast reply! It's very impressive that one titan can handle it so well. And it's very promising to hear that polygon count won't limit the engine at all. I'm also happy that Brigade went back to full PT again!


I've read that you are about to integrate YEBIS 2 into Brigade. This is also incredibily promising since it greatly enhances visuals. I've seen two demos and I am very impressed. Can we expect OTOY to give out licenses to companies for using Brigade + YEBIS Support? If so, is there a vague date on when to expect a "release" or beta or anything ?

should run with more power on intel

haswell cpus. these are available the

next weeks.

i only thought that the combination

of high quality lighting done by Brigade and the amount of unlimited detail (obviously the HDD would be here the last limit)

would be ultimative.

I hope next gen consoles also can read 100GB Blu Rays since DX11.1 supports partially resident textures. Would be a loss not to use this opportunity.

Will we see a Brigade Engine PC Game before PS5?

Kevin, colocolo: no dates yet, as id Software would say "it's done when it's done". Let's hope it's not going down the same path as Doom 4 :)





Waiting for the price..!!

Is there a reason Geforce cards are always used? Could that be programed for one of the dedicated ray tracing hardware cards?

@Sam


Thanks man. Both Octane and Brigade are looking seriously great. And I think your team was on to something with the "no rendering compromise" mantra. By the time this technology comes to market, computational power should increase the framerate and reduce the noise sufficiently.

i saw the video with Mark Cerny speaking at develop.

The design team of PS4 architecture was thinking of putting dedicated ray tracing hardware onto the chip. But then they decided that it is still to early. PS5 then. :)

What will those virtual realities look like. OMG!

Cool demo :)

Is subsurface scattering enabled for the character model?

I just had a thought. I know that the noise is already fairly low, but perhaps it can be reduced further and thus speed up perceived convergence.



Consider this: luminance contrast between adjacent pixels is likely to be similar based on their proximity to one another. Thus a screen-space sampling of some box of pixels around a target pixel should be a reasonable heuristic for a pixels relative luminance and weather it contributes to grain (ie. weather it is darker than its peers). If so, these types of pixels can be prioritized for additional paths to be traced (I don't know if I said that correctly). This priority would mean that those pixels that are dark get higher attention, and thus are more likely to *find* light as the scene converges.

I believe this would still be an unbiased render.

Anonymous: >> Is there a reason Geforce cards are always used? Could that be programed for one of the dedicated ray tracing hardware cards?


We have seen that GeForce cards are always quite a bit faster in path tracing than Quadro and Tesla cards, both with Brigade and Octane + they are significantly cheaper. I can't think of any sane reason to use Tesla or Quadro for GPU rendering.

RE: dedicated hardware, if you mean the Caustic graphics cards, as long as the ray tracing chip is not integrated on the GPU board, it will only be marginally faster than pure CPU path tracing.

Anonymous: we've got our tricks to make it look like subsurface scattering :)




sean, your idea sounds like adaptive sampling, if your sampling budget is constrained by real-time limits, it's actually more efficient to sample all pixels equally and you'll get less noise that way than trying to figure out which pixels are noisier than the rest. It's a useful strategy for non-realtime renderers though.

@Sam


Thanks for the feedback. I knew it was too good to be true. :)

Updated the post with a fresh batch of screenshots to show the extreme texture detail on the LightStage model

Hi Sam, nice to see you back here posting again. You said that soon brigade will be able to handle about 1 million dynamic polygons. I'm not sure why that's necessary in a gaming environment ( as opposed to a cad ), most modern games have way less than 1 million polygons in a screen at any given time. And most characters in games are anywhere from 2000-30k triangles. no need for a million polygon character.



The screenshots of the half naked guy seem to have way too much post processing ( bloom ) to the point that it does not have the realism of pathtracing but look in best case scenario as screenshot from unigine. In my opinion the race to making brigade as more realtime as possible should not compromise way too much to the point of it's rendering results be no better than typical rastering engines.

Thank you for the response. I was thinking along the lines of Caustic R2500 from Imgtech and a lessor amount the RayCore cards from Siliconarts as both are meant to be much faster than Geforce GPU’s or CPU’s. The R2500 has its own on-board memory for up to 120 million triangles real time screens while being much cheaper and faster then Quadro or Tesla cards. It just seemed to me as amazing as your software is it could be even better with a GPU+ Caustic R2500 and that would help you break 1 million dynamic triangles.




Not sure I do not understand the comment “as long as the ray tracing chip is not integrated on the GPU board, it will only be marginally faster than pure CPU path tracing.”

Why would the R2500 be only marginally faster than the CPU? At the shows the R2500 was shown doing hair and fur in real time.

mirromirror: good to have some feedback on the post processing. We're still working on that area.



Anonymous: the Caustic hardware is only calculating ray traversal and intersections, but shading is still done by the CPU. If your scene is shading bound, you'll have only marginally faster performance when you use ray tracing hardware. But it looks like Caustic will integrate their tech into the PowerVR GPUs, and once shading can be done on the GPU (like Brigade and Octane are doing), the Caustic tech will make much more sense.

this was already shown in a dx10 demo 4 years ago. we and the entire gaming industry will go with pre-baking and other tricks at least for the next 2 generations of hw. resolution, framerate and noise, noise, noise making this tech. a showstopper for games today. but please keep on going...

I noticed this strange repetitive pattern in the screenshots.

It is uniformly all over the picture, but most noticeable in dark areas with more noise I guess...

I don't know much about path tracing but is the noise generated in some kind of grid and therefore generates this pattern?

I don't mind much about the noise itself but the pattern is kind of distracting.

I did not noticed this pattern in older posts like the "Real-time GPU path traced Gangnam style".


Is it possible that this has something to do with you using a new kind of tonemapping (I definitely have no insights on this ... Sorry).

If this is unavoidable using this technique I don't know if this is a step in the right direction ... But there must be some benefits and I don't have much knowledge about path tracing as I said.

Same anonymous again by the way...

Sam: It looks like that regular grid like noise is being generated by a bad pseudo number generator, or biased seeding of your random number generator code - this would introduce a patterned bias into the sampling routine which would cause artifacts when the image converges and the random noise disappears.

" Recently even Pixar/Disney went with full path tracing for Monsters University and completely reworked their old Renderman renderer by adding a path tracing mode."What made path tracing the winning GI method?

As a layman I had the impression that PPM based approaches are faster than path tracing.

I can do that and better.

Hello Sam,

The demo looks pretty good.

It was made by Brigade 3? (I only see 2.0 on its window)

Brigade 3 engine can be download for the public? It is working with OpenCL as well?

Is it uses ERPT or simple MLT? ERPT has darker images in lower spp. What is spp in these pictures?

anon, antzrhere: yes, there was a bug in the random number generator causing the pattern, but it's fixed now.








Zsolt: path tracing is very easy to use for artists, has no artifacts when rendering animations and it is extremely parallellizable so you can run it on a cluster with hundreds of GPUs to get completely noiseless renders at high resolution in seconds (like what Octane Cloud Ed is doing).

PPM is now superseded by VCM (vertex connection and merging) which combines the best of bidir path tracing and ppm without their drawbacks. I don't know if VCM can be parallellized as efficiently as standard path tracing, but if it is than I would expect to see a GPU implementation very soon (I suspect it's not because you have to keep lots of paths in memory, which makes it ). I think SmallLuxGPU has a GPU version.

Arjan: good on you, please show me :)

Akos: Brigade is not public yet, it runs on both CUDA and OpenCL

Irakli: this was using standard path tracing, ERPT and MLT are not a good fit for realtime rendering at the moment

Hi :)


Can we see something like a forest soon please ? (Obtional of course :D)

@Sam Lapere









Interesting. Although I see Nvidia pushing PPM a bit.

https://research.nvidia.com/publication/toward-practical-real-time-photon-mapping-efficient-gpu-density-estimation

http://graphics.cs.williams.edu/papers/PhotonI3D13/

"PPM is now superseded by VCM (vertex connection and merging) which combines the best of bidir path tracing and ppm without their drawbacks."Even more interesting. :) It's nice to see new stuff invented for GI. Most seem like polished old ideas.

I don't know if VCM can be parallellized as efficiently as standard path tracing, but if it is than I would expect to see a GPU implementation very soon (I suspect it's not because you have to keep lots of paths in memory,which makes it). I think SmallLuxGPU has a GPU version.This is unclear to me. So you expect a GPU implementation or there is one already? "which makes it" what?

Sam,








Good to hear from you after such a long hiatus :)

This looks amazing, wow path tracing this sort of scene on a single GPU albeit a GFX Titan definetely shows the potential..

This version of brigade you mention runs on opencl and cuda. Whats the performance difference between say a HD 7850 using opencl vs GFX Titan using cuda, is the Titan several times faster or just 2x...what?

Interesting to hear your thoughts on VCM vs PT...?

As you mentioned, VCM has the big memory overhead in storing the photon map/light rays to do all the vertex merging and connection, whats you're take on birectional path tracing vs PT and VCM? ( I know PT is easier to do on GPU's)

One thing that has always been a snagging point with all path tracing is specular surfaces creating lots of artifacts that need a lot of samples to get rid of, how does brigade handle specular surface bounces...

Anyways keep up the good fight, Path tracing is the obvious best way to do graphics rendering and will win out eventually... :)

reminds me of mental ray in real time. its got a grittiness to it, the lighting is amazing, id love to see a grassy field lit by a sunset, it would be heaven for my eyes.

Hello Sam, it's pretty amazing. I'm wondering the solution of generating accelerated construct for animated object. Do you guys use HLBVH/HLBVH2? or something like "Maximizing Parallelism in the Construction of BVHs,Octrees, and k-d Trees" from Nvidia? Thanks.

Hey, i've visited this blog so many times now and everytime it amazes me...



That's just really great work!!!

Just some questions this time: How do you update the BVH so fast for so many polygons? Is the BVH transfer between RAM and GPU fast enough to create the BVH on CPU?

Are there many people working on this project?

Is there any long term aim for this project? (as in: a finished product)

Where did you get that dancing guy? :D

Thanks again! Have success and fun!

Chawki: good idea, need to find a good scene first










Zsolt: there already is a GPU implementation of VCM, apparently it's not too hard to add on top of a GPU bidirectional path tracer

Lensman: thanks. I don't have any numbers comparing the Titan to AMD GPUs, but to give you an idea the OpenCL version of Brigade runs faster on the 7970 than the CUDa version does on a gtx680.

Interesting to hear your thoughts on VCM vs PT...?

>> whats you're take on birectional path tracing vs PT and VCM? ( I know PT is easier to do on GPU's)

For real-time performance, I think standard path tracing is by far the most efficient and easiest to optimize. The newer techniques like bidir, MLT, VCM are better if you need fast convergence of caustics or if you want your renderer to be as robust as possible, so it can handle every thinkable light/surface interaction, but all this cleverness comes at a considerable computing cost which makes it unpractical for real-time purposes. Even Arnold render, a path tracer which is used for production rendering for movies, is still using unidirectional path tracing which says a lot.

rouncer81: I might try that

anonymous: brigade has its own way of rebuilding the acceleration structure in real-time, it's not relying on nvidia's hlbvh research.

samson: thanks, i wish i could say more.

>> Where did you get that dancing guy? :D

The dancing guy is a scanned model of a real guy. The model was autorigged and after that a motioncaptured samba dancing animation was attached to the skeleton. We could have done the motion capture in real-time with Kinect if we could dance like that.

@ Sam Lapere


What about Cone tracing? It received some attention not long ago. It was planned to be in Unreal Engine 4, but it looks like it was dropped.

Something must have been more problematic than it appeared.

a forest would be a really cool example. The only forest in a CGI movie i can think of was in Avatar.

Also forest models in games are the worst looking thing at all.

There was some cool GPU, path tracing demos at siggraph 2013.


Pixar did something

http://www.ustream.tv/recorded/36352323

Hey Sam,

did you find a place and the time to upload the raw video already?

John Carmack mentioned Brigade in his "lighting and rendering" speech recently..cool!

Nothing interesting.








The only real method is:

Doxel Graphics & Rendering Each Ray of Light Separately

And this is not future, this is already almost reality !

But, in this case, you may think, that should require fabulous computational resources, and it's right, however, the simplest solution is also already there:

Room-Temperature Superconducting Transistor based Emitter-Coupled Logic EDGE-architecture Single-Core Super-Threaded Central Processing Unit with Graphene Wiring (electron can be nearly as fast as photon) plus the fattest Caches consisting of the non-volatile ECL (or SCFL) Superconducting SRAM or Superconducting/Ferromagnetic Memory

No graphics cards are needed at all, since they are too ineffective per core and nowadays optimized only for rasterized "graphics".

Cooling, if in general could be required, is made out of a thick hollow diamond (or graphite) wiring filled with lots of hydrogen (gas).

No, thats not the future! ;)

A research group from imperial college London is working on making Single-Electron-Transistors a reality. They will work with 5nm wide quantum dots. To make them they will make a stencil with highly parellelized atomic force microscope probes for Nanoimprint Lithography.

Another international research team has already shown that you can build a half adder only with 3 SETs and 2MOSFETs at room temperature.

A normal half adder needs at least 20 transistors.

So power consumption of those devices will be ultra low and we'll carry Nvidia Sli Volta chips in smartwatches. :)

Why rendering in Windows, as this OS by default takes around 1GB of operating memory up ??!


Moreover, Windows (as well as a whole plenty of others) does use a graphical API, while in such a marvellous operating system as BeOS, it is successfully overridden yet ages ago..

Briefly put:



Path-Tracing is simply the most power-hungry rendering technique compromise.

By the way, there's a possibility, albeit a little, that the best CPU of all - IBM POWER8 - finally comes down to desktop users.. to be used in tandem with four nVidia Quadro K6000 operating in the full SLI mode.

Zsolt: cone tracing looked promising at some point, but I think Epic dropped SVO cone tracing from Unreal Engine 4 because it is not very practical for any scene larger than a room + despite giving noisefree GI, it has a lot of discontinuity artifacts related to the voxel resolution. And to get perfect reflections the cone radius needs to be so small that it basically approaches a path tracer. Moreover, John Carmack said in his QuakeCon talk about the physics of rendering that while some years ago he thought voxel tracing would be the way forward, he doesn't believe so any longer, since everyone (all film studios) is tracing triangles these days.

Anonymous: yes, Pixar's GPU path tracer for preview looked really promising. And Weta is also using a GPU ray tracer to precompute occlusion called PantaRay. I think all 3d animation/vfx preview and also some final quality rendering will be done by GPU path tracers very soon.







Anonymous: "The only real method is: Doxel Graphics & Rendering Each Ray of Light Separately"

I'm pretty sure Doxel Graphics are not the future.

colocolo: totally agreed.

Anonymous: Brigade has the option to kill Aero, so it's only a minor issue.

anonymous: why would you want to use 4x Quadro K6000 in SLI? The GTX Titan is much faster than the Quadro and you don't need SLI for GPU rendering.

Anonymous said...



"John Carmack mentioned Brigade in his "lighting and rendering" speech recently..cool!"

The Carmack? That warrants a blogpost on its own ;) Thanks for notifying me.

I'm quite intrigued by the comments about Arnold. I remember back in the day when Daniel M.Lara from Pepeland was one of the few who was using it and could show off some images rendered by it - I had a talk with Marcosss (IRC nickname creator of Arnold) and he was repeating "unbiased, unbiased, unbiased". I didn't know what he was talking about it at that time (I was about 17) but when I saw a scene that had perfect caustics and very nice object lighting (all pictures were also rendered in big resolutions) I started to wonder if he was using the same technique as the very QMC GI early Vray or Brazil had (they coudln't do such caustics).





The thing was also that all of the beta-testers were saying how Arnold was fast - that some of the scenes were rendered in just over a minute or two. That was amazing considering the fastest PCs at

that time were 1GHZ intels/AMDs.

So all of the conspiracy theories that Arnold uses a completely different technique was true - Arnold has also been using path tracing from the very beginning and not even the Messiah Renderer which was said to have the Arnold code was not doing it.

At this moment I'm not not even sure that Marcos Fajardo has shown off what the real Arnold is. Because if the old renderer was able to pump-out images crazy fast on old 1ghz machines then the "beta" I have seen with my own eyes for Maya is nowhere close to that.. it's way slower but that could be that its output has a much higher quality.

Funny.. it's still a mystery what Arnold is :)

Fantastic!

What's the "ideal" teraflops count for the current graphics in Brigade 3 at 720p to achieve noise-less image?


I think I saw them mention they're using 4 Titans for that last demo now with the cars, so that's about 20-30 TF? Will 100 TF be enough?

Is it possible to get this architecture model with textures from somewhere, are they open source?

Environment is very pretty!

Post a Comment