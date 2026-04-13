---
title: real time ray tracing.
url: https://directtovideo.wordpress.com/2013/05/07/real-time-ray-tracing/
author: Reblogged this
published: '2013-05-07'
source_blog: direct to video
source_site: https://directtovideo.wordpress.com
category: graphics
fetched: '2026-04-13'
---

It’s practically a tradition.

New hardware generation, new feature set. Ask the age old question: “*is real time ray tracing practical yet*?”. *No, no it’s not* is the answer that comes back every time.

But when I moved to Directx 11 sometime in the second half of 2011 I had the feeling that maybe this time it’d be different and the tide was changing. Ray tracing on GPUs in various forms has become popular and even efficient – be it in terms of signed distance field tracing in demos, sparse voxel octrees in game engines, nice looking [WebGL path tracers](http://madebyevan.com/webgl-path-tracing/), or actual proper in-viewport production rendering tracers like Brigade / [Octane ](https://directtovideo.wordpress.com/www.otoy.com/). So I had to try it.

My experience of ray tracing had been quite limited up til then. I had used signed distance field tracing in a 64k, some primitive intersection checking and metaball tracing for effects, and a simple octree-based voxel tracer, but never written a proper ray tracer to handle big polygonal scenes with a spatial database. So I started from the ground up. It didn’t really help that my experience of DX11 was quite limited too at the time, so the learning curve was steep. My initial goal was to render real time sub surface scattering for a certain particular degenerate case – something that could only be achieved effectively by path tracing – and using polygonal meshes with thin features that could not be represented effectively by distance fields or voxels – they needed triangles. I had a secondary goal too; we are increasingly using the demo tools to render things for offline – i.e. videos – and we wanted to be able to achieve much better render quality in this case, with the kind of lighting and rendering you’d get from using a 3d modelling package. We could do a lot with post processing and antialiasing quality but the lighting was hard limited – we didn’t have a secondary illumination method that worked with everything and gave the quality needed. Being able to raytrace the triangle scenes we were rendering would make this possible – we could then apply all kinds of global illumination techniques to the render. Some of those scenes were generated on GPU so this added an immediate requirement – the tracer should work entirely on GPU.

I started reading the research papers on GPU ray tracing. The major consideration for a triangle ray tracer is the data structure you use to store the triangles; a structure that allows rays to quickly traverse space and determine if, and what, they hit. [Timo Aila and Samuli Laine](https://mediatech.aalto.fi/~timo/HPG2009/index.html) in particular released a load of material on data structures for ray acceleration on GPUs, and they also released some source. This led into my first attempt: implementing a bounding volume hierarchy (BVH) structure. A BVH is a tree of (in thise case) axis aligned bounding boxes. The top level box encloses the entire scene, and at each step down the tree the current box is split in half at a position and axis determined by some heuristic. Then you put the triangles in each half depending on which one they sit inside, then generate two new boxes that actually enclose their triangles. Those boxes contain nodes and you recurse again. BVH building was a mystery to me until I read their stuff and figured out that it’s not actually all that complicated. It’s not all that fast either, though. The algorithm is quite heavyweight so a GPU implementation didn’t look trivial – it had to run on CPU as a precalc and it took its time. That pretty much eliminated the ability to use dynamic scenes. The actual tracer for the BVH was pretty straightforward to implement in pixel or compute shader.

Finally for the first time I could actually ray trace a polygon mesh efficiently and accurately on GPU. This was a big breakthrough – suddenly a lot of things seemed possible. I tried stuff out just to see what could be done, how fast it would run etc. and I quickly came to an annoying conclusion – it *wasn’t fast enough*. I could trace a camera ray per pixel at the object at a decent resolution in a frame, but if it was meant to bounce or scatter and I tried to handle that it got way too slow. If I spread the work over multiple frames or allowed it seconds to run I could achieve some pretty nice results, though. The advantages of proper ambient occlusion, accurate sharp shadow intersections with no errors or artefacts, soft shadows from area lights and so on were obvious.

Unfortunately just being able to ray trace wasn’t enough. To make it useful I needed a lot of rays, and a lot of performance. I spent a month or so working on ways to at first speed up the techniques I was trying to do, then on ways to cache or reduce workload, then on ways to just totally cheat.

Eventually I had a solution where every face on every mesh was assigned a portion of a global lightmap, and all the bounce results were cached in a map per bounce index. The lightmaps were intentionally low resolution, meaning fewer rays, and I blurred it regularly to spread out and smooth results. The bounce map was also heavily temporally smoothed over frames. Then for the final ray I traced out at full resolution into the bounce map so I kept some sharpness. It worked..

.. But it wasn’t all that quick, either. It relied heavily on lots of temporal smoothing & reprojection, so if anything moved it took an age to update. However this wasn’t much of a problem because I was using a single BVH built on CPU – i.e. it was completely static. That wasn’t going to do.

At this point I underwent something of a reboot and changed direction completely. Instead of a structure that was quite efficient to trace but slow to build (and only buildable on CPU), I moved to a structure that was as simple to build as I could possibly think of: a voxel grid, where each cell contains a list of triangles that overlap it. Building it was trivial: you can pretty much just render the mesh into the grid and use a UAV to write out the triangle indices of triangles that intersect the voxels they overlapped. Tracing it was trivial too – just ray march the voxels, and if the voxel contains triangles then trace the triangles in it. Naturally this was much less efficient to trace than BVH – you could march over multiple cells that contain the same triangles and had to test them again, and you can’t skip free space at all, you have to trace every voxel. But it meant one important thing: I could ray trace dynamic scenes. It actually worked.

At this point we started work on an ill fated demo for Revision 2012 which pushed this stuff into actual production.










It was here we hit a problem. This stuff was, objectively speaking, pretty slow and not actually that good looking. It was noisy, and we needed loads of temporal smoothing and reprojection so it had to move really slowly to look decent. Clever though it probably was, it wasn’t actually achieving the kind of results that made it stand up well enough on its own to justify the simple scenes we were limited to being able to achieve with it. That’s a hard lesson to learn with effect coding: no matter how clever the technique, how cool the theory, if it looks like a low resolution baked light map but takes 50ms every frame to do then it’s probably not worth doing, and the audience – who naturally finds it a lot harder than the creator of the demo to know what’s going on technically – is never going to “get it” either. As a result production came to a halt and in the end the demo was dropped; we used the violinist and the soundtrack as the intro sequence for Spacecut (1st place at Assembly 2012) instead with an entirely different and much more traditional rendering path.

The work I did on ray tracing still proved useful – we got some new tech out of it, it taught me a lot about compute, DX11 and data structures, and we used the BVH routine for static particle collisions for some time afterwards. I also prototyped some other things like reflections with BVH tracing. And here my ray tracing journey comes to a close.































































.. Until the end of 2012.

In the interim I had been working on a lot of techniques involving distance field meshing, fluid dynamics and particle systems, and also volume rendering techniques. Something that always came up was that the techniques typically involved discretising things onto a volume grid – or at least storing lists in a volume grid. The limitation was the resolution of the grid. Too low and it didn’t provide enough detail or had too much in each cell; too high and it ate too much memory and performance. This became a brick wall to making these techniques work.

One day I finally hit on a solution that allowed me to use a **sparse **grid or octree for these structures. This meant that the grid represented space with a very low resolution volume and then allowed each cell to be subdivided and refined in a tree structure like an octree – but only in the parts of the grid that actually contained stuff. Previously I had considered using these structures but could only build them bottom-up – i.e. start with the highest resolution, generate all the data then optimise into a sparse structure. That didn’t help when it came to trying to build the structure in low memory fast and in realtime – I needed to build it top down, i.e. sparse while generating. This is something I finally figured out, and it proved a solution to a whole bunch of problems.

Around that time I was reading up on sparse voxel octrees and I was wondering if it was actually performant – whether you could use it to ray trace ambient occlusion etc for realtime in a general case. Then I thought – why not put triangles in the leaf nodes so I could trace triangles too? The advantages were clear – fast realtime building times like the old voxel implementation, but with added space skipping when raytraced – and higher resolution grids so the cells contained less triangles. I got it working and started trying some things out. A path tracer, ambient occlusion and so on. Performance was showing a lot more potential. It also worked with any triangle content, including meshes that I generated on GPU – e.g. marching cubes, fluids etc.

At this point I made a decision about design. The last time I tried to use a tracer in a practical application didnt work out because I aimed for something a) too heavy and b) too easy to fake with a lightmap. If I was going to show it it needed to show something that a) couldn’t be done with a lightmap or be baked or faked easily and b) didn’t need loads of rays. So I decided to focus on reflections. Then I added refractions into the mix and started working on rendering some convincing glass. Glass is very hard to render without a raytracer – the light interactions and refraction is really hard to fake. It seemed like a scenario where a raytracer could win out and it’d be obvious it was doing something clever.

