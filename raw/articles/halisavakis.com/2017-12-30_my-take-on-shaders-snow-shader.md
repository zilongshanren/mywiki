---
title: 'My take on shaders: Snow shader'
url: https://halisavakis.com/my-take-on-shaders-snow-shader/
published: '2017-12-30'
source_blog: Technically Art – Harry Alisavakis
source_site: https://halisavakis.com
category: graphics
fetched: '2026-04-13'
---

In this post I have a very simple shader for you, which serves two main purposes: to talk more about our lord and savior, the dot product, and to write a small and easy post to justify me not being so active. Nevertheless, this effect is definitely useful and interesting in many ways. It also gives me the opportunity to discuss some good shader code writing practices. There, now I can sleep without considering myself totally inexcusable for slacking off with this post.

Let’s discuss the effect first. The whole point of this surface shader is to add a different set of textures and PBR settings (in this case glossiness and metallic values) to the object which will applied only on faces with normal vectors that face a certain direction. The most obvious use for this is a snow shader, as one can assume that the snow falls on the top of an object. However, while the shader is named “SnowShader” and many properties use the word “snow”, the effect can obviously be used for other types of textures, like moss. I will just present the snow example, and hopefully my explanation of the logic behind it will inspire you to try out different variations.

Here’s some code:

Shader "Custom/SnowShader" { Properties { _Color ("Color", Color) = (1,1,1,1) _MainTex ("Albedo (RGB)", 2D) = "white" {} _Glossiness ("Smoothness", Range(0,1)) = 0.5 _Metallic ("Metallic", Range(0,1)) = 0.0 _MainNormal ("MainNormal", 2D) = "bump" {} [Header(Snow info)] _SnowTexture("Snow texture", 2D) = "white" {} _SnowNormal("Snow normal", 2D) = "bump" {} _SnowColor("Snow color", color) = (1,1,1,1) _SnowDirection ("Snow direction", Vector) = (0, 1, 0) _SnowLevel ("Snow level", Range(-1, 1)) = 0 _SnowGlossiness("Snow glossiness", Range(0, 1)) = 0.5 _SnowMetallic ("Snow Metallic", Range(0,1)) = 0.0 } SubShader { Tags { "RenderType"="Opaque" } LOD 200 CGPROGRAM // Physically based Standard lighting model, and enable shadows on all light types #pragma surface surf Standard fullforwardshadows // Use shader model 3.0 target, to get nicer looking lighting #pragma target 3.0 sampler2D _MainTex; struct Input { float2 uv_MainTex; float2 uv_MainNormal; float2 uv_SnowNormal; float2 uv_SnowTexture; float3 worldNormal; INTERNAL_DATA }; half _Glossiness; half _Metallic; fixed4 _Color; sampler2D _MainNormal; sampler2D _SnowTexture; sampler2D _SnowNormal; fixed4 _SnowColor; float4 _SnowDirection; float _SnowLevel; float _SnowGlossiness; float _SnowMetallic; // Add instancing support for this shader. You need to check 'Enable Instancing' on materials that use the shader. // See https://docs.unity3d.com/Manual/GPUInstancing.html for more information about instancing. // #pragma instancing_options assumeuniformscaling UNITY_INSTANCING_BUFFER_START(Props) // put more per-instance properties here UNITY_INSTANCING_BUFFER_END(Props) void surf (Input IN, inout SurfaceOutputStandard o) { //Color and normals of the main textures fixed4 c = tex2D (_MainTex, IN.uv_MainTex) * _Color; float3 normals = UnpackNormal (tex2D(_MainNormal, IN.uv_MainNormal)); //Color and normals of the snow textures fixed4 snowColor = tex2D(_SnowTexture, IN.uv_SnowTexture) * _SnowColor; float3 snowNormals = UnpackNormal(tex2D(_SnowNormal, IN.uv_SnowNormal)); //Snow direction calculation half snowDot = step(_SnowLevel, dot(WorldNormalVector(IN, normals), normalize(_SnowDirection))); o.Normal = lerp(normals, snowNormals, snowDot); o.Albedo = lerp(c.rgb, snowColor.rgb, snowDot); o.Metallic = lerp(_Metallic, _SnowMetallic, snowDot); o.Smoothness = lerp(_Glossiness, _SnowGlossiness, snowDot); o.Alpha = c.a; } ENDCG } FallBack "Diffuse" }

It may look intimidating, but the properties and fields are actually more than the lines of actual code, so don’t worry. Lines 10-16 are the property declarations for the snow texture-related information as well as the direction of the snow (“_SnowDirection”) and the level of the snow (“_SnowLevel”) which determines the snow coverage of the object.

In lines 32-37 I add more data in the Input structure to use later. Lines 32-35 are just separate UV coordinates for each texture in order to use the scale and offset fields through the editor. Lines 36 and 37 are used to determine the world normals later in the fragment shader. The “INTERNAL_DATA” looks way out of place here, but it is needed to use the “WorldNormalVector” method later.

After that mess there’s the redeclaration of the pile of fields from the properties and then, the “surf” function. As my, oh so well placed, comments indicated, in lines 63 and 64 I get the original color and normals of the object. There is nothing exotic happening here, this is the standard way to get the albedo color and the normal vectors in a surface shader. In lines 66 and 67 I do exactly the same with the color and normal textures of the snow material.

Then, at line 69, I get a dot product according to which the shader will interpolate between the original material and the snow material. Let’s break this line down to take a closer look:

- dot(WorldNormalVector(IN, normals), normalize(_SnowDirection)): This is the dot product between the world normal vectors of the object and the direction of the snow as set from the properties. In order to move the normals from object space to world space, we need to call the aforementioned “WorldNormalVector” function and pass in the IN object as well as the normals as calculated from the normal map (in line 64). The snow direction is set as (0,1,0) by default, which is vector pointing up. It is also normalized to make sure that our dot product goes from -1 to 1. Therefore, this dot product will return the following values:
- 0 if the face of the object faces in a direction perpendicular to the snow direction
- 1 if the face of the object faces in the same direction as the snow direction (upwards in this case, which is the case where we want the most snow)
- -1 if the face of the object faces in the opposite direction as the snow direction (downwards in this case, which is the most unlikely case to get snow)

- Since we have the dot product, we want to use it along with the _SnowLevel to determine how much snow will be on the object. The premise is simple: if the dot product is larger than the _SnowLevel, return 1, otherwise return 0. This could be easily written with an “if” statement, but as stated in the
[previous post](http://halisavakis.com/my-take-on-shaders-directional-coloring/), “if” conditions in fragment (or in this case, surface) shaders are a no-no performance-wise. Therefore, in order to reproduce the same result in this case, we can use the “step” function, which does exactly what I described: “step(x,y)” will return 0 if x < y and 1 if x >= y. This is why the whole dot product is used in that big “step” function call.

Lines 71 – 74 are pretty straightforward. Using the “snowDot” value from line 69 I interpolate between the original values and the snow values, on normals, albedo, metallic value and glossiness value respectively. The “lerp” function here is kinda overkill, as the snowDot value is either 0 or 1. But it’s still better than a conditional, so I’m sticking with that.

## Conclusion

That’s it for this short tutorial! The main takeaways here (for me at least) are the usefulness of the dot product (again) in terms of thinking with directions as well as thinking “creative” ways to replace “if” statements to improve performance. Getting the world-space normal vectors in a surface shader is also very useful, so I’d keep that in mind too.

That’s all for now, see you in the next one!