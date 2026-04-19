---
title: 'Stingray Renderer Walkthrough #3: Render Contexts'
url: https://bitsquid.blogspot.com/2017/02/stingray-renderer-walkthrough-3-render.html
author: Tobias
published: '2017-02-10'
source_blog: 'bitsquid: development blog'
source_site: https://bitsquid.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

In the last post we covered how to create and destroy various GPU resources. In this post we will go through the system we have for recording a stream of rendering commands/packages that later gets consumed by the render backend (`RenderDevice`

) where they are translated into actual graphics API calls. We call this interface `RenderContext`

and similar to `RenderResourceContext`

we can have multiple `RenderContexts`

in flight at the same time to achieve data parallelism.

Let’s back up and reiterate a bit what was said in the [Overview](http://bitsquid.blogspot.com/2017/02/stingray-renderer-walkthrough-1-overview.html) post. Typically in a frame we take the result of the view frustum culling, split it up into a number of chunks, allocate one `RenderContext`

per chunk and then kick one worker thread per chunk. Each worker thread then sequentially iterates over its range of renderable objects and calls their `render()`

function. The `render()`

function takes the chunk’s `RenderContext`

as one of its argument and is responsible for populating it with commands. When all worker threads are done the resulting `RenderContexts`

gets “dispatched” to the `RenderDevice`

.

So essentially the `RenderContext`

is the output data structure for the second stage `Render`

as discussed in the [Overview](http://bitsquid.blogspot.com/2017/02/stingray-renderer-walkthrough-1-overview.html) post.

The `RenderContext`

is very similar to the `RenderResourceContext`

in the sense that it’s a fairly simple helper class for populating a command buffer. There is one significant difference though; the `RenderContext`

also has a mechanics for reasoning about the ordering of the commands in the buffer before they get translated into graphics API calls by the `RenderDevice`

.

We need a way to reorder commands in one or many `RenderContexts`

to make sure triangles end up on the screen in the right order, or more generally speaking; to schedule our GPU work.

There are many ways of dealing with this but my favorite approach is to just associate one or many commands with a 64 bit sort key and when all commands have been recorded simply sort them on this key before translating them into actual graphics API calls. The approach we are using in Stingray is heavily inspired by Christer Ericsson’s blog post [“Order your graphics draw calls around!”](http://realtimecollisiondetection.net/blog/?p=86). I will be covering our sorting system in more details in my next post, for now the only thing important to grasp is that while the `RenderContext`

records commands it does so by populating two buffers. One is a simple array of a POD struct called `Command`

:

```
struct Command
{
uint64_t sort_key;
void *head;
uint32_t command_flags;
};
```


`sort_key`

- 64 bit sort key used for reordering commands before being consumed by the`RenderDevice`

, more on this later.`head`

- Pointer to the actual data for this command.`command_flags`

- A bit flag encoding some hinting about what kind of command`head`

is actually pointing to. This is simply an optimization to reduce pointer chasing in the`RenderDevice`

, it will be covered in more detail in a later post.

The other buffer is what we call a `RenderPackageStream`

and is what holds the actual command data. The `RenderPackageStream`

class is essentially just a few helper functions to put arbitrary length commands into memory. The memory backing system for `RenderPackageStreams`

is somewhat more complex than a simple array though, this is because we need a way to keep its memory footprint under control. For efficiency, we want to recycle the memory instead of reallocating it every frame, but depending on workload we are likely to get some `RenderContexts`

becoming much larger than others. This creates a problem when using simple arrays to store the commands as the workload will shift slightly over time causing all arrays having to grow to fit the worst case scenario, resulting in lots of wasted memory.

To combat this we allocate and return fixed size blocks of memory from a pool. As we know the size of each command before writing them to the buffer we can make sure that a command doesn’t end up spanning multiple blocks; if we detect that we are about to run out of memory in the active block we simply allocate a new block and move on. If we detect that a single command will span multiple blocks we make sure to allocate them sequentially in memory. We return a block to the pool when we are certain that the consumer of the data (in this case the `RenderDevice`

) is done with it. (This memory allocation approach is well described in Christian Gyrling’s excellent GDC 2015 presentation [Parallelizing the Naughty Dog Engine Using Fibers](http://www.gdcvault.com/play/1022186/Parallelizing-the-Naughty-Dog-Engine))

You might be wondering why we put the `sort_key`

in a separate array instead of putting it directly into the header data of the packages written to the `RenderPackageStream`

, there are a number of reasons for that:

-
The actual package data can become fairly large even for regular draw calls. Since we want to make the packages self contained we have to put all data needed to translate the command into an graphics API call inside the package. This includes handles to all resources, constant buffer reflections and similar. I don’t know of any way to efficiently sort an array with elements of varying sizes.

-
Since we allocate the memory in blocks, as described above, we would need to introduce some form of “jump label” and insert that into the buffer to know how and when to jump into the next memory block. This would further complicate the sorting and traversal of the buffers.

-
It allows us to recycle the actual package data from one draw call to another when rendering multi-pass shaders as we simply can inject multiple

`Command`

s pointing to the same package data. (Which shader pass to use when translating the package into graphic API calls can later be extracted from the`sort_key`

.) -
We can reduce pointer chasing by encoding hints in the

`Command`

about the contents of the package data. This is what we do in`command_flags`

mentioned earlier.

With the low-level concepts of the `RenderContext`

covered let’s move on and look at how it is used from a users perspective.

If we break down the API there are essentially three different types of commands that populates a `RenderContext`

:

**State commands**- Commands affecting the state of the rendering pipeline (e.g render target bindings, viewports, scissoring, etc) + some miscellaneous commands.**Rendering commands**- Commands used to trigger draw calls and compute work on the GPU.**Resource update commands**- Commands for updating GPU resources.

“State commands” are a series of commands getting executed in sequence for a specific `sort_key`

. The interface for starting/stopping the recording looks like this:

```
class RenderContext
{
void begin_state_command(uint64_t sort_key, uint32_t gpu_affinity_mask = GPU_DEFAULT);
void end_state_command();
};
```


`sort_key`

- the 64 bit sort key.`gpu_affinity_mask`

- I will cover this towards the end of this post but, for now just think of it as a bit mask for addressing one or many GPUs.

Here’s a small example showing what the recording of a few state commands might look like:

```
rc.begin_state_command(sort_key);
for (uint32_t i=0; i!=MAX_RENDER_TARGETS; ++i)
rc.set_render_target(i, nullptr);
rc.set_depth_stencil_target(depth_shadow_map);
rc.clear(RenderContext::CLEAR_DEPTH);
rc.set_viewports(1, &viewport);
rc.set_scissor_rects(1, &scissor_rect);
rc.end_state_command();
```


While state commands primarily are used for doing bigger graphics pipeline state changes (like e.g. changing render targets) they are also used for some miscellaneous things like clearing of bound render targets, pushing/poping timer markers, and some other stuff. There is no obvious reasoning for grouping these things together under the name “state commands”, it’s just something that has happened over time. Keep that in mind as we go through the list of commands below.

-
`set_render_target(uint32_t slot, RenderTarget *target, const SurfaceInfo& surface_info);`

`slot`

- Which index of the “Multiple Render Target” (MRT) chain to bind`target`

- What`RenderTarget`

to bind`surface_info`

-`SurfaceInfo`

is a struct describing which surface of the`RenderTarget`

to bind.

`struct SurfaceInfo { uint32_t array_index; // 0 in all cases except if binding a texture array uint32_t slice; // 0 for 2D textures, 0-5 for cube maps, 0-n for volume textures uint32_t mip_level; // 0-n depending on wanted mip level };`

-
`set_depth_stencil_target(RenderTarget *target, const SurfaceInfo& surface_info);`

- Same as above but for depth stencil. -
`clear(RenderContext::ClearFlags flags);`

- Clears currently bound render targets.`flags`

- enum bit flag describing what parts of the bound render targets to clear.

`enum ClearFlags { CLEAR_SURFACE = 0x1, CLEAR_DEPTH = 0x2, CLEAR_STENCIL = 0x4 };`

-
`set_viewports(uint32_t n_viewports, const Viewport *viewports);`

`n_viewports`

- Number of viewports to bind.`viewports`

- Pointer to first`Viewport`

to bind.`Viewport`

is a struct describing the dimensions of the viewport:

`struct Viewport { float x, y, width, height; float min_depth, max_depth; };`

Note that

`x`

,`y`

,`width`

and`height`

are in unsigned normalized [0-1] coordinates to decouple render target resolution from the viewport. -
`set_scissor_rects(uint32_t n_scissor_rects, const ScissorRect *scissor_rects);`

`n_scissor_rects`

- Number of scissor rectangles to bind`scissor_rects`

- Pointer to the first`ScissorRect`

to bind.

`struct ScissorRect { float x, y, width, height; };`

Note that

`x`

,`y`

,`width`

and`height`

are in unsigned normalized [0-1] coordinates to decouple render target resolution from the scissor rectangle.

`set_stream_out_target(uint32_t slot, RenderResource *resource, uint32_t offset);`

`slot`

- Which index of the stream out buffers to bind`resource`

- Which`RenderResource`

to bind to that slot (has to point to a`VertexStream`

)`offset`

- A byte offset describing where to begin writing in the buffer pointed to by`resource`

.

`set_instance_multiplier(uint32_t multiplier);`


Allows the user to scale the number instances to render for each`render()`

call (described below). This is a convenience function to make it easier to implement things like Instanced Stereo Rendering.

`push_marker(const char *name)`


Starts a new marker scope named`name`

. Marker scopes are both used for gathering`RenderDevice`

statistics (number of draw calls, state switches and similar) as well as for creating GPU timing events. The user is free to nestle markers if they want to better group statistics. More on this in a later post.`pop_marker(const char *name)`


Stops an existing marker scope named`name`

.

With most state commands covered let’s move on and look at how to record commands for triggering draw calls and compute work to a `RenderContext`

.

For that we have a single function called `render()`

:

```
class RenderContext
{
RenderJobPackage *render(const RenderJobPackage* job,
const ShaderTemplate::Context& shader_context, uint64_t interleave_sort_key = 0,
uint64_t shader_pass_branch_key = 0, float job_sort_depth = 0.f,
uint32_t gpu_affinity_mask = GPU_DEFAULT);
};
```


`job`


First argument piped to `render()`

is a pointer to a `RenderJobPackage`

, and as you can see the function also returns a pointer to a `RenderJobPackage`

. What is going on here is that the `RenderJobPackage`

piped as argument to `render()`

gets copied to the `RenderPackageStream`

, the copy gets patched up a bit and then a pointer to the modified copy is returned to allow the caller to do further tweaks to it. Ok, this probably needs some further explanation…

The `RenderJobPackage`

is basically a header followed by an arbitrary length of data that together contains everything needed to make it possible for the `RenderDevice`

to later translate it into either a draw call or a compute shader dispatch. In practice this means that after the `RenderJobPackage`

header we also pack `RenderResource::render_resource_handle`

for all resources to bind to all different shader stages as well as full representations of all non-global shader constant buffers.

Since we are building multiple `RenderContexts`

in parallel and might be visiting the same renderable object (mesh, particle system, etc) simultaneously from multiple worker threads, we cannot mutate any state of the renderable when calling its `render()`

function.

Typically all renderable objects have static prototypes of all `RenderJobPackages`

they need to be drawn correctly (e.g. a mesh with three materials might have three `RenderJobPackages`

- one per material). Naturally though, the renderable objects don’t know anything about in which context they will be drawn (e.g. from what camera or in what kind of lighting environment) up until the point where their `render()`

function gets called and the information is provided. At that point their static `RenderJobPackages`

prototypes somehow needs to be patched up with this information (which typically is in the form of shader constants and/or resources).

One way to handle that would be to create a copy of the prototype `RenderJobPackage`

on the stack, patch up the stack copy and then pipe that as argument to `RenderContext::render()`

. That is a fully valid approach and would work just fine, but since `RenderContext::render()`

needs to create a copy of the `RenderJobPackage`

anyway it is more efficient to patch up that copy directly instead. This is the reason for `RenderContext::render()`

returning a pointer to the `RenderJobPackage`

on the `RenderPackageStream`

.

Before diving into the `RenderJobPackage`

struct let’s go through the other arguments of `RenderContext::render()`

:

`shader_context`


We will go through this in more detail in the post about our shader system but essentially we have an engine representation called `ShaderTemplate`

, each `ShaderTemplate`

has a number of `Contexts`

.

A `Context`

is basically a description of any rendering passes that needs to run for the `RenderJobPackage`

to be drawn correctly when rendered in a certain “context”. E.g. a simple shader might declare two contexts: *“default”* and *“shadow”*. The *“default”* context would be used for regular rendering from a player camera, while the *“shadow”* context would be used when rendering into a shadow map.

What I call a “rendering pass” in this scenario is basically all shader stages (vertex, pixel, etc) together with any state blocks (rasterizer, depth stencil, blend, etc) needed to issue a draw call / dispatch a compute shader in the `RenderDevice`

.

`interleave_sort_key`


`RenderContext::render()`

automatically figures out what sort keys / `Commands`

it needs to create on it’s command array. Simple shaders usually only render into one layer in a single pass. In those scenarios `RenderContext::render()`

will create a single `Command`

on the command array. When using a more complex shader that renders into multiple layers and/or needs to render in multiple passes; more than one `Command`

will be created, each command referencing the same `RenderJobPackage`

in its `Command::head`

pointer.

This can feel a bit abstract and is hard to explain without giving you the full picture of how the shader system works together with the data-driven rendering system which in turn dictates the bit allocation patterns of the sort keys, for now it’s enough to understand that the shader system somehow knows what `Commands`

to create on the command array.

The shader author can also decide to bypass the data-driven rendering system and put the scheduling responsibility entirely in the hands of the caller of `RenderContext::render()`

, in this case the sort key of all `Commands`

created will simply become 0. This is where the `interleave_sort_key`

comes into play, this variable will be bitwise ORed with the sort key before being stored in the `Command`

.

`shader_pass_branch_key`


The shader system has a feature for allowing users to dynamically turn on/off certain rendering passes. Again this becomes somewhat abstract without providing the full picture but basically this system works by letting the shader author flag certain passes with a “tag”. A tag is simply a string that gets mapped to a bit within a 64 bit bit-mask. By bitwise ORing together multiple of these tags and piping the result in `shader_pass_branch_key`

the user can control what passes to activate/deactivate when rendering the `RenderJobPackage`

.

`job_sort_depth`


A signed normalized [0-1] floating point value used for controlling depth sorting between `RenderJobPackages`

. As you will see in the next post this value simply gets mapped into a bit range of the sort key, removing the need for doing any kind of special trickery to manage things like back-to-front / front-to-back sorting of `RenderJobPackages`

.

`gpu_affinity_mask`


Same as the `gpu_affinity_mask`

parameter piped to `begin_state_command()`

.

Let’s take a look at the actual `RenderJobPackage`

struct:

```
struct RenderJobPackage
{
BatchInfo batch_info;
#if defined(COMPUTE_SUPPORTED)
ComputeInfo compute_info;
#endif
uint32_t size; // size of entire package including extra data
uint32_t n_resources; // number of resources assigned to job.
uint32_t resource_offset; // offset from start of RenderJobPackage to first RenderResource.
uint32_t shader_resource_data_offset; // offset to shader resource data
RenderResource::Handle shader; // shader used to execute job
uint64_t instance_hash; // unique hash used for instance merging
#if defined(DEVELOPMENT)
ResourceID resource_tag; // debug tag associating job to a resource on disc
IdString32 object_tag; // debug tag associating job to an object
IdString32 batch_tag; // debug tag associating job to a sub-batch of an object
#endif
};
```


`batch_info`

& `compute_info`


First two members are two nestled POD structs mainly containing the parameters needed for doing any kind of drawing or dispatching of compute work in the `RenderDevice`

:

```
struct BatchInfo
{
enum PrimitiveType {
TRIANGLE_LIST,
LINE_LIST
// ...
};
enum FrontFace {
COUNTER_CLOCK_WISE = 0,
CLOCK_WISE = 1
};
PrimitiveType primitive_type;
uint32_t vertex_offset; // Offset to first vertex to read from vertex buffer.
uint32_t primitives; // Number of primitives to draw
uint32_t index_offset; // Offset to the first index to read from the index buffer
uint32_t vertices; // Number of vertices in batch (used if batch isn't indexed)
uint32_t instances; // Number of instances of this batch to draw
FrontFace front_face; // Defines which triangle winding order
};
```


Most of these are self explanatory, I think the only thing worth pointing out is the `front_face`

enum. This is here to dynamically handle flipping of the primitive winding order when dealing with objects that are negatively scaled on an uneven number of axes. For typical game content it’s rare that we see content creators using mesh mirroring when modeling, for other industries however it is a normal workflow.

```
struct ComputeInfo
{
uint32_t thread_count[3];
bool async;
};
```


So while `BatchInfo`

mostly holds the parameters needed to render something, `ComputeInfo`

hold the parameters to dispatch a compute shader. The three element array `thread_count`

containing the thread group count for x, y, z. If `async`

is true the graphics API’s “compute queue” will be used instead of the “graphics queue”.

`resource_offset`


Byte offset from start of `RenderJobPackage`

to an array of `n_resources`

with `RenderResource::Handle`

. Resources found in this array can be of the type `VertexStream`

, `IndexStream`

or `VertexDeclaration`

. Based on the their type and order in the array they get bound to the input assembler stage in the `RenderDevice`

.

`shader_resource_data_offset`


Byte offset from start of `RenderJobPackage`

to a data block holding handles to all `RenderResources`

as well as all constant buffer data needed by all the shader stages. The layout of this data blob will be covered in the post about the shader system.

`instance_hash`


We have a system for doing what we call “instance merging”, this system figures out if two `RenderJobPackages`

only differ on certain shader constants and if so merges them into the same draw call. The shader author is responsible but not required to implement support for this feature. If the shader supports “instance merging” the system will use the `instance_hash`

to figure out if two `RenderJobPackages`

can be merged or not. Typically the `instance_hash`

is simply a hash of all `RenderResource::Handle`

that the shader takes as input.

`resource_tag`

& `object_tag`

& `batch_tag`


Three levels of debug information to make it easier to back track errors/warning inside the `RenderDevice`

to the offending content.

The last type of commands are for dynamically updating various `RenderResources`

(Vertex/Index/Raw buffers, Textures, etc).

The interface for updating a buffer with new data looks like this:

```
class RenderContext
{
void *map_write(RenderResource *resource, render_sorting::SortKey sort_key,
const ShaderTemplate::Context* shader_context = 0,
shader_pass_branching::Flags shader_pass_branch_key = 0,
uint32_t gpu_affinity_mask = GPU_DEFAULT);
};
```


`resource`


This function basically returns a pointer to the first byte of the buffer that will replace the contents of the `resource`

. `map_write()`

figures out the size of the buffer by casting the `resource`

to the correct type (using the type information encoded in the `RenderResource::render_resource_handle`

). It then allocates memory for the buffer and a small header on the `RenderPackageStream`

and returns a pointer to the buffer.

`sort_key`

& `shader_context`

& `shader_pass_branch_key`


In some rare situations you might need to update the same buffer with different data multiple times within a frame. A typical example could be the vertex buffer of a particle system implementing some kind of level-of-detail system causing the buffers to change depending on e.g camera position. To support that the user can provide a bunch of extra parameters to make sure the contents of the GPU representation of the buffer is updated right before the graphics API draw calls are triggered for the different rendering passes. This works in a similar way how `RenderContext::render()`

can create multiple `Commands`

on the command array referencing the same data.

Unless you need to update the buffer multiple times within the frame it is safe to just set all of the above mentioned parameters to 0, making it very simple to update a buffer:

```
void *buf = rc.map_write(resource, 0);
// .. fill bits in buffer ..
```


Note: To shorten the length of this post I’ve left out a few other flavors of updating resources, but `map_write`

is the most important one to grasp.

Before wrapping up I’d like to touch on a few recent additions to the Stingray renderer, namely how we’ve exposed control for dealing with different GPU Queues, how to synchronize between them and how to control, communicate and synchronize between multiple GPUs.

New graphics APIs such as DX12 and Vulkan exposes three different types of command queues: *Graphics*, *Compute* and *Copy*. There’s plenty of information on the web about this so I won’t cover it here, the only thing important to understand is that these queues can execute asynchronously on the GPU; hence we need to have a way to synchronize between them.

To handle that we have exposed a simple fence API that looks like this:

```
class RenderContext
{
struct FenceMessage
{
enum Operation { SIGNAL, WAIT };
Operation operation;
IdString32 fence_name;
};
void signal_fence(IdString32 fence_name, render_sorting::SortKey sort_key,
uint32_t queue = GRAPHICS_QUEUE, uint32_t gpu_affinity_mask = GPU_DEFAULT);
void wait_fence(IdString32 fence_name, render_sorting::SortKey sort_key,
uint32_t queue = GRAPHICS_QUEUE, uint32_t gpu_affinity_mask = GPU_DEFAULT);
};
```


Here’s a pseudo code snippet showing how to synchronize between the graphics queue and the compute queue:

```
uint64_t sort_key = 0;
// record a draw call
rc.render(graphics_job, graphics_shader, sort_key++);
// record an asynchronous compute job
// (ComputeInfo::async bool in async_compute_job is set to true to target the graphics APIs compute queue)
rc.render(async_compute_job, compute_shader, sort_key++);
// now lets assume the graphics queue wants to use the result of the async_compute_job,
// for that we need to make sure that the compute shader is done running
rc.wait_fence(IdString32("compute_done"), sort_key++, GRAPHICS_QUEUE);
rc.signal_fence(IdString32("compute_done"), sort_key++, COMPUTE_QUEUE);
rc.render(graphics_job_using_result_from_compute, graphics_shader2, sort_key++);
```


As you might have noticed all methods for populating a `RenderContext`

described in this post also takes an extra parameter called `gpu_affinity_mask`

. This is a bit-mask used for directing commands to one or many GPUs. The idea is simple, when we boot up the renderer we enumerate all GPUs present in the system and decide which one to use as our default GPU (`GPU_DEFAULT`

) and assign that to bit 1. We also let the user decide if there are other GPUs present in the system that should be available to Stingray and if so assign them bit 2, 3, 4, and so on. By doing so we can explicitly direct control of all commands put on the `RenderContext`

to one or many GPUs in a simple way.

As you can see that is also true for the fence API described above, on top of that there’s also a need for a copy interface to copying resources between GPUs:

```
class RenderContext
{
void copy(RenderResource *dst_resource, RenderResource *src_resource,
render_sorting::SortKey sort_key, Box *src_box = 0, uint32_t dst_offsets[3] = 0,
uint32_t queue = GRAPHICS_QUEUE, uint32_t gpu_affinity_mask = GPU_DEFAULT,
uint32_t gpu_source = GPU_DEFAULT, uint32_t gpu_destination = GPU_DEFAULT);
};
```


Even though this work isn’t fully completed I still wanted to share the high-level idea of what we are working towards for exposing explicit MGPU control to the Stingray renderer. We are actively working on this right now and with some luck I might be able to revisit this with more concrete examples when getting to the post about the *render_config* & data-driven rendering.

With that I think I’ve covered the most important aspects of the `RenderContext`

. Next post will dive a bit deeper into bit allocation ranges of the sort keys and the system for sorting in general, hopefully that post will become a bit shorter.

I think I understand to some degree the details of the low level system and the high level system - the low level being the recording of the command in the command buffer, their sorting, and conversion to the underlying API, and the high level system being the renderable objects in the world - but what I have problems understanding at the level of detail that I would like is the connection between the two.




ReplyDeleteAt one point you mentioned that the recording of the command stream takes place in the render() function on the renderable object. My question is how does the o next know in what context it's being rendered. Say you want to render the object for a Z prepare or a shadow map generation part and for that only the vertex and index streams are required and potentially a different set of shaders, versus the full blown rendering for the main pass.

Do you go all over the render passes, and ask each object to generate the command stream, if any, for that pass?

I would appreciate it if you could elaborate more preferably with an example. Thanks!

Sorry for the typos. I meant ".. how does the objec know ...", and "Z-prepass". I typed this on a phone.

Delete@Ash The render() function of the objects gets called with a RenderContext* passed as argument. There's also some contextual information passed from the outside describing which shader context (i.e if we are rendering into a shadow map or rendering from the regular camera) to use.

ReplyDeletethanks for sharing this article.

ReplyDeletegoogle

Thank you very much for a great series of articles. One question I have is regarding how render targets are handled in the system. In part 2 you list render targets as one of the resource types referenced using RenderResource/render_resource_handle. However in this part, you use a RenderTarget * in the call to set_render_target. Is that simply a typedef for a RenderResource that you use when you know the type is render target? Or is there something more heavyweight involved that let's you deal generically with both back-buffer render targets and generated/dependent ones (gbuffer, etc.)?

ReplyDeleteJust wondering, when you'll post the article about your "Shader System" that you talk about? I've been eagerly waiting since February =P

ReplyDeleteIf you are getting any issue with QUickbooks then make a call at Quickbooks Support number for immediate help. they will provide the best service to you.

ReplyDeleteThank you very much for your great information. It really makes me happy and I am satisfied with the arrangement of your post. You are really a talented person I have ever seen.


ReplyDeleteRegards,

3d Architectural animation services | 3d architectural walkthrough services

This comment has been removed by the author.

ReplyDeletePlease keep writing more about it and give more insight. I'll bookmark your page so that I can visit your site regularly."



ReplyDeletelong term disability lawyer long term disability lawyer

birth injury lawyer birth injury lawyer

Personal Injury Lawyers Personal Injury Lawyers

Personal Injury Lawyers Personal Injury Lawyers

personal injury lawyers Brampton personal injury lawyers Brampton

personal injury lawyers bloor personal injury lawyers Bloor

Insurance lawyer toronto Insurance lawyer toronto

car accident lawyer toronto car accident lawyer toronto

hernia mesh lawyer toronto hernia mesh lawyer toronto

mississauga car accident lawyer mississauga car accident lawyer

brain injury lawyer brain injury lawyer

medical malpractice lawyers medical malpractice lawyers

personal injury law firms toronto personal injury law firms toronto

toronto injury lawyers toronto injury lawyers

I seriously love your site.. Very nice colors & theme. Did you build this amazing site yourself? Please reply back as I’m hoping to create my very own site and want to find out where you got this from or exactly what the theme is named. Kudos! onsite mobile repair bangalore I like it when folks come together and share thoughts. Great blog, continue the good work! asus display repair bangalore Good information. Lucky me I came across your website by chance (stumbleupon). I have book-marked it for later! huawei display repair bangalore


ReplyDeleteThis blog was... how do you say it? Relevant!! Finally I've found something that helped me. Appreciate it! online laptop repair center bangalore Everything is very open with a clear explanation of the issues. It was definitely informative. Your site is extremely helpful. Many thanks for sharing! dell repair center bangalore


ReplyDeleteIt’s hard to find experienced people about this subject, however, you seem like you know what you’re talking about! Thanks macbook repair center bangalore You need to be a part of a contest for one of the finest blogs on the web. I'm going to highly recommend this web site! acer repair center bangalore



ReplyDeleteGreat engaging information. Thank you for sharing. I found the post engaging and meaningful, which has added value in my understanding. Keep sharing good information. Thanks



ReplyDeleteHire Ruby on Rail (ROR) Developer

Hire mobile app developers

Hire android developers

Hire python developers in India

Hire net developers in india

Hire Joomla Developer

Hire PHP Developer

Online Casino Spielautomaten | Bestes Online Casino: Entdecken Sie Neue Online Casinos.

ReplyDeleteI think this is one of the great posts on this topic. This post is really great, very efficiently written information. Keep up the good work and keep us sharing these kinds of informative posts with us. I will also try to check out your other posts.




ReplyDeleteoutsource digital marketing services

outsource website development

top digital marketing agencies in india

virtual assistant websites

web design and development india

This web site really has all the info I needed about this subject and didn’t know who to ask. hdmoviespoint

ReplyDeleteI want to to thank you for this good read!! I definitely enjoyed every little bit of it. I've got you book-marked to look at new stuff you post…Best Plasma Cutter


ReplyDeleteNice blog, thanks for sharing with us this valuable information. I’m always read your blog for and I have got a lot of informative blog for this. Visit following page for Best Digital Marketing Company in India



ReplyDeleteCatering Piknik

ReplyDeleteistanbul catering

kokteyl catering

Mevlüt Yemekleri fiyatları

Mevlüt yemek Menüleri

kokteyl catering fiyatları

istanbul kokteyl catering

catering kokteyl menüleri

fuar yemek organizasyon

fuar yemek organizasyo firmaları

fuar için yemek firmaları

düğün yemek organizasyonu

düğün yemek organizasyonu yapan firmalar

istanbul kokteyl catering

istanbul kokteyl catering firmaları

Kokteyl catering fiyatları

kokteyl prolounge menu

kokteyl prolounge düğün

Paketli Mevlüt yemekleri

Düğün ve Mevlüt Yemekleri

Kokteyl Prolounge Menu

Mevlüt yemeği nedir

Pideli Mevlüt menüsü

Cenaze Yemek Organizasyonu

300 kişilik yemek Fiyatları

istanbul fuar yemek organizasyonn

istanbul fuar yemek organizasyo firmaları

istanbul fuar için yemek firmaları

istanbul düğün yemek organizasyonu

istanbul düğün yemek organizasyonu yapan firmalar

istanbul kokteyl prolounge menu

istanbul kokteyl prolounge düğün

istanbul Paketli Mevlüt yemekleri

istanbul Düğün ve Mevlüt Yemekleri

istanbul Kokteyl Prolounge Menu

istanbul Mevlüt yemeği nedir

istanbul Pideli Mevlüt menüsü

A good website is useful.

ReplyDeletenotstoppingbelieving.com

ghost-system.com

Spot on with this write-up, I absolutely think this amazing site needs a great deal more attention. I’ll probably be back again to read more, thanks for the info!


ReplyDeletebest-cheap-dehumidifier

This is a topic that's near to my heart... Cheers! Where are your contact details though?


ReplyDeletebest-cheap-24-inch-monitors

There is certainly a great deal to find out about this topic. I love all of the points you have made.


ReplyDeletebest-cheap-gaming-headsets

Buy Sex toys in India with with mytimetoy we are #1 seller for sex toys for women, sex toys for men, sex toys for couple and sex toys for bdsm we have high quality products for 100% Satisfaction.

ReplyDelete"

ReplyDelete""Medical Malpractice Lawyers is a Toronto-based personal injury law firm with over 45 years of experience.

Our medical malpractice group can help you pursue your medical malpractice claim.

medical malpractice lawyers

medical malpractice attorney

medical lawyer

medical negligence lawyers

medical malpractice law""

medical malpractice law firms toronto

medical malpractice lawyers toronto

Medical Malpractice Lawyers Barrie

medical negligence lawyers

medical malpractice lawyer ontario

Medical Malpractice Lawyers Alberta"

"

ReplyDelete""Medical Malpractice Lawyers is a Toronto-based personal injury law firm with over 45 years of experience.

Our medical malpractice group can help you pursue your medical malpractice claim.

medical malpractice lawyers

medical malpractice attorney

medical lawyer

medical negligence lawyers

medical malpractice law""

medical malpractice law firms toronto

medical malpractice lawyers toronto

Medical Malpractice Lawyers Barrie

medical negligence lawyers

medical malpractice lawyer ontario

Medical Malpractice Lawyers Alberta"

This is good piece of writing and pleasant urging content



ReplyDeleteWe provide good and appropriate Services for you. They provide 100% customer satisfaction service. If you have any problem in Netflix about then just visit Netflix Phone Number Australia Dial Toll-Free Number 1-800-431-401

ReplyDeleteArticles that are good and very interesting, I love reading the articles you make.

ReplyDeleteDigital Marketing Agency Brisbane

Best Digital Marketing Agency Brisbane

Just wondering, when you'll post the article about your "Shader System" that you talk about? I've been eagerly waiting since August. I love reading your articles. Thanks for sharing it - Deep Things To Say To Your partner

ReplyDeleteAutomated Forex Trading : tradeatf Is An Automated Forex Investing Software. It Is An Algorithmic Trading Software That Provides Automated Forex Trading Signals.


ReplyDeleteI think this article is useful to everyone.


ReplyDeleteรูเล็ต เว็บไหนดี

วิธีเล่น รูเล็ตออนไลน์ เป็นอย่างไร

เทคนิค รูเล็ต

รูเล็ต ขั้นต่ำ 1 บาท

รูเล็ต วิธีเล่น

ตาราง ไฮโล

เกมส์ไฮโลออนไลน์ เกมส์ไฮโลไทย เล่นง่ายได้เงินจริง

ไฮโลออนไลน์ ดีที่สุด

วิธีเล่น ไฮโลออนไลน์

ตาราง ไฮโล

happy-eid-milad-un-nabi-images


ReplyDeleteeid-milad-un-nabi-2021-images

Aaqa-Ka-Milad-Aaya-Lyrics

Eid-Milad-Un-Nabi-Mubarak-Images

Eid-Milad-Un-Nabi-Ki-Haqeeqat-In-Hindi

Eid-Milad-Un-Nabi-In-Quran

undefined

Plan for Jio tower installation 2022 - Apply Now For Jio Tower | Apply Reliance Jio Tower Installation Online | Jio tower installation monthly rent | Jio Tower Complaint Helpline Number - Jio Tower Helpline Number | Reliance Jio Tower Installation Process Steps To Install | Reliance Jio Tower Installation Apply Online and Contact Number 2022 | Jio tower installation customer care number and contact number | Jio tower installation apply online 2021 & jio advance amount

ReplyDeleteبرای رزرو بنر تبلیغاتی در شهرهای ایران می توانید به این سایت مراجعه کنید.

ReplyDelete


ReplyDeleteDefinitely a great site and very informative posts. เว็บ 123betting

코인카지노 | 우리카지노계열 | 코인카지노 쿠폰 - 쿠쿠카지노

ReplyDeleteBadrinath Kedarnath Yatra by helicopter price: The Badrinath shrine, one of the 12 jyotirlingas of Lord Shiva, is a scenic spot situated, against the backdrop of the majestic Kedarnath range. Kedar is another name of Lord Shiva, the protector and the destroyer. According to legend, the Pandavas after having won over the Kaurava in the Kurukshetra war, felt guilty of having killed their own brothers and sought the blessings of Lord Shiva for redemption. He eluded them repeatedly and while fleeing took refuge at Kedarnath in the form of a bull. On being followed he dived into the ground, leaving his hump on the surface. The r! emaining portions of Lord Shiva appeared at four other places and are worshipped there as his manifestations. The arms appeared at Tungnath, the face at Rudranath, the belly at Madhmaheshwar and his locks (hair) with head at Kalpeshwar. Kedarnath and the four above-mentioned shrines are treated as Panch Kedar.


ReplyDeleteAmazing post!I was reading since last week.It was helpful and informative for me.We are offering the best online writing a dissertation proposal to the students at a cheap price.

ReplyDeletekhwaja garib nawaz urus mubarak


ReplyDeletekhwaja garib nawazchatti

syed baba tajuddin

ya syed ahmed jilani

labbaik ya rasool allah hu

Best Fantasy Football Names


ReplyDeleteOdell Beckham JR Fantasy

Nick Chubb Fantasy Names

Kyler Murray Fantasy Team Names

Clever Fantasy Football Names

Davante Adams Fantasy Names

This is excellent article, thank you for the share! This is what I am looking for, hope in future you will continue sharing such an superb work.


ReplyDeleteDumb And Dumber Suits Gif

Marvelous, what a blog it is! This website provides valuable facts to us, keep it up.



ReplyDelete토토사이트

스포츠중계

Hi there everyone, it's my first visit at this web site,




ReplyDeleteand post is actually fruitful in favor of me, keep up posting these types of articles.

토토사이트

배트맨토토프로

All Islamic Knowledge, Dua, Surah Yaseen, Surah Pdf, Full Quran, Tilawat-e-Quran or Some Islamic question and answers.







ReplyDeleteHanuman Chalisa Lyrics, Hanuman Chalisa Pdf File

read hindi songs lyrics, english songs lyrics. Here people can easily search their favourite songs lyrics very easily. You can easily download all songs pdf file just one click.

Surah Yaseen Pdf, Hanuman Chalisa, Lyrics in Hindi

Surah Yaseen Pdf

Hanuman Chalisa Lyrics in Hindi

Songs Lyrics

i loved your post this is interesting post for me . I will be share it my friend circle. your topic is nice and really posting was greate .Camping in rishikesh


ReplyDeleteChardham yatra package

Best travel agency in Dehardun

Rafting in Rishikesh

Travel agents in Uttarakhand

Car rental in haridwar

CAMPING IN RISHIKESH

Nice Article, Keep it up. Check more about How Char Dham Yatra 2023 is going to start soon and what to do for the Char Dham Yatra with Gokeys Best Travel Agents in Haridwar.

ReplyDeleteWe provide Uttarakhand Tour package offers a wide range of travel itineraries, chardham yatra package, Uttarakhand cab rental service, for more Information you must to visit our website...

ReplyDeleteUttarakhand Tour Package

Hill Stations Package

Uttarakhand Holiday Package

Typically, you will get online cash advance loans your funds as soon as the next business day. If you apply online and get approved for a guaranteed installment loans for bad credit Georgia on the morning of the working day, t

ReplyDeleteDallas HVAC (Heating, Ventilation, and Air Conditioning) services ensure year-round comfort in the dynamic Texas climate. Trusted HVAC providers in Dallas offer a range of solutions, including installation, maintenance, and repairs for residential and commercial properties. Expert technicians utilize cutting-edge technology to optimize energy efficiency and indoor air quality.



ReplyDeleteWith a focus on customer satisfaction,

Dallas HVACcompanies prioritize timely and reliable service, addressing issues such as air conditioning malfunctions, heating system inefficiencies, and ventilation concerns. Whether it's sweltering heat or chilly nights, Dallas HVAC professionals keep homes and businesses comfortable, contributing to a healthier and more enjoyable living environment.The Chardham Yatra by Helicopter from Hyderabad is an innovative approach to a sacred pilgrimage. Exploring the pricing details is crucial for potential pilgrims like me. Hoping for reasonable and transparent costs that make this divine journey feasible for spiritual seekers from Hyderabad.



ReplyDeletechardham yatra by helicopter

Char Dham Yatra is a sacred pilgrimage to Yamunotri, Gangotri, Kedarnath & Badrinath. The Char Dham of Uttarakhand requires online registration. How To Register For Char Dham Yatra

ReplyDelete