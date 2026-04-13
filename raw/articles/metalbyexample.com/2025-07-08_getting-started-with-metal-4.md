---
title: Getting Started with Metal 4
url: https://metalbyexample.com/metal-4/
published: '2025-07-08'
source_blog: Metal by Example
source_site: https://metalbyexample.com
category: graphics
fetched: '2026-04-13'
---

[Another WWDC](https://developer.apple.com/wwdc25/) is in the books, and with it came a major update to many platform technologies, including Metal. Metal graduated to version number 4, and in this article, we’ll explore the core features of Metal 4 as they pertain to rendering.

It’s important to state up-front that this article will not cover Metal 4 comprehensively, as many of the new features only make sense in the context of sophisticated use cases. Instead, this is more of a guide for adopting Metal 4 in existing rasterization-based engines. I recommend consulting [WWDC 2025’s videos](https://developer.apple.com/wwdc25/sessions-and-labs/session-videos?q=Metal) and accompanying [sample code](https://developer.apple.com/metal/sample-code/) and documentation to discover the full extent of Metal 4’s potential.


The sample code for this article is available on GitHub [here](https://github.com/metal-by-example/metal-4-basics). It implements a small physically based renderer while keeping things as simple as possible to demonstrate Metal 4 APIs. The material model is heavily inspired by [glTF’s PBR materials](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html#materials-overview). The tropical setting, if not the lighting and material fidelity, has a sort of *Far Cry 3* feel to it.

![A screenshot of the sample app that accompanies this article. It shows a tropical island setting, with the focal point being a treasure chest filled with gold](../../assets/d05761ab01dbf270.png)

Building and running the sample requires Xcode 26 and a Mac or iOS device running version 26 of their respective OS. These releases are in early beta at the time of this writing, and some APIs may change between now and their release in the fall of 2025.

## Core API Redux

The most immediate thing that stands out when browsing the [documentation](https://developer.apple.com/documentation/Metal/understanding-the-metal-4-core-api) is the `MTL4`

prefix on many of the types. These new types augment and in some cases fully supplant older `MTL`

-prefixed types. For instance, the `MTL4RenderPipelineDescriptor`

type looks very similar to the `MTLRenderPipelineDescriptor`

type introduced in Metal 1, and indeed it serves the same basic purpose, but the details of pipeline creation have changed significantly.

We’ll see below how to use the revamped render pipeline descriptor type, `MTL4RenderPipelineDescriptor`

, but to start, we need to look at how function creation has changed.

### Function Descriptors

Function descriptors are now mandatory in Metal 4. To create a function from a `MTLLibrary`

, you start with a `MTL4LibraryFunctionDescriptor`

, populating its `name`

and `library`

properties.

let functionDescriptor = MTL4LibraryFunctionDescriptor() { functionDescriptor.name = "function_name" functionDescriptor.library = library

Since the various function descriptor types don’t have parameterized initializers, this can get verbose. I recommend adding extensions to reduce function descriptor boilerplate. See the sample code for details.

To create specialized functions using Metal function constants, we need to wrap an existing function descriptor in a `MTL4SpecializedFunctionDescriptor`

. This type uses the existing `MTLFunctionConstantValues`

type to populate function constants, which can be used to enable or disable features in shaders or supply values at compile-time.

let functionConstants = MTLFunctionConstantValues() functionConstants.setConstantValue(&someBoolValue, type: .bool, withName: "someCompileTimeFlag") let specializedFunction = MTL4SpecializedFunctionDescriptor() specializedFunction.functionDescriptor = functionDescriptor specializedFunction.constantValues = functionConstants

### The `MTL4Compiler`

Interface

In Metal 4, shader compilation is performed with a compiler object rather than via the device interface. The `MTL4Compiler`

interface has numerous methods for pipeline creation and also supports pipeline serialization, to reduce app startup time.

Although you can still use older APIs to create shader libraries from source, the `MTL4Compiler`

interface provides a new method, `makeLibrary(descriptor:)`

, taking an instance of `MTL4LibraryDescriptor`

, to perform this task. Although it is preferable to precompile shaders into libraries or device-specific binary archives, sometimes you still need to compose shader strings at runtime.

You create a compiler with a Metal device, passing a compiler descriptor (which can be used to supply serialization options beyond the scope of this article).

let compilerDescriptor = MTL4CompilerDescriptor() let compiler = try device.makeCompiler(descriptor: compilerDescriptor)

### Render Pipeline Creation

Creating a render pipeline starts as usual with a render pipeline descriptor. The `MTL4RenderPipelineDescriptor`

type is very similar to the earlier `MTLRenderPipelineDescriptor`

type with a few notable differences.

let renderPipelineDescriptor = MTL4RenderPipelineDescriptor()

Render pipeline descriptors still take function objects, but as mentioned above, these are function descriptors rather than instances of `MTLFunction`

.

renderPipelineDescriptor.vertexFunctionDescriptor = vertexFunction renderPipelineDescriptor.fragmentFunctionDescriptor = fragmentFunction

Various other properties like `vertexDescriptor`

and `rasterSampleCount`

are unchanged.

renderPipelineDescriptor.vertexDescriptor = vertexDescriptor renderPipelineDescriptor.rasterSampleCount = 4 // enable 4x MSAA

Color attachments have been revamped with the new `MTL4RenderPipelineColorAttachmentDescriptor`

type. Configuring the pixel format is the same as before.

renderPipelineDescriptor.colorAttachments[0].pixelFormat = colorPixelFormat

However, many properties related to the treatment of the alpha channel have switched from being raw Booleans to using enums, perhaps for readability or extensibility. For instance, to enable alpha blending on a color attachment, one sets its `blendingState`

to `.enabled`

.

renderPipelineDescriptor.colorAttachments[0].blendingState = .enabled

The remainder of blending factor and operation configuration is unchanged.

Interestingly, there are no depth attachment descriptors in Metal 4. Metal 4 render pass descriptors can, of course, have depth and stencil attachments, but their pixel formats no longer have to be specified up-front.

Finally, to create a render pipeline state, we call the `makeRenderPipelineState`

method on our compiler.

let renderPipelineState = try compiler.makeRenderPipelineState(descriptor: renderPipelineDescriptor)

As in all prior versions of Metal, this render pipeline state can be set on a render command encoder to configure the pipeline to that state before drawing primitives.

## Residency Sets

Introduced in Metal 3.2 (the 2024 release), residency sets give developers greater control over which resources are available to GPU commands. As of Metal 4, residency sets are the only way to signal that a resource should be made resident, so they are more essential than before. Apple has spectacular documentation on residency sets [here](https://developer.apple.com/documentation/metal/mtlresidencyset).

A residency set is a collection of resources that can be made resident in a particular scope. For instance, to make a set of resources available to all of the command buffers committed to a command queue, call the `MTL4CommandQueue`

protocol method `addResidencySet(_:)`

. At a more granular level, you can add a residency set to a single command buffer with the `useResidencySet(_:)`

and `useResidencySets(_:)`

APIs on the `MTL4CommandBuffer`

protocol.

But how do we create and manage residency sets in the first place? `MTLResidencySetDescriptor`

allows you to specify an initial capacity for the residency set, in case you happen to know in advance how many resources it will reference.

let residencyDescriptor = MTLResidencySetDescriptor() residencyDescriptor.initialCapacity = 16

Creating a residency set is then as simple as asking for one from the device:

let residencySet = try device.makeResidencySet(descriptor: residencyDescriptor)

Resources are made resident or non-resident in a two-step process. A resource is made resident by calling the `addAllocation(_:)`

method, and a set of resources can be made resident at once with `addAllocations(_:)`

. Then, calling the `commit()`

method makes the allocations in the residency set resident for subsequent commands on the queue or buffer to which the residency set is attached. You can remove an allocation by calling the `removeAllocation(_:)`

and committing again. A resource only becomes nonresident when it is not contained in any attached residency set (i.e. the set of resident resources is the **union** of all attached residency sets in a particular scope).

## Argument Tables

As a concept, argument tables have existed in Metal since its inception. The argument table is what you manipulate by calling APIs like `setVertexBuffer(_:offset:index:)`

on a command encoder. It’s the “glue” between resources at the API level and the parameters of shader functions.

Prior to Metal 2.0, there was a one-to-one mapping between shader arguments and resources. Over time, Metal’s binding model has become more flexible, first with the introduction of argument buffers, then with Metal 3’s greatly expanded support for [bindless use cases](https://developer.apple.com/videos/play/wwdc2022/10101).

In Metal 4, argument tables are objects that you create and work with explicitly.

To create an argument table, you first create an argument table descriptor. Descriptors require you to specify the maximum counts of resources (textures and buffers) that can be bound to the argument table. For example:

let argumentDescriptor = MTL4ArgumentTableDescriptor() argumentDescriptor.maxBufferBindCount = 16 argumentDescriptor.maxTextureBindCount = 16

Then, to create an argument table, you call the `device.makeArgumentTable(descriptor:)`

method. You should create a different argument table for each pipeline stage, as the resources required by the vertex and fragment function likely differ.

let argumentTable = try device.makeArgumentTable(descriptor: argumentDescriptor)

Binding resources to an argument table is somewhat different from binding resources to a render command encoder. In the case of textures, you bind the `resourceID`

of the texture, which is a 64-bit unique identifier.

argumentTable.setTexture(someTexture.gpuResourceID, index: 0)

Argument indices are the same as before: they correspond to the attributes (`[[buffer(n)]]`

or `[[texture(n)]]`

) on shader parameters in MSL:

fragment float4 fragment_main( FragmentIn in [[stage_in]], // ... texture2d<float, access::sample> someTexture [[texture(0)]])

To bind a buffer to an argument table, you pass its `gpuAddress`

:

argumentTable.setAddress(someBuffer.gpuAddress, index: 0)

It isn’t immediately obvious how to bind a buffer at an offset, which is a common use case when you use a single buffer to store chunks of data that can be accessed separately. It turns out you can just add the offset to the GPU address to form a pointer of sorts to the offset region:

argumentTable.setAddress(someBuffer.gpuAddress + UInt64(myOffset), index: 0)

The sample code uses a lightweight `BufferView`

type to abstract the notion of an untyped region of a buffer that can provide its own GPU address. This is used to suballocate portions of a uniform buffer for storing per-instance data and material [argument buffers](https://developer.apple.com/documentation/metal/improving-cpu-performance-by-using-argument-buffers).

## Command Submission Redux

At the heart of the Metal 4 update is an all-new approach to command encoding. Command buffers, which used to be “fire-and-forget,” transient objects that were recreated every frame, can now be long-lived objects. Command buffers still act as parcels of encoded commands that can be committed to the GPU for execution, but they no longer manage their own memory. Instead, in Metal 4, *command allocators* move this responsibility onto the application, giving you more control over command memory management.

### Command Buffers and Command Allocators

To create a command buffer, you call the new `makeCommandBuffer()`

API on `MTLDevice`

(instead of the API with the same name on `MTLCommandQueue`

). The result is an object that conforms to `MTL4CommandBuffer`

. Similarly, to make a command allocator, you call the `makeCommandAllocator()`

API on a device.

Command buffers and command allocators can be created up-front and retained for the lifetime of your renderer. However, command allocators cannot be reused while the commands they encoded are in-flight. For this reason, you should create a pool of command allocators and only begin reusing them once the commands they encoded have completed execution on the GPU.

Also, command buffers no longer retain references to resources by default, so it is now crucial for your application to ensure that any resource referenced by a command stays alive until that command finishes on the GPU.

When you are ready to start encoding commands for a frame, you retrieve a command allocator from the pool and call its `reset()`

method; this frees the previously encoded commands and make their memory available to be overwritten with new commands.

To start encoding commands into an existing command buffer, you call the `beginCommandBuffer(allocator:)`

method on the target command buffer. This creates a link between the command buffer and the allocator, which will be used by any command encoders subsequently created on the command buffer.

### Render Command Encoders

The Metal 4 render pass descriptor and render command encoder APIs are very similar to the existing interfaces. Calling `makeRenderCommandEncoder(descriptor:)`

on a command buffer returns a `MTL4RenderCommandEncoder`

which can encode a render pass. `MTKView`

has a new `currentMTL4RenderPassDescriptor`

property that conveniently creates and populates a new-style render pass descriptor for you. As always, this descriptor holds render targets and load/store actions in attachments.

guard let renderPassDescriptor = view.currentMTL4RenderPassDescriptor else { return } let commandEncoder = commandBuffer.makeRenderCommandEncoder(descriptor: renderPassDescriptor)

Metal 4 now allows color attachment mapping, which allows you to change render targets in the middle of a pass, an advanced feature that can be used to consolidate rendering work. Also new in Metal 4, you can *suspend* a render pass at the end of one command buffer and *resume* it in a subsequent command buffer (previously, render passes had to be completed within a single command buffer). We won’t look any more deeply at these advanced features in this article.

Once you have a command encoder in hand, you can attach an argument table to each stage to connect resources to shader parameters.

commandEncoder.setArgumentTable(vertexArgumentTable, stages: .vertex) commandEncoder.setArgumentTable(fragmentArgumentTable, stages: .fragment)

Argument tables can be updated between draw calls; argument table state is effectively copied for each command, so you don’t need to pool argument tables or do any other special state management for your resource bindings to “stick.”

### Command Buffer Submission and Presentation

You no longer use the command buffer itself to commit work or schedule drawable presentation. Instead, these operations are done on the command queue in a three-step process. First, you call the `waitForDrawable(_:)`

method on your rendering command queue. This tells Metal to wait for the drawable to become available before executing any subsequent command buffers. Then you call `commit(_:)`

on the command queue to commit one or more command buffers. Finally, you call `signalDrawable(_:)`

on the command queue to tell Metal that all commands that will render to the drawable have been committed.

After these three steps, you can call `present()`

on the drawable itself, which will tell Metal that once all of the preceding commands have executed, it should be composited by the windowing system.

This little dance may seem complex, but it boils down to just a few lines of code.

guard let drawable = view.currentDrawable else { ... } commandQueue.waitForDrawable(drawable) commandQueue.commit([commandBuffer]) commandQueue.signalDrawable(drawable) drawable.present()

## Events

Our last topic is the growing importance of Metal events. For years, it has been common to use [Dispatch semaphores](https://developer.apple.com/documentation/dispatch/dispatchsemaphore) to control access to resources whose contents need to be preserved while commands execute. With Metal 4’s emphasis on *concurrency by default*, we have a new opportunity to modernize resource access with `MTLEvent`

and specifically with `MTLSharedEvent`

.

Shared events give us a way to coordinate work between the CPU and the GPU: by awaiting a particular value on the CPU and signaling that value from a Metal 4 command queue, we can safely wait for work completion without unduly wasting CPU cycles.

We use a `MTLSharedEvent`

in the sample to wait for the work from three frames back (three being the maximum number of frames we want “in-flight” at once). Before we begin encoding the work for frame *N*, we wait on the value *N-3* by calling the `wait(untilSignaledValue:timeoutMS:)`

method on our event. Then, once we’re done encoding work for the frame, we call the `signalEvent(_:value:)`

method on the command queue, which will signal the event once the preceding commands have executed. Although the main resource we want to synchronize—drawables—have their own internal wait mechanism, there are other resources, like uniform buffers and command allocators, that need to be guarded as well.

## Conclusion

Upgrading to Metal 4 requires that you understand resource management and concurrency on a deeper level than previous versions. Metal 4 being “concurrent by default” means that it’s much easier than before to introduce accidental hazards. We didn’t even scratch the surface of how to use barriers to control access to resources that are modified during rendering, but in multipass rendering, this becomes essential. Also, Metal 4 command buffers do not implicitly retain their resources nor make them resident, meaning explicit management of resource memory and lifetimes is crucial. The main purpose of this article is to introduce the new command submission model, including the new concept of command allocators, as a first step toward adopting Metal 4. I expect best practices and interesting new use cases to proliferate as Metal 4 makes its way out into the world.

MichaelThank you Warren, looking forward to more Metal 4 articles, especially on barriers, events and fences.

We will start to adopt Metal 4 incrementally, but right now, it looks like it will shape up to a gargantuan migration that will take some time and considerable effort.

Stuart CarnieMichael, I’m planning on supporting Metal 4 for Godot 4.x. I wrote the original Metal 3 implementation, and plan to introduce a completely new “driver” for Metal 4 rather than an incremental approach.