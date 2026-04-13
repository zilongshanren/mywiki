---
title: 'My take on shaders: Water Shader'
url: https://halisavakis.com/my-take-on-shaders-water-shader/
published: '2019-09-01'
source_blog: Technically Art – Harry Alisavakis
source_site: https://halisavakis.com
category: graphics
fetched: '2026-04-13'
---

## Patrons

This tutorial post is brought to you by:

erich binder

Djinnlord

## Introduction

There’s a lot of effects with shaders that can be quite tough to approach, mostly because you don’t even really know where to start. These tend to be more connected to physical effects, which is precisely what makes them hard to approach. In real time graphics we don’t always have the luxury of accurate simulations, so we try to approximate an effect as well as we can by using different tricks and hacks, so the degree of fidelity can vary in all the different implementations. One of these effects is a shader for water, which for a lot of people, myself including, is one of the holy grails of shaders, as it’s something a lot of people would need in their game, but the degree of complexity in it’s approach can be quite daunting.

Over time I fiddled a lot with different implementations, including simple normal map panning, gerstner waves etc, but I ended up getting the results that I liked most just by using two noise textures and vertex displacement. I was happy to see that this approach gave me some nice results, because at the same time I figured something out which is quite simple but it was giving me trouble for a long time: normal recalculation.

What I ended up with and what I’m showing in the tutorial is by no means accurate and you can find plenty of different and smarter ways to do what I did. But my main goals for this shader were:

- Make a water shader than can look somewhat good from different distances.
- Make the shader highly adjustable.
- Make the shader work on a plane out of the box, with no other setup.
- Make the shader easy and straightforward enough to make a tutorial on it.

When it comes to the techniques used here, there’s nothing really fancy as you’ll see. So this tutorial shouldn’t really be called “water shader” but something like “height texture-based vertex displacement on distance-based tessellated planes with some depth fading” (not as catchy), since the techniques showed here can be easily transferred for a great range of effects.

Due to the shader not being “smart” enough to calculate a lot of stuff on its own, some manual tweaking will be needed to achieve different settings, so besides the shader, I’m also sharing a little UnityPackage to check the settings I used and play around with them. Do note that the effect won’t work in any SRP though.

## The counter

You’ll figure out what that is in the conclusion section.

IIIIIIIIIIII

## The code

Let’s examine some code:

