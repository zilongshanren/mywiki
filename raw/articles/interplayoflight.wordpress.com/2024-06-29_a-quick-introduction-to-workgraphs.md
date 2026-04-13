---
title: A quick introduction to workgraphs
url: https://interplayoflight.wordpress.com/2024/06/29/a-quick-introduction-to-workgraphs/
author: Kostas Anagnostou
published: '2024-06-29'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

Workgraphs is a new feature added recently to DirectX12 with hardware support from NVidia and AMD. It aims to enable a GPU to produce and consume work without involving the CPU in dispatching that work. I spent some time the past couple of weeks experimenting with workgraphs and I’ve put together this high level tutorial on how one can go about using them.

I cobbled together parts I already had in the toy engine to implement a shadow raytracer, comprised of 3 steps: first isolate and filter out pixels that are backfacing to the light (and as such are always is shadow), raymarch the surviving pixels towards the light looking for hits in the depth buffer and then, for pixels that failed to find a hit, raytrace using the acceleration structure. The technique, even if a bit contrived and maybe not too practical, it provides us with many opportunities to produce and consume work on the GPU.

It is beyond the scope of this article to provide a comprehensive introduction to workgraphs, I have listed a few tutorials and posts at the end of the page for further reading. I will only summarize the aspects required for this post. You can imagine a workgraph as a graph of nodes. Each node receives some data either from other nodes or memory, performs some work and outputs data to other nodes or memory. To bring it more into the familiar context of graphics programming, each node is a shader which receives input from other shaders without the typical CPU involvement to dispatch the shader. It is worth mentioning that, at the moment, only compute shaders and inline raytracing are supported but support for other types of shaders is also planned.

Let’s cycle back to the description of the technique to implement, like discussed it has 3 passes:

- a coarse pass to reject tiles of backfacing pixels
- a pass to raymarch pixels in tiles to find collisions in the depth buffer
- a pass to raytrace remaining pixels to find collisions in the acceleration structure.

We can express the above system as a graph with 3 nodes, each producing and feeding data to the other.

![](../../assets/3f4249d1abfe9a99.png)


![](../../assets/3f4249d1abfe9a99.png)

The first node (shader) works on screen tiles; if all pixels in the tile are backfacing (to the light) it stops execution and writes a shadow factor of zero in the shadowmask (shadowmask is a rendertarget where each pixel stores the result of the shadow calculations. It is later used during lighting to occlude the light). Starting with the definition of a node, it is not too dissimilar to a compute shader’s with some specialised annotation:

```
[Shader("node")]
[NodeLaunch("broadcasting")]
[NodeIsProgramEntry]
[NodeDispatchGrid(1, 1, 1)]
[numthreads(8, 8, 1)]
void ClassifyPixels_Node(
in uint3 globalThreadID : SV_DispatchThreadID,
in uint2 groupId : SV_GroupID,
in uint groupThreadIndex : SV_GroupIndex,
[MaxRecords(1)] NodeOutput<TileRecord> Shadows_Node
)
```

There are a couple of things to elaborate on here. The more obvious ones, “NodeIsProgramEntry” defines this shader as the start of the graph, the entry point. “numthreads” is the classic way to define the size of a threadgroup, and “NodeDispatchGrid” how many threadgroups to dispatch. In this instance it has a default value that will get overridden during PSO creation as it depends on the shadowmask size. The inputs to the shader (SV_DispatchThreadID, SV_GroupID etc) are familiar as well from compute shaders. What is really new with workgraphs is the way to launch the node (NodeLaunch) and the definition of the output (NodeOutput).

