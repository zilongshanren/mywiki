---
title: Stylised Grass with Shaders in URP
url: https://danielilett.com/2021-08-24-tut5-17-stylised-grass/
author: Daniel Ilett
published: '2021-08-24'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

*The Legend of Zelda: Breath of the Wild* is one of my favourite games of all time. While playing, I was captivated by the gorgeous landscapes, and I’ve always wanted to recreate that lush grass effect in Unity. Now that Nintendo has blessed us with a few more scraps of information about the sequel and pushed BotW back into everyone’s minds, now’s a good time to revisit the grass effect I’ve longed to make. We’re going unlock some hidden shader knowledge to make it in Universal Render Pipeline.

This shader is based heavily on the work of other talented people, so I’ll be leaving tons of citations for further reading in this article, alongside a [GitHub repo](https://github.com/daniel-ilett/shaders-botw-grass) for the full project. If you need a quick refresher on shaders in URP, I’ve got [an article](https://danielilett.com/2021-04-02-basics-3-shaders-in-urp/) for that!

This tutorial is aimed at people who have at least some experience with Shader Graph. We are using Unity 2020.2 and URP/Shader Graph 10.2.2.

Hang out with me and other shader enthusiasts over on [Discord](https://danielilett.com/(https:/discord.gg/tPQEUwPpb3)) and share what you’re working on!

# The URP Base Shader

BotW’s grass effect can be made using geometry shaders. As opposed to a vertex shader, which just messes with vertices passed to it, a geometry shader can actually create new vertices - and that’s how we’ll add new blades of grass. But we need something to start with.

I’m starting with an unlit shader file (Create -> Shader -> Unlit Shader), but most of the boilerplate won’t make the cut. We’ll remove everything inside the `SubShader`

part of the file. It should now look like this:

```
Shader "Custom/BotWGrass"
{
Properties
{
_MainTex ("Texture", 2D) = "white" {}
}
SubShader
{
}
}
```


We’ll make our shader compatible with URP, so it’ll look a bit different to the steps you might be used to when making shaders for the built-in pipeline - [Cyan’s URP shader tutorial](https://www.cyanilux.com/tutorials/urp-shader-code/) explains the steps required clearly. I’ll give an overview of the key bits here.

We’ll be including a lot of shader variables that can be tweaked in the material Inspector, which need to be included in the `Properties`

section. I’ll explain what each one does as we go.

```
Properties
{
_BaseColor("Base Color", Color) = (1, 1, 1, 1)
_TipColor("Tip Color", Color) = (1, 1, 1, 1)
_BladeTexture("Blade Texture", 2D) = "white" {}
_BladeWidthMin("Blade Width (Min)", Range(0, 0.1)) = 0.02
_BladeWidthMax("Blade Width (Max)", Range(0, 0.1)) = 0.05
_BladeHeightMin("Blade Height (Min)", Range(0, 2)) = 0.1
_BladeHeightMax("Blade Height (Max)", Range(0, 2)) = 0.2
_BladeSegments("Blade Segments", Range(1, 10)) = 3
_BladeBendDistance("Blade Forward Amount", Float) = 0.38
_BladeBendCurve("Blade Curvature Amount", Range(1, 4)) = 2
_BendDelta("Bend Variation", Range(0, 1)) = 0.2
_TessellationGrassDistance("Tessellation Grass Distance", Range(0.01, 2)) = 0.1
_GrassMap("Grass Visibility Map", 2D) = "white" {}
_GrassThreshold("Grass Visibility Threshold", Range(-0.1, 1)) = 0.5
_GrassFalloff("Grass Visibility Fade-In Falloff", Range(0, 0.5)) = 0.05
_WindMap("Wind Offset Map", 2D) = "bump" {}
_WindVelocity("Wind Velocity", Vector) = (1, 0, 0, 0)
_WindFrequency("Wind Pulse Frequency", Range(0, 1)) = 0.01
}
```


Those variables need to be declared a second time in the HLSL shader code inside a special `CBUFFER`

, which stands for ‘constant buffer’. You can use the same types for the variables as you’d usually use for built-in shader code.

```
CBUFFER_START(UnityPerMaterial)
float4 _BaseColor;
float4 _TipColor;
sampler2D _BladeTexture;
float _BladeWidthMin;
float _BladeWidthMax;
float _BladeHeightMin;
float _BladeHeightMax;
float _BladeBendDistance;
float _BladeBendCurve;
float _BendDelta;
float _TessellationGrassDistance;
sampler2D _GrassMap;
float4 _GrassMap_ST;
float _GrassThreshold;
float _GrassFalloff;
sampler2D _WindMap;
float4 _WindMap_ST;
float4 _WindVelocity;
float _WindFrequency;
float4 _ShadowColor;
CBUFFER_END
```


We’ll be using content from Unity’s premade `Core`

and `Lighting`

shader files, so we’ll include those.

```
#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Lighting.hlsl"
```


We’ll also start with two structs called `VertexInput`

and `VertexOutput`

which funnel data to and from the vertex shader respectively. They’ll just contain the vertex position, normal vector, tangent vector and UV coordinates.

```
struct VertexInput
{
float4 vertex : POSITION;
float3 normal : NORMAL;
float4 tangent : TANGENT;
float2 uv : TEXCOORD0;
};
struct VertexOutput
{
float4 vertex : SV_POSITION;
float3 normal : NORMAL;
float4 tangent : TANGENT;
float2 uv : TEXCOORD0;
};
```


Finally, we’ll add a `Pass`

and create a fragment shader which just outputs white, and bam! We’ve got ourselves and skeleton shader to work with. Spooky. Also remember to set `Cull Off`

so that both sides of the grass geometry get drawn and set the correct `Tags`

.

```
SubShader
{
Tags
{
"RenderType" = "Opaque"
"Queue" = "Geometry"
"RenderPipeline" = "UniversalPipeline"
}
LOD 100
Cull Off
...
}
```


From this point onwards, the technique for creating the grass is heavily based on [Roystan’s fantastic article](https://roystan.net/articles/grass-shader.html) on the subject. It’s a wonderful resource so give it a read once you’re done here!

# Geometry Shaders

A geometry shader can add new vertices. It takes every vertex output by the vertex shader, then using that as a basis, it can add new vertices of its own - we’re going to create a single triangle pointing upwards at every vertex as a starting point.

![We'll be sprouting new grass blades from each vertex. Adding geometry.](../../assets/ccff16b05dd9c203.jpg)

*We’ll be sprouting new grass blades from each vertex.*

Our geometry shader outputs slightly different data than the vertex shader, so we’ll make a new struct called `GeomData`

which contains the vertex position and UVs, same as before, plus the world space position. We don’t need it just yet, but we’re sowing seeds for later.

```
struct GeomData
{
float4 pos : SV_POSITION;
float2 uv : TEXCOORD0;
float3 worldPos : TEXCOORD1;
};
```


The geometry shader, which is a function called `geom`

, which will take in a single `point`

, or vertex, and a `TriangleStream`

containing that `GeomData`

struct we just made. Think of this as a big list of vertex data which we’ll add to throughout the geometry shader. We also need to specify the maximum number of vertices the geometry shader can output for every input vertex - we can start off with a `maxvertexcount`

of 3, which corresponds to one triangle.

```
[maxvertexcount(3)]
void geom(point VertexOutput input[1], inout TriangleStream<GeomData> triStream)
{
}
```


Now we’ll add that triangle. I’ll jump the gun a bit and create a function called `TransformGeomToClip`

just above the `geom`

function, because it’ll save us time later. This function will take a root position for the grass blade, then will let us add an offset with a transformation matrix applied to the offset. This will eventually let us rotate and bend the grass blades in all kinds of ways, and it’s a convenient way of doing all the transformation operations in one place while bundling it into a `GeomData`

instance, which gets output.

```
GeomData TransformGeomToClip(float3 pos, float3 offset, float3x3 transformationMatrix, float2 uv)
{
GeomData o;
o.pos = TransformObjectToHClip(pos + mul(transformationMatrix, offset));
o.uv = uv;
o.worldPos = TransformObjectToWorld(pos + mul(transformationMatrix, offset));
return o;
}
```


For that function to work the way we want it to, we need to change our vertex shader so that it doesn’t apply the object-space-to-clip-space transformation - instead, the position and normal need to be transformed from object to world space. The new vertex shader will be called `geomVert`

, and we can update the vertex shader declaration in the `Pass`

accordingly.

```
VertexOutput geomVert (VertexInput v)
{
VertexOutput o;
o.vertex = float4(TransformObjectToWorld(v.vertex), 1.0f);
o.normal = TransformObjectToWorldNormal(v.normal);
o.tangent = v.tangent;
o.uv = TRANSFORM_TEX(v.uv, _GrassMap);
return o;
}
```


Back in the `geom`

function, we’ll create a 3x3 identity matrix, then make three vertices using the `TransformGeomToClip`

function we just wrote. Each one is passed into `triStream.Append`

, which adds them to that big list of vertex data I mentioned (the one which was passed into `geom`

in the first place). `triStream.RestartStrip`

can be used to end this triangle strip and start a new one, but we’ll always create exactly one strip, so this isn’t required.

```
[maxvertexcount(3)]
void geom(point VertexOutput input[1], inout TriangleStream<GeomData> triStream)
{
float3 pos = input[0].vertex.xyz;
float3 normal = input[0].normal;
float3 tangent = input[0].tangent;
float3x3 transformationMatrix = float3x3
(
1, 0, 0,
0, 1, 0,
0, 0, 1
);
triStream.Append(TransformGeomToClip(pos, float3(-0.1f, 0.0f, 0.0f), transformationMatrix, float2(0.0f, 0.0f)));
triStream.Append(TransformGeomToClip(pos, float3( 0.0f, 0.0f, 0.0f), transformationMatrix, float2(1.0f, 0.0f)));
triStream.Append(TransformGeomToClip(pos, float3( 0.0f, 0.5f, 0.0f), transformationMatrix, float2(0.5f, 1.0f)));
triStream.RestartStrip();
}
```


In the `Pass`

, we’ll add `#pragma require geometry`

and `#pragma geometry geom`

to activate the geometry shader. Now let’s see the geometry shader in action!

![Nobody will notice the difference, right? First geometry shader.](../../assets/9887ad6ab42541bc.jpg)

*Nobody will notice the difference, right?*

Our grass looks almost the same as *Breath of the Wild*! Okay, maybe not - there’s still a lot to do. Now that we’ve got our geometry shader working and grass blades sprouting from each vertex of the plane mesh, let’s breathe life into them with some color.

# Color Gradients and UVs

The `TransformGeomToClip`

function did more than just set the position of each grass blade - it also set the UV coordinates for each vertex, and we’ll use those to add much-needed texture and a color gradient. *Breath of the Wild* actually doesn’t add much texture by the looks of it, so the addition of a texture is a bit of a stylistic tweak I chose to add.

In the `Properties`

, I added a `_BaseColor`

and `_TipColor`

for the colour gradient and a `_BladeTexture`

to give each blade a bit of shading in the centre.

![A bit of shading in the centre will look slightly like a grass blade's stem. Blade texture.](../../assets/a180b83483eaf35f.jpg)

*A bit of shading in the centre will look slightly like a grass blade’s stem.*

In the fragment shader, it’s just a couple of lines of code to interpolate between `_BaseColor`

and `_TipColor`

then multiply by the `_BladeTexture`

sample. And now our test scene suddenly looks like someone’s left strings of Pride bunting pointing skywards.

```
float4 frag (GeomData i) : SV_Target
{
float4 color = tex2D(_BladeTexture, i.uv);
return color * lerp(_BaseColor, _TipColor, i.uv.y);
}
```


![It might be slightly genetically modifed. Colorful grass.](../../assets/2ee2301b899efc03.jpg)

*It might be slightly genetically modifed.*

Obviously we can’t keep the grass looking this uniform - let’s add code to rotate each blade.

# Rotation and Bend

One of the problems we have right now is that we’re defining the grass in local space, so if we rotate the plane, it looks like a fold-up pungee pit. We want to the define each blade in tangent space, so that it points along the vertex normal vector, then apply a transformation from tangent to local space.

![Not to be used in war crimes. Fold-up grass.](../../assets/e4268858cde694a2.jpg)

*Not to be used in war crimes.*

We can use the existing normal and tangent vectors to create a third vector called the bitangent vector, and create a `tangentToLocal`

transformation matrix using the three vectors. That also means we need to change vertical offsets to be on the z-axis rather than the y-axis.

```
float3x3 tangentToLocal = float3x3
(
tangent.x, bitangent.x, normal.x,
tangent.y, bitangent.y, normal.y,
tangent.z, bitangent.z, normal.z
);
...
triStream.Append(TransformGeomToClip(pos, float3(-0.1f, 0.0f, 0.0f), transformationMatrix, float2(0.0f, 0.0f)));
triStream.Append(TransformGeomToClip(pos, float3( 0.0f, 0.0f, 0.0f), transformationMatrix, float2(1.0f, 0.0f)));
triStream.Append(TransformGeomToClip(pos, float3( 0.0f, 0.0f, 0.5f), transformationMatrix, float2(0.5f, 1.0f)));
```


For the next part, we’ll include two functions called `rand`

- for random number generation - and `angleAxis3x3`

- for building rotation matrices - as well as defining `PI`

and `TWO_PI`

.

```
#define UNITY_PI 3.14159265359f
#define UNITY_TWO_PI 6.28318530718f
// Following functions from Roystan's code:
// (https://github.com/IronWarrior/UnityGrassGeometryShader)
// Simple noise function, sourced from http://answers.unity.com/answers/624136/view.html
// Extended discussion on this function can be found at the following link:
// https://forum.unity.com/threads/am-i-over-complicating-this-random-function.454887/#post-2949326
// Returns a number in the 0...1 range.
float rand(float3 co)
{
return frac(sin(dot(co.xyz, float3(12.9898, 78.233, 53.539))) * 43758.5453);
}
// Construct a rotation matrix that rotates around the provided axis, sourced from:
// https://gist.github.com/keijiro/ee439d5e7388f3aafc5296005c8c3f33
float3x3 angleAxis3x3(float angle, float3 axis)
{
float c, s;
sincos(angle, s, c);
float t = 1 - c;
float x = axis.x;
float y = axis.y;
float z = axis.z;
return float3x3
(
t * x * x + c, t * x * y - s * z, t * x * z + s * y,
t * x * y + s * z, t * y * y + c, t * y * z - s * x,
t * x * z - s * y, t * y * z + s * x, t * z * z + c
);
}
```


The grass blades will randomly rotate on the spot, so we can build a rotation matrix that spins around the normal vector by a random amount, then we’ll build a second rotation matrix around the x-axis for the grass blades bending forward and backwards. There’s a `_BendDelta`

property for that. Only the tip vertex is influences by the bend transformation, so apply the transformations differently to each vertex accordingly.

```
// Rotate around the y-axis a random amount.
float3x3 randRotMatrix = angleAxis3x3(rand(pos) * UNITY_TWO_PI, float3(0, 0, 1.0f));
// Rotate around the bottom of the blade a random amount.
float3x3 randBendMatrix = angleAxis3x3(rand(pos.zzx) * _BendDelta * UNITY_PI * 0.5f, float3(-1.0f, 0, 0));
// Transform the grass blades to the correct tangent space.
float3x3 baseTransformationMatrix = mul(tangentToLocal, randRotMatrix);
float3x3 tipTransformationMatrix = mul(mul(tangentToLocal), randBendMatrix), randRotMatrix);
```


![You spin me right round baby, right round. Rotated grass.](../../assets/6fa8eba1dd5f9376.jpg)

*You spin me right round baby, right round.*

Now if we pan back out to the Scene View, the blades are a bit more relaxed, like they’re chilling in the sun! However, every blade is still the same shape. Like in nature, we want the grass to have some variation in height, thickness and curvature.

# Shaping Up

So far, we’ve stuck with only three vertices per grass blade, but this restricts the amount of shape we can give them. To add curvature, we’ll need more vertices. We can define a number of `BLADE_SEGMENTS`

at the top of the code and change the `maxvertexcount`

to be `BLADE_SEGMENTS * 2 - 1`

.

```
// Top of code
#define BLADE_SEGMENTS 4
// Above geom
[maxvertexcount(BLADE_SEGMENTS * 2 + 1)]
```


Now we’re going to randomly pick the width and height between a range of possible values and add an additional bend amount, all of which is controlled by new properties.

```
float width = lerp(_BladeWidthMin, _BladeWidthMax, rand(pos.xzy));
float height = lerp(_BladeHeightMin, _BladeHeightMax, rand(pos.zyx));
float forward = rand(pos.yyz) * _BladeBendDistance;
```


Instead of creating all three vertices manually, we’ll create them in pairs inside a `for`

loop then set the tip vertex at the end. Every vertex besides the first two will use the transform matrix we previously used for just the tip, and we’ll add curvature using a new property called `_BladeBendCurve`

. We can set as many `BLADE_SEGMENTS`

as we want, and the loop does the maths for us! The offsets calculated inside the loop make sure the default shape of the blade is still the same triangle, but now it’s made using extra vertices which are able to bend independently.

```
// Create blade segments by adding two vertices at once.
for (int i = 0; i < BLADE_SEGMENTS; ++i)
{
float t = i / (float)BLADE_SEGMENTS;
float3 offset = float3(width * (1 - t), pow(t, _BladeBendCurve) * forward, height * t);
float3x3 transformationMatrix = (i == 0) ? baseTransformationMatrix : tipTransformationMatrix;
triStream.Append(TransformGeomToClip(pos, float3( offset.x, offset.y, offset.z), transformationMatrix, float2(0, t)));
triStream.Append(TransformGeomToClip(pos, float3(-offset.x, offset.y, offset.z), transformationMatrix, float2(1, t)));
}
// Add the final vertex at the tip of the grass blade.
triStream.Append(TransformGeomToClip(pos, float3(0, forward, height), tipTransformationMatrix, float2(0.5, 1)));
```


![Slouching like me after a couple of drinks. Blade curves.](../../assets/ac2e08da8964a647.jpg)

*Slouching like me after a couple of drinks.*

Now we’ve got some lovely bent blades, but the shader still doesn’t make the cut. I want to include something Roystan didn’t in the original tutorial: a way of mowing down some of the grass.

# Grass Visibility Map

It’s common to pass all sorts of data to shaders through the use of extra texture maps, and we’re going to use one to denote which areas of the plane should have grass and which shouldn’t. It’s a greyscale texture called `_GrassMap`

, where a value of 1 means grass should be present, and 0 means it’s gone.

![This map gives us a nice pattern. Grass map.](../../assets/c6321863f9f1db7b.jpg)

*This map gives us a nice pattern.*

We can read textures during the geometry stage if we use `tex2Dlod`

instead of `tex2D`

, which we’ll do now to read the `_GrassMap`

property to get a visibility value. We just pick the highest quality LOD (or Level of Detail), and to do that, we pass in the UVs inside a 4-element vector, where the first two elements are the standard UV coordinates and the fourth component is the level of detail. 0 is the highest quality LOD, so we’ll use that.

```
float grassVisibility = tex2Dlod(_GrassMap, float4(input[0].uv, 0, 0)).r;
```


We also have a `_GrassThreshold`

property - visibility values above or equal this will result in grass being grown. We’ll just wrap most of the geometry code we wrote so far in an `if`

statement and now we can choose not to sow grass where the threshold isn’t met.

```
if (grassVisibility >= _GrassThreshold)
{
// Most of the geom code so far.
}
```


We can add falloff so that the grass gets shorter at the edges too - `smoothstep`

gets us a nice curve for that, then we just multiply the random weights used for the width and height.

```
float falloff = smoothstep(_GrassThreshold, _GrassThreshold + _GrassFalloff, grassVisibility);
float width = lerp(_BladeWidthMin, _BladeWidthMax, rand(pos.xzy) * falloff);
float height = lerp(_BladeHeightMin, _BladeHeightMax, rand(pos.zyx) * falloff);
```


![This will look A LOT better when we make the grass thicker. Grass visibility.](../../assets/99255a0a6f574040.jpg)

*This will look A LOT better when we make the grass thicker.*

You could go one further and devise a method for cutting grass based on in-game actions, such as a green-clad hero hacking at foliage in search of currency. It’d usually involve drawing on the `_GrassMap`

in realtime. [Daniel Santalla has a great tutorial](https://twitter.com/danielsantalla/status/1391135820229222401) for doing something very similar with snow! And on the flipside, [MinionsArt has created a system](https://www.youtube.com/watch?v=xKJHL8nQiuM) for painting grass on a mesh. Both are great places to go after reading this article!

Our grass has plenty of variation now, but it’s still static. Let’s add some atmosphere.

# Wind Zones

I tried really hard to find out how to integrate our grass seamlessly with Unity’s wind zones, but it turned out to be a bit of a forlorn attempt. Basically, wind zones are great for terrains and particles, but not so much shaders. So I resorted to the same method as Roystan - we’ll use a texture to blow wind through the grass.

![That's just the way I flow. Flow map.](../../assets/e5334a5fe5a36912.jpg)

*That’s just the way I flow.*

This technique involves using a flow map and scrolling it over the grass over time, then converting the texture’s colours to directions in which to bend the grass even more. Like before, we can sample the wind flow map using `tex2Dlod`

after calculating the UVs.

```
float2 windUV = pos.xz * _WindMap_ST.xy + _WindMap_ST.zw + normalize(_WindVelocity.xzy) * _WindFrequency * _Time.y;
float2 windSample = (tex2Dlod(_WindMap, float4(windUV, 0, 0)).xy * 2 - 1) * length(_WindVelocity);
```


We’ll use this to create another transformation matrix which gets applied to everything apart from the two base vertices. If we chose to bend the base vertices, they could end up clipping through the floor. That’s a visual bug we don’t want to take root.

```
float3 windAxis = normalize(float3(windSample.x, windSample.y, 0));
float3x3 windMatrix = angleAxis3x3(UNITY_PI * windSample, windAxis);
...
float3x3 tipTransformationMatrix = mul(mul(mul(tangentToLocal, windMatrix), randBendMatrix), randRotMatrix);
```


You’ll need to tweak the values a lot based on the mesh and grass you’re using, but this grass is starting to blow me away!

![It looks better in motion. Windy grass.](../../assets/a259da20b6676caf.jpg)

*It looks better in motion.*

Because of the way I programmed the shader, it’ll look completely silly when you rotate the mesh at runtime. Oh well. You could fix it by calculating the time-based offsets in the script rather than the shader, but it wasn’t really a focus for me.

The individual grass blades are looking full of life now. I mean, if you were a bug… wouldn’t you go for them? Problem is, the grass is a bit too spaced out. We are pretty much done with the geometry shader now, so how do we make the grass thicker? Well, we could use a mesh with more vertices, or we could make use of another optional kind of shader.

# Tessellation Shaders

Tessellation shaders can be used to subdivide a mesh so that it’s made of more primitive shapes - triangles in our case. Typically, this lets you generate highly detailed surfaces from lower-poly meshes, and you can even generate LODs on the fly. But for a start, we’re most interested in just adding vertices within each face of the mesh. The tessellation stage as a whole slots in between the vertex and geometry stages.

![Tessellation subdivides a mesh into a higher-poly version. Tessellation.](../../assets/acf70f0152ec7a41.jpg)

*Tessellation subdivides a mesh into a higher-poly version.*

Roystan’s tutorial covers tessellation, which itself is based on [Catlike Coding’s tutorial](https://catlikecoding.com/unity/tutorials/advanced-rendering/tessellation/) - it goes into far more detail than I will. Compared to geometry shaders, tessellation shaders are a bit more technical. For a start, in HLSL, it’s two shader functions called `hull`

and `domain`

.

We’ll start with the `hull`

shader. It’s responsible for taking an input patch of vertex data and creating new **control points**, which are basically new vertices in the tessellated mesh. We need to define a few things above the function, but probably the most important part is the **patch constant function**. That’s another function we need to write separately. The hull shader function itself just returns a control point.

```
[domain("tri")]
[outputcontrolpoints(3)]
[outputtopology("triangle_cw")]
[partitioning("integer")]
[patchconstantfunc("patchConstantFunc")]
VertexInput hull(InputPatch<VertexInput, 3> patch, uint id : SV_OutputControlPointID)
{
return patch[id];
}
```


The patch constant function is where we write the logic that determines exactly how the new vertices are created, and I like to think of it as part of the hull shader. We’re going to create new vertices along each edge, and also in the centre of the triangle in layers. A new struct called `TessellationFactors`

contains that data.

```
struct TessellationFactors
{
float edge[3] : SV_TessFactor;
float inside : SV_InsideTessFactor;
};
```


In our case, we want to be able to define a distance between grass blades in the Inspector and let the tessellation system work out the right number of vertices. We’ll write another function - yes I know, we’re swimming in them at this stage - called `tessellationEdgeFactor`

, and use this to calculate the number of new vertices on each edge. The number of inside layers can just be the mean average of those three edge values.

The `tessellationEdgeFactor`

function is pretty simple - we’ll take the length of the edge and divide by a property called `_TessellationGrassDistance`

. By doing it this way, the density of grass is independent of the mesh used. Once we’ve done that and assembled all these bits of code in the right order, all we’re left with is the `domain`

shader.

```
float tessellationEdgeFactor(VertexInput vert0, VertexInput vert1)
{
float3 v0 = vert0.vertex.xyz;
float3 v1 = vert1.vertex.xyz;
float edgeLength = distance(v0, v1);
return edgeLength / _TessellationGrassDistance;
}
```


Thankfully, the `domain`

shader is a bit simpler - it takes the new vertices that were generated after the `hull`

shader and is responsible for interpolating properties of the old vertices onto the new ones. These fancy-sounding **barycentric coordinates** are just a way to express the new vertices as a weighted sum of the old ones, so if we take the respective properties of the old vertices and multiply by the barycentric coordinates, we’ll get the right values of the properties for the new vertices.

![They're not centred on someone called Barry. Barycentric Coordinates.](../../assets/faad9477ad2bce3b.jpg)

*They’re not centred on someone called Barry.*

```
[domain("tri")]
VertexOutput domain(TessellationFactors factors, OutputPatch<VertexInput, 3> patch, float3 barycentricCoordinates : SV_DomainLocation)
{
VertexInput i;
// Create interpolation macro.
#define INTERPOLATE(fieldname) i.fieldname = \
patch[0].fieldname * barycentricCoordinates.x + \
patch[1].fieldname * barycentricCoordinates.y + \
patch[2].fieldname * barycentricCoordinates.z;
INTERPOLATE(vertex)
INTERPOLATE(normal)
INTERPOLATE(tangent)
INTERPOLATE(uv)
return tessVert(i);
}
```


We’ll use a macro to do this for each property rather than rewriting the logic for each one, and to make our lives easier, we’ll use a new vertex shader called `tessVert`

which just transforms a `VertexInput`

into a `VertexOutput`

without changing anything. Remember that our geometry shader requires a `VertexOutput`

and that the geometry shader happens after the tessellation shader? That’s why we do the conversion here.

```
VertexOutput tessVert(VertexInput v)
{
VertexOutput o;
o.vertex = v.vertex;
o.normal = v.normal;
o.tangent = v.tangent;
o.uv = v.uv;
return o;
}
```


At the top of the `Pass`

, we’ll need to put `#pragma require tessellation tessHW`

, `#pragma hull hull`

and `#pragma domain domain`

.

```
#pragma require tessellation tessHW
#pragma hull hull
#pragma domain domain
```


![Now the grass looks so much thicker! Tessellated grass.](../../assets/e63daee1563f851a.jpg)

*Now the grass looks so much thicker!*

There’s one shader we’ve barely touched and it’s the good old-fashioned fragment shader. We’ve got a pretty comprehensive grass setup already, but in the final step, we’re gonna make our grass able to receive shadows.

# Receiving Shadows

The last step comes to us courtesy of [Ben Golus on the Unity forums](https://forum.unity.com/threads/water-shader-graph-transparency-and-shadows-universal-render-pipeline-order.748142/#post-5518747). If you’ve ever posted a technical graphics question and got a good answer, it was probably from him.

In our fragment shader, we’re already using a grass blade texture as a sort of greyscale shading map, so all we need to do is multiply this by the lighting amount. Unity provides a couple of functions to help us calculate the lighting here - `GetShadowCoord`

and `MainLightRealtimeShadow`

together gets us the level of light between 0 and 1 falling on this pixel, and I’ll add an offset of 0.25 to simulate ambient light. That’s actually all there is to it!

```
float4 frag (GeomData i) : SV_Target
{
float4 color = tex2D(_BladeTexture, i.uv);
#ifdef _MAIN_LIGHT_SHADOWS
VertexPositionInputs vertexInput = (VertexPositionInputs)0;
vertexInput.positionWS = i.worldPos;
float4 shadowCoord = GetShadowCoord(vertexInput);
half shadowAttenuation = saturate(MainLightRealtimeShadow(shadowCoord) + 0.25f);
float4 shadowColor = lerp(0.0f, 1.0f, shadowAttenuation);
color *= shadowColor;
#endif
return color * lerp(_BaseColor, _TipColor, i.uv.y);
}
```


![This grass is a bit shady. Grass shadows.](../../assets/8ae0b0638054052f.jpg)

*This grass is a bit shady.*

As homework, you could also try making the grass cast shadows too. Roystan’s tutorial does this, and Cyan’s URP guide has some great content on writing a Shadow Caster pass, so those would be a great place to start.

# Conclusion

Grass is a fantastic tool to add detail to your scenes, especially in an open-world setting where it can help break up large, bland sections of ground. We learned a lot today, including two totally different kinds of shader, and we saw how we can upgrade content written for Unity’s built-in pipeline to Universal Render Pipeline.

Look out for more details about the next big shader tutorial!

If you want a grass shader you can plonk in your game and edit at will, then have a look at this asset: