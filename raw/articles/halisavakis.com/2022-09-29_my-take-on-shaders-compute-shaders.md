---
title: 'My take on shaders: Compute shaders'
url: https://halisavakis.com/my-take-on-shaders-compute-shaders/
published: '2022-09-29'
source_blog: Technically Art – Harry Alisavakis
source_site: https://halisavakis.com
category: graphics
fetched: '2026-04-13'
---

# Patrons

This tutorial is brought to you by these awesome Patrons:

- Diarmaid Malone
- Sergey Gonchar
- Tiph’ (DN)

# Introduction

Hey there 👀 It’s been a while since the last “My take on shaders” tutorial. I’m not gonna lie; I’ve been having some trouble considering this series relevant or useful lately, since node-based shader authoring has been getting more and more popular and there’s so many awesome creators sharing tutorials with them.

I thought, however, of a subject that’s certainly useful and that it can’t really be reproduced with visual shader creation systems (as of yet): Compute shaders.

In this tutorial we’ll take a look at what compute shaders are, how they work, why their weird syntax is the way it is, and how to use them in a very simple use case. Hopefully, this tutorial will demystify some of the more obscure elements of compute shaders and it will get you started with making your own applications with them.

Let’s get started!

# Compute shaders

## What are they?

Compute shaders (CS) are shader programs that run on the GPU, much like the shaders we already know. The main difference, however, is that they run outside the main rendering pipeline, meaning that they don’t have to be used just for object materials or post-processing effects. They have the advantage of running on the GPU in a parallel fashion and be very fast and, therefore, are extremely handy for accelerating rendering techniques or for running GPUGPU (General Purpose GPU) algorithms. That means that they can be used to do all the expensive grunt work on the GPU and work with the CPU to present the results or used in any way you can think of.

## What language do they use?

In Unity, compute shaders are written in HLSL, but have some special types and directives that define how they work.

## Anatomy of a compute shader

Here’s what a compute shader looks like when you create it in Unity:

```
// Each #kernel tells which function to compile; you can have many kernels
#pragma kernel CSMain
// Create a RenderTexture with enableRandomWrite flag and set it
// with cs.SetTexture
RWTexture2D<float4> Result;
[numthreads(8,8,1)]
void CSMain (uint3 id : SV_DispatchThreadID)
{
// TODO: insert actual code here!
Result[id.xy] = float4(id.x & id.y, (id.x & 15)/15.0, (id.y & 15)/15.0, 0.0);
}
```

A compute shader file can have **kernels** inside it, which is what we call the compute shader’s main function. When we dispatch a compute shader through C# we specify the **ID** of the **kernel **we want to execute. This is similar to post-processing shaders, were one shader file might have multiple passes and we specify what pass to execute during a **blit** method by passing the ID of it to the method.

We specify that a method is gonna be the main method of a kernel using the `#pragma kernel`

tag and matching the name of the kernel to that of the method:

![](../../assets/ff39db5592474aa5.png)

It’s a similar practice to other shaders where we used `#pragma vertex vert`

to let Unity know that the vertex shader we’ll be using is executed through the `vert`

method.

Outside the methods we can declare properties, much like every other shader. These properties are usually set through C# before the compute shader is dispatched.

Each CS kernel method needs to specify how many threads to use per group on 3 dimensions, x, y and z, since compute shaders can be used to write 1D, 2D or 3D data. That means that they can be used to write data to 1D arrays (which is probably the most common use case), 2D or 3D textures. The template Unity provides us with when we make a new CS, for example, is generating a fractal pattern.

We don’t have to worry about how the fractal pattern is generated, but it’d worth noting something: the use of the **id** parameter.

The **id** parameter refers to the current iteration of the CS. If the texture this CS is writing to is a 256×256 texture, the **id**‘s x and y components are integers ranging from 0 to 255 and correspond to the current execution index of the CS. If this process was instead in a double nested for-loop, `id.x`

would be the iterator of the outer loop and **id.y** would be the iterator of the inner loop.