Briefly, there are 3 ways to launch a node, namely “broadcasting”, “thread” and “coalescing”. The main difference from a user perspective is in the granularity of execution and the way each node receives data (records). With broadcasting the notion of a threadgroup persists, not unlike a classic compute shader dispatch, and all threads in it receive the same data record (NodeOutput). “Same data” could for example be the coordinates of a tile during a tile classification pass. This is the way to launch the node if you want the threads in the threadgroup to share data, using group shared memory. With “thread” launch each thread receives a different data record (NodeOutput). Example of per thread record data could be pixel coordinates, world position, etc. In this case though there is no notion of a threadgroup and the threads can’t use group shared memory any more. They can still use Wave Intrinsics to share data between threads in a wave. The final launch mode is “coalescing”. This sits somewhere between broadcasting and thread launch mode and allows the GPU to attempt to batch individual workitems/threads into threadgroups so that they can share data through groupshared memory. In this example I will be using broadcasting and thread launch modes. To wrap this brief introduction it is worth mentioning NodeOutput, which declares the output of the node, using and arbitrary structure (TileRecord), which depending on the launch mode can be one per threadgroup, one per thread etc, like discussed.

Let’s start with a concrete node example to put the theory into practice, the first workgraph node will check if each 8×8 image tile contains all “backfacing” (to the light) pixels and if it does it will stop execution. Else it will spawn a new node per threadgroup to process the tile further.

```
struct TileRecord
{
uint2 tileXY;
};
groupshared unsigned int g_allbackfacing;
[Shader("node")]
[NodeLaunch("broadcasting")]
[NodeIsProgramEntry]
[NodeDispatchGrid(1, 1, 1)] // This will be overridden during pipeline creation
[numthreads(8, 8, 1)]
void ClassifyPixels_Node(
in uint3 globalThreadID : SV_DispatchThreadID,
in uint2 groupId : SV_GroupID,
in uint groupThreadIndex : SV_GroupIndex,
[MaxRecords(1)] NodeOutput<TileRecord> Shadows_Node
)
{
if ( groupThreadIndex == 0 )
{
g_allbackfacing = 1; // initialise group shared memory
}
Barrier(GROUP_SHARED_MEMORY, GROUP_SCOPE|GROUP_SYNC);
uint2 screenPos = globalThreadID.xy;
float3 normal = ...
float NdotL = dot(normal, lightDir.xyz);
bool backfacing = NdotL <= 0;
// check if all threads in the wave are backfacing
bool allBackfacing = WaveActiveAllTrue(backfacing);
//do an interlocked operation only for the first thread in the wave
if ( WaveIsFirstLane() )
{
int previous;
InterlockedAnd(g_allbackfacing, allBackfacing ? 1 : 0, previous);
}
Barrier(GROUP_SHARED_MEMORY, GROUP_SCOPE|GROUP_SYNC);
// create a record for this tile
GroupNodeOutputRecords<TileRecord> tileRecord = Shadows_Node.GetGroupNodeOutputRecords(g_allbackfacing ? 0 : 1);
if ( !g_allbackfacing )
{
if (groupThreadIndex == 0 )
tileRecord[0].tileXY = groupId; // if not all backfacing write tile coordinate
}
else
{
shadowMask[screenPos] = 0; // else add a zero shadowfactor
}
// mark the node record as complete.
tileRecord.OutputComplete();
}
```

A few things to discuss here, we’ve already talked about the node declaration, worth mentioning that the NodeDispatchGrid size is placeholder and will be overridden on the CPU as it depends on the rendertarget size. The rendertarget itself is split into 8×8 tiles. We allocate some groupshared memory to store whether all threads in that tile are backfacing (NdotL <= 0). That value is different per thread and normally we would need atomic operation to safely access the groupshared memory to “AND” the result. This is a slow operation though as all threads will try to access the memory at the same time effectively serialising access. A much better approach is to use wave intrinsics to calculate the combined result for the whole wave and use just one atomic operation per wave, reducing the number of atomic operations from 64 (8×8 tile size) to just 2 (2 waves of 32 threads in that tile). Since there is no guarantee when the group shared memory will be accessed we also need to add barriers to wait until all group shared memory operations are done before we proceed. Barrier() is a new instruction that replaces all the GroupMemoryBarrier(), GroupMemoryBarrierWithGroupSync(), DeviceMemoryBarrier() etc variations with one single intrinsic which uses flags to declare the behaviour of the barrier.

