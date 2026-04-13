---
title: The care and feeding of worker threads, part 1
url: https://fgiesen.wordpress.com/2013/02/17/care-and-feeding-of-worker-threads-part-1/
published: '2013-02-17'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# The care and feeding of worker threads, part 1

*This post is part of a series – go here for the index.*

It’s time for another post! After all the time I’ve spent on squeezing about 20% out of the depth rasterizer, I figured it was time to change gears and look at something different again. But before we get started on that new topic, there’s one more set of changes that I want to talk about.

### The occlusion test rasterizer

So far, we’ve mostly been looking at one rasterizer only – the one that actually renders the depth buffer we cull against, and even more precisely, only multi-threaded SSE version of it. But the occlusion culling demo has two sets of rasterizers: the other set is used for the occlusion tests. It renders bounding boxes for the various models to be tested and checks whether they are fully occluded. Check out the [code](https://github.com/rygorous/intel_occlusion_cull/blob/4c64fd75/SoftwareOcclusionCulling/TransformedAABBoxSSE.cpp#L165) if you’re interested in the details.

This is basically the same rasterizer that we already talked about. In the previous two posts, I talked about optimizing the depth buffer rasterizer, but most of the same changes apply to the test rasterizer too. It didn’t make sense to talk through the same thing again, so I took the liberty of just making the same changes (with some minor tweaks) to the test rasterizer “off-screen”. So, just a heads-up: the test rasterizer has changed while you weren’t looking – unless you closely watch the Github repository, that is.

And now that we’ve established that there’s another inner loop we ought to be aware of, let’s zoom out a bit and look at the bigger picture.

### Some open questions

There’s two questions you might have if you’ve been following this series closely so far. The first concerns a very visible difference between the depth and test rasterizers that you might have noticed if you ran the code. It’s also visible in the data in [“Depth buffers done quick, part 1”](https://fgiesen.wordpress.com/2013/02/11/depth-buffers-done-quick-part/), though I didn’t talk about it at the time. I’m talking, of course, about the large standard deviation we get for the execution time of the occlusion tests. Here’s a set of measurements for the code right after bringing the test rasterizer up to date:

| Pass | min | 25th | med | 75th | max | mean | sdev |
|---|---|---|---|---|---|---|---|
| Render depth | 2.666 | 2.716 | 2.732 | 2.745 | 2.811 | 2.731 | 0.022 |
| Occlusion test | 1.335 | 1.545 | 1.587 | 1.631 | 1.761 | 1.585 | 0.066 |

Now, the standard deviation actually got a fair bit lower with the rasterizer changes (originally, we were well above 0.1ms), but it’s still surprisingly large, especially considering that the occlusion tests run roughly half as long (in terms of wall-clock time) as the depth rendering. And there’s also a second elephant in the room that’s been staring us in the face for quite a while. Let me recycle one of the VTune screenshots from last time:

Right there at #4 is some code from [TBB](http://threadingbuildingblocks.org/), namely, what turns out to be the “thread is idle” spin loop.

Well, so far, we’ve been profiling, measuring and optimizing this as if it was a single-threaded application, but it’s not. The code uses TBB to dispatch tasks to worker threads, and clearly, a lot of these worker threads seem to be idle a lot of the time. But why? To answer that question, we need a bit different information than what either a normal VTune analysis run or our summary timers give us. We want a detailed breakdown of what happens during a frame. Now, VTune has *some* support for that (as part of their threading/concurrency profiling), but the UI doesn’t work well for me, and neither does the the visualization; it seems to be geared towards HPC/throughput computing more than latency-sensitive applications like real-time graphics, and it’s also still based on sampling profiling, which means it’s low-overhead but fairly limited in the kind of data it can collect.

Instead, I’m going to go for the shameless plug and use [Telemetry](http://www.radgametools.com/telemetry.htm) instead (full disclosure: I work at RAD). It works like this: I manually instrument the source code to tell Telemetry when certain events are happening, and Telemetry collects that data, sends the whole log to a server and can later visualize it. Most games I’ve worked on have some kind of “bar graph profiler” that can visualize within-frame events, but because Telemetry keeps the whole data stream, it can also be used to answer the favorite question (not!) of engine programmers everywhere: “Wait, what the hell just happened there?”. Instead of trying to explain it in words, I’m just gonna show you the screenshot of my initial profiling run after I hooked up Telemetry and added some basic markup: (Click on the image to get the full-sized version)

The time axis goes from left to right, and all of the blocks correspond to regions of code that I’ve marked up. Regions can nest, and when they do, the blocks stack. I’m only using really basic markup right now, because that turns out to be all we need for the time being. The different tracks correspond to different threads.

As you can see, despite the code using TBB and worker threads, it’s fairly rare for more than 2 threads to be actually running anything interesting at a time. Also, if you look at the “Rasterize” and “DepthTest” tasks, you’ll notice that we’re spending a fair amount of time just waiting for the last 2 threads to finish their respective jobs, while the other worker threads are idle. That’s where our variance in latency ultimately comes from – it all depends on how lucky (or unlucky) we get with scheduling, and the exact scheduling of tasks changes every frame. And now that we’ve seen how much time the worker threads spend being idle, it also shouldn’t surprise us that TBB’s idle spin loop ranked as high as it did in the profile.

What do we do about it, though?

### Let’s start with something simple

As usual, we go for the low-hanging fruit first, and if you look at the left side of the screenshot I’ll posted, you’ll see *a lot* of blocks (“zones”) on the left side of the screen. In fact, the count is much higher than you probably think – these are LOD zones, which means that Telemetry has grouped a bunch of very short zones into larger groups for the purposes of visualization. As you can see from the mouse-over text, the single block I’m pointing at with the mouse cursor corresponds to 583 zones – and each of those zones corresponds to an individual TBB task! That’s because this culling code uses one TBB task per model to be culled. *Ouch.* Let’s zoom in a bit:

Note that even at this zoom level (the whole screen covers about 1.3ms), most zones are *still* LOD’d out. I’ve mouse-over’ed on a single task that happens to hit one or two L3 cache miss and so is long enough (at about 1500 cycles) to show up individually, but most of these tasks are closer to 600 cycles. In total, frustum culling the approximately 1600 occluder models takes up just above 1ms, as the captions helpfully say. For reference, the much smaller block that says “OccludeesVisible” and takes about 0.1ms? That one actually processes about 27000 models (it’s the code we optimized in [“Frustum culling: turning the crank”](https://fgiesen.wordpress.com/2013/02/02/frustum-culling-turning-the-crank/)). Again, *ouch*.

Fortunately, there’s a simple solution: don’t use one task per model. Instead, use a smaller number of tasks (I just used 32) that each cover multiple models. The code is fairly obvious, so I won’t bother repeating it here, but I am going to show you the results:

Down from 1ms to 0.08ms in two minutes of work. Now we could apply the same level of optimization as we did to the occludee culling, but I’m not going to bother, because at least not for the time being it’s fast enough. And with that out of the way, let’s look at the rasterization and depth testing part.

### A closer look

Let’s look a bit more closely at what’s going on during rasterization:

There are at least two noteworthy things clearly visible in this screenshot:

- There’s three separate passes – transform, bin, then rasterize.
- For some reason, we seem to have an odd mixture of really long tasks and very short ones.

The former shouldn’t come as a surprise, since it’s explicit in the code:

gTaskMgr.CreateTaskSet(&DepthBufferRasterizerSSEMT::TransformMeshes, this, NUM_XFORMVERTS_TASKS, NULL, 0, "Xform Vertices", &mXformMesh); gTaskMgr.CreateTaskSet(&DepthBufferRasterizerSSEMT::BinTransformedMeshes, this, NUM_XFORMVERTS_TASKS, &mXformMesh, 1, "Bin Meshes", &mBinMesh); gTaskMgr.CreateTaskSet(&DepthBufferRasterizerSSEMT::RasterizeBinnedTrianglesToDepthBuffer, this, NUM_TILES, &mBinMesh, 1, "Raster Tris to DB", &mRasterize); // Wait for the task set gTaskMgr.WaitForSet(mRasterize);

What the screenshot does show us, however, is the cost of those synchronization points. There sure is a lot of “air” in that diagram, and we could get some significant gains from squeezing it out. The second point is more of a surprise though, because the code does in fact try pretty hard to make sure the tasks are evenly sized. There’s a problem, though:

void TransformedModelSSE::TransformMeshes(...) { if(mVisible) { // compute mTooSmall if(!mTooSmall) { // transform verts } } } void TransformedModelSSE::BinTransformedTrianglesMT(...) { if(mVisible && !mTooSmall) { // bin triangles } }

Just because we make sure each task handles an equal number of vertices (as happens for the “TransformMeshes” tasks) or an equal number of triangles (“BinTransformedTriangles”) doesn’t mean they are similarly-sized, because the work subdivision ignores culling. Evidently, the tasks end up *not* being uniformly sized – not even close. Looks like we need to do some load balancing.

### Balancing act

To simplify things, I moved the computation of `mTooSmall`

from `TransformMeshes`

into `IsVisible`

– right after the frustum culling itself. That required some shuffling arguments around, but it’s exactly the kind of thing we already saw in [“Frustum culling: turning the crank”](https://fgiesen.wordpress.com/2013/02/02/frustum-culling-turning-the-crank/), so there’s little point in going over it in detail again.

Once `TransformMeshes`

and `BinTransformedTrianglesMT`

use the exact same condition – `mVisible && !mTooSmall`

– we can determine the list of models that are visible and not too small once, compute how many triangles and vertices these models have in total, and then use these corrected numbers which account for the culling when we’re setting up the individual transform and binning tasks.

This is easy to do: `DepthBufferRasterizerSSE`

gets a few more member variables

UINT *mpModelIndexA; // 'active' models = visible and not too small UINT mNumModelsA; UINT mNumVerticesA; UINT mNumTrianglesA;

and two new member functions

inline void ResetActive() { mNumModelsA = mNumVerticesA = mNumTrianglesA = 0; } inline void Activate(UINT modelId) { UINT activeId = mNumModelsA++; assert(activeId < mNumModels1); mpModelIndexA[activeId] = modelId; mNumVerticesA += mpStartV1[modelId + 1] - mpStartV1[modelId]; mNumTrianglesA += mpStartT1[modelId + 1] - mpStartT1[modelId]; }

that handle the accounting. The depth buffer rasterizer already kept cumulative vertex and triangle counts for all models; I added one more element at the end so I could use the simplified vertex/triangle-counting logic.

Then, at the end of the `IsVisible`

pass (after the worker threads are done), I run

// Determine which models are active ResetActive(); for (UINT i=0; i < mNumModels1; i++) if(mpTransformedModels1[i].IsRasterized2DB()) Activate(i);

where `IsRasterized2DB()`

is just a predicate that returns `mIsVisible && !mTooSmall`

(it was already there, so I used it).

After that, all that remains is distributing work over the active models only, using `mNumVerticesA`

and `mNumTrianglesA`

. This is as simple as turning the original loop in `TransformMeshes`


for(UINT ss = 0; ss < mNumModels1; ss++)

into

for(UINT active = 0; active < mNumModelsA; active++) { UINT ss = mpModelIndexA[active]; // ... }

and the same for `BinTransformedMeshes`

. All in all, this took me about 10 minutes to write, debug and test. And with that, we should have proper load balancing for the first two passes of rendering: transform and binning. The question, as always, is: does it help?

**Change**: Better rendering “front end” load balancing

| Version | min | 25th | med | 75th | max | mean | sdev |
|---|---|---|---|---|---|---|---|
| Initial depth render | 2.666 | 2.716 | 2.732 | 2.745 | 2.811 | 2.731 | 0.022 |
| Balance front end | 2.282 | 2.323 | 2.339 | 2.362 | 2.476 | 2.347 | 0.034 |

Oh boy, does it ever. That’s a 14.4% reduction *on top of what we already got last time*. And Telemetry tells us we’re now doing a much better job at submitting uniform-sized tasks:

In this frame, there’s still one transform batch that takes longer than the others; this happens sometimes, because of context switches for example. But note that the other threads nicely pick up the slack, and we’re still fine: a ~2x variation on the occasional item isn’t a big deal, provided most items are still roughly the same size. Also note that, even though there’s 8 worker threads, we never seem to be running more than 4 tasks at a time, and the hand-offs between threads (look at what happens in the BinMeshes phase) seem too perfectly synchronized to just happen accidentally. I’m assuming that TBB intentionally never uses more than 4 threads because the machine I’m running this on has a quad-core CPU (albeit with HyperThreading), but I haven’t checked whether this is just a configuration option or not; it probably is.

### Balancing the rasterizer back end

Now we can’t do the same trick for the actual triangle rasterization, because it works in tiles, and they just end up with uneven amounts of work depending on what’s on the screen – there’s nothing we can do about that. That said, we’re definitely hurt by the uneven task sizes here too – for example, on my original Telemetry screenshot, you can clearly see how the non-uniform job sizes hurt us:

The green thread picks up a tile with lots of triangles to render pretty late, and as a result everyone else ends up waiting for him to finish. This is not good.

However, lucky for us, there’s a solution: the TBB task manager will parcel out tasks roughly in the order they were submitted. So all we have to do is to make sure the “big” tiles come first. Well, after binning is done, we know exactly how many triangles end up in each tile. So what we do is insert a single task between

binning and rasterization that determines the right order to process the tiles in, then make the actual rasterization depend on it:

gTaskMgr.CreateTaskSet(&DepthBufferRasterizerSSEMT::BinSort, this, 1, &mBinMesh, 1, "BinSort", &sortBins); gTaskMgr.CreateTaskSet(&DepthBufferRasterizerSSEMT::RasterizeBinnedTrianglesToDepthBuffer, this, NUM_TILES, &sortBins, 1, "Raster Tris to DB", &mRasterize);

So how does that function look? Well, all we have to do is count how many triangles ended up in each triangle, and then sort the tiles by that. The function is so short I’m just gonna show you the whole thing:

void DepthBufferRasterizerSSEMT::BinSort(VOID* taskData, INT context, UINT taskId, UINT taskCount) { DepthBufferRasterizerSSEMT* me = (DepthBufferRasterizerSSEMT*)taskData; // Initialize sequence in identity order and compute total // number of triangles in the bins for each tile UINT tileTotalTris[NUM_TILES]; for(UINT tile = 0; tile < NUM_TILES; tile++) { me->mTileSequence[tile] = tile; UINT base = tile * NUM_XFORMVERTS_TASKS; UINT numTris = 0; for (UINT bin = 0; bin < NUM_XFORMVERTS_TASKS; bin++) numTris += me->mpNumTrisInBin[base + bin]; tileTotalTris[tile] = numTris; } // Sort tiles by number of triangles, decreasing. std::sort(me->mTileSequence, me->mTileSequence + NUM_TILES, [&](const UINT a, const UINT b) { return tileTotalTris[a] > tileTotalTris[b]; }); }

where `mTileSequence`

is just an array of `UINT`

s with `NUM_TILES`

elements. Then we just rename the `taskId`

parameter of `RasterizeBinnedTrianglesToDepthBuffer`

to `rawTaskId`

and start the function like this:

UINT taskId = mTileSequence[rawTaskId];

and presto, we have bin sorting. Here’s the results:

**Change**: Sort back-end tiles by amount of work

| Version | min | 25th | med | 75th | max | mean | sdev |
|---|---|---|---|---|---|---|---|
| Initial depth render | 2.666 | 2.716 | 2.732 | 2.745 | 2.811 | 2.731 | 0.022 |
| Balance front end | 2.282 | 2.323 | 2.339 | 2.362 | 2.476 | 2.347 | 0.034 |
| Balance back end | 2.128 | 2.162 | 2.178 | 2.201 | 2.284 | 2.183 | 0.029 |

Once again, we’re 20% down from where we started! Now let’s check in Telemetry to make sure it worked correctly and we weren’t just lucky:

Now that’s just *beautiful*. See how the whole thing is now densely packed into the live threads, with almost no wasted space? This is how you want your profiles to look. Aside from the fact that our rasterization only seems to be running on 3 threads, that is – there’s always more digging to do. One fun thing I noticed is that TBB actually doesn’t process the tasks fully in-order; the two top threads indeed start from the biggest tiles and work their way forwards, but the bottom-most thread actually starts from the end of the queue, working its way towards the beginning. The tiny LOD zone I’m hovering over covers both the bin sorting task and the seven smallest tiles; the packets get bigger from there.

And with that, I think we have enough changes (and images!) for one post. We’ll continue ironing out scheduling kinks next time, but I think the lesson is already clear: you can’t just toss tasks to worker threads and expect things to go smoothly. If you want to get good thread utilization, better profile to make sure your threads actually do what you think they’re doing! And as usual, you can find the code for this post on [Github](https://github.com/rygorous/intel_occlusion_cull/tree/blog), albeit without the Telemetry instrumentation for now – Telemetry is a commercial product, and I don’t want to introduce any dependencies that make it harder for people to compile the code. Take care, and until next time.

The scheduling issue may be due to work stealing. By default a worker pops tasks off of the top of it’s queue, stack-like, whereas stealers grab from the bottom. IIRC.

Probably a way to change that. Or even having a single shared atomic index that you increment at the start of processing a tile to make sure they’re all getting their index based on when they actually started working. That’s extra Contention, but perhaps minor in context.

Which scheduling issue are you talking about?

The last one, where on one worker thread would pick up tasks in reverse order. I.e. smallest first, in this case.

As per the TBB manual, steals don’t reorder jobs. I always get exactly one thread that does this on every task set, so I assume it’s intentional, but I have no idea where in TBB this is done or why.

So I haven’t used TBB, I assumed they use the same algorithms as everyone else (cilk, PPL, etc.), which is consistent with what you’re seeing in the graph.

I.e. whichever worker thread happens to be the last one to finish off the “group” and wake up the continuation tasks puts every single one of the new tasks on its worker queue and starts executing from the end, the other worker threads (now starved) steal from the start of this queue. In this case, the worker that gets the “reverse” order would be whatever worker executed the bin sorting task – is that what you’re seeing?

This is usually a good idea because it reduces contention (steals are rare in cases where tasks spawn child tasks and don’t do these big “global joins” so each queue remains full, and doing them from the back means they only rarely contend with the worker thread that owns the queue).

Either way, having a single global atomic index that each task increments at the start would fix it. That way tasks that start earlier in wall clock time would have a lower index (used to look up in the sorted array), so you’d get the right ordering that way, although having to rely on global counters is a bit unfortunate.

I suspect TBB probably has a gazillion settings and parameters for the scheduler to tweak this behavior.

Yeah, what you describe is consistent with TBB’s behavior.

It doesn’t have any scheduler parameters besides the number of threads to use, though.

Ah, found it: http://threadingbuildingblocks.org/docs/help/reference/task_scheduler/scheduling_algorithm.htm

Looks like changing spawn(..) to enqueue(..) might be enough to switch it to “approximately” FIFO. One-liner!

For folk interested in Telemetry like visualization of tasks, Intel’s free GPA has a platform view which is very similar to Telemetry: http://software.intel.com/en-us/vcsource/tools/intel-gpa (full disclosure I used to work at Intel).

Intel’s game sample group wrote their own simple scheduler which might work better in this case – see http://software.intel.com/en-us/vcsource/samples/tasking-update code and linked article. Using only 4 threads of the potential 8 might be to keep tasks off the main rendering thread’s core, since doing so usually slows things down. I’d expect 7 threads to be better though, particularly since there were a few low CPI functions in the top ten.

I’ll add a few more notes to Doug’s too…

1) If the code were to use a parallel_for or similar construct rather than explicit tasks/task sets (which people are a little too drawn to IMHO), the granularity of tasking can be inferred automatically (see “autopartitioner”) and likely would have avoided the “too many tiny tasks” overhead. Of course it’s always best to give *some* thought to task size, but some simple heuristics based on # HW threads on the machine and total work size (basically how autopartitioner works) usually suffice for the majority of cases. Work stealing should be able to handle the variation in tasks sizes dynamically fairly well with no need to “count” in advance, although obviously if you have that information static scheduling is good too.

2) A lower-overhead alternative to TBB’s tasks is Cilk Plus (a language extension), but you currently need ICC or a branch of GCC to use it. The overhead of Cilk is very low though, so much so that I imagine you could pretty naively use cilk_for’s/spawns and let the scheduler/work stealing completely handle the variation in workload sizes with high efficiency. If I can find some free time, I might try it just for fun :)

In any case, good articles, I’ve been enjoying them :)

If the code was using TBB directly it would be a lot easier to follow what’s going on, and I’d probably just use the parallel_for.

Unfortunately, it’s not even using TBB tasks directly, it has its own task abstraction built on top of that and everything goes through that wrapper layer, which makes it extra-hard to see what’s going on. It also means that TBB never sees the task dependencies directly because the dependency handling gets done somewhere else. As to why that is, I have no idea, but I haven’t touched it.

Ah yeah, fair enough. That sort of layer is unfortunately not very uncommon and falls under my comment about people being “a little too drawn towards [raw tasks]”. I just hate to see full task stealing implementations effectively unable to do their jobs (which they are typically quite good at) because they are hamstrung by people trying to “take control” and treat them just like raw thread pools. In any case, it seems like your modifications captured a good amount of the benefit here; it’s just not always possible to predict task durations until they are running (which is where stealing comes in).

If you want to give it a try with 8 threads (for HT) instead of 4, the settings are in here:

http://threadingbuildingblocks.org/docs/doxygen/a00342.html

Not sure you’ll get any extra performance, but probably worth a try.

Excellent article. Keep writing such kind of information on your blog.

Im really impressed by your blog.

Hey there, You have done an excellent job.

I will certainly digg it and in my opinion recommend to my friends.

I’m sure they’ll be benefited from this website.