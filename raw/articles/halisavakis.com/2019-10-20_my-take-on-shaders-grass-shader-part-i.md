---
title: 'My take on shaders: Grass Shader (Part I)'
url: https://halisavakis.com/my-take-on-shaders-grass-shader-part-i/
published: '2019-10-20'
source_blog: Technically Art – Harry Alisavakis
source_site: https://halisavakis.com
category: graphics
fetched: '2026-04-13'
---

## Patrons

This post is brought to you by:

- Djinnlord
- Nicolo Linder
- orels1
- Tiph’ (DN)

## Introduction

In [the previous tutorial](https://halisavakis.com/my-take-on-shaders-geometry-shaders/) we saw some stuff around geometry shaders, which have a lot of really interesting applications, and grass shaders is one of the most popular ones! Grass shaders, like water shaders, can be infinitely fun and you can pursue any level of physical accuracy you want, from something toony or stylized to something realistic af. The result obviously depends on the work you put in the effect.

The shader I’ll be showing here is more on the stylized side, and is actually completely unlit and unresponsive to shadows. In the next part we’ll add that stuff and some more, but if you’re in a hurry to see how to add these stuff, I highly suggest [Roystan’s grass shader tutorial](https://roystan.net/articles/grass-shader.html). Besides, I learned how to do some of the lighting stuff from that tutorial myself.

It goes without saying that in order to follow some concepts of this shader it’s quite important to check the previous tutorial first, as I won’t be going too much in depth in some of the more basic concepts I already covered.

## Shader overview

Before checking out the code, I’ll first do a quick rundown of what this specific shader does and how it does it. In short, its features are:

- The shader generates a variable number of grass blades per triangle in random positions, heights and orientations. The set maximum number of grass blades for now is 15.
- The shader also calculates new UV coordinates for the generated grass blades.
- Depending on the distance from the camera, the shader will generate less grass blades, for some minor optimization.
- The grass blades will sway based on a displacement texture, resembling motion via wind.
- The grass blades will be colored via a gradient map using their custom-assigned vertex colors and they’ll also have an additional color from the wind, giving a glossy impression as they sway around.

The blade generation algorithm is as follows:

- We get the normal vector of the current triangle and the number of grass blades we’ll spawn (based on distance from the camera)
- For each grass blade
- We get random numbers based on the world position of the triangle’s vertices

- We calculate a random point in the triangle using
[this technique](https://stackoverflow.com/a/19654424). We’ll call this “midpoint”. - We calculate two other points, one on each side of the midpoint. As a reference point for the offset direction of these points we use one of the triangle’s vertex.
- We calculate the wind contribution by sampling a displacement texture.
- We calculate the height offset by sampling a noise texture.
- The top point of the grass blade will be on the same position as the midpoint but it will be offset along the normal vector of the triangle. The point will also be offset on the X and Z axis based on an random amount multiplied by an external property, and it will also be offset based on the wind.
- In the top point’s vertex colors, we store the wind contribution to the green channel and we set the other channels to 1.
- The other 2 points we calculated will have their vertex color set to black.
- The three points get appended to the triangle stream

- We append the original vertices of the triangle to the triangle stream.
- ???
- Profit!

A more visual description of the grass blade generation algorithm is as follows:

![](../../assets/44a7b330cf5b0e44.png)

![](../../assets/a84cd31bbb2f37ab.png)

![](../../assets/5753277406cc3141.png)

![](../../assets/8762131c7c580d8d.png)

Most of that stuff will make more sense in code, so don’t worry if all that seems too much.

## The code

Let’s now check the code:

```
Shader "Geometry/GrassGeometryShaderUnlit"
{
Properties
{
//Color stuff
_Color("Color", Color) = (1,1,1,1)
_GradientMap("Gradient map", 2D) = "white" {}
//Noise and wind
_NoiseTexture("Noise texture", 2D) = "white" {}
_WindTexture("Wind texture", 2D) = "white" {}
_WindStrength("Wind strength", float) = 0
_WindSpeed("Wind speed", float) = 0
_WindColor("Wind color", Color) = (1,1,1,1)
//Position and dimensions
_GrassHeight("Grass height", float) = 0
_GrassWidth("Grass width", Range(0.0, 1.0)) = 1.0
_PositionRandomness("Position randomness", float) = 0
//Grass blades
_GrassBlades("Grass blades per triangle", Range(0, 15)) = 1
_MinimunGrassBlades("Minimum grass blades per triangle", Range(0, 15)) = 1
_MaxCameraDistance("Max camera distance", float) = 10
}
SubShader
{
CGINCLUDE
#include "UnityCG.cginc"
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
float _MinimunGrassBlades;
float _MaxCameraDistance;
float random (float2 st) {
return frac(sin(dot(st.xy,
float2(12.9898,78.233)))*
43758.5453123);
}
g2f GetVertex(float4 pos, float2 uv, fixed4 col) {
g2f o;
o.vertex = UnityObjectToClipPos(pos);
o.uv = uv;
o.col = col;
return o;
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
float4 worldPos = mul(unity_ObjectToWorld, midpoint);
float2 windTex = tex2Dlod(_WindTexture, float4(worldPos.xz * _WindTexture_ST.xy + _Time.y * _WindSpeed, 0.0, 0.0)).xy;
float2 wind = (windTex * 2.0 - 1.0) * _WindStrength;
float noise = tex2Dlod(_NoiseTexture, float4(worldPos.xz * _NoiseTexture_ST.xy, 0.0, 0.0)).x;
float heightFactor = noise * _GrassHeight;
triStream.Append(GetVertex(pointA, float2(0,0), fixed4(0,0,0,1)));
float4 newVertexPoint = midpoint + float4(normal, 0.0) * heightFactor + float4(r1, 0.0, r2, 0.0) * _PositionRandomness + float4(wind.x, 0.0, wind.y, 0.0);
triStream.Append(GetVertex(newVertexPoint, float2(0.5, 1), fixed4(1.0, length(windTex), 1.0, 1.0)));
triStream.Append(GetVertex(pointB, float2(1,0), fixed4(0,0,0,1)));
triStream.RestartStrip();
}
for (int i = 0; i < 3; i++) {
triStream.Append(GetVertex(input[i].vertex, float2(0,0), fixed4(0,0,0,1)));
}
triStream.RestartStrip();
}
fixed4 frag (g2f i) : SV_Target
{
fixed4 gradientMapCol = tex2D(_GradientMap, float2(i.col.x, 0.0));
fixed4 col = (gradientMapCol + _WindColor * i.col.g) * _Color;
return col;
}
ENDCG
Pass
{
Tags { "RenderType"="Opaque"}
Cull Off
CGPROGRAM
#pragma vertex vert
#pragma geometry geom
#pragma fragment frag
ENDCG
}
}
}
```

Before you panic, this shader follows a different format which will be useful in the second part. As you can see, the pass is separate from most of the logic and instead of “CGPROGRAM”, in line 29 there’s “CGINCLUDE”. What that format means is that we can declare the functionality of the fragment/vertex/geometry shader beforehand and then just include it in a pass. If we needed to do a second pass with the same geometry shader but a different fragment shader, for example, this format would prove really useful as we wouldn’t have to write the body of the shader again.

With that out of the way, let’s start with the properties:

### Properties

_Color | The color that will be multiplied by the result of the gradient map |
_GradientMap | Gradient map texture that will be used for coloring |
_NoiseTexture | Noise texture that determines the height randomness of the grass blades |
_WindTexture | The displacement texture to be used as a wind effect |
_WindStrength | The strength of the wind effect |
_WindSpeed | The speed at which the wind displacement texture is being panned |
_WindColor | Though the name doesn’t make sense, this is the color that will be added to the final color to simulate the glossiness of the grass as it gets swayed by the wind |
_GrassHeight | The maximum height of the grass blades |
_GrassWidth | The width of the grass blades |
_PositionRandomness | The amount of random offset that the tip of the grass blades will have in the X and Z axes. If kept at 0, the grass blades will look straight up |
_GrassBlades | The maximum amount of grass blades per triangle |
_MinimunGrassBlades | The minimum amount of grass blades per triangle, when the camera is further away |
_MaxCameraDistance | The distance from the camera at which the grass blades will get fewer |

### The in-between stuff

First up, in lines 33-48 I declare the structs I’ll use to transfer data from the vertex shader to the geometry shader and then to the fragment shader. For now I just need the position of the vertices and nothing more. Since I’m not adding any texture to the original mesh, I don’t even need the UV coordinates of the object, I just generate the UV coordinates for the grass blades.

Actually, since I’m not texturing the blades, I don’t even need to generate the UV coordinates of the blades, but I kept that part in to as an opportunity to discuss how we could generate them, should we needed them.

You might have also noticed that the appdata struct is exactly the same as the v2g struct and yes, we could actually use the same struct for both! But for the sake of clarity and to keep the whole “vertex->geometry->fragment” pipeline, I keep the structs separate.

In the g2f struct I also add the UVs and vertex color, to use in the fragment shader.

In lines 50-67 I redeclare my properties (don’t forget the _ST fields!) and then in lines 69-73 I threw in a random hash function, which you might have already seen in other tutorials and pretty much in every shader that uses randomness.

Finally, to avoid some code repetition, in lines 76-82 I have a method to pass the information I need to a g2f object to append it to the stream. All the method does is to convert the given object-space vertex position to clip-space and pass that, the UVs and the color to a newly created g2f object. Simple enough.

### The vertex shader

Here the vertex shader pretty much loses all its glamour, and all it does is pass the position from appdata to the v2g object. It’s a bit sad, really.

### The geometry shader

Here’s where [everything comes together](https://i.kym-cdn.com/entries/icons/original/000/030/904/Screenshot_10.jpg).

Firstly, in line 92 I have the max vertex count to be 48. This is because, as I mentioned above, we might have a maximum of 15 grass blades per triangle. Therefore, we need the 3 standard vertices of the face, plus 3 vertices for each grass blade, so 3 * 15 + 3 = 48. If we wanted more grass blades per triangle, this number should increase by 3 for each additional blade.

In line 95 I calculate the normal vector of the face. This is a different way than the one from the previous tutorial, but it’s just as effective. I’m just leaving it here as an alternative.

In line 96 I determine the number of grass blades that will be spawned on the current triangle. The way I do that is by using lerp to interpolate between the maximum and minimum number of blades based on the first vertex’s distance from the camera. The more correct approach would be to take the barycenter of the triangle, but that works too, the offset won’t be significant in most cases. The bottom line of that line of code is that the smaller the distance from the camera gets, the more grass blades will be generated. If the distance is equal or larger to “_MaxCameraDistance”, then the number of grass blades that will be generated are equal to “_MinimumGrassBlades”.

Moving inside the loop for each grass blade, in lines 99 and 100 I get two random numbers based on the world position of the first and second vertex of the current triangle, respectively. Again, using the first two points of the triangles is a bit arbitrary, but the world-space conversion helps to keep the seed bound to world-space and have multiple patches of grass without repetition, should we want to. Multiplying by (i + 1) also helps with getting a different seed for every grass blade. Again, kind of arbitrary, but you get the point.

In line 103 I calculate the random midpoint of the grass blade using [this method](https://stackoverflow.com/a/19654424) and then in lines 105 and 106 I remap the random numbers from the [0,1] spectrum to the [-1,1] spectrum, to be used for position randomization.

In lines 108-109 I calculate the two base points of the newly generated triangle by offsetting the midpoint by the value of “_GrassWidth” towards a point of the triangle. Once again, the “i%3” is arbitrary and it’s just so that the grass blades won’t all be rotated the same way. The way it works now, the first grass blade’s base’s direction will look towards the first point of the triangle and each grass blade will cycle through the points.

In line 111 I get the world position of the “midpoint” to use as coordinates for the wind and noise texture. The sampling of the wind texture happens in lines 113-114 and it’s pretty much the same method we’ve seen a bunch of times when it comes to displacement textures: sample the texture, offset the UV’s (here it’s the world position’s x and z components) by time and then map the whole thing from -1 to 1 and multiply it by the strength of the effect. Here I also multiply the world position by “_WindTexture_ST.xy” so that I can adjust the scale of the wind via the tiling of the texture in the material inspector.

In lines 116 and 117 I calculate the final height of the grass blade by sampling the noise texture the same way as the wind texture and multiplying the result by “_GrassHeight”.

Keep in mind that both texture samplings here happen with “tex2Dlod” instead of just “tex2D”, due to the fact that we’re not in the fragment shader.

Then, it’s finally time to make the grass blades! Before I go through the code, I want to explain what I’m doing with the UVs of the blades here:

![](../../assets/e3af98a91952c20b.png)

If we want to add a texture to our grass blades, this is a nice way to apply it. As you know, UV coordinates go from (0,0) (bottom left) to (1,1) (top right), so if we want out grass blades to cover the whole spectrum as isosceles triangles, we’d want the first point on the base to have its UVs at (0,0), the other base point at (1,0) and the middle point at (0.5, 1).

That being said, in line 119 I append the first point of the grass blade with (0,0) as its UV coordinates and a black color for its vertex color. Then, in line 121 I calculate the position of the top point as such:

I get the midpoint and first I offset it along the normal vector by “heightFactor”, then I offset it in the x an z axes firstly by using the random numbers “r1” and “r2” from before, multiplied by “_PositionRandomness” and then by using the wind.

Then I append that point to the stream, assign (0.5, 1) as its UV coordinates and as a color I use 1 for the red, blue and alpha channel and the length of the red and green values from the wind texture as the green channel, so that I can later use the intensity of the wind to adjust the color contribution.

After that, I append the third point with (1,0) as its UVs and assign it a black vertex color too. I also restart the strip after that, as we’ll be making a new triangle when the loop restarts.

Finally, In lines 130-132 I append the actual vertices of the face to the stream, and also use (0,0) as UVs and black as the vertex color.

### The fragment shader

The fragment shader is now fairly simple: I just sample the gradient map using the red channel of the vertex color, which, if you remember, is 1 on the top of the grass blades and 0 on the base, so that gives us a nice grayscale gradient going from black to white from the base to the top of the blades. Therefore, the leftmost part of the gradient map texture should be darker, while the rightmost part should be lighter. For the featured image I used this gradient map texture:

![](../../assets/09a096effa624de7.png)

The final color is then calculated by adding the “_WindColor” multiplied by the green channel of the vertex color to the color from the gradient map and then multiplying the whole thing by “_Color”. The color is returned, and all is well!

### The actual pass

As I mentioned at the start, this is a bit of a different format. Our shaders are not in the “Pass” block like we’re used to, instead they’re in a limbo state inside a “CGINCLUDE” block. Cool thing, though, is that they’re still in the same file as our pass. Therefore, in the “Pass” block in lines 148-158, we just need to match the corresponding “#pragma” directives with the names of the shaders and we’re good! They’ll basically be included in the pass as if we wrote them there in the first place.

Since our shaders are appropriately named “vert”, “geom” and “frag” for “vertex”, “geometry” and “fragment” respectively, the “#pragma” tags in lines 153-155 do all the work for us. Also, don’t forget to add the “Cull off” directive I have in line 151, otherwise a bunch of the blades will be invisible from one point of view, due to their rendering order.

## Conclusion

This is the end of the first part of the grass shader! In the next part we’ll see some more exciting features like lighting, shadows etc, but even with just that shader you can experiment with a bunch of different concepts! For example, you can try instead of generating separate blades, to generate quads in a star formation (see [GPU Gems on grass](https://developer.nvidia.com/gpugems/GPUGems/gpugems_ch07.html)) and add a grass texture on them.

Hope you’ll make some stunning grassy scenes with this one, and I’d love to see and share what you make, so by all means let me know if you end up using this shader somewhere!

See you in the [next one](https://halisavakis.com/my-take-on-shaders-grass-shader-part-ii/)!

## Comments

One improvment to this shader would be to define a number of blade given an area instead of by triangle.

It would be really easy to compute the area of the current triangle with the Heron Formula and then find the number of blades to create.

It would separate the density of the grass from the resolution of the mesh.

Author

That is a good suggestion indeed, especially since there’s no guarantee that all the triangles in a mesh will have the same area. I’ve been working with this effect on planes and terrains where the triangle area is kinda fixed, but with a less uniform topology having a measure like that would be really useful!

I feel that having the explanations of the lines in the actual lines, not afterwards in another section would be way more helpful.

I had to scroll back and forth between the text and the code to see what was happening in each line. It would be enough with a small explanation on code and later on continue with the full stuff, and the diagrams to explain in depth.

Great tutorial! Keep it up!

Author

Thanks for the feedback and the kind words! I’m actually a bit more fond of this format as I find that having notes between parts of the code can end up a bit distracting and confusing, at least that kinda confused me when I was starting. I think of these tutorials as more of a reference point, with the intention to grab the code, throw it in Unity and checking the post to answer any questions/issues, not so much as a reading material. Tutorials that require reading from top to bottom aren’t really my favorite too, so I wouldn’t really expect that people would actually read the whole thing in one sitting ^^”