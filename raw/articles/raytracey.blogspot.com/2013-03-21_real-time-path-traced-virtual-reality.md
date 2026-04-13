---
title: Real-time path traced Virtual Reality
url: http://raytracey.blogspot.com/2013/03/real-time-path-traced-carmageddon.html
author: Sam Lapere
published: '2013-03-21'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

With the GTC almost over, we can finally unveil what we've been working on for the past seven months. Brigade has made massive progress during that time in all areas: performance, quality, sampling efficiency and tremendously improved support for dynamic scenes and multi-GPU setups.

The level of realism in Brigade is just absurd and playing with it often feels like you're watching a real life movie.

We love playing GTA, so we set out to make a real-time path traced GTA like demo to be shown at Nvidia's GTC conference (and also next week at the GDC). The plan was to have hundreds of cars and pedestrians populating a living and breathing city, all path traced in real-time. A rather ambitious goal, since path tracing this kind of highly dynamic scenes in real-time was never done before, but do we love a challenge! After doing successful tests with hundreds of moving cars and characters in a city environment, we added physics, which slowed things down massively so we had to settle on just one car. Brigade was blowing our minds, time and time again, it renders monstrously fast.

The video below shows some of our tests rendered at 1280x72:

- the city scene has 750 instanced animated characters (30k triangles each,

__), all of them physics driven with Bullet physics in a 600k triangle city__**in total 22.5 million animated triangles**
- the Piazza scene is fantastic to test color bleeding, there are 16384 instances of a 846k triangle city,

**rendered in real-time**__13.8 billion triangles in total__,
- interior scene from Octane Render, created by Enrico Cerica, 1 million triangles rendered in real-time

We will post screenshots and a lot more videos after the GDC.

## 99 comments:

Sam have been following your progress with brigade for some time now, speechless doesn't do it justice, well done to the entire team! A few questions if I may:





1. What GPU is being used to render these?

2. Is this unidirectional pathtracing?

3. Is this iteration of brigade using opencl?

4. Please when can we get a demo to try?

Very impressive, what is it running on, and what's the frame rate !?



But what's with the duplicated assets? I mean, I'm not a technical person at all, but somehow I doubt copy-pasting a scene over and over is as demanding as rendering thousands of unique characters and city blocks. I would have been more than happy with one block and a car, as now you're just "faking" detail, kind of like Euclideon. Correct me if any of this is wrong.

Nevertheless, this looks amazing, it's totally going to be the future some years from now.

@Teemu: i may well be wrong but I think this is just to do with not enough time to model the assets, whilst instanced models will save greatly on memory requirements, replacing it with unique model data wouldn't slow it down much if at all, as you're still having to intersect against data whether it's instanced or not. Raytracing and it's more advanced brethren pathtracing can handle vastly more detailed geometry than rasterising, I'm constantly amazed how the software I'm developing a pathtracer for seems to run only slightly slower whether your rendering 100 polys or 100K polys... This is the next gen way of rendering, at least in my opinion :)

Looks good but:







1. With all that noise it's impossible to use it in a game.

It's only good for previsualization.

2. Pls test with a single 7750 and not with 16 GTX Titan :p

3. Oh wait, Bridade only runs on NVIDIA hardware :p

4. Instancing is cool... but pls show us a scene with 200M unique tris (or animated particles ) and see what happens :p

@Lensman


I get what you're saying, but the characters even animate in a synchronized manner. So essentially, you're just animating one character. The demonstration is a bit misleading, is what I'm saying.

@Teemu: I dont agree, they may look like their just one animation running at the beginning, but, did you notice the bit where the car is driving through them? they are being animated and/or influenced by physical interaction with the car, again I think this is just purely down to lack of time to create unique assets.



I've studied and developed my own pathtracer along with the space partitioning acceleration structures necessary to speedup ray intersection tests with the geometry, instanced geometry can provide a speed up over unique geometry, but not that much! you still have to intersect the ray with geometry, be it instanced or unique. Instancing is mainly for saving RAM and modelling time.

@Anonymous: Again I think you are fixating on instanced geometry being used, but, again every instance has to also be processed, animated etc... these are all things that need to be done whether your rasterising or raytracing/pathtracing. I think Brigade can probably handle massive amounts of unique animated polygons, but again, showing just pathtraced particles isnt really showing off pathtracing :) Whilst I agree the noise is there, its most visible on reflective surfaces so a little less reflections would cut the noise right down!... I also agree that whilst some monster GPU was probably used to render these scenes, give a couple more years and thats what mid level GPUs will be able to do...

I'm not tech educated (especially with graphics technology like this) But I'm curious, how is the view distance seem so far and clear? One thing I usually see in other games is that the view distance is usually quite limited and texture popping occurs quite often



