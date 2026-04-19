---
title: A Comparison of Modern Graphics APIs
url: https://alain.xyz/blog/comparison-of-modern-graphics-apis
author: Alain Galvan
published: '2021-01-31'
source_blog: Alain Galvan · Ray Tracing Driver Engineer at AMD
source_site: https://alain.xyz/
category: graphics
fetched: '2026-04-19'
---

Low level Graphics APIs such as **Vulkan**, **DirectX**, **Metal**, and **WebGPU**, are converging to a model similar to the way GPUs are currently built. Graphics Processing Units (GPUs) are asynchronous compute units that can handle large quantities of data, such as complex mesh geometry, image textures, output frame buffers, transformation matrices, or anything you want computed.

GPUs weren't always like this, originally they were a set of fixed hardware based functions with very little programmability. This changed as applications pushed the limits of what these non-programmable systems could do, which warranted a race between GPU manufacturers and application developers constantly pushing the limits of their design [[Peddie 2023]](https://alain.xyz#ref_peddie2023). Frame buffers and rasterizers [[Fatahalian 2018]](https://alain.xyz#ref_fatahalian2018) lead to programable shaders, General Purpose GPU (GPGPU) computing, and recently the addition of hardware for ray traversal acceleration and tensor processing for AI. Graphics APIs have evolved right alongside these changes with additions to the fixed graphics pipeline, compute shaders, and more recently ray traversal functionality (DirectX 12 and Vulkan Ray Tracing).

Let's look at some of the similarities and differences between graphics APIs. We'll be covering the C++ APIs for:

🌋 Vulkan

❎ DirectX 12.x

✖️ DirectX 11.x

🤖 Metal

🕸️ WebGPU

⚪ OpenGL

**OpenGL**'s design originated during the early days of computer graphics and was designed as a state machine, so its interface differs greatly from modern graphics APIs. **DirectX 11**, while closer to modern GPU architectures than OpenGL, tries to be easy for developers by delegating tasks that Vulkan, DirectX 12, and Metal currently leave the developer responsible for to the driver. [[Russell 2014]](https://alain.xyz#ref_russell2014)

It is useful to be aware of the legacy of modern graphics APIs so they are mentioned where relevant.

A graphics application normally follows the following order of execution no matter the API:

**Initializing the API** - Creating the core data structures needed to access the inner workings of the API.

**Loading Assets** - Creating the data structures needed to load things like shaders, describe the graphics pipeline, create and populate commands buffers for the GPU to execute, and send resources to GPU exclusive memory.

**Updating Assets** - Update any uniforms to your shader and perform application level logic here.

**Presentation** - Send your list of command buffers to your command queue and present your swapchain.

**Repeat 2, 3, and 4** until a signal from the application to close.

**Destroy** - Wait for the GPU to finish any remaining work, and destroy all data structures and handles.

Thus we'll be following the creation and use of Graphics API data structures in this order.

![Dependencies Example](../../assets/d2a4be1714e93a44.gif)


| API | Structure |
|---|---|
| Vulkan | `#include <vulkan/vulkan.hpp>` |
| DirectX 12 | `#include <d3d12.h>` |
| DirectX 11 | `#include <d3d11.h>` |
| Metal | `#import <Metal/Metal.h>` |
| WebGPU | Requires
|
| OpenGL | Varies by OS |

When starting a new application you need to include any dependencies you have to external APIs, and graphics APIs are no different. Depending on the API, you may also need other libraries in your project such as a shader compiler.

