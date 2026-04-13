---
title: WebGPU for Metal Developers, Part One
url: https://metalbyexample.com/webgpu-part-one/
published: '2021-06-04'
source_blog: Metal by Example
source_site: https://metalbyexample.com
category: graphics
fetched: '2026-04-13'
---

Doing high-performance 3D rendering on the Web has always been a tricky proposition.

WebGL, in its quest for programmer familiarity and cross-platform ubiquity, adopted the API of OpenGL ES. As such it has never been capable of exploiting the full power of the underlying GPU, even as desktop APIs like DirectX 12, Metal, and Vulkan debuted and became popular. Furthermore, Apple has been slow to build out full support for WebGL 2: as of this writing, it remains an Experimental Feature in Safari).

Fortunately, the situation seems to be changing. After over four years in development by a working group in the W3C Consortium, the WebGPU API is hopefully on the cusp of stability and broad availability.

There are already several implementations of WebGPU across various browsers and operating systems, just as there are for WebGL. These implementations are written atop other APIs like Vulkan and Metal, which I will refer to as “backend APIs” below.

The purpose of this article series is to introduce Metal programmers to modern GPU programming on the Web. There are enough similarities between Metal and WebGPU that we can directly compare their respective APIs and shading languages. Even readers who are not familiar with Metal can hopefully benefit from this overview and the accompanying samples.

