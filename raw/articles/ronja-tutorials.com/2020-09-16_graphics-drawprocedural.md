---
title: Graphics.DrawProcedural
url: https://www.ronja-tutorials.com/post/051-draw-procedural/
published: '2020-09-16'
source_blog: Ronja’s Shader Tutorials
source_site: https://www.ronja-tutorials.com/
category: graphics
fetched: '2026-04-13'
---

The last tutorial was about compute shader basics, how to generate values, read them back to the cpu and use them. One critical aspect in all that is that copying data from the cpu to the gpu (from the ram to the vram) or back takes some time, so wouldn’t it be neat if there was a way to just render the data directly from the GPU without copying it around? Thats where Graphics.DrawProcedural and similar methods come into play, they allow us to do exactly that. So lets build on the result of that tutorial but without using GameObjects for rendering.

First lets remove all code connected to rendering using GameObjects. We don’t need the output array anymore, not the GameObject instances where we stored the Transforms, we don’t need to create them in the start method and don’t need to update their positions in the Update method.

The way Graphics.DrawProcedural works is that all the shader gets as information is the index of the current vertex. That also means we’ll have to make the vertices available to shader ourselves via more compute buffers and then write a custom shader to read from those buffers. Lets add a mesh and a material to our public class variables so we can set them from the inspector and use their data for rendering. Since we’re filling the mentioned buffers ourselves its not nessecary for that data to come from a mesh or even exist in the ram at any point.

/// class variables
public Mesh Mesh;
public Material Material;

In this case we don’t need uv coordinates or normals, so we’ll just create 2 buffers, one for the triangles and one for the positions. The way those work is that each pair of 3 integers in the triangles array define a triangle to be rendered by its index positions in the vertex position array. Just like the previous result array we also need to discard this one at some point (In our case in the OnDestroy method).

The stride (size of a single variable in the buffer) is simply the size of the base type times the components (1 for scalar values and 3 for 3d vectors). And after creating the buffers we already fill them once at the start.

/// class variables

///in Start method
//gpu buffers for the mesh
int[] triangles = Mesh.triangles;
meshTriangles = new ComputeBuffer(triangles.Length, sizeof(int));
meshTriangles.SetData(triangles);
Vector3[] positions = Mesh.vertices;
meshPositions = new ComputeBuffer(positions.Length, sizeof(float) * 3);
meshPositions.SetData(positions);

To allow the material to read from the buffers we just call SetBuffer just like we’d call SetColor or SetTexture.

///in Start method
//give data to shaders
"SphereLocations", resultBuffer);
Material.SetBuffer("Triangles", meshTriangles);
Material.SetBuffer("Positions", meshPositions);

Now we have most things we need to call the DrawProcedural method, but if you take a look at it one of the non-optional arguments we havent accounted for is still the bounds of what we’re drawing. This is here for frustum culling and in our case we can quickly calculate them by creating 40x40 units bounds at the origin and passing them. The reason for the bounds in this case are the compute shader spits out positions in a sphere with a 20 unit radius around the origin.

///class variable

///in start method
//bounds for frustum culling (20 is a magic number (radius) from the compute shader)
new Bounds(Vector3.zero, Vector3.one * 20);

After the material and the bounds are passed the next argument is the topology. Changing that allows us to draw lines, dots or even quads (though they’re slow), but in most cases we like to stick to triangles and its also what our mesh data gave us. Then we pass in the length of the triangle array since in this case we want to run the vertex stage once per trangle corner, not once per position. And we pass the amount of spheres as the instance count. We could also queue the triangle amount times the sphere amount and figure out which sphere we’re in in the shader but this approach makes writing our shader a whole bit easier.

The shader is actually pretty straightforward. We can use the the result of the basics series to start. Then the first few changes are that we throw out the texture rendering and to mark the color property with [HDR] to allow us to go to values beyond 1 and play with bloom up there.

Next we can just delete the appdata and v2f structs. We’re not getting any data from a mesh and we’re not passing any data to the fragment stage. Instead we add our 3 buffers, since we don’t have to write to them we can just make them StructuredBuffers without the read-write functionality.

Then we change the return type of our vertex function to float4 and give it the : SV_POSITION attribute, similarly to the SV_TARGET of the fragment function. The arguments our vertex function now takes are the vertex id as well as the instance id, marked via SV_VertexID and SV_InstanceID.

Our first step is now to get the index of the position in the position list thats saved in the triangle buffer, just like in the compute shader we can access the buffer here like we would with an array in most languages. After getting the position index based on the vertex id, we use that to get the actual position from the position buffer. Then we also add the location of the current sphere by using instance id to the position.

And lastly we transform the position from worldspace to clip space by multiplying the view-projection matrix with it. This isn’t anything we haven’t done yet, it was just hidden in UnityObjectToClipPos until now, which internally only does mul(UNITY_MATRIX_VP, mul(unity_ObjectToWorld, float4(pos, 1.0))); where the inner mul transforms the position to the world coordinates and the outer one to clip coordinates.

//the vertex shader function
float4 vert(uint vertex_id: SV_VertexID, uint instance_id: SV_InstanceID) : SV_POSITION{
//get vertex positionint positionIndex = Triangles[vertex_id];
float3 position = Positions[positionIndex];
//add sphere position
position += SphereLocations[instance_id];
//convert the vertex position from world space to clip spacereturn mul(UNITY_MATRIX_VP, float4(position, 1));
}

