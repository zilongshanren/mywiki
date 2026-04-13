---
title: First Look at MetalKit
url: https://metalbyexample.com/first-look-at-metalkit/
published: '2015-06-25'
source_blog: Metal by Example
source_site: https://metalbyexample.com
category: graphics
fetched: '2026-04-13'
---

MetalKit is a forthcoming framework on iOS 9 and OS X El Capitan that greatly eases certain tasks such as presenting Metal content in a `UIView`

or `NSView`

, texture loading, and working with model data.

This post is an overview of the features offered by MetalKit. Many of our articles so far have focused on details that are not expressly related to Metal, but are instead required to give Metal something to draw on the screen: texture loading, 3D model loading, and setting up the interface between Metal and UIKit.

MetalKit seeks to make these tasks easier by providing classes that perform common operations. In this article, we’ll look briefly at these capabilities.


## Interfacing with UIKit and AppKit

MetalKit provides the cross-platform `MTKView`

class, which subclasses `UIView`

on iOS and `NSView`

on OS X. This class does more than simply encapsulate a `CAMetalLayer`

; it also manages the render target attachments associated with the framebuffer and handles the draw loop. Let’s look at it more detail.

### Creating an `MTKView`


`MTKView`

implements the usual initializers: `initWithFrame:`

and `initWithCoder:`

. On iOS, you can optionally set the `device`

property to an `MTLDevice`

of your choosing, but this isn’t necessary, as it is set to `MTLSystemCreateDefaultDevice()`

by default. On OS X, setting this property is mandatory, as it is `nil`

by default.

### Configuring an `MTKView`


Since the `MTKView`

manages your render target attachments, you must configure a few properties on it to ensure that the formats of these attachments match the needs of your application.

The most important of these properties is `colorPixelFormat`

. For applications that render to a `CAMetalLayer`

, this value is almost always `MTLPixelFormatBGRA8Unorm`

, which is the usual format of renderable textures vended by CAMetalDrawable.

Setting the `clearColor`

, `clearDepth`

, and `clearStencil`

properties passes through these values to the view’s render pass descriptor, which determines how the various attachments are cleared at the beginning of the frame.

### The Draw Loop

To perform drawing, you have the option of subclassing `MTKView`

and overriding `drawRect:`

, or providing a delegate conforming to `MTKViewDelegate`

, wherein you can implement `drawInView:`

to receive regular callbacks.

You can control the rate at which you receive draw callbacks by configuring the view’s `preferredFramesPerSecond`

value. The view maintains an internal timer that fires at a rate that corresponds as closely as possible to this value.

Within your `drawRect:`

or `drawInView:`

implementation, you can access the view’s `currentRenderPassDescriptor`

to get a render pass configured with the current drawable’s texture set as its primary color attachment. With this render pass, you can construct a render command encoder and perform your draw calls.

## Loading Textures

MetalKit also provides a class for loading texture data: `MTKTextureLoader`

. You may recall the work involved in loading image data into a texture, especially compressed image data. MetalKit’s texture utility class makes this process substantially simpler.

You initialize a texture loader by passing it a device. You can then load a texture from disk synchronously with the `textureWithContentsOfURL:options:error:`

method, or asynchronously with `textureWithContentsOfURL:options:completionHandler:`

. The latter method takes a block that is called with the texture when it is fully loaded. There are similar methods for synchronously and asynchronously loading textures from `CGImage`

and `NSData`

. Metal inspects image data to determine its type, whether PNG, JPEG, or a KTX or PVR compressed image container.

Calling any of these methods with a key of `MTKTextureLoaderOptionAllocateMipmaps`

and a value of `@(YES)`

in the options dictionary will produce a mipmapped texture.

## Managing Model Data

A full discussion of MetalKit’s support for model data handling necessarily entails discussing Model I/O, since the two are designed to work together. A companion to this post will go into greater detail on Model I/O, but let’s take a high-level look at MetalKit’s facilities for working with meshes.

### Meshes and Submeshes

Both Model I/O and MetalKit have a hierarchical representation for model data: *meshes* contain vertex data and submeshes, which *submeshes* contain contain an index buffer and a material reference. This means that all of the data for a model can be contained in a single contiguous buffer, with each submesh corresponding to a contiguous set of indices into this vertex data. A submesh also has properties signifying its geometry type (point, line, triangle, etc). MetalKit’s classes for meshes and submeshes are `MTKMesh`

and `MTKSubmesh`

, respectively. The `MTKMeshBuffer`

class abstracts over the Metal buffers that contain the mesh data.

### Rendering Meshes

To render a mesh with Metal, we might set its vertex buffers in the argument table, then iterate over its submeshes, using a draw method like `drawIndexedPrimitives:indexCount:indexType:indexBuffer:indexBufferOffset:`

