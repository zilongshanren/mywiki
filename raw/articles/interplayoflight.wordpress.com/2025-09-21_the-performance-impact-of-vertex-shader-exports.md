---
title: The performance impact of vertex shader exports
url: https://interplayoflight.wordpress.com/2025/09/21/the-performance-impact-of-vertex-shader-exports/
author: Kostas Anagnostou
published: '2025-09-21'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

Following up on the previous post on [GPU utilization and performance](https://interplayoflight.wordpress.com/2025/08/29/gpu-utilisation-and-performance-improvements/), and to provide a practical example, I expanded a bit on a topic discussed in brief: vertex shader exports and their impact on performance. To measure the performance cost, I set up a small experiment, rendering 250 instances of a model 10 times, each time increasing the number of vertex attributes by one until it reached a total of 10 float4 vertex exports, in addition to position export:

![](../../assets/324ab09f0201605a.png)


![](../../assets/324ab09f0201605a.png)

In an attempt to isolate the cost of the fixed function units and queues between vertex and pixel shader, I tried to keep vertex attributes (float4) exported simple on both ends, for example in the vertex the exports are nonsense and cheap to calculate:

```
#if NOOFEXPORTS > 1
result.output1 = input.uv.xyxy / 2.0;
#endif
#if NOOFEXPORTS > 2
result.output2 = input.normal.xyzz - 2;
#endif
#if NOOFEXPORTS > 3
result.output3 = input.normal.xyzz/input.uv.x;
#endif
#if NOOFEXPORTS > 4
result.output4 = input.normal.xyzz + input.uv.xyxy;
#endif
```

while on the pixel shader side they were cheap to use

```
#if NOOFEXPORTS > 1
output.colour.rgba += input.output1;
#endif
#if NOOFEXPORTS > 2
output.colour.rgba += input.output2;
#endif
#if NOOFEXPORTS > 3
output.normal.rgba += input.output3;
#endif
#if NOOFEXPORTS > 4
output.colour.rgba += input.output4;
#endif
```

Also, to keep the cost of pixel shading the same for each iteration, I cleared the depth buffer to reintroduce any overdraw. The pixel shader outputs to 2 rendertargets (G-buffer pass).

Low-level NVidia GPU architecture information online is limited, so, to help interpret the results, we will need to piece together how data flows between vertex shader and pixel shader using Nsight GPU trace and [its documentation](https://docs.nvidia.com/nsight-graphics/AdvancedLearning/index.html), the [Nvidia forums](https://forums.developer.nvidia.com/c/developer-tools/nsight-graphics/115) and a few performance analysis posts linked at the end. Although I believe it is accurate, take the high level description below with a pinch of salt. If any of the assumptions is not correct please let me know.

As data is exported from the vertex shader, it is stored in the L1 memory of a SM, in a special allocation called ISBE. Next the Primitive Engine (PE) takes over, reading the data from ISBE and performing culling and clipping operations, eventually storing the data for the new/remaining triangle vertex attributes in L1 again, in another special allocation called TRAM to be used as pixel shader inputs. The GPU allocates 16KB of TRAM per SM and each attribute component takes up 12 bytes per triangle (sizeof(float) x 3), so a single float4 attribute exported by the vertex shader will take up 48 bytes per triangle, 10 float4s would take up 480 bytes per triangle. All ISBE, PE and TRAM can bottleneck data flowing between vertex to pixel shader and stall execution. We will later see manifestations of this as “Allocation” stalls, which refer to not enough memory being available to store data and “Fill” stalls, which are the result of upstream units that can’t fill the memory with data fast enough.

Running the experiment on a RTX 3080 mobile rendering at 1080p, the cost of the drawcall (in ms) as the number of float4 exports increases from 1 to 10 increases as follows:

![](../../assets/322ada3d5ff2d783.png)


![](../../assets/322ada3d5ff2d783.png)

The cost of the drawcalls between 1 and 10 float4 exports almost triples.

Using Nsight Graphics’ GPU Trace to determine how the allocations discussed above vary:

![](../../assets/784bbc645b57365e.png)


![](../../assets/784bbc645b57365e.png)

There is a noticeable increase in the amount of TRAM allocated as the number of float4 attributes exported increases (left to right). Taking the two ends, with 1 float4 export the first drawcall allocates 1,405 bytes per SM:

while with 10 float4 exports, the last drawcall allocates 4,646 bytes per SM.

Also the latter drawcall’s wave launch is stalled by TRAM fill measurably more than the former’s. This indicates that the Primitive Engine struggles to fill TRAM with vertex data and bottlenecks pixel shader execution. Comparing VPC, the PE unit that performs culling and clipping between one

and 10 vertex exports

the pressure on the VPC unit increases significantly, so it becomes more of a bottleneck, and that could possibly explain the TRAM fill warp stalls. Another interesting observation we can make is that the amount of traffic between the L1 and L2 caches increases significantly with the increased number of exports, which might indicate that VPC uses the L2 cache to store data, which is then copied to L1 (TRAM) before pixel shading.

The same is not true for ISBE allocation, which holds the vertex shader output, it looks about the same across all drawcalls

![](../../assets/27437cefc944a974.png)


![](../../assets/27437cefc944a974.png)

VTG refers to shaders processing geometry (vertex, tessellation, geometry). Comparing one float4 export

to 10 exports

we can confirm that the amount of memory allocated is about the same. The amount of vertex shader warps that stall due to ISBE memory space increases significantly as the number of vertex exports increases (stalls due failed allocation), so ISBE space becomes a bottleneck as well.

So, to summarise the a findings so far, it appears that as the number of exports increases, it puts pressure on Primitive Engine and the intermediate memory used to store the vertex attribute data and call stall both vertex and pixel shader execution that will explain the significant increase of the drawcall cost observed.

An interesting question is what happens if the pixel shader doesn’t use the vertex shader exports. For this, I just stripped out the relevant code from the pixel shader and only kept the vertex shader exports. In this case the drawcall cost remains the same regardless of the number of vertex shader exports. To quickly confirm checking the 2 extremes, one vertex shader export (float4)

and 10 vertex shader exports

The amount of TRAM allocated to store the pixel shader inputs is about the same. This indicates that the GPU knows that the vertex exports won’t be used and doesn’t allocate any extra space for them. Whether it is the shader compiler that strips out the unused exports from the vertex shader, or the hardware itself that doesn’t perform the allocations it is hard to say without access to the produced SASS, the shader ISA.

This behaviour is not consistent across GPU architectures from different vendors. I only have an integrated AMD GCN 5.0 GPU in my laptop, but running the same experiment the drawcall cost between runs remains exactly the same regardless of whether the pixel shader uses the vertex exports or not.

![](../../assets/442b537793beef48.png)


![](../../assets/442b537793beef48.png)

Also worth noting that the cost doesn’t increase as fast as on the Nvidia case with the number of vertex exports. It is not clear why there is drop in the cost for 2 exports, but Radeon profiler doesn’t seem to support GCN any more so I guess we’ll never know.

Going back to the main focus of this post, the Nvidia GPU architecture, if we change the exported data type from float4 to float, the drawcall cost as the number of export increases rises much slower, which is expected as the ISBE, PE and TRAM won’t be as much of a bottleneck any more:

![](../../assets/77fa66ff6372dea1.png)


![](../../assets/77fa66ff6372dea1.png)

Also comparing the amount of TRAM allocated when using float4 and float exports

![](../../assets/60f839730f237897.png)


![](../../assets/60f839730f237897.png)

we notice that it increases roughly linearly as well and we can see for example that the amount allocated for 8 float exports is about the same as 2 float4s. The linear increase also implies that export memory allocation has float and not float4 granularity (i.e., it allocates space for 3 floats if needed and does not round up to a float4).

To wrap up the investigation one more quick experiment, to interleave float and int exports as such

```
struct PSInput
{
float output0 : TEXCOORD0;
#if NOOFEXPORTS > 1
int output1 : TEXCOORD1;
#endif
#if NOOFEXPORTS > 2
float output2 : TEXCOORD2;
#endif
#if NOOFEXPORTS > 3
int output3 : TEXCOORD3;
#endif
}
```

This is to determine if the GPU does any packing of floats and if mixing interpolated with non interpolated exports has any impact. It does not seem to make a measurable difference to the cost and intermediate memory allocated as the number of export increases though, which suggests that this particular GPU doesn’t handle float/int export or interpolation types any different.

To wrap up this quick investigation, this was a practical example of how fixed function units and intermediate memory storage can affect utilisation and rendering cost. Again, these findings might not generalise across different vendors’ GPUs, in some cases even across different architectures from the same vendor, so always profile to determine the actual impact with your rendering setup.

**Further reads**

- Optimizing DX12/DXR GPU Workloads using Nsight GPU Trace
[https://developer.download.nvidia.com/video/GDC-19/NSIGHT_GPU_TRACE_Bavoil.pdf](https://developer.download.nvidia.com/video/GDC-19/NSIGHT_GPU_TRACE_Bavoil.pdf) - The Peak-Performance-Percentage Analysis Method for Optimizing Any GPU Workload
[https://developer.nvidia.com/blog/the-peak-performance-analysis-method-for-optimizing-any-gpu-workload](https://developer.nvidia.com/blog/the-peak-performance-analysis-method-for-optimizing-any-gpu-workload) - Life of a triangle – NVIDIA’s logical pipeline
[https://pixeljetstream.blogspot.com/2015/02/life-of-triangle-nvidias-logical.html](https://pixeljetstream.blogspot.com/2015/02/life-of-triangle-nvidias-logical.html)

If you need access to the NVVM IR and SASS/CUBIN, maybe this might help:

https://github.com/a2flo/floor/blob/master/src/device/vulkan/internal/vulkan_disassembly.cpp#L126

This dumps/disassembles everything from Vulkan pipeline cache data, D3D probably has similar functionality? IIRC the on-disk shader cache uses the same data formats, but it’s of course harder to find the correct file there.

Also note that this requires tools from the CUDA SDK, llvm-dis and zstd.

I assume increasing pixel and/or vertex shader cost would at some point make the stalls disappear. So… maybe these costs are less likely to actually matter for real-world shaders?