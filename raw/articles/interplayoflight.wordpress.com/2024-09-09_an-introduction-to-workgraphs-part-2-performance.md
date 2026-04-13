---
title: 'An introduction to workgraphs part 2: Performance'
url: https://interplayoflight.wordpress.com/2024/09/09/an-introduction-to-workgraphs-part-2-performance/
author: Kostas Anagnostou
published: '2024-09-09'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

In the previous [blog post](https://interplayoflight.wordpress.com/2024/06/29/a-quick-introduction-to-workgraphs/) I described a simple workgraph implementation of a hybrid shadowing system. It was based on a tile classification system with 3 levels (or nodes in workgraph parlance), one to decide which tiles are facing away from the Sun, and as such need no shadows, one to raymarch the surviving tiles’ pixels towards the Sun and look for collisions in the depth buffer and a final one to raytrace the remaining pixels to find collisions in the acceleration structure. In this blog post I explore workgraphs performance a bit and share some observations.

There aren’t many details yet how workgraphs work under the hood. At this year’s HPG conference AMD made a [presentation ](https://www.youtube.com/watch?v=ikwIpn_elgA)which briefly discussed how different ring buffers are allocated for each workgraph node, in VRAM, to store commands triggering its execution, written to by other nodes.

![](../../assets/9a9116c2251e18b6.png)


![](../../assets/9a9116c2251e18b6.png)

This is a presentation worth watching, in summary this ring buffer scheme is similar to the mechanism the CPU uses to pass commands down to the GPU, a main difference in this case is that the GPU itself (SIMD units) can write to those ring buffers. The SIMD units will output records to those ring buffers, corresponding to the nodes they are targeting. The Compute unit of the Micro Engine Scheduler will look into those ring buffers and will use any records there to spawn warps for the various SIMD units in the GPU. There is some additional logic to avoid deadlocks by using the declared number of records each node is expected to output, to ensure that the ring buffer for a downstream node can accommodate the submitted work. There is no information yet on how this is implemented on NVidia GPUs.

Going back workgraph performance, the hybrid shadowcasting system was good as a workgraph learning exercise but I didn’t have a reference implementation using a more traditional compute shader based path to compare with, so I decided to convert parts of FidelityFX’s SSSR technique, I already have [integrated to the toy engine](https://interplayoflight.wordpress.com/2022/09/28/notes-on-screenspace-reflections-with-fidelityfx-sssr/), to a workgraph implementation to compare performance. SSSR also implements a classification pass: a compute shader processes the gbuffer deciding which pixels need raymarching based on the material roughness, outputting their coordinates to a large buffer. Not all threads/pixels in a warp will need raymarching, so the classification shader performs an on the fly [stream compaction](https://interplayoflight.wordpress.com/2022/12/25/stream-compaction-using-wave-intrinsics/) to avoid writing invalid threads/pixels to the buffer. Then a second compute shader takes over to do the raymarching and calculate the screen space reflections.

The implementation of those 2 passes as a workgraph was straightforward reusing the shader code from the original implementation with some workgraph specific syntax. All we need is 2 nodes, the first one to classify the pixels:

```
[Shader("node")]
[NodeLaunch("broadcasting")]
[NodeIsProgramEntry]
[NodeDispatchGrid(1, 1, 1)] // This will be overriden during pipeline creation
[numthreads(8, 8, 1)]
void ClassifyPixels_Node(
in uint3 globalThreadID : SV_DispatchThreadID,
in uint2 group_id : SV_GroupID,
in uint group_index : SV_GroupIndex,
[MaxRecords(64)] NodeOutput<ThreadRecord> SSR_Node
)
```

The classification is still performed using the roughness but unlike the original classification there is no need to compact and write anything to a buffer, we just spawn a node for the thread/pixel that needs raymarching. The node input is the pixel coordinates and some info on whether we need to copy the raymarched value to the other quad pixels (and which), packed in 32 bits:

```
struct ThreadRecord
{
uint screenPosX : 15;
uint screenPosY : 14;
uint copy_horizontal: 1;
uint copy_vertical: 1;
uint copy_diagonal: 1;
};
```

The main modification to the original code was to remove the stream compaction and output to the buffer and replace it with this node spawn logic:

```
ThreadNodeOutputRecords<ThreadRecord> threadRecord = SSR_Node.GetThreadNodeOutputRecords(needs_ray ? 1 : 0);
if (needs_ray)
{
threadRecord.Get().screenPosX = screenPos.x;
threadRecord.Get().screenPosY = screenPos.y;
threadRecord.Get().copy_horizontal = copy_horizontal;
threadRecord.Get().copy_vertical = copy_vertical;
threadRecord.Get().copy_diagonal = copy_diagonal;
}
threadRecord.OutputComplete();
```

I kept the parts of the code that output which tiles need denoising for the denoising pass for reasons I will explain later.

The second node needed is one to raymarch a particular pixel:

```
[Shader("node")]
[NodeLaunch("thread")]
void SSR_Node(
ThreadNodeInputRecord< ThreadRecord> inputData
)
```

Again, the code is reused straight from the original SSSR, nothing worth calling out here. That node writes the reflections to a rendertarget, ready to be used by the denoising passes.

I mentioned earlier that, for simplicity, I only ported the classification and raymarching passes, the reason for this is that denoising introduces a dependency between neighbouring tiles, take for example a blur filter towards the edge of a tile. This will need access to the pixels of the tile next to it but there is no guarantee that that tile’s pixels will have been processed by the time this is required. With a compute shader based approach, this would be solved by a barrier between the dispatches (some more info on node synchronisation in workgraphs [here](https://microsoft.github.io/DirectX-Specs/d3d/WorkGraphs.html#joins---synchronizing-within-the-graph))

Quick showcase of SSSR using the workgraph for classification and raymarching, the output is identical to the original implementation:

![](../../assets/81ffca6a6ceed574.png)


![](../../assets/81ffca6a6ceed574.png)

We now have something that we can compare the workgraph implementation to. All rendering costs refer to SSSR targeting a 1080p resolution on an RTX 3080 laptop GPU. Checking the original implementation in GPU Trace, focusing on the classification and raymarching passes, they add up to a total of 0.65ms:

![](../../assets/a162f66ac45a3886.png)


![](../../assets/a162f66ac45a3886.png)

The bottom graph, in orange, is the shader occupancy. We can also see the drain that is needed due to the barriers (blue lines) between those 2 passes to ensure that the UAV buffer has been fully written to before raymarching can begin. In this case there is a second barrier because there is another quick pass between classification and raymarching to prepare the indirect dispatch arguments.

Next is the equivalent functionality implemented as a workgraph:

![](../../assets/71d10ec1ea139fc9.png)


![](../../assets/71d10ec1ea139fc9.png)

The execution cost is now 2.18ms.

It looks like there is some structure in the occupancy graph starting with a big block followed by a number of similarly shaped smaller blocks. Nsight Graphics’ GPU Trace (using version 2024.2) recognises workgraphs, and can show the utilisation of the various units, similarly to a compute shader, but it doesn’t seem to provide a deeper analysis of the reasons why warp launch stalls. It appears that the workgraph version has lower shader occupancy in overall.

Quick comparison of the combined top level bottlenecks for the compute shader version

and the workgraph based version

shows much lower SM utilisation and also warp occupancy in the latter.

Performing the capture with Real-Time Shader Profiler on:

will provide some more information on the workgraph:

![](../../assets/5530c899ca5e679b.png)


![](../../assets/5530c899ca5e679b.png)

Here we can see that the Classification Node has a theoretical occupancy of 32 and the SSSR (Raymarching) node an occupancy of 16. In the compute shader version, Classification and Raymarching shaders both have a theoretical occupancy of 32.

Latest NSight Graphics introduces a nice new feature, by right clicking on a shader in the Shader Pipelines tab above we can see it where in the timeline it is executing. Workgraphs are supported as well, for example this is the execution for the classification node, zooming in a bit to see more detail:

![](../../assets/a7563edfb399bdd7.png)


![](../../assets/a7563edfb399bdd7.png)

and this is the execution for the raymarch node

![](../../assets/f91757fdc842dedb.png)


![](../../assets/f91757fdc842dedb.png)

We notice some overlap in the execution, it appears as if in the repeated pattern in the shader occupancy graph, the first peak belongs to the classification and the large drain belongs to the raymarching node execution.

To understand the performance profile let’s take a step back and simplify the problem a bit focusing on the classification node alone and modifying it not to spawn any Raymarching nodes.

![](../../assets/c24e103fcce4a34e.png)


![](../../assets/c24e103fcce4a34e.png)

Although not totally equivalent in the work they do, a workgraph with only classification nodes spawned costs 0.49ms, compared to the compute shader based classification pass cost of 0.15ms.

According to GPU trace, the theoretical max occupancy of both is the same, at 32 warps per SIMD, but the actual average occupancy is 25 (52%) for the compute shader version and only 13 (27%) for the workgraph version. One interesting thing I noticed comparing the GPU Traces for both passes, is that while for the compute shader based ClassifyTiles the number of threadgroups launched (32,400), the number of warps launched (64,800) and threads launched (2,073,600) are as expected for a 8×8 threadgroup and a 1920×1080 image, the corresponding numbers for the workgraph based one are quite different: thread groups launched is 40,516, number of warps is 72,937 and the number of threads is 2,082,822. These numbers make little sense, for example, even if the number of thread groups was correct you’d expect 40,516 threadgroups (8×8) to launch 81,032 warps. I did a quick experiment spawning nodes with a 8×4 threadgroup size (exactly a warp) and although the number of threads launched was the same as in the 8×8 case, the number of threadgroups launched was 72,916 and the number of warps launched was 72,937. These numbers all are far from the expected but this time the number of (warp-sized) threadgroups and the number of warps are much closer. I am not sure if this a bug in NSight or in the driver or there is something in the way workgraphs launch work.

Another interesting thing I noticed was that spawning the ClassifyTiles node without it doing any work (shader has an empty body) does not really reduce its execution time. The compute shader version of the ClassifyTiles pass with an empty shader costs ~0.03ms. The workgraph based version costs 0.38ms only around 1ms less than the version that does actually do work (but not spawn any nodes). Comparing the instructions executed by the non-empty ClassifyTiles workgraph node:

with that executed by the empty node

the empty node seems to spend most of its time in shared memory instructions, synchronisation instructions and integer maths, which may have to do with indexing. This suggests that there is likely quite a bit of overhead in the spawning of the workgraph nodes and most of the original ClassifyTiles node cost is due to this.

Going back to the full workgraph SSSR implementation, one thing that stands out is the Sync Q Waiting metric in GPU Trace, something that doesn’t appear for the compute shader version:

![](../../assets/ee997dca59e78d0c.png)


![](../../assets/ee997dca59e78d0c.png)

This signifies that the Front End, which receives instructions and dispatches them to either the graphics or compute pipes, is stalling. There isn’t enough info to determine if this is related to the way nodes are launched and executed but there might be a correlation.

So far I launched nodes to perform the raymarching using the “thread” launch mode, which sounds like a natural fit to the way the Classification node determines per pixel whether it needs raymarching or not. With this mode, the GPU will try to batch threads into warps but there is no guarantee where (which warp) they will end up in. An alternative to this launch mode is “coalescing”, in which we can declare a thread group size which the GPU will attempt to (but there is no guarantee that it will manage to) fill with the maximum number of records specified:

```
[Shader("node")]
[NodeLaunch("coalescing")]
[NumThreads(64, 1, 1)]
void SSR_Node(
[MaxRecords(64)] GroupNodeInputRecords<ThreadRecord> inputData,
uint threadIndex : SV_GroupIndex
)
{
}
```

If we compare to the top bottlenecks of the “thread” launch SSSR node above, the SM throughput is a few percent higher in this case and also the occupancy has increased to 23.3% up from 18.4%,

Also, the overall workgraph dispatch cost when down from 2.18ms to 1.81ms a noticeable improvement. Although [the advice](https://devblogs.microsoft.com/directx/d3d12-work-graphs) is to use coalescing only if you need to use thread group shared memory, in this case it appears that this helps a bit with cache efficiency (L1TEX throughput 15.6% compared to 13% with thread launch) and this contributes to the cost reduction.

I ended this investigation with more questions about workgraphs’ performance than I answered. For the usecase I profiled, possibly for typical classification based techniques, workgraphs appear to be much slower at the moment. It is early days though and I am sure and performance will improve, this is a very exciting technology and I am looking forward to seeing how it will evolve.

Some knowledge of how workgraphs are implemented internally by each IHV would be helpful, as well as deeper profiling and debug info will be necessary for efficient workgraph programming. To add to the wish list, it would be great if NSight Graphics also showed the produced SASS for the shaders to get a better idea what happens under the hood.

I hope people at NV and AMD see this!

Thanks a lot for this great blog post and digging into the numbers! Would be interesting to see that same comparison on an AMD card. The last (AMD) workgraph sample that I checked ran quite horrible on my NV. But that’s already some time ago.

NVIDIA implementation feels like a while loop which polls ready-to-dispatch work of all graph nodes, dispatch them (max in-flight warps), join all (sync with atomics, maybe cost quite some registers, hurting occupancy?), then run the next batch.

Don’t know if AMD cards work similarly.