---
title: 'Up and Running with Metal, Part 2: Drawing Triangles'
url: https://metalbyexample.com/up-and-running-2/
published: '2014-08-26'
source_blog: Metal by Example
source_site: https://metalbyexample.com
category: graphics
fetched: '2026-04-13'
---

This post is several years old and may not reflect modern best practices or up-to-date API usage. For a somewhat newer introduction to Metal, consider starting with [this post](https://metalbyexample.com/modern-metal-1/), especially if you are more comfortable with Swift than Objective-C.

In our [inaugural post of the series](http://metalbyexample.com/up-and-running-1/), we got a glimpse of many of the essential moving parts of the Metal framework: devices, textures, command buffers, and command queues. Although that post was long, it couldn’t possibly cover all these things in detail. This post will add a little more depth to the discussion of the parts of Metal that are used when rendering geometry. In particular, we’ll take a trip through the Metal rendering pipeline, introduce functions and libraries, and issue our first draw calls.

The end goal of this post is to show you how to start rendering actual geometry with Metal. The triangles we draw will only be in 2D. Future posts will introduce the math necessary to draw 3D shapes and eventually animate 3D models.

Download the sample code for this post [here](http://metalbyexample.com/wp-content/uploads/MetalTriangles.zip).


## Setup

The initializer of the `MetalView`

class has been refactored to call a sequence of methods that will do all the work necessary to get us ready to render:

[self buildDevice]; [self buildVertexBuffers]; [self buildPipeline];

`-buildDevice`

is precisely the same code that used to be included directly in the init method, as we saw in the previous post:

- (void)buildDevice { _device = MTLCreateSystemDefaultDevice(); _metalLayer = (CAMetalLayer *)[self layer]; _metalLayer.device = _device; _metalLayer.pixelFormat = MTLPixelFormatBGRA8Unorm; }

The definitions of the other two methods will be given in the sections below.

## Using Buffers to Store Data

Metal provides a protocol, `MTLBuffer`

, for representing an untyped buffer of bytes with a fixed length. Its interface is very similar to `NSData`

. However, Metal buffers are associated with a particular device, which manages how the data is copied during draw calls.

We will use two separate static arrays to define our geometry, which is a triangle with red, green, and blue vertices. We will then ask Metal to create buffers that contain a copy of this data, and store these buffers in new properties on our `MetalView`

class: `positionBuffer`

and `colorBuffer`

.

- (void)buildVertexBuffers { static const float positions[] = { 0.0, 0.5, 0, 1, -0.5, -0.5, 0, 1, 0.5, -0.5, 0, 1, }; static const float colors[] = { 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, }; self.positionBuffer = [self.device newBufferWithBytes:positions length:sizeof(positions) options:MTLResourceOptionCPUCacheModeDefault]; self.colorBuffer = [self.device newBufferWithBytes:colors length:sizeof(colors) options:MTLResourceOptionCPUCacheModeDefault]; }

You might have noticed that each vertex position is composed of four components, even though we only care about the x and y positions (since we’re drawing a 2D triangle). This is because Metal works most naturally in 4D *homogeneous coordinates*, where each point has x, y, z, and w coordinates, with w fixed at 1. The reasons for this involve the mathematics of projective geometry, which is a topic for future posts.

In order to simplify the math we need to do in our shaders, the points are specified in *normalized device coordinates*, where the x-axis runs from -1 to 1 going left to right, and the y-axis runs from -1 to 1 from bottom to top.

Each color is composed of the familiar red, green, blue and alpha components.

Now, let’s look at the vertex and fragment functions that will be processing this data when we draw.

## Functions and Libraries

### Functions (a.k.a. Shaders)

Modern graphics libraries provide a “programmable pipeline,” meaning that they allow a lot of the operations carried out by the GPU to be specified by small programs applied to each vertex or pixel. These are commonly referred to as “shaders”. This is a poor name, since shaders are responsible for much more than calculating the shading (color) of pixels. No Metal class actually has “shader” in the name, but by convention, vertex and fragment functions are often called shaders.

To incorporate Metal shading code into our project, we need to add a Metal source file to our project to contain the shaders that will process our vertices and fragments.

![Adding a Metal shader source file in Xcode](../../assets/596912ccc28bfbc6.png)


![Adding a Metal shader source file in Xcode](../../assets/596912ccc28bfbc6.png)

Here is the source of Shaders.metal:

using namespace metal; struct ColoredVertex { float4 position [[position]]; float4 color; }; vertex ColoredVertex vertex_main(constant float4 *position [[buffer(0)]], constant float4 *color [[buffer(1)]], uint vid [[vertex_id]]) { ColoredVertex vert; vert.position = position[vid]; vert.color = color[vid]; return vert; } fragment float4 fragment_main(ColoredVertex vert [[stage_in]]) { return vert.color; }

The `vertex_main`

function will be run on each vertex that we draw, while the `fragment_main`

function will be run on (essentially) every pixel that we draw. Each function is preceded by a *function qualifier*, which signals how it will be used. In this listing we see `vertex`

and `fragment`

qualifiers. There is also a `kernel`

function qualifier for compute kernels.

We define a struct, `ColoredVertex`

, that will store the result of the vertex function. The vertex function’s parameters correspond to the vertex buffers we created earlier. The `position`

parameter has an *attribute qualifier* of `[[buffer(0)]]`

, which will map to an index we provide when setting up our draw call. Likewise with the `color`

parameter. The `vid`

parameter is the index into these buffers that corresponds to the current vertex being processed, and will run from `0`

to `2`

(once for each point in the triangle).

In the body of `vertex_main`

, we simply copy the incoming position and color data into an intermediate vertex of type `ColoredVertex`

. This essentially packages up the data for the fragment function. If we were doing 3D rendering, quite a bit more math would be involved here (projecting the points from 3D to 2D, per-vertex lighting, etc.)

The fragment function, `fragment_main`

, takes a `ColoredVertex`

qualified with the attribute qualifier `[[stage_in]]`

, which identifies it as per-fragment data rather than data that is constant across a draw call. This `ColoredVertex`

does not correspond exactly to an instance of `ColoredVertex`

returned by the vertex function. After all, the vertex function is only invoked three times to draw our triangle, while the fragment function might be called many thousands of times.

Instead, the `vert`

parameter is constructed during the *rasterization* stage, which determines which pixels are covered by the triangles we draw. This stage occurs *between* the vertex and fragment function calls. The values at the vertices (i.e., those returned by the vertex function) are *interpolated* between the vertices to produce the values passed to the fragment shader. This has the effect of transitioning smoothly between colors across the surface of the triangle.

### Libraries

Often, graphics libraries require the source of each shader to be compiled separately. Shaders must then be linked together to form a *program*. Metal introduces a nicer abstraction around shaders: the *library*. A library is nothing more than a logical group of functions written in the Metal shading language. You’ve already seen above that we have lumped our vertex and fragment function into a single file. This file will be compiled along with the rest of the project, and the compiled shader is included in the app bundle. Metal allows use to easily look up functions by name at runtime as shown in the next listing.

id<MTLLibrary> library = [self.device newDefaultLibrary]; id<MTLFunction> vertexFunc = [library newFunctionWithName:@"vertex_main"]; id<MTLFunction> fragmentFunc = [library newFunctionWithName:@"fragment_main"];

Once you have references to your vertex and fragment functions, you configure your pipeline to use them, and the necessary linkage is performed implicitly by Metal. This is illustrated in the following sections. The code above is incorporated in the `-buildPipeline`

method in the sample code.

## The Render Pipeline

It’s natural to think of graphics hardware as a state machine: you set some state (like where to pull data from, and whether draw calls should write to the depth buffer), and that state affects the draw calls you issue afterwards. Most of the API calls in a graphics library like OpenGL exist to allow you to set various aspects of state.

Metal provides a slightly different abstraction of the hardware state machine. Rather than calling API that acts on some global “context” object, Metal allows you to build an object graph that represents a virtual *pipeline* that takes vertex data from one end and produces a rasterized image on the other end. We’ve already seen part of this in action. By telling our Metal layer which device we’re using, we’ve created one link in the pipeline. Now we’ll discuss a few more kinds of objects that link together to describe the GPU state we want to use when executing render commands: the render pipeline descriptor and render pipeline state.

### Render Pipeline Descriptors

A *render pipeline descriptor* is an object that holds configuration options for a pipeline. In particular, this is where you configure which vertex and fragment shaders will be applied to the geometry that is processed by your draw calls. Here’s the code for creating a descriptor object:

MTLRenderPipelineDescriptor *pipelineDescriptor = [MTLRenderPipelineDescriptor new]; pipelineDescriptor.vertexFunction = vertexFunc; pipelineDescriptor.fragmentFunction = fragmentFunc; pipelineDescriptor.colorAttachments[0].pixelFormat = self.metalLayer.pixelFormat;

We will discuss color attachments in a future post. For now, just know that the first color attachment (at index 0) is commonly used as the framebuffer that gets rendered to screen, so it’s important that the layer and the color attachment agree on the pixel format.

### Render Pipeline State

A *render pipeline state* is an object conforming to protocol `MTLRenderPipelineState`

. We create a pipeline state by providing our newly-created pipeline descriptor to our device, storing the result in another property named `pipeline`

.

self.pipeline = [self.device newRenderPipelineStateWithDescriptor:pipelineDescriptor error:NULL];

The pipeline state encapsulates the compiled and linked shader program derived from the shaders we set on the descriptor. Therefore, it is a somewhat costly object. Ideally, you should only create one pipeline state object for each unique shader program you need to execute. That’s why we store it in a property on our view class. Later on, we’ll configure our command buffer with it so it can use the compiled shader program to process our geometry.

The code above is the central portion of the `-buildPipeline`

method in the sample code.

## Encoding Render Commands

In the previous post, we didn’t interact much with the render command encoder, since we weren’t performing any drawing. This time around, we need to encode actual draw calls into our render command buffer. First, let’s revisit the retrieval of a drawable from the layer and the configuration of a render pass descriptor. This is the beginning of the `-redraw`

method for this sample project:

id<CAMetalDrawable> drawable = [self.metalLayer nextDrawable]; id<MTLTexture> framebufferTexture = drawable.texture; MTLRenderPassDescriptor *renderPass = [MTLRenderPassDescriptor renderPassDescriptor]; renderPass.colorAttachments[0].texture = framebufferTexture; renderPass.colorAttachments[0].clearColor = MTLClearColorMake(0.5, 0.5, 0.5, 1); renderPass.colorAttachments[0].storeAction = MTLStoreActionStore; renderPass.colorAttachments[0].loadAction = MTLLoadActionClear;

The `renderPass`

object is constructed exactly as before, except that I have chosen a neutral gray color to clear the screen with, instead of the obnoxious red we used last time.

Now, we ask the command encoder to encode our draw call:

id<MTLRenderCommandEncoder> commandEncoder = [commandBuffer renderCommandEncoderWithDescriptor:renderPass]; [commandEncoder setRenderPipelineState:self.pipeline]; [commandEncoder setVertexBuffer:self.positionBuffer offset:0 atIndex:0 ]; [commandEncoder setVertexBuffer:self.colorBuffer offset:0 atIndex:1 ]; [commandEncoder drawPrimitives:MTLPrimitiveTypeTriangle vertexStart:0 vertexCount:3 instanceCount:1]; [commandEncoder endEncoding];

The `setVertexBuffer:offset:atIndex:`

method is used to map from the `MTLBuffer`

objects we created earlier to the parameters of the vertex function in our shader code. Recall that the `position`

parameter was qualified with the `[[buffer(0)]]`

attribute qualifier, and notice that we now provide an index of `0`

when preparing our draw call. Likewise with the color buffer index, which was qualified with `[[buffer(1)]]`

.

We call the `drawPrimitives:vertexStart:vertexCount:instanceCount:`

method to encode a request to draw our triangle. We pass `0`

to the `vertexStart`

parameter so that we begin drawing from the very start of the buffer. We pass `3`

for `vertexCount`

because a triangle has three points. The purpose of the `instanceCount`

parameter will be discussed in future posts, but for the time being we set it to `1`

.

We finish up as before by triggering display of the drawable and committing the command buffer:

[commandBuffer presentDrawable:drawable]; [commandBuffer commit];

These lines round out the new implementation of the `-redraw`

method.

## Staying in Sync With CADisplayLink

Now that our `-redraw`

implementation is complete, we need to figure out how to call it repeatedly. We could use a regular old `NSTimer`

, but Core Animation provides a much better way: the `CADisplayLink`

. This is a special kind of timer that is synchronized with the display loop of the device, leading to more consistent timing. Each time the display link fires, we’ll call our `-redraw`

method to update the screen.

We override `didMoveToSuperview`

to configure the display link:

- (void)didMoveToSuperview { [super didMoveToSuperview]; if (self.superview) { self.displayLink = [CADisplayLink displayLinkWithTarget:self selector:@selector(displayLinkDidFire:)]; [self.displayLink addToRunLoop:[NSRunLoop mainRunLoop] forMode:NSRunLoopCommonModes]; } else { [self.displayLink invalidate]; self.displayLink = nil; } }

This creates a display link and schedules it with the main run loop. If we are removed from our superview, we invalidate the display link and nil it out.

Sixty times per second, the display link fires and invokes its target method, `-displayLinkDidFire:`

, which in turn calls `-redraw`

:

- (void)displayLinkDidFire:(CADisplayLink *)displayLink { [self redraw]; }

## Build and Run

The sample project for this post is located [here](http://metalbyexample.com/wp-content/uploads/MetalTriangles.zip). If you build and run it, you should see a very colorful triangle appear on the screen:

![A multicolored triangle, rendered by Metal](../../assets/0045ad3585fb01d3.png)


![A multicolored triangle, rendered by Metal](../../assets/0045ad3585fb01d3.png)

## Conclusion

In this post, we explored some additional features of Metal and finally got to draw something on the screen. In upcoming posts in this series, we’ll get much deeper into the math and the Metal shading language as we explore topics in 3D rendering. Stay tuned!

Pingback: Metal By Example’s second post, in Swift | The Catterwaul Blog

TylerHi,

I have made my metal shaders. However there is aliasing effect along the edges.

I find the texture I got from CAMetalLayer is not converted to Retina resolution:

`id drawable = [self.metalLayer nextDrawable];`


id texture = drawable.texture;

The texture I got is:

`{`

arrayLength = 1;

depth = 1;

framebufferOnly = 1;

height = 488;

mipmapLevelCount = 1;

pixelFormat = MTLPixelFormatBGRA8Unorm;

resourceOptions = None;

sampleCount = 1;

textureType = MTLTextureType2D;

width = 320;

}

{

isFramebufferOnly = 1;

rootResource = "";

}

Warren MooreYou’re responsible for ensuring that the

`drawableSize`

of your Metal layer matches the desired size of your renderbuffer. For example, in my`UIView`

subclass, I override`setFrame:`

to set it appropriately. If you are not overriding`layerClass`

to return`[CAMetalLayer class]`

, you still need to expressly set the desired drawable size, similarly to the code below:`- (void)setFrame:(CGRect)frame`

{

[super setFrame:frame];

// During the first layout pass, we will not be in a view hierarchy, so we guess our scale

CGFloat scale = [UIScreen mainScreen].scale;

// If we've moved to a window by the time our frame is being set, we can take its scale as our own

if (self.window)

{

scale = self.window.screen.scale;

}

CGSize drawableSize = self.bounds.size;

// Since drawable size is in pixels, we need to multiply by the scale to move from points to pixels

drawableSize.width *= scale;

drawableSize.height *= scale;

self.metalLayer.drawableSize = drawableSize;


}

HerkHi, Warren.

Thanks for your reply to a question I asked a couple weeks ago. Perhaps you could offer your advice on another issue.

Would you consider Metal / MetalKit to be suitable for a hobbyist interested in learning physic’s & physics-engine programming? I’ve been working on step #1 of this elementary project (http://www.wildbunny.co.uk/blog/2011/04/06/physics-engines-for-dummies/) for quite some while now and cannot for the life of me manage to get more than a single “particle” to render at any given time. (I’m using an icosahedron mesh to represent particles.)

Thanks for any guidance or suggestions.

Herk

boomHi,

Your example projects don’t take up the entire screen. Any ideas? Great tutorials

Warren MooreI’d be happy to look into this if you can tell me which project you’re referring to, and which hardware and version of iOS you’re running.

Daren ShanHi Warren,

First off great tutorials.

I was wondering how to supply position values as a float3 instead of float4. Does the vertex buffer need to contain four values each, or can i just convert the vertec to float4 at the shader level? My problem is I’m converting an old open gl project and I have a lot of functions that assume 3 values for position. Would be nice not having to change that and simply makes more sense to me.

Warren MooreThere are a couple of points here, one obvious and one subtle. The first point is, of course you can use 3-vectors everywhere, as long as all of your code is consistent. The things that have to be in agreement are: your data structures for holding the data client-side and in your shaders, and any vertex descriptors you associate with your render pipeline state. The second, more subtle, point is alignment and packing. If you use a SIMD type like

`vector_float3`

(`float3`

in C++/shader code), it will still occupy 16 bytes of memory and be aligned at 16-byte boundaries. If your data is actually tightly packed (i.e., a 3-vector is stored as 3 adjacent floats rather than four adjacent floats of which one is ignored dead-space), you must use the “packed” variants of these types when declaring them as struct members.`packed_float3`

, for example, is a type that occupies 12 bytes and is aligned at 4-byte boundaries, which probably fits your use case.Daren ShanThanks Warren,

I can use packed_float3 inside the shader, but in objective C what could I use for a packed float 3? simd only has packed_float2 and packed_float4…

Daren ShanI realized I could easily just use a custom struct in object c, my problem was I never changed the vertex descriptors. Thank you for all your help Warren.

IvanI have a question about the struct returned by the vertex shader,

struct ColoredVertex

{

float4 position [[position]];

float4 color;

};

How does metal know how to interpolate this? Is this an arbitrary struct or does it conform to a standard? If it’s arbitrary would it interpolate *anything* (e.g. nested structs, etc)?

Warren MooreBy default, all members (including structs contained recursively) are interpolated in a perspective-correct manner if they’re of a floating-point type. Integer-typed members take the value of the provoking vertex for the entire face (so-called

`flat`

interpolation). You can read about the various attributes you can apply to a member to get different interpolation behavior here.AnuragHi Warren,

Great material! I have completed the first 3 chapters and it is definitely helping although I have a very minimal Gfx background!

I faced this issue in both the clearscreen and draw the triangle projects, I implemented the code after understanding the material, eventually while trying to Run it, I just got a white blank screen in both the projects.

While trying to debug I figured the code goes to AppDelegate after which it goes to ViewController for some reason it wont goto MBEMetalView. After which I copied each file code from each of your github files, still the situation remains the same.

On the contrary when I clone and run your project it executes perfectly.

Hence, I am at the conclusion this has something to do with some project configuration/setting. I have spent a long time comparing your and mine project and they both seem the exact same.

Would you know why is this happening?

PS. I did use a very bruteforce method to debug but that is on account of being new to iOS development, new to Metal and new to Objective C.

Thank you,

Anurag

Warren MooreHey Anurag, thanks for the comment. I’m very curious to know what might differ between your project and mine. Can you upload your complete project somewhere so I can take a look?

AnuragThank you for the quick response! I appreciate how you are still active on this page!

I have uploaded it to a Github repo- https://github.com/anurag2493/Metal-By-Example.git

I hope it is not something very silly!

Warren MooreFortunately, this is pretty easy to fix. Open the Main.storyboard, select the View, and use the inspector to change its Custom Class name to MBEMetalView. The problem is that it’s currently instantiating a generic UIView instead of the custom subclass.

AnuragGreat! That helped! Thank you!

Looking to work through the book.

Mladen MikićHi Warren,

thank you for this tutorial. I have updated it with Swift for macOS.

https://github.com/Darkwonder/MetalTriangles

Best regards, Mladen