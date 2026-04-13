---
title: What’s New in Metal (2019)
url: https://metalbyexample.com/new-in-metal-3/
published: '2019-06-11'
source_blog: Metal by Example
source_site: https://metalbyexample.com
category: graphics
fetched: '2026-04-13'
---

With WWDC 2019 over, it’s a good time to reflect on everything that was announced and start seeing how we can put it into practice. The purpose of this article is to round up the changes to the Metal framework and tools and provide pointers to where you can learn more. This was a banner year, with significant improvements to Metal itself; major advancements in related frameworks like MetalPerformanceShaders (MPS), CoreML, and ARKit; and the exciting introduction of an all-new augmented reality engine, RealityKit.

Since this was such a big year, this post can’t hope to cover all the improvements that are included in macOS 10.15 Catalina and iOS 13. In particular, raytracing with MPS was a hot topic, but you’ll have to look elsewhere for coverage. [This session](https://developer.apple.com/videos/play/wwdc2019/613/) should get you up-to-speed.


## New Family and Version APIs

If you’ve ever used the `MTLFeatureSet`

API, you know that the number of families and versions has grown combinatorially since Metal was introduced. This year’s version of Metal introduces a new way to detect features and determine device capabilities.

To do this, the enumerations for families and versions have been decoupled. You can now ask whether a device supports the features of a particular GPU *family* (`MTLGPUFamily`

) and whether it supports a particular *software version* (`MTLSoftwareVersion`

). Families themselves have been somewhat simplified, such that you can now determine whether a device supports a particular subset of Metal features by asking whether it supports one of the **Common** families. Enumeration cases also exist for each generation of Apple GPU and groupings of GPUs that have been included in various Macs over the years.

The [ Modern Rendering with Metal](https://developer.apple.com/videos/play/wwdc2019/601/) session is worth watching in its entirety, but especially start watching from 46:05 to catch up on these changes in the family and version APIs.

## Debugging and Tools

### Metal Support in Simulator

Since Metal was introduced, the lack of support for running iOS Metal apps in the Simulator has been a major impediment to development and testing. Fortunately, as of Xcode 11 and macOS 10.15, Metal is now fully supported in the simulator.

### Memory Debugger

Xcode’s GPU tools gained a nice new memory debugger, making it much easier to get visibility on how memory is being allocated among your Metal resources.

### Programmatic Frame Capture

Programmatic GPU frame capture is getting a big upgrade this year, with the new ability to write captured data to disk (instead of immediately loading in the Xcode frame debugger). With the introduction of the `MTLCaptureDescriptor`

type, the old `startCapture(:)`

methods taking a device or queue have been deprecated in favor of the new `startCapture(with:)`

method, which takes a descriptor. This descriptor can target a device or queue and can specify a `destination`

of either `.developerTools`

or `.gpuTraceDocument`

. In the latter case, you also supply a file URL to which the capture data is written. This enhancement will make it much easier to capture detailed information during on-device testing.

### Counters

GPU counters have been available in the Xcode GPU tools for awhile, but now, you can now get counter data programmatically on macOS. The command encoder types have a new `sampleCounters(sampleBuffer:sampleIndex:barrier:)`

method for requesting that counter data be written into the provided `MTLCounterSampleBuffer`

.

To determine which statistics are available from a device, you can use the `counterSets`

property of a `MTLDevice`

. You then configure which counters will be sampled by creating a `MTLCounterSampleBufferDescriptor`

and setting its `counterSet`

property to one of the available sets. Then, you use the device’s `makeCounterSampleBuffer(descriptor:)`

method to create a counter sample buffer to which samples can be written.

## Texture Improvements

### 16-bit Depth Textures

16-bit depth textures are an oft-requested feature, and the [ .depth16unorm](https://developer.apple.com/documentation/metal/mtlpixelformat/depth16unorm) pixel format is now available on iOS and tvOS.

Although 16-bit depth buffers obviously offer much less precision than the more common 24- and 32-bit formats, the savings in bandwidth can be significant for those situations where you actually need to retain the contents of the depth buffer across render passes.

[This post](https://mynameismjp.wordpress.com/2010/03/22/attack-of-the-depth-buffer/) by Matt Pettineo has a good overview of the trade-offs of different approaches to depth buffer precision. You can use the embedded tool in [this post](http://dev.theomader.com/depth-precision/) by Theodor Mader to get a sense of how error is distributed when using 16-bit depth.

### sRGB Views on non-sRGB Textures

This change expands the flexibility of texture view format compatibility by allowing you to create sRGB views on non-sRGB textures, and *vice versa*. In the past, this was possible for compressed formats such as BC1 (on macOS) and PVRTC on (iOS), but it’s now possible between additional formats, provided they meet the other criteria for creating a view (primarily that the source and target formats have the same number of bits per pixel). Consult the [documentation on texture views](https://developer.apple.com/documentation/metal/mtltexture/1515598-maketextureview) for more information.

### Cross-Process Texture Sharing

Originally introduced in macOS 10.14, [ MTLSharedTextureHandle](https://developer.apple.com/documentation/metal/mtlsharedtexturehandle) is now available on iOS and tvOS, enabling sharing of textures across processes. After passing such a handle over an XPC connection, you can get an instance of

`MTLTexture`

in the receiving process by calling the `makeSharedTexture(handle:)`

method on the same device by which the original texture was created. Cross-process resources create an opportunity for more efficient apps, considering the proliferation of app extensions since their introduction in iOS 8.### Custom Texture Swizzle

With texture swizzling you can create a texture or texture view that “redirects” each sampled color channel to a different channel in the source image. For example, using a swizzle object initialized as `MTLTextureSwizzleChannels(red: .alpha, green: .red, blue: .green, alpha: .blue)`

would allow you to read an ARGB texture as if its components were in RGBA order.

Consult the documentation for `MTLTextureDescriptor`

‘s new [ swizzle](https://developer.apple.com/documentation/metal/mtltexturedescriptor/3114305-swizzle) property and

`MTLTexture`

‘s [method for more information.](https://developer.apple.com/documentation/metal/mtltexture/3114303-newtextureviewwithpixelformat)

`makeTextureView(pixelFormat:textureType:levels:slices:swizzle:)`

### 3D ASTC Texture on Apple GPUs

ASTC compressed textures have been supported since iOS 9, but iOS 13 brings support for three-dimensional ASTC textures on A8 and more recent Apple GPUs.

### 3D BC Textures on macOS

Similarly, [BC n texture formats](https://docs.microsoft.com/en-us/windows/desktop/direct3d11/texture-block-compression-in-direct3d-11) (also commonly known as DXT formats) have long been supported on the Mac, but macOS 10.15 gains support for 3D BC

*n*formats.

### Defined Behavior for Out-of-Bounds Texture Accesses

Rounding out the texture category, Metal now provides guarantees about behavior during out-of-bounds (OOB) texture reads and writes. Previously, reading or writing outside the bounds of a texture invoked undefined behavior.

Consult section 6.10 of the recently-published [Metal Shading Language (2.2) Specification](https://developer.apple.com/metal/Metal-Shading-Language-Specification.pdf) for details on OOB accesses. For the most part, the behavior is what you’d want, which makes porting from other APIs with defined OOB behavior much easier.

## Indirect Command Buffers

Introduced in iOS 12 and macOS 10.14 last year, indirect command buffers allow commands to be encoded into a buffer from the [CPU](https://developer.apple.com/documentation/metal/advanced_command_setup/encoding_indirect_command_buffers_on_the_cpu) or [GPU](https://developer.apple.com/documentation/metal/advanced_command_setup/encoding_indirect_command_buffers_on_the_gpu); these buffers can be reused in a subsequent frame, reducing the CPU overhead of issuing commands.

### Support for Indirect Compute Commands

At the time of their introduction, indirect command buffers could only contain rendering commands (binding resources and draw calls). The new [MTLIndirectComputeCommand](https://developer.apple.com/documentation/metal/mtlindirectcomputecommand) type enables compute commands to be encoded for indirect execution as well.

### Pipeline State Object Indirection for iOS

Continuing the theme of more powerful indirect command buffers, pipeline state objects can now be set on `MTLIndirectRenderCommand`

objects on iOS, via the [ setRenderPipelineState:](https://developer.apple.com/documentation/metal/mtlindirectrendercommand/2966625-setrenderpipelinestate) method.

### Range Indirection for iOS

Indirect command buffers on iOS can now reference command ranges to dynamically determine which subsets of a command buffer to execute. The [ executeCommands(in:indirectBuffer:indirectBufferOffset:)](https://developer.apple.com/documentation/metal/mtlrendercommandencoder/2967439-executecommandsinbuffer) API on

`MTLRenderCommandEncoder`

has been added to iOS, while the corresponding `executeCommands(in:indirectBuffer:indirectBufferOffset:)`

method has been newly introduced on `MTLComputeCommandEncoder`

.## Heap Improvements

Introduced in 2016, heaps give Metal users more control over resource allocation by allowing suballocating from a block of GPU memory and by allowing resources to alias with one another, potentially reducing the amount of memory required by some techniques.

### User-defined Resource Placement

In prior versions of Metal, heaps have always had “automatic” allocation, meaning the user could not specify the offset in the heap where new resources should be allocated. With the new `MTLHeapTypePlacement`

heap type, and the new `makeBuffer(length:options:offset:)`

and `makeTexture(descriptor:offset:)`

methods on `MTLHeap`

, users can now manually control allocation on both iOS and macOS.

### Heap Resource Tracking

Previously, resources created from a heap required manual synchronization with fences, due to a lack of hazard tracking. With the new `MTLHazardTrackingMode`

enumeration and the `hazardTrackingMode`

property on `MTLHeapDescriptor`

, you can opt in to have Metal track data dependencies among heap-allocated resources.

*Caveat*: According to Apple engineer [Jedd Haberstro](https://twitter.com/jhaberstro/status/1138243132766613504), “this API requires care as all tracking is done at the granularity of the heap. Thus, it is most appropriate for uses cases where all or most of a heap’s sub-allocated resources alias. Else, GPU submissions may serialize in the kernel due to false dependencies.”

## Limit Changes

### Texture Binding Limit on iOS

The number of textures that can be simultaneously bound on iOS has increased from 32 to 94 with iOS 13. Although this limit is somewhat ameliorated by the use of argument buffers, having more argument slots unlocks the potential of techniques that require very large numbers of bound textures with no modification to shaders.

### Varying Count Limit on iOS

The increase in varying count is perhaps more important than the increase in the texture binding slot increase, simply because this limit can’t easily be worked around by “bindless” techniques enabled by argument buffers. In iOS 13, this limit increases to 124 scalars, which means that 31 separate `float4`

vector quantities can be interpolated on their way to your fragment shaders, more than most techniques are likely to ever need.

### Visibility Buffer Size Limit

The maximum visibility result buffer length has been increased from 64KiB to 256KiB for all device families.

### Blit Alignment Rule Relaxation on macOS

With macOS 10.15, blit alignment has been relaxed to match the requirements of A-series GPUs.

## Acknowledgements

Thanks to Caroline Begbie for providing useful feedback on drafts of this article.

Bruce PayanThank you, Warren, for the excellent synopsis of Metal 3.0. It is MUCH appreciated.

Chris LaurelAny info on how to create a 3D ASTC texture in Metal? I don’t see any new formats exposed in the Metal SDK headers.

Also, the latest Metal feature set table shows ‘Line Width’ as a capability supported across all GPU families, but I can’t find anything in the headers about this either. I’d honestly be a bit surprised if this is something that the Apple GPUs support.

Warren MooreThis wouldn’t require new pixel formats to be exposed–there are no “3D pixel formats”. What’s new here is the ability to create 3D (volume) textures that store one of the existing ASTC formats. I assume that implies that asset catalogs and

`MTKTextureLoader`

will also gain support for storing/loading such textures. You’ll likely be able to create them manually by copying data loaded from a container format (such as KTX) using the existing`replaceRegion`

APIs.Chris LaurelSo with the 3D ASTC support in Metal, you’ll just be able to use 3D textures consisting of layers compressed in one of the 2D block sizes? The full spec from ARM defines block dimensions from 3x3x3 through 6x6x6, all of which fit in 128 bits. That’s what I thought was being exposed in Metal 3.0 (and I was a little surprised, since that obviously requires hardware support which I’d assumed wasn’t present.)

Warren MooreI agree with you about line width. It’s historically not been supported because GPU vendors haven’t ever really agreed about how line joins should be done (if at all), or what quality of anti-aliasing for lines is acceptable. No API was introduced to support this, unless something was added to the shading language to allow this to be specified via a vertex shader (a la point size).

WasimThanks for all the great posts. Question on the debugging front. Is there a way to break on specific Metal Validation error/message? Like in Vulkan you can provide your own message handler and every time a validation error occurs you can break in your handler.

I understand not all validation layer messages in Metal are coming from direct API usage but deferred later once a pipeline is executed but it will still help in some cases.

Warren MooreGreat question. I suspect all validation errors eventually call into

`MTLReportFailure`

, so you could use a symbolic breakpoint to catch that, but I’m not sure how to hook into that programmatically without resorting to dangerous dynamic loader hacks.