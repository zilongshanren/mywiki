---
title: 'Writing a Modern Metal App from Scratch: Part 1'
url: https://metalbyexample.com/modern-metal-1/
published: '2018-07-10'
source_blog: Metal by Example
source_site: https://metalbyexample.com
category: graphics
fetched: '2026-04-13'
---

## Getting Started

This article is a quick introduction to how to use the Metal, MetalKit, and Model I/O frameworks in Swift. If you know your way around UIKit or Cocoa development, you should be able to follow along for the most part. Some things like shaders and matrices will be foreign to you, but you can learn them as you go about exploring Metal on your own. The purpose here is to give you a template to build on.

If you want to follow along without copy-pasting the code yourself, you can [clone this GitHub repository](http://github.com/metal-by-example/modern-metal) and follow the instructions there.

First things first. Use Xcode to create a new project from the iOS Single View App template. Add `import MetalKit`

at the top of the `ViewController.swift`

file. We could use the Game template instead and have some of the boilerplate written for us, but writing it out long-hand will give us more of an appreciation for the moving parts. The Game template also includes a lot of moving parts that get in the way of understanding the basics.


If you’re using the Git repository to follow along, check out the first tag to view the code at this point:

```
git checkout start
```


## Configuring the Metal View

Add a property of type `MTKView`

to your view controller:

var mtkView: MTKView!

`MTKView`

is a class provided by the MetalKit framework that makes working with Metal much easier. It handles things like creating an instance of the special `CALayer`

subclass that talks to UIKit for you and driving the animation loop.

You could make this an `@IBOutlet`

if you want to add your `MTKView`

with Interface Builder instead of in code.

In your view controller’s `viewDidLoad`

implementation, instantiate the `MTKView`

, add it as a subview of the root view and configure it with Autolayout:

mtkView = MTKView() mtkView.translatesAutoresizingMaskIntoConstraints = false view.addSubview(mtkView) view.addConstraints(NSLayoutConstraint.constraints(withVisualFormat: "|[mtkView]|", options: [], metrics: nil, views: ["mtkView" : mtkView])) view.addConstraints(NSLayoutConstraint.constraints(withVisualFormat: "V:|[mtkView]|", options: [], metrics: nil, views: ["mtkView" : mtkView]))

So that the view can create resources on our behalf, we create the Metal default device and set it on our view:

let device = MTLCreateSystemDefaultDevice()! mtkView.device = device

We will also use the Metal device to create resources ourselves, as well as the objects that dispatch commands to the GPU 1.

Finally, we need to tell the view the format of the color texture we will be drawing to. We will choose `bgra8Unorm`

, which is a format that uses one byte per color channel (red, green, blue, and alpha (transparency)), laid out in blue, green, red, alpha order. The `Unorm`

portion of the name signifies that the components are stored as *unsigned* 8-bit values, so that the values 0-255 map to 0-100% intensity (or 0-100% opacity, in the case of the alpha channel).

mtkView.colorPixelFormat = .bgra8Unorm

If you build and run the project on a device at this point, you’ll probably just see a blank white screen. That’s expected—we still have a while to go before we’re drawing 3D content.

## Creating the Renderer Class

Create a new file called `Renderer.swift`

. Also add `import MetalKit`

at the top of this file, since our renderer will need to use classes from Metal and MetalKit.

Create a new class named `Renderer`

that conforms to the `MTKViewDelegate`

protocol. This protocol declares the methods that the `MTKView`

will call to perform rendering, and to notify you when its size changes. Here is the basic implementation that we will be expanding on in the coming sections.

class Renderer: NSObject, MTKViewDelegate { func mtkView(_ view: MTKView, drawableSizeWillChange size: CGSize) { } func draw(in view: MTKView) { } }

The `mtkView(_:drawableSizeWillChange:)`

method is called when the view changes size. This lets us update any resources or properties that might be resolution-dependent, most particularly our projection matrix. More on that later. For now we’re just building the scaffolding.

The `draw(in:)`

method is similar to `UIView`

‘s `draw(_:)`

method, in that it redraws the contents of the view. The difference here is that we’ll be using Metal to render the view’s contents instead of Core Graphics.

Since our renderer will rely on a Metal device to do anything useful, add a property to hold onto one, as well as a property to hold onto the `MTKView`

we are responsible for rendering into. Add an initializer that configures these properties:

let device: MTLDevice let mtkView: MTKView init(view: MTKView, device: MTLDevice) { self.mtkView = view self.device = device super.init() }

### Setting the Renderer as the View’s Delegate

Back in the `ViewController`

class, add a property to hold a strong reference to a `Renderer`

object:

var renderer: Renderer!

At the end of the `viewDidLoad`

method, create the renderer instance, passing the view, and then assign the renderer as the delegate of the `MTKView`

:

renderer = Renderer(view: mtkView, device: device) mtkView.delegate = renderer

Now that we’ve set up communication between the view and the renderer, we’ll be doing most of our work in the `Renderer`

class.

To advance to this point in the Git repository, check out the `step1_1`

tag:

```
git checkout step1_1
```


## Loading Resources with Model I/O

Back in Renderer.swift, import the ModelI/O framework:

import ModelIO

Model I/O is a framework that makes it extremely easy to load 3D data. Model I/O is also built to make it easy to render this data with Metal.

Add a method to `Renderer`

that will be responsible for creating or loading the various resources we will be using: `loadResources()`

. Call it from the initializer:

init(view: MTKView, device: MTLDevice) { self.mtkView = view self.device = device super.init() loadResources() } func loadResources() { // ... }

Find an OBJ model file that you want to render. I chose the classic Utah teapot (available [here](http://graphics.cs.williams.edu/data/meshes.xml#7)). You may need to open your file in a modeling program and ensure it fits in a unit cube to use the code in this article unmodified. If that doesn’t mean anything to you, just use the teapot and forge ahead anyway.

Add the OBJ file to your Xcode project.

Inside the `loadResources()`

method, create a file URL that points to where your OBJ file will be in the app bundle:

let modelURL = Bundle.main.url(forResource: "teapot", withExtension: "obj")!

### The Vertex Descriptor

To tell Model I/O how we want the model’s data to be laid out in memory, we create something called a *vertex descriptor*. A vertex descriptor is metadata that supplies a name, position, and format (data type) for each *attribute* of the vertices that comprise our model data. In our case, we will have attributes for vertex position, vertex normal (i.e., surface direction), and texture coordinates. Still inside the `loadResources()`

method, add:

let vertexDescriptor = MDLVertexDescriptor() vertexDescriptor.attributes[0] = MDLVertexAttribute(name: MDLVertexAttributePosition, format: .float3, offset: 0, bufferIndex: 0) vertexDescriptor.attributes[1] = MDLVertexAttribute(name: MDLVertexAttributeNormal, format: .float3, offset: MemoryLayout<Float>.size * 3, bufferIndex: 0) vertexDescriptor.attributes[2] = MDLVertexAttribute(name: MDLVertexAttributeTextureCoordinate, format: .float2, offset: MemoryLayout<Float>.size * 6, bufferIndex: 0) vertexDescriptor.layouts[0] = MDLVertexBufferLayout(stride: MemoryLayout<Float>.size * 8)

This looks complicated, but it’s conveying a simple idea. It basically says that each vertex’s properties are arranged in memory with the following layout, where each box is a single `Float`

value:

| position | position | position | normal | normal | normal | texCoords | texCoords |
|---|---|---|---|---|---|---|---|
| x | y | z | x | y | z | x | y |

We’ll need to use this vertex descriptor later on, so add a property for it to the renderer class:

var vertexDescriptor: MTLVertexDescriptor!

Then, in `loadResources()`

, populate it using the `MTKMetalVertexDescriptorFromModelIO`

utility function provided by MetalKit for translating between Model I/O’s vertex descriptor type and Metal’s vertex descriptor type, which differ in ways that don’t concern us right now:

self.vertexDescriptor = MTKMetalVertexDescriptorFromModelIO(vertexDescriptor)

### Buffer Allocators

In addition to telling Model I/O how to layout our vertices, we need to tell it where to put them. Or rather, we need to tell it how to create space to put them in. This is done with an object called a *buffer allocator*. We will use a concrete implementation of Model I/O’s buffer allocator protocol provided by MetalKit, since we want to render our content with Metal. This class is called `MTKMeshBufferAllocator`

. Add this line to your `loadResources()`

function:

let bufferAllocator = MTKMeshBufferAllocator(device: device)

### Creating an `MDLAsset`


Now we can ask Model I/O to actually create the asset that represents the complete contents of our model file, including the vertices themselves, and the mesh data that expresses how the vertices are connected together into triangles:

let asset = MDLAsset(url: modelURL, vertexDescriptor: vertexDescriptor, bufferAllocator: bufferAllocator)

An asset can contain many things, including lights, cameras, and meshes. For now, we just care about the meshes. This completes our implementation of `loadResources()`

for now.

### Meshes and Submeshes

In Model I/O parlance, a *mesh* is a collection of vertex buffers and submeshes. A *submesh* contains an index buffer and additional data about how many indices should be rendered when it is drawn, and the type of primitive (triangles, lines, points, etc.) it should be drawn as.

Add a property to the renderer that will hold the collection of meshes:

var meshes: [MTKMesh] = []

Note that we’re dealing here with `MTKMesh`

es rather than `MDLMesh`

es. There *is* an `MDLMesh`

class, but we won’t need to deal with it directly. To get our collection of `MTKMesh`

es we use a convenience method provided by the `MTKMesh`

class:

do { (_, meshes) = try MTKMesh.newMeshes(asset: asset, device: device) } catch { fatalError("Could not extract meshes from Model I/O asset") }

The `newMeshes`

method returns both the “original” `MDLMesh`

objects (which we don’t care about) and the converted `MTKMesh`

objects as a *tuple*. Since we only want to keep the `MTKMesh`

es, we *destructure* the tuple and store only the second part in our `meshes`

property.

Believe it or not, that’s all it takes to prepare the data from our model file to be rendered with Metal. However, we’re really just getting started. Now we need to talk about shaders.

To sync up your local clone of the repository, check out the `step1_2`

tag:

```
git checkout step1_2
```


## Shaders

A *shader* is a small program that runs on the GPU, and in our sample project, we’ll need to deal with two flavors of shaders: vertex and fragment shaders. A *vertex shader* runs once per vertex, each time we draw our geometry. The vertex shader’s job is to transform vertex data from the coordinate space in which it was modeled into the coordinate space expected by the rest of the Metal rendering pipeline, which is called *clip space*.

### Clip Space

Clip space is a coordinate space 2 that describes which portion of the scene is visible to our virtual camera. Specifically, coordinates that are between -1 and 1 in the x and y axes and between 0 and 1 in the z axis in clip space are within the camera’s field of view. Any triangles outside of this box will not appear on the screen, and any triangle that

*intersects*this box will be modified so that only its visible portion continues to the later stages of the pipeline. The process of removing invisible triangles entirely is called

*culling*, and the process of preserving only the visible portion of partially-visible triangles is called

*clipping*, hence the name of clip space.

How we actually get from so-called model space to clip space is beyond the scope of this guide, but briefly, we do it by multiplying the positions of our vertices by a sequence of specially-computed matrices that result in our desired transformation 3. We’ll see some examples of transformation matrices below, including the

*projection matrix*, which represents the last step that takes our vertices into clip space.

### The Shaders File

Create a new Metal File in your project called `Shaders.metal`

. This file will hold all of the shader functions we write. This file is not in Swift, but a variant of the C++ programming language called the Metal Shading Language.

Note the lines at the top of the file:

#include <metal_stdlib> using namespace metal;

These lines import the Metal Standard Library into the global namespace. The Metal Standard Library contains many types and functions for doing vertex and matrix math, which is most of what we’ll be doing in our shaders.

### The Vertex Shader

First, we need to declare a couple of data structures that will hold the input and output parameters of our vertex function:

struct VertexIn { float3 position [[attribute(0)]]; float3 normal [[attribute(1)]]; float2 texCoords [[attribute(2)]]; }; struct VertexOut { float4 position [[position]]; float4 eyeNormal; float4 eyePosition; float2 texCoords; };

The `VertexIn`

struct maps exactly to the vertex descriptor we created when loading our model file with Model I/O: two three-component floating-point vectors (`float3`

), representing position and the surface normal, and a two-component floating-point vector (`float2`

) holding the texture coordinates.

The `VertexOut`

struct describes the data we want to return from our vertex function: the position in clip space, attributed with `[[position]]`

so Metal knows what it is; the surface normal in camera (“eye”) coordinates; the position of the vertex in eye coordinates; and the texture coordinates, which will simply be passed through because they already live in the appropriate coordinate space. We need to know the normal in the coordinate space of the camera in order to do lighting calculations. [4](https://metalbyexample.com#fn-645-4)

Finally, we need a structure that holds the data that doesn’t vary among vertices: so-called *uniform data*:

struct Uniforms { float4x4 modelViewMatrix; float4x4 projectionMatrix; };

The `Uniforms`

struct contains a pair of matrices. The model-view matrix is a matrix that transforms the vertices and normals of the model into camera coordinates. (Note: we’re ignoring the differences between how positions and normals transform, which would turn out badly if we were performing certain transformations like non-uniform scaling, but we’ll ignore that for now for simplicity’s sake).

Now that we have described the data we want to operate on, let’s write our vertex function. It looks like this:

vertex VertexOut vertex_main(VertexIn vertexIn [[stage_in]], constant Uniforms &uniforms [[buffer(1)]]) { VertexOut vertexOut; vertexOut.position = uniforms.projectionMatrix * uniforms.modelViewMatrix * float4(vertexIn.position, 1); vertexOut.eyeNormal = uniforms.modelViewMatrix * float4(vertexIn.normal, 0); vertexOut.eyePosition = uniforms.modelViewMatrix * float4(vertexIn.position, 1); vertexOut.texCoords = vertexIn.texCoords; return vertexOut; }

The first parameter is the incoming vertex data, an instance of the `VertexIn`

struct described above. This parameter is attributed with `[[stage_in]]`

to signify that it is built for us by loading data according to the vertex descriptor. The second parameter is a reference to an instance of the `Uniforms`

struct, which will hold the matrices we use to transform our vertices.

Inside the function, we first instantiate the output vertex structure. Then, we multiply the vertex position by the model-view matrix and the projection matrix (by convention, we read matrix multiplication from right to left). This moves the vertex position from model space to clip space, which is needed by the next stages of the pipeline. Then, we multiply the object normal by just the model-view matrix, which leaves it in eye space. We do this because we will want to calculate things like lighting and reflections in eye space instead of model space. For the same reason, we also compute the eye space *position* of the vertex. Finally, we pass through the texture coordinates and return the transformed vertex structure.

### Rasterization

After each vertex is returned from the vertex function, the GPU determines which pixels on the screen could possibly be contained by its corresponding triangle, then *interpolates* the values we returned from the vertex function to create fragments. This job is specifically done by a portion of the pipeline called the *rasterizer*, and it’s not something we control directly. A *fragment* is a potential contributor to the color of a pixel. Some fragments don’t wind up affecting their corresponding pixel (because they’re hidden behind another surface or because we choose to discard them intentionally), but we still need to compute a color for each fragment. This is the job of the fragment shader.

### The Fragment Function

The fragment shader (or more precisely, *fragment function*) is called once per fragment to determine what its color should be. It can make this determination by performing lighting calculations, sampling colors from a texture, or any other computation. For the time being, we’ll just return a solid red color for every fragment. We’ll write a more sophisticated fragment shader shortly.

fragment float4 fragment_main(VertexOut fragmentIn [[stage_in]]) { return float4(1, 0, 0, 1); }

### Libraries, Functions, and Render Pipelines

To maximize performance, Metal obligates you to compile your vertex and fragment shaders together into a *render pipeline state object* before drawing anything. We will do this work in a new function called `buildPipeline()`

, which should be called from the renderer’s initializer:

// ... loadResources() buildPipeline()

Among other things, we will need references to a pair of objects that represent the shaders we just wrote. These are instances of the `MTLFunction`

type, and we get functions by first creating a *library*. A library is simply a collection of named functions, and the *default library* contains all of the functions that are compiled into our app bundle, like the ones we just wrote.

To get a reference to the default library, we ask the device for it (this is the first code in our new `buildPipeline()`

method:

guard let library = device.makeDefaultLibrary() else { fatalError("Could not load default library from main bundle") }

If we fail to get the default library, we won’t be doing any drawing, so we abort the program.

Assuming we now have a valid library, we can create our function objects from it. These objects are of type `MTLFunction`

, and they represent the functions we wrote in the Metal Shading Language above. Add these lines to `buildPipeline()`

below the point where we created the library:

let vertexFunction = library.makeFunction(name: "vertex_main") let fragmentFunction = library.makeFunction(name: "fragment_main")

Now that we have our functions, we can start to configure the object that will tell Metal about the pipeline we want to create, the *render pipeline descriptor*:

let pipelineDescriptor = MTLRenderPipelineDescriptor() pipelineDescriptor.vertexFunction = vertexFunction pipelineDescriptor.fragmentFunction = fragmentFunction

In addition to the functions that comprise the program that will run on our GPU, we need to tell Metal the format (pixel layout) of the textures we will be drawing into. For now, we only set the color texture’s format:

pipelineDescriptor.colorAttachments[0].pixelFormat = mtkView.colorPixelFormat

We also need to set the vertex descriptor we generated previously, so that the pipeline knows how data is laid out in our vertex buffers:

pipelineDescriptor.vertexDescriptor = vertexDescriptor

Finally, we need to actually create the render pipeline state. This invokes the compiler that actually turns our shaders into the machine code that will run on the GPU, and returns the pipeline state object we will use when rendering. First, add a property to the `Renderer`

class to hold it:

var renderPipeline: MTLRenderPipelineState!

We finish the `buildPipeline()`

method by asking the device to create our render pipeline state object, aborting the app if we fail to do so:

do { renderPipeline = try device.makeRenderPipelineState(descriptor: pipelineDescriptor) } catch { fatalError("Could not create render pipeline state object: \(error)") }

## Drawing

### Command Queues

Finally, we’re getting close to actually issuing drawing commands, but in order to actually issue commands to the GPU, we need to create the object that manages access to the GPU: the *command queue*.

As is now the pattern, add a property to the renderer to hold the command queue:

let commandQueue: MTLCommandQueue

Create the queue near the top of the initializer:

// ... self.device = device self.commandQueue = device.makeCommandQueue()! super.init() // ...

The command queue stores a sequence of *command buffers*, which we will create and write GPU commands into. Commands consist of things like state-setting operations (which describe how things should be drawn and what resources they should be drawn with) as well as *draw calls*, which tell the GPU to actually draw geometry, causing our vertex and fragment functions to be called and producing the pixels that wind up on the screen.

### Command Buffers and Command Encoders

In our app, we will generate one command buffer per frame. When asked to render a frame by our `MTKView`

, we use the following code to create the command buffer into which we will *encode* our rendering commands:

func draw(in view: MTKView) { let commandBuffer = commandQueue.makeCommandBuffer()! // ... }

Encoding is the process of translating from API calls into the actual commands understood by the GPU.

To send uniform data into our vertex function, we need to create a Swift struct that corresponds to the `Uniforms`

struct in our Metal code. Place this near the top of the Renderer.swift file:

import simd struct Uniforms { var modelViewMatrix: float4x4 var projectionMatrix: float4x4 }

Back in the `draw(in:)`

implementation, we ask for a couple of objects from our view: the render pass descriptor and the current drawable:

func draw(in view: MTKView) { let commandBuffer = commandQueue.makeCommandBuffer()! if let renderPassDescriptor = view.currentRenderPassDescriptor, let drawable = view.currentDrawable { } // ... }

The *render pass descriptor* tells Metal which textures we will actually be drawing into. Recall that we previously configured the render pipeline state with the pixel format of one of these textures by setting the `pixelFormat`

property on its first color attachment. The render pass descriptor has corresponding color attachments that represent the actual textures (images) we will be drawing into. Fortunately, the `MTKView`

actually manages these textures for us, so we simply ask for its preconfigured render pass descriptor for the current frame.

A *drawable* is an object that holds a color texture and knows how to present it on the screen. Behind the scenes, the `MTKView`

has already set the current drawable’s texture as the texture of its first color attachment. This means that whatever color is returned by the fragment function will be written into the corresponding pixel of this texture. Once we’re done drawing, we will issue a command to present this texture on the screen, which will make our 3D scene visible to the user.

Once we have these objects, we can create a *render command encoder*, which is the object that actually writes commands into the command buffer:

let commandEncoder = commandBuffer.makeRenderCommandEncoder(descriptor: renderPassDescriptor)!

When drawing, we will iterate over the meshes and submeshes we created earlier from our Model I/O asset, drawing them as we go. The general structure looks like this, though there are still some other pieces to fill in:

for mesh in meshes { for submesh in mesh.submeshes { commandEncoder.drawIndexedPrimitives(/* ... */) } }

### Getting Data into the Vertex Function

To tell our vertex function where to get data from, we need to tell it which buffers contain the data. We will accomplish this in two separate ways, depending on the type of data.

First, we will set up the buffer that contains our vertex data with the `setVertexBuffer(_:offset:index:)`

method. The `offset`

parameter indicates where *in the buffer* the data starts, while the `at`

parameter specifies the *buffer index*. The buffer index corresponds to the `bufferIndex`

property of the attributes specified in our vertex descriptor; this is what creates the linkage between how the data is laid out in the buffer and how it is laid out in the struct taken as a parameter by our vertex function.

Second, we will set up the buffer that contains the uniform data. Because this data is so small, we would like to avoid creating a dedicated buffer for it. Fortunately, the render command encoder has a method called `setVertexBytes(_:length:index:)`

that enables exactly this. This method takes a pointer to some data that will be written into a buffer that is managed internally by Metal. In this case, the buffer index specified by the last parameter matches the index of the `[[buffer()]]`

attribute in the parameter list of the vertex function. In this sample app, we dedicate buffer index 1 to our uniform buffer.

#### Transformation Matrices

In order to have uniform data to send into the vertex function, we need to generate a couple of matrices: the model-view matrix and the projection matrix. The actual math for these is beyond the scope of this article, but for completeness, here are the matrix utilities we will be using (put this in a file named “MathUtilities.swift” or similar):

import simd extension float4x4 { init(scaleBy s: Float) { self.init(float4(s, 0, 0, 0), float4(0, s, 0, 0), float4(0, 0, s, 0), float4(0, 0, 0, 1)) } init(rotationAbout axis: float3, by angleRadians: Float) { let x = axis.x, y = axis.y, z = axis.z let c = cosf(angleRadians) let s = sinf(angleRadians) let t = 1 - c self.init(float4( t * x * x + c, t * x * y + z * s, t * x * z - y * s, 0), float4( t * x * y - z * s, t * y * y + c, t * y * z + x * s, 0), float4( t * x * z + y * s, t * y * z - x * s, t * z * z + c, 0), float4( 0, 0, 0, 1)) } init(translationBy t: float3) { self.init(float4( 1, 0, 0, 0), float4( 0, 1, 0, 0), float4( 0, 0, 1, 0), float4(t[0], t[1], t[2], 1)) } init(perspectiveProjectionFov fovRadians: Float, aspectRatio aspect: Float, nearZ: Float, farZ: Float) { let yScale = 1 / tan(fovRadians * 0.5) let xScale = yScale / aspect let zRange = farZ - nearZ let zScale = -(farZ + nearZ) / zRange let wzScale = -2 * farZ * nearZ / zRange let xx = xScale let yy = yScale let zz = zScale let zw = Float(-1) let wz = wzScale self.init(float4(xx, 0, 0, 0), float4( 0, yy, 0, 0), float4( 0, 0, zz, zw), float4( 0, 0, wz, 0)) } }

These functions allow us to express the basic operations of rotation, scale, translation, and projection.

#### The Model Matrix

Jumping back into the `draw(in:)`

method, we can put these matrix utilities to use in building the matrices we want to consume in our vertex function.

Suppose we want to scale and rotate our model to position and orient it in the world. For my teapot, I chose the following model matrix that transforms from the model coordinates into world coordinates:

let modelMatrix = float4x4(rotationAbout: float3(0, 1, 0), by: -Float.pi / 6) * float4x4(scaleBy: 2)

This matrix scales up the model by a factor of two in all dimensions and rotates it slightly clockwise about the positive Y axis.

#### The View Matrix

The *view matrix*, which describes how our camera is positioned in the world, looks like this:

let viewMatrix = float4x4(translationBy: float3(0, 0, -2))

This matrix causes all vertices to be moved -2 units along the Z axis, which points straight out of the screen. This has the effect of positioning our camera at +2 units along this axis. The view matrix is basically the *inverse* of the transformation that describes how the camera is positioned and oriented in virtual space.

#### The Model View Matrix

We combine these matrices together to get the model-view matrix:

let modelViewMatrix = viewMatrix * modelMatrix

#### The Projection Matrix

Now we need to construct the *projection matrix*, whose job it is to take eye coordinates (the result of the model-view matrix applied to model coordinates) and transform them into clip space coordinates:

let aspectRatio = Float(view.drawableSize.width / view.drawableSize.height) let projectionMatrix = float4x4(perspectiveProjectionFov: Float.pi / 3, aspectRatio: aspectRatio, nearZ: 0.1, farZ: 100)

One of the projection matrix parameters is the screen aspect ratio. Since clip space has a square aspect ratio along its x and y axes, but our screen is a rectangle, we need to apply a non-uniform scale to counteract this mismatch. The `nearZ`

and `farZ`

parameters determine which distances from the eye correspond to the near and far planes of the clipping space volume. Thus, anything nearer to the camera than 0.1 units or further than 100 units will be clipped and not visible.

#### Setting Uniform Data on the Render Command Encoder

Now that we have these two matrices, we can construct a uniforms struct from them:

var uniforms = Uniforms(modelViewMatrix: modelViewMatrix, projectionMatrix: projectionMatrix)

We use the `setVertexBytes(_:length:index:)`

method mentioned above to write this struct into a buffer managed by Metal at buffer index 1:

commandEncoder.setVertexBytes(&uniforms, length: MemoryLayout<Uniforms>.size, index: 1)

The uniform values will now be available inside the vertex function as the parameter attributed with `[[buffer(1)]]`

.

### Draw Calls

We’re now (finally!) ready to issue the sequence of draw calls that will actually render the model to the screen.

As mentioned above, we will iterate over the collection of meshes and submeshes in our model (in the case of the teapot, there is only one mesh comprised of two submeshes). First, we set our render pipeline state on the command encoder so it knows which vertex and fragment function to use to draw our geometry:

commandEncoder.setRenderPipelineState(renderPipeline)

Now, we iterate over the meshes, setting the vertex buffer that corresponds to each mesh at buffer index 0, then iterating over its submeshes and issuing draw calls:

for mesh in meshes { let vertexBuffer = mesh.vertexBuffers.first! commandEncoder.setVertexBuffer(vertexBuffer.buffer, offset: vertexBuffer.offset, index: 0) for submesh in mesh.submeshes { let indexBuffer = submesh.indexBuffer commandEncoder.drawIndexedPrimitives(type: submesh.primitiveType, indexCount: submesh.indexCount, indexType: submesh.indexType, indexBuffer: indexBuffer.buffer, indexBufferOffset: indexBuffer.offset) } }

The `drawIndexedPrimitives`

method tells Metal to render a sequence of *primitives*, or shapes. The `type`

parameter specifies what type of primitive to draw (often, this will be `.triangles`

; here, we just pass the submesh’s `primitiveType`

, derived from the model file we loaded earlier). The subsequent parameters specify how many indices will be used, what type they are (unsigned 16-bit or unsigned 32-bit integer), and the buffer in which the indices are located. Metal will iterate over this index buffer, creating one triangle for each set of three indices. The vertex located at each of these indices will be read from the previously-set mesh vertex buffer and passed into the vertex function. Subsequently, rasterization and fragment shading will be performed for each pixel inside the triangle’s boundary, and the resulting colors will be written into the color texture.

### Finishing Up the Frame

Once we’re done drawing, we need to call `endEncoding()`

on our render command encoder to end the pass—and the frame:

commandEncoder.endEncoding()

Ending encoding signifies that we won’t be doing any more drawing with this render command encoder. If we wanted to draw additional objects, we would need to do that before calling `endEncoding`

.

#### Presenting the Drawable

In order to get our rendered content on the screen, we have to expressly *present* the drawable whose texture we’ve be drawing into. We do this with a call on the command *buffer*, rather than the command encoder:

commandBuffer.present(drawable)

#### Committing the Command Buffer

Once we’re done encoding commands into the command buffer, we *commit* it, so its queue knows that it should ship the commands over to the GPU.

commandBuffer.commit()

A millisecond or two later, drawing will be done, and our image will be ready for display.

![](../../assets/226f86df3da370f9.jpg)

#### Simple Animation

In order to make the teapot spin, we can replace the hard-coded angle in our model matrix construction with a value that changes over time. First, we add a property to our renderer to store the elapsed time:

var time: Float = 0

Then, we accumulate time by adding a fraction of a second each time we draw, based on how often we expect our view to be drawing:

time += 1 / Float(mtkView.preferredFramesPerSecond) let angle = -time let modelMatrix = float4x4(rotationAbout: float3(0, 1, 0), by: angle) * float4x4(scaleBy: 2)

You could speed up or slow down the animation by multiplying time by an additional factor.

To view the code for this step, use `git checkout step1_3`

.

## Conclusion

I’ve tried to keep the number of concepts in this article to a bare minimum, but we’ve covered an astonishing amount of ground, from a blank screen to a spinning 3D object! Despite the density of the material, all of this only took about 200 lines of code, and we’ve laid a great foundation for future work. In subsequent articles, we’ll talk about basic lighting, materials and textures, managing a scene graph with multiple objects, and basics of interaction with 3D scenes. Stay tuned!

-
If you’re already feeling overwhelmed, don’t fret. The purpose of this series is to give you the code to get you started with Metal, without explaining foundational graphics concepts or the core concepts of Metal itself. By working through this series, you’ll get familiar with how the pieces fit together, and there are plenty of other articles on this site that explain Metal in much greater detail.
[↩](https://metalbyexample.com#fnref-645-1) -
A 3-D
*coordinate space*is specified by a set of axes and an origin (0, 0, 0). You might be familiar with seeing points expressed as a tuple of values (x, y, z); these values express how far along each axis you move to locate the point (for example, the point (1, 2, 3) is 1 unit along the x axis, plus 2 units along the y axis, plus 3 units along the z axis). Much of the math of computer graphics involves moving from one coordinate space to another, for the purposes of making it easier to compute certain things.[↩](https://metalbyexample.com#fnref-645-2) -
There’s a lot going on here, so I’ll try to explain further. A 3-D model, such as the teapot we added to the project, has a “local” origin. The vertices of the model are defined relative to this origin. The coordinate space in which the model is specified is called
*model space*. In order to position the model in our virtual world, we need to describe its location and orientation, placing it in so-called “world space.” The way we do this is by building a “transformation,” which is a description of how to move from one coordinate space to another. The way we do this is with a matrix, but we’ll talk more about that shortly. For now, just know that there is one more intermediate coordinate space that we need to move through (variously called “eye space,” “view space,” or “camera space”) before we get to clip space, which is what the GPU wants us to produce in our vertex shader.[↩](https://metalbyexample.com#fnref-645-3) -
At this stage, it’s natural to be confused about what a normal is. Essentially, a normal vector is a vector that is
*perpendicular*to a surface at a given point. For example, the normal of the surface of a desk points straight up because the surface of the desk is horizontal. In the case of a sphere, the normal always points “out” from the center of the sphere through the point in question.[↩](https://metalbyexample.com#fnref-645-4)

Mariusgreat intro, Warren! welcome back to writing 🙂

David GavilanNice! I haven’t used Model I/O. I should give it a try! It looks quite straightforward 🙂

The main problem I have with Metal is that you need a real device for testing. When you develop an iOS app, you need to take screenshots in different devices and aspect ratios, and I usually use the simulator for that (and fastlane if you want automation). But Metal doesn’t work in the simulator. It doesn’t even build, which it’s also a bit annoying… I only have an iPhone and an iPad, so I can’t generate all the screenshots by myself… 🙁

Astemir EleevIt is very nice that you started wring again! Please keep going! The world needs to know more about Metal

João VarelaHi David

I managed to rewrite part of the project done by Warren to run on Macs. If Warren allows me and if someone is interested in that, I can share it in GitHub.

J.

Warren MooreBy all means, share! I’ll happily link to your fork/repo from the post.

João VarelaOK, the link to the Mac version is as follows:

https://github.com/aslr/modern-metal-mac

João VarelaHI Warren

I posted a link, but apparently it was removed. I don’t know if it was by you or by an overeager Akismet anti-spam action. If it was the latter, please send me an email and I will send the link to you directly.

João

CraigKeep up the good work, old friend!

AbstractionHi Warren.

Is Metal using Right hand system like opengl?

I thought it used left hand system.

Thanks,

Warren MooreMetal doesn’t have an opinion about the handedness of coordinate systems until you get into clip space. Metal’s clip space is left-handed in the sense that +X is right, +Y is up, and +Z is “into” the screen. However, screen coordinates are right-handed, since the viewport transform flips the Y axis. All of this agrees with Direct3D’s conventions (including the fact that clip space is a hemicube rather than a cube, as in OpenGL). I prefer right-handed world and view systems with Y up, but that’s an arbitrary choice. The projection matrix is responsible for making eye space “agree” with clip space.

AbstractionThanks for your reply.

It took me sometime to understand.

I am using left-handed system for projection matrix.

I also invert z-axis on the shader ( in.position.z = -1.0f * in.position.z; ) to correctly display blender obj models which has -Z axis forward

I am thinking if it is possible to use right-handed system for projection matrix and don’t invert z-axis on the shader.

Warren MooreI suppose if you use a model matrix with Z inverted, and also reverse the winding order of the mesh, it should be possible to use one projection matrix to handle both types of models (those originating in a left-handed space, and those originating from a right-handed space).

Jared JonesYou have an error in your perspective projection matrix.

Your last row shows: float4( 0, 0, wz, 1))

But it should be: float4( 0, 0, wz, 0))

Warren MooreYou’re absolutely right. Sorry for the error. I’ve fixed this in the article and patched it on GIthub, but it’s something for readers to be aware of if they’re using git to work through the checkpoints in the article.

DariusWarren

I don’t know that if I’m mistaking or not, but There are 3 SIMD Library available for us now in 2019 and frankly I’m really confused by this:

SIMD in swift 5.

simd Module in Accelerate.

simd framework that is in the Xcode documentation.

If I’m writing an app that is working with Metal API and Swift, I always start typing all their names (specially for float4 and matrix4x4 ) until Xcode stops bugging me about it.

The problem starts when I create a bridge header for swift so that he starts to working with this c style structs. I saw this on Apple sample codes. Instead of defining uniforms or other data type that you want to pass to your shaders, both in shader file and your swift files, you just define them ones in a header file and exposed it to both metal and Swift.

I know that in this two Part tutorial you refused to do so for the sake of simplicity.

I already saw you answer to a question like this on:

https://stackoverflow.com/questions/51790490/explaining-the-different-types-in-metal-and-simd

but I’m confused as hell. Specially after this recent update that all the float4 types in swift side are now deprecate. so we have to use simd_float4 or vector_float4 which is essentially is equivalent to simd_float4 which is equivalent to SIMD4

So, the questions are;

1-What the hell is going on?

2-What is the relationship between these frameworks?

3-Why they are so many?

4-How technically they could be exposed to both C code and swift code and at the same time ?

Warren MooreGood questions! I’d break it down like this:

1) SIMD types in Swift have undergone a higher-than-average number of redesigns and deprecations than most APIs. I don’t know the reasons for this, but I’m sure it’s due in part to a combination of internal differences of opinion and limited time to do the work. I do think it’s especially pitiable that all of these changes confuse API users for very little apparent benefit to code brevity, safety, or robustness.

2) I believe that the types and functions linked from the Accelerate documentation are actually those exposed by simd.framework, and therefore there are only two discrete SIMD type definitions in Swift (ignoring Metal Shading Language for now). Basically, the types exposed via simd.framework are designed to be those that can be used universally in C, C++, and Swift code. It used to be the case that you could just write

`vector_float4`

, or later,`simd_float4`

, and you’d get a type that could be used anywhere, because of clever uses of namespaces and the like.These days, Swift insists on using generic SIMD types like

`SIMD4<T>`

instead, deprecating obvious and tidy typenames like`float4`

. This is worse in every possible way (in my opinion) than the previous arrangement, except for consistency with the larger SIMD types now available in Swift. The underlying implementations are either equivalent or actually identical.To answer the question, the types now available in the Swift standard library (as of Swift 4.1 or 5) correspond exactly in size and alignment requirements to the types available via simd.framework (and the Metal standard library), as they always have. The only thing that’s changed from an end-user perspective is that these types now have to be spelled out more verbosely (but you can always add your own typealiases that override the now-deprecated types, and I’ve heard many accounts of people doing exactly that).

3) A foolish insistence on consistency.

4) You’ll need to use a C or Objective-C header to share struct types between (Objective-C) code and Swift. Swift won’t warn on the deprecated types when importing structs via bridging headers. This has the positive benefits of giving stronger guarantees about struct layout as well.

If you want to share structs across C, Swift,

andMetal shaders, you’ll need to do some import and typedef trickery, but it can be made to work.