By the way, will you guys ever do a night scene with tons of street lights and such? I'd like to see how brigade performs with more lights.

Excuse me for my poor english and correct me if I'm wrong.

Hmm... With this level of visual realism, any discrepancy in physics/animation/AI/sounds can easily destroy players' suspension of disbelief (or even turn the game into an uncanny valley experience).

Seems like only the most big-budget gamedev companies (or extremely successful crowdfunded projects) would have the resources to aim for "movie-like" style :)

Well, thats not flabbergasting at all.


Where are the promised videos that are pretty much noise free?

i loved to follow this blog, but now i am pretty annoyed cause ive waited so so long.

If you don't think this is impressive then you have no idea what's being accomplished here. It's certainly faster than previous iterations, and very promising. But then I don't know if that's because of optimization or because this is simply running on tons of GPUs?






That said, I do agree that this is a game engine for a few years down the line. Once it can produce noiseless images at 60fps indoors, then it will be adopted. Having the image refine progressively as the gamer stands still would be too distracting. Maybe some kind of realtime noise filtering would help

Perhaps cloud based, hundreds of GPUS running this could work, but that's an untested model for millions of gamers playing at once.

However as a 3D rendering engine for movies, it's another matter. This is very impressive.

I would love to see how long an image takes to become noiseless in that interior if you keep the camera still.

Also, was that camera motion blur I saw in the street scene? :-)

Awesome demo!!

Do you think there is still room for improvement with the current hardware?(performance wise)

i ve seen that they made major accomplishments, but in comparison

to the previous demos graphicswise this doesnt blow me off my socks and i am sure they have better footage.

in future please dont raise the expectation if you arent allowed to show why you are exactly so excited.

this causes a missalignment between public expectations and yours.

Yeah it is not clear whether the target audience is game developerss, production crowd or neutral crowd here.

This demo naturally shows impressive things on the rendering part, things that we are not accustomed yet. However it fails at answering all the fields of interest of a game dev. It will certainly come with time, tools need time yes, but having multiple characters interacting in an environment with particles, facial animation, streaming, dynamic add/remove, etc... should be of prior importance now.

Really nice demo, thank you. On which hardware does it run? And in how much time we'll have a powerful enough graphic card on the market?

@Sam










Woah! I was blown away by the first demo that had barely any noise. In fact, I have little doubt that without the artefacts of rendering compression, it would be near flawless.

I can only imagine how flawless it would look with a de-noise filter such as Adaptive Manifolds on a copy of the partially-converged buffer, but I suppose there is good reason why this has not been implemented.

I showed the demo to my girlfriend (who has no choice but to hear me excitedly talk for hours about path-tracing :P), and then showed her a rasterized scene by comparison. She agreed that the Brigade render looked "real" and close to a "photo," and could tell that the rasterized game looked "fake." In her words "there is no mistaking the [rasterized] game of being real." She's not technical, but a lay person. Anecdotal sure, but this conforms with my experiences as well.

@all

Instancing is an extremely important aspect of ray tracing. Consider that a traditional renderer would have to sustain BILLIONS of polygons

per frame(not per second) to approach the level of complexity in some of these demos. While it may not be tremendously useful (in real world terms) to render a bunch of gummy-zombies, it is an example that eludes to a tremendous benefit.Consider instancing blades of grass for a field full of grass, trees in a forest full of trees, or a quarry filled with boulders, and you can begin to get a feel for the benefits of and extreme usefulness of instanced geometry.

With a bit more imagination, one can envision a set of architectural-object instances and furniture, that can then be re-arranged and assembled to compose a procedural building including a full interior, and then a number of buildings to form a city. In this city, a relatively few instanced shapes can compose a photo-real city of unparalleled complexity and architectural diversity quickly in seconds. This has the potential to simplify an artists job significantly while maintaining the highest levels of quality. Suddenly, a photo-real GTA is a

muchcheaper proposition.Ray-traced instancing simply has no equivalent in rasterizers. Rasterizers must transform the triangles in each object, instanced or not, and thus incur either a huge computational cost or require developers to devise complex 'tricks' to speed up rendering of the final scene.

@ Sean Lumly


i agree that instancing so many objects will have a major benefit to game developers. i saw a short making of vid of Shakespeare in which artists mentioned that they used a few house components like storages, door or windows to build entire London.

Unhappily i expected for days that

i am going to see pretty noisefree 1080p images at 15FPS like Sam Lapere said.

The difference to the previous instancing demos is noticable, but not in way that it would blow me graphicswise off my socks, so thats why i got that frustrated.

The complaints were not against instancing geometry but more on instancing animations.

