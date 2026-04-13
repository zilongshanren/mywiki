---
title: 'My take on shaders: Geometry Shaders'
url: https://halisavakis.com/my-take-on-shaders-geometry-shaders/
published: '2019-09-29'
source_blog: Technically Art – Harry Alisavakis
source_site: https://halisavakis.com
category: graphics
fetched: '2026-04-13'
---

## Patrons

This post is brought to you by Patrons:

- Djinnlord
- Nicolo Linder

## Introduction

The resources for Unity shaders out there are scarce enough as it is, but there’s a very specific type of Unity shaders that is weirdly rare to find resources upon (at least at the time of writing): Geometry shaders. My presumption is that people don’t really care for them because they can be inefficient and in some cases they can be replaced by faster compute shaders. However, they are still really interesting to examine, and some really cool effects can be created with them. The most obvious example (which we’ll examine in the next (probably) tutorial) is grass shaders. In some cases, generating grass blades or quads with grass textures can be better than instancing grass objects all over the place, plus the geometry shaders can give us some more flexibility when it comes to optimization and customization.

I’ll link here some of the tutorials and resources that helped me get started with geometry shaders, so I definitely recommend them as a supplementary material:

[https://jayjingyuliu.wordpress.com/2018/01/24/unity3d-intro-to-geometry-shader/](https://jayjingyuliu.wordpress.com/2018/01/24/unity3d-intro-to-geometry-shader/)[https://roystan.net/articles/grass-shader.html](https://roystan.net/articles/grass-shader.html)(which also happens to be the definitive tutorial for grass with geometry shaders)- The geometry shaders at
[shaderslab.com](http://shaderslab.com/shaders.html)

## Overview

Before jumping into the code, let’s start with an overview of what a geometry shader is. To help me illustrate their role, here’s a view of a simplified real time rendering pipeline:

![](../../assets/6c92bc016fd83efb.png)

[https://vulkan-tutorial.com/Drawing_a_triangle/Graphics_pipeline_basics/Introduction](https://vulkan-tutorial.com/Drawing_a_triangle/Graphics_pipeline_basics/Introduction)

This one is about the pipeline in Vulkan, but the concept is very similar to other pipelines as well. The yellow boxes are the actual stages of the pipeline that we can program/override with our shaders. It’s also worth noting that the “Tessellation” stage actually breaks into “Hull Shader stage”, “Tessellator stage” and “Domain Shader stage”. The hull and domain stages can also be affected by the corresponding shaders (like the vertex and fragment stage), but the tessellator stage can not be modified (in the context of Unity shaders, that is).

The core takeaway from this is that geometry shaders are the step between vertex shaders and fragment shaders, and this is a concept you’ll keep seeing in the shader examples too. Their main purpose is to get the information from the separate vertices via the vertex shader, assemble the primitives that will form the object (usually it’s going to be triangles) and send the final information on to the fragment shader for coloring, lighting etc.

However, the coolest thing, about geometry shaders is that they take triplets of vertices forming a triangle (for example) and they can not only define what happens to that triangle, but they can also generate **new vertices** and, therefore, **new triangles** and then take all that newly generated geometry and flail it around, like you’d do when displacing vertices in a vertex shader. That can actually allow you, for example, to make particles out of triangles, very much like [VFX Mike has demonstrated](http://vfxmike.blogspot.com/2018/07/geometry-shader-adventures-mesh.html).

Finally, while their code might look scary at first, once you get the hang of some stuff, using them actually becomes really intuitive and you can actually get a better understanding of how stuff like UVs and object space coordinates work. And, if you’re anything like me, you’ll catch yourself saying “Oh damn, I didn’t think this would work!” a lot.

## Basic geometry shader

I thought I’d first start with a very basic geometry shader with no additional functionality, just to get the “paperwork” stuff out of the way. This will also serve as a neat template for new geometry shaders you’ll want to make, so I’d keep it handy somewhere.

Let’s see the code:

```
Shader "Geometry/NewGeometryShader"
{
Properties
{
_MainTex ("Texture", 2D) = "white" {}
}
SubShader
{
Tags { "RenderType"="Opaque" }
LOD 100
Pass
{
CGPROGRAM
#pragma vertex vert
#pragma geometry geom
#pragma fragment frag
// make fog work
#pragma multi_compile_fog
#include "UnityCG.cginc"
struct appdata
{
float4 vertex : POSITION;
float2 uv : TEXCOORD0;
};
struct v2g
{
float4 vertex : SV_POSITION;
float2 uv : TEXCOORD0;
};
struct g2f
{
float2 uv : TEXCOORD0;
UNITY_FOG_COORDS(1)
float4 vertex : SV_POSITION;
};
sampler2D _MainTex;
float4 _MainTex_ST;
v2g vert (appdata v)
{
v2g o;
o.vertex = v.vertex;
o.uv = v.uv;
return o;
}
[maxvertexcount(3)]
void geom(triangle v2g IN[3], inout TriangleStream<g2f> triStream)
{
g2f o;
for(int i = 0; i < 3; i++)
{
o.vertex = UnityObjectToClipPos(IN[i].vertex);
UNITY_TRANSFER_FOG(o,o.vertex);
o.uv = TRANSFORM_TEX(IN[i].uv, _MainTex);
triStream.Append(o);
}
triStream.RestartStrip();
}
fixed4 frag (g2f i) : SV_Target
{
// sample the texture
fixed4 col = tex2D(_MainTex, i.uv);
// apply fog
UNITY_APPLY_FOG(i.fogCoord, col);
return col;
}
ENDCG
}
}
}
```

First up, we have to let the overall shader know that we’re going to use a geometry shader. Therefor, we need to add another #pragma statement in line 16 where we say that there’ll be a method corresponding to the geometry shader called “geom”, which we’ll define later. That’s what the “#pragma geometry geom” does, just like with the vertex and fragment shaders.

In this case we’re not just passing data from the vertex to the fragment shader, but we also have the geometry shader in between. Therefore, we’re going to need three data structures instead of the usual two:

- The “appdata” struct to pass the object’s attributes to the vertex shader, like always.
- The “v2g” struct to pass data from the vertex shader to the geometry shader
- The “g2f” struct to pass data from the geometry shader to the fragment shader.

Moving on to the shaders, first up we see the vertex shader. Instead of a v2f object, it now returns a v2g object, which, as mentioned above, passes the data to the geometry shader. In this simple instance, the vertex just passes the data without any modification whatsoever.

In line 48 I just pass the vertex position in object space as it is, and I also did the same in line 49 for the UV coordinates of the vertex. Notice that I didn’t do the object-to-clip-position conversion or use the “TRANSFORM_TEX” macro for the UVs, as those actions will be done in the geometry shader when transferring the data to the fragment shader.

Keep in mind that we could actually do the object-to-clip-position conversion and the UV calculations in the vertex shader and it might even be better since it will be done fewer times. But passing the data raw like that to the geometry shader gives us more flexibility as to how we’re handling them.

### The geometry shader itself

Here’s where stuff gets trickier. First thing you’ll notice right out of the bat, is the crazy different syntax on the geometry shader. But we’ll go through it step-by-step.

In line 53 there’s a weird attribute above the shader. As the name implies, “maxvertexcount” lets the shader know the maximum number of vertices this geometry shader will be appending. Since we’re just adding the actual triangles of the object, we’ll be just outputting 3 vertices.

Then, in line 54 there’s the method declaration that features a couple of weird parameters:

*triangle*v2g IN[3] : This is an array of three v2g objects, each corresponding to one vertex of the triangle we’re currently examining. The “triangle” tag informs the geometry shader that it will be expecting a triangle as an input. You could be getting a line as an input (so you’d need a v2g object array of size 2) or a point (so you’d need a v2g object array of size 1).*inout*TriangleStream<g2f> triStream : In case you didn’t notice, the geometry shader returns “void”, so we’re not actually returning a single object, like the vertex shader does. The geometry shader actually appends each triangle to a TriangleStream list which takes objects of type “g2f”. If you wanted to output lines you’d turn that into ”*inout*LineStream<g2f> lineStream ” and if you wanted to output points, it’d be ”*inout*PointStream<g2f> pointStream “.

Now let’s move on to the actual functionality. What we want for this geometry shader is to just get the data from the vertex shader, and assemble the triangles that will be then translated to fragments and shaded by the fragment shader.

First, in line 56 we make a g2f object which we’ll use to constantly modify its fields and then append it to the stream.

Then, we’re gonna make a simple loop to append the three input vertices to the stream to create the object’s triangle. And since that data is going to the fragment shader, I’m doing all the modifications I want here.

First, in line 60 I use the ” UnityObjectToClipPos ” method to convert the input vertex position from object space to clip space. Then, I use the ” UNITY_TRANSFER_FOG ” macro to transfer all the information about Unity’s fog . In line 62 I also use the ” TRANSFORM_TEX ” macro to modify the UV coordinates based on the scaling and tiling information of “_MainTex”. All that is done for each of the three vertices of the triangle, just like we’d do in the vertex shader if we didn’t have the geometry shader.

Finally, we’re appending the modified “g2f” object to the triangle stream using ” triStream.Append(o); “. After the loop there’s also the “RestartStrip” method, in line 66. This is to let the stream know that it will be appending a separate triangle afterwards. Here, since we’re not appending any new triangles, it’s not really needed, but I added it so you could easily copy it if you need it, should you extend the shader later on.

### The humble fragment shader

Finally, in lines 69-76 we have the fragment shader. You might notice that it’s completely unchanged from the default fragment shader in a new unlit shader, except that it gets a “g2f” as a parameter, instead of a “v2f”.

## Extruding pyramids

Now that we have the base for a geometry shader we can actually make one that does something. This one specifically, is going to extrude pyramids from each triangle, basically adding a point at the center of each triangle and extruding the pyramid towards the normal vector of the face.

A visual example of what we’ll do on each triangle is this:

![](../../assets/f20f59e14b15d98b.png)

Let’s see the code:

```
Shader "Geometry/TrianglePyramidExtrusion"
{
Properties
{
_MainTex ("Texture", 2D) = "white" {}
_ExtrusionFactor("Extrusion factor", float) = 0
}
SubShader
{
Tags { "RenderType"="Opaque" }
Cull Off
LOD 100
Pass
{
CGPROGRAM
#pragma vertex vert
#pragma geometry geom
#pragma fragment frag
// make fog work
#pragma multi_compile_fog
#include "UnityCG.cginc"
struct appdata
{
float4 vertex : POSITION;
float2 uv : TEXCOORD0;
float3 normal : NORMAL;
};
struct v2g
{
float4 vertex : SV_POSITION;
float2 uv : TEXCOORD0;
float3 normal : NORMAL;
};
struct g2f
{
float2 uv : TEXCOORD0;
UNITY_FOG_COORDS(1)
float4 vertex : SV_POSITION;
float4 color : COLOR;
};
sampler2D _MainTex;
float4 _MainTex_ST;
float _ExtrusionFactor;
v2g vert (appdata v)
{
v2g o;
o.vertex = v.vertex;
o.uv = v.uv;
o.normal = v.normal;
return o;
}
[maxvertexcount(12)]
void geom(triangle v2g IN[3], inout TriangleStream<g2f> triStream)
{
g2f o;
float4 barycenter = (IN[0].vertex + IN[1].vertex + IN[2].vertex) / 3;
float3 normal = (IN[0].normal + IN[1].normal + IN[2].normal) / 3;
for(int i = 0; i < 3; i++) {
int next = (i + 1) % 3;
o.vertex = UnityObjectToClipPos(IN[i].vertex);
UNITY_TRANSFER_FOG(o,o.vertex);
o.uv = TRANSFORM_TEX(IN[i].uv, _MainTex);
o.color = fixed4(0.0, 0.0, 0.0, 1.0);
triStream.Append(o);
o.vertex = UnityObjectToClipPos(barycenter + float4(normal, 0.0) * _ExtrusionFactor);
UNITY_TRANSFER_FOG(o,o.vertex);
o.uv = TRANSFORM_TEX(IN[i].uv, _MainTex);
o.color = fixed4(1.0, 1.0, 1.0, 1.0);
triStream.Append(o);
o.vertex = UnityObjectToClipPos(IN[next].vertex);
UNITY_TRANSFER_FOG(o,o.vertex);
o.uv = TRANSFORM_TEX(IN[next].uv, _MainTex);
o.color = fixed4(0.0, 0.0, 0.0, 1.0);
triStream.Append(o);
triStream.RestartStrip();
}
for(int i = 0; i < 3; i++)
{
o.vertex = UnityObjectToClipPos(IN[i].vertex);
UNITY_TRANSFER_FOG(o,o.vertex);
o.uv = TRANSFORM_TEX(IN[i].uv, _MainTex);
o.color = fixed4(0.0, 0.0, 0.0, 1.0);
triStream.Append(o);
}
triStream.RestartStrip();
}
fixed4 frag (g2f i) : SV_Target
{
// sample the texture
fixed4 col = tex2D(_MainTex, i.uv) * i.color;
// apply fog
UNITY_APPLY_FOG(i.fogCoord, col);
return col;
}
ENDCG
}
}
}
```

### Before the geometry shader

For this shader, I’ve added a new property called “_ExtrusionFactor” which will determine how extruded our pyramids will be. Also, due to some triangles not being drawn in the correct order, to avoid culling some faces, I’ve added the “Cull Off” tag in line 11. The best way would be to actually draw the faces properly, but for now let’s keep it that way so it’ll be easier to use loops.

Some changes were also done in the data structures. In order to get the normal vector of each face, we’d first need to get the normal vector of each vertex, therefore we’ll have to add it to both the “appdata” structure and the “v2g” structure. Furthermore, in the “g2f” structure I add a color field, that will help with a better visualization of the effect.

The vertex shader is almost the same as before, I’m just passing the normal vector to the “v2g” data as additional info.

### The geometry shader

For once, this is where the magic happens! ✨The first you might notice is that in line 12 I’m mentioning that I’ll output a maximum number of 12 vertices in this shader. However, you might think that that’s not correct, as we’re only adding one extra vertex for the tip of the pyramid. At least that what initially confused me. The thing is that since we’re adding new triangles, we’ll have to add **every** new vertex that forms the new triangle. Therefore, since we’ll add a new triangle for each edge we’ll have 3 new triangles from 3 vertices each, plus the original mesh triangle with 3 more vertices. So, 3 * 3 + 3 = 12 new vertices. Now you can see how this number can get out of hand pretty quickly.

For the actual extrusion, we’ll need the center of each triangle as well as its normal vector. Therefore, in line 65 I calculate the barycenter position of the triangle by getting the average position of the triangle’s points, and in line 66 I get the normal vector by also averaging the normal vectors of each triangle’s point.

Then, I proceed to the pyramid generation. The algorithm goes like this:

For each of the triangle's points Get the index of the next point Add a vertex at the position of the current point Add a vertex at the barycenter of the triangle and extruded it along the normal vector of the face by amount equal to "_ExtrusionFactor" Add a vertex at the position of the next point

And that’s exactly what happens in the first for loop. In line 69 I get the index of the next point by increasing i by one and using modulo 3 so that I won’t go out of the range of the array. Then, in lines 71-75 I add a new vertex exactly like in the example above, only this time I also set the color value for that vertex to be black (in line 74).

In lines 77-81 I do the same for the point of the pyramid, but for its position I use the calculated barycenter to which I add the normal vector multiplied by the “_ExtrusionAmount”, to move it upwards. The color I use for the tip of the triangle is white, so that the extrusion will be more obvious.

Then, in lines 83-87 I do exactly the same for the next point, also coloring it black.

Since here we’re actually adding a new triangle in every loop, I added ” triStream.RestartStrip(); ” at the bottom of the loop.

Finally, after the loop, in lines 92-99 I add the vertices of the original triangle, also coloring it black and that’s about it!

With a shader like this, you’ll probably end up with a mesh where there are pyramids extruding from each of its triangles, like so:

![](../../assets/b3cf72e3b2edfc62.png)

oh it’s the featured image

### The fragment shader

The fragment shader remains the same, however I multiply the color with “i.color” so that the vertex colors we assigned are visible.

## Conclusion

I hope this was a gentle enough introduction to the world of geometry shaders! They can definitely seem more intimidating at first, but after getting why they are the way they are, things can get a lot clearer and definitely more fun! I highly suggest playing around with examples from Shaderslab or fiddling with these two shaders in the post to see what you can achieve!

See you in the [next one](https://halisavakis.com/my-take-on-shaders-grass-shader-part-i/)!

## Comments

Hello,

I would simply like to say an enormous thank you for this article. It has aided in breaking down the scary wall that is geometry shaders for me. I have been working with fragment and vertex shaders for a while, but this definitely helped open doors for me. It was the perfect pace.

Thank you so very much, I look forward to reading more tutorials like these later on.

Author

As someone who initially struggled *a lot* to figure out how geometry shaders work, I’m really happy this helped =] The next tutorials on geometry shaders (about grass) will probably help even more with some concepts ^^