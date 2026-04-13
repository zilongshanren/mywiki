---
title: Async compute all the things
url: https://interplayoflight.wordpress.com/2025/05/27/async-compute-all-the-things/
author: Kostas Anagnostou
published: '2025-05-27'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

GPUs make work parallelism very easy by design: each drawcall/dispatch shader instruction operates on batches of vertices, pixels, threads in general at the same time automatically. On the other hand, GPU work is pipelined, its architecture comprises various specialised (fixed function like input assembler, raster) and programmable (like Streaming Multiprocessor/SM) units connected by queues and depending on the nature of the work, a particular unit can become a bottleneck leaving the rest of the GPU underutilised.

We see this quite often in modern engines: rendering might start with some compute shader work to calculate a fluid simulation for example, followed by a GPU skinning pass both often memory and ALU bound, then by a shadow pass, a z-prepass maybe and a g-buffer pass, work that is mainly bottlenecked by geometry processing, i.e. vertex and triangle throughput. Then, for the rest of the frame the GPU transitions to more intensive pixel processing work, either with pixel or compute shaders, stressing again ALUs, caches and memory bandwidth.

My toy renderer is in no way representative of a AAA renderer, nevertheless, a GPU trace can give an example of this in practice:

![](../../assets/63251272df4365d8.png)


![](../../assets/63251272df4365d8.png)

The GPU units utilisation is very uneven, the shadow pass and the g-buffer pass put more pressure on the World Pipe (geometry processing) and VRAM to bring in vertices and textures while screen space lighting techniques like GTAO stress cache and ALU (SM) more. Often the GPU loads between passes are complementary and all passes underutilise some parts of the GPU, potentially leaving performance on the table.

To address this, IHVs have in the past few GPU generations, introduced the Asynchronous Computing (aka async compute, AMD) and Simultaneous Compute and Graphics (NVidia) technologies aimed to improve GPU utilisation by dispatching instructions from different tasks for SM execution, in parallel. This is achieved by separate hardware pipelines, graphics and compute, to submit to and schedule work.

Graphics APIs abstract the hardware pipelines using command queues (DirectX 12), there is one for graphics and compute work (graphics command queue) and one for compute work only (compute command queue). There is also a copy queue for data transfers but it is not relevant to this discussion. All the work we submit to a command queue via command lists, to implement for example techniques like shadowmap rendering, ends up being submitted to a hardware pipeline to be scheduled for execution. Unlike the graphics command queue, the compute queue only has access to units that involve shader execution (SM/caches) and not geometry processing, rasterisation and backend to write to rendertargets, i.e. it has less dependency on fixed function units. The idea is that overlapping work on multiple queues will increase GPU utilisation and improve performance.

Async compute is more of a scheduling mechanism, all tasks still target and compete for the same GPU resources (SM, caches, memory bandwidth). This means that based on how well we manage to pair tasks with the graphics queue will determine if async compute improves or worsens performance. For example pairing tasks that both are ALU bound, or memory bound may increase contention and possibly slow both down.

Let’s say that we want to move to async compute the GTAO (SSAO) technique in the GPU trace screenshot I shared above. The GTAO is cache first and ALU (SM) bound, while the raytraced shadows pass next to it is mainly RT core bound, it looks like pairing them is a good match.

![](../../assets/11ca627b6211e165.png)


![](../../assets/11ca627b6211e165.png)

Moving work to a compute queue is relatively straightforward, the first step is it create another command queue declaring it as “compute” only:

```
D3D12_COMMAND_QUEUE_DESC queueDesc =
{
D3D12_COMMAND_LIST_TYPE_COMPUTE,
D3D12_COMMAND_QUEUE_PRIORITY_NORMAL,
D3D12_COMMAND_QUEUE_FLAG_NONE
};
m_device->CreateCommandQueue(&queueDesc, IID_PPV_ARGS(&m_computeCommandQueue));
```

