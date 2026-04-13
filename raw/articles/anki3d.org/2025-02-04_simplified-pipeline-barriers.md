---
title: Simplified pipeline barriers
url: https://anki3d.org/simplified-pipeline-barriers/
author: Panagiotis Christopoulos Charitos
published: '2025-02-04'
source_blog: AnKi 3D Engine Dev Blog
source_site: https://anki3d.org
category: graphics
fetched: '2026-04-13'
---

One of the challenges of low level APIs such as Vulkan and D3D12 is synchronization of GPU work. The most used primitive in GPU synchronization is pipeline barriers and if someone takes a look at **vkCmdPipelineBarrier** or **ID3D12GraphicsCommandList::ResourceBarrier/Barrier** it’s easy to understand why many people struggle. In this article we will decompose the barriers and put them back together in a more simplified form. We will use Vulkan as the base of our discussion but everything is transferable to D3D12’s **Extended Barriers** ([link](https://microsoft.github.io/DirectX-Specs/d3d/D3D12EnhancedBarriers.html)). D3D12’s Extended Barriers is extremely close to Vulkan’s barrier model so most concepts discussed here are transferable to D3D12 as well. D3D12’s old barrier model (ID3D12GraphicsCommandList::ResourceBarrier) is out of scope since I’m not a big fan of it. Unfortunately this article requires a deep understanding of synchronization so be prepared.

What is a pipeline barrier? More or less it’s an abstraction that defines 3 things:

- Which
**GPU pipelines**to block before we do work on another set of pipelines (via VkPipelineStageFlagBits). These bitmask describes relationships such as: wait for fragment shading before you start the next compute shading. - Which GPU
**caches**to invalidate (via VkAccessFlags). - For some GPU HW images can exist in multiple states. They can be compressed or decompressed for example. So if images are involved, a barrier can define a transition from one
**image state**to another (via VkImageLayout)

And here is a small table with VK to D3D12 mapping:

| Vulkan | D3D12’s Extended Barriers |
|---|---|
| vkCmdPipelineBarrier | ID3D12GraphicsCommandList7::Barrier |
| VkPipelineStageFlagBits | D3D12_BARRIER_SYNC |
| VkAccessFlags | D3D12_BARRIER_ACCESS |
| VkImageLayout | D3D12_BARRIER_LAYOUT |

And the question really is. Do we need 25+ pipeline stages or 30+ access flags to describe a barrier? If we want to maybe future proof our code or we want to be super pedantic about the whole thing then the answer is yes. In practice though we will be wasting our time. If we look deep and gather all the public knowledge out there it’s not that difficult to consolidate and simplify the existing API. In other words, cut some corners. So everything I’ll mention is based on public articles, looking at open source drivers and some things obtained from experimentation.

Let’s start by looking at the **VkPipelineStageFlagBits**. For PC/console HW there are really 2 stages, graphics and compute. There are also DMA (aka transfer-only) queues but those are somewhat orthogonal since they require different sync primitives to be synchronized with the general queue. So let’s forget DMA queues for now. The compute stage though is a bit special and it can be used by multiple types of commands. Dispatches (vkCmdDispatch) are obviously compute, transfers (eg vkCmdCopyBuffer) are often compute, building acceleration structures is compute and dispatching rays (vkCmdTraceRays/DispatchRays) is implemented as compute as well. Most HW runs all those commands as compute but some HW may have the ability to synchronize them separately (use different scoreboards or something). In other words, if you have a vkCmdBuildAccelerationStructures followed by a COMPUTE->COMPUTE barrier followed by a vkCmdDispatch then there is a possibility that some HW will be able to run the dispatch and the AS build concurrently.

For mobile HW things are a little bit more fine grained. Arm HW has 4 stages which are: transfer, compute, geometry and fragment. Recent Adrenos can run binning concurrently with other fragment work (which means geometry and fragment are different stages) but not sure about the rest of the stages. Turnip driver (Mesa’s Adreno VK driver) is probably a bit conservative and bundles many stages into one super stage so I can’t be sure.

Putting everything into a blender VkPipelineStageFlagBits can be simplified into 6 stages:

- Transfers (aka copies)
- Compute
- Geometry. Which includes the stages from VK_PIPELINE_STAGE_VERTEX_INPUT_BIT to VK_PIPELINE_STAGE_GEOMETRY_SHADER_BIT and includes VK_PIPELINE_STAGE_TASK_SHADER_BIT_EXT and VK_PIPELINE_STAGE_MESH_SHADER_BIT_EXT
- Fragment
- TraceRays
- Build acceleration structures

Now let’s look at the **VkAccessFlags**. It not easy to map the access flags to caches and even if it was, it wouldn’t have been very future proof. So we’ll try a different approach here. We’ll bundle the access flags into groups that make logical sense. Different groups for buffers, images and acceleration structures. One interesting thing to mention though is that I had numerous cases where I forgot to include **indirect** **command** access flag (VK_ACCESS_INDIRECT_COMMAND_READ_BIT) and nVidia was hanging intermittently. So indirect might be a separate stage or a special cache for nVidia. Let’s keep that in mind. Another interesting thing to note is that access flags in some cases mirror the **VkBufferUsageFlagBits and VkImageUsageFlagBits** so maybe we could try to combine access and usage flags into one thing and kill two birds with one stone.

Let’s start with **buffers** first where things are more simple. We just need a sensible grouping for the VkBufferUsageFlagBits that will help us with memory allocations and also handle the VkAccessFlags. One example when it comes to memory allocation hints is that if the buffer will only be used as uniform buffer then we might want to allocate it from ReBAR VRAM instead of plain VRAM.

Putting everything into a blender we can come up with a few access flags/usage flags for buffers:

- Undefined state
- Uniform buffer because for some HW this is special (nVidia) and because we may want to allocate UBOs from ReBAR
- Read-only shader resource. This is also known as SRV in D3D. In HLSL this is StructuredBuffer, ByteAddressBuffer and Buffer.
- Read-write shader resource. This is also known as UAV in D3D. In HLSL this is RWStructuredBuffer, RWByteAddressBuffer, RWBuffer and a few other things that should die in a fire (append buffers).
- Index and vertex buffers
- Indirect arguments buffer. For nVidia as I mentioned above
- Transfer (aka copies)
- Acceleration structure build input. This includes 2 things
- The index or position buffers that are used to build the acceleration structures
- And the scratch buffer of the AS builds

- Shader Binding Table used vkCmdTraceRays

Now that we have the simplified stages and some sensible grouping for the buffer access/usage flags we can come up with a new set of buffer states that will help us derive (1) Vulkan’s barrier stages, (2) the barrier access masks and (3) the buffer usage flags:

```
enum class BufferUsageBit : U64
{
kNone = 0,
kConstantGeometry = 1ull << 0ull,
kConstantPixel = 1ull << 1ull,
kConstantCompute = 1ull << 2ull,
kConstantTraceRays = 1ull << 3ull,
kSrvGeometry = 1ull << 4ull,
kSrvPixel = 1ull << 5ull,
kSrvCompute = 1ull << 6ull,
kSrvTraceRays = 1ull << 7ull,
kUavGeometry = 1ull << 8ull,
kUavPixel = 1ull << 9ull,
kUavCompute = 1ull << 10ull,
kUavTraceRays = 1ull << 11ull,
kVertexOrIndex = 1ull << 12ull,
kIndirectCompute = 1ull << 14ll,
kIndirectDraw = 1ull << 15ull,
kIndirectTraceRays = 1ull << 16ull,
kCopySource = 1ull << 17ull,
kCopyDestination = 1ull << 18ull,
kAccelerationStructureBuild = 1ull << 19ull, ///< Will be used as a position or index buffer in a BLAS build.
kShaderBindingTable = 1ull << 20ull, ///< Will be used as SBT in a traceRays() command.
kAccelerationStructureBuildScratch = 1ull << 21ull, ///< Used in buildAccelerationStructureXXX commands.
// Derived
kAllConstant = kConstantGeometry | kConstantPixel | kConstantCompute | kConstantTraceRays,
kAllSrv = kSrvGeometry | kSrvPixel | kSrvCompute | kSrvTraceRays,
kAllUav = kUavGeometry | kUavPixel | kUavCompute | kUavTraceRays,
kAllIndirect = kIndirectCompute | kIndirectDraw | kIndirectTraceRays,
kAllCopy = kCopySource | kCopyDestination,
kAllGeometry = kConstantGeometry | kSrvGeometry | kUavGeometry | kVertexOrIndex,
kAllPixel = kConstantPixel | kSrvPixel | kUavPixel,
kAllGraphics = kAllGeometry | kAllPixel | kIndirectDraw,
kAllCompute = kConstantCompute | kSrvCompute | kUavCompute | kIndirectCompute,
kAllTraceRays = kConstantTraceRays | kSrvTraceRays | kUavTraceRays | kIndirectTraceRays | kShaderBindingTable,
kAllRayTracing = kAllTraceRays | kAccelerationStructureBuild | kAccelerationStructureBuildScratch,
kAllRead = kAllConstant | kAllSrv | kAllUav | kVertexOrIndex | kAllIndirect | kCopySource | kAccelerationStructureBuild | kShaderBindingTable,
kAllWrite = kAllUav | kCopyDestination | kAccelerationStructureBuildScratch,
kAllShaderResource = kAllConstant | kAllSrv | kAllUav,
kAll = kAllRead | kAllWrite,
};
```

As you can see these flags are a combination of pipeline stage, access, and buffer usage. So setting a barrier is just a matter of filling this structure:

```
class BufferBarrierInfo
{
public:
BufferView m_bufferView;
BufferUsageBit m_previousUsage = BufferUsageBit::kNone;
BufferUsageBit m_nextUsage = BufferUsageBit::kNone;
};
```

Similar story for images. Images have the following types of accesses:

- Undefined. This is useful when we want to transition to some image state but don’t care about its previous state.
- Read-only shader resource. This is your typical sampled image. Also known as SRV in D3D.
- Read-write shader resource. This is storage image in VK and as UAV in D3D.
- Render target. Color or depth/stencil RTs. This is RTV or DSV in D3D.
- Shading rate image. The tiled image that is used in Variable Rate Shading (VRS). If you don’t care about VRS then forget that one.
- Destination or source of a transfer operation (Note: AnKi doesn’t have copies that use images as source so you won’t see that in TextureUsageBit).
- Present.

Now we combine everything to this:

```
enum class TextureUsageBit : U32
{
kNone = 0,
kSrvGeometry = 1 << 0,
kSrvPixel = 1 << 1,
kSrvCompute = 1 << 2,
kSrvTraceRays = 1 << 3,
kUavGeometry = 1 << 4,
kUavPixel = 1 << 5,
kUavCompute = 1 << 6,
kUavTraceRays = 1 << 7,
kRtvDsvRead = 1 << 8,
kRtvDsvWrite = 1 << 9,
kShadingRate = 1 << 10,
kCopyDestination = 1 << 11,
kPresent = 1 << 12,
// Derived
kAllSrv = kSrvGeometry | kSrvPixel | kSrvCompute | kSrvTraceRays,
kAllUav = kUavGeometry | kUavPixel | kUavCompute | kUavTraceRays,
kAllRtvDsv = kRtvDsvRead | kRtvDsvWrite,
kAllGeometry = kSrvGeometry | kUavGeometry,
kAllPixel = kSrvPixel | kUavPixel,
kAllGraphics = kAllGeometry | kAllPixel | kRtvDsvRead | kRtvDsvWrite | kShadingRate,
kAllCompute = kSrvCompute | kUavCompute,
kAllCopy = kCopyDestination,
kAllRead = kAllSrv | kAllUav | kRtvDsvRead | kShadingRate | kPresent,
kAllWrite = kAllUav | kRtvDsvWrite | kCopyDestination,
kAll = kAllRead | kAllWrite,
kAllShaderResource = kAllSrv | kAllUav,
};
```

Now let’s discuss some strategies when using BufferUsageBit and TextureUsageBit to derive the Vulkan barriers.

The first thing to note is that as far as I know no HW/driver cares about being precise with buffer barriers. By being precise I mean using VkBufferMemoryBarrier with proper offset and range. What is interesting in buffer barriers (apart from the pipeline stages of cource) is the access flags. In AnKi we chose to translate all BufferBarrierInfo will to a single generic barrier (VkMemoryBarrier). This will work fine for most HW but for Mali it may result into some unnecessary texture cache flushes. Under certain circumstances VkMemoryBarrier may imply texture accesses even if we only care about buffers in this case. But this is a compromise that I was willing to make.

Next stop is **image layouts**. The TextureUsageBit is enough to infer the image layouts and we can be precise with them if we want to. Image layouts were an AMD thing coming from the GCN era but things got better from RDNA2 and on. nVidia doesn’t care about layouts but Mali recent HW has some interactions with them. Not sure about other HW. UNDEFINED and PRESENT layouts are always special for some HW so we need to keep them around. In AnKi we keep computing the optimal layouts for all textures except blocked compressed textures. BC/ASTC/ETC textures only have UNDEFINED and GENERAL layouts and nothing more so for those we don’t bother too much. Block compressed textures don’t have multiple image states that’s why we excluded them.

Image barriers (VkImageMemoryBarrier) also contain information used to **transfer ownership from one queue family to another**. If an image is created with VK_SHARING_MODE_EXCLUSIVE and the image will be used by multiple queue families then we need to set the srcQueueFamilyIndex and dstQueueFamilyIndex in our image barrier. Of course this is only relevant if we are using more than one queue families. Primary use-case is async compute. So in that case we have 2 choices. Either we make all images VK_SHARING_MODE_CONCURRENT and we don’t bother with ownership transfers or we make them VK_SHARING_MODE_EXCLUSIVE and we do bother. By looking at RADV (Mesa’s opensource AMD driver), AMD seems to still care about queue ownership transfers (not sure to what extend though) but if we look at VKD3D (layer translating D3D12 to VK, part of Valve’s proton) and D3D12 we see that queue family transfers are not a thing. Also, other HW besides AMD doesn’t seem to care about ownership transfers. So in this case maybe it’s fine to use VK_SHARING_MODE_CONCURRENT for all images if using async compute and forget all this queue family ownership transfer complexity.

One thing that we completely neglected to mention is the interactions between **host **(aka CPU) and the device (GPU). VkAccessFlags contain host bits as well after-all. Adding a VK_ACCESS_HOST_XXX_BIT in the srcAccessMask is a bit superfluous for 99% of cases though. Writes from the host will be made available to the device when submitting to a queue. Similar story for D3D12 where each submit implies a barrier and an all-cache flush. So every submission starts with clean caches and there is no need for us to do that manually. VK_ACCESS_HOST_XXX_BIT in the dstAccessMask is a different story though. VK_ACCESS_HOST_XXX_BIT in dstAccessMask is technically required if we want to make memory touched by the device visible to the host. In other words, we, the programmer, need to flush the device caches in order to make the memory available to the host. If we neglect to do so none can guarantee that the host will be able to see what the device wrote. In practice this step is also superfluous since most drivers also flush caches when a submission ends. Mali drivers had a few VK conformance test failures back in the day because they decided to play by the book and invalidate only when the user asked them to. Other vendors didn’t have any failures so it seems none plays by the book. Also, D3D12’s D3D12_BARRIER_ACCESS doesn’t have host bits which is a good decision IMHO. Just kill host access flags.

Another omission is video (VK_KHR_video_XXX) which I haven’t taken into account and I have no idea how it interacts with everything else.

And there you have it. We managed to remove the complexity of vkCmdPipelineBarrier/Barrier and simplify our API abstraction… with some minor performance concessions though. If you want to look into some actual code take a peek at CommandBuffer::setPipelineBarrier in the [VK backend](https://github.com/godlikepanos/anki-3d-engine/blob/master/AnKi/Gr/Vulkan/VkCommandBuffer.cpp) and in the [D3D12 backend](https://github.com/godlikepanos/anki-3d-engine/blob/master/AnKi/Gr/D3D/D3DCommandBuffer.cpp) of AnKi. If you have comments or I got something wrong please write a comment and I’ll update the article.