Shader "Custom/WaterShader"
{
Properties
{
[Header(Smoothness)]
_Smoothness ("Smoothness", Range(0,1)) = 0.5
[Header(Colors)]
_GradientMap("Gradient map", 2D) = "white" {}
_ShoreColor("Shore color", Color) = (1,1,1,1)
_ShoreColorThreshold("Shore color threshold", Range(0, 1)) = 0
[HDR]_Emission("Emission", Color) = (1,1,1,1)
[Header(Tessellation)]
_VectorLength("Vector length", Range(0.0001, 0.2)) = 0.1
_MaxTessellationDistance("Max tessellation distance", float) = 100
_Tessellation("Tessellation", Range(1.0, 128.0)) = 1.0
[Header(Vertex Offset)]
_NoiseTextureA("Noise texture A", 2D) = "white" {}
_NoiseAProperties("Properties A (speedX, speedY, contrast, contribution)", Vector) = (0,0,1,1)
_NoiseTextureB("Noise texture B", 2D) = "white" {}
_NoiseBProperties("Properties B (speedX, speedY, contrast, contribution)", Vector) = (0,0,1,1)
_OffsetAmount("Offset amount", Range(0.0, 1.0)) = 1.0
_MinOffset("Min offset", Range(0.0, 1.0)) = 0.2
[Header(Displacement)]
_DisplacementGuide("Displacement guide", 2D) = "white" {}
_DisplacementProperties("Displacement properties (speedX, speedY, contribution)", Vector) = (0,0,0,0)
[Header(Shore and foam)]
_ShoreIntersectionThreshold("Shore intersection threshold", float) = 0
_FoamTexture("Foam texture", 2D) = "white" {}
_FoamProperties("Foam properties (speedX, speedY, threshold, threshold smoothness)", Vector) = (0,0,0,0)
_FoamIntersectionProperties("Foam intersection properties (intersection threshold, foam threshold, threshold smoothness, cutoff)", Vector) = (0,0,0,0)
[Header(Transparency)]
_TransparencyIntersectionThresholdMin("Transparency intersection threshold min", float) = 0
_TransparencyIntersectionThresholdMax("Transparency intersection threshold max", float) = 0
}
SubShader
{
Tags {"Queue"="Transparent" "IgnoreProjector"="True" "RenderType"="Transparent" "DisableBatching"="True"}
Blend One OneMinusSrcAlpha
ZWrite Off
LOD 200
CGPROGRAM
#pragma surface surf Standard fullforwardshadows vertex:vert tessellate:tessDistance alpha:fade addshadow
#pragma require tessellation tessHW
#include "Tessellation.cginc"
#pragma target 3.0
half _Smoothness;
float _SmoothnessFresnel;
sampler2D _GradientMap;
fixed4 _ShoreColor;
float _ShoreColorThreshold;
fixed4 _Emission;
float _VectorLength;
float _MaxTessellationDistance;
float _Tessellation;
sampler2D _NoiseTextureA;
float4 _NoiseTextureA_ST;
float4 _NoiseAProperties;
sampler2D _NoiseTextureB;
float4 _NoiseTextureB_ST;
float4 _NoiseBProperties;
float _OffsetAmount;
float _MinOffset;
float4 _DisplacementProperties;
sampler2D _DisplacementGuide;
float4 _DisplacementGuide_ST;
float _ShoreIntersectionThreshold;
sampler2D _FoamTexture;
float4 _FoamProperties;
float4 _FoamTexture_ST;
float4 _FoamIntersectionProperties;
float _TransparencyIntersectionThresholdMax;
float _TransparencyIntersectionThresholdMin;
sampler2D _CameraDepthTexture;
struct Input
{
float4 color: Color;
float3 worldPos;
float4 screenPos;
};
float4 tessDistance (appdata_full v0, appdata_full v1, appdata_full v2) {
float minDist = 10.0;
float maxDist = _MaxTessellationDistance;
return UnityDistanceBasedTess(v0.vertex, v1.vertex, v2.vertex, minDist, maxDist, _Tessellation);
}
float sampleNoiseTexture(float2 pos, sampler2D noise, float4 props, float2 scale, float2 displ) {
float value = tex2Dlod(noise, float4(pos * scale + displ + _Time.y * props.xy, 0.0, 0.0));
value = (saturate(lerp(0.5, value, props.z)) * 2.0 - 1.0) * props.w;
return value;
}
float noiseOffset(float2 pos) {
float2 displ = tex2Dlod(_DisplacementGuide, float4(pos * _DisplacementGuide_ST.xy + _Time.y * _DisplacementProperties.xy, 0.0, 0.0)).xy;
displ = ((displ * 2.0) - 1.0) * _DisplacementProperties.z;
float noiseA = sampleNoiseTexture(pos, _NoiseTextureA, _NoiseAProperties, _NoiseTextureA_ST.xy, displ);
float noiseB = sampleNoiseTexture(pos, _NoiseTextureB, _NoiseBProperties, _NoiseTextureB_ST.xy, displ);
return noiseA * noiseB;
}
// Add instancing support for this shader. You need to check 'Enable Instancing' on materials that use the shader.
// See https://docs.unity3d.com/Manual/GPUInstancing.html for more information about instancing.
// #pragma instancing_options assumeuniformscaling
UNITY_INSTANCING_BUFFER_START(Props)
// put more per-instance properties here
UNITY_INSTANCING_BUFFER_END(Props)
float smootherstep(float x) {
x = saturate(x);
return saturate(x * x * x * (x * (6 * x - 15) + 10));
}
float remap(float s) {
return (s + 1.0) / 2.0;
}
void vert(inout appdata_full v) {
float4 v0 = v.vertex;
float4 v1 = v0 + float4(_VectorLength, 0.0, 0.0, 0.0);
float4 v2 = v0 + float4(0.0, 0.0, _VectorLength, 0.0);
float4 screenPos = ComputeScreenPos(UnityObjectToClipPos(v0.xyz));
float depth = LinearEyeDepth(tex2Dlod(_CameraDepthTexture, float4(screenPos.xy / screenPos.w, 0.0, 0.0)));
float diff = smootherstep(saturate((depth - screenPos.w) / _ShoreIntersectionThreshold));
float thresDiff = max(_MinOffset, diff);
float factor = thresDiff * _OffsetAmount;
float vertexOffset = noiseOffset(mul(unity_ObjectToWorld, v0).xz);
v0.y += vertexOffset * factor;
v1.y += noiseOffset(mul(unity_ObjectToWorld, v1).xz) * factor;
v2.y += noiseOffset(mul(unity_ObjectToWorld, v2).xz) * factor;
float3 vn = cross(v2.xyz - v0.xyz, v1.xyz - v0.xyz);
v.normal = normalize(vn);
v.vertex = v0;
v.color = fixed4(remap(vertexOffset).xxxx);
}
void surf (Input IN, inout SurfaceOutputStandard o)
{
//Displacement
float2 displ = tex2D(_DisplacementGuide, IN.worldPos.xz * _DisplacementGuide_ST.xy + _Time.y * _DisplacementProperties.xy).xy;
displ = ((displ * 2.0) - 1.0) * _DisplacementProperties.z;
//Foam
float foamTex = tex2D(_FoamTexture, IN.worldPos.xz * _FoamTexture_ST.xy + displ + sin(_Time.y) * _FoamProperties.xy);
float foam = saturate(foamTex - smoothstep(_FoamProperties.z + _FoamProperties.w, _FoamProperties.z, IN.color.x));
//Depth calculations
float depth = tex2Dproj(_CameraDepthTexture, UNITY_PROJ_COORD(IN.screenPos));
float shoreDepth = smoothstep(0.0, _ShoreColorThreshold, Linear01Depth(depth));
depth = LinearEyeDepth(depth);
float foamDiff = smootherstep(saturate((depth - IN.screenPos.w) / _FoamIntersectionProperties.x));
float shoreDiff = smootherstep(saturate((depth - IN.screenPos.w) / _ShoreIntersectionThreshold));
float transparencyDiff = smootherstep(saturate((depth - IN.screenPos.w) / lerp(_TransparencyIntersectionThresholdMin, _TransparencyIntersectionThresholdMax, remap(sin(_Time.y + UNITY_PI / 2.0)))));
//Shore
float shoreFoam = saturate(foamTex - smoothstep(_FoamIntersectionProperties.y - _FoamIntersectionProperties.z, _FoamIntersectionProperties.y, foamDiff) + _FoamIntersectionProperties.w * (1.0 - foamDiff));
float sandWetness = smoothstep(0.0, 0.3 + 0.2 * remap(sin(_Time.y)), foamDiff);
shoreFoam *= sandWetness;
foam += shoreFoam;
//Colors
o.Albedo = lerp(lerp(fixed3(0.0, 0.0, 0.0), _ShoreColor.rgb, sandWetness), tex2D(_GradientMap, float2(IN.color.x, 0.0)).rgb, shoreDepth) + foam * sandWetness;
o.Emission = o.Albedo * saturate(_WorldSpaceLightPos0.y) * _LightColor0 * _Emission;
//Smoothness
o.Smoothness = _Smoothness * foamDiff;
o.Alpha = saturate(lerp(1.0, lerp(0.5, _ShoreColor.a, sandWetness), 1.0 - shoreDiff) * transparencyDiff);
}
ENDCG
}
FallBack "Diffuse"
}



