---
title: 'Optimizing Software Occlusion Culling: The Reckoning'
url: https://fgiesen.wordpress.com/2013/03/10/optimizing-software-occlusion-culling-the-reckoning/
published: '2013-03-10'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Optimizing Software Occlusion Culling: The Reckoning

*This post is part of a series – go here for the index.*

Welcome back! Last time, I promised to end the series with a bit of reflection on the results. So, time to find out how far we’ve come!

### The results

Without further ado, here’s the breakdown of per-frame work at the end of the respective posts (names abbreviated), in order:

| Post | Cull / setup | Render depth | Depth test | Render scene | Total |
|---|---|---|---|---|---|
| Initial | 1.988 | 3.410 | 2.091 | 5.567 | 13.056 |
| Write Combining | 1.946 | 3.407 | 2.058 | 3.497 | 10.908 |
| Sharing | 1.420 | 3.432 | 1.829 | 3.490 | 10.171 |
| Cache issues | 1.045 | 3.485 | 1.980 | 3.420 | 9.930 |
| Frustum culling | 0.735 | 3.424 | 1.812 | 3.495 | 9.466 |
| Depth buffers 1 | 0.740 | 3.061 | 1.791 | 3.434 | 9.026 |
| Depth buffers 2 | 0.739 | 2.755 | 1.484 | 3.578 | 8.556 |
| Workers 1 | 0.418 | 2.134 | 1.354 | 3.553 | 7.459 |
| Workers 2 | 0.197 | 2.217 | 1.191 | 3.463 | 7.068 |
| Dataflows | 0.180 | 2.224 | 0.831 | 3.589 | 6.824 |
| Speculation | 0.169 | 1.972 | 0.766 | 3.655 | 6.562 |
| Mopping up | 0.183 | 1.940 | 0.797 | 1.389 | 4.309 |
Total diff. |
-90.0% | -43.1% | -61.9% | -75.0% | -67.0% |
Speedup |
10.86x | 1.76x | 2.62x | 4.01x | 3.03x |

What, you think that doesn’t tell you much? Okay, so did I. Have a graph instead:

The image is a link to the full-size version that you probably want to look at. Note that in both the table and the image, updating the depth test pass to use the rasterizer improvements is chalked up to “Depth buffers done quick, part 2”, not “The care and feeding of worker threads, part 1” where I mentioned it in the text.

From the graph, you should clearly see one very interesting fact: the two biggest individual improvements – the write combining fix at 2.1ms and “Mopping up” at 2.2ms – both affect the *D3D rendering code*, and don’t have anything to do with the software occlusion culling code. In fact, it wasn’t until “Depth buffers done quick” that we actually started working on that part of the code. Which makes you wonder…

### What-if machine

Is the software occlusion culling actually worth it? That is, how much do we actually get for the CPU time we invest in occlusion culling? To help answer this, I ran a few more tests:

| Test | Cull / setup | Render depth | Depth test | Render scene | Total |
|---|---|---|---|---|---|
| Initial | 1.988 | 3.410 | 2.091 | 5.567 | 13.056 |
| Initial, no occ. | 1.433 | 0.000 | 0.000 | 25.184 | 26.617 |
| Cherry-pick | 1.548 | 3.462 | 1.977 | 2.084 | 9.071 |
| Cherry-pick, no occ. | 1.360 | 0.000 | 0.000 | 10.124 | 11.243 |
| Final | 0.183 | 1.940 | 0.797 | 1.389 | 4.309 |
| Final, no occ. | 0.138 | 0.000 | 0.000 | 6.866 | 7.004 |

Yes, the occlusion culling was a solid win both before and after. But the interesting value is the “cherry-pick” one. This is the original code, with only the following changes applied: (okay, and also with the timekeeping code added, in case you feel like nitpicking)