Over time, sparse voxel octrees just weren’t giving me the performance I needed when tracing – the traversal of the tree structure was just too slow and complex in the shader – so I ended up rewriting it all and replacing it with a different technique: brick maps. Brick maps are a kindof special case of sparse voxels: you only have 2 levels: a complete low resolution level grid where filled cells contain pointers into an array of bricks. A brick is a small block of high resolution cells, e.g. 8x8x8 cells in a brick. So you have for example a 64x64x64 low res voxel map pointing into 8x8x8 bricks, and you have an effective resolution of 512x512x512 – but stored sparsely so you only need the memory requirements of a small % of the total. The great thing about this is, as well as being fast to build it’s also fast to trace. The shader only has to deal with two levels so it has much less branching and path divergence. This gave me much higher performance – around 2-3x the SVO method in many places. Finally things were getting practical and fast.

I started doing some proper tests. I found that I could take a reasonable scene – e.g. a city of 50,000 triangles – and build the data structure in 3-4 ms, then ray trace reflections in 6 ms. Adding in extra bounces in the reflection code was easy and only pushed the time up to around 10-12 ms. Suddenly I had a technique capable of rendering something that looked impressive – something that wasn’t going to be easily faked. Something that actually looked worth the time and effort it took.

Then I started working heavily on glass. Getting efficient raytracing working was only a small part of the battle; making a good looking glass shader even with the ray tracing working was a feat in itself. It took a whole lot of hacking, approximations and reading of maths to get a result.