Many instances of one animation requires much much less work in the acceleration structure than having tens of different animations whether they use instances of the same geometry or not.

That is the main battlefield now.

@MrPapillon: Whilst I agree that instanced animations and geometry can be an optimisation when creating and traversing an acceleration structure, I dont believe this to be the case here. Sam I thought had said that Brigade supports large numbers of unique animations and geometry in a previous post, Im guessing as Ive said a few times before now that this is simply a case of lack of time and assets to create and animate lots of unique characters. Lets not forget, that model animation is not strictly the role of a 3d graphics rendering technology (i know gpus CAN use vertex/geometry shaders to acoomplish this whilst rendering, but even here the CPU is involved in feed the animation/kinematic data to the GPU in some form), we are seeing realtime pathtracing not a complete game engine here...

I love it! Looks more amazing each time, especially the convergence speed in the very beginning of the video.


Are there any near-future plans to develop a demo that the blog readers can run on their own machines? Just pie in the sky thinking, perhaps OTOY could even do a promotional benchmark similar to Futuremark, where scores can be given and uploaded to a leaderboard.

@Lensman



- Showing different animation steps is orthogonal to having different animation data. A simple way to do that is to randomize the animation time for each character.

- While the complex animation blending system is not the job of the renderer, updating the renderer's acceleration structure is.

I was really impressed with how low the sample noise was in a lot of that video. It's on par with the film-grain effects developers intentionally add.

That's amazing! Now to wait for physics engines to start running on the GPU :)



Having written a basic physics engine, I'm thinking narrow phase collision and maybe BVH generation can be offloaded to the GPU, those are pretty much the most parallelizable parts.

In any case, the future is bright for VR.

@MrPapillon


- I must admit not having to include animation in the BVH accelerated path tracer Ive been developing, Im genuinely intrigued what the difference is between a different frame of the same animation and a completely different animation when rebuilding an acceleration structure? Surely you're treating both as a local transformation of the bounding volume for the animated geometry...?

Sam, Dude!. Ignore the haters; I think they missed the most important part of the whole video. The 4-5 seconds of noise free fully reflective, AO'd, GI, DOF, Motion blurred realtime camera look around at the buildings. Boys and girls grow up!, this is a proof of concept full stop!. GPU's / APU's / Memory structures on the main board are in no way optimised for this type of work yet (shit it took 20 years to get where we are now with the concrete understanding of rasterisation). What makes me interested is the realtime reflection area of this work (and how we could use whitted reflections as a post process G-Buffer ammendment composite layer for the reflection ((Mixed with a hybrid multi view screen space raytraced reflection setup, screen space reflection helps to cut workload by masking scene geometry that doesn’t need to pass through the full raytrace engine reflection, tests I’ve done in the past look like meaning even up to 60-70% of reflective surfaces could be ignored with a decent multi view screen space raytracer, don’t ask there's no work on this and even makes me have to think hard)), Not the path traced shadows, GI,. This demo shows even a full on path tracer is near to fully possible, I want to strip only the path traced realtime raytraced reflections to push through a hybrid rasterisation renderer. Think it's time me and the brigade team had a Skype session. Sorry this rant is probably incoherent, Friday=Pub=Beer=Head ache tomorrow.

Hi,



Amazing stuff - particularly the last interior scene.

Have you tried implementing Random Parameter Filtering for the noise? I heard this would be quite effective.

SHIT @ this many comments!! :D


Ok, I'll just work my way through it one by one

Lensman: Sam have been following your progress with brigade for some time now, speechless doesn't do it justice, well done to the entire team! A few questions if I may:









1. What GPU is being used to render these?

couple of Titans

2. Is this unidirectional pathtracing?

Yes

3. Is this iteration of brigade using opencl?

No, it's CUDA, but we have an OpenCL version as well (see further)

4. Please when can we get a demo to try?

Next week, if you attend the GTC :)

Teemu:








Very impressive, what is it running on, and what's the frame rate !?Couple of Titans, 40 fps at 720p, 25fps at 1080p

But what's with the duplicated assets? I mean, I'm not a technical person at all, but somehow I doubt copy-pasting a scene over and over is as demanding as rendering thousands of unique characters and city blocks. I would have been more than happy with one block and a car, as now you're just "faking" detail, kind of like Euclideon. Correct me if any of this is wrong.We wanted to show something that cannot be done in a rasterizer, I still have to see the first rasterizer that does billions of polygons at 30 fps. We did not find an artist that was able to craft a 60 billion polygon city in less than a decade, so we settled for 16,000 instances of the same city model

Nevertheless, this looks amazing, it's totally going to be the future some years from now.Much sooner actually.Lensman