A quick detour to talk about the groupshared memory and barriers, these are actually needed because with the current configuration we have 2 waves per threadgroup (I am targeting an Nvidia GPU with 32-thread waves and an 8×8 threadgroup). If the threadgroup size was equal to the wave size WaveActiveAllTrue(backfacing) alone would be enough to classify the tile as all backfacing or not. We could make the threadgroup 8×4 and get rid of all these but I’ve found that the larger the threadgroup the better this first classification pass performs, removing large areas in the image from the later, more expensive stages. Your mileage may vary, always profile to find the best setup.

Jumping back to the node declaration, we specified the node output as: [MaxRecords(1)] NodeOutput Shadows_Node. This means that the current graph node can spawn a maximum of one data record for the graph node named Shadows_Node (we will get back to that later). To actually create that data record for the current tile we can use this instruction:

```
GroupNodeOutputRecords tileRecord = Shadows_Node.GetGroupNodeOutputRecords(g_allbackfacing ? 0 : 1);
```

This will create a number of records for this tile. Since we only emit one record per tile from that node, we need to specify 0 or 1 nodes based on whether the whole tile is backfacing or not (we also promised that we will only spawn a maximum of one record with MaxRecords(1)). Then based on the value of g_allbackfacing we can choose to populate that record with the tile coordinate, if not all threads are backfacing, or ignore it and write a shadow value of zero for all threads if all are backfacing. Finally, we signify that are done modifying the record by calling tileRecord.OutputComplete(). And that is it, we’ve successfully created a node that will either spawn another node to process the current tile or cut execution short and fill the shadowmask with zeros for that tile.

Before we move on one important thing to mention: the call to GetGroupNodeOutputRecords() must be threadgroup uniform. This means that it can’t be included in an if-statement or used in a thread-divergent way. Same holds true for OutputComplete(), that is why they are both use outside the if-statement. In this case this has little impact as the operation we performed applies to the whole threadgroup, so there is no opportunity for divergence but this will matter later. Failure to respect this will lead to undefined behaviour.