And with all of that you rendered objects at positions the cpu never knew about! And depending on your situation that can be pretty fast.

Because we left the world of GameObjects and Transforms theres no easy way to resize objects in this thing, which is a thing I want to do. So lets add that functionality by just multiplying all positions with a value before putting them into the buffer with a linq function.

Vector3[] positions = Mesh.vertices.Select(p => p * Scale).ToArray(); //adjust scale here
new ComputeBuffer(positions.Length, sizeof(float) * 3);
meshPositions.SetData(positions);

Also as a tiny note microsoft is very clear in their docs that they prefer the content type of structured buffers to have a stride thats a power of 2 (more specifically a value 128 is dividable by), but in my playing around with float3 and float4 they seemed very similar in performance. Do with that information what you will.

Oh, and I moved the the calculation of the thread group count as well as the setting of the result buffer to the compute kernel to the Start method.

usingSystem;
usingSystem.Collections;
usingSystem.Collections.Generic;
usingUnityEngine;
usingSystem.Linq;
publicclassProceduralComputeSpheres : MonoBehaviour
{
//rough outline for data
publicint SphereAmount = 17;
public ComputeShader Shader;
//what is rendered
public Mesh Mesh;
public Material Material;
publicfloat Scale = 1;
//internal data
int kernel;
uint threadGroupSize;
Bounds bounds;
int threadGroups;
void Start()
{
//program we're executing
"Spheres");
Shader.GetKernelThreadGroupSizes(kernel, out threadGroupSize, out _, out _);
//amount of thread groups we'll need to dispatch
int) ((SphereAmount + (threadGroupSize - 1)) / threadGroupSize);
//gpu buffer for the sphere positions
new ComputeBuffer(SphereAmount, sizeof(float) * 3);
//gpu buffers for the mesh
int[] triangles = Mesh.triangles;
meshTriangles = new ComputeBuffer(triangles.Length, sizeof(int));
meshTriangles.SetData(triangles);
Vector3[] positions = Mesh.vertices.Select(p => p * Scale).ToArray(); //adjust scale here
new ComputeBuffer(positions.Length, sizeof(float) * 3);
meshPositions.SetData(positions);
//give data to shaders
"Result", resultBuffer);
Material.SetBuffer("SphereLocations", resultBuffer);
Material.SetBuffer("Triangles", meshTriangles);
Material.SetBuffer("Positions", meshPositions);
//bounds for frustum culling (20 is a magic number (radius) from the compute shader)
new Bounds(Vector3.zero, Vector3.one * 20);
}
void Update()
{
//calculate positions
"Time", Time.time);
Shader.Dispatch(kernel, threadGroups, 1, 1);
//draw result
void OnDestroy()
{
resultBuffer.Dispose();
meshTriangles.Dispose();
meshPositions.Dispose();
}
}

Shader "Tutorial/051_ProceduralSpheres"{
//show values to edit in inspector
Properties{
[HDR] _Color ("Tint", Color) = (0, 0, 0, 1)
}
SubShader{
//the material is completely non-transparent and is rendered at the same time as the other opaque geometry
Tags{ "RenderType"="Opaque""Queue"="Geometry" }
Pass{
CGPROGRAM
//include useful shader functions#include "UnityCG.cginc"//define vertex and fragment shader functions#pragma vertex vert
#pragma fragment frag
//tint of the texture
fixed4 _Color;
//buffers
StructuredBuffer<float3> SphereLocations;
StructuredBuffer<int> Triangles;
StructuredBuffer<float3> Positions;
//the vertex shader function
float4 vert(uint vertex_id: SV_VertexID, uint instance_id: SV_InstanceID) : SV_POSITION{
//get vertex positionint positionIndex = Triangles[vertex_id];
float3 position = Positions[positionIndex];
//add sphere position
position += SphereLocations[instance_id];
//convert the vertex position from world space to clip spacereturn mul(UNITY_MATRIX_VP, float4(position, 1));
}
//the fragment shader function
fixed4 frag() : SV_TARGET{
//return the final color to be drawn on screenreturn _Color;
}
ENDCG
}
}
Fallback "VertexLit"
}

// Each #kernel tells which function to compile; you can have many kernels#pragma kernel Spheres#include "Random.cginc"//variables
RWStructuredBuffer<float3> Result;
uniformfloat Time;
[numthreads(64,1,1)]
void Spheres (uint3 id : SV_DispatchThreadID)
{
//generate 2 orthogonal vectors
float3 baseDir = normalize(rand1dTo3d(id.x) -0.5) * (rand1dTo1d(id.x)*0.9+0.1);
float3 orthogonal = normalize(cross(baseDir, rand1dTo3d(id.x +7.1393) -0.5)) * (rand1dTo1d(id.x+3.7443)*0.9+0.1);
//scale the time and give it a random offsetfloat scaledTime = Time *2+ rand1dTo1d(id.x) *712.131234;
//calculate a vector based on vectors
float3 dir = baseDir * sin(scaledTime) + orthogonal * cos(scaledTime);
Result[id.x] = float3(dir *20);
}

I hope you enjoyed my tutorial ✨. If you want to support me further feel free to follow me on twitter,
throw me a one-time donation via ko-fi
or support me on patreon
(I try to put updates also there, but I fail most of the time, bear with me 💖).