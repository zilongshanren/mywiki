---
title: 'My take on shaders: Grass Shader (Part II)'
url: https://halisavakis.com/my-take-on-shaders-grass-shader-part-ii/
published: '2019-11-30'
source_blog: Technically Art – Harry Alisavakis
source_site: https://halisavakis.com
category: graphics
fetched: '2026-04-13'
---

## Patrons

This post is brought to you by these awesome Patreon supporters:

- Djinnlord
- Nicolo Linder
- orels1
- Tiph’ (DN)

## Introduction

Welcome to the second, and probably final part of the grass shader tutorial! Here we’ll expand on the shader from [the first grass tutorial](https://halisavakis.com/my-take-on-shaders-grass-shader-part-i/) and add some neat features to get yourself some nice looking grass! Specifically the features we’ll add are:

- Tessellation for more lush grass
- Lighting, translucency and shading
- Shadow receiving and casting
- A small grass trample effect (only for one object though)

Most of the features, especially the shadow and tessellation stuff, are from [Roystan’s grass shader tutorial](https://roystan.net/articles/grass-shader.html) and they’ve been adjusted to fit the shader from the previous tutorial. You can see these stuff in Roystan’s tutorial too, so this tutorial won’t be the only one on these subjects, it’s just supplementary material.

## Shader overview

The blade generation algorithm is exactly the same as before, as far as the geometry and placement are concerned. However, there are two additional things we calculate in the geometry shader:

- Normal generation: Since we will light up our grass blades, we need to calculate the normal vector for each vertex of each blade and pass it to our fragment shader. The way these are calculated are fairly straightforward:
- We need the vector that’s perpendicular to the grass blade
- We have 4 points when it come to the grass blade: the two points of the base (A and B), the middle point on the base (M) and the top point of the triangle (C)
- The normal vector N will be the cross product of the vectors AB and MC


![](../../assets/1c18d83ecc6a8dbc.png)

- Grass trample: Based on a position and a radius, the grass blades are offset from the position in a sphere-like configuration to simulate being trampled by an external object.

The tessellation on the shader is added in the exact same way as it’s added in Roystan’s tutorial:

- You grab the “CustomTessellation.cginc” from
[this great tutorial by Catlike Coding](https://catlikecoding.com/unity/tutorials/advanced-rendering/tessellation/) - You include it in your shader using
*#include “CustomTessellation.cginc”* - You add a float property called ” _TessellationUniform” to the shader
- In your passes, besides the
*#pragma vertex vert*and similar directives, you add*#pragma hull hull*and*#pragma domain domain*

Finally there’s the lighting and shadow side of things:

- Lighting: For the main lighting technique I went with a Half-Lambert type of lighting (NdotL * 0.5 + 0.5) in order to have a softer type of shading. Keep in mind that since we’re in a vertex-(geometry-)fragment shader, it’s not as straightforward to have the grass react to all types of light or to any number of them. So here I’ve settled for just the first directional light in the scene. Also, to add more consistency to the scene, I’m adding the ambient color of the scene to the final color.
- Translucency: There’s a very very simple translucency effect here, which is achieved by getting the dot product of the view direction vector and the inversed direction of the directional light. The result is then multiplied by an HDR color for the added translucency and the whole thing is applied on a fresnel mask on the grass.
- Shadows: The grass will be able to receive shadows using the “SHADOW_ATTENUATION” macro (more on that later). It will also be able to cast shadows via a separate, shadow-casting pass.

## The code

Let’s see how all that looks in-code:

```
//Multiple features of this shader come from Roystan's grass shader tutorial: https://roystan.net/articles/grass-shader.html
Shader "Geometry/GrassGeometryShader"
{
Properties
{
//Color stuff
_Color("Color", Color) = (1,1,1,1)
_GradientMap("Gradient map", 2D) = "white" {}
//Tessellation
_TessellationUniform ("Tessellation Uniform", Range(1, 64)) = 1
//Noise and wind
_NoiseTexture("Noise texture", 2D) = "white" {}
_WindTexture("Wind texture", 2D) = "white" {}
_WindStrength("Wind strength", float) = 0
_WindSpeed("Wind speed", float) = 0
[HDR]_WindColor("Wind color", Color) = (1,1,1,1)
//Position and dimensions
_GrassHeight("Grass height", float) = 0
_PositionRandomness("Position randomness", float) = 0
_GrassWidth("Grass width", Range(0.0, 1.0)) = 1.0
//Grass blades
_GrassBlades("Grass blades per triangle", float) = 1
_MinimunGrassBlades("Minimum grass blades per triangle", float) = 1
_MaxCameraDistance("Max camera distance", float) = 10
//Light stuff
[Toggle(IS_LIT)]
_IsLit("Is lit", float) = 0
_RimPower("Rim power", float) = 1
[HDR]_TranslucentColor("Translucent color", Color) = (1,1,1,1)
//Grass trample
_GrassTrample("Grass trample (XYZ -> Position, W -> Radius)", Vector) = (0,0,0,0)
_GrassTrampleOffsetAmount("Grass trample offset amount", Range(0, 1)) = 0.2
}
SubShader
{
CGINCLUDE
#include "UnityCG.cginc"
//Downloaded from Catlike Coding: https://catlikecoding.com/unity/tutorials/advanced-rendering/tessellation/
#include "CustomTessellation.cginc"
#include "Autolight.cginc"
struct appdata
{
float4 vertex : POSITION;
};
struct v2g
{
float4 vertex : POSITION;
};
struct g2f
{
float2 uv : TEXCOORD0;
float4 vertex : SV_POSITION;
float4 col : COLOR;
float3 normal : NORMAL;
unityShadowCoord4 _ShadowCoord : TEXCOORD1;
float3 viewDir : TEXCOORD2;
};
fixed4 _Color;
sampler2D _GradientMap;
sampler2D _NoiseTexture;
float4 _NoiseTexture_ST;
sampler2D _WindTexture;
float4 _WindTexture_ST;
float _WindStrength;
float _WindSpeed;
fixed4 _WindColor;
float _GrassHeight;
float _GrassWidth;
float _PositionRandomness;
float _GrassBlades;
float _MaxCameraDistance;
float _MinimunGrassBlades;
float4 _GrassTrample;
float _GrassTrampleOffsetAmount;
g2f GetVertex(float4 pos, float2 uv, fixed4 col, float3 normal) {
g2f o;
o.vertex = UnityObjectToClipPos(pos);
o.uv = uv;
o.viewDir = WorldSpaceViewDir(pos);
o.col = col;
o._ShadowCoord = ComputeScreenPos(o.vertex);
o.normal = UnityObjectToWorldNormal(normal);
#if UNITY_PASS_SHADOWCASTER
o.vertex = UnityApplyLinearShadowBias(o.vertex);
#endif
return o;
}
float random (float2 st) {
return frac(sin(dot(st.xy,
float2(12.9898,78.233)))*
43758.5453123);
}
v2g vert (appdata v)
{
v2g o;
o.vertex = v.vertex;
return o;
}
//3 + 3 * 15 = 48
[maxvertexcount(48)]
void geom(triangle v2g input[3], inout TriangleStream<g2f> triStream)
{
g2f o;
float3 normal = normalize(cross(input[1].vertex - input[0].vertex, input[2].vertex - input[0].vertex));
int grassBlades = ceil(lerp(_GrassBlades, _MinimunGrassBlades, saturate(distance(_WorldSpaceCameraPos, mul(unity_ObjectToWorld, input[0].vertex)) / _MaxCameraDistance)));
for (uint i = 0; i < grassBlades; i++) {
float r1 = random(mul(unity_ObjectToWorld, input[0].vertex).xz * (i + 1));
float r2 = random(mul(unity_ObjectToWorld, input[1].vertex).xz * (i + 1));
//Random barycentric coordinates from https://stackoverflow.com/a/19654424
float4 midpoint = (1 - sqrt(r1)) * input[0].vertex + (sqrt(r1) * (1 - r2)) * input[1].vertex + (sqrt(r1) * r2) * input[2].vertex;
r1 = r1 * 2.0 - 1.0;
r2 = r2 * 2.0 - 1.0;
float4 pointA = midpoint + _GrassWidth * normalize(input[i % 3].vertex - midpoint);
float4 pointB = midpoint - _GrassWidth * normalize(input[i % 3].vertex - midpoint);
float4 worldPos = mul(unity_ObjectToWorld, pointA);
float2 windTex = tex2Dlod(_WindTexture, float4(worldPos.xz * _WindTexture_ST.xy + _Time.y * _WindSpeed, 0.0, 0.0)).xy;
float2 wind = (windTex * 2.0 - 1.0) * _WindStrength;
float noise = tex2Dlod(_NoiseTexture, float4(worldPos.xz * _NoiseTexture_ST.xy, 0.0, 0.0)).x;
float heightFactor = noise * _GrassHeight;
triStream.Append(GetVertex(pointA, float2(0,0), fixed4(0,0,0,1), normal));
float4 newVertexPoint = midpoint + float4(normal, 0.0) * heightFactor + float4(r1, 0.0, r2, 0.0) * _PositionRandomness + float4(wind.x, 0.0, wind.y, 0.0);
float3 trampleDiff = mul(unity_ObjectToWorld, newVertexPoint).xyz - _GrassTrample.xyz;
float4 trampleOffset = float4(float3(normalize(trampleDiff).x, 0, normalize(trampleDiff).z) * (1.0 - saturate(length(trampleDiff) / _GrassTrample.w)) * random(worldPos), 0.0) * noise;
newVertexPoint += trampleOffset * _GrassTrampleOffsetAmount;
float3 bladeNormal = normalize(cross(pointB.xyz - pointA.xyz, midpoint.xyz - newVertexPoint.xyz));
triStream.Append(GetVertex(newVertexPoint, float2(0.5, 1), fixed4(1.0, length(windTex), 1.0, 1.0), bladeNormal));
triStream.Append(GetVertex(pointB, float2(1,0), fixed4(0,0,0,1), normal));
triStream.RestartStrip();
}
for (int i = 0; i < 3; i++) {
triStream.Append(GetVertex(input[i].vertex, float2(0,0), fixed4(0,0,0,1), normal));
}
}
ENDCG
Pass
{
Tags { "RenderType"="Opaque" "LightMode" = "ForwardBase" }
Cull Off
CGPROGRAM
#pragma vertex vert
#pragma geometry geom
#pragma fragment frag
#pragma hull hull
#pragma domain domain
#pragma target 4.6
#pragma multi_compile_fwdbase
#pragma shader_feature IS_LIT
#include "Lighting.cginc"
float _RimPower;
fixed4 _TranslucentColor;
fixed4 frag (g2f i) : SV_Target
{
fixed4 gradientMapCol = tex2D(_GradientMap, float2(i.col.x, 0.0));
fixed4 col = (gradientMapCol + _WindColor * i.col.g) * _Color;
#ifdef IS_LIT
float light = saturate(dot(normalize(_WorldSpaceLightPos0), i.normal)) * 0.5 + 0.5;
fixed4 translucency = _TranslucentColor * saturate(dot(normalize(-_WorldSpaceLightPos0), normalize(i.viewDir)));
half rim = pow(1.0 - saturate(dot(normalize(i.viewDir), i.normal)), _RimPower);
float shadow = SHADOW_ATTENUATION(i);
col *= (light + translucency * rim * i.col.x ) * _LightColor0 * shadow + float4( ShadeSH9(float4(i.normal, 1)), 1.0) ;
#endif
return col;
}
ENDCG
}
Pass
{
Tags {
"LightMode" = "ShadowCaster"
}
CGPROGRAM
#pragma vertex vert
#pragma geometry geom
#pragma fragment fragShadow
#pragma hull hull
#pragma domain domain
#pragma target 4.6
#pragma multi_compile_shadowcaster
float4 fragShadow(g2f i) : SV_Target
{
SHADOW_CASTER_FRAGMENT(i)
}
ENDCG
}
}
}
```

## Properties

Most of the properties in the shader share the exact same purpose the did in the shader of [the first part](https://halisavakis.com/my-take-on-shaders-grass-shader-part-i/), so I’ll just be covering the new ones:

| Name | Purpose |
|---|---|
| _TessellationUniform | Determines the amount of tessellation on the mesh. |
| _IsLit | Toggles the “IS_LIT” keyword which determines whether or not lighting and shadow receiving will be applied on the grass. |
| _RimPower | Adjusts the size of the fresnel/rim mask on the grass blades. |
| _TranslucentColor | The HDR color that’s being added to the grass blades due to translucency. |
| _GrassTrample | A 4D vector describing the position (XYZ components) and radius (W component) of the grass-trampling object. |
| _GrassTrampleOffsetAmount | The amount the grass blades will be offset when inside the radius of the grass-trampling object. |

### The in-between stuff

Starting up, in lines 46 and 48 I have to include 2 cginc files: the one for the tessellation (downloaded from [this tutorial](https://catlikecoding.com/unity/tutorials/advanced-rendering/tessellation/) by Catlike Coding) and the “Autolight.cginc” which is needed for some information around shadow receiving and it’s a built-in .cginc file, so you don’t have to add it manually like the first one.

Similarly to the first part, the appdata struct doesn’t really need to hold a lot of info for us, just the vertex position. The “v2g” struct stays the same too, passing just the vertex position to the geometry shader.

The “g2f” struct, however, has some additional fields:

- The “normal” field which will hold the normal vector we calculate for each new vertex
- The “_ShadowCoord” field which is needed to calculate the shadow attenuation
- The “viewDir” which holds the view direction vector

After that, I redeclare the properties (except for some that are needed for the lighting, so there’s no need to redeclare them in the CGINCLUDE block).

As I mentioned in the previous tutorial, this shader follows a different structure: firstly there’s a CGINCLUDE block that holds the vertex and geometry shaders and all the necessary structs, and then there are 2 passes: one for the color and another one for the shadow casting. While in the first part there wasn’t much of a reason to have that structure, here it’s quite useful, because we need the vertex and geometry methods in both passes, and if we didn’t follow that structure we’d have to rewrite them in both passes (or use an external .cginc file).

The “GetVertex” method in lines 92-104 also got some more stuff: Firstly, in line 96I calculate the view direction and store it in the local g2f object and in line 98 I also store the screen position of the vertex. Then, in line 99 I store the vertex’s normal, after I convert it from object space to world space. Finally there’s the weird block in lines 100-102. This one says that only during the shadow casting pass, the “UnityApplyLinearShadowBias” macro will be called for the vertex clip position. This helps a lot with shadow bias artifacts on the grass blades, which look like some annoying color banding.

In lines 106-110 there’s also the boilerplate random method, same as before.

I won’t have a separate section for the vertex method because it’s the same as before and it’s still sadly plain: just passing the vertex position to the struct for the geometry shader.

### The geometry shader

I won’t go into too much detail here, because a solid 90% is the same as before. I made sure that every line is the same and in the same position as the unlit shader, so the changes actually start from line 153.

One thing to note, though, is that now at line 149 I also pass the existing normal vector to the “GetVertex” method for the first point of the new triangle.

There I calculate the direction towards which the grass blade should be offset, by subtracting the position of the grass trampling object (stored in the xyz components of _GrassTrample) from the world-space position of the grass blade tip point.

The trample offset is then calculated (in line 154) as the normalized result of line 153 in the x and z axes, multiplied by the distance from the center, so that the effect is not applied if the blades are further away from the trampling object. The offset is also multiplied by a random number for some variation, and the whole thing is also multiplied by the noise for additional variation.

In line 156 the offset is added to the position of the tip point. Then, in line 157 I calculate the normals for the tip point using the method I mentioned above: getting the normalized cross product of the vector formed by the 2 base points and the vector formed by the midpoint and tip point.

After that, in line 159 I append the tip point and in line 161 I append the second vertex of the point and, in line 163, I make sure to restart the triangle strip.

Finally, in lines 166-168 I append the original vertices of the face to the stream, using the original normal vector.

### Fragment shader pass

In line 173 starts the actual pass that returns the color of the grass and applies the lighting and shading. Before the fragment shader, however, there’s a bunch of other important stuff.

First, in line 175 it’s important to add the ” “LightMode” = “ForwardBase” ” tag, in order to have the shadow attenuation work. In line 176 I also make sure to turn the culling off so we can see all the grass blades.

In lines 178-185 there’s a bunch of #pragma directives. The first fiveassign the vertex, geometry, fragment, hull and domain shaders to the corresponding methods. Don’t worry about the whereabouts of the “hull” and “domain” methods, they’re in the “CustomTessellation.cginc” file.

The “#pragma target 4.6” helps with the support of the geometry shader, while the “#pragma multi_compile_fwdbase” is needed for the shadow receiving.

Finally, there’s the “#pragma shader_feature IS_LIT” directive which adds a variant to the shader and uses the “IS_LIT” keyword to toggle between a lit and unlit configuration.

Also, in line 187 I’m including “Lighting.cginc” (also built-in, so no manual installation needed) which is needed for some lighting information I’m using. In lines 189-190 I redeclare the properties I didn’t add in the CGINCLUDE block, since I’ll be using them in this pass only.

### The fragment shader

Here is where all the coloring and shading is applied. Lines 194 and 195 are the same as the first part, still applying color based on a gradient map, the wind and the “_Color” property.

Moving on to the lit 🔥 block, in line 197 I do a simple Half-Lambert calculation by getting the dot product of the directional light’s direction and the world-space normal vector, which I then multiply by 0.5 and add 0.5 to it. This is to ensure that if the grass is not directly lit, it won’t be completely dark but have a smoother falloff.

In line 198 I calculate the translucency by multiplying the “_TranslucentColor” property by the dot product of the view direction and the inversed direction of the directional light. Then, in line 199 I calculate the fresnel mask using a pretty standard technique: dot product of the view direction and the normal, subtract that from 1.0 and raise it to a power to control its concentration/power.

In line 200 I get the shadow attenuation and in line 201 I get the result of the Half-Lambert lighting and add the translucency multiplied by the rim and by the red channel of the vertex color to it (so it fades from the top of the blade to the bottom). The result is then multiplied by “_LightColor0” (which will give me the color of the directional light taking the intensity into account too) and by the shadow attenuation calculated above. Then I add the result of the ShadeSH9 method, which will give me the color information of the ambient light and the baked light probes of the scene. The original color is then multiplied by the result of that whole operation and it is then returned in line 203.

### The shadow casting pass

In line 209 starts the pass that takes care of shadow casting. First, in line 211 there’s a special tag for it, ” “LightMode” = “ShadowCaster” ” which marks the pass as a shadow casting pass.

Later, in lines 215-219 I add the same #pragma directives as before, with the only difference that instead of “#pragma fragment frag” I use “#pragma fragment fragShadow” because I’ll be using a different fragment function. It’s important to have the other pragmas though, because the shadow casting pass needs to have the same information about the geometry as the first pass, so that it can cast the shadows properly.

In line 222 it’s also important to include ” #pragma multi_compile_shadowcaster ” for the shadow casting to actually work.

The fragment shader method is really simple in this pass; it’s just using the “SHADOW_CASTER_FRAGMENT(i)” macro and that’s it, you don’t really need to worry about what that does.

## The grass trampling object

Something I forgot to add is the script that the grass-trampling object should have, in order for the grass to react. It’s a very simple demo script and you could do a lot of different stuff for that purpose but here it is:

```
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
[ExecuteInEditMode]
public class GrassTramplePosition : MonoBehaviour {
public Material material;
public float radius;
public float heightOffset;
void Update() {
material?.SetVector("_GrassTrample", new Vector4(transform.position.x, transform.position.y + heightOffset, transform.position.z, radius));
}
}
```

It’s applied on a specific material, however it would probably be better if it was a global property in order to be applied on all different grass materials. But that’s up to you I guess.

## Unity package

Similarly to the water shader, the grass shader can take a fair amount of tweaking to have something nice looking, so I’ll also be providing a unity package with a small demo to get you started:

## Conclusion

This grass shader can produce some really cool-looking results, however my approach might not be the most ideal one. Geometry shaders in general are infamous for their not-so-great performance, and this one in particular is not very versatile as it doesn’t have any feature that allows you to have grass in specific areas instead of the whole mesh. Plus, geometry shaders don’t really work on mobile and Mac (as far as I know), so they’re even less versatile.

But that’s not really the point. The point is to have fun with this different type of shader and possibly apply whatever you got out of it to a more solid implementation (with compute shaders for example).

I hope you have as much fun with this one as I did!

See you in the [next one](https://halisavakis.com/my-take-on-shaders-cel-shading/)! 😀

## Comments

Hello Harry, thank you for sharing your amazing work!

Is it possible to use your grass shader on a terrain? How would you do this?

Author

Hi! Yeah, it is quite possible, you just need to go to the terrain setting and instead of the default standard terrain material you can use a custom one with the grass shader on it. The problem with the current setup is that you can’t really define areas where there’s no grass easily. Also, depending on the settings it can get pretty heavy when applied in a whole terrain, so I’d keep an eye out for that too ^^”