Hopefully more things about compute shaders will be clearer with the simple example later on, but another noteworthy element of the template is the property type `RWTexture2D<float4>`

. The important thing to note here is that the property type is written like that because we’re modifying the texture and writing to it. If we only used the texture for reading, we could just declare it as `Texture2D<float4>`

.

## Other resources

Here’s some other sources where you can learn more about compute shaders that also helped me get started:

- Ronja’s tutorial:
[https://www.ronja-tutorials.com/post/050-compute-shader/](https://www.ronja-tutorials.com/post/050-compute-shader/) - Kyle’s tutorial:
[http://kylehalladay.com/blog/tutorial/2014/06/27/Compute-Shaders-Are-Nifty.html](http://kylehalladay.com/blog/tutorial/2014/06/27/Compute-Shaders-Are-Nifty.html) - Catlike coding:
[https://catlikecoding.com/unity/tutorials/basics/compute-shaders/](https://catlikecoding.com/unity/tutorials/basics/compute-shaders/)

# A simple CS use case

One reason compute shaders can be daunting is because of the set up required for them to run. Because they’re independent from the rendering pipeline and their purpose is so generic, there’s no ready-made system to just plug in a compute shader and see it working, like with object material shaders.

I struggled a lot with thinking of the most bare example that could demonstrate the potential of compute shaders and I ended up with something similar to what I made a while back, with the first ever compute shader that I wrote on my own. This was my reaction to it btw:

Basically, I needed a little system to paint mesh vertices on runtime based on a spherical mask. You don’t really need compute shaders to do that, but the speed-up you get from using them instead of doing it all in CPU is remarkable.

This is how the end result of this example should look like:

# The code

To get this up and running we’ll need to write 3 files:

- The compute shader
- The C# that manages the whole effect and dispatches the compute shader
- The object shader for the sphere that outputs the modified color

While this tutorial is about compute shaders, the larger focus will be on the C# side (which has the larger file too). So let’s start with that.

## The C# side

Here’s the C# file for this little system:

```
using System.Collections;
using System.Collections.Generic;
using Unity.Collections;
using UnityEngine;
[RequireComponent(typeof(MeshRenderer), typeof(MeshFilter))]
public class ComputeShaderTutorial : MonoBehaviour {
//Public fields
public ComputeShader computeShader;
public Transform paintSphere;
public float radius;
//Mesh related properties
private Mesh mesh;
private Material material;
private int vertexCount;
//Compute shader related properties
private int kernelID;
private int threadGroups;
private ComputeBuffer vertexBuffer;
private ComputeBuffer colorBuffer;
private void OnEnable() {
mesh = GetComponent<MeshFilter>().sharedMesh;
material = GetComponent<MeshRenderer>().sharedMaterial;
vertexCount = mesh.vertexCount;
SetupBuffers();
SetupData();
}
private void OnDisable() {
DiscardBuffers();
}
private void SetupBuffers() {
vertexBuffer = new ComputeBuffer(vertexCount, sizeof(float) * 3, ComputeBufferType.Default, ComputeBufferMode.Immutable);
colorBuffer = new ComputeBuffer(vertexCount, sizeof(float) * 4);
}
private void DiscardBuffers() {
if (vertexBuffer != null) {
vertexBuffer.Dispose();
vertexBuffer = null;
}
if (colorBuffer != null) {
colorBuffer.Dispose();
colorBuffer = null;
}
}
private void SetupData() {
kernelID = computeShader.FindKernel("CSMain");
computeShader.GetKernelThreadGroupSizes(kernelID, out uint threadGroupSizeX, out _, out _);
threadGroups = Mathf.CeilToInt((float)vertexCount / threadGroupSizeX);
using (var meshDataArray = Mesh.AcquireReadOnlyMeshData(mesh)) {
var meshData = meshDataArray[0];
using (var vertexArray = new NativeArray<Vector3>(vertexCount, Allocator.TempJob, NativeArrayOptions.UninitializedMemory)) {
meshData.GetVertices(vertexArray);
vertexBuffer.SetData(vertexArray);
}
}
//Static data
computeShader.SetBuffer(kernelID, "_VertexBuffer", vertexBuffer);
computeShader.SetBuffer(kernelID, "_ColorBuffer", colorBuffer);
computeShader.SetInt("_VertexCount", vertexCount);
material.SetBuffer("_ColorBuffer", colorBuffer);
}
private void Update() {
//Dynamic data
computeShader.SetMatrix("_LocalToWorld", transform.localToWorldMatrix);
computeShader.SetVector("_Sphere", new Vector4(paintSphere.position.x, paintSphere.position.y, paintSphere.position.z, radius));
computeShader.Dispatch(kernelID, threadGroups, 1, 1);
}
private void OnDrawGizmos() {
if (paintSphere != null) {
Gizmos.DrawWireSphere(paintSphere.position, radius);
}
}
}
```

Lots of scary stuff going on here, but we’ll break it all down, don’t worry.

This approach features a pattern that I like to use with compute shader systems. Specifically:

- I like to have one method to initialize the buffers and one to discard them, which get called in
`OnEnable`

and in`OnDisable`

respectively. I usually call these methods`SetupBuffers`

and`DiscardBuffers`

respectively. - I also like to have one method to set up any static data for the compute shader that need to be passed only once, which I usually call
`SetupData`

. This usually gets called in`OnEnabled`

as well, after the buffers get set up. - I like to pass the dynamic data to the compute shader in
`Update`

or whenever I also dispatch the compute shader.

In the script I do things way too explicitly, sacrificing the brevity of the script, but hopefully that will help make things clearer.

Let’s check out the specifics:

Lines 9-22 is declaring our properties, nothing weird here.

In `OnEnable`

I get all the necessary components and call the methods to set up my buffers and my static data. In `OnDisable`

I just discard my buffers.

Let’s dive into the methods:

### SetupBuffers

`SetupBuffer`

is responsible for creating our compute buffers that contain the information we send to and receive from the compute shader. These buffers get created with a specific way so it’s worth breaking things down:

- The first parameter of the constructor is the maximum amount of data in each buffer; think of it as the size of a fixed array.
- The second parameter contains the
**stride**, which basically signifies how many bytes each element takes up in the buffer. In`vertexBuffer`

I store vertex positions, which correspond to a 3D vector, so the stride will be equal to 3 times the size of a`float`

. Similarly, the color is stored in a 4D vector, so the stride will be equal to 3 times the size of a`float`

. - There are some extra parameters that define some characteristics of our compute buffer. The default type is
`ComputeBufferType.Default`

and the default mode is`ComputeBufferMode.Immutable`

in both cases, I just set it explicitly on one of the buffers for clarity.**NOTE:**The`Immutable`

mode doesn’t mean that the buffer will be read-only from our compute shader. Instead, it means that the buffer won’t be modified by the CPU apart from some initial data assignment.

### DiscardBuffers

Discarding buffers is crucial to avoid any memory leaks. In the `DiscardBuffers`

method I just check if a buffer is null and, if it’s not, I dispose the contents and set it to null.

### SetupData

This is where I set some compute-shader related data along with the static data that our compute shader needs.

First, in line 55, I get the kernel ID that we want to use. As mentioned above, a compute shader can have multiple **kernels **in it, each with its own ID, starting from 0, similar to conventional shader passes. If we have just the one kernel, we know that the ID is gonna be 0, but for clarity reasons I’m using the `FindKernel`

method to get the ID of the kernel I want using its name, as declared in the compute shader.

In line 56 I use the `GetKernelThreadGroupSizes`

method to get the thread group size of our kernel. Again, this could be hardcoded to whatever we set in the `numthreads`

field, but it’s better to have it dynamic, in case we change the number in the CS.

The number of thread groups we’ll end up using are gonna be equal to however many iterations we want the compute shader to run for, divided by the thread group size. We then take the ceiling of the result and cast that to an int. So, in this case, if we have 48 vertices and a kernel with a thread group size of 32 on the X, we’d need 2 groups to run.

Lines 59-65 are about getting our mesh data. I’m using the `AcquireReadOnlyMeshData`

method to get the vertex position data using a native array; it’s generally faster and allocates less memory that way.

I get the vertex positions and store them in the temporary `vertexArray`

array, and then I use that array to set the data of the compute buffer containing the vertex positions.

**IMPORTANT:** **You’ll have to make sure your mesh has read/write enabled. Things might work inside the editor, but getting the mesh data probably won’t work in builds otherwise.**

I don’t need to set up any data in the color buffer, as only the compute shader will write stuff there.

I then pass the buffers to the compute shader, along with the number of the mesh vertices. I usually forget about actually setting the buffers after I set the data, which is bad. Don’t forget to pass your buffers, please.

Finally, I also pass the color buffer over to the material so the shader can read the colors. I could also use a material property block instead, so that I don’t mess with every object using the same material.

### Update

This is where I set the dynamic data and actually dispatch my compute shader. Since both my object and the sphere mask might move on runtime, there’s no point for me to only set these data in `SetupData`

.

The vertex positions in the compute buffer are straight from the mesh, so they’re in **object space**. That’s why I also need the `_LocalToWorld`

matrix, to transform these positions in world space. That matrix can change on runtime as the transform moves, rotates, or scales up/down.

Similarly, I also pass my sphere mask parameters to the compute shader. We can pack those into a 4-dimensional vector, containing the world-space position of the sphere and its radius.

Finally, I dispatch the compute shader, using the kernel ID I got before, and the amount of thread groups that I calculated in `SetupData`

.

I also draw some gizmos for the paint sphere to be more visible, but that doesn’t really have anything to do with the compute shader.

**SUPER IMPORTANT: **Do not perceive compute shaders so much as normal shaders or classes. Instead, think of them as objects/materials. That being said, when you set buffers and data to a compute shader in a script (let’s call it script A), if another script (script B) dispatches the same compute shader, **it’ll get the same results as if it was script A**. The data get stored in the compute shader itself. That’s why it’s common practice to **instantiate** instances of the compute shader in a script, so that there’s no data conflicts. I’m not doing that in this example to keep things simple, but you have been warned.

### Wait, where am I applying the newly-painted colors?

So, one could apply these colors on the object’s vertex colors, by using the `ComputeBuffer.GetData`

method, for which you can learn more in [Unity’s documentation](https://docs.unity3d.com/ScriptReference/ComputeBuffer.GetData.html). This, however will introduce an unwanted bottleneck to our process. See, compute shaders are *fast*, but when they have to move data back and from the CPU and the GPU, things slow down. So it’s good practice to keep things on one side, especially if that side is the GPU. That’s why **line 72** is important in that regard. We’ll come back to that as I get into the object shader.

## The compute shader

This is the code of the compute shader; the 20 most terrifying lines in this whole blog post:

```
#pragma kernel CSMain
StructuredBuffer<float3> _VertexBuffer;
RWStructuredBuffer<float4> _ColorBuffer;
float4x4 _LocalToWorld;
float4 _Sphere;
uint _VertexCount;
[numthreads(32,1,1)]
void CSMain (uint id : SV_DispatchThreadID)
{
if (id >= _VertexCount) {
return;
}
float3 pos = mul(_LocalToWorld, float4(_VertexBuffer[id], 1.0)).xyz;
float mask = 1.0 - saturate(distance(pos, _Sphere.xyz) / _Sphere.w);
_ColorBuffer[id] += float4(mask, 0, 0, 1);
}
```

Amazing right? Let’s dig into it.

First off we have the kernel name declaration mentioned above; I kept the name `CSMain`

but I could also change it to something more fitting, like `MeshColoring`

or something.

Lines 3-7 contain the declaration of the CS variables:

- First, there’s the structured buffer for the vertex positions.
- Then, we have the structured buffer for the colors that we’re outputting. Notice this is an
`RWStrcturedBuffer`

, as we want to write to this buffer, not just read from it. - We also have the local to world matrix.
- After that, there’s the
`_Sphere`

vector holding the information of the sphere mask (position and radius). - Finally, the vertex count of our mesh.

I’m running the compute shader in 1 dimension, so I only use the x dimension of the threads. I’ve set the group size to be to 32, but that’s a bit arbitrary, you can try going higher to see what works better in terms of performance. Powers of two are preferable, as you can probably imagine.

In lines 12-14 I do a small check to make sure I don’t get out of bounds on my buffer: I compare the current iteration id with the amount of vertices and if it’s larger or equal I just return. Like I mentioned before, if I had 48 vertices, I’d end up with 2 thread groups of size 32 each. That means that the id can range from 0 to 63, but if I try and access, say, the 54th vertex on my buffer I’d get some undefined results.

In line 16 I use the `_LocalToWorld`

matrix to convert my vertex position from object space to world space.

**NOTE:** When applying 4×4 matrix transformations to **positions**, you want to convert your positions to a 4-dimensional vector with the w component set to **1**. If that were a **direction** (say, a normal vector), the w component should be set to **0**.

In line 17 I calculate the distance of my world-space vertex position to that of the sphere mask and inverting it (as it would be 0 closer to the center of the sphere, and I want the opposite). This is a standard sphere masking approach, but you can make it harder or softer, that’s up to you.

Finally, in line 19, I add a red color, based on my sphere mask, to the current color of the `_ColorBuffer`

.

**IMPORTANT: **You’ll notice that there’s a 1-1 relation between the vertex buffer and the color buffer. If the two buffers had no relation between them things would be messy, as we only have the one `id`

from the compute shader.

## The object shader

I tried to keep the shader as minimalistic as possible to just focus on the interesting bits. Let’s see the code:

```
Shader "Unlit/PaintedObject"
{
SubShader
{
Tags { "RenderType"="Opaque" }
LOD 100
Pass
{
CGPROGRAM
#pragma vertex vert
#pragma fragment frag
#include "UnityCG.cginc"
struct appdata
{
float4 vertex : POSITION;
uint id : SV_VertexID;
};
struct v2f
{
float4 vertex : SV_POSITION;
float4 color : COLOR;
};
StructuredBuffer<float4> _ColorBuffer;
v2f vert (appdata v)
{
v2f o;
o.vertex = UnityObjectToClipPos(v.vertex);
o.color = _ColorBuffer[v.id];
return o;
}
fixed4 frag (v2f i) : SV_Target
{
return i.color;
}
ENDCG
}
}
}
```

I assume you already know have some basic shader knowledge so I won’t go through the boring stuff. There’s specific lines of which we need to take note:

- In line 19 I add another field to the
`appdata`

struct:`SV_VertexID`

. This gives us an integer index of the current vertex in the object’s vertex buffer. It’s literally the array index of the vertices based on how the model was created. Remember how we got the vertex array from the mesh data in our C# script, in line 62? The order of the vertices in that array match the one passed to our shader, and it’s the same as with the compute buffer we passed to the compute shader. - In line 25 I add another field to the
`v2f`

struct for the colors I pass from the vertex to the fragment shader. The syntax is the same as if we passed on vertex colors. - In line 28 I declare the structured buffer containing the color information that got generated from the compute shader. This is passed through that important
**line 72**of the C# script I mentioned before. - Then, in line 34 I access
`_ColorBuffer`

and get the color of the current vertex from it, using the vertex id I added in the`appdata`

struct. That gives me the modified color of the specific vertex. - Finally, in the fragment shader, in line 40, I just return the interpolated color value.

## The result

You can assign the C# script to the object you want to paint and make sure you have a transform assigned for the paint sphere as well as the compute shader in the appropriate field. The setup should look like this:

![](../../assets/04b60e01b3645203.png)

If everything went well, hitting play should give you this result:

## Unity package

You can download a package with this test scene to see everything working.

# Conclusion

Compute shaders are wonderful tools that can make things work much cleaner and *way* faster. This tutorial only scratches the surface of what one can do with them, but I hope that it makes getting started with them a tiny bit easier and less intimidating.

Not sure when that will be, but oh well. See you in the next one!