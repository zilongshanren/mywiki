---
title: Getting started with D3D12
url: https://anteru.net/blog/2015/getting-started-with-d3d12
published: '2015-08-23'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

Welcome to a short introduction to Direct3D 12 (also know as DX12, DirectX12 and D3D12) - the new graphics API from Microsoft, which brings new concepts to the table that have been introduced with [Mantle](http://www.amd.com/Documents/Mantle-Programming-Guide-and-API-Reference.pdf). These new APIs could be classified as “explicit” APIs, as they have very few things that happen automatically unlike previous APIs like Direct3D 11 and OpenGL 4. In this blog post, I’ll introduce the basic concepts behind these new APIs. To follow along, I’d recommend that you check out my [tiny D3D12 sample application](https://github.com/anteru/d3d12sample) which illustrates the techniques.

## Some kind of motivation

So why did these new APIs emerge? Let’s start with a motivating example. In D3D11, you can map a buffer for writing and specify the [discard flag](https://msdn.microsoft.com/en-us/library/windows/desktop/ff476181%28v=vs.85%29.aspx). That flag is actually a serious problem for the GPU. Let’s assume for a moment that the buffer hasn’t been used yet, and that a frame where it will be used is queued and being processed by the GPU. The driver can’t simply overwrite the buffer in GPU memory because when you submitted the frame, it wasn’t mapped, and time travel is still quite hard.

The driver has only two choices. The naïve one is to simply drain the GPU and wait for it to finish. Performance will be horrible if this happens for every map call, but it will be correct. The right choice is to simply create a new buffer, put the data in there, upload it to the GPU and track the original buffer. Once the frame where the original buffer is used finishes, the original buffer can be recycled and everything is fine. Except the driver now needs to manage a new buffer per map call – tricky, but possible.

If you think that’s just an example – no, it isn’t. This buffer replacement is called **buffer renaming** and is a standard technique used by D3D11 drivers. Depending on how large the rename buffer is, and how often buffers are discarded, it can work quite well but it means there has to be some logic in the driver to manage and track this.

## Going explicit

With D3D12, these things go away, and the developer is now directly exposed to memory management and synchronization. What does this mean exactly? Well, for starters, tracking of resources has to be done by the developer. If you look into my sample, you’ll notice I create “frame fences” which allow me to check if a frame has finished. For the constant buffers, I have one constant buffer **per queued frame** in a cheap-man’s ring buffer. Using the frame fence, I can synchronize with the GPU while still allowing the GPU queue to fill up. This removes the need for rename buffers from the driver.

**Memory management** is now also explicit, for instance, uploading does no longer happen “under the hood”. You’ll notice that I use two kinds of resources: Static data like the vertex and index buffer as well as the texture, and dynamic data like the constant buffer. For the dynamic data, which is read only once, it doesn’t make too much sense to push it to the GPU at all. In my sample, I hence place the constant buffer in CPU memory and let the GPU read that directly. In D3D11, the driver has to guess how often a buffer will be read and where to place it, but in D3D12, I can use the knowledge I have about my access patterns to optimize this.

The other data needs to be uploaded, and unlike D3D11 where this happens automatically, I have to do this on my own. Which means I need to reserve space on the CPU from where to stage the update, allocate some GPU memory, issue a copy and wait for it to finish before I use the resource. In the small sample, you can see that I wait for it to finish manually and hence keep everything deterministic but in a larger application I could take advantage of the copy queue and copy data **independent of the rendering**. This makes it easy to implement advanced streaming which was very hard to do before, as the driver can’t predict when a resource has to be resident on the GPU.

## Resource state tracking

Another completely new responsibility for developers is state tracking. In D3D11, resources transition between states automatically which can lead to bad performance. Imagine the following scenario: Four shadow maps are rendered and applied onto the scene. The application renders into a shadow map, changes the target, renders into the next and so on and then finally loops over the four shadow maps and reads them. What you may not know is that **GPUs compress depth data** to improve bandwidth and eventually performance, but the texture units may not be able to read that compressed data directly and hence require a decompression. This decompression can potentially require a flush and wait-for-idle to make sure that the compressed data is written completely and no longer used before it gets decompressed.

Now, if the driver is not careful, this could result in a decompress, flush, read cycle, four times. The reason for this is that the driver only notices that the decompression is needed when it sees that the resource is bound for reading. With D3D12, these **transitions are now explicit** and the developer can schedule them. In the example above, he can choose to decompress all four shadow maps at once in a **single transition**, pay the cost for the flush once and improve performance.

## Draw state & shaders

Another big area where the D3D11 driver spends time is setting and validating state. For instance, let’s assume you set a vertex and a pixel shader. The driver must check that the signatures of both match and this can only happen at draw time because the driver cannot precompute all permutations of vertex and pixel shaders to look this up. Often, the driver will even **delay** the compilation of a shader until it is used for the first time to improve startup time and easily skip unused shader. Games often have to to “pre-warm” the driver shader cache by touching all combinations once during loading to ensure that the gameplay doesn’t get interrupted when the driver starts to compile a shader.

In D3D12, this changes completely with the introduction of [pipeline state objects](https://msdn.microsoft.com/en-us/library/windows/desktop/dn899196%28v=vs.85%29.aspx#pipeline_state_overview) which group all shaders and quite a bit of rendering state together. Grouping this data allows the driver to **validate everything once** and at runtime just swap the state without any further checks. It also means the driver can check if the pixel shader output is used at all and optimize the shader is some data is going to be discarded anyway. This is a huge change from previous APIs, and is also a major pain point when transitioning legacy engines which tend to identify the required combinations at run-time. In the D3D12 world, the shaders need to become part of the asset pipeline. In the sample, you can see how much state actually goes into the pipeline state object, even for a rather simple shader setup.

## Resource binding

Finally, resource binding in the D3D12 world is totally different from D3D11. Legacy APIs tend to model the GPU as something I call the “slot machine”. You have lots of different slots where you plug in textures, samplers, etc. This used to be the case how hardware worked but it’s not true since several years. If you look for instance at the [GCN ISA documentation](http://amd-dev.wpengine.netdna-cdn.com/wordpress/media/2013/07/AMD_GCN3_Instruction_Set_Architecture.pdf), specifically for “image resources”, you’ll notice that there is no “sampler slot” or “texture slot” being used there. Instead, the texture and sampler **descriptor** is loaded into a bunch of registers and that’s it. This new model is what is used by D3D12 through the root signature and descriptor tables.

The root signature serves as the first indirection level for resource bindings. It can contain some data in-line if it is small enough – for instance, a pointer to memory (also known as a constant buffer) or a few floats, or pointers to descriptor tables that can contain larger descriptors (for instance, texture descriptors.)

It is interesting that the root signature is still tracked with renaming, but as it is generally very small, this is not a huge problem (for best performance, it should be small and some other rules should be followed as well – check out [this GDC 2015 presentation on D3D12](http://amd-dev.wpengine.netdna-cdn.com/wordpress/media/2012/10/Getting-the-best-out-of-D3D12.ppsx) for details.) In the sample, you can see how the texture descriptor is placed in such a table and then referenced from the root signature. Again, the goal here is to allow to **change large amounts of bindings very quickly**. Unlike in D3D11, where the developer changes slots and the driver needs to map them to descriptors and build the table on demand, the developer can now swap for instance all textures and samplers required by a material by updating the descriptor table pointers in the root signature – a very cheap and fast operation.

## Things we didn’t look at

D3D12 also comes with explicit **command buffers** which allow multiple CPU threads to record commands. I’m not covering this here as the sample doesn’t take advantage of multiple threads – maybe some other time :) I’m also not covering the different queues exposed by D3D12 today. In D3D12, it is possible to **execute a compute shader concurrently with draw calls** and data transfers happening by taking advantage of the graphics, compute and copy queue. This is again and advanced feature which is no good fit for an introductory post.