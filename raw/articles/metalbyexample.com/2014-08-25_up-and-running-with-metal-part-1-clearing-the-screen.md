---
title: 'Up and Running with Metal, Part 1: Clearing the Screen'
url: https://metalbyexample.com/up-and-running-1/
published: '2014-08-25'
source_blog: Metal by Example
source_site: https://metalbyexample.com
category: graphics
fetched: '2026-04-13'
---

This post is several years old and may not reflect modern best practices or up-to-date API usage. For a somewhat newer introduction to Metal, consider starting with [this post](https://metalbyexample.com/modern-metal-1/), especially if you are more comfortable with Swift than Objective-C.

This post covers the bare minimum needed to clear the screen to a solid color in Metal. Even this simple operation requires many of the concepts exposed by the Metal framework. The next few posts in the Up and Running series will build on what we discuss here and take us through the basics of 3D rendering and image processing.

You can download the sample project for this post [here](http://metalbyexample.com/wp-content/uploads/HelloWorld1.zip).


Note that as of this writing, you cannot run Metal code in the iOS Simulator. You will need an iOS device with an A7 processor (such as an iPhone 5s or iPad mini with Retina display) running iOS 8. Additionally, you’ll need the latest version of Xcode, Xcode 6, to compile apps for iOS 8. The APIs are still in flux, so beta 6 is necessary to compile the sample project.

## Creating a New Project

Let’s create a new project in Xcode. I prefer to start with the Single View template, as it creates a view controller and wires it up to a window for us.

![Creating a new single-view project in Xcode](../../assets/bca245e1b0e6763b.png)


![Creating a new single-view project in Xcode](../../assets/bca245e1b0e6763b.png)

We need to link against Metal and Core Animation, so in the “Build Phases ▸ Link Binary with Libraries” step, filter down and add Metal.framework and QuartzCore.framework. Quartz Core is also known as Core Animation; the terms are interchangeable.

![Adding linked frameworks in Xcode](../../assets/104aeb660b6f2d3a.png)


![Adding linked frameworks in Xcode](../../assets/104aeb660b6f2d3a.png)

## Interfacing with UIKit

As you may know, UIView on iOS uses Core Animation as its backing store. The view’s layer holds the actual contents that get drawn on screen. We say that the such a view is *backed* by a `CALayer`

instance.

You can tell a `UIView`

to change the type of layer it instantiates as its backing layer by overriding the `+layerClass`

method on your `UIView`

subclass.

You can follow along in your own project by using the “File ▸ New ▸ File…” menu in Xcode and generating a new Cocoa Touch class which is a subclass of UIView. I’ll call mine `MetalView`

.

![Adding a new UIView subclass in Xcode](../../assets/9d9334e89a7a890f.png)


![Adding a new UIView subclass in Xcode](../../assets/9d9334e89a7a890f.png)

We need to make sure Xcode knows what we’re talking about when we refer to Metal classes, so be sure to import these two headers in your view subclass’ header file:

#import <Metal/Metal.h> #import <QuartzCore/CAMetalLayer.h>

You’ll notice that `CAMetalLayer`

is provided not by the Metal framework, but by Core Animation. `CAMetalLayer`

is the glue that binds UIKit and Metal together, and it provides some very nice features that we’ll be seeing shortly.

Let’s implement `+layerClass`

in our UIView subclass so it knows we want a Metal layer instead of a stock CALayer. Here’s the complete MetalView implementation as it stands:

@implementation MetalView + (id)layerClass { return [CAMetalLayer class]; } @end

Change the Custom Class of the view in the main storyboard file to `MetalView`

. This will cause the subclass to be instantiated when the storyboard is loaded. This in turn gives us a proper Metal layer-backed view.

For the sake of convenience, you can add a property to your view class that is of type `CAMetalLayer`

and assign it the result of `[self layer]`

in your `-init`

method. That prevents you from having to repeatedly cast from the type of the `layer`

property (i.e., `CALayer`

) to the actual subclass (`CAMetalLayer`

), since `CAMetalLayer`

offers a few methods not found on `CALayer`

.

If you build and run this project on your device, you will see nothing more than a plain white screen. To actually do any drawing, we need to learn about Metal *devices* and all the other objects they help us create. First, a word on the use of protocols in Metal.

## Protocols

A common theme in the Metal API is the use of *protocols*, rather than concrete classes, to expose Metal functionality. Many Metal APIs return objects conforming to particular protocols, with the concrete type being secondary. This has the advantage that you don’t need to care about the exact class implementing the functionality. We’ll need a

The syntax for referring to an object conforming to protocol `MTLDevice`

will look like this:

id <MTLDevice> device;

Now, let’s look at how to retrieve and use a device.

## Devices

A device is an abstraction around the GPU. It provides methods for creating objects like command queues, render states, and libraries. We’ll look at each of these in turn shortly.

Metal provides a C function, `MTLCreateSystemDefaultDevice`

, that creates and returns a `id<MTLDevice>`

that will suit our needs. This function takes no parameters, as there are no device properties that can be specified.

Our Metal layer needs to know which device will be rendering into it. We also need to configure a pixel format on the layer so everyone is in agreement about the size and order of its color components. `MTLPixelFormatBGRA8Unorm`

is a good choice. Each pixel will be comprised of a blue, green, red, and alpha component, and each component will be an 8-bit unsigned integer (between 0 and 255).

It’s helpful to create a `device`

property on your view subclass, as we will need the device to create various resources for us in the remainder of the code.

Here is the complete implementation of `-init`

showing all of the necessary configuration:

- (instancetype)initWithCoder:(NSCoder *)aDecoder { if ((self = [super initWithCoder:aDecoder])) { _metalLayer = (CAMetalLayer *)[self layer]; _device = MTLCreateSystemDefaultDevice(); _metalLayer.device = _device; _metalLayer.pixelFormat = MTLPixelFormatBGRA8Unorm; } return self; }

## The redraw method

In future posts, the `-redraw`

method is where we’ll issue drawing commands. In this sample project, we won’t be redrawing the screen repeatedly, just clearing it once to a solid color. Therefore, it is sufficient to invoke `-redraw`

just once. We can call it from our override of the `-didMoveToWindow`

method, since it will be called once as the app starts.

- (void)didMoveToWindow { [self redraw]; }

The `redraw`

method itself will do all of the work required to clear the screen. All code for the rest of the post is contained in this method.

## Textures and Drawables

Textures in Metal are containers for images. You might be used to thinking of a texture as a single image, but textures in Metal are a little more abstract. Metal also permits a single texture object to represent an *array* of images, each of which is called a *slice*. Each image in a texture has a particular size and a pixel format. Textures may be 1D, 2D, or 3D.

We don’t need any of these exotic types of textures for this post. Instead, we will be using a single 2D texture as our frame buffer (i.e., where the actual pixels get written). This texture will have the same resolution as the screen of the device our app is running on. We get a reference to this texture by using one of the features provided by Core Animation: the `CAMetalDrawable`

protocol.

A drawable is little more than a wrapper around a texture. Each time we draw, we will ask our Metal layer for a drawable object, from which we can extract a texture that acts as our framebuffer. The code is very straightforward:

id<CAMetalDrawable> drawable = [self.metalLayer nextDrawable]; id<MTLTexture> texture = drawable.texture;

We will also use the drawable to signal to Core Animation when we’re done rendering into the texture, so it can be presented on the screen. To actually clear the framebuffer’s texture, we need to set up a render pass descriptor that describes the actions to take each frame.

## Render Passes

A *render pass descriptor* tells Metal what actions to take while an image is being rendered. At the beginning of the render pass, the `loadAction`

determines whether the previous contents of the texture are cleared or retained. The `storeAction`

determines what effect the rendering has on the texture: the results may either be stored or discarded. Since we want our pixels to wind up on the screen, we select our store action to be `MTLStoreActionStore`

.

The pass descriptor is also where we choose which color the screen will be cleared to before we draw any geometry. In the case below, we choose an opaque red color (red = 1, green = 0, blue = 0, alpha = 1).

MTLRenderPassDescriptor *passDescriptor = [MTLRenderPassDescriptor renderPassDescriptor]; passDescriptor.colorAttachments[0].texture = texture; passDescriptor.colorAttachments[0].loadAction = MTLLoadActionClear; passDescriptor.colorAttachments[0].storeAction = MTLStoreActionStore; passDescriptor.colorAttachments[0].clearColor = MTLClearColorMake(1.0, 0.0, 0.0, 1.0);

The render pass descriptor will be used below to configure a command encoder for performing render commands.

## Queues, Buffers, and Encoders

A *command queue* is an object that keeps a list of render command buffers to be executed. We get one by simply asking the device. Typically, a command queue is a long-lived object, so in more advanced scenarios, we would hold onto the queue we create for more than one frame.

id<MTLCommandQueue> commandQueue = [self.device newCommandQueue];

A *command buffer* represents a collection of render commands to be executed as a unit. Each command buffer is associated with a queue:

id<MTLCommandBuffer> commandBuffer = [commandQueue commandBuffer];

A *command encoder* is an object that is used to tell Metal what drawing we actually want to do. It is responsible for translating these high-level commands (set these shader parameters, draw these triangles, etc.) into low-level instructions that are then written into its corresponding command buffer. Once we have issued all of our draw calls (which we aren’t doing in this post), we send the `endEncoding`

message to the command encoder so it has the chance to finish its encoding.

id <MTLRenderCommandEncoder> commandEncoder = [commandBuffer renderCommandEncoderWithDescriptor:passDescriptor]; [commandEncoder endEncoding];

As its last action, the command buffer will signal that its drawable will be ready to be shown on-screen once all preceding commands are complete. Then, we call `commit`

to indicate that this command buffer is complete and ready to be placed in command queue for execution on the GPU. This, in turn, will cause our framebuffer to be filled with our selected clear color, red.

[commandBuffer presentDrawable:drawable]; [commandBuffer commit];

## Build and Run

The sample code for this post can be found at [this link](http://metalbyexample.com/wp-content/uploads/HelloWorld1.zip). If you compile and run the project on an iOS device at this point, you should see a red screen. Behold, the fruits of our labor.

![The results of clearing the screen to a solid red color](../../assets/f0ab2f19efce8972.png)


![The results of clearing the screen to a solid red color](../../assets/f0ab2f19efce8972.png)

## Conclusions

This post set the groundwork for more exciting topics, such as 3D rendering. Hopefully, you now have a sense for a few of the objects you’ll see when working with Metal. Our next post will detail how to do basic rendering, such as drawing triangles. If you have topic ideas for future posts, please get in touch.

BarryHello Warren,

I’m interested in learning about graphics programming, especially 3D, but the field seems so wide and broad that it’s intimidating. I have intermediate capability in Objective-C (one app in the App Store) and very limited experience with Swift, largely because I didn’t want to dive into it last year when it was so young and immature.

Now, my question:

Any suggestions of where to begin? I’m wondering if I should follow along with the slide in your SLUG presentation, learning/studying SpriteKit then CoreAnimation then … and finally ending up with Metal? Sure, that would take a long time but I imagine I’d have a very comprehensive understanding. But then again, that’s a long program of study and work.

Many thanks and I look forward to your upcoming book.

Barry

warrenmI would say, if you want to get into 3D programming, there are two roads. One for the merely curious, and one for the intrepid.

For the curious, those who want to explore the surface before diving far below, definitely start with SceneKit or a similar technology. You’ll see universal concepts like meshes, transformations, materials, and scene graphs, at a high level. Then you can choose among these to decide where you focus your energies. You’re right in saying that 3D graphics is both broad and deep. This path is the best way to get a broad impression without getting bogged down in the details.

For the intrepid, I recommend a multi-year course of learning that incorporates all of the fundamentals, starting from the bottom up. This is tremendously harder, but sets you on the path to expert-hood a little earlier. My go-to resource is not a Metal tutorial, but an OpenGL tutorial: Learning Modern 3D Graphics Programming by Jason L. McKesson(now archived). There is approximately a 90% overlap between the topics covered by the arcsynthesis tutorial and the knowledge you need to do 3D programming with Metal or OpenGL ES, and it’s simply the best free resource.

As far as books are concerned, I strongly recommend Gortler’s book on 3D. It’s not too deep, but it hits all the important topics. Apart from that, one of the old standards like Hughes & Van Dam or Akenine-Möller & Haines is the way to go.

Hope this helps. If you encounter particular questions as you go on your way, please let me know. I’ll do my best to help.

danbeaulieuthanks for asking this barry, and for your answer warren. I’ll be watching this blog for sure.

Nathan YoungmanThe gltut mentioned is a broken link, but you can still find a PDF if you Google for:

Learning Modern 3D Graphics Programming by Jason L. McKesson

Nathan.

Warren MooreThanks for the note, Nathan! I’ve updated the link to point to an Internet Archive mirror of Jason’s site.

Pingback: Metal By Example’s first post, in Swift | The Catterwaul Blog

liHello Warren,

I am new in Metal.

Now I get a problem about this. I want to get the image rendered by the Metal API so I can grab the screen in time. I want to convert drawable.texture to CVPixelBufferRef, I write the code like this , but it did not work , please help me.

https://github.com/oklyc/oklyc.github.io

liHello Warren,

I am new in Metal.

Now I got a problem, I want to get the image rendered by the Metal API . I want get CVPixelBufferRef from the drawable.texture. I use the code (link: https://github.com/oklyc/oklyc.github.io ). But it did not work. I do not know where is wrong . Can you help me ? Or should I change another way to get the CVPixelBufferRef ?

Warren MooreI see a couple of problems here. Firstly, you’re committing your command buffer, but then asking for a blit command encoder and writing commands into it. You should wait to commit the command buffer till all of its encoders have ended encoding. Secondly, commands are processed asynchronously, but you’re not waiting for the rendering and blitting work to complete before trying to copy out the rendered pixels. You should defer that work by performing it in a completion block added to the command buffer with

`addCompletedHandler`

.liNow I changed my code in another project .

But the UIImageview meaned “_iv” did not display right. I think maybe some param was set wrong . But I could not find them . Can you help me ?

liOh , here is the link of the project.

https://github.com/oklyc/MetalCameraSample-master-2

HerkHi, Warren.

Great stuff. Your Swift-Metal video presentation was also very well done.

Now that Metal will soon be available on OS X, is there any chance of including OS X-specific material/code, along with iOS? With a few changes to your iOS code on my 2012 MacBook Pro beta version of El Capitan), I was able to get “Up and Running with Metal, Part 1” to build and display a white window. However, with the following error message:

2015-08-17 17:17:39.563 Hello-OSX-World[1806:127307] Metal API Validation Enabled

/Library/Caches/com.apple.xbs/Sources/Metal/Metal-54.16/ToolsLayers/Debug/MTLDebugCommandBuffer.mm:296: failed assertion `No textures set.’

I don’t know enough to know if this is due to differences between iOS and OS X, or due to my coding errors/omissions.

Good luck with your book project.

Best regards,

Herk

Warren MooreHey Herk, I found that I had to do two things (apart from making

`MetalView`

subclass`NSView`

in the first place) to get this code working on the Mac. First, because`NSViews`

are not layer-backed by default, you have to call`setWantsLayer:`

on the view really early in its lifecycle (I called it up-front inside`initWithCoder:`

, you can also tick the appropriate box in Interface Builder). This causes`makeBackingLayer`

to be called. From`makeBackingLayer`

I just return a new CAMetalLayer.LukeHi, Warren. After reading your reply to Barry on July 9, I thought I’d go for the ground-up learning approach to 3D graphics. Unfortunately, Jason McKesson’s book relies on the unofficial gl sdk, which isn’t supported on OS X. Can you recommend a place to go to learn fundamental graphics concepts with a long-term view of circling around to your book and mastering Metal on Mac?

Warren MooreI think of the Unofficial GL SDK as a piece of scaffolding. The actual substance of the tutorials is the GLSL code and GL API calls, which are the same regardless of the scaffold you use. It’s unfortunate that the Unofficial SDK is unsupported on OS X, and that GLUT is now deprecated. These impedance mismatches are just one more thing that make learning this stuff harder. But I think you can progress through the tutorials by stealing some GLKit code (substituting

`NSOpenGLView`

for`GLKView`

and`GLKViewController`

where appropriate) and stuffing in the tutorial code. You won’t be able to compile Jason’s sample codeper se, but I think typing it yourself affords more chances for learning and creativity.If you prefer dead-tree mode, I’ll put in one more plug for Gortler’s book, which is quite dry and terse, but has fewer external dependencies (i.e., it might be easier to port from GLUT to GLKit).

One final suggestion I might make is Ed Angel’s Coursera class on WebGL. If you aren’t averse to learning the API in Javascript instead of C, it’s very-well presented, and all of the concepts (and much of the syntax, actually) will transfer.

CharlesHi Warren.

Thanks for this great website and it is extremely helpful so far.

Here is one question that I have and I cant seem to understand this concept very well. What are color attachments exactly ? I see both pipelinestate descriptor and pass render descriptor have an array of color attachments. What are they for and what would be the case when we need to use something other than colorattachments[0]?

Linhua XieHi Warren, I’m also a new to 3D graphics, but I’m very curious about it. I try to learn it, but everytime I found it very very big bone, my confidence lose a half. Luckily, I found your blog, especially the suggestions for beginners.

I’m just an app develop, not excellent. My math is not good also, so, is it very very difficult for me to dive into 3D graphics world?

CheneyChenIs there a method in the metal as same as glViewport in OpenGL, set the viewport ,to achieve split-screen as the VR mode.

Rajan SHi Warren,

Awesome job with “Metal by Example”.

I have just started to get into Metal. All the examples I find are targeted towards ios. I am looking for steps to setup my xcode to get a simple triangle rendered using swift 3 for OSX . Could you suggest any blogs/website that could help me with this?

Warren MooreYou could use the Metal game template included in Xcode. File ▸ New ▸ Project… ▸ macOS ▸ Game ▸ (Language: Swift; Game Technology: Metal)

Mladen MikićHi Warren,

thank you for this tutorial. This tutorial helped me and a colleague to get started with Metal.

Here is a updated Swift version:

https://github.com/Darkwonder/HelloWorldMetal

Best regards, Mladen