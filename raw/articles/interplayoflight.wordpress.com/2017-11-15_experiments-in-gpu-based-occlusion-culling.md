---
title: Experiments in GPU-based occlusion culling
url: https://interplayoflight.wordpress.com/2017/11/15/experiments-in-gpu-based-occlusion-culling/
author: Kostas Anagnostou
published: '2017-11-15'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

Occlusion culling is a rendering optimisation technique that refers to not drawing triangles (meshes in general) that will not be visible on screen due to being occluded by (i.e. they are behind) some other solid geometry. Performing redundant shading of to-be-occluded triangles can have an impact on the GPU, such as wasted transformed vertices in the vertex shader or shaded pixels in the pixel shader, and on the CPU (performing the drawcall setup, animating skinned props etc) and should be avoided where possible.


There are ways to avoid pixel shader work for occluded triangles. In general, a front to back sorted drawcall list, for solid meshes, or a z-prepass rendering architecture will practically eliminate the overhead of shading to-be-occluded pixels. A g-buffer pass or a [visibility buffer](http://jcgt.org/published/0002/02/04/) pass can help reduce the cost as well. Reducing the overhead of vertex shading or, at a higher level, submitting work to the GPU for occluded props/triangles is a harder task.

One option to tackle occlusion culling at a high level is by determining, on the CPU, which props will be occluded by big occluders like walls using software rasterisation. The CPUs can’t do rasterisation as fast as the GPUs though, so the success of this technique will depend on such things as the number of occluders that need to be rasterised, their size on screen, the resolution of the occlusion buffer, how optimised the implementation is to take advantage of SIMD/multithreading etc. Nevertheless this technique is successfully being used in game engines, like [Frostbite](https://www.slideshare.net/DICEStudio/culling-the-battlefield-data-oriented-design-in-practice), and games, like [Killzone 3](https://www.guerrilla-games.com/read/practical-occlusion-culling-in-killzone-3), for low resolution occlusion buffers. Also Intel provides their implementation of [software occlusion culling](https://software.intel.com/en-us/articles/software-occlusion-culling) which is worth studying.

The GPU on the other hand is a very efficient rasteriser which can determine occlusion very quickly and indeed GPUs have supported occlusion queries in hardware for some time now. Although hardware occlusion queries can provide “exact” occlusion results, down to the level of how many pixels are visible, they have two main disadvantages: first, their granularity is at “drawcall level” meaning that we must fence each drawcall with a pair of queries. If you have 1000 drawcalls in your main pass, you will need twice as many queries. If you use instancing, the result of the query will refer to all the instances of a prop (meaning it is all or nothing, there is no way to figure out which individual instances are visible). Attempts have been made to improve this using a [hierarchy](https://developer.nvidia.com/gpugems/GPUGems2/gpugems2_chapter06.html). The second disadvantage is that you need to read the results back to the CPU in order to decide whether a prop is visible. This introduces a sync point, meaning that the CPU will have to wait for the GPU to finish the work to get the results back, then process and submit the unoccluded props to the GPU while it waits around doing nothing. This is highly undesirable so, typically, rendering engines do not wait for the current frame’s occlusion results but use the ones from the previous or the one before that, something that might introduce visible popping with fast moving objects or camera.

An alternative to hardware occlusion culling, which has been used in [The March of Froblins](http://www.chrisoat.com/papers/Oat-Tatarchuk-Froblins-Siggraph2008.pdf) demo and games like [Splinter Cell: Conviction](http://blog.selfshadow.com/publications/practical-visibility/), is to produce a low resolution occlusion buffer on the GPU by rendering the occluders’ depths, and produce a hierarchical depth (Hi-Z) mip chain of that buffer. Then we can determine occlusion for each prop by calculating the screen-space size of its axis aligned bounding box and using it to select a Hi-Z mip level to pull the occluders’ depth for comparison. This is clever trick that avoids rasterisation of the prop we are testing, replacing it with a fixed number of texture reads (4 in the case of Splinter Cell). The visibility test results are then passed back to the CPU which uses them to submit unoccluded props for rendering.

The advantage of this technique, over hardware occlusion queries, is that it offers finer granularity in our tests (we could test individual props or instances without having to submit many drawcalls), as there is no need to render the props at all to determine whether they are occluded or not. The sync point restriction remains though as the results need to be read back on the CPU.

The real issue here is that the CPU needs to know which props are occluded, or not, in order to submit them for rendering. With modern graphics APIs this is not entirely true though, as there is API functionality to let the GPU determine and set up its own work up to a degree, using compute shaders (or write to buffer in general). I recommend reading [these](http://advances.realtimerendering.com/s2015/aaltonenhaar_siggraph2015_combined_final_footer_220dpi.pdf) [two](https://www.ea.com/frostbite/news/optimizing-the-graphics-pipeline-with-compute) very good presentations on occlusion culling and GPU-driven rendering. The described approaches go much deeper, introducing mesh batching into “units” of a fixed number of vertices to improve culling of larger props and combining the visible mesh batches into larger lists for more efficient rendering. Wihlidals’s presentation goes even further to describe a more general compute shader triangle filtering pipeline that eliminates many types of redundant triangle rendering like backfacing triangles (which we still run the vertex shader for), small triangle culling (i.e. triangles that are small enough not to get rasterised) etc. The techniques described in those two presentations rely on advanced API features (DX12 and console) and special processing of meshes/triangles which might be a bit complicated/out of reach in some cases.

In this particular case, I wanted to explore if it is possible to retrofit an occlusion system to an existing content pipeline without extensive changes, something I had to deal with in the previous game I was working on, using a DX11 class API.

A good starting point is the [Splinter Cell: Conviction](http://blog.selfshadow.com/publications/practical-visibility/) technique I mentioned above, updating it a bit to take advantage of newer, DX11 features. In this case I will be using a compute shader to perform the occlusion tests, producing a list of visible props that I will then be consuming on the GPU, avoiding the CPU roundtrip. I will also be using instance rendering to render the props, something that is particularly suited to games that are rendering lots of copies of the same prop.

As we already seen, the technique is comprised of the following steps:

**Occlusion buffer**

Render the depth of all main occluders to the occlusion buffer. In this context “occlusion buffer” is a texture with a DepthStencil view. Depending on your rendering budget and/or the occlusion accuracy requirements, this buffer can be full resolution or it can be lower (half/quarter res). A low resolution buffer for example will be prone to occluding small props more than it should. Also, it can be of power of two dimensions to help with the mip-chain production or not (March of the Froblins demonstrates how the reduction can work with a non power of two occlusion buffer dimensions). You don’t need a pixel shader to write depth to the occlusion buffer, only a simple vertex shader, something that doubles the rate of writing to the buffer.

A side note: it might be worth considering a screen resolution (or quarter resolution) occlusion buffer in cases you’d like to reuse the buffer to prime the main rendering z-buffer to further reduce overdraw.

In my simple demo I render some large “walls”, using a null pixel shader, producing this 1024×1024 z-buffer:

![z-buffer](../../assets/c60e2f26bfc61527.png)


**Hierarchical-Z mip chain**

Create a Hierarchical-Z mip chain of the occlusion buffer, using the max operator to produce each mip level. Depending on what you render into the occlusion buffer, this Hi-z mip chain could also be used in other contexts, for example to speed up volumetric fog calculations, screen space reflections etc. I am using a compute shader to do the downsampling, although I don’t expect a particular advantage in doing so, especially as I don’t have access to async compute to overlap tasks.

In your downsampling shader, in each step, you can either use 4 texture reads to read the depths to calculate the maximum or a Gather operation that will return all 4 depths with one read.

void downscale(uint3 threadID : SV_DispatchThreadID) { if (all(threadID.xy < RTSize.xy)) { float4 depths = inputRT.Gather(samplerPoint, (threadID.xy + 0.5)/ RTSize.xy); //find and return max depth outputRT[threadID.xy] = max(max(depths.x, depths.y), max(depths.z, depths.w)); } }

A disadvantage of this approach is that since Gather does not support mip level selection you will have to create a different shader/rendertarget view per mip level and bind them successively during downsampling. Alternately you can use 4 texture reads with SampleLevel to select the mip to read from.

Running the compute shader as many times as you need to produce the required number of mips, you will get something similar to this HiZ buffer (showing just a few levels).

![z-buffer](../../assets/9e54e410b1f4f971.png)

![z-buffer1](../../assets/fdc45c1224f3af40.png)

![z-buffer2](../../assets/9ad0df3f8641d51d.png)

![z-buffer4](../../assets/176a78d465df5a73.png)


**Prop visibility calculation**

Next, I packed data for instances of props in a Structured buffer. The world transform as well as the axis aligned bounding box should be enough. At this point you can decide whether to let the GPU perform frustum culling along with occlusion culling, meaning that you will have to pass data for all instances in your world or do the frustum culling on the CPU and pass data for only the potentially visible ones. This particular implementation assumes frustum culling on the CPU but it should be easy to extend the code to let the GPU perform it.

Since occlusion will take place on the GPU, and the results consumed by the GPU as well without CPU intervention, we will need to use

void DrawIndexedInstancedIndirect( ID3D11Buffer *pBufferForArgs, UINT AlignedByteOffsetForArgs);

This is functionally the same as DrawIndexedInstanced, the main difference being that it receives the arguments through ID3D11Buffer which is something that we can conveniently write to from a shader.

Occlusion culling is implemented with compute shader, based on the code from Stephen Hill’s [blog post](http://blog.selfshadow.com/publications/practical-visibility/).

Texture2D inputRT : register(t0); RWTexture2D outputRT : register(u0); StructuredBuffer instanceDataIn : register(t1); AppendStructuredBuffer instanceDataOut : register(u0); RWBuffer instanceCounts : register(u1); SamplerState samplerPoint : register(s0); void occlusion(uint3 threadID : SV_DispatchThreadID) { //make sure that we not processing more instances than available if (threadID.x < NoofInstances) { float3 bboxMin = instanceDataIn[threadID.x].bboxMin.xyz; float3 bboxMax = instanceDataIn[threadID.x].bboxMax.xyz; float3 boxSize = bboxMax - bboxMin; float3 boxCorners[] = { bboxMin.xyz, bboxMin.xyz + float3(boxSize.x,0,0), bboxMin.xyz + float3(0, boxSize.y,0), bboxMin.xyz + float3(0, 0, boxSize.z), bboxMin.xyz + float3(boxSize.xy,0), bboxMin.xyz + float3(0, boxSize.yz), bboxMin.xyz + float3(boxSize.x, 0, boxSize.z), bboxMin.xyz + boxSize.xyz }; float minZ = 1; float2 minXY = 1; float2 maxXY = 0; [unroll] for (int i = 0; i < 8; i++) { //transform world space aaBox to NDC float4 clipPos = mul(float4(boxCorners[i], 1), ViewProjection); clipPos.z = max(clipPos.z, 0); clipPos.xyz = clipPos.xyz / clipPos.w; clipPos.xy = clamp(clipPos.xy, -1, 1); clipPos.xy = clipPos.xy * float2(0.5, -0.5) + float2(0.5, 0.5); minXY = min(clipPos.xy, minXY); maxXY = max(clipPos.xy, maxXY); minZ = saturate(min(minZ, clipPos.z)); } float4 boxUVs = float4(minXY, maxXY); // Calculate hi-Z buffer mip int2 size = (maxXY - minXY) * RTSize.xy; float mip = ceil(log2(max(size.x, size.y))); mip = clamp(mip, 0, MaxMipLevel); // Texel footprint for the lower (finer-grained) level float level_lower = max(mip - 1, 0); float2 scale = exp2(-level_lower); float2 a = floor(boxUVs.xy*scale); float2 b = ceil(boxUVs.zw*scale); float2 dims = b - a; // Use the lower level if we only touch <= 2 texels in both dimensions if (dims.x <= 2 && dims.y <= 2) mip = level_lower; //load depths from high z buffer float4 depth = { inputRT.SampleLevel(samplerPoint, boxUVs.xy, mip), inputRT.SampleLevel(samplerPoint, boxUVs.zy, mip), inputRT.SampleLevel(samplerPoint, boxUVs.xw, mip), inputRT.SampleLevel(samplerPoint, boxUVs.zw, mip) }; //find the max depth float maxDepth = max(max(max(depth.x, depth.y), depth.z), depth.w); if (ActivateCulling == 0 || minZ <= maxDepth) { //instance is visible, add it to the buffer instanceDataOut.Append(instanceDataIn[threadID.x].world); InterlockedAdd(instanceCounts[1], 1); } } }

The compute shader receives the input instance data (world space bounding box) and writes out the visible instance prop data (world space transform) in a Append buffer. It also has to write the data to the argument buffer that will be used by DrawIndexedInstancedIndirect to render the instances. Looking at the data DrawIndexedInstanced receives:

void DrawIndexedInstanced( UINT IndexCountPerInstance, UINT InstanceCount, UINT StartIndexLocation, INT BaseVertexLocation, UINT StartInstanceLocation );

at a minimum we will need to provide the number of indices of the mesh (IndexCountPerInstance) and how many instances of the mesh to render (InstanceCount). I used a normal UAV of a 5 unsigned its buffer to achieve that and I cheated a bit setting the number of mesh indices on the CPU when initialising the buffer. Then all I had to do is use an InterlockedAdd on the second position of the buffer, which is the number of instances.

Finally, in the vertex shader that renders the instances of each prop, all I have to do is use the SV_InstanceID to access the data (world matrix) of the current instance:

struct InstanceData { matrix World; }; StructuredBuffer<InstanceData> Instances : register(t0); struct VS_INPUT { float3 vPosition : POSITION; float3 vNormal : NORMAL; float2 vTexcoord : TEXCOORD0; uint vInstanceID : SV_InstanceID; }; struct VS_OUTPUT { float3 vNormal : NORMAL; float2 vTexcoord : TEXCOORD0; float4 vPosition : SV_POSITION; }; VS_OUTPUT VSMain( VS_INPUT Input ) { VS_OUTPUT Output; //get world matrix for this insance matrix world = Instances[Input.vInstanceID].World; Output.vPosition = mul(float4(Input.vPosition, 1), world); Output.vPosition = mul(Output.vPosition, ViewProjection); Output.vNormal = mul(Input.vNormal, (float3x3)world); Output.vTexcoord = Input.vTexcoord; return Output; }

This is the output of the demo, in it I have rendered the occluders with stippled alpha to show what the actually occlude.

You can also see that this occlusion culling is conservative in that it will never occlude something that is visible.

This naive first attempt will work and will perform the culling on the GPU, but it has at least two disadvantages: first it uses an AppendBuffer to output the instance data which although it handles synchronisation for us, it also offers no guarantee about the order the instances will be written to the buffer. This means that if we have chosen to sort the instances front-to-back (to reduce overdraw for example) on the CPU before passing them down to the occlusion shader, this ordering has now been lost. Second, and maybe more important, ideally we would like to perform occlusion for all instances of all props with one pass in order to reduce the number of drawcalls and utilise the compute units better (as opposed to dispatching with a small number of threads/groups). We could additionally write argument data for all meshes in one buffer and since DrawIndexedInstancedIndirect receives an offset into that buffer, it sounds plausible to draw all visible instances of all prop in one go.

Unfortunately at this point we hit a D3D11 restriction, DrawIndexedInstancedIndirect does not support reading the offset into the arguments buffer from another buffer, it must be explicitly passed as an argument during the API call. That prohibits us from using one drawcall to render all instances of all props, we will have to use one drawcall per mesh (which would then render all instances of that mesh that pass the occlusion culling).

Still, it would be desirable if we could cull all types of meshes using one occlusion culling pass at least, to write data for all instances of all props in a “global” buffer. That definitely seems feasible as we have the arguments buffer offset to use on the CPU during each drawcall and StartInstanceLocation sounds ideal as an instance ID offset for each mesh in the global instance data buffer. Then we hit the second restriction, StartInstanceLocation only works in D3D11 for instance data that go through the input assembler (i.e. as a vertex stream) and not accessed through SV_InstanceID like I did. Not to be deterred by this, we will calculate and write that value to the arguments buffer regardless and then read it with an SRV in the vertex shader to apply the instance ID offset manually.

So the plan is to pack the instance data for all meshes in a buffer and pass them down the occlusion shader to cull. In my test scene I have 4 different instanced meshes which I will process in order, something like:

![Input1](../../assets/31fb6667a4545dd6.png)


Then, when I do the rendering, all I need is to pass down an offset to the beginning of the instances for a particular prop. Since the code makes assumptions about the order of the instances, using an AppendBuffer is no longer possible. Also it is highly likely that occlusion will cull some instances and create “invalid” entries in the output buffer that I have no way of skipping/not rendering.

![Culling1](../../assets/de4cd124f3c7cae2.png)


The extra step that we will need to perform in this case, to remove invalid entries from the buffer, is called stream compaction. Briefly, this is how it will work: Instead of writing instance data for each visible instance in the compute shader, we will output a bool value that signifies whether this instance is visible or not.

bool predicate = false; if (minZ <= maxDepth) { //write predicate for this thread predicate = true; //increase instance count for this particular prop type InterlockedAdd(instanceCounts[ instanceDataIn[threadID.x].instanceCountOffset ], 1); } instanceFlagsData[threadID.x] = predicate;

Now, the output of the compute shader looks something like this:

![Culling2](../../assets/47446c51b7af8fdb.png)


The stream compaction pass consists of using the bool values written to the output array as predicates to write instance data (for visible only instances) to the final buffer, preserving in the meantime the ordering. To implement stream compaction in this demo I used the parallel prefix scan method proposed by [Blelloch ](http://www.cs.cmu.edu/~scandal/papers/CMU-CS-90-190.html)and also described in [GPU Gems](https://developer.nvidia.com/gpugems/GPUGems3/gpugems3_ch39.html). Describing the method and its implementation is beyond the scope of this post, I will refer you to the attached links and the demo code for more details.

// Based on Parallel Prefix Sum (Scan) with CUDA by Mark Harris groupshared uint temp[2048]; [numthreads(1024, 1, 1)] void streamcompaction(uint3 threadID : SV_DispatchThreadID) { int tID = threadID.x; int offset = 1; temp[2 * tID] = instanceFlagsDataIn[2 * tID]; // load input into shared memory temp[2 * tID + 1] = instanceFlagsDataIn[2 * tID + 1]; //perform reduction for (int d = NoofInstances >> 1; d > 0; d >>= 1) { GroupMemoryBarrierWithGroupSync(); if (tID < d) { int ai = offset*(2 * tID + 1) - 1; int bi = offset*(2 * tID + 2) - 1; temp[bi] += temp[ai]; } offset *= 2; } // clear the last element if (tID == 0) temp[NoofInstances - 1] = 0; //perform downsweep and build scan for (int d = 1; d < NoofInstances; d *= 2) { offset >>= 1; GroupMemoryBarrierWithGroupSync(); if (tID < d) { int ai = offset*(2 * tID + 1) - 1; int bi = offset*(2 * tID + 2) - 1; int t = temp[ai]; temp[ai] = temp[bi]; temp[bi] += t; } } GroupMemoryBarrierWithGroupSync(); //scatter results if (instanceFlagsDataIn[2 * tID] == true) { instanceDataOut[temp[2 * tID]] = instanceDataIn[2 * tID].world; } if (instanceFlagsDataIn[2 * tID + 1] == true) { instanceDataOut[temp[2 * tID + 1]] = instanceDataIn[2 * tID + 1].world; } if (tID == 0) { //patch up the visible instance counts per prop type, could possible be done in a different compute shader for (int k = 1; k < NoofPropTypes; k++) { instanceCounts[k * 5 + 4] = instanceCounts[(k - 1) * 5 + 4] + //previous prop type offset instanceCounts[(k - 1) * 5 + 1]; //previous prop type number of instances } } }

In short, it will interpret the booleans as integers xn and produce an array of yn elements as such:

y0 = 0

y1 = x0

y2 = x0 + x1

y3 = x0 + x1 + x2

…

yn-1= x0 + x1 + … + xn-2

So given this input:

![Input2](../../assets/890d130881e8fe89.png)


It will produce this output:

![output2](../../assets/5f82f500cfb40447.png)


In reality, the array would be of power of two dimensions to make calculations easier for the parallel scan algorithm. The nice thing about this method is that if we combine the output elements with the input predicates we can get the indices into the output instance data array of the visible instances! That is, we compact the stream producing indices only for the visible elements. For example, something like this:

for ( int i = 0 ; i < NoofInstances ; i ++) { if ( input[i] ) { instanceDataOut[ output[i] ] = instanceDataIn[i]; } }

The above compute shader implementation of the method has two issues, the first is that it can handle inputs of only a maximum of 2048 elements (instances), as it spawns the maximum allowed 1024 threads per thread group and it processes two elements per thread. If the number of instances in our world is larger than that we will need to spread the work across threadgroups and combine the results in the end. The second issue, also discussed by [Mark Harris](https://developer.nvidia.com/gpugems/GPUGems3/gpugems3_ch39.html), is that it will create many bank conflicts due to threads trying to access memory in the same shared memory banks. Bank conflicts are generally bad as they serialise memory access and reduce the opportunity for parallelism. Mark goes on to describe more efficient implementations of this method.

The final step of the shader iterates over the arguments buffer and calculates the StartInstanceLocation offsets for each mesh (prop) type:

if (tID == 0) { //patch up the visible instance counts per prop type, could possible be done in a different compute shader for (int k = 1; k < NoofPropTypes; k++) { instanceCounts[k * 5 + 4] = instanceCounts[(k - 1) * 5 + 4] + //previous prop type offset instanceCounts[(k - 1) * 5 + 1]; //previous prop type number of instances } }

As I mentioned earlier, D3D11 will ignore StartInstanceLocation when the instance data are not provided to the vertex shader via a vertex stream, but there is nothing prohibiting us from binding the arguments buffer with an SRV and applying the offset manually:

struct InstanceData { matrix World; }; StructuredBuffer<InstanceData> Instances : register(t0); Buffer<uint> InstanceArgs : register(t1); struct VS_INPUT { float3 vPosition : POSITION; float3 vNormal : NORMAL; float2 vTexcoord : TEXCOORD0; uint vInstanceID : SV_InstanceID; }; struct VS_OUTPUT { float3 vNormal : NORMAL; float2 vTexcoord : TEXCOORD0; float4 vPosition : SV_POSITION; }; VS_OUTPUT VSMain( VS_INPUT Input ) { VS_OUTPUT Output; uint startInstance = InstanceArgs[StartInstanceOffset]; //get world matrix for this insance matrix world = Instances[Input.vInstanceID + startInstance].World; Output.vPosition = mul(float4(Input.vPosition, 1), world); Output.vPosition = mul(Output.vPosition, ViewProjection); Output.vNormal = mul(Input.vNormal, (float3x3)world); Output.vTexcoord = Input.vTexcoord; return Output; }

And that is it, we can now add instances of many different props to the global instance data buffer and let the occlusion culling shader cull them all in one pass.

In my totally exaggerated test case, the occlusion pass can give some nice savings, reducing the frame time from 5+ ms down to 1.5 ms in some cases (NVidia GTX 970), with negligible occlusion pass cost (0.1 ms), which is nice considering that the occlusion system was “bolted on” with no changes to the content pipeline.

As they say, your mileage may vary and the efficiency of this technique in culling props will depend on the occluders, size of props, typical position of camera etc. For example a big wall with a see-through window will have much reduced efficiency as the conservative downscaling will create big holes in the HiZ buffer. Also being GPU-driven, the technique does not allow the CPU to use the prop visibility to perform some extra processing, like performing skeletal animation or not, or switching an particle effect attached to the prop on/off, or some other gameplay related operations. As we are moving towards GPU driven rendering more (GPU skeletal animation, GPU particles) this might be less of the problem. You could still read the results back on the CPU to make gameplay decisions (delaying a couple of frames so as not to stall).

There is some code available ([100MB download](https://1drv.ms/u/s!AmOPA68QU4JIiNAi_vzwv5K9MKsrwQ)) if you want to have a play (as well as an executable). If you want to build the code you will need [assimp ](http://assimp.sourceforge.net/main_downloads.html)(v1.1 or thereabouts). It is a slice of my perpetually in-development toy engine which at some point I will upload to github.

**Resources on GPU-driven occlusion culling**


Small correction: GPU driven rendering was implemented with DX11

The Red Lynx part only though, if I am not mistaken. The first part is based on MultiDrawIndexedInstancedIndirect.

[…] Experiments in GPU-based occlusion culling […]

[…] Experiments in GPU-based occlusion culling […]

The code in here:

// Texel footprint for the lower (finer-grained) level

float level_lower = max(mip – 1, 0);

float2 scale = exp2(-level_lower);

float2 a = floor(boxUVs.xy*scale);

float2 b = ceil(boxUVs.zw*scale);

float2 dims = b – a;

In my opinion, it seems like the variable “scale” should be multiplied by screen size, Otherwise both boxUVs and scale will always less than zero.

Do you mean that scale can reach negative values? The exp2() function won’t return a negative result so multiplying scale by the boxUVs should never be negative.

Ah, sorry about my explaination got a little problem. I believe the code:

float2 scale = exp2(-level_lower)

should be

float2 scale = exp2(-level_lower) * RTSize.xy;

so that the scale will be the real pixel’s size.

[…] выигрыши не так очевидны (а для заинтересованных вот и вот). Я пока не […]