**OpenGL** stands out as the exception to every other graphics API, in that depending on the operating system and your personal setup, there can be a [variety of imports from different locations](https://github.com/alaingalvan/CrossWindow-Graphics/blob/master/src/CrossWindow/Graphics/OpenGL.h#L24).

| API | Structure |
|---|---|
| Vulkan | `#include "glslang/Include/revision.h"` |
| DirectX 12 | `#include <D3Dcompiler.h>` |
| DirectX 11 | `#include <D3Dcompiler.h>` |
| Metal | `#import <Metal/Metal.h>` |
| WebGPU | N/A |
| OpenGL | `void glShaderSource(...)` |

**Vulkan** requires that you use an external shader compiler that generates SPIR-V such as [glslang](https://github.com/KhronosGroup/glslang) or the [DirectX Shader Compiler](https://github.com/microsoft/DirectXShaderCompiler/wiki/SPIR%E2%80%90V-CodeGen).

For **DirectX**, It's recommended that you use the [DirectX Shader Compiler](https://github.com/microsoft/DirectXShaderCompiler) rather than the included compiler since it supports newer shader model versions and more optimizations and speed.

**Metal** shaders can be compiled at runtime or compiled at build time with the `metallib`

command line tool included in your MacOS path.

**OpenGL** doesn't require an external library to compile shaders since it's included with the library, though it also supports SPIR-V as an optional alternative to GLSL with OpenGL 4.6.

**WebGPU** shaders are plaintext strings, so there's no need to compile them, though it is a good idea to strip whitespace and minify/mangle symbols for production.

For a comparison of shader languages,

[visit my blog post reviewing shader languages.]

| API | Structure |
|---|---|
| Vulkan | `vk::Instance` |
| DirectX 12 | `IDXGIFactory4` |
| DirectX 11 | `IDXGIFactory` |
| Metal | `CAMetalLayer` |
| WebGPU | `GPU` |
| OpenGL | Varies by OS |

The entry point to a graphics API generally allows you to access the API's inner classes.

**Vulkan**'s entry point involves choosing what version of the API you intend to use as well as any extensions or layers you want, such as error checking, window surfaces, etc.

**DirectX 11** and **12** requires that you create a **Factory**, and optionally a **Debug** data structure.

On **Metal**, an `NSWindow`

is required to have an `NSView`

with a `CAMetalLayer`

in it (which is a part of QuartzCore). Once a layer exists and is attached to a window, that window can use the rest of the Metal API.

For **OpenGL**, the closest thing to an entry point is an operating system specific *Context* that you can request for after creating an OS Window.

| API | Structure |
|---|---|
| Vulkan | `vk::PhysicalDevice` |
| DirectX 12 | `IDXGIAdapter1` |
| DirectX 11 | `IDXGIAdapter` |
| Metal | `MTLDevice` |
| WebGPU | `GPUAdapter` |
| OpenGL | `glGetString(GL_VENDOR)` |

**Physical Devices** allow you to query for important device specific details such as memory size and feature support.

**Metal** is the only outlier here since both the physical and logical device are shared by the same data structure.

**OpenGL** cannot query for any device details unless you use a manufacturer exclusive extension. You can get some miscellaneous data though like the driver vendor name, renderer, and OpenGL version.

| API | Structure |
|---|---|
| Vulkan | `vk::Device` |
| DirectX 12 | `ID3D12Device` |
| DirectX 11 | `ID3D11Device` |
| Metal | `MTLDevice` |
| WebGPU | `GPUDevice` |
| OpenGL | N/A |

A **Device** gives you access to the core inner functions of the API, such as creating graphics data structures like textures, buffers, queues, pipelines, etc. This type of data structure is the same for the most part across all modern graphics APIs with very few changes between them.

**Vulkan** and **DirectX 12** offer control over memory via creating memory data structures via a device.

| API | Structure |
|---|---|
| Vulkan | `vk::Queue` |
| DirectX 12 | `ID3D12CommandQueue` |
| DirectX 11 | `ID3D11DeviceContext` |
| Metal | `MTLCommandQueue` |
| WebGPU | `GPUQueue` |
| OpenGL | N/A |

A **Queue** allows you to enqueue tasks for the GPU to execute. A GPU is an asynchronous compute device, so the idea here is to always keep it busy while having control over when items are added to the queue.

**Vulkan** queues require you to specify what queues the device will use before even creating it.

| API | Structure |
|---|---|
| Vulkan | `vk::CommandPool` |
| DirectX 12 | `ID3D12CommandAllocator` |
| DirectX 11 | `ID3D11DeviceContext` |
| Metal | `MTLCommandQueue` |
| WebGPU | `GPUDevice` |
| OpenGL | N/A |

A **Command Pool** is a data structure that allows you to create command buffers.

**Metal** stands out by having the queue also be the data structure from which to allocate command buffers.

| API | Structure |
|---|---|
| Vulkan | `vk::Surface` |
| DirectX 12 | `ID3D12Resource` |
| DirectX 11 | `ID3D11Texture2D` |
| Metal | `CAMetalLayer` |
| WebGPU | `GPUCanvasContext` |
| OpenGL | Varies by OS |

A window **Surface** allows you to bind all draw calls to an OS specific window.

On **DirectX**, since there's only Windows / Xbox as targets for the API, the closest thing to a surface is the texture back buffer you receive from a swapchain. A swapchain receives your window handle and from there it'll create a surface internal to the DirectX driver.

Since MacOS and iOS windows feature a hierarchical structure where an Application contains a View, which can contain a layer, the closest thing to a surface in **Metal** is either a metal layer or view that wraps it.

| API | Structure |
|---|---|
| Vulkan | `vk::Swapchain` |
| DirectX 12 | `IDXGISwapChain3` |
| DirectX 11 | `IDXGISwapChain` |
| Metal | `CAMetalDrawable` |
| WebGPU | `GPUCanvasContext` |
| OpenGL | Varies by OS |

A **Swapchain** flips between different back buffers for a given window, and controls aspects of rendering such as refresh rate and back buffer swapping behavior.

**Metal** and **OpenGL** stands out here in that the API lacks the idea of a swapchain, leaving that to the OS windowing API instead.

| API | Structure |
|---|---|
| Vulkan | `vk::Framebuffer` |
| DirectX 12 | `ID3D12Resource` |
| DirectX 11 | `ID3D11RenderTargetView` |
| Metal | `MTLRenderPassDescriptor` |
| WebGPU | `GPURenderPassDescriptor` |
| OpenGL | `GLuint` |

**Frame Buffers** Are groups of output textures used during a raster based graphics pipeline execution as outputs.

**DirectX 12 and 11** don't feature an explicit data structure for this per say, rather you can pass a set of Views.

| API | Structure |
|---|---|
| Vulkan | `vk::Image & vk::ImageView` |
| DirectX 12 | `ID3D12Resource` |
| DirectX 11 | `ID3D11Texture2D` |
| Metal | `MTLTexture` |
| WebGPU | `GPUTexture & GPUTextureView` |
| OpenGL | `GLuint` |

**Textures** are arrays of data that store color information, and serve as inputs/outputs for rendering. Vulkan, DirectX 12, and WebGPU introduce the idea of having multiple views of a given texture that can view that texture in different encoded formats or color spaces. Vulkan introduces the idea of managed memory for Images and buffers, thus a texture is a triplet of an *Image*, *Image View* when used (there can be multiple of these), and *Memory* in either device only or in CPU-GPU accessible space.

For a more traditional way of managing memory in Vulkan, I would highly recommend the [AMD Vulkan Memory Allocator](https://gpuopen.com/vulkan-memory-allocator/). For DirectX 12 the same authors released the [AMD D3D12 Memory Allocator](https://gpuopen.com/d3d12-memory-allocator/).

| API | Structure |
|---|---|
| Vulkan | `vk::Buffer & vk::BufferView` |
| DirectX 12 | `ID3D12Resource` |
| DirectX 11 | `ID3D11Buffer` |
| Metal | `MTLBuffer` |
| WebGPU | `GPUBuffer & GPUBufferView` |
| OpenGL | `GLuint` |

A **Buffer** is an array of data, such as a mesh's positional data, color data, index data, etc. Similar rules for images apply to buffers in Vulkan and WebGPU.

| API | Structure |
|---|---|
| Vulkan | `vk::ShaderModule` |
| DirectX 12 | `ID3DBlob` |
| DirectX 11 | `ID3D11VertexShader or ID3D11PixelShader` |
| Metal | `MTLLibrary` |
| WebGPU | `GPUShaderModule` |
| OpenGL | `GLuint` |

A **Shader** tends to be a handle to a compiled blob of shader (HLSL, GLSL, MSL, etc.) code to be fed to a given Pipeline.

| API | Structure |
|---|---|
| Vulkan | `vk::PipelineLayout & vk::DescriptorSet` |
| DirectX 12 | `ID3D12RootSignature` |
| DirectX 11 | `ID3D11DeviceContext::VSSetConstantBuffers(...)` |
| Metal | `[MTLRenderCommandEncoder setVertexBuffer: uniformBuffer]` |
| WebGPU | `GPUPipelineLayout` |
| OpenGL | `GLint` |

Most modern graphics APIs feature a binding data structure to help connect uniform buffers and textures to graphics pipelines that need that data. Metal is unique in that you can bind uniforms with `setVertexBuffer`

in a command encoder, making it much easier to architect compared to Vulkan, DirectX 12, and WebGPU.

| API | Structure |
|---|---|
| Vulkan | `vk::Pipeline` |
| DirectX 12 | `ID3D12PipelineState` |
| DirectX 11 | Various State Calls |
| Metal | `MTLRenderPipelineState` |
| WebGPU | `GPURenderPipeline` |
| OpenGL | Various State Calls |

**Pipelines** are an overarching description of what will be executed when performing a raster draw call, compute dispatch, or ray tracing dispatch.

[DirectX 11](https://docs.microsoft.com/en-us/windows/win32/api/d3d11/nf-d3d11-id3d11devicecontext-rssetstate) and OpenGL are unique here where they don't have a dedicated object for the graphics pipeline, but instead use calls to set the pipeline state in between executing draw calls.

| API | Structure |
|---|---|
| Vulkan | `vk::CommandBuffer` |
| DirectX 12 | `ID3D12GraphicsCommandList` |
| DirectX 11 | `ID3D11DeviceContext` |
| Metal | `MTLRenderCommandEncoder` |
| WebGPU | `GPUCommandEncoder` |
| OpenGL | Intenal to Driver or with `GL_NV_command_list` |

A **Command Buffer** is an asynchronous computing unit, where you describe procedures for the GPU to execute, such as draw calls, copying data from CPU-GPU accessible memory to GPU exclusive memory, and set various aspects of the graphics pipeline dynamically such as the current scissor.

Previously you would declare what you wanted the GPU to execute procedurally and it would do those tasks, but GPUs are inherently asynchronous, so the driver would have been responsible for figuring out when to schedule tasks to the GPU.

| API | Structure |
|---|---|
| Vulkan | `vk::SubmitInfo` |
| DirectX 12 | `ID3D12CommandList[]` |
| DirectX 11 | `ID3D11CommandList` |
| Metal | `MTLCommandBuffer` |
| WebGPU | `GPUCommandEncoder[]` |
| OpenGL | Intenal to Driver or with `GL_NV_command_list` |

**Command Lists** are groups of command buffers pushed in batches to the GPU. The reason for doing this is to keep the GPU constantly busy, leading to less de-synchronization between the CPU and GPU [[Foley 2015]](https://alain.xyz#ref_foley2015).

| API | Structure |
|---|---|
| Vulkan | `vk::Fence` |
| DirectX 12 | `ID3D12Fence` |
| DirectX 11 | `ID3D11Fence` |
| Metal | `MTLFence` |
| WebGPU | N/A |
| OpenGL | `glFenceSync` |

**Fences** are objects used to synchronize the CPU and GPU. Both the CPU and GPU can be instructed to wait at a fence so that the other can catch up. This can be used to manage resource allocation and deallocation, making it easier to manage overall graphics memory usage. [[Satran et al. 2018]](https://alain.xyz#ref_satran2018)

| API | Structure |
|---|---|
| Vulkan | `vkCmdPipelineBarrier` |
| DirectX 12 | `D3D12_RESOURCE_BARRIER` |
| DirectX 11 | N/A |
| Metal | `MTLFence` |
| WebGPU | N/A |
| OpenGL | `glMemoryBarrier` |

A more granular form of synchronization, inside command buffers. Hans-Kristian Arntzen wrote an [article on synchronization in Vulkan that's worth a look](https://themaister.net/blog/2019/08/14/yet-another-blog-explaining-vulkan-synchronization/).

| API | Structure |
|---|---|
| Vulkan | `vk::Semaphore` |
| DirectX 12 | `HANDLE` |
| DirectX 11 | `HANDLE` |
| Metal | `dispatch_semaphore_t` |
| WebGPU | N/A |
| OpenGL | Varies by OS |

**Semaphores** are objects used introduce dependencies between operations, such as waiting before acquiring the next image in the swapchain before submitting command buffers to your device queue.

Vulkan is unique in that semaphores are a part of the API, with [DirectX](https://docs.microsoft.com/en-us/windows/win32/direct3d12/user-mode-heap-synchronization) and [Metal](https://developer.apple.com/documentation/metal/synchronization/synchronizing_cpu_and_gpu_work) delegating that to OS calls.

Each graphics API can have different defaults for axis direction, NDC coordinate direction, matrix alignment, texture alignment, and more, for the most part this isn't much of an issue, and you'll just have to flip a `y`

value in your UVs in your fragment shader.

| API | Structure |
|---|---|
| Vulkan | `Bottom Left` |
| DirectX 12 | `Top Left` |
| DirectX 11 | `Top Left` |
| Metal | `Top Left` |
| WebGPU | `Bottom Left` |
| OpenGL | `Bottom Left` |

DirectX uses the upper [left corner for pixel space coordinates](https://docs.microsoft.com/en-us/windows/win32/direct3d10/d3d10-graphics-programming-guide-resources-coordinates), as does most close source APIs, with open source opting to use the bottom left.

While each of these APIs have their subtle differences, they are extremely close to one another in design. It's up to library architects to decide on where the limits to their desired API surface area are, be it concise and simple like Metal/WebGPU, complex like Vulkan.

Here's a few frameworks, libraries, and blog posts focused on graphics api abstractions in no particular order:

[Alex Tardif](https://twitter.com/longbool)'s [Opinionated Post on Modern Rendering Abstraction Layers](http://alextardif.com/RenderingAbstractionLayers.html)

Gijs Richard Kaerts ([@BelgianRenderer](https://twitter.com/BelgianRenderer)) released his [musings on cross-platform graphics engine architectures here](http://www.gijskaerts.com/wordpress/?p=98).

Andre Weissflog ([@FlohOfWoe](https://twitter.com/flohofwoe)) wrote [Sokol](https://github.com/floooh/sokol/blob/master/sokol_gfx.h), an [STB (eg. stb_image.h)](https://github.com/nothings/stb/blob/master/docs/stb_howto.txt) style cross platform rendering library, with his

[Branimir Karadzic](https://twitter.com/bkaradzic)'s [bgfx](https://github.com/bkaradzic/bgfx) library.

[Dawn](https://dawn.googlesource.com/dawn) is a WebGPU implementation that uses DirectX 12, Metal, Vulkan, or OpenGL as a possible backend.

[Dzmitry Malyshau](https://github.com/kvark)'s [gfx](https://github.com/gfx-rs/gfx), a rust abstraction library.

NVIDIA's GameWorks division released [Falcor](https://github.com/NVIDIAGameWorks/Falcor), a research framework with a thin abstraction over Vulkan and DirectX 12.

NVIDIA's [Alexey Panteleev (@more_fps)](https://twitter.com/more_fps), [Neil Bickford](https://neilbickford.com/) ([@neilbickford](https://twitter.com/neilbickford)) et al. also released the [NVIDIA Render Hardware Interface (NVRHI)](https://github.com/NVIDIAGameWorks/nvrhi), an abstraction layer on top of Vulkan/DirectX 12/11.

Wolfgang Engel ([@wolfgangengel](https://twitter.com/wolfgangengel)) and his team released [The Forge](https://github.com/ConfettiFX/The-Forge), a cross platform rendering framework that supports DirectX 12, 11, Metal, or Vulkan.

For a look at the driver level, some vendors release aspects of what the driver does under the hood with these calls:

For more details on each of the APIs discussed, here's their specification pages:

In addition, you can find specific posts on every graphics API here:

| [Peddie 2023] |
| [Fatahalian 2018] |
| [Russell 2014] |
| [Foley 2015] |
| [Satran et al. 2018] |