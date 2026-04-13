---
title: The journey of porting AnKi to Vulkan
url: https://anki3d.org/porting-anki-to-vulkan/
author: Panagiotis Christopoulos Charitos
published: '2016-09-13'
source_blog: AnKi 3D Engine Dev Blog
source_site: https://anki3d.org
category: graphics
fetched: '2026-04-13'
---

Someone once said “make it work, make it fast, make it pretty” and I’m happy (and at the same time relieved) to say that the effort of porting AnKi to Vulkan just hit the first major milestone! It’s working! I think this is a good time to share a few thoughts on how this milestone was achieved, the pains and generally the overall experience. Disclaimer: Whatever you read in the following lines reflects my own views and not those of my current employer.

So let’s start from the beginning.

It become apparent from the beginning that this task will not be easy. My biggest fear was to start writing something and then realize that it will not work and that I have to rewrite it. I had to be extremely careful in order to avoid any kind of frustrations. That’s why everything started by **designing a graphics abstraction** that will work well under GL and Vulkan. Step by step the old abstraction was modified according to the new design.

After a short while AnKi ended up having an abstraction layer with two backends. The GL backend was working well and the only thing I had to do was to write the Vulkan backend. To move forward I was adding some Vulkan bits and then creating small unit tests to test the correctness. **Test driven development** basically. The first milestone was to clear the default framebuffer with some color, so the framebuffer class was implemented, also the present mechanism and some command buffer bits. After getting that done the next milestone was to draw a flat triangle. The next one was to add uniforms and so on.

After adding most of the code in the Vulkan backend it was time to **test the fully fledged renderer**. This was the tough part. The first sub step was to run everything without any validation errors. Fortunately the validation layers are in a good shape and that helped alot. After fixing the validation errors I found myself in front of a black screen. Engineers before me used RenderDoc or other tools in order to debug their ports. Unfortunately RenderDoc doesn’t have a Linux GUI (it’s under development AFAIK) so I had to do some work on Windows. I spent a few days trying on Windows but I give up (Sorry, I really can’t stand developing on windows anymore). I moved back to Linux and tried debugging the old fashion way. Never really relied on debugging tools in the past anyway. So I was fixing various bugs and enabling one renderpass after the other until the last one.

# AnKi’s graphics API abstraction (aka GR)

The most important thing in the whole process was to create a graphics abstraction that sits on top of GL and Vulkan. The goals for this abstraction were very simple:

- Work fast with Vulkan
- Work VERY fast with Vulkan
- Avoid any unneeded complexity. Increased complexity most of the time leads to more bugs and worst performance

Vulkan is less flexible than GL. In GL you can bind stuff at any time and that’s it. The driver will do all the magic behind the scenes (behind your back actually). In Vulkan there is a need to batch state into pipelines and descriptors sets. At the same time I wanted to avoid hashing state, hashing or creating descriptor sets etc. It’s more complex, a bit slower and the alternative didn’t prove that bad of a choice. So what’s the alternative?

Create an abstraction that is closer to Vulkan. The classes of this abstraction are:

- CommandBuffer
- Pipeline
- Shader
- ResourceGroup (something like descriptor set)
- Texture
- Buffer
- OcclusionQuery
- Framebuffer
- Sampler

That’s it. Way more simple than Vulkan but it exposes pipelines and descriptor sets to the upper layers. At the same time it’s more cumbersome than GL since it forces the upper layers to create pipelines and resource groups.

# Implementation details

This section describes some of the internals of Vulkan’s backend.

The **memory manager **is the class that handles all GPU memory allocations. It allocates big chunks and suballocates from them. It works like malloc and free and the output is a VkDeviceMemory and an offset. The internals of the memory manager are a bit complex and they deserve another post.

The **sampler** object is pretty easy to grasp and maps to Vulkan 1 to 1. Nothing interesting here.

The **texture** object is more complex. For compatibility reasons it contains a sampler object just like GL. It has a single VkImage and multiple VkImageViews. The image views are created on request and then cached. Different image views are needed if the texture will be used for sampling, different if it’s going to be used as a framebuffer attachment, different if it’s for storage images etc. Apart from that everything else is straight forward.

The **buffer** object is also quite straight forward. Nothing interesting here.

The **shader** is also relatively simple at this point. Its input is pure GLSL and it’s using glslang to compile that down to SPIR-V. AnKi doesn’t compile shaders offline at the moment.

The **pipeline** is also relatively simple and it maps nicely to Vulkan. The key difference is that it’s using a single global VkPipelineLayout. For simplicity GR is using a global pre-created VkDescriptorSetLayout and a global VkPipelineLayout. These layouts contain a fixed number of descriptors at specific bindings. For example the sampled images are from binding 0 to binding 10. One more problem with VkPipeline is that it requires the VkRenderPass. Internally there is a global cache of “compatible render passes” and the pipeline requests a render pass using the number of attachments and their formats. According to the spec these information are enough to create a compatible renderpass and that eliminates the need of passing another object into the pipeline’s initialization.

The **resource group** wraps a single VkDescriptorSet. It’s been allocated from of a global descriptor pool. As stated before it’s using a global VkDescriptorSetLayout. The engine never allocates descriptor sets inside a frame. Resource groups are created on asset loading.

The **framebuffer** wraps a single VkFramebuffer and a single VkRenderPass. The renderpass contains a single subpass without any implicit image transitions. At the moment all barriers are set outside.