It looks a lot right now, but most of it is the properties and fields and we’ll examine the rest together.

## Properties

For the first time, I think I’m going to use a table for this one.

| _Smoothness | The glossiness value of the water. I usually have it be 1.0, cause water tends to be s m o o t h. |
| _GradientMap | This is a gradient texture that’s used to color the major part of the water based on its displacement height. The left-most value corresponds to the deeper parts, while the right-most to the highest parts. |
| _ShoreColor | As the water plane intersects with other objects, like the terrain, it will have a different, lighter color which is determined by this property. |
| _ShoreColorThreshold | The threshold for the shore coloring based on linear depth. |
| _Emission | An HDR color property that’s multiplied with the rest of the color. It can be used to boost the colors of the water a bit, but it’s not really necessary. |
| _VectorLength | Used when recalculating the normals so I won’t go into too much detail now as to what it does. Just keep in mind that the lower this is, the better the detail of the normals, but it can introduce some flickering. The value is a variable because depending on the scale of the object more or less detail might be needed. |
| _MaxTessellationDistance | The tessellation used here is distance-based, so vertices that are further away from the camera won’t be as tessellated, which helps with performance and visual clarity sometimes. This value determines the point where the tessellation amount starts getting lower. |
| _Tessellation | Determines how tessellated the object will be.It’s not a great idea to crank this up to a large number, but that depends on how much detail you want. |
| _NoiseTextureA | The first noise texture to use for the vertex displacement. |
| _NoiseAProperties | A 4D vector containing properties of the noise texture: x -> the texture’s speed in the X axis y -> the texture’s speed in the Y axis z -> the grayscale contrast of the texture, to adjust abrupt value changes w -> the texture’s contribution to the vertex displacement |
| _NoiseTextureB | The second noise texture to use for the vertex displacement. |
| _NoiseBProperties | Same as “_NoiseAProperties”, but for the second noise. |
| _OffsetAmount | This is a value going from 0 to 1 that defines the amount of vertex offset happening on the object for both noise textures. It’s basically a global controller for the vertex offset. Also useful to adjust the vertex offset when scaling up the water mesh, as that will exaggerate the vertex displacement. |
| _MinOffset | When intersecting with objects and the terrain, we probably want the waves to stop being so intense, but not completely stop. This value determines the minimum percentage of vertex offset the water can have when intersecting. |
| _DisplacementGuide | The texture to use for the displacement when sampling the other textures. |
| _DisplacementProperties | A 4D vector containing settings for the displacement: x -> The texture’s speed in the X axis y -> The texture’s speed in the Y axis z -> The amount of the displacement w -> Unused, could be anything you’d like, maybe a separate contribution only for one of the other textures. |
| _ShoreIntersectionThreshold | The value determining how large the intersection area will be with other objects, like the terrain. |
| _FoamTexture | The texture for the foam for both the top of the waves and for the intersection with objects. You can use different ones for each use case if you want. |
| _FoamProperties | A 4D vector containing settings for the foam that’s on top of the waves:x -> the foam texture’s speed on the X axis y -> the foam texture’s speed on the Y axis z -> the height threshold for the foam to appear on the top of the waves w -> the smoothness of the cutoff for the foam on top of the waves Note that the speed here is not linear but the foam is actually doing a bobbing movement going back and forth using a sine wave. |
| _FoamIntersectionProperties | A 4D vector handling the properties of the foam that appears when intersecting with geometry:x -> the intersection threshold of the foam y -> the cutoff value of the foam on the intersection z -> the smoothness of the cutoff w -> an added value to the intersection foam, in case it’s not visible enough |
| _TransparencyIntersectionThresholdMin | The minimum intersection threshold value used for transparency when intersecting with other objects. |
| _TransparencyIntersectionThresholdMax | The maximum intersection threshold value used for transparency when intersecting with other objects. |