Time to talk about the second node of the graph. This node will receive the record from the first node and continue execution by per-pixel raymarching towards the light direction looking for collisions in the depth buffer. To detect a collision I reused the hierarchical depth buffer raymarching code from the [integration of FidelityFX SSSR](https://interplayoflight.wordpress.com/2022/09/28/notes-on-screenspace-reflections-with-fidelityfx-sssr/) I’d already had in the toy renderer:

```
struct PixelRecord
{
uint2 screenPos;
float3 rayDir;
float3 rayOrigin;
};
[Shader("node")]
[NodeLaunch("broadcasting")]
[NodeDispatchGrid(1, 1, 1)]
[numthreads(8, 8, 1)]
void Shadows_Node(
DispatchNodeInputRecord<TileRecord> inputData,
uint2 groupThreadId : SV_GroupThreadID,
uint threadIndex : SV_GroupIndex,
uint2 groupId : SV_GroupID,
[MaxRecords(64)] NodeOutput<PixelRecord> ShadowsDXR_Node
)
{
// use the record data to reconstruct screen position for this thread
const uint2 screenPos = inputData.Get().tileXY * uint2(8, 8) + groupThreadId;
if (any(screenPos >= RTSize.xy))
return;
// read depth from mip 0 of the hierarchical depth buffer
float depth = FFX_SSSR_LoadDepth(screenPos.xy, 0);
// calculate world position for this pixel
float4 worldPos = .....
// calculate a ray towards the light
float3 rayDir = ....
// project ray to screen space
float3 screen_uv_space_ray_origin = float3(uv, depth);
float3 screen_space_ray_direction = ProjectDirection(worldPos.xyz, rayDir, screen_uv_space_ray_origin, projView);
bool valid_hit = false;
//raymarch until we find a hit
float3 hit = FFX_SSSR_HierarchicalRaymarch(screen_uv_space_ray_origin, screen_space_ray_direction, true, int2(RTSize.xy), 0, 1, 512, valid_hit);
// we may want to validate the hit here, check if off-screen, use thickness etc
//allocate one record for this thread if needed
ThreadNodeOutputRecords<PixelRecord> threadRecord = ShadowsDXR_Node.GetThreadNodeOutputRecords( valid_hit ? 0 : 1);
if (!valid_hit)
{
//invalid hit, we need to populate record
threadRecord.Get().screenPos = screenPos;
threadRecord.Get().rayDir = rayDir;
threadRecord.Get().rayOrigin = worldPos.xyz;
}
else
{
//this is a valid hit, write a shadow factor of zero to the shadowmask
shadowMask[screenPos.xy] = 0;
}
//mark record as done
threadRecord.OutputComplete();
}
```

A few things to unpack here, first notice the name of the node, Shadows_Node, it is the one referenced in the first graph node shader. It is again launched as broadcasting, meaning that all threads in the threadgroup will receive the same input record. This makes sense as the record only holds the tile coordinate which is the same for all threads. We also declare that we will create a maximum of 64 PixelRecord records (one for each thread in the 8×8 threadgroup) for the ShadowsDXR_Node node, which follows the current one in the graph.

The tile coordinates are used to reconstruct the screen space position for each thread, and once a ray dir (based on light dir) and world position have been determined we can start raymarching the hierarchical depth buffer until a hit is found. Not shown in the code for brevity but we would need to validate that hit to ensure it is not out of the screen, maybe use some object thickness to avoid over occlusion etc. Once we are satisfied that the hit is not valid, we need to create a record for the next node in the graph (which will do the raytracing).

A few paragraphs ago we discussed how the call to create the record for a threadgroup (GetGroupNodeOutputRecords) should be threadgroup uniform. The same holds true for the call to create a record for the thread, GetThreadNodeOutputRecords(). This means that it can’t be in an if-statement, it needs to be called for every thread even if not needed. The way to express whether it is needed or not is through the number of records we request, which is 0 for a valid hit and 1 for an invalid hit. Calling GetThreadNodeOutputRecords() in a non-threadgroup uniform way can lead to undefined behaviour like already mentioned. Same if the number of records requested for the whole threadgroup doesn’t add up to the maximum of 64 records declared. We finally call OutputComplete() as previously to mark the record as ready to use.

Almost at the end, we need a final node to raytrace the remaining pixels, those that are neither backfacing nor have a hit in the depth buffer.

```
[Shader("node")]
[NodeLaunch("thread")]
void ShadowsDXR_Node(
ThreadNodeInputRecord<PixelRecord> inputData
)
{
uint2 screenPos = inputData.Get().screenPos;
RayDesc ray;
ray.Origin = inputData.Get().rayOrigin;
ray.Direction = inputData.Get().rayDir;
ray.TMin = 0.01;
ray.TMax = 100000;
RayQuery<RAY_FLAG_CULL_NON_OPAQUE | RAY_FLAG_ACCEPT_FIRST_HIT_AND_END_SEARCH> rayQuery;
rayQuery.TraceRayInline(Scene, RAY_FLAG_NONE, 0xFF, ray);
rayQuery.Proceed();
float shadow = (rayQuery.CommittedStatus() == COMMITTED_NOTHING) ? 1.0 : 0.0;
shadowMask[screenPos.xy] = shadow ;
}
```

Again, notice the name of the node, ShadowsDXR_Node, as referenced from the previous node. Also this node is launched differently, as “thread”. This means that each thread will receive a different input record, which again makes sense as the ray direction and origin will differ per thread. No need for thread group and dispatch sizes declarations, as they don’t make sense in this context.

The node itself is simple, it retrieves the ray origin and direction from the input record and launches a ray using inline raytracing, writing a shadow factor of 0.0 or 1.0 depending on whether a hit has been found.

And that is it, with this cascade of graph nodes we filtered down pixels that actually need raytracing. The following is an example of the above workgraph in action in the Bistro scene:

![](../../assets/08f968472c928d67.png)


![](../../assets/08f968472c928d67.png)

Green areas correspond to the output of the first node, i.e. tiles that are backfacing to the light and need neither raymarching nor raytracing as they are always occluded. Blue areas correspond to the output of the second node, pixels that have found a hit in the hierarchical depth buffer and are deemed occluded. Finally, red areas correspond to the output of the third node, to pixels that actually need raytracing.

Also, here is an example of the output of the graph, backfacing, raymarched and raytraced occlusion for the directional light.

![](../../assets/59f27aa1f5096c95.png)


![](../../assets/59f27aa1f5096c95.png)

It is worth briefly discussing setting up the workgraph on the CPU side, as with DXR it uses sub objects to define the various configurations of the Pipeline State Object (PSO), and compiles libraries (lib) for the shaders. Also it needs allocating a buffer for the backing memory, used by the nodes to pass data around. A global root signature can be used to bind data to a workgraph, visible to all node shaders. Additionally, a block of memory can be allocated for each a node to be used as a fixed storage for local root arguments. Finally, workgraphs are kicked off with a call to DispatchGraph().

I won’t be discussing the CPU side of workgraph creation too much as the post is getting long already, I will suggest studying the code resources at the end of the post. I will paste the code though in case it is of use to anyone, first to create the global root signature, shader library, backing memory and PSO:

```
void FeaxRenderer::LoadShadowMaskWorkGraph()
{
// give the workgraph a name
const std::wstring workGraphName = L"ShadowMaskClassifier";
// Create global root signature for the workgraph.
{
m_ShadowMaskWorkGraphRS.Reset(3, 1);
m_ShadowMaskWorkGraphRS[0].InitAsDescriptorRange(D3D12_DESCRIPTOR_RANGE_TYPE_CBV, 0, 3, D3D12_SHADER_VISIBILITY_ALL, 0);
m_ShadowMaskWorkGraphRS[1].InitAsDescriptorRange(D3D12_DESCRIPTOR_RANGE_TYPE_SRV, 0, 4, D3D12_SHADER_VISIBILITY_ALL, 0);
m_ShadowMaskWorkGraphRS[2].InitAsDescriptorRange(D3D12_DESCRIPTOR_RANGE_TYPE_UAV, 0, 1, D3D12_SHADER_VISIBILITY_ALL);
m_ShadowMaskWorkGraphRS.InitStaticSampler(0, SamplerPointClampDesc);
m_ShadowMaskWorkGraphRS.Finalise((ID3D12Device*)m_device.Get(), L"m_ShadowMaskWorkGraphRS", D3D12_ROOT_SIGNATURE_FLAG_NONE);
}
//compile all shaders for the nodes into a library
ShaderDesc wgShaderDesc = { L"ShadowMaskWG", L"ShadowMaskWG.hlsl", L"", L"lib_6_8" };
Shader* wgShader = m_shaderManager.Create(wgShaderDesc);
//create state object for the workgraph program
CD3DX12_STATE_OBJECT_DESC stateObjectDec{ D3D12_STATE_OBJECT_TYPE_EXECUTABLE };
// Add global root signature as subobject.
auto rootSigSubObject = stateObjectDec.CreateSubobject<CD3DX12_GLOBAL_ROOT_SIGNATURE_SUBOBJECT>();
rootSigSubObject->SetRootSignature(m_ShadowMaskWorkGraphRS.GetSignature());
// Add library bytecode as subobject.
auto libSubObject = stateObjectDec.CreateSubobject<CD3DX12_DXIL_LIBRARY_SUBOBJECT>();
CD3DX12_SHADER_BYTECODE libBytecode = CD3DX12_SHADER_BYTECODE((void*)wgShader->m_shader.Get()->GetBufferPointer(), wgShader->m_shader->GetBufferSize());
libSubObject->SetDXILLibrary(&libBytecode);
// Add a workgraph subobject
auto graph = stateObjectDec.CreateSubobject<CD3DX12_WORK_GRAPH_SUBOBJECT>();
graph->SetProgramName(workGraphName.c_str());
graph->IncludeAllAvailableNodes(); // add all nodes
graph->Finalize();
// We want to override the dispatch size for the first node in the graph according to the target image isze
auto rootNodeDispatchGridSizeOverride = graph->CreateBroadcastingLaunchNodeOverrides(L"ClassifyPixels_Node");
rootNodeDispatchGridSizeOverride->DispatchGrid(GetDispatchDim(m_width, 8), GetDispatchDim(m_height, 8), 1);
ThrowIfFailed(m_device->CreateStateObject(stateObjectDec, IID_PPV_ARGS(&m_ShadowMaskWorkGraphSO)));
ComPtr<ID3D12StateObjectProperties1> stateObjectProperties ;
ComPtr<ID3D12WorkGraphProperties> workGraphProperties;
m_ShadowMaskWorkGraphSO.As(&stateObjectProperties);
m_ShadowMaskWorkGraphSO.As(&workGraphProperties);
// find the index of the workgraph program
UINT wgIndex = workGraphProperties->GetWorkGraphIndex(workGraphName.c_str());
// calculate the size of the backing memory buffer
D3D12_WORK_GRAPH_MEMORY_REQUIREMENTS memRequirements = {};
workGraphProperties->GetWorkGraphMemoryRequirements(wgIndex, &memRequirements);
Buffer* backingBuffer = nullptr;
//allocate backing memory buffer, if needed
if (memRequirements.MaxSizeInBytes > 0)
{
Buffer::Description desc = {};
desc.m_elementSize = 1;
desc.m_format = DXGI_FORMAT_R8_UINT;
desc.m_descriptorType = Buffer::DescriptorType::SRV;
desc.m_noofElements = memRequirements.MaxSizeInBytes;
desc.m_resourceFlags = D3D12_RESOURCE_FLAG_NONE;
backingBuffer = m_bufferManager.FindOrCreate(L"ShadowMaskBackingMemoryResource", desc);
}
//create the workgraph program description and attach the backing memory buffer
D3D12_SET_PROGRAM_DESC desc = {};
desc.Type = D3D12_PROGRAM_TYPE_WORK_GRAPH;
desc.WorkGraph.ProgramIdentifier = stateObjectProperties->GetProgramIdentifier(workGraphName.c_str());
desc.WorkGraph.Flags = D3D12_SET_WORK_GRAPH_FLAG_INITIALIZE;
if (backingBuffer)
{
desc.WorkGraph.BackingMemory = { backingBuffer->GetResource()->GetGPUVirtualAddress(), memRequirements.MaxSizeInBytes };
}
m_shadowMaskWorkGraphDesc = desc;
}
```

Worth calling out how we can access the properties of a specific node to override the dispatch size, to make it match the threadgroup size and target image resolution.

```
auto rootNodeDispatchGridSizeOverride = graph->CreateBroadcastingLaunchNodeOverrides(L"ClassifyPixels_Node");
rootNodeDispatchGridSizeOverride->DispatchGrid(GetDispatchDim(m_width, 8), GetDispatchDim(m_height, 8), 1);
```

Also, here is the method that executes the workgraph, for reference:

```
void FeaxRenderer::DispatchShadowMaskWorkGraph()
{
ProfileBlock gpuProfileBlock(m_commandList.Get(), "Shadomask WG");
Rendertarget* normalsRT = m_rendertargetManager.Find(L"NormalsRT");
Rendertarget* hierarchicalDepth = m_rendertargetManager.Find(L"HiZ");
GPUDescriptorHeap* gpuDescriptorHeap = m_context->GetGPUDescriptorHeap();
// bind the global root signature
m_commandList->SetComputeRootSignature(m_ShadowMaskWorkGraphRS.GetSignature());
// set up resources
DescriptorHandle cbvHandle = gpuDescriptorHeap->GetHandleBlock(3);
gpuDescriptorHeap->AddToHandle(cbvHandle, m_lightingCB->GetCBV());
gpuDescriptorHeap->AddToHandle(cbvHandle, m_lightsCB->GetCBV());
gpuDescriptorHeap->AddToHandle(cbvHandle, m_shadowsCB->GetCBV());
DescriptorHandle srvHandle = gpuDescriptorHeap->GetHandleBlock(4);
gpuDescriptorHeap->AddToHandle(srvHandle, hierarchicalDepth->GetSRV());
gpuDescriptorHeap->AddToHandle(srvHandle, normalsRT->GetSRV());
gpuDescriptorHeap->AddToHandle(srvHandle, m_blueNoiseTexture[m_frameCount % 64]->GetSRV());
gpuDescriptorHeap->AddToHandle(srvHandle, m_dxrTopLevelAccelerationStructure->GetSRV());
DescriptorHandle uavHandle = gpuDescriptorHeap->GetHandleBlock(1);
gpuDescriptorHeap->AddToHandle(uavHandle, m_shadowMaskRT->GetUAV());
m_commandList->SetComputeRootDescriptorTable(0, cbvHandle.GetGPUHandle());
m_commandList->SetComputeRootDescriptorTable(1, srvHandle.GetGPUHandle());
m_commandList->SetComputeRootDescriptorTable(2, uavHandle.GetGPUHandle());
// we need to initialise the backing memory only the first time we run the workgraph
m_shadowMaskWorkGraphDesc.WorkGraph.Flags = m_InitWorkGraphBackingMemory ? D3D12_SET_WORK_GRAPH_FLAG_INITIALIZE : D3D12_SET_WORK_GRAPH_FLAG_NONE;
// bing the workgraph program with the reference to the backing memory
m_commandList->SetProgram(&m_shadowMaskWorkGraphDesc);
// dispatch work graph
D3D12_DISPATCH_GRAPH_DESC desc = {};
desc .Mode = D3D12_DISPATCH_MODE_NODE_CPU_INPUT;
desc .NodeCPUInput = { };
desc .NodeCPUInput.EntrypointIndex = 0;
desc .NodeCPUInput.NumRecords = 1;
m_commandList->DispatchGraph(&desc);
m_InitWorkGraphBackingMemory = false;
}
```

This whole example was in effect a tile/pixel classification implementation, where, based on some criteria (back facing, hit in depth buffer), we can get the GPU to decide how much work it needs to perform, usually leading to a performance improvement. A similar scheme can be used for deferred shading as well, to simplify the shaders needed to light each tile based on the material properties in the gbuffer. Such techniques where the GPU decides the amount of work it needs to do (GPU driven rendering) are possible without workgraphs, by getting the GPU to fill argument buffers to use with ExecuteIndirect. There are some issues with that approach though:

- It is not easy to predetermine how much work the GPU will create for itself, so usually conservative buffer allocation is needed which could lead to memory waste.
- Extra work is needed to batch and compact the indirect dispatch arguments buffer to avoid “empty” dispatches (where no work was produced)
- The GPU passes to produce and consume work usually need barriers to ensure that one pass has finished outputting before execution begin. This leads to drains in the pipeline.

We can showcase the last issue using FidelityFX’s SSSR which performs a similar classification step to produce work and Execute Indirect to process the tiles. There is a barrier and a pipeline drain in order to ensure that the classification step is finished before execution begins.

![](../../assets/0b58c4da7f40f4ea.png)


![](../../assets/0b58c4da7f40f4ea.png)

Workgraphs can address such issues by localising production and consumption of work on the GPU without intermediate storage and global barriers as well as CPU intervention to kick off the work, which simplifies GPU driven rendering significantly, and should lead to less memory requirements and better GPU utilisation.

As with any GPU driven rendering approach, good debugging tools will be critical to the success of the feature, with validation of node definition and output and visualisation of the data flow between nodes, especially as workgraphs become larger and involve different types of shaders. There already is some support for workgraphs in PIX, and NVidia’s GPU Trace can provide performance data.

## Further reading

Some resources for those who want to study workgraphs further, some of the resources also link to repositories with various workgraph sample worth studying as well.

[https://developer.nvidia.com/blog/work-graphs-in-direct3d-12-a-case-study-of-deferred-shading/](https://developer.nvidia.com/blog/work-graphs-in-direct3d-12-a-case-study-of-deferred-shading/)[https://gpuopen.com/learn/gpu-work-graphs/gpu-work-graphs-intro/](https://gpuopen.com/learn/gpu-work-graphs/gpu-work-graphs-intro/)[https://gpuopen.com/learn/rgp-work-graphs/](https://gpuopen.com/learn/rgp-work-graphs/)[https://developer.nvidia.com/blog/advancing-gpu-driven-rendering-with-work-graphs-in-direct3d-12/](https://developer.nvidia.com/blog/advancing-gpu-driven-rendering-with-work-graphs-in-direct3d-12/)[https://github.com/microsoft/DirectX-Specs/blob/master/d3d/WorkGraphs.md](https://github.com/microsoft/DirectX-Specs/blob/master/d3d/WorkGraphs.md)