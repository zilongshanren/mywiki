---
title: Writing Shader Code in Universal RP (v2)
url: https://www.cyanilux.com/tutorials/urp-shader-code/
author: Cyanilux
published: '2021-05-17'
source_blog: Cyanilux Shader Tutorials
source_site: https://www.cyanilux.com/
category: graphics
fetched: '2026-04-19'
---

# Writing Shader Code in Universal RP (v2)

## Intro

Many shader code tutorials online are intended to be used in Unity’s **Built-in Render Pipeline** and might not work in the **Universal Render Pipeline** – They’ll either produce magenta errors or at least won’t be compatible with the [SRP Batcher](https://www.cyanilux.com/tutorials/intro-to-shaders/#srp-batcher), which batches the setup between draw calls for each shader/material, so rendering many objects with that shader will be more performant.

You can check if a shader is compatible with the SRP Batcher by looking in the **Inspector** when the shader is selected in the **Project** window. And you can check objects are being batched correctly via the [Frame Debugger](https://docs.unity3d.com/Manual/FrameDebugger.html) window. If the shader is **Unlit** and doesn’t use any properties (except textures) it may already be compatible.

If not, then ideally it should be re-written. Any shaders using the Surface Shader template (`#pragma surface`

function) also aren’t compatible with URP and will need rewriting into a vertex/fragment one. Using Shader Graph can be easier, but it doesn’t have access to everything and some people may prefer writing code instead.

If you’re unsure what a shader even is, see my [Intro to Shaders](https://www.cyanilux.com/tutorials/intro-to-shaders) post first, and consider using Shader Graph as it should be easier for beginners. I’ve got an [Intro to Shader Graph](https://www.cyanilux.com/tutorials/intro-to-shader-graph) post too.

If you are already familiar with writing shaders for the **Built-in Render Pipeline** you may want to skip to the final sections for summaries of differences, list of functions and templates you can use.

[old wordpress article](https://cyangamedev.wordpress.com/2020/06/05/urp-shader-code/)of the same name. All on a single page, more detailed, better formatting, and no annoying ads. There’s a few sections I might rewrite further but enjoy! 💙

### Sections :


[ShaderLab](https://www.cyanilux.com#shaderlab)[Properties](https://www.cyanilux.com#properties)[SubShader](https://www.cyanilux.com#subshader)[Pass](https://www.cyanilux.com#pass)[LightMode Tag](https://www.cyanilux.com#lightmode-tag)[Cull](https://www.cyanilux.com#cull)[Depth Test/Write](https://www.cyanilux.com#depth-test-write)(ZTest, ZWrite & Offset)[Blend & Transparency](https://www.cyanilux.com#blend)(Blend, BlendOp)

[Multi-Pass](https://www.cyanilux.com#multi-pass)

[HLSL](https://www.cyanilux.com#hlsl)[Summary of Built-in vs URP differences](https://www.cyanilux.com#summary)[Templates](https://www.cyanilux.com#templates)


# ShaderLab

Shader files in Unity are written using two languages. A unity-specific **ShaderLab** language is used define the shader properties, subshaders and passes, while actual shader code is written in **HLSL (High Level Shading Language)**.

The ShaderLab syntax hasn’t changed much compared to the built-in pipeline. Unity provides [some documentation](https://docs.unity3d.com/Manual/SL-Shader.html) but I’m going over some important parts of it here too. If you are already familiar with ShaderLab you’ll mainly want to read the [Render Pipeline](https://www.cyanilux.com#render-pipeline), [LightMode Tag](https://www.cyanilux.com#lightmode-tag), and [Multi Pass](https://www.cyanilux.com#multi-pass) sections.

All shaders start with the **Shader** block, which includes a path and name to determine how it appears in the dropdown when changing the shader on the Material in the Inspector window.

```
Shader "Custom/UnlitShaderExample" {
...
}
```


Other blocks will go inside here, including a Properties block and various Subshader blocks.

## Properties

The Properties block is for any values that need to be exposed to the Material Inspector, so that we can use the same shader for materials with different textures/colours for example.

```
Properties {
// [name] ("[name in inspector]", [type]) = [default value]
"Base Texture", 2D) = "white" {}
_BaseColor ("Base Colour", Color) = (0, 0.66, 0.73, 1)
// _ExampleDir ("Example Vector", Vector) = (0, 1, 0, 0)
// _ExampleFloat ("Example Float (Vector1)", Float) = 0.5
```


We can also change these properties from C# scripts (e.g. using `material.SetColor / SetFloat / SetVector / etc`

). If the properties will be different per material, we must include them in the Properties block as well as the UnityPerMaterial CBUFFER to support the SRP Batcher correctly, which will explained later.

If all shaders should share the same value, then we don’t have to expose them here. Instead we only define them later in the HLSL code. We can still set them from C# using `Shader.SetGlobalColor / SetGlobalFloat / SetGlobalVector / etc`

.

More information about setting properties from C# can be found in the [Intro to Shaders](https://www.cyanilux.com/tutorials/intro-to-shaders/#properties) post.

## SubShader

Our Shader block can include multiple **SubShaders**. Unity will use the first Subshader block that is supported on the GPU. The **RenderPipeline** tag, as I’ll explain more in the next section, should also prevent the SubShader from being chosen if the shader shouldn’t be used in that pipeline, allowing a shader to have multiple versions for each pipeline.

We can also define a **Fallback** if no SubShaders are supported. If a fallback isn’t used, then it’ll show the magenta error shader instead.

```
Shader "Custom/UnlitShaderExample" {
Properties { ... }
SubShader { ... }
FallBack "Path/Name"
}
```


Later we’ll define passes in each SubShader which can include HLSL code. Inside this we can specify a [Shader Compile Target](https://docs.unity3d.com/Manual/SL-ShaderCompileTargets.html). Higher targets support more GPU features but might not be supported on all platforms.

For versions prior to v10, URP used to use the following in all passes :

```
// Required to compile gles 2.0 with standard SRP library
// All shaders must be compiled with HLSLcc and currently only gles is not using HLSLcc by default
#pragma prefer_hlslcc gles
#pragma exclude_renderers d3d11_9x
#pragma target 2.0
```


You can see an example of this in the [URP/Lit shader (v8.3.1)](https://github.com/Unity-Technologies/Graphics/blob/v8.3.1/com.unity.render-pipelines.universal/Shaders/Lit.shader).

With v10+, deferred support has started to be added so it appears the [provided shaders](https://github.com/Unity-Technologies/Graphics/tree/master/com.unity.render-pipelines.universal/Shaders) use two SubShaders instead. The first uses this for each pass :

```
#pragma exclude_renderers gles gles3 glcore
#pragma target 4.5
```


Basically meaning “use this for all platforms except OpenGL ones”. The second SubShader uses :

```
#pragma only_renderers gles gles3 glcore d3d11
#pragma target 2.0
```


As far as I can tell both SubShaders are indentical, except for these targets and the second SubShader excludes the UniversalGBuffer pass, used for [deferred rendering](https://docs.unity3d.com/Manual/RenderTech-DeferredShading.html), likely because it can’t be supported on those platforms at this time (note that link is for the built-in pipeline’s deferred rendering, but the technique is the same). For this post/tutorial I’m not including this target stuff but it might be important if you’re supporting deferred and targetting OpenGL platforms to split it into two SubShaders like the [URP/Lit shader (v10.5.0)](https://github.com/Unity-Technologies/Graphics/blob/v10.5.0/com.unity.render-pipelines.universal/Shaders/Lit.shader).

I’m also not using the deferred pass since it hasn’t been properly released in URP yet. I’ll try to update the post later to include it properly, (but no promises!)

### Render Pipeline

The **RenderPipeline** tag should prevent the SubShader from being used unless it’s intended for the current render pipeline being used. The tag corresponds to the `Shader.globalRenderPipeline`

value which is set when using a Scriptable Render Pipeline.

The value can be set to **“UniversalPipeline”** (or the old “LightweightPipeline”) and **“HDRenderPipeline”**. While I haven’t tested, using a different value likely means the SubShader would always be ignored unless a Custom Render Pipeline is used and it sets the `Shader.globalRenderPipeline`

string.

Excluding the tag completely means any pipeline can use it. I’m unsure on the behaviour if the tag value is set to a blank string ("") but it may be the same. There isn’t a value for the Built-In RP so if you want to target it I’d recommend using the **last SubShader** without the RenderPipeline tag, acting similar to a Fallback. e.g.

```
Shader "Custom/UnlitShaderExample" {
Properties { ... }
SubShader {
Tags { "RenderPipeline"="UniversalPipeline" "Queue"="Geometry" }
...
}
SubShader {
Tags { "RenderPipeline"="HDRenderPipeline" "Queue"="Geometry" }
...
}
SubShader {
Tags { }
...
}
FallBack "Path/Name"
}
```


Of note : When I did tests previously with the RenderPipeline tag (in Unity 2019.3, URP 7.x), it appeared that if the shader only includes a single SubShader it didn’t matter what the tag is set to, it would always try to use it. Unsure if this has been changed.

Also if you see the tag “UniversalRenderPipeline” mentioned anywhere, this is incorrect so don’t use it! It only worked previously because of the issue mentioned above. It was actually even used in official documentation but was quickly fixed as soon as I mentioned it. <3

Unity 2018 versions also seemed to always use the SceneSelectionPass & Picking passes from the first pass regardless of the tag. Unity 2019+ fixed this though, unsure if it was backported but something to be aware of if doing any custom scene selection rendering.

### Queue

The **Queue** tag is important to determine when the object is rendered, though it can also be overriden on the **Material** (via the Inspector, **Render Queue**).

The tag has to be set to one of these predefined names, each of which correspond with a Render Queue value :

- “Background” (1000)
- “Geometry” (2000)
- “AlphaTest” (2450)
- “Transparent” (3000)
- “Overlay” (4000)

We can also append +N or -N to the name to change the queue value the shader uses. e.g. “Geometry+1” will be 2001, so rendered after other objects using 2000. “Transparent-1” would be 2999 so would be rendered before other transparent objects using 3000.

Values up to 2500 are considered **Opaque** so objects using the same queue value render front-to-back (objects nearer the camera render first). This is for optimised rendering so later fragments can be discarded if they fail the depth test (explained in more detail later).

2501 onwards is **Transparent** and renders back-to-front (objects further away are rendered first). Because transparent shaders tend not to use depth test/write, altering the queue will change how the shader sorts with other transparent objects.

You can also find other tags that can be used listed in the [Unity SubShaderTags documentation](https://docs.unity3d.com/Manual/SL-SubShaderTags.html).

## Pass

Pass blocks are defined in each SubShader. There can be multiple passes, where each should include a specific tag named **LightMode** which **determines when/how the pass is used** (explained further in the next section).

```
SubShader {
Tags { "RenderPipeline"="UniversalPipeline" "Queue"="Geometry" }
Pass {
Name "Forward"
Tags { "LightMode"="UniversalForward" }
...
}
Pass {
Name "ShadowCaster"
Tags { "LightMode"="ShadowCaster" }
...
}
Pass {
Name "DepthOnly"
Tags { "LightMode"="DepthOnly" }
...
}
//UsePass "Universal Render Pipeline/Lit/ShadowCaster"
}
```


You can also give them an optional **Name** which allows `UsePass`

to be used in a different shader. An example is shown with using the ShadowCaster pass from the URP Lit shader, however I’ve commented it out. This is because it actually isn’t recommended to use `UsePass`

. In order to keep SRP Batcher compatibility, **all passes in the shader must have the same UnityPerMaterial CBUFFER**, and `UsePass`

currently can break that as it uses the CBUFFER as defined in that previous shader. Instead, you should write each pass yourself or copy it manually. We’ll be going over some of these passes in a later section.

Depending on what the shader is for you might not even need additional passes. A shader used in a Blit render feature to apply a fullscreen image effect for example will only need a single pass where the LightMode tag could be left out completely.

### LightMode Tag

As mentioned, each pass includes a tag named **LightMode**, which describes to Unity how the pass is used. The Universal Render Pipeline uses the following modes :

- “UniversalForward” - Used to render objects in the
**Forward**rendering path. Renders geometry with lighting. - “ShadowCaster” - Used for casting shadows
- “DepthOnly” - Used by the
**Depth Prepass**to create the**Depth Texture**(_CameraDepthTexture) if MSAA is enabled or the platform doesn’t support copying the depth buffer - “DepthNormals” - Used by the
**Depth Normals Prepass**to create the**Depth Texture**(_CameraDepthTexture) and**Normals Texture**(_CameraNormalsTexture) if a renderer feature requests it (via`ConfigureInput(ScriptableRenderPassInput.Normal);`

in the ScriptableRenderPass, see[SSAO feature](https://github.com/Unity-Technologies/Graphics/blob/master/Packages/com.unity.render-pipelines.universal/Runtime/RendererFeatures/ScreenSpaceAmbientOcclusion.cs)for example) - “Meta” - Used during Lightmap Baking
- “Universal2D” - Used for rendering when the 2D Renderer is enabled
- “SRPDefaultUnlit” - Default if no LightMode tag is included in a Pass. Can be used to draw extra passes (in both forward/deferred rendering), however this can break SRP Batcher compatibility. See
[Multi-Pass](https://www.cyanilux.com#multi-pass)section below

Future changes will also add these (v12+?) :

- “UniversalGBuffer” - Used to render objects in the
**Deferred**rendering path. Renders geometry into multiple buffers without lighting. Lighting is handled later in the path. - “UniversalForwardOnly” - Similar to “UniversalForward”, but can be used to render objects as forward even in the Deferred path which is useful if the shader features data that won’t fit in the GBuffer, such as Clear Coat normals.

I’m currently not including a section on the UniversalGBuffer pass since it hasn’t been properly released yet. I may update the post in the future (but no promises!)

Tags like “Always”, “ForwardAdd”, “PrepassBase”, “PrepassFinal”, “Vertex”, “VertexLMRGBM”, “VertexLM” are intended for the Built-In RP and are not supported in URP.

You can also use custom LightMode tag values, which you can trigger to be rendered via a Custom Renderer Feature or the RenderObjects feature that URP provides.

### Cull

Each pass can include **Cull** to control which sides of a triangle is rendered.

```
Pass {
//Cull Back // Default, back faces are culled
//Cull Front // Front faces are culled
Cull Off // No faces are culled. Both sides are rendered.
...
}
```


Which faces correspond to the “front” or “back” sides depends on the winding order of the vertices per triangle. In Blender, this is determined by the Normals.

### Depth Test/Write

Each pass can include the depth test (**ZTest**) and depth write (**ZWrite**) operations.

```
Pass {
ZTest LEqual // Default
// ZTest Less | Greater | GEqual | Equal | NotEqual | Always
ZWrite On // Default
// ZWrite Off
...
}
```


Depth test determines how fragments are rendered depending on how their depth value compares to the value in the depth buffer. For example, **LEqual** (which is also the default if not included), will only render fragments if their depth is **less or equal** to the buffer value.

Depth write determines whether the fragment’s depth value replaces the value in the buffer when the test passes. With `ZWrite Off`

, the value remains unchanged. This is mainly useful for Transparent objects in order to achieve the correct blending, however this is also why sorting them is difficult and they sometimes can render in the incorrect order.

Also related, the **Offset** operation allows you to offset the depth value with two parameters (factor, units). I’m actually not very familiar with it myself, so… copying the explanation from the docs (sorry) :

Factor scales the maximum Z slope, with respect to X or Y of the polygon, and units scale the minimum resolvable depth buffer value. This allows you to force one polygon to be drawn on top of another although they are actually in the same position. For example `Offset 0, -1`

pulls the polygon closer to the camera, ignoring the polygon’s slope, whereas `Offset -1, -1`

will pull the polygon even closer when looking at a grazing angle.

```
Pass {
Offset 0, -1
}
```


### Blend & Transparency

For a shader to support transparency, a **Blend** mode can be defined. This determines how the fragment result is combined with existing values in the camera’s colour target/buffer. The syntax is :

```
Blend SrcFactor DstFactor
// or
Blend SrcFactor DstFactor, SrcFactorA DstFactorA
// to support different factors for Alpha channel
```


Where the shader colour result is multiplied with the `SrcFactor`

, and the existing colour target/buffer pixel is multiplied with the `DstFactor`

. Each of these values is then combined based on a separate **BlendOp** operation, (which defaults to **Add**), to produce the final colour result which replaces the value in the buffer.

The factors can be one of the following :

`One`

`Zero`

`SrcColor`

`SrcAlpha`

`DstColor`

`DstAlpha`

`OneMinusSrcColor`

`OneMinusSrcAlpha`

`OneMinusDstColor`

`OneMinusDstAlpha`


Also see the [Blend docs page](https://docs.unity3d.com/Manual/SL-Blend.html) for a list of the supported `BlendOp`

operations if you want to select a different one than `Add`

.

The most common blends include :

`Blend SrcAlpha OneMinusSrcAlpha`

- Traditional transparency`Blend One OneMinusSrcAlpha`

- Premultiplied transparency`Blend One One`

- Additive`Blend OneMinusDstColor One`

- Soft Additive`Blend DstColor Zero`

- Multiplicative`Blend DstColor SrcColor`

- 2x Multiplicative

A few examples :

```
Pass {
Blend SrcAlpha OneMinusSrcAlpha // (Traditional transparency)
// (is default anyway)
/*
This means,
newBufferColor = (fragColor * fragColor.a) + (bufferColor * (1 - fragColor.a))
Which in this case is also equal to what a lerp does :
newBufferColor = lerp(bufferColor, fragColor, fragColor.a)
Of note :
- If fragColor.a is 0, the bufferColor is not changed.
- If fragColor.a is 1, fragColor is used fully.
*/
}
Pass {
Blend One One // (Additive)
// (is default anyway)
/*
This means,
newBufferColor = (fragColor * 1) + (bufferColor * 1)
Of note :
- Alpha does not affect this blending (though the final alpha value
may change, likely affecting DstAlpha if used in the future. Hence why
you may want different factors to be used for the alpha channel).
- In order to not change the bufferColor, fragColor must be black (0,0,0,0)
*/
}
```


## Multi-Pass

If you have additional passes without using a LightMode tag (or using SRPDefaultUnlit), it will be used alongside rendering the main UniversalForward one. This is commonly referred to as “Multi-pass”. However while this may work in URP, it is **not recommended** as again it is something that breaks the SRP Batcher compatibility, which means rendering objects with the shader will be more expensive.

Instead, the recommended way to achieve Multi-pass is via one of the following :

- A separate shader, applied as a
**second material**to the Mesh Renderer. If using submeshes, more materials can be added and it loops back around. **RenderObjects**feature on the Forward Renderer can be used to re-render all Opaque or Transparent objects on a**specific unity Layer**with an**Override Material**(which uses a separate shader). This is only really useful if you want to render a lot of objects with this second pass - don’t waste an entire Layer on a single object. Using the Override Material also**will not keep properties/textures**from the previous shader.**RenderObjects**feature again, but instead of an Override Material you can use a**Pass with a custom LightMode tag**in your shader and use the**Shader Tag ID**setting on the feature to render it. This method will keep properties/textures since it’s the same shader still, however it is only suitable for code-written shaders as Shader Graph doesn’t provide a way to inject custom passes.

# HLSL

Shader code is written using the High Level Shading Language (HLSL) in Unity.

## HLSLPROGRAM & HLSLINCLUDE

Inside each ShaderLab Pass, we define blocks for HLSL code using HLSLPROGRAM and ENDHLSL tags. Each of these blocks must include a Vertex and Fragment shader. We use the `#pragma vertex/fragment`

to set which function is going to be used.

For built-in pipeline shaders “vert” and “frag” are the most common names, but they can be anything. For URP, it tends to use functions like “UnlitPassVertex” and “UnlitPassFragment” which is a bit more descriptive of what the shader pass is doing.

Inside the SubShader we can also use HLSLINCLUDE to include the code **in every Pass inside that SubShader**. This is very useful for writing shaders in URP as every pass needs to use the same `UnityPerMaterial CBUFFER`

to have compatibility with the SRP Batcher and this helps us reuse the same code for every pass instead of needing to define it separately. We could alternatively use a separate include file instead too.

```
SubShader {
Tags { "RenderPipeline"="UniversalPipeline" "Queue"="Geometry" }
HLSLINCLUDE
...
ENDHLSL
Pass {
Name "Forward"
// LightMode tag. Using default here as the shader is Unlit
// Cull, ZWrite, ZTest, Blend, etc
HLSLPROGRAM
#pragma vertex UnlitPassVertex
#pragma fragment UnlitPassFragment
ENDHLSL
}
}
```


We’ll discuss the contents of these code block later. For now, we need to go over some of the basics of HLSL which is important to know to be able to understand the later sections.

## Variables

In HLSL, we have a few different variable types, the most common consisting of Scalars, Vectors and Matrices. There’s also special objects for Textures/Samplers. Arrays and Buffers also exist for passing more data into the shader.

### Scalar

The scalar types include :

`bool`

– true or false.`float`

– 32 bit floating point number. Generally used for world space positions, texture coordinates, or scalar computations involving complex functions such as trigonometry or power/exponentiation.`half`

– 16 bit floating point number. Generally used for short vectors, directions, object space positions, colours.`double`

– 64 bit floating point number. Cannot be used as inputs/outputs, see note here.`real`

– Used in URP/HDRP when a function can support either half or float. It defaults to half (assuming they are supported on the platform), unless the shader specifies “#define PREFER_HALF 0″, then it will use float precision. Many of the common math functions in the ShaderLibrary functions use this type.`int`

– 32 bit signed integer`uint`

– 32 bit unsigned integer (except GLES2, where this isn’t supported, and is defined as an int instead).

Also of note :

`fixed`

– 11(ish) bit fixed point number with -2 to 2 range. Generally used for LDR colours. Is something from the older CG syntax, though all platforms seem to just convert it to half now even in CGPROGRAM. HLSL does not support this but I felt it was important to mention as you’ll likely see the “fixed” type used in shaders written for the Built-In RP, use half instead!

### Vector

A vector is created by appending a component size (integer from 1 to 4) to one of these scalar data types. Some examples include :

`float4`

– (A float vector containing 4 floats)`half3`

- (A half vector, 3 components)`int2`

, etc- Technically
`float1`

would also be a one dimensional vector, but as far as I’m aware it’s equivalent to`float`

.

In order to get one of the components of a vector, we can use `.x`

, `.y`

, `.z`

, or `.w`

(or `.r`

, `.g`

, `.b`

, `.a`

instead, which makes more sense when working with colours). We can also use `.xy`

to obtain a vector2 and `.xyz`

to obtain a vector3 from a higher dimensional vector.

We can even take this further and return a vector with components rearranged, which is referred to as swizzling. Here is a few examples :

```
float3 vector = float3(1, 2, 3); // defined a 3 dimensional float vector
float3 a = vector.xyz; // or .rgb, a = (1, 2, 3)
float3 b = vector3.zyx; // or .bgr, b = (3, 2, 1)
float3 c = vector.xxx; // or .rrr, c = (1, 1, 1)
float2 d = vector.zy; // or .bg, d = (3, 2)
float4 e = vector.xxzz; // or .rrbb, e = (1, 1, 3, 3)
float f = vector.y; // or .g, f = 2
// Note that mixing xyzw/rgba is not allowed.
```


### Matrix

A matrix is created by appending two sizes (integers between 1 and 4) to the scalar, separated by an “x”. The first integer is the number of **rows**, while the second is the number of **columns** in the matrix. For example :

`float4x4`

– 4 rows, 4 columns`int4x3`

– 4 rows, 3 columns`half2x1`

– 2 rows, 1 column`float1x4`

– 1 row, 4 columns

Matrices are used for transforming between different spaces. If you aren’t very familiar with them, I’d recommend looking at [this tutorial by CatlikeCoding](https://catlikecoding.com/unity/tutorials/rendering/part-1/).

Unity has built-in transformation matrices which are used for transforming between common spaces, such as :

`UNITY_MATRIX_M`

(or`Unity_ObjectToWorld`

) -**Model**Matrix, Converts from Object space to**World space**`UNITY_MATRIX_V`

-**View**Matrix, Converts from World space to**View space**`UNITY_MATRIX_P`

-**Projection**Matrix, Converts from View space to**Clip space**`UNITY_MATRIX_VP`

-**View Projection**Matrix, Converts from World space to**Clip space**

Also inverse versions :

`UNITY_MATRIX_I_M`

(or`unity_WorldToObject`

) -**Inverse Model**Matrix, Converts from World space to**Object space**`UNITY_MATRIX_I_V`

-**Inverse View**Matrix, Converts from View space to**World space**`UNITY_MATRIX_I_P`

-**Inverse Projection**Matrix, Converts from Clip space to View space`UNITY_MATRIX_I_VP`

- Inverse View Projection Matrix, Converts from Clip space to World space

While you can use these matrices to convert between spaces via matrix multiplication (e.g. `mul(matrix, float4(position.xyz, 1))`

), there is also helper functions in the SRP Core ShaderLibrary [SpaceTransforms.hlsl](https://github.com/Unity-Technologies/Graphics/blob/master/Packages/com.unity.render-pipelines.core/ShaderLibrary/SpaceTransforms.hlsl).

Something to be aware of is when dealing with matrix multiplciation, the order is important. Usually the matrix will be in the first input and the vector in the second. A Vector in the second input is treated like a Matrix consisting of up to 4 rows (depending on the size of the vector), and a single column. A Vector in the first input is instead treated as a Matrix consisting of 1 row and up to 4 columns.

Each component in the matrix can also be accessed using either of the following : The zero-based row-column position:

- ._m00, ._m01, ._m02, ._m03
- ._m10, ._m11, ._m12, ._m13
- ._m20, ._m21, ._m22, ._m23
- ._m30, ._m31, ._m32, ._m33

The one-based row-column position:

- ._11, ._12, ._13, ._14
- ._21, ._22, ._23, ._24
- ._31, ._32, ._33, ._34
- ._41, ._42, ._43, ._44

The zero-based array access notation:

- [0][0], [0][1], [0][2], [0][3]
- [1][0], [1][1], [1][2], [1][3]
- [2][0], [2][1], [2][2], [2][3]
- [3][0], [3][1], [3][2], [3][3]

With the first two options, you can also use swizzling. e.g. `._m00_m11`

or `._11_22`

.

Of note, `._m03_m13_m23`

corresponds to the translation part of each matrix. So `UNITY_MATRIX_M._m03_m13_m23`

gives you the World space position of the origin of the GameObject, (assuming there is no static/dynamic batching involved for reasons explained in my [Intro to Shaders post](https://www.cyanilux.com/tutorials/intro-to-shaders/#material-instances)).

### Texture Objects

Textures store a colour for each **texel** - basically the same as a pixel, but they are known as texels (short for texture elements) when referring to textures and they also aren’t limited to just two dimensions.

The fragment shader stage runs on a per-fragment/pixel basis, where we can access the colour of a texel with a given coordinate. Textures can have different sizes (widths/heights/depth), but the coordinate used to sample the texture is normalised to a 0-1 range. These are known as Texture Coordinates or UVs. (where U corresponds to the horizontal axis of the texture, while V is the vertical. Sometimes you’ll see UVW where W is the third dimension / depth slice of the texture).

The most common texture is a 2D one, which can be defined in URP using the following macros in the global scope (outside any functions) :

```
TEXTURE2D(textureName);
SAMPLER(sampler_textureName);
```


For each texture object we also define a [SamplerState](https://docs.unity3d.com/Manual/SL-SamplerStates.html) which contains the wrap and filter modes from the texture’s import settings. Alternatively, we can define an inline sampler, e.g. `SAMPLER(sampler_linear_repeat)`

.

**Filter Modes**

**Point**(or Nearest-Point) : The colour is taken from the nearest texel. The result is blocky/pixellated, but that if you’re sampling pixel art you’ll likely want to use this.**Linear / Bilinear**: The colour is taken as a weighted average of close texels, based on the distance to them.**Trilinear**: The same as Linear/Bilinear, but it is also blends between mipmap levels.

**Wrap Modes**

**Repeat**: UV values outside of 0-1 will cause the texture to tile/repeat.**Clamp**: UV values outside of 0-1 are clamped, causing the edges of the texture to stretch out.**Mirror**: The texture tiles/repeats while also mirroring at each integer boundary.**Mirror Once**: The texture is mirrored once, then clamps UV values lower than -1 and higher than 2.

Later in the fragment shader we use another macro to sample the Texture2D with a uv coordinate that would also be passed through from the vertex shader :

```
float4 color = SAMPLE_TEXTURE2D(textureName, sampler_textureName, uv);
// Note, this can only be used in fragment as it calculates the mipmap level used.
// If you need to sample a texture in the vertex shader, use the LOD version
// to specify a mipmap (e.g. 0 for full resolution) :
= SAMPLE_TEXTURE2D_LOD(textureName, sampler_textureName, uv, 0);
```


Some other texture types include : Texture2DArray, Texture3D, TextureCube (known as a Cubemap outside of the shader) & TextureCubeArray, each using the following macros :

```
// Texture2DArray
SAMPLER(sampler_textureName);
// ...
= SAMPLE_TEXTURE2D_ARRAY(textureName, sampler_textureName, uv, index);
float4 color = SAMPLE_TEXTURE2D_ARRAY_LOD(textureName, sampler_textureName, uv, lod);
// Texture3D
SAMPLER(sampler_textureName);
// ...
= SAMPLE_TEXTURE3D(textureName, sampler_textureName, uvw);
float4 color = SAMPLE_TEXTURE3D_LOD(textureName, sampler_textureName, uvw, lod);
// uses 3D uv coord (commonly referred to as uvw)
// TextureCube
SAMPLER(sampler_textureName);
// ...
= SAMPLE_TEXTURECUBE(textureName, sampler_textureName, dir);
float4 color = SAMPLE_TEXTURECUBE_LOD(textureName, sampler_textureName, dir, lod);
// uses 3D uv coord (named dir here, as it is typically a direction)
// TextureCubeArray
SAMPLER(sampler_textureName);
// ...
= SAMPLE_TEXTURECUBE_ARRAY(textureName, sampler_textureName, dir, index);
float4 color = SAMPLE_TEXTURECUBE_ARRAY_LOD(textureName, sampler_textureName, dir, lod);
```


### Array

Arrays can also be defined, and looped through using a for loop. For example :

```
float4 _VectorArray[10]; // Vector array
float _FloatArray[10]; // Float array
void ArrayExample_float(out float Out){
float add = 0;
[unroll]
for (int i = 0; i < 10; i++){
add += _FloatArray[i];
}
Out = add;
}
```


If the size of the loop is fixed (i.e. not based on a variable) and the loop does not exit early, it can be more performant to “unroll” the loop, which is like copy-pasting the same code multiple times with the index changed.

It’s technically also possible to have other types of arrays, however Unity can only set Vector (float4) and Float arrays from a C# script.

I also recommend to always set them **globally**, using `Shader.SetGlobalVectorArray`

and/or `Shader.SetGlobalFloatArray`

rather than using the `material.SetVector/FloatArray`

versions. The reason for this is arrays cannot be properly included in the UnityPerMaterial CBUFFER (as it requires it to also be defined in the ShaderLab Properties, and arrays aren’t supported there). If the objects are batched using the SRP Batcher, multiple materials trying to use different arrays leads to glitchy behaviour where the values will change for all objects depending on what is being rendered on screen. By setting them globally, there can only ever be one array used which avoids this.

Note that these SetXArray methods are also limited to a maximum array size of 1023. If you need larger you might need to try alternative solutions instead, e.g. Compute Buffers (StructuredBuffer), assuming they are supported on the target platform.

### Buffer

An alternative to arrays, is using [Compute Buffers](https://docs.unity3d.com/ScriptReference/ComputeBuffer.html), which in HLSL is referred to as a **StructuredBuffer** (which is read-only. Alternatively there’s **RWStructuredBuffer** for reading & writing but is only supported in pixel/fragment and compute shaders).

You’d also need at least `#pragma target 4.5`

to use these. Not all platforms will support compute buffers too (and some might not support StructuredBuffer in vertex shaders). You can use `SystemInfo.supportsComputeShaders`

in C# at runtime to check if the platform supports them.

```
struct Example {
float3 A;
float B;
};
StructuredBuffer<Example> _BufferExample;
void GetBufferValue(float Index, out float3 Out) {
Out = _BufferExample[Index].A;
}
```


And using this C# for setting it, as a test :

|
|

I’m not super familiar with StructuredBuffers so sorry if this section is a bit lacking. I’m sure there are resources online that can explain it better!

## Functions

Declaring functions in HLSL is fairly similar to C#, however it is important to note that you can only call a function if it’s already been declared. You cannot call a function before declaring it so the order of functions and `#include`

files matters!

```
float3 example(float3 a, float3 b){
return a * b;
}
```


Here `float3`

is the return type, “example” is the function name and inside the brackets are the parameters passed into the function. In the case of no return type, `void`

is used. You can also specify output parameters using `out`

before the parameter type, or `inout`

if you want it to be an input that you can edit and pass back out. (There’s also `in`

but we don’t need to write it)

```
// Alternative that uses void, with float3 as an output parameter :
void example(float3 a, float3 b, out float3 Out){
Out = a * b;
}
/* This might be more useful for passing multiple outputs,
though they could also be packed into a struct */
```


You may also see `inline`

before the function return type. This is the default and only modifier a function can actually have, so it’s not important to specify it. It means that the compiler will generate a copy of the function for each call. This is done to reduce the overhead of calling the function.

You may also see functions like :

`#define EXAMPLE(x, y) ((x) * (y))`


This is referred to as a [macro](https://docs.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-appendix-pre-define-2). Macros are handled before compiling the shader and they get replaced with the definition, with any parameters substituted. For example :

```
float f = EXAMPLE(3, 5);
float3 a = float3(1,1,1);
float3 f2 = EXAMPLE(a, float3(0,1,0));
// just before compiling this becomes :
float f = ((3) * (5));
float a = float(1,1,1);
float3 f2 = ((a) * (float3(0,1,0)));
// An important note, is that the macro has () around x and y.
// This is because we could do :
float b = EXAMPLE(1+2, 3+4);
// which becomes :
float b = ((1+2) * (3+4)); // 3 * 7, so 21
// If those () wasn't included, it would instead be :
float b = (1+2*3+4)
// which equals 11 due to * taking precedence over +
```


Another macro example is :

```
#define TRANSFORM_TEX(tex,name) (tex.xy * name##_ST.xy + name##_ST.zw)
// Usage :
OUT.uv = TRANSFORM_TEX(IN.uv, _MainTex)
// which becomes :
OUT.uv = (IN.uv.xy * _MainTex_ST.xy + _MainTex_ST.zw);
```


The `##`

operator is a special case where macros can be useful. It allows us to concatenate the name and `_ST`

parts, resulting in `_MainTex_ST`

for this input. If the `##`

part was left out, it would just produce `name_ST`

, resulting in an error since that hasn’t be defined. (Of course, _MainTex_ST still also needs to be defined, but that’s the intended behaviour. Appending `_ST`

to the texture name is how Unity handles the tiling and offset values for a texture).

## UnityPerMaterial CBUFFER

Moving onto actually creating the shader code, we should first specify the **UnityPerMaterial CBUFFER** inside a **HLSLINCLUDE** block inside the SubShader. This ensures the same CBUFFER is used for all passes, which is important for the shader to be compatible with the SRP Batcher.

The CBUFFER must include all of the **exposed** properties (same as in the Shaderlab Properties block), except textures, though you still need to include the texture tiling & offset values (e.g. _ExampleTexture_ST, where S refers to scale and T refers to translate) and TexelSize (e.g. _ExampleTexture_TexelSize) if they are used.

It cannot include other variables that aren’t exposed.

```
HLSLINCLUDE
#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
CBUFFER_START(UnityPerMaterial)
float4 _ExampleTexture_ST; // Tiling & Offset, x = TilingX, y = TilingY, z = OffsetX, w = OffsetY
// x = 1/width, y = 1/height, z = width, w = height.
float _ExampleRange;
float _ExampleFloat;
float4 _ExampleVector;
// etc.
ENDHLSL
```


Note : While variables don’t *have to be exposed* to set them via the C# `material.SetColor / SetFloat / SetVector / etc`

, if multiple material instances have different values, this can produce glitchy behaviour as the SRP Batcher will still batch them together when on screen. If you have variables that aren’t exposed – **always** set them using `Shader.SetGlobalX`

functions, so that they remain constant for all material instances. If they need to be different per material, you should expose them via the Shaderlab Properties block and add them to the CBUFFER instead.

In the above code we are also including **Core.hlsl** from the **URP ShaderLibrary** using the #include as shown above. This is basically the URP-equivalent of the built-in pipeline UnityCG.cginc. Core.hlsl (and other ShaderLibrary files it automatically includes) contain a bunch of useful functions and macros, including the `CBUFFER_START`

and `CBUFFER_END`

macros themselves, which is replaced with “cbuffer name {” and “};” on platforms that support them, (I think all except GLES2, which makes sense as the SRP Batcher isn’t supported for that platform too).

## Structs

Before we define the vertex or fragment shader functions we need to define some **structs** which are used to pass data in and out of them. In built-in it is common to create two named “appdata” and “v2f” (short for “vertex to fragment”) while URP shaders tend to use “Attributes” and “Varyings” instead. These are just names and usually aren’t too important though, name them “VertexInput” and “FragmentInput” if you want.

The URP ShaderLibrary also uses some structs to help organise data needed for certain functions – such as InputData and SurfaceData which are used in lighting/shading calculations, I’ll be going through those in the Lighting section.

Since this is a fairly simple Unlit shader our Attributes and Varyings won’t be all that complicated :

### Attributes (VertexInput)

```
struct Attributes {
float4 positionOS : POSITION;
float2 uv : TEXCOORD0;
float4 color : COLOR;
};
// Don't forget the semi-colon at the end of the struct here,
// or you'll get "Unexpected Token" errors!
```


The **Attributes** struct will be the input to the vertex shader. It allows us to obtain the per-vertex data from the mesh, using the strings (most of which are all in caps) which are known as [semantics](https://docs.microsoft.com/en-gb/windows/win32/direct3dhlsl/dx-graphics-hlsl-semantics).

Can find the full list of semantics via that link, but here’s some semantics commonly used in the vertex input :

`POSITION`

: Vertex position`COLOR`

: Vertex colour`TEXCOORD0-7`

: UVs (aka texture coordinates). A mesh has 8 different UV channels accessed with a value from 0 to 7. Note that in C#, Mesh.uv corresponds to`TEXCOORD0`

. Mesh.uv1 does not exist, the next channel is uv2 which corresponds to`TEXCOORD1`

and so on up to Mesh.uv8 and`TEXCOORD7`

.`NORMAL`

: Vertex Normals (used for lighting calculations. This is unlit currently so isn’t needed)`TANGENT`

: Vertex Tangents (used to define “tangent space”, important for normal maps and parallax effects)

There’s also some more special semantics, like `SV_VertexID`

(requires `#pragma target 3.5`

), which allows you to obtain an identifer per-vertex (`uint`

type). Useful for use with a ComputeBuffer.

### Varyings (FragmentInput)

```
struct Varyings {
float4 positionCS : SV_POSITION;
float2 uv : TEXCOORD0;
float4 color : COLOR;
};
// Don't forget the semi-colon at the end of the struct here,
// or you'll get "Unexpected Token" errors!
```


The **Varyings** struct will be the input to the fragment shader, and the output of the vertex shader (assuming there’s no geometry shader in-between, which might need another struct, but we aren’t going through that in this post).

Unlike the previous struct, we use `SV_POSITION`

instead of `POSITION`

, which stores the **clip space position** from the vertex shader output. It’s important to convert the geometry to fragments/pixels on the screen at the correct location.

We also use the `COLOR`

and/or `TEXCOORDn`

(where n is a number) semantics but unlike before don’t have to correspond to the mesh vertex colors / uvs at all. Instead they are used to **interpolate data across the triangle**. `NORMAL/TANGENT`

is typically not used in the Varyings struct, and although I have seen them still work (along with completely custom semantics, e.g. Shader Graph uses `INTERPn`

), it might not supported on all platforms so I’d stick to `TEXCOORDn`

to be safe.

Depending on the platform & compile target, the number of interpolators available can vary :

- OpenGL ES 2.0 (Android), Direct3D 11 9.x level (Windows Phone), and Direct3D 9 Shader Model 2.0 (
`#pragma target 2.0`

) supports up to**8**interpolators (e.g.`TEXCOORD0-7`

) - Direct3D 9 Shader Model 3.0 (
`#pragma target 3.0`

) supports up to**10**(e.g.`TEXCOORD0-9`

) - OpenGL ES 3.0 (Android) and Metal (iOS) platforms support up to
**16**(e.g.`TEXCOORD0-15`

) - Direct3D 10 Shader Model 4.0 (
`#pragma target 4.0`

) supports up to**32**(e.g.`TEXCOORD0-31`

)

Another useful semantic, used with `Cull Off`

, is `VFACE`

(float type, available in Direct3D 9 Shader Model 3). A negative value means it is a back face, while a positive value indicates a front face. So could use a ternary like `(face > 0) ? _ColorFront : _ColorBack`

to apply colours to different sides. Direct3D 10 has a similar `SV_IsFrontFace`

but is a bool type rather than float.

See the [Shader Semantics docs page](https://docs.unity3d.com/Manual/SL-ShaderSemantics.html) and [Shader Compile Targets docs page](https://docs.unity3d.com/Manual/SL-ShaderCompileTargets.html) for more info.

### FragmentOutput

The fragment shader can also provide an output struct. However it’s usually not needed as it typically only uses a single output semantic, `SV_Target`

, which is used to write the fragment/pixel colour to the current render target. In this case we can just define it with the function like :

```
half4 UnlitPassFragment(Varyings input) : SV_Target {
// ... // calculate color
return color;
}
```


It is possible for a shader to output to more than one render target though, known as **Multi Render Target** (MRT). This is used by the Deferred Rendering path, e.g. [see UnityGBuffer.hlsl](https://github.com/Unity-Technologies/Graphics/blob/master/Packages/com.unity.render-pipelines.universal/ShaderLibrary/UnityGBuffer.hlsl) (which isn’t fully supported in URP yet).

If not using the deferred path, using MRT would require setup on the C# side, such as using `Graphics.SetRenderTarget`

with a `RenderBuffer[]`

array, or `CommandBuffer.SetRenderTarget`

with a `RenderTargetIdentifier[]`

array. MRT is not supported on all platforms however (e.g. GLES2)

In the shader we would define the MRT output like so :

```
struct FragOut {
half4 color : SV_Target0; // aka SV_Target
// another render target
FragOut UnlitPassFragment(Varyings input) {
// ... // calculate color and color2
output.color = color;
output.color2 = color2;
return output;
}
```


It is also possible to change the value used for depth, using the `SV_Depth`

semantic (or `SV_DepthGreaterEqual`

/ `SV_DepthLessEqual`

) as explained in my [Depth article](https://www.cyanilux.com/tutorials/depth/#depth-output).

## Vertex Shader

The main thing that our vertex shader needs to do is convert the object space position from the mesh into a clip space position. This is required in order to correctly render fragments/pixels in the intended screen position.

In built-in shaders you would do this with the `UnityObjectToClipPos`

function, but this has been renamed to `TransformObjectToHClip`

(which you can find in the SRP-core [SpaceTransforms.hlsl](https://github.com/Unity-Technologies/Graphics/blob/master/Packages/com.unity.render-pipelines.core/ShaderLibrary/SpaceTransforms.hlsl)). That said, there’s another way to handle the transform in URP as shown below which makes conversions to other spaces much easier too.

```
Varyings UnlitPassVertex(Attributes IN) {
Varyings OUT;
// alternatively, Varyings OUT = (Varyings)0;
// to initalise all struct inputs to 0.
// otherwise, every variable in the struct must be set
//OUT.positionCS = TransformObjectToHClip(IN.positionOS.xyz);
// Or :
= GetVertexPositionInputs(IN.positionOS.xyz);
OUT.positionCS = positionInputs.positionCS;
// which also contains .positionWS, .positionVS and .positionNDC (aka screen position)
// Pass through UV/TEXCOORD0 with texture tiling and offset (_BaseMap_ST) applied :
= TRANSFORM_TEX(IN.uv, _BaseMap);
// Pass through Vertex Colours :
= IN.color;
return OUT;
}
```


GetVertexPositionInputs computes the position in each of the commonly used spaces. It used to be a part of Core.hlsl, but was separated into it’s own file – [ShaderVariablesFunctions.hlsl](https://github.com/Unity-Technologies/Graphics/blob/master/Packages/com.unity.render-pipelines.universal/ShaderLibrary/ShaderVariablesFunctions.hlsl) in URP v9, but this file is automatically included when we include Core.hlsl anyway.

The function uses the object space position from the `Attributes`

as an input and returns a `VertexPositionInputs`

struct, which contains:

`positionWS`

: the position in**World**space`positionVS`

: the position in**View**space`positionCS`

: the position in**Clip**space`positionNDC`

: the position in**Normalised Device Coordinates**, aka Screen Position. (0,0) in bottom left, (w,w) in top right. Of note, we would pass the position to the fragment stage, then handle the perspective divide (`positionNDC.xy / positionNDC.w`

) so (1,1) is top right instead.

For our current unlit shader, we don’t need these other coordinate spaces, but this function is useful for shaders where we do. The unused ones also won’t be included in the compiled shader so there isn’t any unnecessary calculations.

The vertex shader is also responsible for passing data to the fragment, such as the texture coordinates (UV) and vertex colours. The values get interpolated across the triangle, as discussed in the [Intro to Shaders post](https://www.cyanilux.com/tutorials/intro-to-shaders/#shader). For the UVs, we could just do `OUT.uv = IN.uv;`

assuming both are set to `float2`

in the structs, but it’s common to include the Tiling and Offset values for the texture which Unity passes into a `float4`

with the texture name + `_ST`

(s referring to scale, and t for translate). In this case, `_BaseMap_ST`

which is also included in our UnityPerMaterial CBUFFER from earlier. In order to apply this to the UV, we could do :

`OUT.uv = IN.uv * _BaseMap_ST.xy + _BaseMap_ST.zw;`


But the `TRANSFORM_TEX`

macro can also be used instead, which is included in the Built-in RP as well as URP.

While we don’t need any normal/tangent data for our Unlit shader, there is also `GetVertexNormalInputs`

which can obtain the World space position of the normal, tangent and generated bitangent vectors.

```
VertexNormalInputs normalInputs = GetVertexNormalInputs(IN.normalOS, IN.tangentOS);
OUT.normalWS = normalInputs.normalWS;
OUT.tangentWS = normalInputs.tangentWS;
OUT.bitangentWS = normalInputs.bitangentWS;
```


This will be useful later when Lighting is needed. There’s also a version of the function which takes only the `normalOS`

, which leaves `tangentWS`

as `(1,0,0)`

and `bitangentWS`

as `(0,1,0)`

, or you could use `positionWS = TransformObjectToWorldNormal(IN.normalOS)`

instead, which is useful if the tangent/bitangent isn’t needed (e.g. No normal/bump or parallax mapping effects).

## Fragment Shader

The fragment shader is responsible for determining the colour of the pixel output (including alpha). For unlit shaders this can be a fairly simple solid colour or a colour obtained from sampling an input texture. For lit shaders, it’s a bit more complicated but URP provides some handy functions which I’ll be going through in the Lighting section.

For now since our shader is Unlit, all we need is :

```
half4 UnlitPassFragment(Varyings IN) : SV_Target {
// Sample BaseMap Texture :
= SAMPLE_TEXTURE2D(_BaseMap, sampler_BaseMap, IN.uv);
// Tint texture result with Color property and vertex colours :
return baseMap * _BaseColor * IN.color;
}
```


This produces a shader which outputs a half4 colour, based on the sampled `_BaseMap`

texture, which is also tinted by the `_BaseColor`

property and interpolated vertex colour. The `SAMPLE_TEXTURE2D`

macro is provided by the ShaderLibrary and returns the colour at the given uv coordinate, since the shader runs per-fragment/pixel.

As mentioned in the [FragmentOutput](https://www.cyanilux.com#fragment-output) section, `SV_Target`

is used to write the fragment/pixel colour to the current render target.

Something that we might also want to do, is discard pixels if their alpha value is below a certain threshold, so that the entire mesh isn’t visible – e.g. for grass/leaf textures on quads. This can be done in opaque shaders as well as transparent, and is usually referred to as **Alpha Clip/Cutout/Cutoff**. If you are familiar with **Shader Graph**, it’s handled with the **Alpha Clip Threshold**. In Shader Code this commonly involves a Float property named `_Cutoff`

(added to Shaderlab Properties as well as the UnityPerMaterial CBUFFER for SRP Batcher-compatibility). This can then be used in the fragment shader :

```
if (_BaseMap.a < _Cutoff){
discard;
}
// OR
clip(_BaseMap.a - _Cutoff);
// inside the fragment function, before returning
```


This is essentially the Unlit Shader Code complete.

## Keywords & Shader Variants

Before we go over Lighting, we need to talk about keywords and shader variants first. In shaders we can specify the `#pragma multi_compile`

and `#pragma shader_feature`

directives which are used to specify **keywords** for toggling certain parts of the shader code “on” or “off”. The shader actually gets compiled into multiple versions of the shader, known as **shader variants**. In Unity, we can then enable and disable keywords per material to select which variant gets used.

This is useful as it allows us to write a single shader, but create different versions of it with some features off to save on performance. This needs to be used carefully however, as different shader variants will not batch together. URP uses some of these keywords for toggling features like lighting (i.e. `#pragma multi_compile _ _MAIN_LIGHT_SHADOWS`

prior to v11) and fog (which uses the slightly special `#pragma multi_compile_fog`

, same as in the built-in RP).

### Multi Compile

`#pragma multi_compile _A _B _C (...etc)`


In this example we are producing three variants of the shader, where _A, _B, and _C are keywords.
We can then use `#if defined(KEYWORD)`

/ `#ifdef KEYWORD`

to determine which code is toggled by the keyword. For example :

```
#ifdef _A
// Compile this code if A is enabled
#endif
#ifndef _B
// Compile this code if B is disabled, aka only in A and C.
// Note the extra "n" in the #ifndef, for "if not defined"
#else
// Compile this code if B is enabled
#endif
#if defined(_A) || defined(_C)
// Compile this code in A or C. (aka the same as the above, assuming there's no other keywords)
// We have to use the long-form "#if defined()" if we want multiple conditions,
// where || is "or", && is "and", and ! for "not", similar to C#.
// Note however, that since the keywords are defined in one multi_compile statement
// it's actually impossible for both to be enabled, so && wouldn't make sense here.
#endif
/* There's also #elif, for an "else if" statement */
```


URP uses a bunch of multi_compiles, but here is some common ones. Not every shader needs to include all of these, but some of the functions in the ShaderLibrary rely on these keywords being included, otherwise they may skip calculations.

```
// Additional Lights (e.g. Point, Spotlights)
#pragma multi_compile _ _ADDITIONAL_LIGHTS_VERTEX _ADDITIONAL_LIGHTS
// Shadows
#pragma multi_compile _ _MAIN_LIGHT_SHADOWS
#pragma multi_compile _ _MAIN_LIGHT_SHADOWS_CASCADE
// Note, v11 changes this to :
// #pragma multi_compile _ _MAIN_LIGHT_SHADOWS _MAIN_LIGHT_SHADOWS_CASCADE _MAIN_LIGHT_SHADOWS_SCREEN
#pragma multi_compile _ _ADDITIONAL_LIGHT_SHADOWS
#pragma multi_compile _ _SHADOWS_SOFT
// Baked Lightmap
#pragma multi_compile _ LIGHTMAP_ON
#pragma multi_compile _ DIRLIGHTMAP_COMBINED
#pragma multi_compile _ LIGHTMAP_SHADOW_MIXING
#pragma multi_compile _ SHADOWS_SHADOWMASK
// Other
#pragma multi_compile_fog
#pragma multi_compile_instancing
#pragma multi_compile _ DOTS_INSTANCING_ON
#pragma multi_compile _ _SCREEN_SPACE_OCCLUSION
```


### Shader Feature

Shader Features are similar to Multi-Compile, but an additional variant is generated with all keywords disabled and any **unused variants will be not be included in the final build**. This can be useful to keep build times down, but it’s not good to enable/disable these keywords at runtime, since the shader it needs might not be included in the build! If you need to handle keywords at runtime, multi_compile should be used instead.

`#pragma shader_feature _A _B (...etc)`


The above code generates **three** variants, where _A and _B are keywords. While there’s only two keywords, an additional variant where both are disabled is also generated. When using Multi-Compile we can also do this, by specifying the first keyword as blank by using one or more underscores (`_`

). e.g.

`#pragma multi_compile _ _A _B`


### Shader Variants

With each added multi_compile and shader_feature, it produces more and more shader variants for each possible combination of enabled/disabled keywords. Take the following for example :

```
#pragma multi_compile _A _B _C
#pragma multi_compile _D _E
#pragma shader_feature _F
```


Here, the first line is producing 3 shader variants. But the second line, needs to produce 2 shader variants for those variants where _D or _E is already enabled. So, A & D, A & E, B & D, B & E, C & D and C & E. That’s now 6 variants.

Third line, is another 2 variants for each of those 6, so we now have a total of 12 shader variants. (While it’s only one keyword, it has the additional variant with it disabled since that line is a shader_feature. Some of those variants might also not be included in the build depending on what is used by materials)

Each added multi_compile with 2 keywords will double the amount of variants produced, so a shader that contains 10 of these will result in 1024 shader variants! It’ll need to compile each shader variant that needs to be included in the final build, so will increase build time as well as the size of the build.

If you want to see how many shader variants a shader produces, click the shader and in the inspector there’s a “Compile and Show Code” button, next to that is a small dropdown arrow where it lists the number of included variants. If you click the “skip unused shader_features” you can toggle to see the total number of variants instead.

To assist with reducing the number of variants produced, There is also “vertex” and “fragment” versions of these directives. For example :

```
#pragma multi_compile_vertex _ _A
#pragma multi_compile_fragment _ _B
#pragma shader_feature_vertex _C
#pragma shader_feature_fragment _D
```


In this example, the _A and _C keywords are only being used for the vertex program and _B and _D only for the fragment. Unity tells us that this produces 2 shader variants, although it’s more like one shader variant where both are disabled and two “half” variants when you look at the actual compiled code it seems.

The [documentation](https://docs.unity3d.com/Manual/SL-MultipleProgramVariants.html) has some more information on shader variants.

### Keyword Limits

An important note is there is also a maximum of **256 global keywords per project**, so it can be good to stick to the naming conventions of other shaders to ensure the same keywords are reused rather than defining new ones.

You’ll also notice for many Multi-Compile the first keyword is usually left as just “_”. By leaving the keyword blank, it leaves more space available for other keywords in the 256 maximum. For Shader Features, this is done automatically.

```
#pragma multi_compile _ _KEYWORD
#pragma shader_feature _KEYWORD
// If you need to know if that keyword is disabled
// We can then just do :
#ifndef _KEYWORD
// aka "#if !defined(_KEYWORD)"
// or "#ifdef _KEYWORD #else" also works too
// ... code ...
#endif
```


We can also avoid using up the maximum keyword count by using **local versions** of the `multi_compile`

and `shader_feature`

. These produce keywords that are local to that shader, but there’s also a maximum of **64 local keywords per shader**.

```
#pragma multi_compile_local _ _KEYWORD
#pragma shader_feature_local _KEYWORD
// There's also local_fragment/vertex ones too!
#pragma multi_compile_local_vertex _ _KEYWORD
#pragma multi_compile_local_fragment _ _KEYWORD
#pragma shader_feature_local_vertex _KEYWORD
#pragma shader_feature_local_fragment _KEYWORD
```


## Lighting Introduction

In the built-in pipeline, custom shaders that required lighting/shading was usually handled by **Surface Shaders**. These had the option to choose which lighting model to use, either the physically-based **Standard/StandardSpecular** or **Lambert** (diffuse) and **BlinnPhong** (specular) models. You could also write custom lighting models, which you would use if you wanted to produce a toon shaded result for example.

The Universal RP does not support surface shaders, however the ShaderLibrary does provide functions to help handle a lot of the lighting calculations for us. These are contained in Lighting.hlsl – (which isn’t included automatically with Core.hlsl, it must be included separately).

There are even functions inside that lighting file that can completely handle lighting for us, including **UniversalFragmentPBR** and **UniversalFragmentBlinnPhong**. These functions are really useful but there is still some setup involved, such as the InputData and SurfaceData structures that need to be passed into the functions.

We’ll need a bunch of exposed Properties (which should also be added to the CBUFFER) to be able to send data into the shader and alter it per-material. You can check the templates for the exact properties used - for example, [PBRLitTemplate](https://github.com/Cyanilux/URP_ShaderCodeTemplates/blob/main/URP_PBRLitTemplate.shader).

There’s also keywords that need to be defined before including the Lighting.hlsl file, to ensure the functions handle all the calculations we want, such as shadows and baked lighting. It’s common for a shader to also include some shader feature keywords (not included below but see template) to be able to toggle features, e.g. to avoid unnecessary texture samples and make the shader cheaper.

```
#pragma multi_compile _ _MAIN_LIGHT_SHADOWS
#pragma multi_compile _ _MAIN_LIGHT_SHADOWS_CASCADE
// Note, v11 changes this to :
// #pragma multi_compile _ _MAIN_LIGHT_SHADOWS _MAIN_LIGHT_SHADOWS_CASCADE _MAIN_LIGHT_SHADOWS_SCREEN
#pragma multi_compile _ _ADDITIONAL_LIGHTS_VERTEX _ADDITIONAL_LIGHTS
#pragma multi_compile_fragment _ _ADDITIONAL_LIGHT_SHADOWS
#pragma multi_compile_fragment _ _SHADOWS_SOFT
#pragma multi_compile _ LIGHTMAP_ON
#pragma multi_compile _ DIRLIGHTMAP_COMBINED
#pragma multi_compile _ LIGHTMAP_SHADOW_MIXING
#pragma multi_compile _ SHADOWS_SHADOWMASK
#pragma multi_compile _ _SCREEN_SPACE_OCCLUSION
#pragma multi_compile_fog
#pragma multi_compile_instancing
// Include Lighting.hlsl
#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Lighting.hlsl"
```


### Surface Data & Input Data

Both of these `UniversalFragmentPBR`

/ `UniversalFragmentBlinnPhong`

functions use two structures to pass data through : `SurfaceData`

and `InputData`

.

The **SurfaceData** struct is responsible for sampling textures and providing the same inputs as you’d find on the URP/Lit shader. Specifically it contains the following :

```
struct SurfaceData {
half3 albedo;
half3 specular;
half metallic;
half smoothness;
half3 normalTS;
half3 emission;
half occlusion;
half alpha;
// And added in v10 :
half clearCoatMask;
half clearCoatSmoothness;
};
```


Note that you don’t need to include this code, as this struct is part of the ShaderLibrary and we can instead include the file it is contained in. Prior to v10, the struct existed in [SurfaceInput.hlsl](https://github.com/Unity-Technologies/Graphics/blob/v8.3.1/com.unity.render-pipelines.universal/ShaderLibrary/SurfaceInput.hlsl) but the functions in Lighting.hlsl did not actually make use of it.

While you could still use the struct, you would instead need to do :

```
half4 color = UniversalFragmentPBR(inputData, surfaceData.albedo, surfaceData.metallic, surfaceData.specular,
surfaceData.smoothness, surfaceData.occlusion, surfaceData.emission, surfaceData.alpha);
```


In v10+ the struct moved to it’s own file, [SurfaceData.hlsl](https://github.com/Unity-Technologies/Graphics/blob/master/Packages/com.unity.render-pipelines.universal/ShaderLibrary/SurfaceData.hlsl), and the `UniversalFragmentPBR`

function was updated so we can simply pass both structs through instead (for the `UniversalFragmentBlinnPhong`

function a SurfaceData version is being added in v12 but current versions will need to split it. Examples shown later).

`half4 color = UniversalFragmentPBR(inputData, surfaceData);`


We can still include **SurfaceInput.hlsl** instead though, as SurfaceData.hlsl will automatically be included by that file too, and it also contains the `_BaseMap`

, `_BumpMap`

and `_EmissionMap`

texture definitions for us and some functions to assist with sampling them. We’ll of course still need the Lighting.hlsl include too in order to have access to those functions.

```
#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Lighting.hlsl"
#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/SurfaceInput.hlsl"
```


The **InputData** struct is used to pass some extra things through that are required for lighting calculations. In v10, in includes the following :

```
struct InputData {
float3 positionWS;
half3 normalWS;
half3 viewDirectionWS;
float4 shadowCoord;
half fogCoord;
half3 vertexLighting;
half3 bakedGI;
float2 normalizedScreenSpaceUV;
half4 shadowMask;
};
```


Again, we don’t need to include this code as it’s already in [Input.hlsl](https://github.com/Unity-Technologies/Graphics/blob/master/Packages/com.unity.render-pipelines.universal/ShaderLibrary/Input.hlsl) and that’s automatically included when we include Core.hlsl anyway.

Since the lighting functions use these structs, we’ll need to create them and set each variable it contains. To be more organised, we should do this in separate functions then call them in the fragment shader. The exact contents of the functions can vary slightly depending on what is actually needed for the lighting model.

For now I’m leaving the functions blank to first better see how the file is structured. The next few sections will go through the contents of the `InitializeSurfaceData`

and `InitializeInputData`

functions.

```
// Includes
#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Lighting.hlsl"
#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/SurfaceInput.hlsl"
// Attributes, Varyings, Texture definitions etc.
// ...
// Functions
// ...
// SurfaceData & InputData
void InitializeSurfaceData(Varyings IN, out SurfaceData surfaceData){
surfaceData = (SurfaceData)0; // avoids "not completely initalized" errors
// ...
void InitializeInputData(Varyings IN, half3 normalTS, out InputData inputData) {
inputData = (InputData)0; // avoids "not completely initalized" errors
// ...
// Vertex Shader
// ...
// Fragment Shader
LitPassFragment(Varyings IN) : SV_Target {
// Setup SurfaceData
InitializeSurfaceData(IN, surfaceData);
// Setup InputData
InitializeInputData(IN, surfaceData.normalTS, inputData);
// Lighting Model, e.g.
= UniversalFragmentPBR(inputData, surfaceData);
// or
// half4 color = UniversalFragmentBlinnPhong(inputData, surfaceData); // v12 only
// half4 color = UniversalFragmentBlinnPhong(inputData, surfaceData.albedo, half4(surfaceData.specular, 1),
// surfaceData.smoothness, surfaceData.emission, surfaceData.alpha);
// or something custom
// Handle Fog
= MixFog(color.rgb, inputData.fogCoord);
return color;
}
```


It’s also not too important that the functions are void as far as I’m aware. We could instead return the struct itself. I kinda prefer it that way, but I thought I’d try keeping it more consistent with how the URP/Lit shader code looks.

If you want to organise things further, we could also move all the functions to **separate .hlsl files** and use a `#include`

for it. This would also allow you to reuse that code for multiple shaders, and the Meta pass if you need to support that (discussed in more detail in a later section). At the very least, I’d recommend having a hlsl file containing `InitializeSurfaceData`

and it’s required functions / texture definitions.

### InitializeInputData

As mentioned previously, our `InitializeInputData`

function needs to set each of the variables inside the InputData struct, but this mainly obtaining the data passed through from the vertex stage and using some macros and functions (e.g. in order to handle transformations between spaces).

This struct can also be the same for all lighting models, though I’m sure you could leave some parts out, e.g. if you aren’t supporting baked lighting or the shadowMask. It is important to note that everything in the InputData struct needs to be initalised, so the first line in the function sets everything to 0 initally to avoid errors. You’ll need to be careful then to not miss anything important though. It also helps prevent the shader breaking if an extra variable is added to the struct in future updates to the ShaderLibrary.

```
#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Lighting.hlsl"
#if SHADER_LIBRARY_VERSION_MAJOR < 9
// These functions were added in URP v9.x versions, if we want to support URP versions before, we need to handle it
// If you're in v10 you could remove this if you don't care about supporting prior versions.
// (Note, also using GetWorldSpaceViewDir in Vertex Shader)
// Computes the world space view direction (pointing towards the viewer).
GetWorldSpaceViewDir(float3 positionWS) {
if (unity_OrthoParams.w == 0) {
// Perspective
return _WorldSpaceCameraPos - positionWS;
} else {
// Orthographic
= GetWorldToViewMatrix();
return viewMat[2].xyz;
}
}
half3 GetWorldSpaceNormalizeViewDir(float3 positionWS) {
float3 viewDir = GetWorldSpaceViewDir(positionWS);
if (unity_OrthoParams.w == 0) {
// Perspective
return half3(normalize(viewDir));
} else {
// Orthographic
return half3(viewDir);
}
}
#endif
void InitializeInputData(Varyings input, half3 normalTS, out InputData inputData) {
inputData = (InputData)0; // avoids "not completely initalized" errors
inputData.positionWS = input.positionWS;
#ifdef _NORMALMAP
= half3(input.normalWS.w, input.tangentWS.w, input.bitangentWS.w);
inputData.normalWS = TransformTangentToWorld(normalTS,half3x3(input.tangentWS.xyz, input.bitangentWS.xyz, input.normalWS.xyz));
#else
= GetWorldSpaceNormalizeViewDir(inputData.positionWS);
inputData.normalWS = input.normalWS;
#endif
inputData.normalWS = NormalizeNormalPerPixel(inputData.normalWS);
viewDirWS = SafeNormalize(viewDirWS);
inputData.viewDirectionWS = viewDirWS;
#if defined(REQUIRES_VERTEX_SHADOW_COORD_INTERPOLATOR)
= input.shadowCoord;
#elif defined(MAIN_LIGHT_CALCULATE_SHADOWS)
= TransformWorldToShadowCoord(inputData.positionWS);
#else
= float4(0, 0, 0, 0);
#endif
// Fog
#ifdef _ADDITIONAL_LIGHTS_VERTEX
= input.fogFactorAndVertexLight.x;
inputData.vertexLighting = input.fogFactorAndVertexLight.yzw;
#else
= input.fogFactor;
inputData.vertexLighting = half3(0, 0, 0);
#endif
/* in v11/v12?, could use this :
#ifdef _ADDITIONAL_LIGHTS_VERTEX
inputData.fogCoord = InitializeInputDataFog(float4(inputData.positionWS, 1.0), input.fogFactorAndVertexLight.x);
inputData.vertexLighting = input.fogFactorAndVertexLight.yzw;
#else
inputData.fogCoord = InitializeInputDataFog(float4(inputData.positionWS, 1.0), input.fogFactor);
inputData.vertexLighting = half3(0, 0, 0);
#endif
// Which currently just seems to force re-evaluating fog per fragment
*/
inputData.bakedGI = SAMPLE_GI(input.lightmapUV, input.vertexSH, inputData.normalWS);
inputData.normalizedScreenSpaceUV = GetNormalizedScreenSpaceUV(input.positionCS);
inputData.shadowMask = SAMPLE_SHADOWMASK(input.lightmapUV);
}
```


It’s a bit difficult to go through every function here, so I hope most of this is self-explanatory. The only thing that might not be that clear is the normalizedScreenSpaceUV which is currently only used to sample the **Screen Space Ambient Occlusion** texture later. If you don’t need to support that you could leave it out, but it also doesn’t hurt to include it. If unused, the compiler will likely remove it anyway.

Also in case it’s not clear, `bakedGI`

refers to the **Baked Global Illumination** (baked lighting) and `shadowMask`

refers specifically to when that is set to [Shadowmask mode](https://docs.unity3d.com/Manual/LightMode-Mixed-Shadowmask.html) as an additional shadow mask texture is then used. The `SAMPLE_GI`

and `SAMPLE_SHADOWMASK`

macros will change when compiled depending on specific keywords. You can find those functions in [Lighting.hlsl](https://github.com/Unity-Technologies/Graphics/blob/v10.5.0/com.unity.render-pipelines.universal/ShaderLibrary/Lighting.hlsl) (split/moved to [GlobalIllumination.hlsl](https://github.com/Unity-Technologies/Graphics/blob/master/Packages/com.unity.render-pipelines.universal/ShaderLibrary/GlobalIllumination.hlsl) in v12), and [Shadows.hlsl](https://github.com/Unity-Technologies/Graphics/blob/master/Packages/com.unity.render-pipelines.universal/ShaderLibrary/Shadows.hlsl) of the URP ShaderLibrary.

### Simple Lighting

The URP/SimpleLit shader uses the `UniversalFragmentBlinnPhong`

function from Lighting.hlsl, which uses the **Lambert** and **Blinn-Phong** lighting models. If you aren’t familiar with them I’m sure there are better resources online, but I’ll attempt to explain them quickly :

Lambert models a perfectly **diffuse** surface, where light is reflected in all directions. This involves a **dot product** between the **light direction** and **normal vector** (both normalised).

Phong models the **specular** part of the surface, where light is reflected more when the **view direction** aligns with the light vector reflected by the normal. Blinn-Phong is a slight alteration where instead of a reflected vector, it uses a **half vector** between the light vector and view direction which is more computationally efficient.

While it can be useful to know how to calculate these lighting models, they can be handled for us by the functions in the URP ShaderLibrary. The `UniversalFragmentBlinnPhong`

function uses both the `LightingLambert`

and `LightingSpecular`

(blinn-phong model) functions included in Lighting.hlsl, which are :

```
half3 LightingLambert(half3 lightColor, half3 lightDir, half3 normal) {
half NdotL = saturate(dot(normal, lightDir));
return lightColor * NdotL;
}
half3 LightingSpecular(half3 lightColor, half3 lightDir, half3 normal, half3 viewDir, half4 specular, half smoothness) {
float3 halfVec = SafeNormalize(float3(lightDir) + float3(viewDir));
half NdotH = half(saturate(dot(normal, halfVec)));
half modifier = pow(NdotH, smoothness);
half3 specularReflection = specular.rgb * modifier;
return lightColor * specularReflection;
}
```


We could call these functions by including Lighting.hlsl, or copy the code out, but since the `UniversalFragmentBlinnPhong`

does it for us we can use that instead. We need the two structs to pass into it though. The `InitializeInputData`

function we went through in the section above, but for the `InitializeSurfaceData`

function, it can vary slightly depending on what we need to support (Blinn-Phong doesn’t use the metallic like PBR for example). I’m using the following :

```
#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/SurfaceInput.hlsl"
// Textures, Samplers
// (note, BaseMap, BumpMap and EmissionMap is being defined by the SurfaceInput.hlsl include)
// Functions
SampleSpecularSmoothness(float2 uv, half alpha, half4 specColor, TEXTURE2D_PARAM(specMap, sampler_specMap)) {
half4 specularSmoothness = half4(0.0h, 0.0h, 0.0h, 1.0h);
#ifdef _SPECGLOSSMAP
= SAMPLE_TEXTURE2D(specMap, sampler_specMap, uv) * specColor;
#elif defined(_SPECULAR_COLOR)
= specColor;
#endif
#ifdef _GLOSSINESS_FROM_BASE_ALPHA
= exp2(10 * alpha + 1);
#else
= exp2(10 * specularSmoothness.a + 1);
#endif
return specularSmoothness;
}
void InitializeSurfaceData(Varyings IN, out SurfaceData surfaceData){
surfaceData = (SurfaceData)0; // avoids "not completely initalized" errors
half4 baseMap = SAMPLE_TEXTURE2D(_BaseMap, sampler_BaseMap, IN.uv);
#ifdef _ALPHATEST_ON
// Alpha Clipping
- _Cutoff);
#endif
half4 diffuse = baseMap * _BaseColor * IN.color;
surfaceData.albedo = diffuse.rgb;
surfaceData.normalTS = SampleNormal(IN.uv, TEXTURE2D_ARGS(_BumpMap, sampler_BumpMap));
surfaceData.emission = SampleEmission(IN.uv, _EmissionColor.rgb, TEXTURE2D_ARGS(_EmissionMap, sampler_EmissionMap));
half4 specular = SampleSpecularSmoothness(IN.uv, diffuse.a, _SpecColor, TEXTURE2D_ARGS(_SpecGlossMap, sampler_SpecGlossMap));
surfaceData.specular = specular.rgb;
surfaceData.smoothness = specular.a * _Smoothness;
}
```


As mentioned previously, in the fragment shader we can then call all these functions :

```
#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Lighting.hlsl"
// ...
LitPassFragment(Varyings IN) : SV_Target {
// Setup SurfaceData
InitializeSurfaceData(IN, surfaceData);
// Setup InputData
InitializeInputData(IN, surfaceData.normalTS, inputData);
// Simple Lighting (Lambert & BlinnPhong)
// half4 color = UniversalFragmentBlinnPhong(inputData, surfaceData); // v12 only
= UniversalFragmentBlinnPhong(inputData, surfaceData.albedo, half4(surfaceData.specular, 1),
surfaceData.smoothness, surfaceData.emission, surfaceData.alpha);
color.rgb = MixFog(color.rgb, inputData.fogCoord);
return color;
}
```


For a full example, see the [URP_SimpleLitTemplate](https://github.com/Cyanilux/URP_ShaderCodeTemplates/blob/main/URP_SimpleLitTemplate.shader).

### PBR Lighting

The URP/Lit shader uses a more accurate **Physically Based Rendering** (PBR) model, which is based on Lambert and a [Minimalist CookTorrance model](http://www.thetenthplanet.de/archives/255). The exact implementation is slightly different according to the ShaderLibrary. If interested, you can find how it’s implemented by looking at the `LightingPhysicallyBased`

function in [Lighting.hlsl](https://github.com/Unity-Technologies/Graphics/blob/master/Packages/com.unity.render-pipelines.universal/ShaderLibrary/Lighting.hlsl) and the DirectBRDFSpecular function in [BRDF.hlsl](https://github.com/Unity-Technologies/Graphics/blob/master/Packages/com.unity.render-pipelines.universal/ShaderLibrary/BRDF.hlsl).

We don’t necessarily need to understand how it’s implemented to use it though, we can just call the `UniversalFragmentPBR`

function. As mentioned previously in v10+ it takes the two structs, InputData and SurfaceData. We’ve already discussed creating the `InitializeInputData`

function in a couple sections above. For the `InitializeSurfaceData`

we’ll use :

```
// ...
#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/SurfaceInput.hlsl"
// Textures, Samplers
// (note, BaseMap, BumpMap and EmissionMap is being defined by the SurfaceInput.hlsl include)
TEXTURE2D(_OcclusionMap); SAMPLER(sampler_OcclusionMap);
// Functions
SampleMetallicSpecGloss(float2 uv, half albedoAlpha) {
half4 specGloss;
#ifdef _METALLICSPECGLOSSMAP
= SAMPLE_TEXTURE2D(_MetallicSpecGlossMap, sampler_MetallicSpecGlossMap, uv)
#ifdef _SMOOTHNESS_TEXTURE_ALBEDO_CHANNEL_A
= albedoAlpha * _Smoothness;
#else
*= _Smoothness;
#endif
#else // _METALLICSPECGLOSSMAP
#if _SPECULAR_SETUP
= _SpecColor.rgb;
#else
= _Metallic.rrr;
#endif
#ifdef _SMOOTHNESS_TEXTURE_ALBEDO_CHANNEL_A
= albedoAlpha * _Smoothness;
#else
= _Smoothness;
#endif
#endif
return specGloss;
}
half SampleOcclusion(float2 uv) {
#ifdef _OCCLUSIONMAP
#if defined(SHADER_API_GLES)
return SAMPLE_TEXTURE2D(_OcclusionMap, sampler_OcclusionMap, uv).g;
#else
= SAMPLE_TEXTURE2D(_OcclusionMap, sampler_OcclusionMap, uv).g;
return LerpWhiteTo(occ, _OcclusionStrength);
#endif
#else
return 1.0;
#endif
void InitializeSurfaceData(Varyings IN, out SurfaceData surfaceData){
surfaceData = (SurfaceData)0; // avoids "not completely initalized" errors
half4 albedoAlpha = SampleAlbedoAlpha(IN.uv, TEXTURE2D_ARGS(_BaseMap, sampler_BaseMap));
surfaceData.alpha = Alpha(albedoAlpha.a, _BaseColor, _Cutoff);
surfaceData.albedo = albedoAlpha.rgb * _BaseColor.rgb * IN.color.rgb;
surfaceData.normalTS = SampleNormal(IN.uv, TEXTURE2D_ARGS(_BumpMap, sampler_BumpMap));
surfaceData.emission = SampleEmission(IN.uv, _EmissionColor.rgb, TEXTURE2D_ARGS(_EmissionMap, sampler_EmissionMap));
surfaceData.occlusion = SampleOcclusion(IN.uv);
half4 specGloss = SampleMetallicSpecGloss(IN.uv, albedoAlpha.a);
#if _SPECULAR_SETUP
= 1.0h;
surfaceData.specular = specGloss.rgb;
#else
= specGloss.r;
surfaceData.specular = half3(0.0h, 0.0h, 0.0h);
#endif
= specGloss.a;
}
```


Then in the fragment shader :

```
#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Lighting.hlsl"
// ...
LitPassFragment(Varyings IN) : SV_Target {
// Setup SurfaceData
InitializeSurfaceData(IN, surfaceData);
// Setup InputData
InitializeInputData(IN, surfaceData.normalTS, inputData);
// PBR Lighting
= UniversalFragmentPBR(inputData, surfaceData);
// Fog
= MixFog(color.rgb, inputData.fogCoord);
return color;
}
```


## Other Passes

There are other passes that the Universal RP uses, such as the **ShadowCaster**, **DepthOnly**, **DepthNormals** (v10+) and **Meta** passes. We can also create passes with a custom LightMode tag, discussed in the earlier [Multi-Pass](https://www.cyanilux.com#multi-pass) section.

### ShadowCaster

The pass tagged with `"LightMode"="ShadowCaster"`

is responsible for allowing the object to cast realtime shadows.

In a section earlier I mentioned that `UsePass`

could be used to trigger the shader to use a pass from a different shader, however since this breaks the SRP Batching compatibility we need to instead define the pass in the shader itself.

I find that the easiest way to handle this is let the [ShadowCasterPass.hlsl](https://github.com/Unity-Technologies/Graphics/blob/master/Packages/com.unity.render-pipelines.universal/Shaders/ShadowCasterPass.hlsl) do the work for us (used by shaders like URP/Lit). It contains the Attributes and Varyings structs and fairly simple Vertex and Fragment shaders, handling the shadow bias offsets and alpha clipping/cutout.

```
//UsePass "Universal Render Pipeline/Lit/ShadowCaster"
// Breaks SRP Batcher compatibility, instead we define the pass ourself :
Pass {
Name "ShadowCaster"
Tags { "LightMode"="ShadowCaster" }
ZWrite On
ZTest LEqual
HLSLPROGRAM
#pragma vertex ShadowPassVertex
#pragma fragment ShadowPassFragment
// Material Keywords
#pragma shader_feature _ALPHATEST_ON
#pragma shader_feature _SMOOTHNESS_TEXTURE_ALBEDO_CHANNEL_A
// GPU Instancing
#pragma multi_compile_instancing
// (Note, this doesn't support instancing for properties though. Same as URP/Lit)
// #pragma multi_compile _ DOTS_INSTANCING_ON
// (This was handled by LitInput.hlsl. I don't use DOTS so haven't bothered to support it)
#include "Packages/com.unity.render-pipelines.core/ShaderLibrary/CommonMaterial.hlsl"
#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/SurfaceInput.hlsl"
#include "Packages/com.unity.render-pipelines.universal/Shaders/ShadowCasterPass.hlsl"
}
```


The URP/Lit shader usually includes LitInput.hlsl, however this defines many textures that our shader might not use (which would likely be ignored / compiled out anyway) and it also includes a `UnityPerMaterial CBUFFER`

which we’ve already defined in our `HLSLINCLUDE`

. This causes redefinition errors so I’m instead including a few of the ShaderLibrary files that was included by LitInput.hlsl to make sure the pass still functions without erroring.

CommonMaterial.hlsl is mainly included because of the LerpWhiteTo function is used by Shadows.hlsl when sampling the shadowmap. SurfaceInput.hlsl is included as ShadowCasterPass.hlsl makes use of the `_BaseMap`

and `SampleAlbedoAlpha`

function for the alpha clipping/cutout support.

With this ShadowCaster, our shader should also include the `_BaseMap`

, `_BaseColor`

and `_Cutoff`

properties. If they aren’t included then it won’t error though as it will use them are global shader properties instead.

```
Properties {
[MainTexture] _BaseMap("Base Map (RGB) Smoothness / Alpha (A)", 2D) = "white" {}
[MainColor] _BaseColor("Base Color", Color) = (1, 1, 1, 1)
[Toggle(_ALPHATEST_ON)] _AlphaTestToggle ("Alpha Clipping", Float) = 0
_Cutoff ("Alpha Cutoff", Float) = 0.5
// ...
```


If our main shader uses vertex displacement, we would also need to handle that in the ShadowCaster pass too or the shadow won’t move. This involves swapping the vertex shader out for a custom one, e.g. :

```
HLSLPROGRAM
#pragma vertex DisplacedShadowPassVertex // (instead of ShadowPassVertex)
// ...
Varyings DisplacedShadowPassVertex(Attributes input) {
Varyings output = (Varyings)0;
UNITY_SETUP_INSTANCE_ID(input);
// Example Displacement
+= float4(0, _SinTime.y, 0, 0);
output.uv = TRANSFORM_TEX(input.texcoord, _BaseMap);
output.positionCS = GetShadowPositionHClip(input);
return output;
}
ENDHLSL
```


### DepthOnly

The pass tagged with `"LightMode"="DepthOnly"`

is responsible for writing the object’s depth to the **Camera Depth Texture** - specifically, when the depth buffer cannot be copied or MSAA is enabled. If your shader is opaque and uses `ZWrite On`

in the main pass, it should include a DepthOnly pass, regardless of it being lit/unlit. Transparent shaders can also include it but since the depth texture is generated before drawing transparent objects they won’t appear in it.

The DepthOnly pass is almost identical to what the ShadowCaster does above, except it does not use the shadow bias offsets in the vertex shader (uses the regular `TransformObjectToHClip(IN.positionOS.xyz)`

instead of `GetShadowPositionHClip(input)`

).

Again similar to the above we can make use of the [DepthOnlyPass.hlsl](https://github.com/Unity-Technologies/Graphics/blob/master/Packages/com.unity.render-pipelines.universal/Shaders/DepthOnlyPass.hlsl) used by shaders like URP/Lit to define the Attributes and Varyings structs and Vertex and Fragment shaders for us.

```
Pass {
Name "DepthOnly"
Tags { "LightMode"="DepthOnly" }
ColorMask 0
ZWrite On
ZTest LEqual
HLSLPROGRAM
#pragma vertex DepthOnlyVertex
#pragma fragment DepthOnlyFragment
// Material Keywords
#pragma shader_feature _ALPHATEST_ON
#pragma shader_feature _SMOOTHNESS_TEXTURE_ALBEDO_CHANNEL_A
// GPU Instancing
#pragma multi_compile_instancing
// #pragma multi_compile _ DOTS_INSTANCING_ON
#include "Packages/com.unity.render-pipelines.core/ShaderLibrary/CommonMaterial.hlsl"
#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/SurfaceInput.hlsl"
#include "Packages/com.unity.render-pipelines.universal/Shaders/DepthOnlyPass.hlsl"
}
```


Again, if we want to support vertex displacement we need a custom vertex shader :

```
HLSLPROGRAM
#pragma vertex DisplacedDepthOnlyVertex // (instead of DepthOnlyVertex)
// ...
Varyings DisplacedDepthOnlyVertex(Attributes input) {
Varyings output = (Varyings)0;
UNITY_SETUP_INSTANCE_ID(input);
UNITY_INITIALIZE_VERTEX_OUTPUT_STEREO(output);
// Example Displacement
+= float4(0, _SinTime.y, 0, 0);
output.uv = TRANSFORM_TEX(input.texcoord, _BaseMap);
output.positionCS = TransformObjectToHClip(input.position.xyz);
return output;
}
ENDHLSL
```


### DepthNormals

The pass tagged with `"LightMode"="DepthNormals"`

is responsible for writing the object’s depth to the **Camera Depth Texture** and normals to the **Camera Normals Texture** if requested by a **Renderer Feature** on the camera’s Forward/Universal Renderer.

For example, the **Screen Space Ambient Occlusion** feature can support using the **Depth Normals** as it’s source, or can reconstruct normals from **Depth** (so use the DepthOnly pass instead) which avoids creating an additional buffer / render texture to store that `_CameraNormalsTexture`

.

If you’re really sure that you don’t need SSAO or other features that might use it you could exclude the pass, but I’d recommend supporting it anyway to avoid later confusion when objects aren’t appearing in the depth & normals textures!

Similar to the previous passes, we can use the [DepthNormalsPass.hlsl](https://github.com/Unity-Technologies/Graphics/blob/master/Packages/com.unity.render-pipelines.universal/Shaders/DepthNormalsPass.hlsl).

```
Pass {
Name "DepthNormals"
Tags { "LightMode"="DepthNormals" }
ZWrite On
ZTest LEqual
HLSLPROGRAM
#pragma vertex DepthNormalsVertex
#pragma fragment DepthNormalsFragment
// Material Keywords
#pragma shader_feature_local _NORMALMAP
//#pragma shader_feature_local _PARALLAXMAP
//#pragma shader_feature_local _ _DETAIL_MULX2 _DETAIL_SCALED
#pragma shader_feature_local_fragment _ALPHATEST_ON
#pragma shader_feature_local_fragment _SMOOTHNESS_TEXTURE_ALBEDO_CHANNEL_A
// GPU Instancing
#pragma multi_compile_instancing
//#pragma multi_compile _ DOTS_INSTANCING_ON
#include "Packages/com.unity.render-pipelines.core/ShaderLibrary/CommonMaterial.hlsl"
#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/SurfaceInput.hlsl"
#include "Packages/com.unity.render-pipelines.universal/Shaders/DepthNormalsPass.hlsl"
// Note if we do any vertex displacement, we'll need to change the vertex function. e.g. :
/*
#pragma vertex DisplacedDepthOnlyVertex (instead of DepthOnlyVertex above)
Varyings DisplacedDepthOnlyVertex(Attributes input) {
Varyings output = (Varyings)0;
UNITY_SETUP_INSTANCE_ID(input);
UNITY_INITIALIZE_VERTEX_OUTPUT_STEREO(output);
// Example Displacement
input.positionOS += float4(0, _SinTime.y, 0, 0);
output.uv = TRANSFORM_TEX(input.texcoord, _BaseMap);
output.positionCS = TransformObjectToHClip(input.position.xyz);
VertexNormalInputs normalInput = GetVertexNormalInputs(input.normal, input.tangentOS);
output.normalWS = NormalizeNormalPerVertex(normalInput.normalWS);
return output;
}
*/
ENDHLSL
}
```


It’s worth mentioning that newer versions of URP (v12) use [LitDepthNormalsPass.hlsl](https://github.com/Unity-Technologies/Graphics/blob/master/Packages/com.unity.render-pipelines.universal/Shaders/LitDepthNormalsPass.hlsl) instead, which provides support for using the normal map and detail normal map, as well as parallax/height mapping (requiring the additional keywords commented in the above code too).

### Meta

The pass tagged with `"LightMode"="Meta"`

is used when baking global illumination. If you aren’t using baked GI then you could ignore this pass.

For Unlit shaders, you may want to look into using the [UnlitMetaPass.hlsl](https://github.com/Unity-Technologies/Graphics/blob/master/Packages/com.unity.render-pipelines.universal/Shaders/UnlitMetaPass.hlsl) similar to the above passes.

For Lit shaders, we could probably use [LitMetaPass.hlsl](https://github.com/Unity-Technologies/Graphics/blob/master/Packages/com.unity.render-pipelines.universal/Shaders/LitMetaPass.hlsl), however it wants a `InitializeStandardLitSurfaceData`

function which isn’t exactly what we’re using and my PBR example also includes vertex colour so we would need to change the Varyings too. Instead I ended up using this instead :

```
Pass {
Name "Meta"
Tags{"LightMode" = "Meta"}
Cull Off
HLSLPROGRAM
#pragma vertex UniversalVertexMeta
#pragma fragment UniversalFragmentMeta
#pragma shader_feature_local_fragment _SPECULAR_SETUP
#pragma shader_feature_local_fragment _EMISSION
#pragma shader_feature_local_fragment _METALLICSPECGLOSSMAP
#pragma shader_feature_local_fragment _ALPHATEST_ON
#pragma shader_feature_local_fragment _ _SMOOTHNESS_TEXTURE_ALBEDO_CHANNEL_A
//#pragma shader_feature_local _ _DETAIL_MULX2 _DETAIL_SCALED
#pragma shader_feature_local_fragment _SPECGLOSSMAP
struct Attributes {
float4 positionOS : POSITION;
float3 normalOS : NORMAL;
float2 uv0 : TEXCOORD0;
float2 uv1 : TEXCOORD1;
float2 uv2 : TEXCOORD2;
#ifdef _TANGENT_TO_WORLD
#endif
};
struct Varyings {
float4 positionCS : SV_POSITION;
float2 uv : TEXCOORD0;
float4 color : COLOR;
};
#include "PBRSurface.hlsl"
#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/MetaInput.hlsl"
Varyings UniversalVertexMeta(Attributes input) {
Varyings output;
output.positionCS = MetaVertexPosition(input.positionOS, input.uv1, input.uv2, unity_LightmapST, unity_DynamicLightmapST);
output.uv = TRANSFORM_TEX(input.uv0, _BaseMap);
return output;
}
half4 UniversalFragmentMeta(Varyings input) : SV_Target {
SurfaceData surfaceData;
InitializeSurfaceData(input, surfaceData);
BRDFData brdfData;
InitializeBRDFData(surfaceData.albedo, surfaceData.metallic, surfaceData.specular, surfaceData.smoothness, surfaceData.alpha, brdfData);
MetaInput metaInput;
metaInput.Albedo = brdfData.diffuse + brdfData.specular * brdfData.roughness * 0.5;
metaInput.SpecularColor = surfaceData.specular;
metaInput.Emission = surfaceData.emission;
return MetaFragment(metaInput);
}
ENDHLSL
}
```


Where `PBRSurface.hlsl`

is a custom HLSL file in the same folder as the shader file. It contains the `InitializeSurfaceData`

function used in the PBR Lighting section, (as well as the SurfaceInput.hlsl include, Texture/Sampler definitions and functions required by `InitializeSurfaceData`

such as `SampleMetallicSpecGloss`

and `SampleOcclusion`

. The UniversalForward pass also includes that file instead of having that code in the shader.

If you’ve read this far, thanks! The final section contains a summary of all the differences between URP and the Built-in RP - mostly intended for those that are already familiar with coding shaders, but still a useful summary of everything discussed already too.

I’ve also got a section below containing **examples/templates** built from the shader code used in this post.

# Summary of Built-in vs URP differences

## ShaderLab :

- SubShader in URP uses the “RenderPipeline”=”UniversalPipeline” tag
- Passes in URP use some different “LightMode” tags than Built-In. The most common being “UniversalForward” or left out completely (which defaults it to “SRPDefaultUnlit”). See
[LightMode Tag section](https://www.cyanilux.com#lightmode-tag)for list. - Only the first UniversalForward pass is rendered. Multi-Pass shaders in URP is supported with additional passes using SRPDefaultUnlit, but it breaks SRP Batcher compatibility so is not recommended. See the
[Multi-Pass section](https://www.cyanilux.com#multi-pass)for alternatives (i.e Second Material or RenderObjects feature). - URP does not support GrabPass. Instead, a camera opaque texture is captured between rendering opaque and transparent objects which can be used for some distortion/refraction effects for shaders in the transparent queue.
`#include`

the[DeclareOpaqueTexture.hlsl](https://github.com/Unity-Technologies/Graphics/blob/master/Packages/com.unity.render-pipelines.universal/ShaderLibrary/DeclareOpaqueTexture.hlsl)file and use it’s`SampleSceneColor`

function with the ScreenPos (positionNDC) as the uv input. Other transparent objects will not appear in the texture. If you need that, an alternative may be to use a Custom Renderer Feature to render additive distortion objects into an offscreen buffer then distort the final screen result using`CommandBuffer.Blit`

. The idea would be similar to this[Makin’ Stuff Look Good in Unity video](https://www.youtube.com/watch?v=xH5uUfeB2Go)but the code used there is still intended for built-in.

## HLSL :

- HLSLPROGRAM and ENDHLSL should always be used instead of CGPROGRAM/ENDCG. This is because the latter includes some additional files which conflicts with the URP ShaderLibrary causing redefinitions errors.
- The “fixed” type/precision does not exist in HLSLPROGRAM, use “half” instead.
- URP does not support Surface shaders (
`#pragma surface`

), only Vertex/Fragment style shaders. (Geometry and Hull/Domain is also still supported) - Structs used to pass data between the vertex and fragment shaders is commonly called Attributes and Varyings in URP instead of appdata and v2f. This is mainly a naming convention and isn’t important though.
- Instead of including UnityCG.cginc, use the URP ShaderLibrary. The main one to include is :

`#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"`


- The SRP Batcher batches the setup between draw calls, so rendering multiple objects with the same shader is less expensive. It even batches objects with different materials, but not different shaders / shader variants. In order for a shader to be compatible with this, it must include the URP ShaderLibrary and include a UnityPerMaterial CBUFFER that contains each of the exposed ShaderLab Properties (except textures). It cannot include global shader variables or compatibility breaks. You can check whether a shader is compatible from the Inspector. The CBUFFER must also remain constant for all shader passes, so it is recommended to put it inside HLSLINCLUDE in the SubShader. For example :

```
HLSLINCLUDE
#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
CBUFFER_START(UnityPerMaterial)
float4 _ExampleTexture_ST; // Tiling & Offset, x = TilingX, y = TilingY, z = OffsetX, w = OffsetY
// x = 1/width, y = 1/height, z = width, w = height.
float _ExampleRange;
float _ExampleFloat;
float4 _ExampleVector;
// etc.
ENDHLSL
```


- Instead of
`_MainTex`

, URP tends to use`_BaseMap`

instead. It’s mostly just a naming convention difference, and isn’t too important unless you include[SurfaceInput.hlsl](https://github.com/Unity-Technologies/Graphics/blob/master/Packages/com.unity.render-pipelines.universal/ShaderLibrary/SurfaceInput.hlsl)which defines the Albedo, Bump and Emission textures for you.`_MainTex`

should still be used for image effects using`CommandBuffer.Blit`

(i.e.[Blit Render Feature](https://github.com/Cyanilux/URP_BlitRenderFeature)) and obtaining the sprite from a SpriteRenderer component. - URP provides macros for defining textures, and uses the DX10+ style syntax which defines a Texture and Sampler separately :

```
TEXTURE2D(_BaseMap);
SAMPLER(sampler_BaseMap);
```


- And for sampling the texture :

```
half4 baseMap = SAMPLE_TEXTURE2D(_BaseMap, sampler_BaseMap, IN.uv);
// Can only be used in fragment shader, similar to tex2D() from built-in
// If sampling in vertex shader, use LOD version to select the mipmap level used :
= SAMPLE_TEXTURE2D_LOD(_BaseMap, sampler_BaseMap, IN.uv, 0);
// Also tex2Dbias and tex2Dgrad would be equivalent to these macros in URP :
float bias = -1;
half4 baseMap = SAMPLE_TEXTURE2D_BIAS(_BaseMap, sampler_BaseMap, IN.uv, bias);
float dpdx = ddx(IN.uv.x);
float dpdy = ddy(IN.uv.y);
half4 baseMap = SAMPLE_TEXTURE2D_GRAD(_BaseMap, sampler_BaseMap, IN.uv, dpdx, dpdy);
```


- For other texture types (i.e. Texture2DArray, Texture3D, TextureCube, TextureCubeArray), see the
[Texture Objects section](https://www.cyanilux.com#texture-objects)for additional macros. - URP includes a function called
`GetVertexPositionInputs`

which can be used in the vertex shader to easily obtain transforms to other spaces. Any unused ones won’t be calculated so using this is quite a convenient. For example :

```
struct Attributes {
float4 positionOS : POSITION;
};
struct Varyings {
float3 positionCS : SV_POSITION;
float3 positionWS : TEXCOORD2;
};
Varyings vert(Attributes IN) {
Varyings OUT;
VertexPositionInputs positionInputs = GetVertexPositionInputs(IN.positionOS.xyz);
OUT.positionCS = positionInputs.positionCS; // Clip Space
= positionInputs.positionWS; // World Space
// OUT.positionVS = positionInputs.positionVS; // View Space
// OUT.positionNDC = positionInputs.positionNDC; // Normalised Device Coords, aka ScreenPos
return OUT;
}
```


- Similarly, there is a
`GetVertexNormalInputs`

, to obtain the world space normal (`normalWS`

), as well as world space tangent (`tangentWS`

) and bitangent (`bitangentWS`

). If you just need the normal you can use`TransformObjectToWorldNormal`

instead too.

## Keywords

Shaders in URP commonly use these keywords for a Lit shader :

```
// Additional Lights (e.g. Point, Spotlights)
#pragma multi_compile _ _ADDITIONAL_LIGHTS_VERTEX _ADDITIONAL_LIGHTS
// Shadows
#pragma multi_compile _ _MAIN_LIGHT_SHADOWS
#pragma multi_compile _ _MAIN_LIGHT_SHADOWS_CASCADE
// Note, v11 changes this to :
// #pragma multi_compile _ _MAIN_LIGHT_SHADOWS _MAIN_LIGHT_SHADOWS_CASCADE _MAIN_LIGHT_SHADOWS_SCREEN
#pragma multi_compile_fragment _ _ADDITIONAL_LIGHT_SHADOWS
#pragma multi_compile_fragment _ _SHADOWS_SOFT
// Baked GI
#pragma multi_compile _ LIGHTMAP_ON
#pragma multi_compile _ DIRLIGHTMAP_COMBINED
#pragma multi_compile _ LIGHTMAP_SHADOW_MIXING
#pragma multi_compile _ SHADOWS_SHADOWMASK
// Other
#pragma multi_compile_fog
#pragma multi_compile_instancing
#pragma multi_compile _ DOTS_INSTANCING_ON
#pragma multi_compile_fragment _ _SCREEN_SPACE_OCCLUSION
```


If unlit, the fog and instancing ones may be the only ones needed.

There’s also a bunch of shader_feature ones that shaders could include, you can see the templates (below) for common ones (e.g. _NORMALMAP) but they depend on the shader and shouldn’t always be included unless supporting what the keyword does.

## Common Functions/Macros :


| Built-In | URP Equivalent |
|---|---|
`TRANSFORM_TEX(uv, textureName)` |
`TRANSFORM_TEX(uv, textureName)` |
`tex2D` , `tex2Dlod` , etc |
`SAMPLE_TEXTURE2D` , `SAMPLE_TEXTURE2D_LOD` , etc. See above |
`UnityObjectToClipPos(positionOS)` |
`TransformObjectToHClip(positionOS)` , or use `GetVertexPositionInputs().positionCS` |
`UnityObjectToWorldNormal(normalOS)` |
`TransformObjectToWorldNormal(normalOS)` , or use `GetVertexNormalInputs().normalWS` |
`ComputeScreenPos(positionCS)` |
`ComputeScreenPos(positionCS)` , though
`GetVertexPositionInputs().positionNDC` instead |
`ComputeGrabScreenPos(positionCS)` |
GrabPass is not supported in URP |
`WorldSpaceViewDir(positionOS)` |
Calculate `positionWS` and use the below function instead |
`UnityWorldSpaceViewDir(positionWS)` |
`GetWorldSpaceViewDir(positionWS)` (added to
`GetWorldSpaceNormalizeViewDir(positionWS)` instead. |
`WorldSpaceLightDir(positionOS)` |
See below |
`UnityWorldSpaceLightDir(positionWS)` / `_WorldSpaceLightPos0` |
For Main Directional Light, use `GetMainLight().direction` . See
|
`Shade4PointLights(...)` |
No direct equivalent really, but built-in uses this for vertex lighting in Forward, so see below. |
`ShadeVertexLights(vertex, normal)` |
`VertexLighting(positionWS, normalWS)` in
|
`ShadeSH9(half4(worldNormal,1))` |
`SampleSH(normalWS)` , but use `SAMPLE_GI(input.lightmapUV, input.vertexSH, inputData.normalWS)` macro / `SampleSHVertex/SampleSHPixel` functions in
|
`UNITY_FOG_COORDS(n)` |
`float fogFactor : TEXCOORDn` |
`UNITY_TRANSFER_FOG(o, positionCS)` |
`OUT.fogFactor = ComputeFogFactor(positionCS.z)` |
`UNITY_APPLY_FOG(fogCoord, color)` |
`color.rgb = MixFog(color.rgb, fogCoord)` |
`UNITY_APPLY_FOG_COLOR(fogCoord, color, fogColor)` |
`color.rgb = MixFogColor(color.rgb, fogColor.rgb, fogCoord)` |
`Linear01Depth(z)` |
`Linear01Depth(z, _ZBufferParams)` |
`LinearEyeDepth(z)` |
`LinearEyeDepth(z, _ZBufferParams)` |
`ParallaxOffset(h, height, viewDirTS)` |
`ParallaxOffset1Step(h, amplitude, viewDirTS)` if in v10.1+ (for versions prior, copy function out). See
|
`Luminance(rgb)` |
`Luminance(rgb)` , See
|
`V2F_SHADOW_CASTER` |
Equivalent is roughly just `float4 positionCS : SV_POSITION;` but see the
|
`TRANSFER_SHADOW_CASTER_NORMALOFFSET` |
See `GetShadowPositionHClip(input)` example in
|
`SHADOW_CASTER_FRAGMENT` |
`return 0;` |
`SHADOW_COORDS(1)` |
`float4 shadowCoord : TEXCOORD1; ` |
`TRANSFER_SHADOW(o)` |
`TransformWorldToShadowCoord(inputData.positionWS)` |
`SHADOW_ATTENUATION(i)` |
`MainLightRealtimeShadow(shadowCoord)` , though `GetMainLight(shadowCoord)` will also handle it. See
|


(If there’s any commonly used functions from built-in not listed here, let me know and I’ll look into adding them!)

# Templates

You can find some templates/examples that I’ve shared on my [github here](https://github.com/Cyanilux/URP_ShaderCodeTemplates). It includes :

- Opaque Unlit Shader Template
- Transparent Unlit Shader Template
- Opaque Unlit+ Shader Template
- (includes optional Alpha Clipping and ShadowCaster, DepthOnly & DepthNormals passes)

- Diffuse Lit Shader Template
- (Ambient / Baked GI & Lambert Diffuse shading from Main Directional Light only)

- Simple Lit Shader Template
- (Lambert Diffuse & Blinn-Phong Specular. Uses
`UniversalFragmentBlinnPhong`

method from Lighting.hlsl, similar to URP/SimpleLit shader)

- (Lambert Diffuse & Blinn-Phong Specular. Uses
- PBR Lit Shader Template
- (Physically Based Rendering lighting model. Uses
`UniversalFragmentPBR`

method from Lighting.hlsl, similar to URP/Lit shader. Note, doesn’t include height/parallax mapping, detail maps or clear coat. Split into URP_PBRLitTemplate.shader, PBRSurface.hlsl and PBRInput.hlsl for organisation & Meta pass support)

- (Physically Based Rendering lighting model. Uses

## Thanks for reading! 😊

If you find this post helpful, please consider sharing it with others / on socials

Donations are also **greatly** appreciated! 🙏✨

(Keeps this site free from ads and allows me to focus more on tutorials)