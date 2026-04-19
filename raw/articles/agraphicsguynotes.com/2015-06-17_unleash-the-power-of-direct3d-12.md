---
title: Unleash the power of Direct3D 12
url: https://agraphicsguynotes.com/posts/unleash_the_power_of_direct3d_12/
author: Jiayin Cao
published: '2015-06-17'
source_blog: A Graphics Guy's Note
source_site: https://agraphicsguynotes.com/
category: graphics
fetched: '2026-04-19'
---

Direct3D12 is about to come. There are several presentations available in GDC this and last year talking about the new features in it. I’m gonna list some of the changes that D3D12 introduces in this post. It only covers some of the changes.

# The big picture

Different from its predecessors, D3D12 mainly aims at reducing CPU overhead. Improving CPU performance is the first priority in this new API. Of course that’s not to say there is nothing more. Besides better CPU performance, it has some feature improving GPU performance. Apart from performance improvement, there are also some new graphics features available on latest hardware, such as conservative rasterization, raster ordered view, etc. In this article, I’m gonna talk something about the new features in D3D12 that improves performance. New graphics features are won’t be mentioned.

The followings are the most important changes between 11 and 12:

- D3D11 uses an immediate context with one or more deferred context. Deferred context is rarely used because most of the driver work is still in one single thread, like resolving resource dependencies. There is no immediate context in d3d12 anymore, everything is deferred. With this change, it allows game developers to utilize the multi-thread power of their hardware.
- Hardware states used to be merged into several separated state group, like rasterizer state, depth stencil state. And programmable shaders are set through dedicated interfaces, such as VSSetShader. That’s the old model in d3d11. In the brand new d3d12 model, we have PSO(pipeline state object) grouping almost all of the states and shaders together as a single object.
- Memory used to be strongly typed in old d3d. Developers have full control on it now. For buffers, we have buffer heap and it is totally valid for games developers to place multiple vertex buffer data and index buffer data in the same heap. This is no such as thing called vertex buffer object or index buffer object anymore, every buffer is just generic data. Though, there is still flags indicating the usages of buffers.
- There are 128 shader resource views for per programmable stage in D3D11. The number is limitless for d3d12. However, it is set in a whole new different way. Root signature is the window for doing all the resource binding stuff. There are still some resources to be set through old-school interface, like vertex buffer and index buffer. For the ones we care, like textures, constant data, samplers, it is no longer working this way.
- D3D11 tracks the resource states through reference counting, making sure that resource lifetime and residency management is well handled and avoids resource hazard. It is used to be a strange topic for some PC developers because game developers are not required to handle the issues themselves. In D3D12, developer needs to resolve these things themselves. It does intrudoce more work, but this is one of the key changes to allow multi-thread rendering, which simpliy puts is to allow issuing draw calls in different threads.
- D3D11 will accumulate commands for at most three frames before flushing the command list to hardware push buffer, the number is basically transparent to programmers. Now it is developers’ responsibility to manage it explicitly, fencing is a necessary thing in D3D12.
- And D3D12 users should also manage back buffer explicitly from now on, D3D runtime won’t babysit it for us.

The above list is by no means a full review of what d3d12 has brought to us. But they are considered some of the most important changes.

# Explicit Memory Management:

Memory in D3D11 used to be strongly typed during initialization and declaration. A vertex buffer is created through the interface called createvertexbuffer, very self-explanatory, it just returns an object that represents the resource of vertex buffer. We can fill the data during creation or later. There are some drawbacks with the resource management model. Memory address is transparent to the developers, who are out of control. There may be some small pieces memory between resources which will never be used for a decent-sized resource, it depends on the specific implementation of drivers. And little detail information is revealed to public.

The good news in D3D12 is that we will have full control on the memory allocation and residency management. Let’s take an example, we want a vertex buffer and an index buffer for a specific model, it is a typical scene. What we have to do in D3D11 is to create two separate resources. Here is the new way, it is necessary to create a heap for buffers first. The size of the heap can be the sum of the size of total vertices data and indices data or more if we like. After creating the heap, we can copy the vertex and index data into the heap to some location. Where and when to copy the data is totally up to us. We can create a vertex buffer view and index buffer view according to the addresses we put them. Those views will be used to set the buffers. We have a lot more control during the initialization. What’s more nature is that we are treating vertex and index data as generic ones, they are just some memory. Regardless of their usages, there are no essentially difference. Even amazing is that we can put constant buffer in the same heap, it is totally a valid way of doing it. Those geometry information is parsed from files and developers are free to choose what kind of memory to use for them. There is just no reason to give up that flexibility in graphics interface.