Then we create command lists as normal and submit them to the compute queue for scheduling and async execution. There is one complication what needs special handling: once the work starts on the compute pipe, we need a way of knowing when it will finish. If the async task has any dependencies up stream, we need a way of knowing when they will be ready. In this particular case for example, GTAO needs the depth buffer and the normal buffer from the G-buffer pass so it can’t start before it finishes and downstream, the Composite pass needs to use the output of GTAO so it can’t start before GTAO finishes. The way to coordinate all this and work across GPU pipes in general is by using [fences](https://learn.microsoft.com/en-us/windows/win32/api/d3d12/nn-d3d12-id3d12fence). Using a fence object the command queues can notify that a command list has finished execution by using the Signal() method, or wait for a command list to finish execution, using the Wait() method.

In the above case I set it up roughly as follows

```
// fences and values variables added here for reference
ComPtr<ID3D12Fence> m_toGraphicsFence; // to notify the graphics queue
ComPtr<ID3D12Fence> m_toComputeFence; // to notify the compute queue
UINT64 m_toGraphicsFenceValue;
UINT64 m_toComputeFenceValue;
//create command list for gbuffer pass
RenderGBuffer();
if (m_state.AppSettings.AsyncCompute)
{
// execute command list
m_commandList->Close());
m_commandQueue->ExecuteCommandLists(1, CommandListCast(m_commandList.GetAddressOf()));
// Add a signal command to the graphics queue to notify listeners
m_commandQueue->Signal(m_toComputeFence.Get(), ++m_toComputeFenceValue));
}
// .. do other work
if (m_state.AppSettings.AsyncCompute)
{
// wait for the GBuffer rendering work to finish
m_computeCommandQueue->Wait(m_toComputeFence.Get(), m_toComputeFenceValues);
}
// create command list for GTAO
RenderGTAO();
if (m_state.AppSettings.AsyncCompute)
{
// execute the command list on the compute pipe
m_computeCommandList->Close());
m_computeCommandQueue->ExecuteCommandLists(1, CommandListCast(m_computeCommandList.GetAddressOf()));
// notify any listeners downstream when the work is done
m_computeCommandQueue->Signal(m_toGraphicsFence.Get(), ++m_toGraphicsFenceValues));
}
// .. do other work
if (m_state.AppSettings.AsyncCompute)
{
// execute command list
m_commandList->Close());
m_commandQueue->ExecuteCommandLists(1, CommandListCast(m_commandList.GetAddressOf()));
// wait for the signal for GTAO completion.
m_commandQueue->Wait(m_toGraphicsFence.Get(), m_toGraphicsFenceValues);
}
//Create command list for composite pass
RenderComposite();
```

This is pretty much all that is needed to submit work to the 2 command queues and synchronise between them, effectively a command queue signals completion of a command list and the other command queue waits for that signal before it executes its own command list. Worth mentioning that Wait() is blocking on the GPU (but not on the CPU), work will stop on that command queue/hardware pipe until it gets the Signal() from the other command queue.

In a proper engine command list creation would be multithreaded and each pass would likely have its own command list. In my toy engine I use a single command list for graphics and another one for compute so to simplify things I close, execute and reuse them.

There is one more thing to consider, we talked about how the compute queue can’t see the fixed function units related to vertex and pixel shader execution. This has a knock on effect on resource transitions, a command list submitted to the command queue can’t transition a resource from states like D3D12_RESOURCE_STATE_RENDER_TARGET or D3D12_RESOURCE_STATE_PIXEL_SHADER_RESOURCE. Transitions like these need to happen on the graphics queue.

With this in place, let’s start reviewing some performance results. Here we see the outcome of GTAO running on the compute pipe with correct synchronisation using a fence (all costs refer to an NVidia 3080 mobile running at 1080p):

![](../../assets/51cf1cbf6f879a44.png)


![](../../assets/51cf1cbf6f879a44.png)

The task starts after the GBuffer pass has finished and runs in parallel to the raytraced shadows pass on the compute pipe. The throughput of the various units has improved and the GPU is now better utilised. GTAO and shadows when run serially take 5.73ms, while when GTAO runs async over the raytraced shadows, the combined cost is about 4.6ms a saving of more than a ms (it is slightly more as GTAO overlaps the hierarchical depth buffer pass a bit as well). Even if the pairing between these 2 tasks is good, there is still an impact on the cost of the individual tasks, they are both individually more expensive compared to when run serially on the graphics pipe, for example the GTAO cost increases from 1.97ms to 3.22ms. What really matters in this case though is the combined cost when run in parallel and this is the measure of success.

One thing worth checking is if running GTAO on the compute queue alone has any impact on its execution time.

![](../../assets/effbb48d012c2ed9.png)


![](../../assets/effbb48d012c2ed9.png)

Interestingly no, it takes the same amount of time when scheduled on the compute pipe and when running alone, indicating that there is nothing inherently limiting when running a task async, it is the contention for GPU resources that slows the 2 overlapped tasks down.

If by the time the downstream task needs to run a Signal() from the other command queue has been called with the appropriate fence value, Wait() doesn’t have an impact on the execution. If Signal() hasn’t be called and the correct fence value hasn’t been sent, GPU execution on the command queue will block, draining the hardware pipe from any work. To showcase this I made the raytraced shadows pass artificially faster and moved the Wait() right after it on the graphics queue.

![](../../assets/5461f350b8b55138.png)


![](../../assets/5461f350b8b55138.png)

We notice 2 things, first all work on the graphics pipe stops when the Shadowmask dispatch finishes as all subsequent work must Wait() for the correct fence value and this doesn’t happen until GTAO finishes, creating a bubble. This highlights a potential difficulty in scheduling async work with varying workloads on the graphics pipe, as they can finish earlier or later. Second, the GTAO cost is much smaller in this case compared to what it was when it fully overlapped the Shadowmask pass earlier, 2.3ms vs 3.22ms, which indicates that there is no static allocation/assignment of SMs to each task, and that the GPU can dynamically reallocate SMs to each hardware pipe as needed.

We talked about how correct pairing of tasks is of great importance and will determine the success of async compute and this is likely the harder to get right aspect of it. Focusing on SM (ALU) throughput alone is not enough, for example overlapping GTAO over a BRDF LUT dispatch that is SM bottlenecked, even though GTAO itself is ALU heavy:

![](../../assets/7dddd6e239bfd697.png)


![](../../assets/7dddd6e239bfd697.png)

leads to the combined pass of the 4 passes (Hierachical depth, GTAO, BRDF LUT and Shadowmap) dropping from 7ms down to 5.7ms, effectively giving us the BRDF pass for “free”:

![](../../assets/9320271e70b1c643.png)


![](../../assets/9320271e70b1c643.png)

Overlapping GTAO over other work that has both high SM and cache throughputs, such as the Generate Rays for RTGI and Lighting passes leads to somewhat reduced gains dropping the combined cost from 6.8ms (on the graphics pipe) to 6.1ms

![](../../assets/66297a26b3a305b4.png)


![](../../assets/66297a26b3a305b4.png)

Like discussed, the 2 command queues dispatch work in parallel, letting the tasks contest for GPU resources during execution. There is no good way to determine the priority of each tasks, there is a Priority field in D3D12_COMMAND_QUEUE_DESC which can be set to Normal or High but I found it to make no different on this GPU.

In the end it will take some experimentation to determine what works best in your case, comparing the main bottlenecks and SM occupancy for each pass and attempting and profiling combinations that reduce GPU resource contention to achieve the best possible utilisation.

For example, like I mentioned at the start of the post, the frame typically starts geometry bound, with shadowmap rendering pass, z-prepass and g-buffer pass usually bottlenecked by vertex and triangle processing and rasterisation. This is a good opportunity to overlap compute shader work to soak up all the unused SM. Since a lot of screen space lighting passes depend on the g-buffer output, swapping the order of shadow map rendering and g-buffer pass and overlapping this work over the shadowmap pass might be a good idea.

In this case overlapping GTAO, RTGI ray generation and BRDF LUT generation for good measure over the shadowmap rendering pass reduces the combined cost from to 6.63ms when running on the graphics pipe to 4.71ms when running async.

![](../../assets/eb96504683a3f2f1.png)


![](../../assets/eb96504683a3f2f1.png)

It also appears that GTAO is a better pairing for (rasterised) shadowmap rendering than raytraced shadows we examined earlier, finishing in 2.1ms as opposed to 3.22ms.

Although GPU are getting increasingly “wider”, capable of parallelising massive amounts of work, there will always be units to bottleneck execution and for that, async compute is something worth considering to fill-in those low utilisation moments. YMMV though depending on the engine architecture and rendering passes implemented as well as the targeted GPUs as their level of support for async compute may vary and will require experimentation to find which pairings work well for your case. It is also worth adding support for both async and non-async execution paths for a compute task to compare costs in each case and also for when improving the performance of a dispatch which should be done on the graphics queue, non-overlapping, to determine the real impact of the improvement work with no resource contention.

**Further reads**

- Advanced API Performance: Async Compute and Overlap
[https://developer.nvidia.com/blog/advanced-api-performance-async-compute-and-overlap/](https://developer.nvidia.com/blog/advanced-api-performance-async-compute-and-overlap/) - Deep Dive: Asynchronous Compute
[https://gpuopen.com/wp-content/uploads/2017/03/GDC2017-Asynchronous-Compute-Deep-Dive.pdf](https://gpuopen.com/wp-content/uploads/2017/03/GDC2017-Asynchronous-Compute-Deep-Dive.pdf) - Breaking Down Barriers: An Intro to GPU Synchronization
[https://gpuopen.com/gdc-presentations/2019/gdc-2019-agtd5-breaking-down-barriers.pdf](https://gpuopen.com/gdc-presentations/2019/gdc-2019-agtd5-breaking-down-barriers.pdf)

Very useful practical info, thanks for posting!

Do you think this is what workgraphs are doing under the hood?