[Don’t read back from the constant buffers we’re writing](https://github.com/rygorous/intel_occlusion_cull/commit/e1839f69cf0680ad3339a5aa0f0b633bf71bcb68). Total diff: 3 lines.[Don’t update debug counters in CPUTFrustum](https://github.com/rygorous/intel_occlusion_cull/commit/1e1b5cca743c5ce26d2d5e8570f1ac689b5ce7fb). Total diff: 2 lines.[Use only one dynamic constant buffer](https://github.com/rygorous/intel_occlusion_cull/commit/2504647a050e8c56ef2c4b4e03cce2ca7608343e). Total diff: 10 lines changed, 8 added.[Load materials only once](https://github.com/rygorous/intel_occlusion_cull/commit/b4e29b2dfb43a040a9eb5ed5c074092766fe4ba7). Total diff: 7 lines changed, 1 added.[Share materials instead of cloning them](https://github.com/rygorous/intel_occlusion_cull/commit/464503ca5bd657d7d6c6dc9e8a9144e1f223a278). Total diff: 3 lines changed.[AABBoxRasterizer traversal fix](https://github.com/rygorous/intel_occlusion_cull/commit/aa09c99a361988c1e7dd8765c0cbb9bd3bb5d527)– keep list of models instead of going over whole database every time. Total diff: 15 lines added, 18 deleted.

In other words, “Cherry-pick” is within a few dozen lines of the original code, all of the changes are to “framework” code not the actual sample, and none of them do anything fancy. Yet it makes the difference between occlusion culling enabled and disabled shrink to about a 1.24x speedup, down from the 2x it was before!

### A brief digression

This kind of thing is, in a nutshell, the reason why graphics papers really need to come with source code. Anything GPU-related in particular is *full* of performance cliffs like this. In this case, I had the source code, so I could investigate what was going on, fix a few problems, and get a much more realistic assessment of the gain to expect from this kind of technique. Had it just been a paper claiming a “2x improvement”, I would certainly not have been able to reproduce that result – note that in the “final” version, the speedup goes back to about 1.63x, but that’s with a considerable amount of extra work.

I mention this because it’s a very common problem: whatever technique the author of a paper is proposing is well-optimized and tweaked to look good, whereas the things that it’s being compared with are often a very sloppy implementation. The end result is lots of papers that claim “substantial gains” over the prior state of the art that somehow never materialize for anyone else. At one extreme, I’ve had one of my professors state outright at one point that he just stopped giving out source code to their algorithms because the effort invested in getting other people to successfully replicate his old results “distracted” him from producing new ones. (I’m not going to name names here, but he later stated a several other things along the same lines, and he’s probably the number one reason for me deciding against pursuing a career in academia.)

To that kind of attitude, I have only one thing to say: If you care only about producing results and not independent verification, then you may be brilliant, but you are not a scientist, and there’s a very good chance that your life’s work is useless to anyone but yourself.

Conversely, exposing your code to outside eyes might not be the optimal way to stroke your ego in case somebody finds an obvious mistake :), but it sure makes your approach a lot more likely to actually become relevant in practice. Anyway, let’s get back to the subject at hand.

### Observations

The number one lesson from all of this probably is that there’s lots of ways to shoot yourself in the foot in graphics, and that it’s really easy to do so without even noticing it. So don’t assume, *profile*. I’ve used a fancy profiler with event-based sampling (VTune), but even a simple tool like Sleepy will tell you when a small piece of code takes a disproportionate amount of time. You just have to be on the lookout for these things.

Which brings me to the next point: you should always have an expectation of how long things should take. A common misconception is that profilers are primarily useful to identify the hot spots in an application, so you can focus your efforts there. Let’s have another look at the very first profiler screenshot I posted in this series:

If I had gone purely by what takes the largest amount of time, I’d have started with the depth buffer rasterization pass; as you should well recall, it took me several posts to explain what’s even going on in that code, and as you can see from the chart above, while we got a good win out of improving it (about 1.1ms total), doing so took lots of individual changes. Compare with what I *actually* worked on first – namely, the Write Combining issue, which gave us a 2.1ms win for a three-line change.

So what’s the secret? Don’t use a profile exclusively to look for hot spots. In particular, if your profile has the hot spots you expected (like the depth buffer rasterizer in this example), they’re not worth more than a quick check to see if there’s any obvious waste going on. What you really want to look for are *anomalies*: code that seems to be running into execution issues (like `SetRenderStates`

with the read-back from write-combined memory running at over 9 cycles per instruction), or things that just shouldn’t take as much time as they seem to (like the frustum culling code we looked at for the next few posts). If used correctly, a profiler is a powerful tool not just for performance tuning, but also to find deeper underlying architectural issues.