# Explicit Resource Management:

## Resource lifetime and residency

Resource lifetime and residency management used to be handled by D3D11 runtime. Programmers usually don’t need to care much about it. The sacrifices we have to make for this convenience is more CPU overhead through a lot of reference counting under the hood and the common ‘solution’, which is more of workarounds to me, is to find varies ways to reduce the number of draw calls.

In order to reduce the CPU overhead, D3D12 programmers need to manage resource life time and residency explicitly. In this way, there is no need for D3D12 runtime to add reference counting for the purpose of lifetime and residency management, it will assume that everything is handled by programmer with their higher level knowledge. For example, in the old d3d, if we want to change something in a vertex buffer, we can map it first with “discard” flag, we will get a memory address immediately after this function call without flushing all API commands that relate to this specific vertex buffer, what happens is actually that another piece of memory is returned to us by driver and this very piece of memory will be used as the vertex buffer at a latter point. Through that way, the driver doesn’t need to flush any related command calls before returning the memory address and it looks decent to the programmers. The efficiency will be lower if the size of memory is quite large. Of course there are other methods for updating the resource. In the new model, we are responsible for everything. It works in a map-persistent way similar to OpenGL4. We can map the buffer at the initialization stage and never unmap it. We can change the memory anytime we want. One simple rule holds here, since CPU and GPU are working asynchronously, it is necessary to make sure that we don’t stamp on the memory in use by GPU. Usually a ring/circular buffer is used to avoid conflict.

## Resource hazard tracking

Similar to resource lifetime and residency management, resource hazard is another issue that belongs to the programmers’ responsibilities from now on.

Suppose we have a shadow map algorithm, a shadow map generation pass is performed first, followed with a shadow masking pass. In the first pass, a texture is used as a render target and it is then used as a shader resource view for reading in shadow masking pass. D3D11 runtime and driver will make sure to finish the shadow map generation pass before the execution of shadow masking pass, it won’t in D3D12. D3D12 runtime will only guarantee that shadow map generation pass is issued earlier than shadow masking pass, in other words, instructions for the first pass will be before the instructions in the second pass in the command list or push buffer. However what it doesn’t promise is that shadow masking pass is finished before the beginning of shadow masking pass, which may result in invalid reading of shadow map in shadow masking pass just because the first pass may not finish itself. That is a typical resource hazard case.

What we need to do in D3D12 is to add a resource barrier to make sure everything is in the right state. With a resource barrier, the driver will wait for the first pass to finish before proceeding to the next ones. A big difference is that programmers are in control now.

For better performance, a group of resource barriers can be triggered together. Resource barrier can even be split into two parts, begin and end. It will avoid dummy idle waits if there is gonna be one.

# Resource binding:

Resources, like vertex buffer and render target, are still set in a similar way. Only the ones we care are mentioned in this section. They are the famous draw call breakers, constant data, textures and samplers. We have four type of views in D3D11, shader resource view, render target view, depth stencil view and unordered access view. There will be more in 12, vertex buffer view, index buffer view, constant buffer view, stream output buffer view. Good thing is they are no longer d3d object anymore. Most of the new comers are just simple, transparent structures well defined in the d3d12 header file, we can see everything in the structure. For SRV, RTV, DSV, UAV and CBV, a heap needs to be created first. Each should have a dedicated heap, we can’t mixed them in one single heap, except that we can mix SRV, CBV, UAV in a same heap. Within the heap, we can create as many views as we want. Most of the views are set through specific interfaces. However for SRV, CBV and UAV, we need to set them through a new object, called root signature.

## Root Signature:

Root Signature is a whole new concept. It behaves like a window for binding resources to shaders. There are three type of data can be set through it:

- Descriptor table. It is nothing mystery. Just an offset in the heap and the number of descriptors(views) to be set.
- Descriptor. It should be the same with view, just different names.
- Constant Data.

Each has some unique features. Descriptor table can bind multiple resources in one go. While it requires two extra memory fetches on GPU, get the memory of descriptor table, then get the descriptor before reaching the data we are interested. Putting constant data in root signature will get the best performance in term of GPU, because there is no extra memory fetch at all. Descriptor is someone middle, we can only set one resource once and it only introduces one extra memory fetch.

And don’t put too much data in root signature, because d3d runtime will version it under the hood. The specific detail is not revealed, however that should be the reason developers don’t need to maintain root signature’s lifetime before the draw call is executed on GPU. Another thing to be noted is to reduce changes in root signature. Each change will trigger some cost in the runtime and driver. Change it only if it is necessary.

