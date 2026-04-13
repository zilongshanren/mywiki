---
title: Metal Performance Shaders in Swift
url: https://metalbyexample.com/metal-performance-shaders-in-swift/
published: '2015-10-14'
source_blog: Metal by Example
source_site: https://metalbyexample.com
category: graphics
fetched: '2026-04-13'
---

## What is the Metal Performance Shaders Framework?

Announced at WWDC 2015, the Metal Performance Shaders (MPS) framework is a collection of high-performance image filters for iOS 9. Each filter in the library is an efficient black-box implementation of a common image processing task: blur, edge detection, convolution, etc. One useful trait of Apple’s black-box approach with the framework is that Apple can improve the implementation of these filters as new hardware becomes available, and users of MPS can avoid having to code them from scratch.

## Architecture

Every class in the framework derives from `MPSKernel`

. The term “kernel” is somewhat overloaded in this context. A *kernel function* in the Metal shading language is a shader for performing data-parallel work, but a *kernel* in the world of image processing usually refers to a matrix of weights that are convolved with a source image to produce an output image. Since the filters in Metal Performance Shaders all use kernel functions, but only a subset of them use convolution, we assume the former meaning.

By itself, `MPSKernel`

does nothing but provide an interface for giving a kernel a name and creating a copy of itself (through conformance to the `NSCopying`

protocol). The true power comes from its concrete subclasses. These concrete classes are subclasses of two additional abstract types: `MPSUnaryImageKernel`

and `MPSBinaryImageKernel`

. There is a third subclass of `MPSKernel`

named `MPSImageHistogram`

that is out of scope for this article.

### Unary Image Kernels

A *unary image kernel* operates on a single input texture to produce a single output texture.

The unary image operations available in MPS break down into several categories (The names given in parentheses form, along with the `MPSImage`

prefix, the names of the various subclasses of `MPSUnaryImageKernel`

):

- Convolutional operations (Box, Tent, GaussianBlur, Sobel, Convolution)
- Threshold (ThresholdBinary, ThresholdBinaryInverse, ThresholdToZero, ThresholdToZeroInverse, ThresholdTruncate)
- Resampling (LanczosScale)
- Morphological operations (Erode, Dilute)
- Sliding-neighborhood operations (AreaMax, AreaMin, Median, Integral, IntegralOfSquares, Threshold)

We’ll look at the effects of a few of these below.

### Binary Image Kernels

In contrast to unary image kernels, binary image kernels operate on two input textures to produce a single output kernel. Although MPS defines an abstract class for processing binary image kernels (`MPSBinaryImageKernel`

), it has no concrete subclasses. Therefore, we have to assume that it exists only to demonstrate the expected interface of a family of kernels that may exist in the future.

### Image Filter Geometry

The `MPSKernel`

interface declares two properties that determine which portion of the source image is read and which portion of the destination image is written.

The `offset`

property, of type `MPSOffset`

, determines which point of the source image is sampled for a given input coordinate. Thus, a positive offset has the effect of moving the source image up and to the left.

The `clipRect`

is an `MTLRegion`

structure (with an `origin`

and a `size`

) that describes the region of the destination texture that should be written. Pixels outside the clip rect are not affected by the kernel. If the offset is zero, the upper-left of the source image coincides with the origin of the clip rect.

![The effect of applying a clip rect with the default offset](../../assets/84853dba7dd59177.png)


![The effect of applying a clip rect with the default offset](../../assets/84853dba7dd59177.png)

![Here, the offset has been set to the origin of the clip rect, causing the origin of the source to coincide with the origin of the destination rather than the origin of the clip rect](../../assets/b720f8fdef633d05.png)


![Here, the offset has been set to the origin of the clip rect, causing the origin of the source to coincide with the origin of the destination rather than the origin of the clip rect](../../assets/b720f8fdef633d05.png)

### Edge Modes

The `edgeMode`

property of a kernel affects what happens when the kernel samples outside the bounds of the source texture. The edge mode options are reminiscent of the address mode options for texture samplers but are more restricted. The two permitted values are `MPSImageEdgeModeZero`

and `MPSImageEdgeModeClamp`

.

Selecting the `Zero`

edge mode simply results in all pixels outside the source texture bounds being treated as black (or clear, if the image has an alpha channel). Specifying the `Clamp`

