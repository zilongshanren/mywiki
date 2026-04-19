---
title: GPU Instanced Grass Breakdown
url: https://www.cyanilux.com/tutorials/gpu-instanced-grass-breakdown/
author: Cyanilux
published: '2025-10-03'
source_blog: Cyanilux Shader Tutorials
source_site: https://www.cyanilux.com/
category: graphics
fetched: '2026-04-19'
---

# GPU Instanced Grass Breakdown

## Intro

Way back in 2021, I experimented with grass rendering in URP & Shader Graph using GPU Instancing, which can allow us to efficiently render millions of grass blades/quads. At the time that was using `Graphics.DrawMeshInstancedProcedural`

(or `DrawMeshInstancedIndirect`

if instance count needs to be set/adjusted on the GPU)

For a while I’ve had some info/files linked under my [FAQ](https://www.cyanilux.com/faq/#sg-drawmeshinstancedindirect) showing a brief example of that setup. But I thought I’d revisit/rewrite those experiments and write up a proper breakdown, which should be easier to find and lets me update some things :

**Unity 2021.2**introduced`Graphics.RenderX`

functions to replace the older`Graphics.DrawX`

functions (and renames “Procedural” to “Primitives”)**Unity 2022**onwards considers the older functions to be obsolete. For the functions mentioned above, the equivalents would be`Graphics.RenderMeshPrimitives`

and`Graphics.RenderMeshIndirect`

respectively.**Unity 6**onwards changed the functionality of the**Instance ID**node, meaning we can support these GPU instancing functions in a less hacky way.

Note that grass rendering is a fairly complex topic and this post only goes through one(ish) setup. There may be grass tools which extend this concept to painting/placing instances by hand, but in my case the grass is spawned automatically. There may also be other rendering techniques (e.g. shell texturing) that could be more suitable depending on the desired artstyle. For more grass tutorials or ready-made tools from others, may be some links on my [resources](https://www.cyanilux.com/resources/?filter=grass) page.

## What is GPU Instancing?

### Instancing

The main advantage of GPU Instancing is that you can render many objects in a single draw call. And by calling these functions under the [Graphics API](https://docs.unity3d.com/ScriptReference/Graphics.html), we can avoid the overhead of many **GameObjects**.

The mesh and material/shader needs to stay the same, but we can have different per-instance properties (e.g. positions/matrices, different colours, etc) by passing that data as arrays or buffers, which then are indexed in the shader using a variable/input with the `SV_InstanceID`

semantic.

Generally when creating scenes, we tend to render lots of *different models* with the same shader, so in URP/HDRP it is likely more performant to rely on the [SRP Batcher](https://docs.unity3d.com/Manual/SRPBatcher.html) for optimising the majority of the scene’s draw calls. However in some cases GPU Instancing could be better, and I think rendering grass blades/quads is a good example - though I haven’t tested that extensively tbh. ([BatchRendererGroup](https://docs.unity3d.com/ScriptReference/Rendering.BatchRendererGroup.html) might also be more performant, but the setup looks far more complicated)

Also note that with these GPU Instancing functions you only get frustum culling as a whole based on the bounds passed in. You would typically need to handle your own culling per-instance via Compute Shader (a later section provides an example of this) or perhaps in C# but probably split into chunks/cells/quad-tree (maybe also multithreaded via Jobs?)

### Instancing in ShaderGraph

Shader Graph used to have very limited support for instancing. Unity 2021.2 exposed an **Instance ID** node, but back then it returned `unity_InstanceID`

which would always be 0 unless the shader takes one of the “instancing paths” :

- For “regular” instancing (
`DrawMeshInstanced`

/`RenderMeshInstanced`

), that mostly required the GPU Instancing tickbox to be enabled on the material (though per-instance properties[needed more setup](https://www.cyanilux.com/faq/#sg-gpu-instancing)). But that is limited to 1023 instances (due to using arrays) and uploads matrices every frame, so that function is somewhat inefficient compared to the others. - For the functions listed in the intro above, they will try to use the “procedural instancing path” if the shader supports it. By default Shader Graph doesn’t include support, but we can add it using a couple
**Custom Function**nodes (as shown in breakdown below in tabs prior to Unity 6)

As of Unity 6, the functionality of the **Instance ID** node changed slightly, to instead hook directly into declaring `SV_InstanceID`

. Therefore, while custom code is still required for declaring and indexing the buffer, the workaround to force the procedural instancing path is no longer required. (But now means “Object” space in the graph is relative to the bounds, not per-instance)

You may also need *additional code* to support some instancing functions properly. [This discussions thread](https://discussions.unity.com/t/indirect-procedural-rendering-with-shader-graph/1664601) shows how Shader Graphs can support the newer instancing functions. (Though I will mention that `Graphics.RenderMeshIndirect`

does still seem to work without the `UnityIndirect.cginc`

and `InitIndirectDrawArgs / GetCommandID`

setup - provided you don’t use more than one command and leave `startInstance`

at 0. More details are provided in a later section when relevant)

The breakdown below is structured like so :

[Basic Instancing Setup](https://www.cyanilux.com#setup)- C# Script
- Shader Graph

[Optional Additions](https://www.cyanilux.com#optional)- Make grass visible in editor
- Adapt instance spawning for Terrain
- Split instances into cells/chunks
- Remove/Hide instances on non-grass TerrainLayer
- Simulate wind / swaying

[Adapting Setup for Indirect](https://www.cyanilux.com#indirect)- C# Side
- Shader Graph

[Adding GPU Frustum Culling](https://www.cyanilux.com#frustum-culling)- Compute Shader
- C# Changes
- Shader Graph Include File Changes


Each section here builds on the previous. The idea behind this order being, you could stop after each main section and still have grass rendering. (There’s also tabs, which makes sure the page content is correct for that Unity version)

## Basic Instancing Setup

### C# Script

We first need some setup on the CPU side to tell Unity to draw our grass. Create a C# script and attach it to a new GameObject in the scene.

We’ll begin the script by exposing some fields to the inspector :

```
using UnityEngine;
public class DrawGrass : MonoBehaviour {
public int instanceCount = 1000;
public Mesh mesh;
public Material material;
// ...
}
```


For this example I’m using the default quad for the grass `mesh`

, which’ll be scattered randomly by the script. Later we’ll set up the shader (used by the assigned `material`

) which will sample a grass texture with alpha clipping.

(You could alternatively use a grass blade mesh. Though if you’re drawing millions of instances you probably don’t want that too high-poly)

If the instance count is known/set from the CPU / C# Script we can use the simpler `Graphics.DrawMeshInstancedProcedural`

to draw our grass. If you need to be able to set the instance count from the GPU (i.e. in Compute Shaders for generating the instances on the GPU and/or frustum culling) you would instead use `Graphics.DrawMeshInstancedIndirect`

. Both functions follow the same inital setup - later sections will show the Indirect setup further if needed.

```
private UnityEngine.Rendering.ShadowCastingMode castShadows = UnityEngine.Rendering.ShadowCastingMode.Off;
private bool receiveShadows = true;
// Could also make these shadow settings public / [SerializeField] if you want to expose them to inspector
private MaterialPropertyBlock MPB;
private Bounds bounds;
void OnEnable() {
MPB = new MaterialPropertyBlock();
Vector3 boundsSize = new Vector3(20, 1, 20);
bounds = new Bounds(transform.position + boundsSize * 0.5f, boundsSize);
}
void Update() {
if (instanceCount <= 0) return;
Graphics.DrawMeshInstancedProcedural(mesh, 0, material, bounds, instanceCount, MPB, castShadows, receiveShadows);
}
```


In this version, `Graphics.RenderX`

functions were introduced. According to the docs, the older `Graphics.DrawX`

ones technically aren’t marked as obsolete until Unity 2022, but since the new functions exist it probably makes sense to use them…

In this version, the older `Graphics.DrawX`

functions are obsolete and should be replaced with `Graphics.RenderX`

.

If the instance count is known/set from the CPU / C# Script we can use the simpler `Graphics.RenderMeshPrimitives`

to draw our grass. If you need to be able to set the instance count from the GPU (i.e. in Compute Shaders for generating the instances on the GPU and/or frustum culling) you would instead use `Graphics.RenderMeshIndirect`

. Both functions follow the same inital setup - later sections will show the Indirect setup further if needed.

Unity also introduces the [RenderParams](https://docs.unity3d.com/ScriptReference/RenderParams.html) struct which is passed as the first parameter to the above functions. This structure collects together a bunch of data related to rendering that would have been passed as separate parameters in the older `DrawX`

functions.

In this breakdown we’ll only be setting the `material`

, `matProps`

, `shadowCastingMode`

and `worldBounds`

. See docs page linked above for the other properties.

```
private UnityEngine.Rendering.ShadowCastingMode castShadows = UnityEngine.Rendering.ShadowCastingMode.Off;
private bool receiveShadows = true;
// Could also make these shadow settings public / [SerializeField] if you want to expose them to inspector
private RenderParams rParams;
private MaterialPropertyBlock MPB => rParams.matProps;
private Bounds bounds => rParams.worldBounds;
/*
(These properties are used in SetupInstances() function defined later.
Just allows me to use that snippet in multiple Unity versions...
You can just reference rParams in the function instead if you prefer)
*/
void OnEnable() {
Vector3 boundsSize = new Vector3(20, 1, 20);
rParams = new RenderParams(material) {
worldBounds = new Bounds(transform.position + boundsSize * 0.5f, boundsSize),
shadowCastingMode = castShadows,
receiveShadows = receiveShadows,
matProps = new MaterialPropertyBlock()
};
bounds = rParams.worldBounds;
MPB = rParams.matProps;
}
void Update() {
if (instanceCount <= 0) return;
Graphics.RenderMeshPrimitives(rParams, mesh, 0, instanceCount);
}
```


#### Instance Data

That triggers the rendering, but to actually control the position of the instances (and optionally colour, etc), we also need to set/pass a **ComputeBuffer** with that data, which I’ve named `instancesBuffer`

. In this case I’m spawning instances randomly in some `bounds`

.

If you only need Matrix4x4 you could just use that type, or pass multiple buffers with different data types. But to be more flexible I’m using a struct type which allows us to pack multiple types together. We need to be a bit careful to match the memory layout on the shader side though or it can cause crashes. To avoid issues with how different graphics APIs structure the data, always order fields from largest to smallest and use Vector4/float4 instead of Vector3/float3.

```
#region Instances
[LayoutKind.Sequential]
private struct InstanceData {
public Matrix4x4 matrix;
//public Color color;
public static int Size() {
return
sizeof(float) * 4 * 4 // matrix
//+ sizeof(float) * 4 // color
;
// Alternatively one of these might work to calculate the size automatically?
// return System.Runtime.InteropServices.Marshal.SizeOf(typeof(InstanceData));
// return Unity.Collections.LowLevel.Unsafe.UnsafeUtility.SizeOf<InstanceData>();
}
/*
Must match the layout/size of the struct in shader
See https://docs.unity3d.com/ScriptReference/ComputeBufferType.Structured.html
To avoid issues with how different graphics APIs structure data :
- Order by largest to smallest
- Use Vector4/Color/float4 & Matrix4x4/float4x4 instead of float3 & float3x3
*/
}
private ComputeBuffer instancesBuffer;
private void SetupInstances(){
if (instanceCount <= 0) {
// Avoid negative or 0 instances, as that will crash Unity
instanceCount = 1;
}
InstanceData[] instances = new InstanceData[instanceCount];
Vector3 boundsSize = bounds.size;
for (int i = 0; i < instanceCount; i++) {
// Random Position
Vector3 position = new(
Random.Range(0, boundsSize.x),
0,
Random.Range(0, boundsSize.z)
);
// Random Rotation around Y axis
Quaternion rotation = Quaternion.Euler(0, Random.Range(0f, 360f), 0);
// Random Height
Vector3 scale = new Vector3(1, Random.Range(0.4f, 0.9f), 1);
// Position Offsets
position.y += scale.y * 0.5f; // (assuming origin of mesh is in center, like Quad primitive)
position -= boundsSize * 0.5f; // Makes position relative to bounds center
// Or if you'd prefer to store the matrix positions in world space, instead use :
//position += transform.position;
/* Though this also requires some changes on the shader side.
e.g. an additional Transform node converting from World to Object space
*/
instances[i] = new(
matrix = Matrix4x4.TRS(position, rotation, scale)
);
}
instancesBuffer = new ComputeBuffer(instanceCount, InstanceData.Size());
instancesBuffer.SetData(instances);
MPB.SetBuffer("_PerInstanceData", instancesBuffer);
}
#endregion
void OnEnable() {
// ... (function body from previous snippet)
SetupInstances();
}
void OnDisable() {
if (instancesBuffer != null) {
instancesBuffer.Release();
instancesBuffer = null;
}
}
```


### Shader Graph

For the graph, I’m using a **Lit Graph** since I want the grass to be affected by lighting.

If you are unfamiliar with the **Custom Function** node, see the [docs page](https://docs.unity3d.com/Packages/com.unity.shadergraph@17.4/manual/Custom-Function-Node.html). Below shows HLSL snippets but may assume you know how to set that up in Shader Graph. i.e. for File mode :

- Inputs/Outputs should match the types and order defined in the function parameters.
- Name field should match the function name without
`_float`

. - (May also want to set node precision to Single/Float. Or add
`_half`

function versions if you need support for that)

#### Vertex Stage

To support instancing we need to use the `SV_InstanceID`

shader input [semantic](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-semantics). But for versions prior to Unity 6, there isn’t an easy way to do that as it needs to be included in the struct passed to the vertex shader (usually named “Attributes”), or passed as an additional parameter to the vertex function. Both of which are part of the generated code and not accessible in the graph or even through a **Custom Function**.

But Shader Graph can declare it for us if an “instancing path” is taken. I discovered we could force that by using a **Custom Function** with a Vector3 input (named `In`

- caps important) and output (named `Out`

) :

```
Out = In;
#pragma multi_compile _ PROCEDURAL_INSTANCING_ON
#pragma instancing_options procedural:InstancingSetup
```


That must use **String** mode as unlike other pragmas, `instancing_options`

must be defined in the main shader and won’t work inside include files. I’ve named this node/function “Procedural” as this code tells the shader to compile the “procedural instancing” variants of the shader.

(In the past I’ve defined the `multi_compile`

in the **Blackboard** as a **Boolean Keyword** instead - but afaik declaring it directly in the code here also works)

We then need another **Custom Function** to attach a HLSL file containing that `InstancingSetup`

function, which can also declare & index the compute buffer (aka `StructuredBuffer`

on this side) used to pass per-instance data in. It must use **File** mode to allow us to define all that outside the function body. I’ve named this node “Instancing” (matching `Instancing_float`

as defined below)

```
// Instancing.hlsl
#ifndef GRASS_INSTANCED_INCLUDED
#define GRASS_INSTANCED_INCLUDED
// Declare structure & buffer for passing per-instance data
// This must match the C# side
struct InstanceData {
float4x4 m;
//float4 color;
StructuredBuffer<InstanceData> _PerInstanceData;
#if UNITY_ANY_INSTANCING_ENABLED
// Based on ParticlesInstancing
// https://github.com/Unity-Technologies/Graphics/blob/master/Packages/com.unity.shadergraph/Editor/Generation/Targets/BuiltIn/ShaderLibrary/ParticlesInstancing.hlsl
// and/or
// https://github.com/TwoTailsGames/Unity-Built-in-Shaders/blob/master/CGIncludes/UnityStandardParticleInstancing.cginc
void InstancingMatrices(inout float4x4 objectToWorld, out float4x4 worldToObject) {
InstanceData data = _PerInstanceData[unity_InstanceID];
// If matrix is relative to Bounds :
= mul(objectToWorld, data.m);
// Alternatively, if instanced matrices are stored in world space we can override matrix :
//objectToWorld = data.m;
// This may avoid needing an additional World->Object conversion in the graph
// ----------
// If World->Object transforms are required by shader,
// can use this to calculate the inverse matrix :
w2oRotation[0] = objectToWorld[1].yzx * objectToWorld[2].zxy - objectToWorld[1].zxy * objectToWorld[2].yzx;
w2oRotation[1] = objectToWorld[0].zxy * objectToWorld[2].yzx - objectToWorld[0].yzx * objectToWorld[2].zxy;
w2oRotation[2] = objectToWorld[0].yzx * objectToWorld[1].zxy - objectToWorld[0].zxy * objectToWorld[1].yzx;
float det = dot(objectToWorld[0].xyz, w2oRotation[0]);
w2oRotation = transpose(w2oRotation);
w2oRotation *= rcp(det);
float3 w2oPosition = mul(w2oRotation, -objectToWorld._14_24_34);
worldToObject._11_21_31_41 = float4(w2oRotation._11_21_31, 0.0f);
worldToObject._12_22_32_42 = float4(w2oRotation._12_22_32, 0.0f);
worldToObject._13_23_33_43 = float4(w2oRotation._13_23_33, 0.0f);
worldToObject._14_24_34_44 = float4(w2oPosition, 1.0f);
/*
This may be somewhat expensive and this function runs in both vertex and fragment shader
(Though if the matrix is unused the compiler might optimise this away? Unsure)
Could instead calculate inverse matrices on the CPU side and pass them in too
(But would mean additional GPU memory is needed in struct/buffer)
*/
}
void InstancingSetup() {
/* // For HDRP may also need to remove/override these macros. Untested.
#undef unity_ObjectToWorld
#undef unity_WorldToObject
*/
InstancingMatrices(unity_ObjectToWorld, unity_WorldToObject);
}
#endif
// Shader Graph Functions
// Just passes the position through, allows us to actually attach this file to the graph.
// Should be placed somewhere in the vertex stage, e.g. right before connecting the object space position.
void Instancing_float(float3 Position, out float3 Out){
Out = Position;
}
#endif
```


In both custom functions, `Out = In;`

/`Out = Position;`

is just so we can hook the node up to the **Master Stack** - which is required for the code to be included in the final generated shader. We should make all these ports **Vector3** so we can pass the **Position** node (Object space) through, and connect to the **Position** port in the **Vertex** stage.

While the functions don’t alter the value passed through, the procedural instancing setup overrides the matrices used by the graph behind the scenes when converting between Object & World space - automatically applying to the Position, Normal (and Tangent) Vector ports/blocks/nodes.

Due to this and the C# side which sets the matrix rotation to match the terrain normal, we can make the grass normal match the terrain’s normal (to make it shaded/lit the same) by simply attaching a **Vector3** node set to **(0, 1, 0)** to the **Normal** port as shown above.

For versions prior to 2021.2, we may also want a function to return the Instance ID if needed in the graph. e.g. could be used as the **Seed** to a **Random Range** node to generate a random value for each instance. This can be placed in the same file and used by multiple **Custom Function** nodes - thanks to the `#ifndef GRASS_INSTANCED_INCLUDED`

at the top which prevents the file being included multiple times.

```
void GetInstanceID_float(out float Out){
Out = 0;
#ifndef SHADERGRAPH_PREVIEW
#if UNITY_ANY_INSTANCING_ENABLED
= unity_InstanceID;
#endif
#endif
```


For 2021.2+, this is already exposed through the **Instance ID** node.

As mentioned in the intro, Unity 6 changed the functionality of the **Instance ID** node so that it hooks directly into defining the `SV_InstanceID`

semantic. We can pass this into a **Custom Function** to define and index our per-instance data compute buffer (which defaults to a `StructuredBuffer`

object on the shader side)

Note the **Custom Function** must use **File** mode to allow us to define the buffer outside the function body.

```
// Instancing.hlsl
#ifndef GRASS_INSTANCED_INCLUDED
#define GRASS_INSTANCED_INCLUDED
// Declare structure & buffer for passing per-instance data
// This must match the C# side
struct InstanceData {
float4x4 m;
//float4 color;
StructuredBuffer<InstanceData> _PerInstanceData;
// Shader Graph function(s)
void Instancing_float(float3 Position, float InstanceID, out float3 OutPosition, out float3 OutNormal){
InstanceData data = _PerInstanceData[InstanceID];
OutPosition = mul(data.m, float4(Position, 1)).xyz;
OutNormal = mul(data.m, float4(0, 1, 0, 0)).xyz;
/*
Shader Graph assumes Object space for the Vertex stage ports in the Master Stack
so will apply the Object->World transform behind the scenes.
If matrices are in world space rather than relative to bounds, undo that by
using an additional Transform node in graph,
or Subtract Position output from the Object node.
(Should only be important for Position, as model matrix
won't include rotation for instanced rendering afaik)
*/
}
#endif
```


The **Position** node (Object) space is connected to the first port, and **Instance ID** to the second. The outputs are used in the **Position** and **Normal** ports in the **Vertex** stage of the **Master Stack**.

In previous Unity versions we instead had to rely on the “procedural instancing path” to force the Instance ID to be generated. (Can switch the tab above temporarily to see what that looks like). A somewhat important difference is that allowed us to override the matrices used for converting between Object & World space - which automatically would apply to these ports. Since we aren’t using that setup, we need to handle the matrix transformations manually, hence `mul()`

in the code shown above. And as commented above, you may need some additional nodes if matrices store world space positions.

If you have more per-instance data you could add another `out`

param & output to the node. Though, Shader Graph doesn’t usually allow connecting a node to both stages. For values that need to connect to the **Fragment** stage, we’ll create a separate function - see below.

After saving the graph we should now see our instances, though they don’t have a texture yet.



![(Image)](../../assets/f7c64755eb33d3e2.png)

1024 instances rendering in bounds of 20x20 units. A darker grey plane (with x2 scale) is placed below.

#### Fragment Stage

For the fragment side things are much simpler. We can apply a simple colour gradient using the `UV0.y`

and input into the **Base Color** :

If you have per-Instance data for the fragment stage you can add another **Custom Function** node and function to the file to output those. For example for an instanced colour (as commented in the InstanceData) :

```
void InstancingFragment_float(float InstanceID, out float4 Out){
InstanceData data = _PerInstanceData[InstanceID];
Out = data.color;
}
// Or for versions older than 2021.2 :
/*
void InstancingFragment_float(out float4 Out){
InstanceData data = _PerInstanceData[unity_InstanceID];
Out = data.color;
}
*/
```


Which could replace one of the Color properties, or **Multiply** after to tint both.

Under the **Graph Settings** (tab of Graph Inspector window), we can enable **Alpha Clipping** which adds some blocks to the Master Stack. I’ve left the **Alpha Clip Threshold** at **0.5**. To control the **Alpha**, I’m applying a grass texture.

For added variation this texture contains multiple grass blade shapes (and somewhat thick/blocky for a more stylised look - I much prefer this over pointy grass, but up to you) :

To randomly select a portion of the texture I’m using the **Flipbook** node with **Width** and **Height** set to 2 (since the texture contains 2x2 grass tiles), with the **Tile** port set to the **Instance ID** node (or output `unity_InstanceID`

for older versions) into a **Random Range** node (Min of 0 to Max of 4)

As shown above I’ve also used a **Tiling And Offset** node with a Y tiling of 0.9, connected to the UV port on the **Flipbook**. This stretches the texture slightly to avoid previous tiles leaking through at the top of the texture.

Note that using the Instance ID here assumes the instances are consistent. If the buffer is updated you’d likely need to store a random value in the InstanceData instead. (In the past I used the `color.a`

for that, as transparency isn’t used)

Looking better!

## Optional Additions

With all the above you should at least be able to see the grass during play mode.

Below are some optional things we can add/adjust. May not be full examples but starting points at least :

## Make grass visible in editor

By adding the `[ExecuteAlways]`

attribute (or `[ExecuteInEditMode]`

for much older Unity versions) before the class definition we can allow the script to run even when not in play mode.

```
[ExecuteAlways] // Allow grass rendering while not in play mode
public class DrawGrass : MonoBehaviour {
```


Though increasing `instanceCount`

won’t update the grass unless we **disable & re-enable the component**. (Potentially also means we index outside of the buffer size on the GPU which *might* cause crashes on some Graphics APIs? Seems fine for DX11 though. Caching `instanceCount`

could avoid that if required)

We could use `OnValidate()`

to detect any inspector changes. But that function is also triggered with reloads / script compiles, and forcing the buffers to be reinitalised here seems to leak resources (likely as Unity can call the function from other threads). It might be better to use a CustomEditor. e.g. to add a “Refresh” button :

```
// in DrawGrass.cs :
public void Refresh() {
OnDisable();
OnEnable();
}
// in DrawGrassEditor.cs (must be placed in a folder named "Editor") :
using UnityEngine;
using UnityEditor;
[CustomEditor(typeof(DrawGrass))]
public class DrawGrassEditor : Editor {
public override void OnInspectorGUI() {
base.OnInspectorGUI();
bool clicked = GUILayout.Button("Refresh");
if (clicked) {
DrawGrass grass = target as DrawGrass;
grass.Refresh();
}
}
}
```


## Adapt instance spawning for Terrain

If using a **Terrain** component in the scene we could adapt the C# Script to use that to spawn the grass.

With `terrain.SampleHeight`

we can move the grass upwards to match the terrain height and by creating the rotation with `terrainData.GetInterpolatedNormal`

we can optionally make the grass match the slope of the terrain. That normal can also be extracted from the matrix in the shader later, to make the shading match the terrain - so the grass blends in better/softly, as if it’s part of the terrain rather than just placed ontop.

(If you use the “Random Rotation around Y axis” rotation above instead, you may still want to keep the normal calculation and pass that into shader by adding a **Vector4/float4** to the **InstanceData**. Be sure to update the Size method as well)

For example, might be something like :

```
public Terrain terrain;
// expose terrain object to inspector,
// or set private & uncomment line in OnEnable() if script is attached to same GameObject
...
private void SetupInstances() {
TerrainData terrainData = terrain.terrainData;
Vector3 terrainSize = terrainData.size;
InstanceData[] instances = new InstanceData[instanceCount];
for (int i = 0; i < instanceCount; i++) {
Vector3 position = new(
Random.Range(0, terrainSize.x),
0,
Random.Range(0, terrainSize.z)
);
// Align rotation to terrain normal
Vector3 normal = terrainData.GetInterpolatedNormal(position.x / terrainSize.x, position.z / terrainSize.z);
float dot = Mathf.Abs(Vector3.Dot(normal, Vector3.forward));
float dot2 = Mathf.Abs(Vector3.Dot(normal, Vector3.right));
Vector3 perp = Vector3.Cross(normal, (dot2 > dot) ? Vector3.right : Vector3.forward);
Vector3 forward = Quaternion.AngleAxis(Random.Range(0f, 360f), normal) * perp; // Random rotation around normal
Quaternion rotation = Quaternion.LookRotation(forward, normal);
Vector3 scale = new Vector3(1, Random.Range(0.4f, 0.9f), 1); // Random Height
position.y += scale.y * 0.5f; // assuming origin of mesh is in center, like the unity primitive Quad
// If you want positions stored in world space,
/*
position += transform.position;
position.y += terrain.SampleHeight(position);
*/
// else :
position.y += terrain.SampleHeight(transform.position + position);
position -= bounds.size * 0.5f; // make position relative to bounds center
// (SampleHeight still expects world space, hence the "transform.position +")
instances[i] = new() {
matrix = Matrix4x4.TRS(position, rotation, scale)
};
}
if (instancesBuffer == null)
instancesBuffer = new ComputeBuffer(instanceCount, InstanceData.Size());
instancesBuffer.SetData(instances);
MPB.SetBuffer("_PerInstanceData", instancesBuffer);
}
...
void OnEnable() {
...
//terrain = GetComponent<Terrain>();
Vector3 boundsSize = terrain.terrainData.size;
...
}
```


Of note, this example spawns grass across the *entire terrain* which could be costly, both in terms of rendering those instances and their storage in memory/VRAM. For large terrains it’s likely that you’d want to adjust this - Maybe by only spawning grass within some bounds around the player/camera. I haven’t attempted that yet but for that to be optimised it may be a good idea to first split the grass into cells/chunks, as the next foldout explains.

The foldout after the next also shows how to better control where grass appears by accessing TerrainLayer data.

## Split instances into cells/chunks

We may want to adjust the instances data to be arranged in cells/chunks rather than be completely random. If only spawning grass around the player, or doing frustum culling on the CPU side, this could reduce how often those calculations needs to be triggered and/or buffers to be reuploaded (via `buffer.SetData`

) for optimisation purposes. May also help distribute the instances more uniformly.

Not a full example, but it would involve adjusting the loop in `SetupInstances()`

. Perhaps something like :

```
public float cellSize = 5; // Desired cell size, changes to fit into bounds/terrainSize
...
private void SetupInstances() {
InstanceData[] instances = new InstanceData[instanceCount];
float terrainSize = 20; // Assuming square area
// Or if using terrain,
//terrainSize = terrain.terrainData.size.x; // Assuming square terrain
int rowCount = (int)(terrainSize / cellSize);
int cellCount = rowCount * rowCount;
cellSize = terrainSize / rowCount;
int instanceCountPerCell = instanceCount / cellCount;
for (int y = 0; y < rowCount; y++) {
for (int x = 0; x < rowCount; x++) {
for (int i = 0; i < instanceCountPerCell; i++) {
Vector3 position = new(
x * cellSize + Random.Range(0, cellSize),
0,
y * cellSize + Random.Range(0, cellSize)
);
...
instances[(y * rowCount + x) * instanceCountPerCell + i] = new() {
matrix = Matrix4x4.TRS(position, rotation, scale)
};
}
}
}
if (instancesBuffer == null){
instancesBuffer = new ComputeBuffer(instanceCount, InstanceData.Size());
}
instancesBuffer.SetData(instances);
MPB.SetBuffer("_PerInstanceData", instancesBuffer);
}
```


## Remove/Hide instances on non-grass TerrainLayer

If using a **Terrain** component, we could also only spawn grass on specific **TerrainLayer**(s). To handle that we can use [TerrainData.GetAlphamaps](https://docs.unity3d.com/ScriptReference/TerrainData.GetAlphamaps.html). The docs page isn’t that clear, so to explain :

- Each TerrainLayer you assign to the Terrain generates an “alphamap” which contains the weights for that layer, which are used to blend the terrain textures together. Before these are passed to the shader, multiple alphamaps are packed into different colour channels, often called
*splatmaps*. (Which is passed into`_Control`

texture reference. Don’t confuse the splatmap with the`_Splat0`

,`_Splat1`

, etc texture references that Unity uses to pass the layer “Diffuse” textures) `GetAlphamaps(0, 0, width, height)`

returns a multi-dimensional array, where the first and second indices control the`y`

and`x`

to sample at (in terms of texels, aka texture pixels), and third index is what TerrainLayer. e.g.`[y, x, 0]`

would access the first layer.

So to limit where grass spawns, we can access `[y, x, grassLayerIndex]`

and only spawn if above a certain threshold (i.e. `> 0.5`

)

```
public int grassLayerIndex = 0; // TerrainLayer index for grass
/*
If you have multiple layers can duplicate this & grassWeight below,
Or set this to an array and loop over it (combining weights with max())
*/
...
private int cachedInstanceCount;
private void SetupInstances() {
TerrainData terrainData = terrain.terrainData;
Vector3 terrainSize = terrainData.size;
int alphamapWidth = terrainData.alphamapWidth;
int alphamapHeight = terrainData.alphamapHeight;
float[,,] maps = terrainData.GetAlphamaps(0, 0, alphamapWidth, alphamapHeight);
/*
Contains weights for painted terrain layers
Index with [ Y, X, LayerIndex ]
*/
InstanceData[] instances = new InstanceData[instanceCount];
cachedInstanceCount = instanceCount;
for (int i = 0; i < cachedInstanceCount; i++) {
...
float uvX = position.x / terrainSize.x; // 0 to 1 across terrain width
float uvY = position.z / terrainSize.z; // 0 to 1 across terrain height
...
Vector3 normal = terrainData.GetInterpolatedNormal(uvX, uvY);
...
int texelX = (int)(uvX * alphamapWidth);
int texelY = (int)(uvY * alphamapHeight);
// Remove grass from areas not painted with grass layer
float grassWeight = maps[texelY, texelX, grassLayerIndex];
if (grassWeight <= 0.5f) {
scale = Vector3.zero;
position = Vector3.one * float.NaN;
/*
If looping over full instanceCount,
can also discard / not store the instance :
*/
i--; cachedInstanceCount--; // (or convert instances to a List<>)
continue;
/*
And use cachedInstanceCount when creating buffers
and in Graphics.Draw/Render call (or indirect args).
If looping over instanceCountPerCell, must comment this out.
*/
}
instances[i] = new() {
matrix = Matrix4x4.TRS(position, rotation, scale)
};
// or instances.Add() (if List<>)
}
//cachedInstanceCount = instances.Count; // (if List<>)
...
}
```


As commented above, when looping over the full `instanceCount`

we can discard the data for that instance. But if using the setup in the previous foldout, where instances are split into cells/chunks, the `instanceCountPerCell`

needs to remain constant so we cannot discard data - only override the scale/position to *hide* it.

That would still take space in memory, but a scale of 0 and/or setting positions to NaN prevents fragments from being generated. Overriding the position also means that the instance can be culled by the frustum culling compute shader later (when using indirect instancing)

The result is :

Could perhaps also look into obtaining the actual terrain grass texture (`terrainData.terrainLayers[grassLayerIndex].diffuseTexture`

and/or tint `.diffuseRemapMin`

/`.diffuseRemapMax`

if used), to set the grass colour (via the `float4 color`

in `InstanceData`

). That might be more important if you have *multiple textures* that grass can spawn on and want it to match the ground colour.

## Simulate wind / swaying

We can also add **Vertex Displacement** to make the grass less static.

For Unity6+ versions this should be done on the *output* from the **Custom Function** node. If applied to the input, the displacement would instead be relative to each instance, but in this case we want the wind applied in the same direction for all instances.

Using **Time** into a **Sine** node setup as shown below produces a light wind/swaying effect :

Can adjust the values here for a stronger wind, but the motion may look unrealistic. You’d probably want to look into a more accurate method for that. But this is as far as I’m going for this tutorial.

## Adapting Setup for Indirect

### C# Side

There may be optimisations we can do to our instancing rendering to make it perform better, such as **Frustum Culling** on the GPU via a **Compute Shader** (which the next section provides an example of). But for that to be able to adjust the number of instances that get drawn, we first need to switch to using the **Indirect** version of the instancing function.

That also requires an additional buffer known as the “indirect arguments”, which stores :

**Index Count****Instances Count****Start Index**- (Mostly only important if you are drawing a submesh other than the first)

**Base Vertex Index**- (Set if submeshes have an offset, see
[Mesh.GetBaseVertex](https://docs.unity3d.com/ScriptReference/Mesh.GetBaseVertex.html))

- (Set if submeshes have an offset, see
**Start Instance**- (We’ll leave this at 0 to draw all instances. You might set this to a different value if the instances buffer holds data for other instanced calls. This in combination with the Instances Count would let you draw a section of that buffer. But supporting this requires additional setup on the shader side… which isn’t documented)


For older versions the function is `Graphics.DrawMeshInstancedIndirect`

. The indirect arguments should still be initalised in the below script, but we also dispatch a Compute Shader later to alter values.

```
...
#region IndirectArgs
private ComputeBuffer argsBuffer;
private void SetupIndirectArgs(){
argsBuffer = new ComputeBuffer(1, args.Length * sizeof(uint), ComputeBufferType.IndirectArguments);
// Init
uint[] args = new uint[5] { 0, 0, 0, 0, 0 };
args[0] = (uint)mesh.GetIndexCount(0);
args[1] = (uint)instanceCount;
// and optionally,
args[2] = (uint)mesh.GetIndexStart(0);
args[3] = (uint)mesh.GetBaseVertex(0);
args[4] = 0;
argsBuffer.SetData(args);
}
#endregion
void OnEnable() {
if (instancesBuffer != null) return;
SetupInstances();
SetupIndirectArgs();
//... (etc, see previous setup)
}
void OnDisable() {
if (instancesBuffer != null) {
instancesBuffer.Release();
instancesBuffer = null;
}
if (argsBuffer != null) {
argsBuffer.Release();
argsBuffer = null;
}
}
void Update() {
if (instanceCount <= 0 || instancesBuffer == null) return;
if (argsBuffer == null) return;
Graphics.DrawMeshInstancedIndirect(mesh, 0, material, bounds, argsBuffer, 0, MPB, castShadows, receiveShadows);
}
```


As of Unity 2021.2 we use `Graphics.RenderMeshIndirect`

.

Compared to the older `DrawMeshInstancedIndirect`

, the newer function seemingly allows for multiple draw commands from the same function call. (Though currently these still apparently end up as separate draw calls - [related issue](https://issuetracker.unity3d.com/issues/graphics-dot-rendermeshindirect-does-not-issue-multi-draw-rendering-commands-when-using-a-graphics-api-capable-of-multi-draw-commands))

Unity also provides the [GraphicsBuffer.IndirectDrawIndexedArgs](https://docs.unity3d.com/ScriptReference/GraphicsBuffer.IndirectDrawIndexedArgs.html) struct to hold the indirect arguments (with proper field/property names rather than needing to use a `uint[5]`

and remember what they correspond to! Though note the order is as mentioned above, not alphabetical as they are in the documentation… which will be somewhat important later). These should still be initalised in the script, but we can also dispatch a Compute Shader later to alter values.

```
#region IndirectArgs
private GraphicsBuffer indirectBuffer;
private GraphicsBuffer.IndirectDrawIndexedArgs[] commandData;
private int commandCount;
private void SetupIndirectArgs() {
commandCount = 1;
commandData = new GraphicsBuffer.IndirectDrawIndexedArgs[commandCount];
commandData[0].indexCountPerInstance = mesh.GetIndexCount(0);
commandData[0].instanceCount = (uint)instanceCount;
// and optionally,
commandData[0].startIndex = mesh.GetIndexStart(0);
commandData[0].baseVertexIndex = mesh.GetBaseVertex(0);
commandData[0].startInstance = 0;
indirectBuffer = new GraphicsBuffer(GraphicsBuffer.Target.IndirectArguments, commandCount, GraphicsBuffer.IndirectDrawIndexedArgs.size);
indirectBuffer.SetData(commandData);
}
#endregion
void OnEnable() {
if (instancesBuffer != null) return;
SetupInstances();
SetupIndirectArgs();
//... (etc, see previous setup)
}
void OnDisable() {
instancesBuffer?.Release();
instancesBuffer = null;
indirectBuffer?.Release();
indirectBuffer = null;
}
void Update() {
if (instanceCount <= 0 || instancesBuffer == null) return;
if (indirectBuffer == null) return;
Graphics.RenderMeshIndirect(rParams, mesh, indirectBuffer, commandCount);
}
```


### Shader Graph

At least for this tutorial, we don’t really *need* changes on the shader side to support the `Indirect`

instancing functions, provided you leave the `startInstance`

in the indirect arguments Buffer at 0, and only have a single command.

## What if we have a different startInstance?

When setting `startInstance`

, you need to offset the Instance ID in the shader to take that into account. But that doesn’t need to be done on *all* Graphics APIs - Vulkan and WebGPU seem to bake it into `SV_InstanceID`

so it renders the correct instances without an offset. To handle these platform differences, Unity 2021.2+ added functions in an `UnityIndirect.cginc`

include file in the built-in shaders (can be used by all render pipelines). If you want to view the file, download the shaders source from [Unity’s download archive](https://unity.com/releases/editor/archive) (click “See All” of an appropriate version → “Other installs” → Shaders. Will be under CGIncludes folder)

(For older versions… I haven’t tested, but you’d probably need to pass the `startInstance`

in a separate float property, or if set on GPU maybe try passing the 5 uint `argsBuffer`

manually and index it (`[4]`

would be the `startInstance`

). Apply the offset (`unity_InstanceID + offset`

) inside an `#if !defined(SHADER_API_VULKAN) && !defined(SHADER_API_WEBGPU)`

block to avoid it on those platforms)

For Unity 2021.2+ we can do :

```
#define UNITY_INDIRECT_DRAW_ARGS IndirectDrawIndexedArgs
#include "UnityIndirect.cginc"
```


This adds functions that return uints, accessing the CommandID and Indirect Arguments :

`GetCommandID(svDrawID)`

`GetIndirectVertexCount()`

: (Actually index count for indexed/mesh calls)`GetIndirectInstanceCount()`

: (Number of instances drawn)`GetIndirectInstanceID(svInstanceID)`

: (Returns 0 to InstanceCount, where 0 is first instance actually being drawn)`GetIndirectVertexID(svVertexID)`

: (Returns 0 to VertexCount, presumably. More important for RenderPrimitivesX calls)

The example in the [RenderMeshIndirect docs page](https://docs.unity3d.com/6000.3/Documentation/ScriptReference/Graphics.RenderMeshIndirect.html) uses some of these to set positions and colours (though that’s mostly only a test setup)

But a few of these functions have *two* versions, which aren’t mentioned by the docs :

`GetIndirectInstanceID_Base(svInstanceID)`

`GetIndirectVertexID_Base(svVertexID)`


I haven’t seen *any* examples that actually use these `_Base`

versions, but afaik they are what you should **use to correctly index a buffer**, assuming it contains the full data set.

In the case of `GetIndirectInstanceID`

/ `GetIndirectInstanceID_Base`

, these are defined as :

```
#if defined(SHADER_API_VULKAN) || defined(SHADER_API_WEBGPU)
GetIndirectInstanceID(IndirectDrawIndexedArgs args, uint svInstanceID) {
return svInstanceID - args.startInstance;
}
uint GetIndirectInstanceID_Base(IndirectDrawIndexedArgs args, uint svInstanceID) {
return svInstanceID;
}
#else
GetIndirectInstanceID(IndirectDrawIndexedArgs args, uint svInstanceID) {
return svInstanceID;
}
uint GetIndirectInstanceID_Base(IndirectDrawIndexedArgs args, uint svInstanceID) {
return svInstanceID + args.startInstance;
}
#endif
// (Later also defines functions without the first input, which is what
// "#define UNITY_INDIRECT_DRAW_ARGS IndirectDrawIndexedArgs" before the #include is for.
// For non-indexed draw functions you would use IndirectDrawArgs instead on both C#/shader sides.
```


I haven’t really checked/tested the VertexID versions as those are typically used for `DrawProceduralIndirect/RenderPrimitivesIndirect`

rather than mesh based functions so aren’t as relevant here. I think the examples on [RenderPrimitivesIndirect](https://docs.unity3d.com/ScriptReference/Graphics.RenderPrimitivesIndirect.html) and [RenderPrimitivesIndexedIndirect](https://docs.unity3d.com/ScriptReference/Graphics.RenderPrimitivesIndexedIndirect.html) actually incorrectly uses `GetIndirectVertexID`

instead of `GetIndirectVertexID_Base`

, which only works because it doesn’t set `startIndex`

or uses submesh 0… Whoops? 🙃)

## Example using UnityIndirect.cginc (Unity 2021.2+)

```
#ifndef GRASS_INSTANCED_INCLUDED
#define GRASS_INSTANCED_INCLUDED
#define UNITY_INDIRECT_DRAW_ARGS IndirectDrawIndexedArgs
#include "UnityIndirect.cginc"
// Declare structure & buffer for passing per-instance data
// This must match the C# side
struct InstanceData {
float4x4 m;
//float4 color;
StructuredBuffer<InstanceData> _PerInstanceData;
// Shader Graph function(s)
void Instancing_float(float3 Position, float InstanceID, out float3 OutPosition, out float3 OutNormal){
InitIndirectDrawArgs(0);
uint index = GetIndirectInstanceID_Base(InstanceID);
InstanceData data = _PerInstanceData[index];
OutPosition = mul(data.m, float4(Position, 1)).xyz;
OutNormal = mul(data.m, float4(0, 1, 0, 0)).xyz;
}
// (and same GetIndirectInstanceID_Base usage in other functions where buffers are indexed using InstanceID)
#endif
```


If you set multiple commands in the `indirectBuffer`

for the `RenderMeshIndirect`

call, you may also need to access the `uint commandID = GetCommandID(0);`

and use that to offset the buffer index further. But how likely depends how the `instancesBuffer`

data is formatted.

## Adding GPU Frustum Culling

Now that we’ve switched to `Indirect`

we can add **Frustum Culling** to prevent instances being drawn outside of the camera view, as well as optionally limit the distance we render at (if you want that different from the camera’s far plane value)



![(Image)](../../assets/cfcb7d6bfcdc7685.png)

500K instances in an 256x256 area.

Rendering ~89K instances due to frustum culling (FOV = 60 & Far Plane = 100).

In my case performs 500FPS+ regardless of frustum culling (but it does help), but scene is empty and measured based on a (few years old) high-end PC GPU. Probably better to profile for yourself.

The implementation will include :

- Provide an additional
`uint`

buffer using the “Append” type, which will hold indices of which instances to draw. - Use a Compute Shader to check which instance positions are within the camera frustum and append them to that buffer. I’ll be transforming the positions into clip space to handle that.
- The instanceCount in the indirect args buffer will be updated to match the count of this buffer. Can handle this by using
[GraphicsBuffer.CopyCount](https://docs.unity3d.com/ScriptReference/GraphicsBuffer.CopyCount.html)to copy a “hidden counter” associated with the Append buffer to the Indirect Args buffer. - In the shader graph include file, we index this ViewIndices buffer using the InstanceID and use that result to index the PerInstance buffer, (rather than using the InstanceID directly)

### Compute Shader

Firstly let’s set up the compute shader. This should be a file with the `.compute`

file extension.

```
#pragma kernel FrustumCullInstances
#include "Instancing.hlsl" // ShaderGraph include file (assumes this is in the same folder)
// Alternatively, copy structure & buffers. But as we must keep them in sync, it's easier to use an #include
/*
struct InstanceData {
float4x4 m;
// Layout must match C# side
};
StructuredBuffer<InstanceData> _PerInstanceData;
*/
AppendStructuredBuffer<uint> _VisibleIDsAppend; // Buffer that holds the indices of visible instances
float4x4 _Matrix; // (matrix passed in should convert to Clip Space e.g. projection * view * model)
float _MaxDrawDistance;
uint _StartOffset;
[numthreads(64, 1, 1)]
void FrustumCullInstances (uint3 id : SV_DispatchThreadID) {
InstanceData data = _PerInstanceData[_StartOffset + id.x];
float4 absPosCS = abs(mul(_Matrix, float4(data.m._m03_m13_m23, 1.0)));
if ( absPosCS.x <= absPosCS.w * 1.1 + 0.5
&& absPosCS.y <= absPosCS.w * 1.1 + 0.5 // (scaling/padding hides pop-in/out at screen edges)
&& absPosCS.z <= absPosCS.w
&& absPosCS.w <= _MaxDrawDistance // optional max draw distance
// Is inside camera frustum
+ id.x);
}
}
```


## What is [numthreads(64, 1, 1)] ?

The values here specify the number of threads in each thread-group that will be dispatched, since GPUs are all about executing things in parallel. Our buffer data is one dimensional so it makes sense to only use the X workgroup size (defined by `[numthreads()]`

), leaving Y and Z at 1. (But if instances were split into cells would probably use a 2D thread count)

I don’t want to go too deep into the GPU hardware/architecture, (I’m sure there’s better tutorials for that), but typically these values should multiply together to a minimum of 64 (e.g. `(64, 1, 1)`

, `(8, 8, 1)`

, etc.) - as most AMD GPUs execute in groups of 64 threads and lower sizes would just cause some to be idle. Some newer AMD GPUs ([RDNA](https://en.wikipedia.org/wiki/RDNA_(microarchitecture))) and NVIDIA GPUs use groups of 32 instead, but specifying a size of 64 is still easier to support all cases without wasted threads.

When googling around you might see the terms “wavefront” and “warp” which traditionally correspond to these 64/32 sized groups of threads, though are also often used interchangeablely.

To handle the culling, the compute shader transforms the instance positions (extracted from the matrices using `_m03_m13_m23`

) into **Clip Space**. This is the same space that vertex shaders typically output to, though in this case the projection matrix used will be passed from the C# script without using `GL.GetGPUProjectionMatrix`

, so follows the **OpenGL** conventions that Unity uses by default. This is useful as we don’t need to worry about [how the clip space Z would differ in other graphics APIs](https://docs.unity3d.com/Manual/SL-PlatformDifferences.html#:~:text=%E2%80%931.0%20at%20the%20near%20plane%20to%20%2B1.0).

To test whether this point is within the camera frustum, we simply take the `abs()`

, and use `<=`

to compare against the W component. When this passes we add the index to the `AppendStructuredBuffer`

.

This works because while the camera culls in a *frustum* in terms of **View space**. After the projection matrix, that area is a **cube** in **Clip space** (in OpenGL convention at least), with XYZ components ranging from **-W to W** (where W is the fourth component of that position). For the XY axis, (0,0) is the screen center. For the Z axis, **-W is at the near plane and W is at the far plane**. (Meaning the camera would typically be at some Z distance smaller than -W. We don’t normally need the camera’s position in clipspace but might be good to have that kind of reference point to help you visualise the space)

Also note that `Z=0`

wouldn’t be half-way between as depth is *non-linear* - as explained further in my post on [Depth](https://www.cyanilux.com/tutorials/depth/).

### C# Changes

On the C# side we need to set up that additional buffer and pass it to the instanced rendering & compute shader (which is exposed to and assigned in the inspector). Note that the property names are different to avoid conflicts (when using the `#include`

line in the compute shader), because the buffer needs to be defined as an **AppendStructuredBuffer** in the compute shader but a **StructuredBuffer** in the regular shader to be able to index it. (Hence `_VisibleIDsAppend`

and `_VisibleIDs`

)

```
public ComputeShader computeFrustumCulling;
...
void SetupInstances(){
...
visibleBuffer = new ComputeBuffer(instanceCount, sizeof(uint), ComputeBufferType.Append);
// may also want to initalise to showing all instances, not sure how important that is though.
/*
uint[] ids = new uint[instanceCount];
...
ids[i] = i;
...
visibleBuffer.SetData(ids);
*/
}
void OnEnable() {
...
rParams.matProps.SetBuffer("_VisibleIDs", visibleBuffer);
int kernel = 0;
/*
0 to reference first kernel in compute file
Could alternatively use computeFrustumCulling.FindKernel("FrustumCullInstances");
and cache that in a private variable for use in Update too
*/
computeFrustumCulling.SetBuffer(kernel, "_PerInstanceData", instancesBuffer);
computeFrustumCulling.SetBuffer(kernel, "_VisibleIDsAppend", visibleBuffer);
computeFrustumCulling.SetFloat("_MaxDrawDistance", 100);
computeFrustumCulling.SetInt("_StartOffset", 0); // set to "Start Instance" in indirect args if used
}
void OnDisable() {
...
visibleBuffer?.Release();
visibleBuffer = null;
}
```


For `Update()`

we reset a “hidden counter” on the append buffer which keeps track of how many elements are in the buffer. Then pass the view projection matrix to the compute shader and `Dispatch`

to execute it. To update the instance count used by the instancing call, we copy the counter to the Indirect Args Buffer by using `GraphicsBuffer.CopyCount`

. The third parameter of that needs to be `1 * sizeof(uint)`

(equivalent to a value of 4) as the instance count is the second uint in the buffer. This occurs on the GPU without copying to / stalling the CPU.

(Of note, the actual append buffer size/length is fixed when the ComputeBuffer is created. The counter just allows `Append()`

calls in the shader to override existing data. Without the reset, appending would continue to increment the hidden counter every frame. It wouldn’t write to the buffer out of bounds, but it would cause the instanced rendering to draw many overlapping instances (indexing the first _PerInstanceData entry) before crashing)

void Update() { if (instanceCount <= 0 || instancesBuffer == null) return; if (argsBuffer == null) return;

```
// Frustum Culling
if (computeFrustumCulling != null) {
// Reset Visible Buffer
visibleBuffer?.SetCounterValue(0);
// Set Matrix & Dispatch Compute Shader
Camera cam = Camera.main;
Matrix4x4 m = Matrix4x4.Translate(bounds.center);
Matrix4x4 v = cam.worldToCameraMatrix;
Matrix4x4 p = cam.projectionMatrix;
// With regular shaders you'd normally use GL.GetGPUProjectionMatrix to convert this matrix to graphics API being used
// but in this case the compute shader expects the OpenGL convention that Unity uses by default
Matrix4x4 mvp = p * v * m;
// (If instanced matrices are stored in world space can remove the m matrix here)
computeFrustumCulling.SetMatrix(prop_Matrix, mvp);
/*
Note : If you have multiple objects creating grass,
either need to make sure the buffers are set here.
Or create & use an instance of the compute shader, e.g.
Instantiate(computeFrustumCulling) in Start() & Destroy that in OnDestroy()
*/
int kernel = 0; // or cache computeFrustumCulling.FindKernel("FrustumCullInstances");
uint numthreads = 64;
// keep in sync with compute shader, or set automatically with :
//computeFrustumCulling.GetKernelThreadGroupSizes(kernel, out numthreads, out _, out _);
// (probably in OnEnable & cache in private variable for usage here)
computeFrustumCulling.Dispatch(kernel, Mathf.CeilToInt((float)instanceCount / numthreads), 1, 1);
// Copy Counter to Instance Count in Indirect Args
ComputeBuffer.CopyCount(visibleBuffer, argsBuffer, 1 * sizeof(uint));
}
Graphics.DrawMeshInstancedIndirect(mesh, 0, material, bounds, argsBuffer, 0, MPB, castShadows, receiveShadows);
```


}

```
private readonly int prop_Matrix = Shader.PropertyToID("_Matrix");
void Update() {
if (instanceCount <= 0 || instancesBuffer == null) return;
if (indirectBuffer == null) return;
// Frustum Culling
if (computeFrustumCulling != null) {
// Reset Visible Buffer
visibleBuffer?.SetCounterValue(0);
// Set Matrix & Dispatch Compute Shader
Camera cam = Camera.main;
Matrix4x4 m = Matrix4x4.Translate(bounds.center);
Matrix4x4 v = cam.worldToCameraMatrix;
Matrix4x4 p = cam.projectionMatrix;
// With regular shaders you'd normally use GL.GetGPUProjectionMatrix to convert this matrix to graphics API being used
// but in this case the compute shader expects the OpenGL convention that Unity uses by default
Matrix4x4 mvp = p * v * m;
// (If instanced matrices are stored in world space can remove the m matrix here)
computeFrustumCulling.SetMatrix(prop_Matrix, mvp);
/*
Note : If you have multiple objects creating grass,
either need to make sure the buffers are set here.
Or create & use an instance of the compute shader, e.g.
Instantiate(computeFrustumCulling) in Start() & Destroy that in OnDestroy()
*/
uint numthreads = 64;
// keep in sync with compute shader, or set automatically with :
//computeFrustumCulling.GetKernelThreadGroupSizes(kernel, out numthreads, out _, out _);
// (probably in OnEnable & cache in private variable for usage here)
int kernel = 0; // or cache computeFrustumCulling.FindKernel("FrustumCullInstances");
computeFrustumCulling.Dispatch(kernel, Mathf.CeilToInt(instanceCount / numthreads), 1, 1);
// Copy Counter to Instance Count in Indirect Args
GraphicsBuffer.CopyCount(visibleBuffer, indirectBuffer, 1 * sizeof(uint));
}
Graphics.RenderMeshIndirect(rParams, mesh, indirectBuffer, commandCount);
}
```


The values in the `Dispatch`

call are how many thread-groups to launch, so to run the compute shader on `instanceCount`

, we need to divide by the thread-group sizes we set in the compute shader. Can either hardcode this and be sure to keep them in sync, or call [ComputeShader.GetKernelThreadGroupSizes.html](https://docs.unity3d.com/Documentation/ScriptReference/ComputeShader.GetKernelThreadGroupSizes.html).

Note that we also cast the count to float and round up (using `Mathf.CeilToInt`

) to ensure we dispatch enough thread-groups to cover all the instances. Though this sometimes means threads are wasted - though unlikely to make much difference on performance. Could make `instanceCount`

a multiple of the `numthreads`

(64) to avoid that.

Note that the implementation above uses `Camera.main`

so always culls based on the Main Camera, even for Scene View. Can use the following to change that (but doesn’t seem to update instantly - only on focus changes)

```
Camera cam = Camera.main;
#if UNITY_EDITOR
if (Camera.current != null) {
cam = Camera.current;
}
#endif
```


### Shader Graph Include File Changes

Finally, we need to adjust the file used by our **Custom Function** node(s) to define the VisibleIDs Buffer (`_VisibleIDs`

), index it using the **InstanceID** and use the result to index `_PerInstanceData`

:

```
#ifndef GRASS_INSTANCED_INCLUDED
#define GRASS_INSTANCED_INCLUDED
// Declare structure & buffer for passing per-instance data
struct InstanceData {
float4x4 m;
//float4 color;
// Layout must match C# side
StructuredBuffer<InstanceData> _PerInstanceData;
StructuredBuffer<uint> _VisibleIDs;
void Instancing_float(float3 Position, uint InstanceID, out float3 OutPosition, out float3 OutNormal){
uint index = _VisibleIDs[InstanceID];
InstanceData data = _PerInstanceData[index];
OutPosition = mul(data.m, float4(Position, 1)).xyz;
OutNormal = mul(data.m, float4(0, 1, 0, 0)).xyz;
}
// If using other per-instance data for fragment stage, update this too
void InstancingFragment_float(float InstanceID, out float4 Out){
uint index = _VisibleIDs[InstanceID];
InstanceData data = _PerInstanceData[index];
Out = data.color;
}
#endif
```


```
#ifndef GRASS_INSTANCED_INCLUDED
#define GRASS_INSTANCED_INCLUDED
// Declare structure & buffer for passing per-instance data
// This must match the C# side
struct InstanceData {
float4x4 m;
//float4 color;
StructuredBuffer<InstanceData> _PerInstanceData;
StructuredBuffer<uint> _VisibleIDs;
#if UNITY_ANY_INSTANCING_ENABLED
void InstancingMatrices(inout float4x4 objectToWorld, out float4x4 worldToObject) {
uint index = _VisibleIDs[unity_InstanceID];
InstanceData data = _PerInstanceData[index];
// ... (rest is same as before)
#endif
// If using functions that access other per-instance data, update those too. e.g.
void InstancingFragment_float(out float4 Out){
uint index = _VisibleIDs[unity_InstanceID];
InstanceData data = _PerInstanceData[index];
Out = data.color;
}
```


Note that the **Instance ID** will also no longer be consistent. If using that in the graph for other calculations (e.g. I use it with **Random Range** to select a random tile from the texture, which flickers with the culling), we’d need to add an additional **Custom Function** to obtain the new index :

```
void VisibleID_float(uint InstanceID, out float Out){
Out = _VisibleIDs[InstanceID];
}
```


Though this also assumes the instances buffer is consistent. If that changes you’d likely need to store a random value in the InstanceData struct instead. (In the past I used the `color.a`

for that, as transparency isn’t used)

If also using the `GetInstanceID_float`

snippet from earlier (e.g. with **Random Range** to select a random tile from the texture), we need to alter that function to return the updated ID, as `unity_InstanceID`

will no longer be consistent (so flicker between tiles) with the frustum culling :

```
void GetInstanceID_float(out float Out){
Out = 0;
#ifndef SHADERGRAPH_PREVIEW
#if UNITY_ANY_INSTANCING_ENABLED
= _VisibleIDs[unity_InstanceID];
#endif
#endif
```


Though this also assumes the instances buffer is consistent. If that changes you’d likely need to store a random value in the InstanceData struct instead. (In the past I used the `color.a`

for that, as transparency isn’t used)

## Wrap up

For further optimisations, it could also make sense to try implementing **Occlussion Culling**, to stop rendering grass that is behind other objects. Probably more important for scenes that contain many objects/walls/hills that could actually block large amounts of grass. If you want to look into that, I’ve seen examples from others that uses a **Hierarchical Depth (Hi-Z) Buffer** to do this I think. But not something I’ve looked into, and this post is already long enough…

Compared to my old FAQ example, this took much longer than expected to write, (the tabs to change page content for different Unity versions probably didn’t help that). Hopefully I didn’t ramble on too much, but I’m sure it’ll be useful regardless!~

## Thanks for reading! 😊

If you find this post helpful, please consider sharing it with others / on socials

Donations are also **greatly** appreciated! 🙏✨

(Keeps this site free from ads and allows me to focus more on tutorials)