## Pipeline State Object:

A single PSO almost captures all of the hardware states except those ones that are easy to be set, like view port and scissor rect. It usually needs to be created during initialization. There are some benefits by introducing PSO:

- Shader compiling will be done after PSO is created. There won’t be any shader recompiling that stalls the graphics pipeline during rendering. On some old hardware without ROPs, switching between different blend states may even trigger shader recompile.
- There are usually several states to be set before issuing a draw call and those hardware instructions used to be generated on the fly in rendering loop, which take some CPU cycles. With PSO, all of the hardware instructions could be pre-baked during initialization.
- A lot of validation work needs to be done right before issuing a draw call, for example checking if the bound textures are valid ones. They are gone now.

There are something deserve our attention when using PSO:

- Create them on separate threads to avoid stalling rendering.
- Use default values for fields that we don’t care. Most of game engines have their high level cache of PSO, setting default values for don’t-care field will also result in better cache hit rate.
- Avoid frequent switching hardware states by using similar PSOs among successive draw calls.

# Draw Call Issuing

There are also some dramatic changes going on in the draw call execution model between 11 and 12.

11 is pretty simple, we want to issue a draw call or other API call, we feed it to the immediate context. Of course it doesn’t mean that the draw call is performed by GPU immediately, however it does return immediately, the command will be buffered for later execution. A big disadvantage is that immediate context is not thread-safe. There is no way to submit draw calls across multiple threads. 11 tried to distribute CPU overhead across multiple cpu cores through the introduction of deferred context. Although we can submit more draw calls through the deferred context in another thread, most of the heavy lifting is still done in one single thread, the main rendering thread which immediate context is working. It doesn’t work too well, no where near what d3d12 brings.

12 solved the issue in a perfect way. There is no immediate context anymore. What we have now is a brand new method for submitting draw calls.

There is command queue. More like a low level concept which used to exist in drivers. There are three types, graphics, compute and copy queue. Each is a super set of the following one. The graphics command queue can perform any kind of method, draw calls, dispatch calls and copy commands. The compute queue can’t do any graphics command and copy queue can only perform copy instructions. We can have multiple command queues available in our program. The hardware may overlap some operations if possible.

Let’s focus on graphics queue. The draw calls can’t be put in the command queue directly. Command queue only takes in command list. A command list is a bunch of commands to be executed by GPU, we can record the command list by submitting draw calls to it. And command list is thread-safe. That said we can allocate many command lists and each one of them is handled in a separate thread. In that way we can do the real multi-thread rendering which will distribute the cpu overhead during command recording across multiple cpu cores. Recording of command lists takes most of the time and executing them on a command queue doesn’t take much cpu overhead on CPU. And we don’t need to generate the command lists in the same order they are submitted.

If something is visible in this frame, it is highly possible that it will be available in the next frame except that it may be in different position. However the set of commands of generating it could be exactly the same, only some constant data, such as view matrix, is changed. So we waste a big amount of time to do something that we’ve already done in the previous frame. Bundle tries to solve the problem by pre-baking all of the hardware instructions for certain number of draw calls, which is usually 10+. Bundle behaves like a smaller version of command list and it should be reusable across frames, not intend to regenerate every frame.

# Summary

This post only summarize some of the important changes introduced in D3D12. It doesn’t cover all of the changes. There are things like conservative rasterization, raster ordered view and a bunch of other fancy graphics features introduced in D3D12 too.

Comparing with its predecessor, D3D12 brings a lot more flexibility, which comes along with lots of responsibility. And similar APIs, like Vulkan, Metal, share a common way of how modern graphics API works.

# References

[1] [Advanced DirectX12 Graphics And Performance](http://schedule.gdconf.com/session/advanced-directx12-graphics-and-performance-presented-by-microsoft)

[2] [Better Game, Better Performance : Your Game on DirectX12](http://schedule.gdconf.com/session/better-power-better-performance-your-game-on-directx12-presented-by-microsoft)

[3] [Direct3D12 API Preview](https://channel9.msdn.com/Events/Build/2014/3-564)

[4] [Approaching Zero Driver Overhead](http://gdcvault.com/play/1020791/)

[5] [Getting the best out of Direct3D12](http://amd-dev.wpengine.netdna-cdn.com/wordpress/media/2012/10/Getting-the-best-out-of-D3D12.ppsx)

[6] [Direct3D12 A new Meaning and Efficiency for Performance](http://amd-dev.wpengine.netdna-cdn.com/wordpress/media/2012/10/D3D12-A-new-meaning-for-efficiency-and-performance.ppsx)