@Teemu: i may well be wrong but I think this is just to do with not enough time to model the assets, whilst instanced models will save greatly on memory requirements, replacing it with unique model data wouldn't slow it down much if at all, as you're still having to intersect against data whether it's instanced or not. Raytracing and it's more advanced brethren pathtracing can handle vastly more detailed geometry than rasterising, I'm constantly amazed how the software I'm developing a pathtracer for seems to run only slightly slower whether your rendering 100 polys or 100K polys... This is the next gen way of rendering, at least in my opinion :)Correct, Brigade doesn't break a sweat at hundreds of billions of triangles as long as the geometry fits in the GPU VRAM. This is supereasy for Brigade.

Anonymous




Looks good but:




1. With all that noise it's impossible to use it in a game.

It's only good for previsualization.

2. Pls test with a single 7750 and not with 16 GTX Titan :p

3. Oh wait, Bridade only runs on NVIDIA hardware :p

4. Instancing is cool... but pls show us a scene with 200M unique tris (or animated particles ) and see what happens :p

tbh, I don't care about noise free images. At some point we had a bilateral filter working in Brigade and while it was very good at what did (removing noise), it made everything look like a rasterized game again, introduced a lot of artifacts, aliasing and DOF was not possible anymore. In the end we never used it, because we are purists and love the pristine noisy look produced by a path tracer. Also, perceptual studies have shown that the human eye perceives noisy images as more photoreal than completely noisefree images which are perceived as fake or CG. The noise levels in the first part of the video is what we were striving for and we don't want to push it any further towards noisefreeness for the reasons outlined above.

Brigade runs fantastic on AMD cards. The 7970 actually has long been the fastest GPU for Brigade for a long time (30% faster than the gtx 680), until the GTX Titan appeared. The Titan is twice as fast as the gtx 680, it's a monster GPU for path tracing.

As said above, Brigade doesn't care about how much geometry you throw at it. As long as it fits in VRAM you can render it at high speed. We also rendered a ZBrush model of a troll containing 32 million polygons in Octane and you can still move the camera at 30 fps, it just doesn't matter. You have to see it to believe it I guess.

Lensman, Anonymous, Teemu Re characters: Brigade can currently animate up to 300,000 random triangles at 30 fps, this means you can do 10 unique animated meshes of 30k triangles each or 30 unique animated characters of 10k triangles. When you use instancing, you can easily go into the billions of animated triangles, which is cool for vast landscapes of grass blades swaying in the wind for example. There are ways to make the animated instances look less in sync, but we didn't use that here. Completely rigid objects like cars are a piece of cake, you can easily have tens of thousands of them moving in real-time.

colocolo: as explained above, I really don't care about completely noise free images and actually prefer a bit of noise, because it make it more filmic. I'm more than happy with the noise level we were able to achieve with Brigade (in the first part of the video). Soon we will make a 1080p video as well.

Karl: the interior scene takes less than a quarter second to converge

Mr Papillon, yep tool side needs some work










Sean: damn, you must be looking into our minds, because we had the exact same idea of the procedural city, it's already in progress ;)

Reaven: good idea about the benchmark , have to keep that in mind

Wormslayer: exactly my point! :D

Anonymous: yep, the physics are bringing the perf down a lot, still waiting for my dedicated PhysX card as promised by Ageia a decade ago :)

KingBadger3D: yep, I agree about the beers on Friday


Actually (to my surprise), current hardware is already very close to doing this type of rendering at 1080p, especially the newly released Titan. A couple of them is enough to run Brigade at 1080p/30fps with the same noise levels as in the first part of the video. What we need is specialised hardware to rebuild acceleration structures, and preferrably on the same board as the GPU; Nvidia's Maxwell could be very interesting, because it has 4-16 ARM cores on the GPU.

Thanks for the responses Sam









Clearly you guys know what you're doing, and I dont want to be a voice of dissent but I think you're jumping to a big conclusion saying noise wont be a problem for people.

IMO the noise from film grain is not like the noise here. Film has a layer of noise over a complete image, mainly in the shadows, whereas here it isn't noise per say - its parts of the image that haven't been calculated yet, and because of that can appear like a partly drawn image with missing information in places that you wouldn't expect in the real world.

Clearly multiple bounces of light cause this, which are not just in shadows. The windows of the car outside contain dancing noise, the wine glass indoors produces more noise than the flower inside it. Light bounces from the window produce noisy 'bright' patches - which to the eye is something I don't think people would let pass unnoticed, and so on.

I actually agree that a bit of noise is a good thing, and you've made huge strides, but to me this is still a big problem because it's noise not just confined to shadows. I'm sure optimizations for interiors are coming, but I hope you don't give up on this hurdle.