This is actually a neat format, I think I’ll keep it for next tutorials too.

## The in-between stuff

Firstly, in lines 46-48 we take care of the transparency stuff. Also, in line 46 I added two more tags: one for ignoring projectors (so if I were to add a projector for caustics for example, the water wouldn’t be affected), and one for disabling batching. Without the “disableBatching” tag, if the water mesh was marked as static and there were other instances of it in the scene, the vertex offset just wouldn’t work.

In line 53 I add some more stuff after the “surface” pragma. Specifically there’s these directives: vertex:vert tessellate:tessDistance alpha:fade addshadow.

- vertex:vert is to declare that we’ll be using a vertex shader named “vert”
- tessellate:tessDistance is to declare that there will be a method called “tessDistance” used for tessellation
- alpha:fade is needed along with the transparency stuff to let the shader know that it’ll use the alpha channel for transparency fade
- addshadow is to change the shadow that the water casts after its vertices are modified

For the tessellation I also needed to add two more directives in lines 54 and 55:

*#pragma require tessellation tessHW*

*#include “Tessellation.cginc”*

In lines 55-94 I redeclare all the properties from the properties field and for each of the samplers I also add the corresponding float4 field with the scaling and offset, so that I can control them through the material inspector. Furthermore, in line 94 I declare the “_CameraDepthTexture” to use for the depth operations.