After at last getting a decent result out of the ray tracer I started working on a demo for Revision 2013. At the time I was also working with Jani on a music video – the tail end of that project – so I left him to work on that and tried to do the demo on my own; sometimes doing something on your own is a valuable experience for yourself, if nothing else. It meant that I basically had no art whatsoever, so I went on the rob – begged stole and borrowed anything I could from my various talented artist friends, and filled in the gaps myself.

I was also, more seriously, completely without a soundtrack. Unfortunately Revision’s rules caused a serious headache: they don’t allow any GEMA-affiliated musicians to compete. GEMA affliated equates to “member of a copyright society” – which ruled out almost all the musicians I am friends with or have worked with before who are actually still active. Gargaj one day suggested to me, “why don’t you just ask this guy”, linking me to [Cloudkicker ](http://cloudkicker.bandcamp.com)– an amazing indie artist who happily appears to be anti copyright organisations and releases his stuff under “pay what you want”. I mailed him and he gave me the OK. Just hoped he would be OK with the result..

I spent around 3 weeks making and editing content and putting it all together. Making a demo yourself is hard. You’re torn between fixing code bugs or design bugs; making the shaders & effects look good or actually getting content on screen. It proved tough but educational. Using your own tool & engine in anger is always a good exercise, and this time a positive one: it never crashed once (except when I reset the GPU with some shader bug). It was all looking good..

.. until I got to Revision and tried it on the compo PC. I had tested on a high end Radeon and assumed the Geforce 680 in the compo PC would behave similarly. It didn’t. It was about 60% the performance in many places, and had some real problems with fillrate-heavy stuff (the bokeh DOF was slower than the raytracer..). The performance was terrible, and worse – it was erratic. Jumping between 30 and 60 in many places. Thankfully the kind Revision compo organisers (Chaos et al) let me actually sit and work on the compo PC and do my best to cut stuff around until it ran OK, and I frame locked it to 30.

And .. we won! (I was way too hung over to show up to the prize giving though.)

Demo here:

[5 Faces by Fairlight feat. CloudKicker](http://www.pouet.net/prod.php?which=61211)

[[Youtube]](http://www.youtube.com/watch?v=i8hSZGTXTx8)

After Revision I started working on getting the ray tracer working in the viewport, refining on idle. Much more work to do here, but some initial tests with AO showed promise. Watch this space.



So the chromatic aberration / color shifting, is that done by shooting the rays by component?

Comment by Gargaj — May 7, 2013 @ 5:59 pm

Yes and no..

Yes, I do have 3 rays, one per RGB component. But no, I don’t trace and intersect them separately – it’s way too slow. Instead I only trace & intersect one ray with the triangles, and pretend each ray hits the same point on the surface, but they each get refracted by their own refraction index. Of course after several refraction steps they get pretty diverged and it’s not really accurate, but anyway. Graphics == faking.. 🙂

Then at the end for rays that exit I sample into a skybox cubemap which handles sky, background, distant geometry etc. And for that lookup I handle each component ray separately. That’s what gives the chromatic aberration.

I’ve heard some commercial ray tracing plugins actually do this too, so it’s clearly not completely hack. 🙂

Comment by directtovideo — May 8, 2013 @ 9:00 am

Too slow with my comment below 🙂

So are you tracing just one ray through the scene, and only splitting the 3 components when you exit into the sky box? That’s a little fake, but a good speed compromise. Or are you splitting them on the first glass intersection? If it’s the latter, I don’t see how that’s fake really, since you’re tracing the primaries through the full scene. Unless you’re thinking it’s not sampling all the rays for each part of the spectrum, which is serious overkill for most offline renderers never mind realtime 😉

Comment by Chris Wood (@psonice_cw) — May 8, 2013 @ 9:15 am

Refracting them separately for each intersection.

It’s a fake in that because each component ray “hits the same thing” (even though they shouldn’t), they don’t get tinted differently by the colours of the glass they hit and the thickness of the glass they pass through (I have some absorbtion term), and they don’t consider hitting different normals etc.

If you a) assume the glass is a consistent colour and is very thin, and b) try and compensate for the lack of divergence / bending that you’d get if you hit different normals by just upping the refraction index, then yea – it’s a pretty good approximation.

Let’s call it that. An approximation. Yea. See Gargaj, still no fakes. 🙂

Comment by directtovideo — May 8, 2013 @ 9:25 am

YOU SAID NO FAKES YOU BASTARD

Comment by Gargaj — May 8, 2013 @ 9:20 am

Ok, so the 3 rays bend differently but travel the same path. Dirty, but I like it, and I guess it’s going to look pretty convincing in most scenes since the divergence isn’t all that extreme normally.

Comment by Chris Wood (@psonice_cw) — May 8, 2013 @ 9:39 am

Yeah, I’m curious about this too. I suspect it’s fake, since the background also shows chromatic aberration where there’s no reason for the colour split (no glass in the ray path), and colour splitting would get expensive fast in a scene with so many small glass pieces.

If it’s fake though, it’s very well done. The refracted colours are much stronger than the background, so it really stands out and looks convincing.

Comment by Chris Wood (@psonice_cw) — May 8, 2013 @ 9:06 am

Congratulations on winning Revision 2013, I saw your demo on youtube and was very impressed.

And now that you’ve posted about it I’m very intrigued by your technique.

Could you please talk about the brick map technique a little more?

Comment by Ah — May 7, 2013 @ 11:26 pm

Yes I will, but I’m going to do that in a follow up post. Stay tuned for part 2..

Comment by directtovideo — May 8, 2013 @ 9:00 am

Thanks for the write-up smash, this is really good reading once again. I seriously look forward to your write-up more than your next demo, and I really look forward to the demos already 😀

It’ll be very helpful to look back at what worked for you and what didn’t when I get to the point where I want to start using real geometry in my own tracer. It’s currently limited to balls + boxes, but I’m trying out an idea I had that should give me noise-free DOF, AO etc. with very few rays – the maths is giving me headaches, but I’m at the point where it’s starting to look viable (working DOF, buggy but visible soft reflections). Brick maps look like a good fit, although z-ordering (which is important for my method) might be an issue. Have to look into that soon 🙂

Comment by Chris Wood (@psonice_cw) — May 8, 2013 @ 8:58 am

Noise-free DOF and AO in a general case scene with few rays .. it sounds like you’ve hit upon the holy grail there, so I hope you’re going to write it up. 🙂

How do you mean by Z ordering? Brick map tracing has a nice property which is that cells (and triangles in cells, with a bit more effort) are visited in order along the ray.

Comment by directtovideo — May 8, 2013 @ 9:07 am

It’ll be sweet if it works, and if it does I’ll write it up. There are downsides, naturally, when isn’t there? 😀 And there’s a fair chance it’ll collapse into a steaming pile of failure. But I have a (very buggy, literally just at that point where there’s a visible working thing on screen for the first time) sphere on a plane with DOF and soft reflections, using 2 rays (primary and reflection). AO should be one extra ray, soft shadows one more. It’s running realtime on an ipad mini (this is why I’m playing with different techniques instead of monte carlo or something 😉

By z-ordering, I mean the ray ideally needs to intersect anything in the scene in front to back order. Just intersecting everything and picking the closest intersection is possible, but then it becomes necessary to sort the intersection results and then repeat the intersection test, or do a buttload of extra work and store a lot of data. It gets ugly very fast without z ordering.

Comment by Chris Wood (@psonice_cw) — May 8, 2013 @ 9:31 am

Reblogged this on Indefinite Seven.

Comment by Indefinite Seven — May 8, 2013 @ 9:05 am

[…] https://directtovideo.wordpress.com/2013/05/07/real-time-ray-tracing/ https://directtovideo.wordpress.com/2013/05/08/real-time-ray-tracing-part-2/ […]

Pingback by Fairlight – 5 Faces « startup-sequence.pl — May 9, 2013 @ 10:06 am