I know it would be a cheat, but is there any way that when a light ray has say more than x number of bounces you begin to enlarge and blur it with the surrounding samples of similar bounces? If it bounces again enlarge and blur more, maybe lower its opacity the further it bounces... I dunno just some way to create a smoother image but only in areas which produce the noise effect in the first place. The rest of the image would be sharp.

Using noise filtering as you said you tried affects the whole image detail, rather than just the problem areas.

I'm probably talking rubbish, but it seems to me there would be a way to deal with this without having too add 10 more titans.

What you have done is amazing so far and its clear to me one day this will be standard for games and 3D creation.

Oh, when I say blur above, I meant the resultant intensity and area the light sample affects. So as it bounces it gets larger but less intense, illuminating more than a single pixel.





If the noise is a result of not enough rays hitting that area, (therefore causing noise as small as a single pixel/samples) is there a way of not only growing them but also averaging them ?

I know that moves into 'tricks' but it would only be for stubborn, hard to render areas.

you really have to see it move before you realize this is the future. :)

Sam,




a follow-up question to

"Couple of Titans, 40 fps at 720p, 25fps at 1080p"

Is this true for both the Brigade engine city scene, as well as the Octane interior scene? I find the interior scene especially impressive, hard to believe it can converge on two Titans in less than a quarter second...!

60 billion polys offers truly new possibilities. (whole hotels with interior furniture etc....)




have you already tried a instanced forest scene? that would be amazing.

would it be possible to load new

3D models proceduraly into the RAM at runtime.

i was thinking of that because then your world could become vast and would only be limited by the capacity of a SSD or HDD.

how do you manage to overcome the the lack of calculating random polys? 500,000 doesnt sound much in comparison to tessellated multi-million poly characters for PS4 games.

Sam, will it be possible to precompute and keyframe the local acceleration structure for each frame of an animation and have it directly in the data ?



I guess there will certainly be solutions happening in the near future and I am really enjoying the progress done.

Thanks for the details, I think we all know how hard it is to lead in an unknown area of engineering.

Like I said earlier, the current engine could certainly already be used for some specific indie games.

The noise of a path tracer is far less annoying than mpeg artifacts, tearing or aliasing issues and could work well for fixed-camera or isometric games.

Karl, correct me if Iùm wrong but your idea sounds a lot like filtering indirect light only with progressively larger kernels. We have tried that and it works for most areas that are not too indirectly lit. It's not without problems though, but we can probably optimize that a bit more.






rouncer81: indeed :)

Anonymous: the interior scene needs a quarter second, the outdoor scene even less

colocolo: streaming the scene is on the to do list. We've tried forests, but they are quite slow currently: the shape of a tree is very expensive to trace for a path tracer because rays get trapped between the densely packed leaves and keep on bouncing, which is detrimental for the performance. We could probably optimize for that case.

Is the PS4 really capable of multimillion poly animated characters? Path tracers can do the same by doing displacement mapping at runtime on animated characters (only the acc structure of the coarse mesh needs to be rebuild, so you can effectively animate multimillion triangle meshes that way).

MrPapillon: yes, we thought about precalculating the whole animation, and I agree it's already viable now.

Very, very exciting. I especially like the first part and the Piazza scene ;).







Few questions:

Video compression creates much more artifacts when using noisy video because compression doesn't like randomness. Doesn't that make it harder to run Brigade in the "cloud" (I hate this word) and stream it over the internet, all without artifacts? What video codec do you use? Are VP9 or H.265 a choice?

Would it be possible for developers to customize the kernels a little bit (maybe by some configuration files) to create new looks that can't be achieved by using post effects? For example a painterly look like this http://cg.iit.bme.hu/~zsolnai/gfx/smallpaint/index.html comes to mind.

The performance of Brigade improved a lot last year. Do you think this kind of improvements are still possible, e.g. a factor of two so the first scene can run on one Titan with this little noise? Or do you concentrate more on features and tools?

Good luck!

Congratulation for the accomplishment ! I'm myself in the process of creating a real-time path tracer (in my spare time as I'm working in the video game industry and currently being "stuck" with good'ol rasterization...).






As I see it there are still a few road-blocks before this kind of technology can be adopted in video games:

- Obviously too much noise (especially in interior scenes) is a problem, but it will tend to reduce with future GPU generations.

( and maybe some appropriate filter )

- I understand that the acceleration structure update (animation) is a major concern, but I'm not too worried about that, you've made great progress on this aspect at Otoy, I know NVidia Optix also as some quite good solutions to this problem. And research is ongoing...

- I know a bare bone path tracer as trouble converging caustics fast enough. Specular surfaces in general tend to "spawn" a lot of bright speckles in your image ( I "solved" this with a median filter ). However in a real world scenario, one can live without caustics and without too many specular surfaces (appart from fresnel effect at grazing angles, most dry surfaces are diffuse)

