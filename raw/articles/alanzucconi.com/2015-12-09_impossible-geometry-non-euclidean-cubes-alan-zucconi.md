---
title: 'Impossible Geometry: Non-Euclidean Cubes - Alan Zucconi'
url: https://www.alanzucconi.com/2015/12/09/3873/
author: Alan Zucconi
published: '2015-12-09'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This tutorial will teach you how to create **non euclidean cubes** in Unity, giving the illusion that each face is a door onto another dimension. This post is part of a series of tutorials on **impossible geometries**.

![antichamber](../../assets/53af99d188c00d8d.gif)

This effect can be seen in many game, most notoriously [Antichamber](http://store.steampowered.com/app/219890/) which uses it extensively.

- Step 1.
[Stencil Theory](https://www.alanzucconi.com#step1) - Step 2.
[The stencil mask](https://www.alanzucconi.com#step2) - Step 3.
[The stencil geometry](https://www.alanzucconi.com#step3) - Step 4.
[Putting all together](https://www.alanzucconi.com#step4) [Conclusion](https://www.alanzucconi.com#conclusion)

You can download the [Unity package](https://drive.google.com/file/d/0B4nCcaMlgxV2WURnZkRLd0ZBXzg/view?usp=sharing) here.

For this example, all the geometries will be contained within the cube, at the same time. This particular effect is achieved using [stencil buffer](http://docs.unity3d.com/Manual/SL-Stencil.html). The GPU offers a special buffer which can be used to mask and discard pixels. The idea behind non-euclidean cubes is strikingly simple and it requires two steps:

**Stencil mask:**each face of the cube writes a specific value to the stencil buffer (yellow and green, in this example).![s1](../../assets/149254a57c0cbe0d.png)

**Stencil geometry:**the geometry that has to be shown in the yellow face only draws pixels where the stencil buffer is yellow.

All the objects exists at the same time, but their pixels are only drawn in the respective faces.

The first step is to create a material that initialises the stencil buffer with a specific value. To do this, we use a simple **vertex and fragment shader** (learn how to use them: [Vertex and Fragment Shader](https://www.alanzucconi.com/2015/07/01/vertex-and-fragment-shaders-in-unity3d/)). Even if in front of the geometry, is essential that this mask is drawn before the content of the cube. To do this, we change the `Queue`

value to `Geometry-100`

.

Shader "Stencils/StencilMask" { Properties { _StencilMask("Stencil Mask", Int) = 0 } SubShader { Tags { "RenderType" = "Opaque" "Queue" = "Geometry-100" } ColorMask 0 ZWrite off Stencil { Ref[_StencilMask] Comp always Pass replace } Pass { CGPROGRAM #pragma vertex vert #pragma fragment frag struct appdata { float4 vertex : POSITION; }; struct v2f { float4 pos : SV_POSITION; }; v2f vert(appdata v) { v2f o; o.pos = mul(UNITY_MATRIX_MVP, v.vertex); return o; } half4 frag(v2f i) : COLOR { return half4(1,1,0,1); } ENDCG } } }

**Lines 10-16** write into the stencil buffer. The line `Ref[_StencilMask]`

indicates that the value we want to write is provided in the property `_StencilMask`

. `Comp always`

indicates that the value has to be written regardless of what was on the stencil buffer already.

### ⭐ Recommended Unity Assets

What we need now is a material which draws only if the stencil buffer has been initialised accordingly to a specific value. This is done using the `Comp equal`

condition.

Shader "Stencils/StencilGeometry" { Properties { _StencilMask("Stencil Mask", Int) = 0 _Color ("Color", Color) = (1,1,1,1) _MainTex ("Albedo (RGB)", 2D) = "white" {} _Glossiness ("Smoothness", Range(0,1)) = 0.5 _Metallic ("Metallic", Range(0,1)) = 0.0 } SubShader { Tags { "RenderType"="Opaque" } LOD 200 Stencil { Ref[_StencilMask] Comp equal Pass keep Fail keep } CGPROGRAM // Physically based Standard lighting model, and enable shadows on all light types #pragma surface surf Standard fullforwardshadows // Use shader model 3.0 target, to get nicer looking lighting #pragma target 3.0 sampler2D _MainTex; struct Input { float2 uv_MainTex; }; half _Glossiness; half _Metallic; fixed4 _Color; void surf (Input IN, inout SurfaceOutputStandard o) { // Albedo comes from a texture tinted by color fixed4 c = tex2D (_MainTex, IN.uv_MainTex) * _Color; o.Albedo = c.rgb; // Metallic and smoothness come from slider variables o.Metallic = _Metallic; o.Smoothness = _Glossiness; o.Alpha = c.a; } ENDCG } FallBack "Diffuse" }

The `Stencil`

block in **lines 13-18** can be easily added to many existing shaders, allowing to use virtually any material you want.

To recap:

- A standard cube structure;
- Each face of the cube is a quad has a different material, which uses the
`StencilMask`

shader with a unique value for`_StencilMask`

; - All the geometry pieces are inside the cube;
- Each geometry piece has it’s own material, derived from
`StencilGeometry`

and initialised to match the`_StencilMask`

property of its respective face.

You can download the full [Unity package](https://drive.google.com/file/d/0B4nCcaMlgxV2WURnZkRLd0ZBXzg/view?usp=sharing) here.

Non-euclidean cubes are always intriguing and can add an interesting twist to your game.

Despite the name, these cubes are actually euclidean. This technique works nicely for decorative elements, but it fails to provide an efficient solution to the portal effect seen in (guess!) [Portal](http://store.steampowered.com/app/620/) or [Parallax](http://store.steampowered.com/app/325060/). Future tutorials will cover other impossible geometries.

**Part 1:**Non-Euclidean Cubes**Part 2:**The Portal Effect**Part 3:**The Physics of Monument Valley

This tutorial is inspired by Noisecrime’s post called “[Stencils for portal rendering](http://forum.unity3d.com/threads/unity-4-2-stencils-for-portal-rendering.191890/)“.

## Leave a Reply Cancel reply