The **command buffer** is an interesting beast. It does many things but it maps well to Vulkan. There are N command pools one for each thread. So every command buffer must be created, built and submitted from a specific thread. The engine creates and destroys many command buffers every frame, to minimize the cost of creation GR recycles the command buffers. AnKi also creates lots of command buffers at load time. These command buffers contain, at most, 10 commands that do texture or buffer loading. To avoid recycling fat command buffers to slim ones command buffer initialization accepts a flag that denotes the number of commands this command buffer will hold (CommandBufferFlag::SMALL_BATCH). One interesting aspect is that pipeline barriers are **explicit** command buffer commands just like in Vulkan. This help us avoid many headaches down the line.

The **occlusion query** is pretty straight forward too. Nothing interesting to mention here.

As you can see the abstraction is very explicit and very close to Vulkan. It hides many things (like memory management) without sacrificing much of the performance characteristics of Vulkan. At the same time the Vulkan backend is extremely simple. The GL backend is 6K loc and the Vulkan is 9K.

The **image layouts** are a pain. There is no easy way to handle the transitions so I tried to be explicit just like Vulkan. For that reason there is a bitmask of texture usage (TextureUsageBit::SAMPLED_VERTEX, TextureUsageBit::FRAMEBUFFER_ATTACHMENT_READ etc). When creating a texture someone will need to specify all the possible texture usage bits. When binding that texture to a resource group we also need to specify the usage for that particular binding. Also when binding that texture to a framebuffer we need the usage. The TextureUsageBit is a mask that follows the texture everywhere, unfortunately. This mask is been used to set barriers as well. The pipeline barriers take the previous and the next usage of a texture and calculate the layouts, the access masks etc.

cmdb->setTextureSurfaceBarrier(aTexture, TextureUsageBit::GENERATE_MIPMAPS, // Prev usage TextureUsageBit::SAMPLED_FRAGMENT | TextureUsageBit::FRAMEBUFFER_ATTACHMENT_READ, // Next usage TextureSurfaceInfo(i, 0, 0, 0));

The next major pain is the **differences in coordinate system** between GL and Vulkan. I have to mention that this was the number one source of rendering bugs. How it is solved in AnKi at the moment? For Vulkan this is what happens:

- Appending this to every vertex shader to change the depth range: gl_Position = x_; gl_Position.z = (gl_Position.z + gl_Position.w) * 0.5
- Changing the triangle winding from counter clockwise to clockwise. That eliminates the need for y flip.
- For the last renderpass in the pipeline flips the input texture coordinates in order to flip the image.

This might be the least intrusive way to workaround the issue but we are not quite there yet. I hope Khronos releases an extension that allows us to configure the coordinate system and the various ranges just like GL does.

# Future improvements

The Vulkan backend is not quite where I want it yet. There are some improvements planed for the future:

Perform some **performance analysis** and drop a few words. The windowing system prevents me from running at full speed.

Get my hands on an **AMD GPU** to test there as well. AMD HW is in the middle of two worlds at the moment (on Linux always). On one hand we have the AMDGPU-PRO that seems to support everything AnKi requires but not sure about its quality. On the other hand Mesa seems quite promising but it doesn’t support GL 4.5 yet and the opensource Vulkan driver is MIA.

Add support for **push constants**. Some platforms will benefit significantly from push constants. ARM’s Mali and AMD’s GPUs for sure.

Another thing is to **batch command buffer commands**. At the moment there is no batching of barriers for example. This kind of optimizations were left out until all other bugs were fixed.

Add support for **multiple sub passes**. This will benefit ARM and IMG and, to a lesser degree, other vendors as well.

Add support for **async compute**. ~~At this point I’ll have to rant a bit. I don’t quite understand why async compute is considered great. Let me put it this way. There is a piece of silicon in the HW that sits idle and it can only do compute work. How is that a good piece of engineering? Most HW out there tried to unify the execution units.~~ UPDATE: See comments.

# Footnote

So what worked well IMO:

- glslang worked with zero issues.
- The validation layers, even if they won’t catch everything yet, they are quite decent at this point.

What didn’t work well:

- Vulkan’s coordinate system creates unnecessary frustrations and it was the number one source of bugs.
- Windowing system extension is very hard to get right. More on that in the future.
- Hate image layouts.

Vulkan has a bright future IMHO and people should start investing more time learning it and using it. Porting to Vulkan is not extremely time consuming or difficult and if a guy with a small kid can do it during his free time then imagine what a major studio can do.

“One interesting aspect is that pipeline barriers are explicit command buffer commands just like in Vulkan. This avoided many headaches down the line.”

I guess you meant ‘like in OpenGL’? 🙂

…and that.

My biggest fear (for a GPU bound scenario) is to have tiny bubbles because of the barriers. It’s unclear (to me at least) what is the best point to set them, how to best batch them etc. So I said fuck it let’s expose them to the high level abstraction. It’s something like ~21 barriers so it can’t be that bad. Maybe I’ll find a better way down the line.

PS: Good luck with your Vulkan backend! (sorry, wordpress give you away :))

No worries 🙂

Basically we’re all trying to reverse engineer what driver writers spent years working on!

We are all still learning how/where to do the transitions/barriers…

Hardware for async compute in AMD cards is not a separate piece of GPU that sits idle. These are the very same compute units that calculate your vertex shaders, fragment shaders, or regular compute shaders. They are just not fully utilized all the time, so while you execute some workload that is bottlenecked on some other stage of 3D pipeline (like when rendering geometry into a shadow map) you may get benefit from running some ALU-intensive computer shader in async compute at the same time.

@Adam: Thanks for the clarification. I’ve edited the article.

I’m still scratching the surface on how to saturate a GCN GPU (recently started actually). After firing the RadeonGraphicsProfiler the first thing I noticed was that G-buffer pass was mostly idle (no surprise). Executing (ALU heavy) async compute parallel to G-buffer pass will fix that problem. What I don’t know is if compute in the graphics queue will. In other words running something like this:

1. pipeline barrier

2. g-buffer-pass

3. some-compute

4. pipeline barrier