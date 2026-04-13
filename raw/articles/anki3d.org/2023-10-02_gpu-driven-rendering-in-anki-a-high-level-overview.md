---
title: 'GPU driven rendering in AnKi: A high level overview'
url: https://anki3d.org/gpu-driven-rendering-in-anki-a-high-level-overview/
author: Panagiotis Christopoulos Charitos
published: '2023-10-02'
source_blog: AnKi 3D Engine Dev Blog
source_site: https://anki3d.org
category: graphics
fetched: '2026-04-13'
---

For the last few months AnKi underwent a heavy re-write in order to enable GPU driven rendering. This post will quickly go through the changes and the design without diving too deep into details. There will be another post (or maybe video) with all the implementation details.

What is GPU driven rendering (**GDR** from now on)? It’s the process of moving logic that traditionally runs into the CPU, to the GPU. The first category of GDR work includes various simulation workloads. Things like particle simulations, clutter placement, snow/water deformations, cloth simulation and more. The next GDR category includes techniques that do GPU based occlusion culling. That includes per object occlusion and more fine-grained meshlet (aka cluster) occlusion. The last category is generating command buffers from the GPU directly. In DX12 this is done using Extended Indirect and in Vulkan with NV_device_generated_commands. A very recent addition to this category is Workgraphs from AMD but that’s a bit experimental at the moment. Due to Vulkan limitations AnKi doesn’t use device generated commands so the ceiling of AnKi’s implementation is multi-draw indirect with indirect count (aka VK_KHR_draw_indirect_count, aka **MDI**).

So what kind of GDR variant AnKi uses? The final goal was to perform all per-object visibility on the GPU. Visibility for regular meshes as well as lights, probes, decals and the rest of the meta-objects. The whole work was split into 2 logical parts. The 1st part re-organizes data in a more GDR friendly way and the 2nd is the GPU visibility and command buffer generation itself.

## GDR Data / GPU Scene

With GDR the way we store data needs to be re-thinked. So for AnKi there are 3 main components. The 1st is the Unified Geometry Buffer (**UGB**) which is a huge buffer that holds all index and vertex buffers of the whole game. The 2nd is the **GPU scene** buffer that stores a GPU view of the scenegraph. Things like object transforms, lights, probes, uniforms (aka constants) and more. The 3rd bit is a descriptor set with all the textures, in other words **bindless textures**. Every renderable object has a structure (a data record) in the GPU scene that points to transforms, uniforms, bindles texture indices etc.

The intent with these 3 data holders is to have persistent data in the GPU and be able to address index and vertex buffers using indirect arguments. No more CPU to GPU roundtrips. At the beginning of the frame there is what we call **micro-patching** of the GPU scene. For example, if an object was moved there will be a small copy from the CPU to the GPU scene.

## GPU occlusion

The next bit to discuss is how GPU occlusion works at a very high level. Here things are somewhat vanilla. Nothing that hasn’t been tried before. There is a Hierarchical Z Buffer (**HZB**) generated in frame N and used in frame N+1. This HZB is used for the occlusion of GBuffer pass and the Transparents rendering but also used to cull lights, decals and probes. The 1 frame delay is fine since the occlusion is per object but if it was per meshlet this delay might have been problematic.

Occlusion is also done for the shadow cascades using a variation of Assasin Creed’s Unity technique. Meaning, get the max (in our case) depth of each 64×64 tile of the depth buffer, then render boxes for each tile into light space and use that to construct the HZB. Do that for each cascade.

One additional problem had to do with the other shadow casting lights (and the probes). The CPU is not aware of the visible punctual lights but it needs to know them in order to build the commands required for shadows. What AnKi does in this case is to send some info of the visible lights from the GPU to the CPU. With a few frames delay the CPU will schedule the shadow passes. This mechanism is also used for probes that need to be updated real-time.

## Command Buffer Building

As we mentioned at the beginning AnKi is using multi-draw indirect. The CPU organizes all renderable objects present in the scene into graphics state buckets. The state is actually derived by the graphics pipeline. Then the renderer will build a single MDI call for each state bucket. When doing visibility testing the GPU will place the indirect arguments of the visible renderables into the correct bucket.

The GPU visibility will populate the indirect arguments but also an additional buffer per visible instance. This buffer is a vertex buffer with per-instance rate and this is a well known trick to workaround the lack of base instance support in DX. This vertex buffer holds some offsets required by the renderable. For example one of these offsets points to the transform and another to the uniforms.

There are a few complexities in this scheme that have to do with counting drawcalls for gathering statistics. For that reason there is a small drawcall at the beginning of the renderpass that iterates the buckets and gathers the draw counts. The CPU will read that count at some point later.

## Future

Next stop is extending the occlusion to meshlets. Let’s see how that goes.