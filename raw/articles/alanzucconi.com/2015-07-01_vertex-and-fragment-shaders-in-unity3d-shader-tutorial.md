---
title: Vertex and fragment shaders in Unity3D - Shader tutorial
url: https://www.alanzucconi.com/2015/07/01/vertex-and-fragment-shaders-in-unity3d/
author: Alan Zucconi
published: '2015-07-01'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

[Part 1](https://www.alanzucconi.com/2015/06/10/a-gentle-introduction-to-shaders-in-unity3d/), [Part 2](https://www.alanzucconi.com/2015/06/17/surface-shaders-in-unity3d/), [Part 3](https://www.alanzucconi.com/2015/06/24/physically-based-rendering-and-lighting-models-in-unity3d/), **Part 4**, [Part 5](https://www.alanzucconi.com/2015/07/08/screen-shaders-and-postprocessing-effects-in-unity3d/), [[download the Unity3D package](https://drive.google.com/file/d/0B4nCcaMlgxV2eGhTWHNlT3pmcW8/view?usp=sharing)]

The previous three posts of this tutorial have introduced surface shaders and how they can be used to specify physical properties (such as albedo, gloss and specular reflections) of the materials we want to model. The other type of shader available in Unity3D is called [vertex and fragment shader](http://docs.unity3d.com/Manual/SL-VertexFragmentShaderExamples.html). As the name suggests, the computation is done in two steps. Firstly, the geometry is passed through a function called (typically called `vert`

) which can alter the position and data of each vertex. Then, the result goes through a `frag`

function which finally outputs a colour.

![Vertex and Fragment shader](../../assets/7ca8786e765b678b.png)

The workflow, *loosely* described in the diagram above, sounds very similar to a surface shader. The main difference is that there is no semantic for physical properties here. Concepts such as albedo, gloss and specular are simply not present at this level. For this reason, vertex and fragment shaders are often used for non-realistic materials, 2D graphics or post-processing effects. It is still possible, however, to re-implement a custom lighting model within a vertex and fragment shader. In actuality, every surface shader is actually compiled into a vertex and fragment one.

### A toy example

![shader_01](../../assets/535281dc9fc297d0.png)

If you remember the tutorial about surface shaders, returning a red colour resulted in a diffuse red material.Since vertex and fragment shaders don’t have any notion of lighting, returning red here means that the entire model will be #ff0000 red, with no shades or details; just a red silhouette.

Shader "Custom/SolidColor" { SubShader { Pass { CGPROGRAM #pragma vertex vert #pragma fragment frag struct vertInput { float4 pos : POSITION; }; struct vertOutput { float4 pos : SV_POSITION; }; vertOutput vert(vertInput input) { vertOutput o; o.pos = mul(UNITY_MATRIX_MVP, input.pos); return o; } half4 frag(vertOutput output) : COLOR { return half4(1.0, 0.0, 0.0, 1.0); } ENDCG } } }

![soldier red](../../assets/178bcf0fbebac5e7.png)

**Line 6-7** specifies which functions will be used for the vertex and fragment computations.

**Line 19** is surely the most mysterious. What `vert`

receives is the position of a vertex in world coordinates, which has to be converted into screen coordinates. Without entering into details, this is called *model-view projection*. In Unity3D this is possible using a matrix called `UNITY_MATRIX_MVP`

; when combined with the position a vertex, it returns its position on the screen. This information is packed into a struct called `vertOutput`

and it is sent to the fragment function.

### The binding semantics

**Lines 10, 14** and **23** use something you might have never encountered before: a new construct called *binding semantic*. When a colon is placed after a variable or a function, it is used to indicates that the variable itself will play a special role. For example, this is how `vertInput`

is actually initialised; `float4 pos : POSITION`

indicates that we want Unity3D to initialised `pos`

with the vertex positions.

The struct `vertOutput`

is decorated with `SV_POSITION`

, which indicates that we will initialise it with the screen position of a vertex. Despite requiring only two values (X and Y), `SV_POSITION`

typically contains also a Z and W components, used to store the depth (ZTest) and one value for the homogeneous space, respectively.

While Unity3D will use the decorators to initialise the `vertInput`

structure, it is our duty to fill `vertOutput`

with the appropriate values. All the fields in both structs, however, need to be decorated with a valid semantic. Cg allows a huge variety of these binding semantics. You might never encounter most of them, so take this list only as something you need to memorise in order to understand shaders. If you want, you can rather skip to the next section of this tutorial and come back here every time you encounter a new binding semantics.

#### Input semantics

This is a list of the most common binding semantics available in Cg for the fields of `vertInput`

, according to [its manual](http://developer.download.nvidia.com/cg/Cg_3.1/Cg-3.1_April2012_ReferenceManual.pdf).

`POSITION`

,`SV_POSITION`

: the position of a vertex in world coordinates (*object space*);`NORMAL`

: the normal of a vertex, relative to the world (not to the camera);`COLOR`

,`COLOR0`

,`DIFFUSE`

,`SV_TARGET`

: the colour information stored in the vertex;`COLOR1`

,`SPECULAR`

: the secondary colour information stored in the vertex;`FOGCOORD`

: the fog coordinate;`TEXCOORD0`

,`TEXCOORD1`

, …,`TEXCOORDi`

: the*i-th*UV data stored in the vertex.

#### Output semantics

And these are the binding semantics available for the fields of `vertOutput`

:

`POSITION`

,`SV_POSITION`

,`HPOS`

: the position of a vertex in camera coordinates (*clip space*, from zero to one for each dimension);`COLOR`

,`COLOR0`

,`COL0`

,`COL`

,`SV_TARGET`

: the front primary colour;`COLOR1`

,`COL1`

: the front secondary colour;`FOGC`

,`FOG`

: the fog coordinate;`TEXCOORD0`

,`TEXCOORD1`

, …,`TEXCOORDi`

,`TEXi`

: the*i-th*UV data stored in the vertex;`PSIZE`

,`PSIZ`

: the size of the point we are drawing;`WPOS`

: the position, in pixel, within the window (origin in the lower left corner).

#### A major headache

These binding semantics are one of the major sources of confusion for this type of shaders.

- All the semantics have multiple synonyms (for instance,
`COLOR`

and`COLOR0`

), which often cause panic to developers who approach shaders for the first time; - The same decorator can have different meanings if used in
`verInput`

or`vertOutput`

(for instance,`POSITION`

is the world coordinates or the screen coordinates, respectively); - The same meaning can have different decorators (for instance,
`FOGCOORD`

and`FOG`

for`vertInput`

and`vertOutput`

, respectively); - Most hardwares forces all fields of the structs to have a binding semantics; if you want to include something which doesn’t exactly fit the ones listed here, you’ll have to find another way or cheekily store it into a
`TEXCOORDi`

; - Some semantics can only run on certain hardwares and have been replaced (for instance,
`WPOS`

should be replaced by`ComputeScreenPos`

, as shown later).

### ⭐ Recommended Unity Assets

### Glass shading

Vertex and fragment shaders are often used for special materials. Water and glass, for instance, often come with distortion effects and lighting models which do not fit into the logic of a surface shader. As a toy example, let’s replicate, step, by step, the glass shader which comes with Unity5 standard assets. This effect is achieved in three steps:

- Grab what has already been drawn under the object into a texture
- Use a normal map to displace pixels in the texture
- Render the distorted pixels to the screen

With the current knowledge of shaders accumulated in this tutorial, none of the above-mentioned steps is possible. Yet.

#### Step 1&3: The grab pass

Some shaders are so complicated they need to be rendered multiple times in different *passes*. Unity3D supports a special type of pass called `GrabPass`

; it doesn’t render anything on screen, but it captures what’s already been drawn so far onto a texture. The following shader utilises a GrabPass to take a texture and re-output it onto the screen. Basically, it does a lot of things to do literally nothing.

Shader "Custom/GrabShader" { SubShader { Tags {"Queue"="Transparent" "IgnoreProjector"="True" "RenderType"="Opaque"} ZWrite On Lighting Off Cull Off Fog { Mode Off } Blend One Zero GrabPass { "_GrabTexture" } Pass { CGPROGRAM #pragma vertex vert #pragma fragment frag #include "UnityCG.cginc" sampler2D _GrabTexture; struct vin_vct { float4 vertex : POSITION; }; struct v2f_vct { float4 vertex : POSITION; float4 uvgrab : TEXCOORD1; }; // Vertex function v2f_vct vert (vin_vct v) { v2f_vct o; o.vertex = mul(UNITY_MATRIX_MVP, v.vertex); o.uvgrab = ComputeGrabScreenPos(o.vertex); return o; } // Fragment function half4 frag (v2f_vct i) : COLOR { fixed4 col = tex2Dproj( _GrabTexture, UNITY_PROJ_COORD(i.uvgrab)); return col; } ENDCG } } }

**Line 4** is where the `GrabPass`

is executed, specifying what’s on screen will be available in a texture called `_GrabTexture`

. It’s important to remember that when sampling from a texture, its UV data is required. Since this texture wasn’t originally designed to be used in a 3D model, it has no UV data associated with it. We need to take into account the current position of the object relative to the camera; the functions `ComputeGrabScreenPos`

and `UNITY_PROJ_COORD`

do exactly this. That’s the standard way to generate the UV data of a grab texture and to re-map it onto the screen.

#### Step 2: The distortion

There are several ways to distort an image. The way shaders usually do this is via another texture called *bump map*. Bump maps are usually used to indicate how light should reflect onto a surface; we can use them to do the same onto a glass. In this case, the bump map will indicate how much the grab texture will be deformed:

_BumpMap ("Noise text", 2D) = "bump" {}

In a traditional bump map, the RGB channels indicate the displacement on the X, Y and Z axes respectively. Since we’re interested in flat glasses, we’ll only take into account the first two components. The first problem arises since the values of pixels in an image range from 0 to 1, while we want to be able to have a displacement which goes from -1 to +1. unity3D provides a helper function to do this conversion:

half4 bump = tex2D(_BumpMap, i.texcoord); half2 distortion = UnpackNormal(bump).rg; // From 0..1 to -1..+1

![glass](../../assets/df530029f5b75156.png)

There are two ways to create a normal map. The first one, is to create three separate grayscale images to be used at R, G and B channels. This, however, is very laborious. Unity3D provides another approach, which is based on *height maps*. Instead of drawing a normal map directly, you can draw a grayscale image which represents the distance of an object from the camera: white pixels are debossed and black pixels are embossed.

![glass normal](../../assets/ea3914fde3b34b12.png)

The image above shows, left to right, the albedo map of the glass, its height map and how it appears once imported from Unity3D as a normal map.

#### Step 3: putting everything together

We now have all the necessary knowledge to assemble a glass shader:

Shader "Custom/GlassShader" { Properties { _MainTex ("Base (RGB) Trans (A)", 2D) = "white" {} _Colour ("Colour", Color) = (1,1,1,1) _BumpMap ("Noise text", 2D) = "bump" {} _Magnitude ("Magnitude", Range(0,1)) = 0.05 } SubShader { Tags {"Queue"="Transparent" "IgnoreProjector"="True" "RenderType"="Opaque"} ZWrite On Lighting Off Cull Off Fog { Mode Off } Blend One Zero GrabPass { "_GrabTexture" } Pass { CGPROGRAM #pragma vertex vert #pragma fragment frag #include "UnityCG.cginc" sampler2D _GrabTexture; sampler2D _MainTex; fixed4 _Colour; sampler2D _BumpMap; float _Magnitude; struct vin_vct { float4 vertex : POSITION; float4 color : COLOR; float2 texcoord : TEXCOORD0; }; struct v2f_vct { float4 vertex : POSITION; fixed4 color : COLOR; float2 texcoord : TEXCOORD0; float4 uvgrab : TEXCOORD1; }; // Vertex function v2f_vct vert (vin_vct v) { v2f_vct o; o.vertex = mul(UNITY_MATRIX_MVP, v.vertex); o.color = v.color; o.texcoord = v.texcoord; o.uvgrab = ComputeGrabScreenPos(o.vertex); return o; } // Fragment function half4 frag (v2f_vct i) : COLOR { half4 mainColour = tex2D(_MainTex, i.texcoord); half4 bump = tex2D(_BumpMap, i.texcoord); half2 distortion = UnpackNormal(bump).rg; i.uvgrab.xy += distortion * _Magnitude; fixed4 col = tex2Dproj( _GrabTexture, UNITY_PROJ_COORD(i.uvgrab)); return col * mainColour * _Colour; } ENDCG } } }

![glass](../../assets/914d71a4244f23f9.gif)

If your glass renders things upside down, is because of an inconsistency between how different versions of Unity3D interprets UV data. To solve this you can use the nasty `UNITY_UV_STARTS_AT_TOP`

:

#if UNITY_UV_STARTS_AT_TOP o.uvgrab.y *= -1; #endif

Despite being used for glass, this shading technique is perfect for other effects such as running water, the shock wave of an explosion of the air turbulence generated by fire.

### Animated materials: a water shader

What we can currently do is simulating a static distortion. Water, fire and other moving materials manifest more complex distortions which are constantly moving. To do this, we need a way to add the notion of *time* to a shader. Theoretically this is possible by adding a `_Time`

property which is updated every frame with the current game time. Luckily, Unity3D is already doing this. The [built-in variable](http://docs.unity3d.com/460/Documentation/Manual/SL-BuiltinValues.html) `_Time`

is a packed array of length four which contains `t/20`

, `t`

, `t*2`

and `t*3`

, respectively (where `t`

is the actual time). If we need something to oscillate over time, we can also use `_SinTime`

(`sin(t/8)`

, `sin(t/4)`

, `sin(t/2) `

and `sin(t)`

).

The next toy shader will show how to realise a toony 2D water shader. Similarly to the glass shader previously seen, it displaces a previously grabbed textures. The difference is that now it uses the current time into the calculation of its displacement. The new shader uses three textures:

`_GrabTexture`

: the previously grabbed texture;`_NoiseTex`

: a texture filled with random noise which is used to increase the random look of the water;`_CausticTex`

: a texture which a caustic reflection, used to give a more realistic feel to the water.

// Fragment function fixed4 frag (v2f_vct i) : COLOR { fixed4 noise = tex2D(_NoiseTex, i.texcoord); fixed4 mainColour = tex2D(_MainTex, i.texcoord); float time = _Time[1]; float2 waterDisplacement = sinusoid ( float2 (time, time) + (noise.xy) * _offset, float2(-_waterMagnitude, -_waterMagnitude), float2(+_waterMagnitude, +_waterMagnitude), float2(_waterPeriod, _waterPeriod) ); i.grabUV.xy += waterDisplacement; fixed4 col = tex2Dproj( _GrabTexture, UNITY_PROJ_COORD(i.grabUV)); fixed4 causticColour = tex2D(_CausticTex, i.texcoord.xy*0.25 + waterDisplacement*5); return col * mainColour * _waterColour * causticColour; } float2 sinusoid (float2 x, float2 m, float2 M, float2 p) { float2 e = M - m; float2 c = 3.1415 * 2.0 / p; return e / 2.0 * (1.0 + sin(x * c)) + m; }

![water](../../assets/f9ebca7da58b31f9.gif)

Rather than relying on `_SinTime`

, I’ve decided to use the function `sinusoid`

for a better control. What it does is to create a custom sinusoidal wave with the known *minimum*, *maximum* and *period*.

The complete toony 2D water shader is present in the package attached to this tutorial.

### World, screen and object positions

Let’s conclude this tutorial with some more shader theory. In the input structure of a surface shaders is possible to declare special fields such as `worldPos`

and `screenPos`

which contain the position of the current pixel in world and screen coordinates, respectively. Vertex and fragment shaders don’t support them. The following snippet shows how to replicate them:

#include "UnityCG.cginc" struct vertOutput { float4 pos : SV_POSITION; // Clip space fixed4 color : COLOR; // Vertex colour float2 texcoord : TEXCOORD0; // UV data float3 wPos : TEXCOORD1; // World position float4 sPos : TEXCOORD2; // Screen position float3 cPos : TEXCOORD3; // Object center in world }; vertOutput vert (appdata_full v) { vertOutput o; o.pos = mul(UNITY_MATRIX_MVP, v.vertex); o.color = v.color; o.texcoord = v.texcoord; o.wPos = mul(_Object2World, v.vertex).xyz; o.sPos = ComputeScreenPos(o.pos); o.cPos = mul(_Object2World, half4(0,0,0,1)); return o; } half4 frag (vertOutput i) : COLOR { i.sPos.xy /= i.sPos.w; // ...rest of the shader }

As already explained, `wPos`

, `sPos`

and `cPos`

don’t have a real binding semantics. However, one must be assigned to them. `TEXCOORD`

s are usually used, even if they don’t contain any direct information on UV data.

### Conclusion

This post gives a general overview of vertex and fragment shaders, and how they differ from the previously discussed surface shaders. They can still be used to create materials which are affected by lights, but this requires a very good understanding of lighting models. If you’re interested in this, Antti Verajankorva has posted [an interesting article](http://www.verajankorva.com/cms/?p=203) about it. This post also introduces normal maps, grab passes and how they can be used to implement displacement effects useful for glass, water or fire.

- Part 1:
[A gentle introduction to shaders in Unity3D](https://www.alanzucconi.com/2015/06/10/a-gentle-introduction-to-shaders-in-unity3d/) - Part 2:
[Surface shaders in Unity3D](https://www.alanzucconi.com/2015/06/17/surface-shaders-in-unity3d/) - Part 3:
[Physically Based Rendering and lighting models in Unity3D](https://www.alanzucconi.com/2015/06/24/physically-based-rendering-and-lighting-models-in-unity3d/) - Part 4:
**Vertex and fragment shader in Unity3D** - Part 5:
[Screen shaders and postprocessing effects in Unity3D](https://www.alanzucconi.com/2015/07/08/screen-shaders-and-postprocessing-effects-in-unity3d/)

## Leave a Reply Cancel reply