mode causes the kernel to extrapolate beyond the texture bounds by repeating the pixel values that occur along the image edge.

![The effect of the Zero edge mode. Pixels outside the source image are assigned a (clear) black color.](../../assets/496b868e45cd5d08.png)


![The effect of the Zero edge mode. Pixels outside the source image are assigned a (clear) black color.](../../assets/496b868e45cd5d08.png)

![The effect of the Clamp edge mode. Pixels outside the source image's left and top edges are clamped to the values at those edges.](../../assets/44accbde9f89c969.png)


![The effect of the Clamp edge mode. Pixels outside the source image's left and top edges are clamped to the values at those edges.](../../assets/44accbde9f89c969.png)

## Using Metal Performance Shaders in Swift

In a departure from previous posts, we’ll explore MPS using Swift instead of Objective-C. Of course, MPS is exposed as an Objective-C API, so you should find that all of the concepts transfer if Objective-C is still your language of choice.

### Instantiating Kernels

The initializers of MPS kernels take a Metal device and some number of other parameters that specify how the kernel should behave. For example, the `MPSImageGaussianBlur`

kernel takes a `sigma`

parameter that determines its blur radius:

MPSImageGaussianBlur(device: device, sigma: 3.0)

In most cases, kernel properties may not be modified after initialization. This tells us that if we want to use different parameters, we have to create multiple filter instances. Apple tells us that kernels are fairly lightweight objects. Still, if you create new instances every frame, you will notice a performance hit, so try to reuse kernels as often as possible.

### Encoding Kernels to a Command Buffer

In order for a kernel to actually do its work, it must be encoded to a command buffer. Kernels operate on Metal textures, reading from their source and writing to their destination. Once you have asked your command queue for a command buffer, it is fairly simple to encode a kernel to it:

kernel.encodeToCommandBuffer(commandBuffer, sourceTexture: sourceTexture, destinationTexture: destinationTexture)

Command buffers in Metal are inherently heterogenous, meaning you can encode both rendering and compute commands into the same buffer. This means that you can bind the destination texture of a kernel in a subsequent draw call before calling `endEncoding`

on the command buffer. There is a performance penalty associated with switching between compute and render modes, so you should group together your kernel operations and your render operations when possible.

### In-Place Encoding

In some cases, MPS kernels can operate in-place, meaning they appear to read and write to the same texture. I say “appear,” since literally reading and writing the same texture is forbidden in the Metal shading language, but under the covers, MPS can operate in such a way that the texture you hand to it is the destination of the filter.

Even kernels which can sometimes operate in-place may not always be able to do so. For this reason, the method that encodes a kernel for in-place processing takes a closure (block) that allows the kernel to request a copy of a texture, which it then uses as a fallback to complete its processing in an out-of-place fashion. This makes in-place encoding substantially more reliable.

To encode a kernel in-place:

kernel.encodeToCommandBuffer(commandBuffer, inPlaceTexture:&texture, fallbackCopyAllocator:MBECopyAllocator)

Note that the `inPlaceTexture`

parameter is of type `UnsafeMutablePointer<MTLTexture?>`

, so if you pass an instance property here, it must be of type `MTLTexture?`

rather than an implicitly unwrapped optional (`MTLTexture!`

) or non-optional (`MTLTexture`

). The address of this object will change if the kernel succeeds, so the kernel needs to be able to overwrite it.

How do we define a fallback copy allocator? I choose to use a free function, but you could just as easily use a local function or trailing closure syntax.

let MBEFallbackAllocator = { (kernel: MPSKernel, commandBuffer: MTLCommandBuffer, sourceTexture: MTLTexture) -> MTLTexture in return sourceTexture.device.newTextureWithDescriptor(sourceTexture.matchingDescriptor()) }

The `matchingDescriptor`

method is a protocol extension to `MTLTexture`

that generates an `MTLTextureDescriptor`

that matches the source texture in pixel format and size. The code for this method is provided in the sample project. The descriptor is then used to request a new texture from the device, and returned.

### Examples of Kernels in Practice

The `MPSImageGaussianBlur`

class implements a blur filter that looks like a Gaussian blur but is specially tailored to be more performant than the 2D convolution a naïve implementation might use. It trades some precision and “non-Gaussian behavior” for much faster operation. Instantiate it as shown above, with a selectable blur radius. The blur radius, like most kernel properties, cannot be changed at runtime.

![Effect of a Gaussian blur kernel with a blur radius of 3](../../assets/fa1efe3c0ab54c8f.png)


![Effect of a Gaussian blur kernel with a blur radius of 3](../../assets/fa1efe3c0ab54c8f.png)

The `MPSImageSobel`

class implements Sobel edge detection, which increases the intensity of pixels that lie on the edges contained in the image (i.e., regions where the luminance changes rapidly).

The Sobel filter class optionally takes a “linear gray color transform”, a set of `Float`

values that are multipled by the RGB components of each pixel, then summed, to find its luminance. Most of the time, you’ll omit this parameter to use the default weight array of ![Rendered by QuickLaTeX.com [0.299, 0.587, 0.114]](https://metalbyexample.com/wp-content/ql-cache/quicklatex.com-215fd271d3a759b6b4a88c879280c023_l3.png)


let luminanceWeights: [Float] = [ 0.333, 0.334, 0.333 ] let sobelFilter = MPSImageSobel(device: device, linearGrayColorTransform: luminanceWeights)

![Effect of a Sobel edge detection kernel](../../assets/676f94d9f2147388.png)


![Effect of a Sobel edge detection kernel](../../assets/676f94d9f2147388.png)

MPS contains several threshold filters, each of which determines the result of the destination pixel by comparing the luminance of the source value to some constant threshold. As an example of this kind of filter, the `MPSImageThresholdToZero`

class sets to zero any destination pixel whose corresponding source pixel’s luminance does not exceed the threshold. The threshold value is set at initialization time and cannot be altered at runtime. The initializer also takes a linear gray color transform, which behaves as described above.

To instantiate a threshold filter:

let thresholdFilter = MPSImageThresholdToZero(device: device, thresholdValue: 0.5, linearGrayColorTransform: nil)

![Effect of a threshold-to-zero kernel](../../assets/f750f9431dc66f6e.png)


![Effect of a threshold-to-zero kernel](../../assets/f750f9431dc66f6e.png)

## Sample Project

The sample code for this article demonstrates the filters shown above. [Download it here](http://metalbyexample.com/wp-content/uploads/PerformanceShaders.zip). This sample also includes a custom desaturation kernel that conforms to the `MPSUnaryImageKernel`

interface so you can see how one might implement such a filter.

RicardoNice!

Great explanation of the basic MPS building blocks and also great to see some Metal in Swift 😉

An important note though:

Metal Performance Shaders are *not* available in OS X El Capitan and are only available in some iOS Feature Sets. Check out the feature availability table here:

https://developer.apple.com/library/ios/documentation/Miscellaneous/Conceptual/MetalProgrammingGuide/MetalFeatureSetTables/MetalFeatureSetTables.html#//apple_ref/doc/uid/TP40014221-CH13-SW1

Warren MooreDuly noted! I should’ve included a mention of

`MPSSupportsMTLDevice`

for testing the availability of MPS, and the mention of El Cap was an oversight.Filip LederleitnerHello Warren,

once again, a great post. Thank you for sharing your knowledge. I am very much looking forward to reading your upcoming book. Keep up the good work!

Ian Ollmann> The offset property, of type

`MPSOffset`

, determines which point of the source image is sampled for a given input coordinate.Strictly speaking, the offset property gives the position (in source coordinates) of the pixel read to create the top left corner pixel of the clipRect. The rest follow from there so as to fill the portion of the clipRect that overlaps the destination texture.

Any additional offset to account for the reach of kernel weights for things like blurs or Lanczos resampling is handled automatically by the

`MPSKernel`

. If you need to know this information, for example if you are doing some tiling on your own and need to know the extent of the kernel weight reach so that you don’t see artifacts at the tile seams, then you can call`-sourceRegionForDestinationSize:`

Warren MooreThanks for the clarification and further information, Ian.

MortenHey Warren,

all your Sample Code is NOT compiling on OS X 10.12 and Xcode 8.

Warren MooreShould compile and run fine now. Just needed to be updated to Swift 3 syntax.

NumairIt would be awesome if you wrote an updated version of your book targeting Swift 3 and iOS 10+. I’d buy it right away!

NeilA most excellent post. Well done!