In Part One (this article), we will learn the fundamentals of the WebGPU API in Javascript, from scratch, culminating in a single, colored triangle in 2D. In [Part Two](https://metalbyexample.com/webgpu-for-metal-developers-part-two/), we look at a slightly more practical example of 3D terrain rendering.

If you want to view the samples embedded in this page, I recommend using a bleeding-edge browser like [Chrome Canary](https://www.google.com/chrome/canary/), as existing implementations vary significantly in their support for the WebGPU draft standard (at the time of this writing).

## Preparing to Draw

In contrast to native development, where we use [view](https://developer.apple.com/documentation/metalkit/mtkview) and [layer](https://developer.apple.com/documentation/quartzcore/cametallayer) classes to display drawable content, on the Web we use the [ <canvas>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/canvas) HTML element.

The core structure of the sample HTML looks like this:

<html lang="en"> <body> <canvas id="gpuCanvas" width="800" height="600"></canvas> </body> </html>

To draw into the canvas with WebGPU, we first need to know when the page has loaded. We do this by registering an event listener that calls a function called `main()`

. The main function in turn calls `init()`

, which does all necessary one-time object initialization:

async function main() { await init(); // … } async function init() { const adapter = await window.navigator.gpu.requestAdapter(); const device = await adapter.requestDevice(); // … use the device … } window.addEventListener('load', main);

The `main`

function is marked `async`

because it uses the `await`

keyword to suspend its execution while calling into asynchronous WebGPU APIs.

### Adapters and Devices

The first API we use is `window.navigator.gpu`

. A [GPU](https://www.w3.org/TR/webgpu/#gpu) is an object that allows us to request [adapters](https://gpuweb.github.io/gpuweb/#gpuadapter). An *adapter* is an implementation of WebGPU made available by a system. There may be multiple adapters, but in this case, we call `requestAdapter()`

with no parameters to get the default adapter.

The adapter, in turn, allows us to query the available features and limits of the implementation, as well as request [devices](https://gpuweb.github.io/gpuweb/#gpudevice). In this sample, we ask the adapter for the default device, which will be suitable for most purposes. As you might expect, a device in WebGPU is very similar to a `MTLDevice`

in Metal: with a device, you can create resources and submit work to the GPU.

### Getting the Canvas Context

To draw, we need to retrieve a *context* from the canvas. First, we use the `querySelector`

function to get a reference to the canvas element we created above, then we ask for its `gpupresent`

context, which gives us access to WebGPU resources associated with the canvas.

canvas = document.querySelector('#gpuCanvas'); context = canvas.getContext('gpupresent');

### Configuring the Swap Chain

To display what we draw on the screen, we need to configure the context’s *swap chain*. Abstractly, the swap chain is the pool of textures that we will render to and which will be shown on-screen. This is similar to how we configure the device and pixel format of an `MTKView`

or `CAMetalLayer`

.

context.configure({ device: device, format: 'bgra8unorm' });

By passing the device to the `configure()`

function, we create a linkage between the GPU and the canvas.

### Establishing the Draw Loop

If you haven’t used WebGL or done animation with Web technologies before, the way we set up the draw loop may seem a little odd.

JavaScript has a function called [ requestAnimationFrame](https://developer.mozilla.org/en-US/docs/Web/API/window/requestAnimationFrame) that schedules a function to be called the next time the browser decides it’s ready to repaint. However, the passed function is only called once: we are responsible for requesting the

*next*frame at the end of the

*current*frame if we want to render repeatedly. This leads to the following pattern:

function draw() { // … issue drawing commands … requestAnimationFrame(() => { draw(); }); }

Of course, unconditionally requesting drawing can be inefficient if the content being rendered hasn’t changed. We do so here only for demonstration purposes.

## The Command Submission Model

Just like Metal, WebGPU requires us to record GPU commands into a *command buffer* to submit them to the GPU for execution.

In contrast to Metal, WebGPU does not require you to explicitly create a command buffer *prior* to encoding commands. Instead, you create a [ command encoder](https://www.w3.org/TR/webgpu/#gpucommandencoder) directly from the device, and when you’re ready to submit a batch of commands for execution, you call the

`finish()`

function on the encoder. This function returns a command buffer that can be submitted to the device’s [command queue](https://www.w3.org/TR/webgpu/#gpuqueue).

To understand exactly how to submit rendering work to the GPU, we first need to understand the anatomy of render passes.

### Render Passes

Each frame is subdivided into one or more render passes. A *render pass* is a sequence of commands that consists of a load phase, one or more draw calls, and a store phase.

The outputs of a render pass are written to one or more [ attachments](https://www.w3.org/TR/webgpu/#color-attachments). In the simplest case, there is just one color attachment, and it stores the rendered image that will be displayed on the screen. Other scenarios may use several color attachments, a depth attachment, etc.

Each attachment has its own *load operation*, which determines its contents at the beginning of the pass, and *store operation*, which determines whether the results of the pass are stored or discarded. By providing a load value of `'load'`

, we tell WebGPU to retain the existing contents of the target; by providing a value (such as a color) instead, we indicate that the target should be “cleared” to that value.

To tell WebGPU which textures to draw into, we create a [ render pass descriptor](https://www.w3.org/TR/webgpu/#dictdef-gpurenderpassdescriptor), which is little more than a collection of attachments:

const clearColor = { r: 0.0, g: 0.5, b: 1.0, a: 1.0 }; const renderPassDescriptor = { colorAttachments: [{ loadValue: clearColor, storeOp: 'store', view: context.getCurrentTexture().createView() }] };

Here, we have specified that there is one color attachment, that we want to clear it to a particular color during the load phase, and that we want to store the results at the end of the pass. To indicate the texture to draw into, we get the current swap chain texture from the context, then create a [view](https://www.w3.org/TR/webgpu/#gpu-textureview) from it. This is analogous to asking a `CAMetalLayer`

for its [next drawable](https://developer.apple.com/documentation/quartzcore/cametallayer/1478172-nextdrawable).

(A *view* is a thin abstraction over a texture that allows us to refer to a subset of its mip levels and array elements (its so-called *subresources*). In Metal, a texture view is literally just [another texture](https://developer.apple.com/documentation/metal/mtltexture/1515409-newtextureviewwithpixelformat), but in WebGPU they are distinct types.)

### Encoding a Pass

The load and store operations of a render pass occur independently of whether the pass actually includes any draw calls. We can use this to clear the canvas to a solid color by beginning a render pass and immediately ending it:

const passEncoder = commandEncoder.beginRenderPass(renderPassDescriptor); // … optional draw commands … passEncoder.endPass();

If we were doing real work, we would use the render pass encoder to encode drawing commands. We’ll see an example of that shortly.

### Ending a Frame

device.queue.submit([commandEncoder.finish()]);

As mentioned above, finishing a command encoder produces a command buffer that can be submitted to the GPU. We do this by asking the device for its command queue and passing an array of command buffers to be enqueued for execution. Once the work is complete, the image will be displayed by the canvas.

The result of the above code is embedded below. Depending on when you’re reading this and which browser you’re using, you might see an error message. If everything is working correctly, you should see a solid blue box.

Now that we know the basics of setting up a canvas and encoding rendering work, let’s begin drawing in earnest. We’ll start with an overview of WebGPU’s all new shading language.

## A Brief Orientation to WGSL

Shaders in WebGPU are written in a language called [WebGPU Shading Language](https://www.w3.org/TR/WGSL/), abbreviated WGSL 1.

Modern shading languages have more similarities among them than differences. After all, their purpose is to provide a high-level syntax for the I/O and arithmetic operations available on the typical GPU.

Syntactically, WGSL borrows much from Rust. Functions definitions begin with `fn`

; return types appear after the parameter list, preceded by an arrow (`->`

); generics use angle brackets (e.g., `vec4<f32>`

). Scalar numeric types have terse names like `f32`

and `u32`

.

WGSL also has some similarities to Metal Shading Language (MSL). Attributes (e.g., `[[location(0)]]`

) use C++-style double square brackets. Varyings are returned from the vertex shader as a struct, and the interpolated fragment values are taken as a struct-valued parameter to the fragment shader (which may or not be of the same as the output type of the vertex shader, but must be [“compatible”](https://www.w3.org/TR/WGSL/#pipeline-compatibility)).

As an introduction to the language, we will look at the vertex and fragment shaders that will produce our first triangle.

### A Basic Vertex Shader

As in Metal Shading Language, we can define a struct that contains the outputs of our vertex shader. We are obligated to provide a `vec4<f32>`

(a four-element floating-point vector) containing the clip-space vertex position, attributed with `[[builtin(position)]]`

. In this sample, we also return a vertex color, which will be used by the fragment shader:

struct VertexOut { [[builtin(position)]] position : vec4<f32>; [[location(0)]] color : vec4<f32>; };

The vertex shader itself is a function attributed with `[[stage(vertex)]]`

, similar to MSL’s `vertex`

keyword. Vertex function parameters indicate where their values should be fetched from with `location`

attributes. We will see shortly how to create a mapping from these location indices to the vertex buffers we bind when drawing.

In this sample, the vertex function simply constructs an instance of the output struct, populates it with the fetched vertex data, and returns it:

[[stage(vertex)]] fn vertex_main([[location(0)]] position: vec4<f32>, [[location(1)]] color: vec4<f32>) -> VertexOut { var output : VertexOut; output.position = position; output.color = color; return output; }

### A Basic Fragment Shader

The fragment shader’s job is to return a color for its pixel based on its inputs. In this example, the output color is just the interpolated color from the rasterizer:

[[stage(fragment)]] fn fragment_main(fragData: VertexOut) -> [[location(0)]] vec4<f32> { return fragData.color; }

The `location`

attribute on the return type indicates the index of the color attachment to which the color should be written. In Metal, a single vector return value is inferred to correspond to the first color attachment. In WGSL, we are obligated to provide this index explicitly.

This completes the shader code for the sample. We’ll see in the next section how to incorporate this shader code into a complete render pipeline.

## Creating and Uploading Vertex Data

To have something to draw, we need to generate or load a mesh, perhaps from a 3D model file. In this sample, we’ll just be drawing one triangle, so we’ll specify its data by hardcoding it as a list of floats. Each vertex has a position and a color packed in memory in `X Y Z W R G B A`

order:

const vertices = new Float32Array([ 0.0, 0.6, 0, 1, 1, 0, 0, 1, -0.5, -0.6, 0, 1, 0, 1, 0, 1, 0.5, -0.6, 0, 1, 0, 0, 1, 1 ]);

To use this data on the GPU, we need to copy it into a *buffer*. As in Metal, we create buffers with the device. The `createBuffer`

function takes a [ buffer descriptor](https://www.w3.org/TR/webgpu/#GPUBufferDescriptor), containing the size of the buffer, some usage flags, and whether the buffer should be “mapped” for writing at creation.

If we map the buffer at creation, it is ready to have data copied into it immediately. Since we will use the buffer as a vertex buffer when drawing, we pass the `GPUBufferUsage.VERTEX`

flag. Since we want to use it as the destination of a copy operation, we also include the `GPUBufferUsage.COPY_DST`

flag.

vertexBuffer = device.createBuffer({ size: vertices.byteLength, usage: GPUBufferUsage.VERTEX | GPUBufferUsage.COPY_DST, mappedAtCreation: true });

The buffer’s [ getMappedRange()](https://www.w3.org/TR/webgpu/#dom-gpubuffer-getmappedrange) function returns an

`ArrayBuffer`

which can be wrapped in a typed array of our choosing to copy data into it, via the [function:](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/set)

`set()`

new Float32Array(vertexBuffer.getMappedRange()).set(vertices);

We then unmap the vertex buffer, which indicates we’re done changing its contents. The new contents are implicitly copied to the GPU.

vertexBuffer.unmap();

## Render Pipelines

Now that we have some shaders and some vertex data, we’re ready to assemble our render pipeline. This consists of several steps involving many different descriptor types, so we’ll go one step at a time.

### Creating Shader Modules

First, we need the shaders as a string. In this sample, the shaders are contained in an HTML `<script>`

element, but they could be sourced from an external file, typed in by the end user, or included as a JavaScript string literal.

We use the device’s `createShaderModule()`

function to turn the shader string into a *shader module*, from which we can get shader functions. Different implementations will do different things behind the scenes, but a Metal implementation might create a [ MTLLibrary](https://developer.apple.com/documentation/metal/mtllibrary) at this point, since there is a natural parallel between a WebGPU shader module and a Metal shader library.

const shaderNode = document.querySelector('#shaders'); const shaderModule = device.createShaderModule({ code: shaderNode.textContent });

There is nothing exactly like an [ MTLFunction](https://developer.apple.com/documentation/metal/mtlfunction) in WebGPU. Instead, functions are uniquely identified by their module and their name.

### Describing Vertex Data

As in Metal, we need to describe the layout of our vertex data up-front so it can be incorporated into the render pipeline. This description, called a *vertex state*, consists of an array of layouts, with each layout containing one or more *attributes*. This directly corresponds to Metal concept of a [vertex descriptor](https://developer.apple.com/documentation/metal/mtlvertexdescriptor), with the difference that the attributes are contained by the layouts rather than living in a separate container.

Each layout has a *stride*, which indicates the number of bytes between vertices, and a *step mode*, which indicates whether data should be fetched per-vertex or per-instance 2.

Each member of the attributes array describes a single vertex attribute, including its *offset* from the start of vertex data, a *format*, and a *shader location*. This shader location is what is used to map from vertex buffers to the vertex shader parameters attributed with `location(n)`

.

Mirroring the layout of our vertex data, we define two vertex attributes (position and color), both with format `'float32x4'`

, which maps to the WGSL `vec4<f32>`

type.

Putting all of this together, here is the complete list of vertex layouts for this sample:

const vertexBuffers = [{ attributes: [{ shaderLocation: 0, // position offset: 0, format: 'float32x4' }, { shaderLocation: 1, // color offset: 16, format: 'float32x4' }], arrayStride: 32, stepMode: 'vertex' }];

### Render Pipeline Descriptors

Render pipelines contain most of the data necessary to configure the programmable and fixed-function portions of the GPU to execute rendering commands. So it’s no surprise that the *render pipeline descriptor* is the most complex descriptor we’ve seen so far.

Each pipeline stage (vertex and fragment) has an associated entry point and state. In the case of the vertex stage, the state is the previously-defined list of vertex buffer layouts. In the case of the fragment stage, the state is an array of [color target state](https://www.w3.org/TR/webgpu/#dictdef-gpucolortargetstate)s, which describe the format of the render pass attachments that will be targeted by the pipeline. Each color target state also has an optional *blend state*, which controls fixed-function alpha blending. We don’t use alpha blending in this sample, so we omit this portion of the state.

The final piece of state that is incorporated into the render pipeline is the primitive state. At its most basic, this is just an indication of which type of primitive we will be drawing. In Metal, we specify this at the time we encode draw calls, but since some APIs require it up-front, we provide it as part of the pipeline configuration.

Bringing all of this together, here is the complete definition of our sample render pipeline descriptor:

const pipelineDescriptor = { vertex: { module: shaderModule, entryPoint: 'vertex_main', buffers: vertexBuffers }, fragment: { module: shaderModule, entryPoint: 'fragment_main', targets: [{ format: 'bgra8unorm' }] }, primitive: { topology: 'triangle-list' } };

Notice that the names of the entry points match the names of the functions we wrote in our shader source. We use a primitive topology of `'triangle-list'`

, since we will be drawing a list of triangles (really just one triangle).

### Creating a Render Pipeline

Now that we’ve slogged through all of the above concepts, actually creating a pipeline is simple:

renderPipeline = device.createRenderPipeline(pipelineDescriptor);

## Drawing

To encode rendering work, we create a command encoder and begin a render pass as before:

const passEncoder = commandEncoder.beginRenderPass(renderPassDescriptor);

Equipped with a pipeline and a vertex buffer, we bind each of them and issue our first draw call:

passEncoder.setPipeline(renderPipeline); passEncoder.setVertexBuffer(0, vertexBuffer); passEncoder.draw(3);

The `draw()`

function has a number of parameters, most of them optional, but the first one—the vertex count—is the most important. In this case, because we’re drawing a single triangle, it is 3.

We then end the pass, finish encoding, and enqueue the work as before.

The result of this is embedded below. In browsers with an up-to-date WebGPU implementation, it should display a single colored triangle.

## Conclusion and a Look Ahead

In spite of the humble result, we’ve covered a lot of conceptual ground:

- Canvases and contexts
- Adapters and devices
- Command encoders, render passes, and attachments
- Uploading and describing vertex data
- Basics of WGSL, vertex and fragment shaders
- Configuring and creating render pipelines
- Encoding draw calls

In [Part 2](https://metalbyexample.com/webgpu-part-two), we look at intermediate topics including texture loading, displacement mapping, and instancing.

-
For better and for worse, WebGPU is an open standard predominantly designed by a consortium of several large companies. Without delving into corporate politics, it is obvious that WGSL is the product of
[compromise](https://lobste.rs/s/2niccd/tint_google_s_proposed_shader_language)among these entities. Despite the inconveniences associated with introducing Yet Another Shading Language, having a textual shading language designed for safety and ease of conversion to backend shading languages seems like the best outcome we could hope for.[↩](https://metalbyexample.com#fnref-833-1) -
This is a natural extension point for tessellation. If WebGPU’s tessellation model looks like Metal’s, vertex fetch could be used to fetch per-patch data in addition to per-vertex data.
[↩](https://metalbyexample.com#fnref-833-2)

Marcin IgnacFor those wondering how to create a commandEncoder it’s just one line of code missing above

const commandEncoder = device.createCommandEncoder();

Peter WongGreat article, this really helped me get started/understand some WebGPU fundamentals (I’m not even a Metal developer).

Just noticed the iframed examples were not working on Chrome Canary (as of Sep 14, 2021 version 96.0.4642.2), because of recent change in how to get the canvas context…

Before: context = canvas.getContext(“gpupresent”);

After: context = canvas.getContext(“webgpu”);

Reference:

– https://github.com/gpuweb/gpuweb/pull/1930

– https://chromium-review.googlesource.com/c/chromium/src/+/3027671

Warren MooreThanks, Peter! I’ve updated the code so that it works in Chrome Canary Version 96.0.4652.0.