### While you’re at it…

Anyway, once you’ve picked a suitable target, I recommend that you do not just the necessary work to knock it out of the top 10 (or some other arbitrary cut-off). After “[Frustum culling: turning the crank](https://fgiesen.wordpress.com/2013/02/02/frustum-culling-turning-the-crank/)“, a commenter asked why I would spend the extra time optimizing a function that was, at the time, only at the #10 spot in the profile. A perfectly valid question, but one I have three separate answers to:

First, the answer I gave in the comments at the time: code is not just isolated from everything else; it exists in a context. A lot of the time in optimizing code (or even just reading it, for that matter) is spent building up a mental model of what’s going on and how it relates to the rest of the system. The best time to make changes to code is while that mental model is still current; if you drop the topic and work somewhere else for a bit, you’ll have to redo at least part of that work again. So if you have ideas for further improvements while you’re working on code, that’s a good time to try them out (once you’ve finished your current task, anyway). If you run out of ideas, or if you notice you’re starting to micro-optimize where you really shouldn’t, then stop. But by all means continue while the going is good; even if you don’t need that code to be faster now, you might want it later.

Second, never mind the relative position. As you can see in the table above, the “advanced” frustum culling changes reduced the total frame time by about 0.4ms. That’s about as much as we got out of our first set of depth buffer rendering changes, even though it was much simpler work. Particularly for games, where you usually have a set frame rate target, you don’t particularly care where exactly you get the gains from; 0.3ms less is 0.3ms less, no matter whether it’s done by speeding up one of the Top 10 functions slightly or something else substantially!

Third, relating to my comment about looking for anomalies above: unless there’s a really stupid mistake somewhere, it’s fairly likely that the top 10, or top 20, or top whatever hot spots are actually code that does substantial work – certainly so for code that other people have already optimized. However, most people do tend to work on the hot spots first when looking to improve performance. My favorite sport when optimizing code is starting in the middle ranks: while everyone else is off banging their head against the hard problems, I will casually snipe at functions in the 0.05%-1.0% total run time range. This has two advantages: first, you can often get rid of a lot of these functions entirely. Even if it’s only 0.2% of your total time, if you manage to get rid of it, that’s 0.2% that are gone. It’s usually a lot easier to get rid of a 0.2% function than it is to squeeze an extra 2% out of a 10%-run time function that 10 people have already looked at. And second, the top hot spots are usually in leafy code. But down in the middle ranks is “middle management” – code that’s just passing data around, maybe with some minor reformatting. That’s your entry point to re-designing data flows: this is the code where subsystems meet – the place where restructuring will make a difference. When optimizing interfaces, it’s crucial to be working on the interfaces that actually have problems, and this is how you find them.

### Ground we’ve covered

Throughout this series, my emphasis has been on changes that are fairly high-yield but have low impact in terms of how much disruption they cause. I also made no substantial algorithmic changes. That was fully intentional, but it might be surprising; after all, as any (good) text covering optimization will tell you, it’s much more important to get your algorithms right than it is to fine-tune your code. So why this bias?

Again, I did this for a reason: while algorithmic changes are indeed the ticket when you need large speed-ups, they’re also very context-sensitive. For example, instead of optimizing the frustum culling code the way I did – by making the code more SIMD- and cache-friendly – I could have just switched to a bounding volume hierarchy instead. And normally, I probably would have. But there’s plenty of material on bounding volume hierarchies out there, and I trust you to be able to find it yourself; by now, there’s also a good amount of Google-able material on “Data-oriented Design” (I dislike the term; much like “Object-oriented Design”, it means everything and nothing) and designing algorithms and data structures from scratch for good SIMD and cache efficiency.

But I found that there’s a distinct lack of material for the actual problem most of us actually face when optimizing: how do I make existing code faster without breaking it or rewriting it from scratch? So my point with this series is that there’s a lot you can accomplish purely using fairly local and incremental changes. And while the actual changes are specific to the code, the underlying ideas are very much universal, or at least I hope so. And I couldn’t resist throwing in some low-level architectural material too, which I hope will come in handy. :)

