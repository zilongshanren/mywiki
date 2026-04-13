---
title: 'Shader bits: World and screen space position'
url: https://halisavakis.com/shader-bits-world-and-screen-space-position/
published: '2017-10-11'
source_blog: Technically Art – Harry Alisavakis
source_site: https://halisavakis.com
category: graphics
fetched: '2026-04-13'
---

Debuting a new post series that will hopefully feature more posts in the future, tonight I just wanted to mention some quick tips that could be really useful for lots of use cases! This time, we’ll see how to get an object’s position in world and screen space, for both vertex-fragment and surface shaders. So let’s-a go!

## Vertex-fragment shader

In order to get our object’s position in world and screen space for this type of shaders, we need to use some of the built-in [values](https://docs.unity3d.com/Manual/SL-UnityShaderVariables.html) and [functions](https://docs.unity3d.com/Manual/SL-BuiltinFunctions.html) provided by Unity.

### World space position

For an object’s world space position, all we need is to add these lines to our shader’s v2f struct and vert function:

struct v2f { float2 uv : TEXCOORD0; UNITY_FOG_COORDS(1) float4 vertex : SV_POSITION; float4 worldPos : TEXCOORD2; };

v2f vert (appdata v) { v2f o; o.vertex = UnityObjectToClipPos(v.vertex); o.uv = TRANSFORM_TEX(v.uv, _MainTex); o.worldPos = mul(unity_ObjectToWorld, v.vertex); UNITY_TRANSFER_FOG(o,o.vertex); return o; }

After we declare our variable in the v2f struct, we just have to multiply the built-in matrix “unity_ObjectToWorld” with our object’s vertex position in order to map it to the object’s position in world space. After that, we can take it in either the vertex or fragment shader and use it as we please!

### Screen space position

To get our object’s position in screen space, the process is similar, though a bit more straightforward. Again, these are the changes that are needed to be done in the v2f struct and the vertex shader:

struct v2f { float2 uv : TEXCOORD0; UNITY_FOG_COORDS(1) float4 vertex : SV_POSITION; float4 scrPos : TEXCOORD2; };

v2f vert (appdata v) { v2f o; o.vertex = UnityObjectToClipPos(v.vertex); o.uv = TRANSFORM_TEX(v.uv, _MainTex); o.scrPos = ComputeScreenPos(o.vertex); UNITY_TRANSFER_FOG(o,o.vertex); return o; }

In this case there’s a function that takes the object’s clip space position and gives us it’s screen space position.

## Surface shader

As you probably already know, surface shaders are a bit more straightforward than vertex-fragment shaders, as they abstract some of the nitty gritty of the shader’s functionality. That makes them great to iterate on some effects quickly, but because of all the abstraction, they can be a bit hard to customize. Nevertheless, in this case, their straightfowardness is really helpful, as they make the task of getting the world and screen space coordinates of our object a matter of 2 words.

You also can check Unity’s [manual](https://docs.unity3d.com/Manual/SL-SurfaceShaders.html) on the different built-in stuff for surface shaders.

### World space position

In the case of surface shaders, there is no need to add a vertex segment for our task. Unity provides a bunch of built-in parameters for the “Input” struct which can help us with what we want. Specifically, all we need to get the world space of our object is this small change:

struct Input { float2 uv_MainTex; float3 worldPos; };

Seriously, that’s it. You can then take the worldPos in the surface segment and just go nuts.

### Screen space position

Prepare to have your mind blown:

struct Input { float2 uv_MainTex; float3 screenPos; };

Job’s done.

## Conclusion

You can tell, there’s nothing too fancy going on here; and that’s ok! My purpose for this series is to have small useful bits in one place for somebody (myself included) to find. I have more bits like that, which I hope that I’ll post soon. So, see you in the [next one](http://halisavakis.com/shader-bits-camera-distance-view-direction-and-normal-vectors/)!