- I'm more concerned by the lack of volumetric effects. One can't imagine a game engine without explosions, smoke, maybe some atmospheric scattering etc... I know path tracing can handle all this elegantly, but at what performance/convergence cost ?!

IMO it would be interesting to implement some eularian and/or lagrangian (grid or particle based) "fluid" (by fluid I mean smoke, fire, water, dust etc...) simulation in brigade and try to path trace that to see if the perf does or doesn't take a huge perf hit. ( see http://www.youtube.com/watch?v=7obZdsEoGGA )

Instead of just "volumes" or "fluids", I like more the idea of custom shapes. I think this would be near impossible for most current implementations, but the idea is interesting in itself.


I am currently thinking of a broadphase acceleration structure and narrow one. The broadphase let you hit one "shape" that could be of any type (triangle BVH, volumetric function, voxels, ...) and you then process the narrow phase by each kind of tracing is the more appropriate for the specific shape (raytrace, raymarching, ...).

Maybe new opportunities will be available on future hardwares (we now have dynamic threading in CUDA 5.0 for example).

i have to congratulate you Sam.

i now look different at my environment.

i checked out some polycounts of objects on turboquid and observing my surrounding i have to establish that with Brigade Engine

you could now imitate real world, for example cars with machinery parts up to plates with real crumbs.....whole cities with building interiors.....i have done some serious counts :)(average object size 10-20MB)...........

Brigade Engine 2 has the potential to become the Matrix.

Very impressive!!! Pls test with a single 7970 GHz, 7870 and GTX 680 on OpenCL. Many OpenCL benchmarks shows, that 7970 couple times faster than 680 and has similar to Titan performance (see Luxmark benchmark results).

Why OTOY only works with Nvidia, not with AMD? Although previously collaborated with AMD.

Hi Sam









Well this is where my knowledge runs out and all this is simple suggestions which may be useless... ;-)

I'm rightly or wrongly assuming that noise is where light rays of say 2-3 bounces just haven't been calculated yet, and fireflies are anomalies where a single ray has shot off something reflective. Hence pixel size noise. So I was suggesting rather than filtering the image, the light ray itself is widened or encompasses a greater area as it bounces, meaning a light ray which starts as a single point at source and illuminates a single pixel onscreen would get wider after say 2 bounces, therefore illuminating a larger area. So it would produce more splotchy bigger patches of noise, but only in the indirect areas. Less samples should be needed to get an idea of the lighting in that area. Just thinking its one way to get more light into areas where you'd have to wait longer for it to 'hit'. Then averaging the results of this may smooth out the area around them. - maybe that's exactly what you tried.

Im sure it isnt as easy as this and Im making lots of assumptions!

Also I was wondering with PT if there's a way to intelligently focus on the parts that need to? Lets say 70% of the image is clear and clean, how do you get the PT to work on the areas which have noise, and only those areas? Cut out GPU calculations that add nothing to the image and focus on indirect hard to reach places. The GPU could be spending 90% of its time recalculating light samples that do not add any visual refinement to the image.

If you can figure these things out I guess thats where big speeds ups could come.

I find the same with Octane, I can wait 2 mins to get a render which is 80% complete but 20 mins later the image quality has improved very little. Maybe 85%. I assume this is because only a small % of the GPU calculations are actually now refining my image. It almost needs to work backwards at that point.

Karl, I really like your second proposal. I think computing some temporal error + some heuristics would have interesting results.

My guess is that Brigade already does that.

Your first proposal is also interesting, it is something like what Unreal engine, Unity and other engines are currently playing with : voxel cone tracing by Cyril Crassin. I would enjoy seeing results from an hybrid approach like what you described.

Anonymous: it's true that youtube doesn't like pt noise and makes it noisier and splotchier than it really is. I don't thinkit will be an issue though.







Non-photoreal effects are probably possible, we haven't tried any of that.

i'm pretty sure we can optimize it much more. We actually got another 50% boost last week from a rather simple optimization, so I'm confident we can do more especially if we target only GTX Titans, cause they have some cool features.

florent: thanks; I actually wrote about that video a while ago here: http://raytracey.blogspot.co.nz/2012/03/real-time-volume-rendering-with-path.html, it's definitely interesting

Mrpapillon: that's an interesting idea, we might try it in the future

colocolo: hehe thanks, yep Brigade wiil let you enter the matrix soon enough, especially combined with the rift

Anon: As said above, Brigade runs extremely well on the 7970, btw the benchmarks comparing OpenCL on Nvidia vs AMD are rubbish because Nvidia's OpenCL perf is horrible. Only CUDA makes sense for Nvidia cards