### Changes I intentionally did not make

So finally, here’s a list of things I did *not* discuss in this series, because they were either too invasive, too tricky or changed the algorithms substantially:

*Changing the way the binner works*. We don’t need that much information per triangle, and currently we gather vertices both in the binner and the rasterizer, which is a fairly expensive step. I did implement a variant that writes out signed 16-bit coordinates and the set-up Z plane equation; it saves roughly another 0.1ms in the final rasterizer, but it’s a fairly invasive change. Code is[here](https://github.com/rygorous/intel_occlusion_cull/tree/blog_past_the_end)for those who are interested. (I may end up posting other stuff to that branch later, hence the name).*A hierarchical rasterizer for the larger triangles*. Another thing I[implemented](https://github.com/rygorous/intel_occlusion_cull/tree/hier_rast)(note this branch is based off a pre-blog version of the codebase) but did not feel like writing about because it took a lot of effort to deliver, ultimately, fairly little gain.*Other rasterizer techniques or tweaks*. I could have implemented a scanline rasterizer, or a different traversal strategy, or a dozen other things. I chose not to; I wanted to write an introduction to edge-function rasterizers, since they’re cool, simple to understand and less well-known than they should be, and this series gave me a good excuse. I did not, however, want to spend more time on actual rasterizer optimization than the two posts I wrote; it’s easy to spend years of your life on that kind of stuff (I’ve seen it happen!), but there’s a point to be made that this series was already too long, and I did not want to stretch it even further.*Directly rasterizing quads in the depth test rasterizer*. The depth test rasterizer only handles boxes, which are built from 6 quads. It’s possible to build an edge function rasterizer that directly traverses quads instead of triangles. Again, I wrote the code (not on Github this time) but decided against writing about it; while the basic idea is fairly simple, it turned out to be really ugly to make it work in a “drop-in” fashion with the rest of the code. See[this comment](https://fgiesen.wordpress.com/2013/02/28/reshaping-dataflows/#comment-2466)and my reply for a few extra details.*Ray-trace the boxes in the test pass instead of rasterizing them*. Another suggestion by[Doug](https://fgiesen.wordpress.com/2013/02/28/reshaping-dataflows/#comment-2466). It’s a cool idea and I think it has potential, but I didn’t try it.*Render a lower-res depth buffer using very low-poly, conservative models*. This is how I’d actually use this technique for a game; I think bothering with a full-size depth buffer is just a waste of memory bandwidth and processing time, and we do spend a fair amount of our total time just transforming vertices too. Nor is there a big advantage to using the more detailed models for culling. That said, changing this would have required dedicated art for the low-poly occluders (which I didn’t want to do); it also would’ve violated my “no-big-changes” rule for this series. Both these changes are definitely worth looking into if you want to ship this in a game.*Try other occlusion culling techniques*. Out of the (already considerably bloated) scope of this series.

And that’s it! I hope you had as much fun reading these posts as I did writing them. But for now, it’s back to your regularly scheduled, piece-meal blog fare, at least for the time being! Should I feel the urge to write another novella-sized series of posts again in the near future, I’ll be sure to let you all know by the point I’m, oh, nine posts in or so.

Using low-poly conservative models is how Crytek do this (see coverage buffer, or c-buffer), and when I worked with Doug we discussed this but art time was an issue, and a reasonably optimized general CPU rasterizer seemed a good target. Some quick tests I did when the first code came out showed that on my PC a smaller software depth buffer target well, but results will vary with GPU/CPU combinations. I note Crytek now use GPU depth buffer down sample and re-projection on consoles and DX11 hardware.

Hey Doug! Right, art time is an issue. And, not just with us, but for real game developers too. Many developers tell us that significant content/art changes aren’t an option. We wanted to show this extreme case is still a win; don’t require special art, don’t limit the resolution, etc. We worried that if we started with a highly-optimized occluder set that people would dismiss it as requiring an unrealistic investment. We were also happy to save time wherever we could :) We also aimed for a realistic scene. Our scene is far from representative of real game scenes; in most ways it’s too simple (no shadows, no complex shaders, not fancy post, etc.) That suggests if the scene was even more complex, the implementation should deliver even more value!

