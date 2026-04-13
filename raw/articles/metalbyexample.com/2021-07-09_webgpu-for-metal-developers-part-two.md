---
title: WebGPU for Metal Developers, Part Two
url: https://metalbyexample.com/webgpu-part-two/
published: '2021-07-09'
source_blog: Metal by Example
source_site: https://metalbyexample.com
category: graphics
fetched: '2026-04-13'
---

In the [previous article](https://metalbyexample.com/webgpu-part-one) we took a first look at WebGPU and got familiar with the essential pieces of the API, the command submission model, and drawing in 2D from a static buffer.

In this article, we’ll look much deeper into WebGPU. Some of our topics include:

- texture creation and sampling
- displacement mapping in WGSL
- bind groups for efficient resource binding
- indexed and instanced draw calls

## Overview of the Sample

The basic structure of the sample remains the same as last time: request an adapter, request a device, configure the swap chain, and set up the draw loop.

Building on this base, we will render an infinite landscape for the camera to meander around in. The terrain will consist of a tiled planar mesh that is displaced with a heightmap. [this post](https://blogs.igalia.com/itoral/2016/10/13/opengl-terrain-renderer-rendering-the-terrain-mesh/) by Iago Toral.

If you are viewing this post in a browser that supports WebGPU, you can see the final result embedded below.

## Generating a Terrain Mesh

The terrain mesh is a plane consisting of vertices laid out in a grid and indices connecting the vertices in a regular topology (two triangles per grid square). The code for this is straightforward, so I won’t reproduce it here. The Toral article linked above has good illustrations and explanations.

The vertex data consist of interleaved positions and texture coordinates. We omit the vertex normals, since we’ll be dynamically generating them in our vertex shader. This type of mesh is often rendered as a set of triangle strips, but for simplicity, we use regular old triangles, which requires six indices per grid square (comprising two triangles).

The mesh generator produces a `Float32Array`

containing vertex data and a `Uint32Array`

containing index data.

As in the previous sample, we map the buffers at creation so we can immediately copy data into them. For the vertex data, there’s nothing new at all, but I include the code here for completeness:

vertexBuffer = device.createBuffer({ size: vertices.byteLength, usage: GPUBufferUsage.VERTEX | GPUBufferUsage.COPY_DST, mappedAtCreation: true }); new Float32Array(vertexBuffer.getMappedRange()).set(vertices); vertexBuffer.unmap();

Creating the index buffer is very similar, but we change the usage hint to `GPUBufferUsage.INDEX`

, and the intermediate array is a `Uint32Array`

, since our indices are stored as an array of 32-bit integers.

indexBuffer = device.createBuffer({ size: indices.byteLength, usage: GPUBufferUsage.INDEX | GPUBufferUsage.COPY_DST, mappedAtCreation: true }); new Uint32Array(indexBuffer.getMappedRange()).set(indices); indexBuffer.unmap();

As before, we store the buffers in global variables so we have access to them later when drawing.

The dimensions and number of grid subdivisions of the terrain patch are configurable in the sample code. I chose parameters that seemed to work well together, but you’re welcome to do your own tweaking.

## Textures

There are myriad uses for textures, so we should get acquainted with how to use them in WebGPU. In this sample, we use textures in two distinct ways. First, we texture map the terrain to provide more detail than can be achieved with vertex colors. Second, we displace the flat terrain mesh with a heightmap texture that defines the altitude of the terrain at each vertex.

To perform either of these techniques, we first need to know how to create textures and load them with image data. We’ll also briefly introduce depth textures in this section.

### Loading Textures from Files

Web browsers are great at loading and displaying images, so we can use their existing faculties to get image data that we can copy into textures. Since we need to load more than one such texture, we will create a utility function, `loadTexture()`

.

To load an image, we create an `Image`

instance and set its `src`

property to a URL (which can be absolute or relative to the document). We then use the `decode()`

function to load the image’s contents into memory:

async function loadTexture(path) { const image = new Image(); image.src = path; await image.decode();

Decoding an image does not make its bytes available in a way that we can use directly; for that, we can create an `ImageBitmap`

:

let imageBitmap = await createImageBitmap(image);

We continue the `loadTexture()`

implementation by creating the actual texture object and copying the image’s contents into it.

### Creating Textures

To create a texture, we first populate a [ texture descriptor](https://www.w3.org/TR/webgpu/#dictdef-gputexturedescriptor). The texture descriptor requires familiar properties such as the size, dimension (

`1d`

, `2d`

, `3d`

, etc.), and pixel format. We also supply three usage flags: `GPUTextureUsage.COPY_DST`

(which signals that a resource is the destination of a copy operation); `GPUTextureUsage.RENDER_ATTACHMENT`

; and `GPUTextureUsage.SAMPLED`

, which indicates that we will be sampling from the texture in shader functions.We can then use the device’s `createTexture()`

function to create the texture:

const textureSize = { width: image.width, height: image.height, depth: 1 }; const texture = device.createTexture({ size: textureSize, dimension: '2d', format: 'rgba8unorm', usage: GPUTextureUsage.COPY_DST | GPUTextureUsage.RENDER_ATTACHMENT | GPUTextureUsage.SAMPLED });

To copy the image bytes into the texture, we use the `copyExternalImageToTexture()`

function on our device’s queue. This is analogous to calling [ replaceRegion:mipmapLevel:withBytes:bytesPerRow:](https://developer.apple.com/documentation/metal/mtltexture/1515464-replaceregion) on a

`MTLTexture`

.

[1](https://metalbyexample.com#fn-848-1)The copy operation requires a [source](https://gpuweb.github.io/gpuweb/#gpu-image-copy-external-image), a [destination](https://gpuweb.github.io/gpuweb/#gpu-image-copy-texture-tagged), and the extent of the image to copy into the texture (which in our case is simply the entire image):

device.queue.copyExternalImageToTexture({ source: imageBitmap }, { texture: texture, mipLevel: 0 }, textureSize);

Once we have copied the image data to the texture, we return the texture object from our `loadTexture()`

function:

return texture; } // end of loadTexture()

To get filtered texture data in our shaders, we need to create one or more samplers.

### Samplers and Sampling

In Metal, we have two options when it comes to samplers: preconfigured [sampler states](https://developer.apple.com/documentation/metal/mtlsamplerstate) and `constexpr`

samplers in shader source. WebGPU only supports the former.

As you might reasonably expect, we create a sampler with a [ sampler descriptor](https://www.w3.org/TR/webgpu/#dictdef-gpusamplerdescriptor). This object has essentially the same properties as a

[.](https://developer.apple.com/documentation/metal/mtlsamplerdescriptor)

`MTLSamplerDescriptor`

In the sample code, we specify that the U and V coordinates should repeat (wrap around), that the magnification filter mode should use bilinear interpolation, and that minification should use nearest filtering. We intentionally *don’t* set a mip filter. Since support for creating mipmaps in the WebGPU API is an [open question](https://github.com/gpuweb/gpuweb/issues/386) at the time of this writing, we deal with the artifacts that naturally arise from minification without mips 2.

Like other resource types, samplers are created with the device object. We call the `createSampler()`

function to create a sampler state from our descriptor:

linearSampler = device.createSampler({ addressModeU: 'repeat', addressModeV: 'repeat', magFilter: 'linear', minFilter: 'nearest' });

We can now bind the sampler alongside our buffers and textures to use them in our shaders.

### Depth Textures

To use depth buffering, we need to create a depth texture 3. A descriptor for a depth texture is the same as that for an ordinary 2D texture, but we specify a depth (or depth-stencil) pixel format and also a usage flag of

`GPUTextureUsage.RENDER_ATTACHMENT`

to signify that the texture will be used as a depth attachment in our render pass:depthStencilTexture = device.createTexture({ size: { width: canvas.width, height: canvas.height, depth: 1 }, dimension: '2d', format: 'depth32float', usage: GPUTextureUsage.RENDER_ATTACHMENT });

As we saw previously, we don’t use textures as attachments directly; instead we need to create a *view* that points to the *subresource* we want to render to. Since the swap chain’s drawable changes every frame, we created its view dynamically when creating our render pass descriptor, but since the depth buffer is static, we create a single view up-front that we can reuse every frame:

depthStencilTextureView = depthStencilTexture.createView();

## Shader Topics

With all of our resources created, it’s now time to turn back to shaders. This section will introduce the new shader concepts used by the sample. For full details, you’ll probably want to read the sample code itself and consult the linked references.

### Resources and Uniform Data

First, we need to declare the resources used by our shader functions. We will defer a full discussion of the `group`

and `binding`

attributes to a later section, but for now, just notice that we will be binding a sampler, a couple of textures, and a buffer containing uniform data.

[[group(0), binding(0)]] var linearSampler: sampler; [[group(0), binding(1)]] var colorTexture: texture_2d<f32>; [[group(0), binding(2)]] var heightmap: texture_2d<f32>; [[group(1), binding(0)]] var<uniform> uniforms : Uniforms;

The `f32`

type parameter to the `texture_2d`

type indicates that we want to receive single-precision floating-point color values when sampling our textures.

The `Uniforms`

struct is a custom type we declare to hold transform matrices and other uniform data. We will see its definition later.

### Displacement Mapping

We will perform rudimentary displacement mapping on our plane mesh to simulate terrain. In the vertex shader, we sample the heightmap to get the displacement along the model Y axis. We then sample adjacent texels to get an approximation to the displaced surface normal 4. We use these samples to produce the new model-space vertex position and normal. We then multiply these by the model-view-projection matrix and normal matrix in the ordinary way.

Let’s walk through the vertex shader a few lines at a time. The vertex function signature is very similar to the one we used to render a single triangle:

[[stage(vertex)]] fn vertex_main([[location(0)]] position: vec4<f32>, [[location(1)]] texCoords : vec2<f32>) -> VertexOut

We first set up some constants that represent the various scaling factors that will affect our position and normal calculations. These could also be provided as uniforms if the displacement needed to be dynamic:

{ let patchSize: f32 = 50.0; let heightScale: f32 = 8.0; let d: vec3<f32> = vec3<f32>(1.0 / 256.0, 1.0 / 256.0, 0.0); let dydy: f32 = heightScale / patchSize;

Since we don’t have access to [screen-space derivatives](http://www.aclockworkberry.com/shader-derivative-functions/) in the vertex function, we must explicitly provide a mip level (“lod”) when sampling the texture. Sampling is done with the [ textureSampleLevel](https://www.w3.org/TR/WGSL/#texturesamplelevel) function. We find the displacement and approximate gradient by taking three samples: one centered on the vertex, one to the right, and one below (in texture space):

let height : f32 = textureSampleLevel(heightmap, linearSampler, texCoords, 0.0).r; let dydx : f32 = height - textureSampleLevel(heightmap, linearSampler, texCoords + d.xz, 0.0).r; let dydz : f32 = height - textureSampleLevel(heightmap, linearSampler, texCoords + d.zy, 0.0).r;

We then calculate the model position by offsetting the vertex vertically by the (scaled) displacement, and the model normal by normalizing the approximate gradient:

let modelPosition: vec4<f32> = vec4<f32>(position.x, position.y + height * heightScale, position.z, 1.0); let modelNormal: vec4<f32> = vec4<f32>(normalize(vec3<f32>(dydx, dydy, dydz)), 0.0);

The rest of the vertex shader plays out as usual: we transform the position and normal by the appropriate matrices, pass through the texture coordinates, and return the vertex struct:

let modelViewMatrix: mat4x4<f32> = uniforms.modelViewMatrix; let modelViewProjectionMatrix: mat4x4<f32> = uniforms.modelViewProjectionMatrix; var output : VertexOut; output.position = modelViewProjectionMatrix * modelPosition; output.eyePosition = modelViewMatrix * modelPosition; output.normal = (modelViewMatrix * modelNormal).xyz; output.texCoords = texCoords; return output; }

Note that we generate both a clip space position **and** an eye-space position, since we’re going to do our lighting in eye space. Speaking of lighting…

### Lighting

As we did with the vertex function, let’s step through the fragment function one line at a time. Our signature looks just like the one from the previous sample. We receive our varyings as a struct and return a fragment color that will be blended into the primary color attachment:

[[stage(fragment)]] fn fragment_main(fragData: VertexOut) -> [[location(0)]] vec4<f32> {

We declare some lighting constants: the light intensity and the light direction (in eye space). These, like the terrain constants above, could be passed in as uniforms instead.

let lightColor: vec3<f32> = 2.0 * vec3<f32>(0.812, 0.914, 1.0); let L: vec3<f32> = normalize(vec3<f32>(1.0, 1.0, 1.0));

To determine the diffuse light contribution, we need the normal in eye space (`N`

) and the direction to the light (`L`

). We find the diffuse factor in the [ordinary way](https://www.scratchapixel.com/lessons/3d-basic-rendering/introduction-to-shading/diffuse-lambertian-shading):

let N: vec3<f32> = normalize(fragData.normal.xyz); let diffuseFactor: f32 = clamp(dot(N, L), 0.0, 1.0);

To repeat the terrain color texture over the surface of each terrain patch, we multiply the texture coordinates by a scalar. This is an arbitrary constant that can be tuned to taste. We sample the texture at these scaled coordinates to get the base surface color. Since we are in a fragment shader, we can use the [ textureSample](https://www.w3.org/TR/WGSL/#texturesample) function (without specifying an explicit lod).

The lit surface color is the product of the diffuse weight, the light intensity, and the sampled base color:

let texCoordScale: f32 = 4.0; let baseColor: vec3<f32> = textureSample(colorTexture, linearSampler, fragData.texCoords * texCoordScale).rgb; let litColor: vec3<f32> = diffuseFactor * lightColor * baseColor;

### Fog

Since we only render a limited number of terrain tiles in the the vicinity of the camera, distant tiles will appear to pop in and out as the camera moves around. To hide this unsightly artifact, we want to apply fog to the lit color so that it fades out to the sky color in the distance.

We can cheaply simulate fog by blending from the lit color of the terrain to the sky color based on the distance of the eye to the fragment being shaded.

First, let’s set up some constants that describe the color of the fog and the minimum and maximum (eye-space) distances over which it will apply:

let fogColor: vec3<f32> = vec3<f32>(0.812, 0.914, 1.0); let fogStart: f32 = 3.0; let fogEnd: f32 = 50.0;

The fragment’s distance in eye space is simply the length of the eye-space position vector. The fog blending factor is calculated to make the color fall off linearly from the start distance to the end distance of the fog:

let fogDist: f32 = length(fragData.eyePosition.xyz); let fogFactor: f32 = clamp((fogEnd - fogDist) / (fogEnd - fogStart), 0.0, 1.0);

The final color of the fragment is a linear combination of the lit color and the sky color:

let finalColor: vec3<f32> = (fogColor * (1.0 - fogFactor)) + (litColor * fogFactor); return vec4<f32>(finalColor, 1.0); } // end of fragment_main()

With our shaders sorted out, we’re ready to combine them into a render pipeline.

## Creating the Render Pipeline

The render pipeline descriptor for this sample is quite similar to the previous one. We will first update the vertex state so it matches our terrain mesh.

### Vertex State

The vertex state mirrors the layout of the vertex data we created above. We have two attributes: a 4-element position and a 2-element set of texture coordinates. They are interleaved. This, then, is the definition of the vertex state:

const vertexBuffers = [{ attributes: [{ format: 'float32x4', // position shaderLocation: 0, offset: 0 }, { format: 'float32x2', // texCoords shaderLocation: 1, offset: 16 }], arrayStride: 24, stepMode: 'vertex' }];

Since each vertex has six floats of (packed) data, the stride of the buffer is 24 bytes.

### Render Pipeline Descriptors

The chief difference between the previous render pipeline descriptor and the one for this sample is the introduction of depth buffering. In addition to the vertex and fragment states we already had, which remain unchanged, we add a fixed-function *depth-stencil state*. The depth-stencil state specifies the depth texture’s format, the depth comparison function, and whether depth write is enabled.

In Metal, we would create a [MTLDepthStencilState](https://developer.apple.com/documentation/metal/mtldepthstencilstate) to contain this state. WebGPU needs it up front.

One other slight change we make to the render pipeline descriptor is the introduction of [ back-face culling](https://www.khronos.org/opengl/wiki/Face_Culling). For scenes like smooth terrain, backfaces comprise relatively little of the geometry for any given viewpoint (as long as we’re above the ground!), but in other situations, back-facing geometry can approach 50% of the scene, even when occlusion culling and frustum culling are being used.

To enable culling, we specify which *winding* is front-facing. We choose counterclockwise, denoted by the string `ccw`

. The cull mode is `back`

, meaning faces wound *clockwise* from the perspective of the camera will be eliminated.

Here is our complete render pipeline descriptor:

renderPipeline = device.createRenderPipeline({ vertex: { module: shaderModule, entryPoint: 'vertex_main', buffers: vertexBuffers }, fragment: { module: shaderModule, entryPoint: 'fragment_main', targets: [{ format: 'bgra8unorm' }], }, depthStencil: { format: 'depth32float', depthWriteEnabled : true, depthCompare: 'less' }, primitive: { topology: 'triangle-list', frontFace: 'ccw', cullMode: 'back' }, });

We then create the render pipeline itself as before.

Now that we have a render pipeline, we need to talk about how to efficiently feed it with our new resources.

## Bind Groups

In WebGPU, we don’t set individual resources through an API like `setTexture:index:`

or `setSampler:index:`

as we can in Metal. Instead, resources are bound in collections called bind groups.

A *bind group* is an object that represents a collection of resources that can all be bound at once. This can be significantly more efficient than binding resources one at a time, and we can partition our bind groups by how often resource bindings change (per-frame, per-instance, etc.) to minimize the work done by the driver.

Bind groups are created by passing a *bind group descriptor* to the device’s [ createBindGroup()](https://www.w3.org/TR/webgpu/#dom-gpudevice-createbindgroup) function. The bind group descriptor has a layout and an array of entries.

A *bind group layout* describes which stages the bind group’s resources are visible to. We have the option of creating our own bind group layouts, but it’s easier to request them from a previously compiled pipeline via reflection with the [ getBindGroupLayout()](https://www.w3.org/TR/webgpu/#dom-gpupipelinebase-getbindgrouplayout) function.

A *bind group entry* describes a single resource to be bound in its containing bind group. It has a `binding`

index and a `resource`

, which is the actual resource that will be bound.

We will use two separate bind groups: one that holds the resources related to texturing, and another that holds uniform data.

The first bind group holds the sampler, the terrain color texture, and the terrain heightmap texture:

frameConstantsBindGroup = device.createBindGroup({ layout: renderPipeline.getBindGroupLayout(0), entries: [{ binding: 0, resource: linearSampler }, { binding: 1, resource: colorTexture.createView() }, { binding: 2, resource: heightmapTexture.createView() }] });

The second bind group has a single entry: the buffer containing our instance data.

instanceBufferBindGroup = device.createBindGroup({ layout: renderPipeline.getBindGroupLayout(1), entries: [{ binding: 0, resource: { buffer: instanceBuffer } }], });

Since the set of resources we use when drawing doesn’t change from frame to frame, we can create these bind groups up front and use them repeatedly.

Referring back to the resource binding declarations in our shaders, notice that their layout exactly corresponds to our bind group definitions: the `group`

attribute maps to the bind group layout index, and the `binding`

attribute maps to the binding index specified in the corresponding bind group entry.

## Render Pass Descriptor Depth Buffer Attachments

As in the previous article, our render pass descriptor has a single color attachment that refers to the swap chain’s current drawable texture.

Since we’re drawing in 3D now, we need a depth buffer to ensure that geometry gets sorted correctly. In WebGPU, we achieve this by adding a depth-stencil attachment that refers to the depth texture we created earlier. We also configure the depth and stencil aspects of the attachment with their own load and store actions.

Here is the complete definition of the render pass descriptor:

const renderPassDescriptor = { colorAttachments: [{ loadValue: clearColor, storeOp: 'store', view: swapChain.getCurrentTexture().createView() }], depthStencilAttachment: { depthLoadValue: 1.0, depthStoreOp: 'clear', stencilLoadValue: 0, stencilStoreOp: 'store', view: depthStencilTextureView } };

We choose to clear the depth buffer to its maximum value by setting the `depthLoadValue`

to 1.0. Combined with the previously-configured depth comparison function of `less`

, this means nearer geometry will occlude farther geometry, which is what we want. We set the `depthStoreOp`

to `discard`

to signify that we don’t want to keep the depth buffer contents beyond the pass, which can be a significant optimization on some GPUs.

We don’t care about the load and store actions of the stencil buffer, but we are required to provide them, even if (as in this case) our depth-stencil texture has no storage for stencil values!

## Drawing

We are finally ready to put all of these new resources and shaders to good use by encoding some draw calls. In this section we will look at two techniques that allow us to draw more geometry more efficiently: indexed drawing and instancing.

### Indexed Drawing

Since vertices are often used by multiple primitives, we generated an index buffer when creating our mesh. This means that each vertex in the vertex buffer is unique, and the duplication moves to the index buffer, which is a much more compact representation.

First, as before, we set the render pipeline and vertex buffer on the pass encoder, so the GPU knows which shaders to use and which vertex data to use.

passEncoder.setPipeline(renderPipeline); passEncoder.setVertexBuffer(0, vertexBuffer);

Then, we set our two previously created bind groups at their respective group indices. This informs the GPU which resources we want to use in our shaders.

passEncoder.setBindGroup(0, frameConstantsBindGroup); passEncoder.setBindGroup(1, instanceBufferBindGroup);

To do indexed drawing, we need a list of indices that indicate how our vertices should be stitched together. As mentioned above, this is just the index buffer we created when generating our terrain mesh. Since our indices are 32-bit integers, we indicate this when binding the index buffer.

passEncoder.setIndexBuffer(indexBuffer, 'uint32');

We use a slightly different draw function than the one we used before to do non-indexed drawing. The `drawIndexed()`

function takes the index count as its first parameter:

passEncoder.drawIndexed(patchIndexCount);

### Instanced Drawing

So far, we have only been drawing a single mesh with each draw call. Often, though, we find that we want to draw the same mesh multiple times with different transforms (and potentially other unique data). In these cases, we can use *instancing*. Instancing allows us to draw multiple mesh instances with a single call, by providing per-instance data in a separate buffer.

Similar to how shaders extract per-vertex attributes from the bound vertex buffers, they can also extract per-instance data.

When instancing, we can use the same resource bindings as before. Instead of writing a single set of uniform data to the uniforms buffer, we write as many instances as we want to draw.

We have been deferring a discussion of the actual `Uniforms`

struct that contains our uniform data, so let’s look at it now:

struct Instance { modelViewMatrix: mat4x4<f32>; modelViewProjectionMatrix : mat4x4<f32>; }; [[block]] struct Uniforms { instances : array<Instance, 9>; };

The per-instance data consist of two 4×4 matrices: the model-view matrix and model-view-projection matrix. We have already seen these in action in the vertex shader.

We wrap an array of these `Instance`

structs in the `Uniforms`

type. The generic `array`

type takes two parameters: the type of object stored in the array, and the count (in this case, 9). The `block`

attribute on the `Uniforms`

struct indicates that its storage is a buffer object.

To load the per-instance uniform data in the shaders, we index into the uniforms buffer with the *instance ID*. The instance ID is a “built-in” vertex shader input that indicates the index of the instance that is currently being drawn. We get it by adding a parameter to our vertex function:

[[builtin(instance_index)]] instanceID : u32

We can then index into the `instances`

array to retrieve the matrices for the current instance:

let modelViewMatrix: mat4x4<f32> = uniforms.instances[instanceID].modelViewMatrix; let modelViewProjectionMatrix: mat4x4<f32> = uniforms.instances[instanceID].modelViewProjectionMatrix;

The remainder of the vertex shader is unchanged.

To encode instanced draw calls, we add a second parameter to the [ drawIndexed()](https://www.w3.org/TR/webgpu/#dom-gpurenderencoderbase-drawindexed) function, which indicates the number of instances to render:

passEncoder.drawIndexed(patchIndexCount, instanceCount);

## Animation and Dynamic Uniforms

Since this post is exceptionally long already, I won’t go into the details of constructing the animated model and view transforms for the terrain patches.

The sample code includes a minimal matrix math library. In practice, one would probably use a more robust library like [glMatrix](https://glmatrix.net/). As we calculate the transform matrices, we write them into a `Float32Array`

, and once we have all of them, we copy them into the instance uniform buffer using the GPU queue’s [ writeBuffer()](https://www.w3.org/TR/webgpu/#dom-gpuqueue-writebuffer) function:

device.queue.writeBuffer(instanceBuffer, 0, instanceData, 0, instanceData.length);

This is a different method than we used previously to copy data to the GPU. Rather than explicitly mapping the destination buffer, we let the implementation decide how to best copy the data. In a Metal-backed implementation, this might or might not entail first copying to a staging buffer and then blitting.

By updating the uniforms array each time we draw, we cause the camera to move around the terrain, and we also dynamically determine where we should draw instances of the terrain mesh to cover the field of view.

## Results and Conclusion

In this post we’ve covered an enormous amount of ground (no pun intended):

- Creating and populating textures
- Texture sampling and displacement mapping in WGSL
- Depth buffering
- Bind groups
- Dynamically updating uniform data
- Indexed and instanced draw calls

I hope this pair of articles have been useful as you begin (or continue) your WebGPU journey. I don’t anticipate writing additional articles on Web graphics, but I continue to be confident that WebGPU is shaping up to be a good candidate for the next ten years of high-performance graphics on the Web and beyond.

-
On some implementations and hardware, the
`copyExternalImageToTexture()`

function might first copy the data to a*staging buffer*, then*blit*to the texture itself. For related considerations in Metal, consult[this documentation page](https://developer.apple.com/library/archive/documentation/3DDrawing/Conceptual/MTLBestPracticesGuide/ResourceOptions.html).[↩](https://metalbyexample.com#fnref-848-1) -
For details, see Lance Williams’s classic paper,
[“Pyramidal Parametrics.”](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.210.5694&rep=rep1&type=pdf). To opine for just a moment, I would prefer that WebGPU provide an API for mipmap generation to make it easier for less advanced users to get good results, instead of omitting such an API on the principle that it can’t cover every possible use case.[↩](https://metalbyexample.com#fnref-848-2) -
On some hardware—notably Apple GPUs—depth data never has to be stored to a texture. Instead, the depth for each pixel can be stored in
*tile memory*and discarded at the end of the pass, unless it is needed by a subsequent pass. Nevertheless, WebGPU currently does not have a notion oftextures, so we are obligated to create a memory-backed texture.*memoryless*[↩](https://metalbyexample.com#fnref-848-3) -
The normals produced in this way are not very high-quality.
[This post](http://thedemonthrone.ca/projects/rendering-terrain/rendering-terrain-part-20-normal-and-displacement-mapping/)produces better normals by baking a normal map from the heightmap using many more samples. This is preferable, especially when the heightmap is known in advance.[↩](https://metalbyexample.com#fnref-848-4)