Karl: sounds indeed like voxel cone tracing, I was very interested in that a couple of years ago, but I think it has too many limitations to be really useful and doesn't offer the photorealistic quality that we are looking for.

The adaptive sampling technique you described is sadly very expensive and not practical in real-time.

Sam : Perhaps if there was a way to identify parts of the image that are likely to be interpreted by the eye as noisy, and then targeting those areas directly for further rendering time.


Consider a scene where 90% of the screen space is well converged, but 10% is a dark, relatively noisy area. It might be more efficient to target just the noise than send 10x more rays out indiscriminately.

Ryan: what you describe is called adaptive sampling. It's not useful for real-time path tracing, because you first need a good estimate of your image to identify the most noisy parts, which requires a sufficient number of samples for the entire image. Then you need to find out which parts of the image are noisier than others, which is not trivial and costs a lot of time, which is actually much better spent on tracing more samples for every pixel.


As suggested by Wormslayer above, what we can do is having a device that tracks your pupils and only renders the part of the image your eyes are focusing on in full detail with a high samplecount. The human peripheral vision is completely insensitive to colors and geometric details, but it is extremely sensitive to subtle differences in light intensity, so you could actually get away with monochrome undersampled and subsampled rendering in that area.

quote:


As suggested by Wormslayer above, what we can do is having a device that tracks your pupils and only renders the part of the image your eyes are focusing on in full detail with a high samplecount. The human peripheral vision is completely insensitive to colors and geometric details, but it is extremely sensitive to subtle differences in light intensity, so you could actually get away with monochrome undersampled and subsampled rendering in that area.

that would be a cool feature for the Oculus Rift.

In fact there already exists a display technique by the Fraunhofer Institut that contains between display pixels another array of photo pixels that can track your eyes.

http://www.oled-info.com/more-info-fraunhofer-bi-directional-oled-display

Hi Sam,









For an architectural designer, what you're showing here seems like the key to the gates of heaven !

I'm wondering :

- You said that the indoor scene took 0.25 sec to converge on two Titans, in HD, so 1920x1080.

For an architectural image, the resolution used is more often close to something like 6000x3000.First, could Brigade render such sizes. Then, if yes, the image being about 9 x bigger, will it takes 9 x the time, which means here about 2.5 sec ?

If we continue this little calculation game, will it takes about 5 sec on only one Titan ?

Mid range GPU, or notebook ones are about, at least, 5 to 10 time less powerful than a titan, so, in the worst case, will a complex render, 6000x3000 pixel wide, took only less than a minute to render with brigade, on a notebook ?

... If it's true,then just release the damn thing now and you will rule the market in a day...

- Does the Ray tracing method used in Brigade present some disadvantage compared to the one used in more classical raytracing engines, like Maxwell, or Octane ?

Is there some situations that it could not correctly handle ? For example, how does it deals with large space with several hundred of emissive surfaces and many many reflexive elements (an airport, or a big shopping mall) ?

Hey Sam, do post more videos when u find time :)

Why don't you use the CrossfireX-driven bundle of four Sapphire Radeon HD 7970 6GB GHz Toxic Edition, since it still remains the most powerful graphics rendering solution ?


Wouldn't that really more relevant to simply manually render each ray of light in a scene to get lot higher picture quality than path-tracing is actually capable of ?..

Another idea to get rid of the noise.

First render a low resolution image, as good as noiseless, maybe a pixel for each 4x4. Then bilinear upscale this image. Next do your normal full resolution rendering with the low resolution as the background.

This is likely to result in significant improvements imho.

You can't use this directly like you describe because that would throw a lot of blur on the player's experience and that is really something not appreciated.

You would need to do some blending between the low resolution and high resolution image. The more a hires pixel is recalculated, the more opaque it becomes. I don't see why there would be blur, the noisy pixels will have a background corresponding more to final value, making the noise less visible.

To be more precise the blending factor would need to correspond to the rate of convergence of a pixel

@Sam Lapere,



So nvidia next GPU has a strong 64-bit multicore ARM CPU on die. What could you do with Maxwell that would be impossible to do Kelper/Fermi?

in other words how would Brigade benefit from a ARM CPU?

I'd love to see the new day light system ported over to Brigade. I think a beautiful sky system is underrated :)

Warto zawiesić oko na Twoim blogu :)

The ARM CPU cores can rebuild the acceleration structures!

Hi Sam.. How are you? Are you ok? Have you any news? )))

Fajny blog :)

Very good job

Dzięki za ten wpis.

Hey Sam, what happened. Are you guys over there at OTOY lost in path traced VR, or what. LOL ;)

Hi,



not sure if it's already used in the engine. But it seems to me that