Charu and Glen are almost done with an update to the sample (with improvements we couldn’t afford the first time, and Fabian’s excellent improvements). This time, she and Glen use a simplified occluder set. Its definitely the right thing to do, but hopefully we showed with the first one that there may be a more-affordable middle ground.

On rendering to a smaller buffer. That’s clearly the right thing to do too. Hopefully we showed that extremely small buffers aren’t required (they have their own issues and its nice to see there are options). The code provides a relatively-easy way to experiment with smaller depth buffers. Constants in the code control buffer width and height, tile width and height, task counts, etc. That they are compile-time constants is annoying. But, we hard-code them wherever we can to give the compiler optimization opportunities. Note that the occlussion-depth-buffer is constant-sized; it can be interesting to resize the window (i.e., the “real” render) to see if/when depth-buffer size issues manifest.

I just realized the hierarchical rasterizer might be a bigger win now, with optimized geometry. The optimized geometry has far fewer small triangles.

@mcnabbd

Will the new update include working Visual Studio 2012 solution? Currently the sample can’t be compiled with VS2012, because the required TBBGraphicSample library doesn’t include VS12 binaries (and I can’t find this library project/source anywhere, it seems to be some custom build of Intel Thread Building Blocks).

I’m fairly sure you can remove that dependency by using the alternative scheduler Intel has provided. Remove the TBBGraphicSamples.lib from the Linker Inputs properties for SoftwareOcclusionCullingDX_2010, and in file SampleComponents.h comment out STATIC_TBB and then uncomment STATIC_SS. For a bit more information on this scheduler see http://software.intel.com/en-us/articles/comparative-performance-of-game-threading-apis-in-task-managers

I’ve not been able to test this as the free Express edition I’ve got lacks cstringt.h and atlstr.h (more than reason enough to remove these in my view).

Thanks, it helped me a lot, althogh I had to make few more changes apart from the ones you mentioned to actually make it work – sample uses gTaskMgr everywhere, which is TaskMgrTbb, so I modified all occurences of gTaskMgr to gTaskMgrSS (which is TaskMgrSS). I wonder, isn’t the right way of accessing the task manager doing this via g_pTaskMgr from TaskMgr.h?

I see that we have a version working for VS2012, but I’m not clear yet if it has any issues. It should be included in the update, but, as with all features, could still miss the final cut.

PS Doug BInks, you’re awesome :)

I think it’s likely that a game implementation for PC would need runtime modification of the culling buffer size, since the wide variety of hardware in the field might require different settings – but for the demo hard-coded is certainly not an issue. If the depth pass is normally rasterized and the occlusion test is conservatively rasterized (or just +1 pixel width increase the quad) then the only issue should be less occlusion.

I compiled the code form your blog_past_the_end branch and on my hardware I noticed strange annomaly – the FPS is very inconsistent and jumps around like crazy, both in windowed and fullscreen mode. In default view (just after sample start) FPS fluctuates from ~30 to ~160, when I move the camera so that the whole castle is visible it’s switching from ~6 to ~100 (!). Original Intel version doesn’t have this problem. Is it possible that this is the effect of the different task manager I’m using (TaskMgrSS instead of TaskMgrTBB, unfortunately I can’t test the latter)?

Seems likely.

Here’s what VerySleepy told me:

http://imgur.com/4U6lDpZ

Seems like thread management fail, guess this simple task manager is not really up to the task.

You can’t infer much from that; at the slightly above 4.3ms processing time per frame my final version of the code runs at, for example, all threads

