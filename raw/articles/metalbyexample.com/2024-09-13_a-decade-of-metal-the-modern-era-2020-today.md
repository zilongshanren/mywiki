---
title: 'A Decade of Metal: The Modern Era (2020–Today)'
url: https://metalbyexample.com/a-decade-of-metal-the-modern-era/
published: '2024-09-13'
source_blog: Metal by Example
source_site: https://metalbyexample.com
category: graphics
fetched: '2026-04-13'
---

Welcome back to our ten-year retrospective on the Metal API. You can [read the first part here](https://metalbyexample.com/a-decade-of-metal-early-years/). This post will cover the last five years of Metal’s evolution as an enabling platform technology and bring us up to the present day.

## 2020 – Raytracing Redux

2020 was the year of the A14 Bionic, the powerhouse inside the entire iPhone 12 product line (base model, Mini, Pro, and Pro Max). Perhaps more saliently, the Apple M1, the ARM-based system-on-a-chip that began the [Mac transition to Apple Silicon](https://en.wikipedia.org/wiki/Mac_transition_to_Apple_silicon), debuted that fall.

Metal already had support for raytracing in the form of [MPS raytracing](https://developer.apple.com/documentation/metalperformanceshaders/mpsrayintersector) since 2018, but the release of Metal 2.3 in 2020 provided an opportunity to revisit raytracing and introduce support for raytracing in the core API itself: *bona fide* Metal raytracing.

Numerous features came to Metal’s library and shader function support in this release. The addition of the `[[visible]]`

function qualifier attribute made it possible to get programmatic access to functions that are *not* shader entry points (those qualified with `vertex`

, `fragment`

, `kernel`

, etc.) from the Metal API. Such functions can be referenced via [function pointers](https://developer.apple.com/wwdc20/10013) to create more flexible pipeline objects. Visible function tables, dynamic libraries, incremental pipeline compilation, and binary archives were also included.

On the machine learning front, the 2020 release included the new MetalPerformanceShaders Graph (`MPSGraph`

) API, which greatly simplifies ML use cases by providing a set of primitives ([tensor](https://developer.apple.com/documentation/metalperformanceshadersgraph/mpsgraphtensor) types and [operations](https://developer.apple.com/documentation/metalperformanceshadersgraph/mpsgraphoperation)) that can be composed into a DAG. Custom operations, such as activation functions, can be constructed from lower-level building blocks, and the MPS Graph compiler stitches the graph into a single performant Metal kernel.

Finally, [hardware counter](https://developer.apple.com/documentation/metal/mtlcounter) APIs made it easier to get granular [timing and utilization](https://developer.apple.com/documentation/metal/mtlcommoncounter) data on some GPUs.

## 2021 – Incremental

Released in the doldrums of the COVID-19 pandemic, Metal 2.4 debuted in iOS 15 and macOS 12 Monterey. This release included relatively few new features, but did showcase improvements to Metal raytracing and texture compression.

Metal raytracing gained support for animated transforms for [instance](https://developer.apple.com/documentation/metal/mtlinstanceaccelerationstructuredescriptor/3750501-motiontransformcount) acceleration structures, along with [animated data](https://developer.apple.com/documentation/metal/mtlmotionkeyframedata) for [triangle meshes](https://developer.apple.com/documentation/metal/mtlaccelerationstructuremotiontrianglegeometrydescriptor) and custom shape [bounding boxes](https://developer.apple.com/documentation/metal/mtlaccelerationstructuremotionboundingboxgeometrydescriptor). Together, these features make it much easier to render temporal effects like motion blur.

A15 Bionic, released in the fall (and M2, released later), included support for [lossy](https://developer.apple.com/documentation/metal/mtltexturecompressiontype/mtltexturecompressiontypelossy) texture [compression](https://developer.apple.com/documentation/metal/mtltexturedescriptor/3763055-compressiontype), enabling up to 50% savings in memory for textures that reside in private storage, with commensurate savings in bandwidth.

In 2021 we also got stitched functions, which introduce even more flexibility to how shader functions can be combined at compile time. Functions qualified with the `[[stitchable]]`

attribute may be combined together in a graph to produce a stitched function. Stitched functions are a subset of visible functions, meaning it is possible to create a `MTLFunction`

object referring to a stitched function programmatically. Such a function can then be used in other shader workflows, including those enabled by Metal function pointer support.

For a comprehensive introduction to the compilation workflows introduced in this release, refer to the WWDC 2021 video, [“Discover compilation workflows in Metal”](https://developer.apple.com/videos/play/wwdc2021/10229/).

## 2022 – Metal 3

If 2021’s release was incremental, 2022’s was anything but. Metal’s marketing version number was finally incremented to 3, having remained at 2 since 2017. Metal 3 brought not only major new features to the Metal framework itself, but a new utility framework dedicated to spatio-temporal upscaling: MetalFX.

Metal 3 introduced significant enhancements to argument buffers. Prior to Metal 3, resources were recorded into argument buffers using an argument encoder. With Metal 3, it became possible to ask a resource for a GPU-specific handle/address (`gpuResourceID`

in the case of `MTLTexture`

, and `gpuAddress`

in the case of `MTLBuffer`

). These values can be written directly into a Metal buffer from the CPU or GPU without an intervening encoder, and the referenced resources can be bound in a single call using the ordinary buffer binding APIs. It is also possible to get a GPU resource ID for pipeline state objects, which unlocks sophisticated GPU-driven rendering techniques.

[Last time](https://https://metalbyexample.com/a-decade-of-metal-early-years/), we noted that Metal never supported geometry shaders, but it has gradually gained more specialized geometry amplification features over the years (e.g. tessellation in 2016 and vertex amplification in 2019). Metal 3 added support for [mesh shaders](https://metalbyexample.com/mesh-shaders/), a more modern, flexible programmable geometry processing feature. With object and mesh shaders, you can perform granular meshlet culling; generate detail geometry like foliage, fur, or hair; and enhance particle systems with trails and ribbons; among many other possibilities.

[MetalFX](https://developer.apple.com/documentation/metalfx) is a new utility framework that provides two flavors of upscaling: temporal upscaling and spatial upscaling. Spatial upscaling is the simpler of the two, requiring just a color render target as an input and producing an upscaled color render target of your desired resolution (for example, from 1080p to 4K). Temporal upscaling, by contrast, requires a color texture, depth texture, and pixel motion vector texture (in addition to the previous frame’s color texture) in order to interpolate frames across time.

Metal also gained a new set of APIs that can greatly speed up [resource loading](https://developer.apple.com/documentation/metal/resource_loading). The new `MTLIOCommandQueue`

protocol and the corresponding `MTLIOCommandBuffer`

protocol allow you to concurrently load a file on disk directly into a Metal buffer or texture, without needing to load the asset’s data into memory. The Metal I/O APIs seamlessly supports a number of built-in compression schemes (ZLib, [LZBITMAP](https://developer.apple.com/documentation/compression/compression_algorithm/compression_lzbitmap), and [LZFSE](https://en.wikipedia.org/wiki/LZFSE)) which allows you to pack assets together in a smaller footprint. Custom compression codecs are also supported. Taken together these APIs allow you to implement sophisticated resource streaming and can be used in tandem with sparse texture APIs to maintain control over your video memory budget.

## 2023 – The Dawn of Spatial Computing

On June 5, 2023, Apple unveiled the Vision Pro (AVP), the culmination of many years of secretive work, and their entry into the world of mixed reality, rechristened as *spatial computing*.

Metal is a foundational technology in visionOS, the operating system that runs on Vision Pro. In addition to its role as the low-level graphics API beneath Reality Kit, Metal is available directly as a means of programming the M2 processor in the headset. In a moment of [connecting the dots with hindsight](https://youtu.be/UF8uR6Z6KLc?t=288), it became evident that features like vertex amplification, layered rendering, and rasterization rate maps are ideally suited for maximizing performance in the brave new world of spatial computing and stereo rendering on AVP.

Of course, there were many other features and APIs introduced in 2023 in support of the Vision Pro. A newly revamped ARKit, along with the all-new Compositor Services framework, provided low-level means of implementing high-performance virtual reality experiences in immersive spaces.

Although Vision Pro was the biggest news of WWDC 2023, Metal received other enhancements that didn’t pertain directly to it. In particular, Metal ray tracing received an upgrade in the form of curve primitives, useful for rendering geometry like hair, fur, foliage, and other long, thin, curving shapes. Curve primitives can also be [animated](https://developer.apple.com/documentation/metal/mtlaccelerationstructuremotioncurvegeometrydescriptor) similarly to triangle meshes and custom shapes.

Additionally, Metal ray tracing acceleration structures can now use multi-level instancing to support truly huge scenes. Now, instead of a top-level instance acceleration structure that directly contains primitive acceleration structures, you can compose instance acceleration structures into hierarchies with deeper nesting to take advantage of instanced groups of geometry. And for real-time use cases, you can split scene content into static and dynamic groups, speeding up refits and rebuilds of dynamic content.

2023 also brought enhancements to GPU-accelerated machine learning. MetalPerformanceShaders Graph gained APIs for [serializing](https://developer.apple.com/documentation/metalperformanceshadersgraph/mpsgraphexecutable/serialize(package:descriptor:)) and deserializing graphs, saving valuable time during app startup for large inference graphs. It also gained the ability to convert CoreML and ONNX models to the MPS Graph format.

## 2024 – The World of Tomorrow

This year, Metal hits version 3.2. The number of core API changes is fairly small, but there are some quality-of-life improvements, and the theme of Metal interoperability with system frameworks continues apace.

One interesting addition to RealityKit is the inclusion of new “low-level” APIs that allow much more efficient interoperability between the engine and custom Metal code. The [ LowLevelTexture](https://developer.apple.com/documentation/realitykit/lowleveltexture) type allows you to render content into a texture that can be used as a material property within a RealityKit scene, and the

[type allows you to manipulate the vertex positions and topology of a triangle mesh without needing to make excessive copies to transfer the data to the GPU.](https://developer.apple.com/documentation/realitykit/lowlevelmesh)

`LowLevelMesh`

Also on the interoperability front, Compositor Services gained new APIs and capabilities for rendering passthrough immersive experiences with Metal. This was both somewhat surprising and extremely exciting because it unlocks a huge number of potential augmented reality use cases outside the confines of RealityKit.

Resource types in Metal (`MTLBuffer`

, `MTLHeap`

, and `MTLTexture`

) now conform to a newly introduced protocol: `MTLAllocation`

. Such objects are backed by GPU memory and can report the amount of memory they occupy via the [ allocatedSize](https://developer.apple.com/documentation/metal/mtlallocation/4391635-allocatedsize) property.

A related change—perhaps the largest change to the Metal framework this year—is the introduction of [ residency sets](https://developer.apple.com/documentation/metal/mtlresidencyset). A residency set is a collection of resources (objects conforming to

`MTLAllocation`

) that can be made resident with a single call to the command buffer or command queue. Residency sets [simplify how we mark resource residency while also making it more efficient](https://developer.apple.com/documentation/metal/resource_fundamentals/simplifying_gpu_resource_management_with_residency_sets).

Metal raytracing received small improvements, notably to instance and motion transforms, which can now be specified as being in either row-major or column-major order. Transforms can also be specified by components (scale, translation, and orientation) to allow for more correct pose interpolation.

The Metal shader compiler API got a small upgrade in the form of the new [ mathMode](https://developer.apple.com/documentation/metal/mtlcompileoptions/4354201-mathmode) property on

`MTLCompileOptions`

: this allows you to select the [precision](https://developer.apple.com/documentation/metal/mtlmathmode)of math operations in shaders more granularly, replacing the

`fastMathEnabled`

flag.There were also minor improvements to binary archive handling. Stitched function graphs can now refer to binary archives, and binary archives can now contain stitched functions and mesh render pipeline functions.

A new [logging system](https://developer.apple.com/documentation/metal/mtllogstate) allows programmatic interception of log messages generated by shaders.

Finally, on the deprecation front, Metal support for PVRTC texture compression has been deprecated. Along with ETC2, PVRTC is now a rather old compression scheme and has been surpassed by the much more flexible ASTC standard. With near-universal adoption of ASTC in mobile chips, broader availability of BC(n) formats, and the imminent debut of [Binomial UASTC HDR](https://x.com/_binomial/status/1833645929192177783?s=61), there’s simply very little reason for new applications to adopt PVRTC.

We now find ourselves on the cusp of the release of macOS 15 Sequoia, iOS 18, and visionOS 2. With nearly a decade of Metal in the rear-view mirror, what can be said about the future? One thing is certain: Metal has cemented itself as a foundational technology across the entire Apple software ecosystem. From deep integration with SwiftUI, to enablement of machine learning, to supporting ultra high-fidelity games, Metal’s evolution has mostly kept pace with industry trends while bolstering Apple’s own hardware ambitions.

I expect Metal to continue growing and evolving for at least the next decade to come.