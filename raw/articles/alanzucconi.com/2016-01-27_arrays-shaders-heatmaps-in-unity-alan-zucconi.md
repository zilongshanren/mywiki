---
title: 'Arrays & shaders: heatmaps in Unity - Alan Zucconi'
url: https://www.alanzucconi.com/2016/01/27/arrays-shaders-heatmaps-in-unity3d/
author: Alan Zucconi
published: '2016-01-27'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This tutorial explains how to pass arrays to shaders in Unity. This feature has been present for a long time, but is mostly undocumented. [Unity 5.4.0 Beta 1](https://unity3d.com/unity/beta/unity5.4.0b1) will introduce a proper API to pass arrays to shaders; this technique however will work with any previous version.

[Introduction](https://www.alanzucconi.com#intro)- Step 1:
[The arrays](https://www.alanzucconi.com#step1) - Step 2:
[The shader](https://www.alanzucconi.com#step2) - Step 3:
[The C# code](https://www.alanzucconi.com#step3) - Step 4:
[A more general approach](https://www.alanzucconi.com#step4) [Conclusion & download](https://www.alanzucconi.com#conclusion)

If you are using Unity 5.4+, please refer to the [Arrays & Shaders in Unity 5.4+](https://www.alanzucconi.com/?p=5745) tutorial.

One of the characteristic which makes shaders hard to master is the lack of a proper documentation. Most developers learn shaders by messing up with the code, without having a deep knowledge of what’s going on. The problem is amplified by the fact that Cg / HLSL makes lot of assumptions, some of which are not properly advertised. Unity3D allows C# scripts to communicate to shaders using methods such as `SetFloat`

, `SetInt`

, `SetVector`

and so on. Unfortunately, Unity3D doesn’t have a `SetArray`

property method, which led many developers to believe Cg / HLSL doesn’t support arrays either. Which is not true. This post will show how is possible to pass arrays to shaders. Just remember that GPUs are highly optimised for parallel computations, and that using for loops within a shader will dramatically drops its performance.

![heatmap4](../../assets/469bfddfa0508549.gif)

If you are familiar with heatmaps, you’ll know that they visualise the density of a certain phenomenon using a colour gradient. They are usually generated from a set of points, each one with its radius and intensity. There is no easy way to implement a heatmap in a shader, without using arrays. What we are going to do is to pass a list of points to the material, and iterate on each one to calculate its colour contribution for every pixel of the image. There are then three pieces of information needed for each points: its position, its radius and its intensity. Since Unity3D doesn’t provide APIs to set arrays, they won’t be mentioned in the `Properties`

section of the shader. Instead, they’ll be declared as the follow:

uniform int _Points_Length; // How many points uniform float3 _Points [100]; // The positions (x,y,z) uniform float2 _Properties [100] // The properties (x = radius, y = intensity)

Cg / HLSL doesn’t support arrays with variable size, so they need to be initialised with the maximum number of points (100, in this example). We also have to signal to the shader that these variables will be modified from outside, hence the `uniform`

qualifier. As it happens in C, there is an extra variable which indicates how many points are actually used.

It’s possible to notice that instead of having three variables per each point, we only have two. This is due to a nasty ~~bug~~ feature of Cg which doesn’t allow arrays such as `float _Intensities [100]`

to be accessed from outside the shader. All the arrays we want to access from C# must be *packed arrays*, such as `float2`

, `float3`

, and so on. For this reason, the radius and intensity of points will be packed, respectively, in the `x`

and `y`

fields of `_Properties`

.

The variables `_Points`

and `_Properties`

are actual arrays, so their elements can be accessed simply using the square bracket notation.

Shader "Example/Heatmap" { Properties { _HeatTex ("Texture", 2D) = "white" {} } SubShader { Tags {"Queue"="Transparent"} Blend SrcAlpha OneMinusSrcAlpha // Alpha blend Pass { CGPROGRAM #pragma vertex vert #pragma fragment frag struct vertInput { float4 pos : POSITION; }; struct vertOutput { float4 pos : POSITION; fixed3 worldPos : TEXCOORD1; }; vertOutput vert(vertInput input) { vertOutput o; o.pos = mul(UNITY_MATRIX_MVP, input.pos); o.worldPos = mul(_Object2World, input.pos).xyz; return o; } uniform int _Points_Length = 0; uniform float3 _Points [20]; // (x, y, z) = position uniform float2 _Properties [20]; // x = radius, y = intensity sampler2D _HeatTex; half4 frag(vertOutput output) : COLOR { // Loops over all the points half h = 0; for (int i = 0; i < _Points_Length; i ++) { // Calculates the contribution of each point half di = distance(output.worldPos, _Points[i].xyz); half ri = _Properties[i].x; half hi = 1 - saturate(di / ri); h += hi * _Properties[i].y; } // Converts (0-1) according to the heat texture h = saturate(h); half4 color = tex2D(_HeatTex, fixed2(h, 0.5)); return color; } ENDCG } } Fallback "Diffuse" }

For every pixel of the geometry, **lines 41-47** calculate the *heat contribution* given from each point. The final heat, `h`

, (ranging from 0 to 1) is then used to sample a texture which will determine the actual colour and opacity. **Lines 6-7** are necessary if we want the geometry to support alpha transparency.

The only thing which is missing, is the initialisation of the arrays. On compilation, something magical happens: every cell of the array `_Points[i]`

will be accessible from C# as `_Pointsi`

. Armed with this knowledge, we can pass an array very easily to the shader:

using UnityEngine; using System.Collections; public class Heatmap : MonoBehaviour { public Vector3[] positions; public float[] radiuses; public float[] intensities; public Material material; void Start () { material.SetInt("_Points_Length", positions.Length); for (int i = 0; i < positions.Length; i ++) { material.SetVector("_Points" + i.ToString(), positions[i]); Vector2 properties = new Vector2(radiuses[i], intensities[i]); material.SetVector("_Properties" + i.ToString(), properties); } } }

All the public fields can be initialised directly from the inspector. The overall look of the heatmap can change dramatically just by playing a little bit with its heat texture. Using toom ramps generally yields visually pleasant results.

![map_02](../../assets/7f365bfbaf15d671.png)

To overcome the huge limitation Unity3D has when it comes to pass arrays to shaders, we can create a more general class.

using UnityEngine; using System.Collections; public class SetVector3Array : MonoBehaviour { public Material material; public string name; // The name of the array public Vector3[] array; // The values public void UpdatePoints() { // Requires an array called "[name]" // and another one called "[name]_Length" material.SetInt(name + "_Length", array.Length); for (int i = 0; i < array.Length; i++) material.SetVector(name + i.ToString(), array[i]); } }

In order to work, it needs a material with a shader which contains an array. Its name must be specified in the string `name`

. The shader must also have a variable with the same name of the array, followed by `_Length`

.

Using arrays in Shader is possible with any recent version of Unity, due to a poorly documented feature. Official APIs are planned from [Unity 5.4.0 Beta 1](https://unity3d.com/unity/beta/unity5.4.0b1). The technique introduced in this tutorial is compatible with earlier versions.

Arrays can be used for a variety of reasons. They can be used to initiate hundreds of properties via scripting, without the need to expose each one of them individually.

You can download the complete [Unity package](https://drive.google.com/file/d/0B4nCcaMlgxV2Y1o0OG5NcTVfMTQ/view?usp=sharing) for this project here.

#### Other resources

- Part 1.
[A Gentle Introduction to Shaders](https://www.alanzucconi.com/2015/06/10/a-gentle-introduction-to-shaders-in-unity3d/) - Part 2.
[Surface Shaders](https://www.alanzucconi.com/2015/06/17/surface-shaders-in-unity3d/) - Part 3.
[Physically Based Rendering and Lighting Models](https://www.alanzucconi.com/2015/06/24/physically-based-rendering-and-lighting-models-in-unity3d/) - Part 4.
[Vertex and Fragment Shaders](https://www.alanzucconi.com/2015/07/01/vertex-and-fragment-shaders-in-unity3d/) - Part 5.
[Screen Shaders and Image Effects](https://www.alanzucconi.com/2015/07/08/screen-shaders-and-postprocessing-effects-in-unity3d/)

## Leave a Reply Cancel reply