willbe idle for at least 75% of the total frame time when VSync to 60Hz is on. For threading issues, you really need a timeline profiler.Intel’s free GPA (http://software.intel.com/en-us/forums/intel-graphics-performance-analyzers) platform analyzer has the ability to view tasks in a way which should show up task management issues, and I think the relevant itt_* calls are in the code base though some configuration will be required. I’d love to help more but I’m a little rushed at the moment, apologies.

Hi.

No dates on comments?

Is it too late to talk about this?

I got a idea.

If I understand correctly, the first pass renders depth and the second pass renders boxes and checks if the render of the box is occluded by the depth buffer, I suppose it’s something like bailing out as soon as a render fragment is detected to be in front or on the previous depth buffer. Could aswell render the full object in the second pass too, would be no false positives due to corners of boxes sticking out of the previous depth buffer, but this is faster.

I *think* I got another elegant idea.

The information is almost fully present in the first buffer.

How many boxes/objects do you have? Give each one a number.

Then during the first render, store that number near the depth value for each pixel, in the depth buffer, when updating. For every pixel, you save the depth AND object id.

While doing this, you keep a small array up-to-date, an array with one cell for each object id, each cell contains the number of pixels currently in the depth buffer for this id, ie, each case contains the number of pixels for this object that are still in front. How to keep this up-to-date? Simple, each time you really update the depth buffer, substract 1 from the cell of the prevous object at this location and add 1 to the cell of the current object.

At the end, the objects to draw with the gpu are the ones in the array whose pixel count is not zero. Loop on it to find out where they are.

TADA!

Only one pass.

No bounding boxes needed, perfect object filtering(no false positives).

Neat eh?

(Yeah, conceptually, if you’re a picky, the ending loop on my array could be considered a second pass cause it iterates on nonvisible objects too, whereas in the previous method you can construct just the right list in the second pass, or push the object to the gpu right in the second pass. BUT, let’s say i meant ‘only one RENDERING pass’. I also reckon that for visible objects, the full box rendering was not needed, prolly even just one pixel. Also, with this method I don’t think you can shrink the resolution or polycount as easily (or at all) without everything screwing up too. Also, the first pass is a bit more expensive obviously, but hey what did you expect. But still. I find my idea is quite cool, like a counting sort or something.)

The objects rendered in the two passes are not the same. The first pass renders only occluder objects (usually something like 30-60 of them) while the second pass checks the bounding boxes for occludees (thousands of them). Rendering the full objects is orders of magnitude more expensive, and there’s no point doing it on the CPU – if you pay that cost, might as do it on the GPU (in a Z-prepass) where you benefit from it.

On a separate point, updating any per-object counter incrementally is a terrible idea in a multi-threaded environment, because an object can be visible in multiple tiles, meaning there is contention for that counter. If you were to store object IDs per pixel, you’d still want to render in a first pass and then do a separate scan pass that marks the visible objects; it’s much cheaper overall.

I see, indeed it seems that I missed quite a few things :)

Oh, I forgot.

Thank you so much for what you write, the way you do it, the fact you do it, and being so great.

Really.

And yeah, maybe I underestimate the slowing factor of the the first pass in my method, cause for every z update theres two array updates. The array better be in the cache, so there better not be *too* many objects. Then again, thats prolly not big compared to the depth buffer. How many distinct objects are there by the way? How many total polys? (yeah, maybe it’s somewhere here and I didnt read it, sorry) Oh maybe theres instancing. Bits per depth value? float?

But still :)

Another thought:

At constant cpu rendering performance, any improvement to the gpu rendering code decreases the software occlusion culling advantage ; at constant gpu rendering performance, any improvement to the cpu rendering code increases the advantage of using this whole method.

That shows us that the factor you mentioned (that went to 2x speedup to 1.2x) is only valid in the current state of optimisation and *has probably jumped up and down* during the course of the optimisation process; and would have jumped differently if the optimisations had been applied in a different order. The moment you stop freezes this to an ‘arbitrary’ value, since you could keep a better ratio at the cost of worse overall performance.

But things are even more intricated than this:

Having a better software culling method that doesnt do false positives (like my method) has a hidden advantage, in that it will also impact the gpu side of things positively by generating less draw calls and useless draws that will be overdrawn.

aaaaargh shhhh the depth rendering is multithreaded, if I dont want to mess everything or slow to a halt with mutexes on the array I’ll need one array per thread/zbuffer and merge them somehow after.

Not a huge deal but less beautiful.

I did not think very deep into it but I suspect this approach is not suited for gpu for kind of the same reason.

Screw parallelism :)

its a shame you got out of the scientific/educational career. its like dooming it to “stay like it is”. there is some need for change though in this often so damn unscientific area of computer science (depending on the topic you can replace “often so damn” by “completely”).