and providing the geometry type, index count, index type, and index buffer contained by the submesh. In order to draw a submesh properly, we would also need to take into account the properties specified by its associated material, which might entail writing various shaders and ancillary resources like BRDF lookup tables.

## Future Directions

The future is now! With Metal coming to OS X with El Capitan, Metal is more important than ever, and you can experiment with MetalKit using prerelease versions of Xcode, OS X, and iOS. Refer to the complete [MetalKit reference](https://developer.apple.com/library/prerelease/ios/documentation/MetalKit/Reference/MTKFrameworkReference/index.html#//apple_ref/doc/uid/TP40015356) for more details. We’ll be covering MetalKit here as the public release of the framework approaches.

Simon GladmanThat’s a great summary of MetalKit, thanks Warren.

Incidentally, I’ve updated my Metal particles demo to use MTKView and I’m now able to use the same Swift class to run my particles simulation on both OS X and iOS. As of Beta 2, the performance between my iPad Air 2 and MacBook Pro is pretty much the same.

The source code is all open and you can read about my experiments here:

http://flexmonkey.blogspot.co.uk/2015/06/cross-platform-metal.html

Cheers,

Simon

Warren MooreThanks for the feedback and signal-boosting, Simon! I’ve been following your work in porting your particle sims to OS X. I’m super excited to get my dedicated El Capitan machine in time for this weekend. Really looking forward to working with Metal on the Mac 🙂

Simon GladmanWhich Mac are you installing 10.11 on? On my MBP, Metal runs beautifully, but another developer has had real issues running my code on their Pro (I’ve raised a Radar). I’d love to know how my particles run on your OS X machine.

Now I’m on tenterhooks WRT the rumored “iPad Pro”. Considering how powerful the A8X is, I can’t wait to see what A9 based devices will be like.

Simon

dr.ainwe already know the limitation of 5W TDP

in the new Macbook. So what makes you believe

iPad pro will do any better.

14 nm is 30%

A57 to A72 is 50%

Series 7XT probably is 50%.

at most it will be around 500 GFLOPS.

Simon GladmanWell, I guess nobody outside of Apple knows what the future brings.

However, *if* there is an iPad Pro in the works and it’s being geared towards serious gaming and content creation, I’m sure Apple will be trying their hardest to squeeze as much performance out of it as possible. It’s in their interest to differentiate it from existing devices – not only in size but in performance too.

The leap between the A7 and A8 chip sets was immense, hence my “tenterhooks”!

Max ZangsWill your book also talk about Metal on Mac OS?

So far I’m learning from scratch and trying to map textures to simple triangles, but seem to fail. Maybe it’s because Metal for OS X isn’t fully developed yet or it’s me doing something wrong – which is more likely…

Warren MooreNot currently planning on covering Metal for OS X, regrettably. Happy to help you debug if you can describe the issue further, though.

lfHow about a future post on Swift with Metal? I noticed in your lecture demo code that you rolled your own Swift types (Matrix4x4, Vector4, etc.) rather than using SIMD. Was this because of the divide between Swift and C++, or issues using SIMD in Swift?

Warren MooreYeah, full simd support has been a long time coming in Swift. I think it’s pretty much there with Swift 2.0, but that’s still a few weeks out at the earliest. I’ve tried to keep most of the material here relevant to the contemporary releases, but as Swift comes to the fore, I’m happy to cover it as well.

JohnForgive my ignorance on this, I’m not an engineer…just a curious PM. I’m working on a medical imaging app that needs to render high resolution photography at various zoom levels. Is there anything Metal offers that can improve performance when viewing/interacting with large images? Anything to be aware of if trying to leverage CATiledLayer?

Warren MooreHi John, sorry for the delayed response on this. Rendering arbitrarily high resolution imagery is not really in my wheelhouse, but it occurs to me that a lot of your performance considerations come from the format of the images, which is to say: can you progressively decode random regions of your images from the available format or not? If so, you can stream in the relevant regions (whether that’s in response to a callback from a tiled layer or something lower level like a Metal renderer). If not, you’re likely to carry a pretty big footprint just to decompress the image in the first place. If you can share some particulars about your situation, I’ll try to help further.

AlexanderSHi Warren, just curious what your plans are with this site? Also are you planning on doing a book on metal?

There are almost no resources covering metal, but much interest out there.

Warren MooreMy current plan is for the site to remain online as a resource, and I hope to publish some of the material here along with some exclusive material in the form of a book later this year. I’m curious, since you’re looking for Metal resources: what are you using Metal for, and what kind of tutorials would you like to see?

MaxHi Warren, really great site!

Thanks for all the unique material.

I’m very interested in doing GPGPU with Metal, it would be fantastic to have at least something relevant covered in your forthcoming book!

Warren MooreTo be perfectly frank, the extent of data-parallel programming in the book is limited to image processing. I wish I had more time to address proper GPGPU, but the vagaries of life require me shipping the book in a timely fashion.