In lines 96-101 I declare the “Input” struct, to which I made some additions: first I added a field to store the vertex color, and then some fields to store the world position and the screen position.

## Outside methods

There are some methods besides the vertex shader and the “surf” function that are provide some specific functionality or are made for ease of use.

### tessDistance

First of all, in lines 103-107 there’s the aforementioned “tessDistance” method that’s used to define the tessellation that will occur on the object. This method is pretty boilerplate and you can find more about it and other tessellation methods from [Unity’s official docs](https://docs.unity3d.com/Manual/SL-SurfaceShaderTessellation.html).

### sampleNoiseTexture

Afterwards, in lines 109-113 there’s the “sampleNoiseTexture” method. It’s used for both of the noise textures and as parameters it gets the sampling position, the noise texture, the properties of the noise texture, its scale and the displacement value (so that it won’t have to be calculated more than once).

The method uses “tex2Dlod” to sample the texture, as this will be called in the vertex shader and as UVs it uses the sampling position multiplied by the given scale, and to that I’m adding the displacement value and the value of time multiplied by its speed as specified by the properties vector.

The result is then adjusted based on the contrast value and then multiplied by its contribution before it’s returned.

### noiseOffset

In lines 115-121 I have the “noiseOffset” method which takes care of calculating the displacement and sampling both noise textures using “sampleNoiseTexture”. The results of both calls are then multiplied with each other between returning.

### smootherstep and remap

Finally there are 2 more smaller methods: “smootherstep” and “remap”. “smootherstep” takes a float and maps it to Ken Perlin’s “smootherstep” curve.

“remap” just takes a value from [-1,1] and maps it to the [0,1] range. I had to extract that code because I have some sin calls which needed remapping and didn’t want to have a lot of “(x + 1.0) / 2.0” everywhere.

## The vertex shader

As you can imagine, more than 50% of the magic happens right here, in the vertex shader. And it’s not as large as one would think. The helper functions help with that too. That’s why I just called them “heper” functions.

The tasks of the vertex shader are:

- Displace the vertices according to the provided noise textures
- Recalculate the normal vector for each displaced vertex
- Calculate where the object intersects with other objects so that it can reduce the vertex displacement there
- Pass the vertex displacement to the vertex colors so that it can be used in the “surf” function

In lines 142-144 I declare some local vectors and to them I store the object space position of the current vertex, the object space position displaced by “_VectorLength” along the vertex’ tangent vector and the object space position displaced by “_VectorLength” along the vertex’ bitangent vector. As mentioned, the smaller “_VectorLength” is, the more detail the normals will have.

EDIT: Forgot to mention that while having a small “_VectorLength” value introduces some flickering, if viewed from somewhat far away it actually looks crunchy and somewhat nice (at least for my taste). From up close though, it doesn’t look great. You could actually have a “_VectorLengthMax” and a “_VectorLengthMin” value and interpolate between the two based on camera distance. Just a thought.

In lines 146-148 I calculate the intersection of the water object with other objects so that I get a float value from 0 to 1 representing the area of the object that is intersecting. That value is 0 when it’s closer to the object that it’s intersecting and 1 as it gets further away.

As I mentioned, we don’t want to completely turn the vertex displacement off, so in line 149 I use “max” to clamp the intersection value between “_MinOffset” and 1.

Then, in line 150 I calculate the vertex displacement factor which is just the clamped intersection value multiplied by “_OffsetAmount”.

The actual vertex displacement is being calculated in lines 152-156. For the vertex’ object space position, I use “noiseOffset” to calculate the vertex offset and store it in a local variable called “vertexOffset” so that I can use it in the vertex colors later on. Do note that here I’m passing the world space position of the vertex (by multiplying the object space position with “unity_ObjectToWorld”) to the “noiseOffset” method. This is to ensure that the displacement occurs in world space, so different “water tiles” can be placed next to each other and work seamlessly.

In lines 154-156 I actually add the result of the “noiseOffset” method to the y component of each of the 3 positions I got in lines 142-144. It’s very important to note that each vector passes itself to the “noiseOffset” as the sampling position (after it’s converted to world space coordinates). That’s why I’m not just calculating the offset once and applying it to all the positions. This is basically the key to recalculating the normals.

In lines 158-159 the actual normal recalculation and assignment happens. Since we have the original position, the position offset along the tangent vector and the position offset along the bitangent vector, we can get the tangent and bitangent vectors and the new normal will be the cross product of the two. This is what happens in line 158, and in line 159 it’s assigned to “v.normal” after it’s normalized.

Finally, in line 161 the new position is assigned to “v.vertex” and the “vertexOffset” from before is assigned to “v.color” (after it’s remapped because “noiseOffset” returns values from -1 to 1) for us to use later.

## The surface shader

This is where the rest of the magic happens. And I know it looks weird and complicated but trust me, there’s some “logic” behind all of this. Let’s go through it step by step.

### Displacement

Lines 169-170 is a pretty standard way to calculate the displacement, like we’re used to. It’s the same thing I’m doing in the “noiseOffset” method. Keep in mind, that this and all other textures are all sampled “biplanarly” in world space, to keep the whole thing tiling and to keep it consistent with the world space sampled height textures used for the vertex displacement.

### Foam texture

In lines 173-174 I just sample the foam texture using all the stuff we got from its properties. As UVs I use the x and z components of the world space position multiplied by the scaling from “_FoamTexture_ST”. To that I add the displacement value and the time **in a sine function** multiplied by the texture’s speed in both axes. The reason for the sine function instead of just “_Time.y” is to have a bobbing front-back movement. If you want it to be continuous, just remove the sin function.

In line 174 I use the vertex color to take the vertex displacement value and use it with a smoothstep using the z and w components of the “_FoamProperties” property.

### Depth calculations

In lines 177-182 there’s the calculations needed for everything that has to do with depth and intersection. Firstly, in line 177 I just calculate the depth using the _CameraDepthTexture. Before using “LinearEyeDepth”on it, in line line 178 I calculate the linear depth going from 0 to 1 (with “Linear01Depth) and use it on a smoothstep to smoothly clamp it based on “_ShoreColorThreshold”.

In line 179 I use “LinearEyeDepth” on the original depth and then use the modified “depth” variable to calculate the intersections in lines 180-182. The process of getting the intersection value is pretty standard (we’ve also seen it with soft blending in the [vfx master shader](https://halisavakis.com/my-take-on-shaders-vfx-master-shader-part-iii/)). The only thing worth noting here is that I use “smootherstep” on the result for a nicer blending, and that in line 182 I don’t use a single intersection threshold value, but rather lerp between ” _TransparencyIntersectionThresholdMin ” and ” _TransparencyIntersectionThresholdMax ” based on a value that ping-pongs between 0 and 1 using a sine function. The reason for that is to give the impression of the sand-wetness effect, as it fades in and out over time.

### The shore

I keep referring to this part as the “shore” but it’s basically every intersection with any object, including the terrain. But let’s just say that this is for just the shore for now, it makes more sense that way.

Initially, in line 185 I get the foam on the shore by using the “foamTex” from line 173 and using the intersection value of the foam (“foamDiff”) with the “_FoamIntersectionProperties” to determine the amount of the foam that will appear on the edge of the intersections. To that value I also add the value “_FoamIntersectionProperties.w” multiplied by the inverted “foamDiff” to contribute only to the area of the intersection foam. If you play around with these numbers, their purpose will be more apparent.

In line 186 I perform the necessary calculations for the sand wetness effect. The whole line was a product of trial and error, hence the magic numbers there. The core concept is that I mask out a part of the intersection foam area to use as the wet sand area. I also use a sin(_Time.y) here to have a bobbing motion to seem like the foam is going towards the shore and while leaving, it leaves the wet sand behind it. It’s not perfect, but it helps with blending the water with the land a bit better.

In line 187 I multiply the sand-wetness mask with the shoreFoam so that the foam is not added to that area. Finally, in line 188 I add the final shore foam to the previous foam, to add it all together in the next section.

In lines 191-192, I handle the overall coloring of the water. The final color results from:

- The gradient map which gets mapped based on the vertex displacement
- The black color of the sand wetness
- The shore color which is based on the linear depth
- The added foam

The albedo in line 191 is calculated with all those in mind:

- The gradient map is being sampled using the vertex color
- The shore color is being calculated by lerping between black and “_ShoreColor” using the sand wetness value as the lerping factor
- The shore color and the gradient map colors are blended using “shoreDepth” as the lerping factor
- The “foam” value is then added on top of all that, after it’s being multiplied by “sandWetness”, so that we don’t have any foam on top of the wet sand effect.

In line 192 I calculate the emission color by using the albedo color, multiplying it by the saturated y position of the directional light (so it’s 1 when it’s completely on top and 0 when it’s on the bottom), multiplying that by the light color and, finally multiplying the whole thing by the extra emission value from the “_Emission” property.

There are definitely better ways to deal with the lighting, like a custom lighting model using SSS (like I showed in [the previous tutorial](https://halisavakis.com/my-take-on-shaders-simple-subsurface-scattering/)), but this is a simple enough for various effects.

### Smoothness and alpha

The smoothness value is assigned in line 195 where I use the “_Smoothness” value multiplied by “shoreDiff” to not make the foam and sand wetness as smooth as the rest of the water.

The alpha of the water is also calculated with a kinda weird way. First, I lerp from 0.5 (the sand wetness alpha, consider it another “magic number”) to the alpha value of “_ShoreColor” using “sandWetness” as the lerping factor. The result is then blended with 1.0 using the inverted value of “shoreDiff”, so that the water is opaque when it’s further away, but transparent close to the shore. The whole thing is then multiplied by the transparency intersection value so that it fades more when closer to the shore (or other objects 👀).

## Assets

Here’s the assets and values that I mostly used for my water:

### Noise textures

![](../../assets/78f01a5305be83e6.png)

![](../../assets/c92a0973d54e41be.png)

### Displacement

![](../../assets/d574e3e1415dc752.png)

### Foam

![](../../assets/c1ac0a7eef58aef3.png)

### Gradient map

![](../../assets/0251b1da8bba1967.png)

Forgot to mention that probably the best way to create gradient map textures for this shader is using a tool like [the gradient map tool I showed in a previous tutorial](https://halisavakis.com/my-take-on-shaders-gradient-mapper/), especially since it allows previewing in real time.

### Material settings

Here’s the material setup I use:

![](../../assets/5ca18c189ae165ab.png)

### Unity package

I made a reaaaaaaaally quick scene to demonstrate how I’ve set up my water and you can use it as a playground to familiarize yourselves with the properties and whatnot:

In the package you’ll also find another shader that adds caustics based on world-space height. Consider it a freebie, even though I neglected to cover it in this post. I still hope it can be useful. The whole caustics technique was very much inspired by [this tweet](https://twitter.com/kolyaTQ/status/1165251296720576512?s=20) by [FLOG](https://twitter.com/kolyaTQ).

## Conclusion

There’s a lot of decisions to take when making a shader like this, and a bunch of different approaches. This one worked for what I wanted, but it might not work for what you want. Nevertheless, it’s a fun thing to experiment with, and there are some nice takeaways, like the normal recalculation and all the depth stuff.

Just to show you how many times you can fiddle and experiment with a shader like that, every time I was changing something in the shader *while* writing this post, I increased the counter above. That’s 12 times.

I hope you’ll have fun with this shader as much as I did, and that you’ll make some pretty neat stuff with it, which I’d love to see!

For now, I’ll see you in the [next one](https://halisavakis.com/my-take-on-shaders-geometry-shaders/)!