reverse reprojectioncould be used to help converge quicker.of course a ratio would be applied depending of the reflectiveness of the surface.

this way you may cut paths early or use less rays on diffuse surfaces.

Sam, when you said using 'a couple of Titans' to render this scene, what do you mean by a couple? 2? In your 580 GTX video days you quite clearly put 2x580, but I get the impression you are making use of a colloquial expression, or am i wrong?


Why not be more specific, as this is more important than any pretty demo. Path tracing is not novel, what is novel is being able to render on high end consumer hardware (Cloud aside) (i.e. if your rendering on 4xTitan then that's about 8-12x the compute power of a typical high end consumer system)

Warto wgłębić się w artykuły na Twoim blogu :)

Sam, it's been ages.


I want to be flooded with awesome updates or a badass anouncement.

yeah, where are the promised tons of videos on YouTube?

"couple" always mean 2 in the English language. I would love to see some update on Brigade?!

Strictly speaking yes it means 2, but it can mean more than that in every day use. If it were why not say 2xTitan? - there's a good reason you couldn't write 'a couple of GPUs' in a journal paper - because by it's very nature it is ambiguous - language has changed it's meaning since its conception and it can mean more than 2.

The informal term 'a couple of' can mean 2 or more:





Adj "a couple of" - more than one but indefinitely small in number; eg. "a few roses"; "a couple of roses"

Source: TheFreeDictionary.com

Pronoun "a couple of" - informal an indefinite small number

Source: oxforddictionaries.com

I'm sure Sam means 2 Titans GPU were used ;)

yeah, probably he does mean 2, just would be nice to know for certain as I'm not 100% sure (remember he does have access to as many GPUs as he wants, why not use 3?)...just to gauge how this would run on a typical high end system.



I want to see a jungle please :)

So, uh, the OTOY session with Jules is now finally online:



http://nvidia.fullviewmedia.com/gtc2013/0319-210B-S3442.html

Why don't you make a new post about it, Sam? :)

Youtube version:


http://www.youtube.com/watch?v=b4MY9bjv_B8

Aaaand, here's a working link in HD:


http://www.youtube.com/watch?v=etoS6daj20c&hd=1

I don't know whether it's just me or if everyone


else experiencing issues with your website. It looks like some

of the text on your content are running off the screen. Can someone else

please provide feedback and let me know if this is happening to them as well?

This may be a problem with my web browser because I've had this happen before. Many thanks

Here is my webpage :: Abercrombie France

Hi Sam,

We have been hearing from you a long time ago. Are you all right? Do you have any marvellous video/demo? :)

Hi there, I think your blog could be having web browser compatibility problems.


When I take a look at your web site in Safari, it looks fine but when opening

in IE, it has some overlapping issues. I just wanted to give you a quick heads up!

Besides that, fantastic blog!

My blog - Silkn Flash & Go hair removal device review

hey, where is the hype gone ?



just technical demos that washed up

at the end. heads up, there will be

sunshine again.

What happened to this blog?


i wanna dream again!

Sorry but it's time to stop dreaming.

This stuff will need at least PlayStation 5 technology (or cloud streaming) to look decent.

"will need at least PlayStation 5 technology"


You mean like whatever’s out in two/three years for the PC? Like Skylake (Intel) or Excavator (AMD), than on GPU side you’ll have Volta (Nvidia) with 1TB/s of bandwidth and Pirate Islands (AMD). So we won’t have to wait that long to see path tracing in games; well maybe not on consoles, but there’s the cloud as you said…

Cloud means latency, that is bad for most gaming genres. While you enhance graphics which are mostly good for marketing purpose, you destroy gameplay quality. Most people won't understand it, but it's still a lost in what makes games unique.

Forget the Cloud. I hate it by the way. Sounds like some peep,peep want to steal computers from humanity.

Anyway VR will take over the world

and therefore we cant tolerate any latency.

Could the authour of this blog be so merciful and tell us what happened to Brigade Engine and its progess? ;)

Alright then, we'll have something cool to show soon :)

Glad to hear from you Sam, hope everything’s going smoothly.




Btw to all of you bit*hing, you do understand this is a blog right!? So Sam has no obligation to answer to your "whining" or "requests".

'Whining' and waiting for the holy grail of realtime computer graphics are two different things,


especially if you could experience it in VR. :)

This sounds almost like a second genesis. haha

This sounds great, I tend to get far more comments here than I get directly on my blog. If I could combine the two streams, my blog readers who come from other sources might provide more feedback. Lets Have a look to my website

http://clippingpathsource.com/Have Fun!!Hey, its a really great blog post of i enjoyed lot.Thanks for a share with us.good bye.

Post a Comment