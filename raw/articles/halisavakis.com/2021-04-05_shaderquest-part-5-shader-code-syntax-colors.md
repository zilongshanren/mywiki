---
title: 'ShaderQuest Part 5: Shader code syntax & Colors'
url: https://halisavakis.com/shaderquest-part-5-shader-code-syntax-colors/
published: '2021-04-05'
source_blog: Technically Art – Harry Alisavakis
source_site: https://halisavakis.com
category: graphics
fetched: '2026-04-13'
---

## Patrons

The 5th part of ShaderQuest is brought to you by these awesome Patrons:

- Not Invader Zim
- orels1
- Sergey Gonchar
- Tiph’ (DN)

## Introduction

This part is going to combine two subjects as I thought that a part on each individual subject would end up a bit short. The first part is going to cover some stuff around the syntax of shader code languages while in the second part we’ll take a look at how colors work in the context of shaders.

In the second part we’ll finally start modifying a shader and seeing stuff changing on our objects!

## Shader code syntax

As I mentioned in [a previous ShaderQuest part](https://halisavakis.com/shaderquest-part-2-introducing-shaders/), there’s some different shader coding languages out there with the more common being CG, HLSL and GLSL. There might be some very small differences in their syntax, but all shader coding languages are very similar in many ways, especially in the key elements I’ll be mentioning here.

### Data types

Shaders mostly operate with floating point fields and vectors. The more common data types you find in other programming languages can also be found here, like `float`

and `int`

. The differences begin when we’re looking into vectors.

In CG and HLSL, an N-dimensional vector can be declared as `floatN`

, where N is the dimension ranging from 2 to 4. So in CG and HLSL, the main vector data types look like this:

Dimensions | Data type |
| 2 | `float2` |
| 3 | `float3` |
| 4 | `float4` |

One key difference with CG/HLSL and GLSL is that in GLSL, instead of using `floatN`

, vector data types are written as `vecN`

. So in GLSL, vector data types look like this:

Dimensions | Data type |
| 2 | `vec2` |
| 3 | `vec3` |
| 4 | `vec4` |

It’s also worth mentioning that CG and HLSL can use different types for floating point numbers and vectors based on the desired precision. Specifically, instead of `float`

, which offers the highest precision, we can use `half`

for medium precision or `fixed`

for low precision. Consequently, the respective vectors can be written like so:

Dimensions | Half precision | Fixed precision |
| 2 | `half2` | `fixed2` |
| 3 | `half3` | `fixed3` |
| 4 | `half4` | `fixed4` |

You can find more on data precision in [Unity’s official manual](https://docs.unity3d.com/Manual/SL-DataTypesAndPrecision.html).

### Creating Vectors

Creating vectors in shader code is pretty straightforward; it’s as if you’re creating a vector object without the need for the `new`

keyword.

So, if we want to create a vector in CG/HLSL we can just say:

`float3 vector = float3(0.5, 0.6, 0.7);`


The same vector in GLSL can be created like so:

`vec3 vector = vec3(0.5, 0.6, 0.7);`


Another key difference between CG/HLSL and GLSL is that **all explicitly typed numeric values in GLSL need to have a decimal point if they correspond to a float/vec data type.** So, while in CG and GLSL we can say

`float x = 2;`


in GLSL we have to say

`float x = 2.0;`


If we want to create vectors that have the same value in each component we can declare that implicitly in different ways for CG/HLSL and GLSL:

CG/HLSL – `float4 c = 0.5;`


GLSL – `vec4 c = vec4(0.5);`


That’s a very subtle difference, but if you’re bringing shaders written in GLSL into Unity, it’s something that’s worth noting.

### Implicit truncation

That’s a small thing, but it’s handy to know it if it’s going to offer you a little peace of mind. The value of a higher dimension vector can be assigned to a field of a lower dimension data type, but the latter will just keep the components of the former in order.

An example will make it a bit clearer:

`float4 v = float4(0.2, 0.3, 0.4, 0.5);`


`float2 c = v;`


That’s allowed and will cause the vector `c`

to have an x component with the value of 0.2 and a y component with the value of 0.3. That doesn’t work just for vectors but for `float`

fields too (which can be considered one-dimensional vectors).

### Swizzling

You are going to love this, swizzling is probably my favorite thing in shaders.

Swizzling is the ability to compose vectors by arbitrarily rearranging and combining components of other vectors. You can access the components of a vector in any order and even use the components more than once to create new vectors.

Some examples of swizzling to better understand the concept:

fixed4 sw1 = fixed4(0.1, 0.2, 0.3, 0.4); fixed4 sw2 = sw1.xzyw; fixed4 sw3 = sw1.zzyx; fixed3 sw4 = fixed3(sw2.zw, sw3.x);

Do take note of that last line; swizzling allows the construction of vectors using other, lower dimension vectors. The order doesn’t matter, it’s total anarchy!

## Colors in shaders

Colors in shaders are not represented with any special structure or data type; instead they behave exactly like a 4-dimensional vector, where each component corresponds to the value of a color channel, specifically **red, green, blue and alpha**, in this order. Their representation is similar to an RGBA color scheme you see on any graphics related program, with the main difference that instead of having values in the `(0, 255)`

range, the values of the color channels in shaders range from `0.0`

to `1.0`

.

Therefore, we can represent the white color like so:

`fixed4 whiteColor = fixed4(1.0, 1.0, 1.0, 1.0);`


Since colors are represented with simple numbers we can perform normal math operations on them, such as addition and multiplication, which will make the colors blend in different ways. In case you haven’t guessed it already, the “Add” and “Multiply” layer modes you find in image processing software like Adobe Photoshop just perform these math operations on the colors in the same way.

Let’s see how colors are used in action!

### ShaderLab

In ShaderLab shaders the importance of colors is a bit more apparent compared to visual shader creation systems. As I’ve mentioned, the purpose of a shader is, in most cases, to throw a color on your screen. This is very apparent when you take a look at the `frag`

method of a newly created unlit shader:

```
Shader "Unlit/Colors"
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
#pragma fragment frag
// make fog work
#pragma multi_compile_fog
#include "UnityCG.cginc"
struct appdata
{
float4 vertex : POSITION;
float2 uv : TEXCOORD0;
};
struct v2f
{
float2 uv : TEXCOORD0;
UNITY_FOG_COORDS(1)
float4 vertex : SV_POSITION;
};
sampler2D _MainTex;
float4 _MainTex_ST;
v2f vert (appdata v)
{
v2f o;
o.vertex = UnityObjectToClipPos(v.vertex);
o.uv = TRANSFORM_TEX(v.uv, _MainTex);
UNITY_TRANSFER_FOG(o,o.vertex);
return o;
}
fixed4 frag (v2f i) : SV_Target
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

The method returns a `fixed4`

which is the color that will end up on our screen in the specific pixel that’s being processed.

The default `frag`

method is using a texture but we don’t care about that, so let’s make it return a fixed color by replacing its contents like so:

```
fixed4 frag (v2f i) : SV_Target
{
fixed4 col = fixed4(1.0, 0.0, 0.0, 1.0);
return col;
}
```

This will assign 1.0 to the red channel and 0.0 to every other color channel (alpha excluded), so if you create a material with this shader and assign it to a sphere, you’ll get this result:

![](../../assets/a5a20d76511c1b20.png)

This color, however, is hard-coded right now, so let’s mix it up with some editor control.

We can add a color property in the `Properties`

block named “`_Color`

” and add it to our hardcoded color:

```
Properties
{
_MainTex ("Texture", 2D) = "white" {}
_Color("Color", Color) = (0,0,0,1)
}
```

I’m defaulting its value to (0,0,0,1) because I’m adding it to the red color.

In order to use that property in our shader though, we’ll have to declare it in the CGPROGRAM block as well:

```
sampler2D _MainTex;
float4 _MainTex_ST;
fixed4 _Color;
```

Finally, we can add the `_Color`

property to our color like so:

```
fixed4 frag (v2f i) : SV_Target
{
fixed4 col = fixed4(1.0, 0.0, 0.0, 1.0);
col += _Color;
return col;
}
```

Now you can control the color that’s being added to the hardcoded red through the inspector, and get this result:

![](../../assets/5f19704330ae3e54.gif)

If we wanted to multiply the colors instead, we’d use

`col *= _Color;`


instead of

`col += _Color;`


Due to the additive nature of the colors it’s a bit harder to get control over the final color like that, but you could just return the value of `_Color`

to get the exact color you see in the inspector.

Here’s the full, modified shader:

```
Shader "Unlit/Colors"
{
Properties
{
_MainTex ("Texture", 2D) = "white" {}
_Color("Color", Color) = (0,0,0,1)
}
SubShader
{
Tags { "RenderType"="Opaque" }
LOD 100
Pass
{
CGPROGRAM
#pragma vertex vert
#pragma fragment frag
// make fog work
#pragma multi_compile_fog
#include "UnityCG.cginc"
struct appdata
{
float4 vertex : POSITION;
float2 uv : TEXCOORD0;
};
struct v2f
{
float2 uv : TEXCOORD0;
UNITY_FOG_COORDS(1)
float4 vertex : SV_POSITION;
};
sampler2D _MainTex;
float4 _MainTex_ST;
fixed4 _Color;
v2f vert (appdata v)
{
v2f o;
o.vertex = UnityObjectToClipPos(v.vertex);
o.uv = TRANSFORM_TEX(v.uv, _MainTex);
UNITY_TRANSFER_FOG(o,o.vertex);
return o;
}
fixed4 frag (v2f i) : SV_Target
{
fixed4 col = fixed4(1.0, 0.0, 0.0, 1.0);
col += _Color;
return col;
}
ENDCG
}
}
}
```

### Shader Graph

Here’s how the shader above gets translated in an unlit Shader Graph:

![](../../assets/2d895009b2ae33e4.png)

I added a Color node and set it to red for our hardcoded (or, I guess, hardnoded – © Harry Alisavakis, 2021) color and I created a property named “Color” which I’m adding to the red color via an “Add” node.

The default value of the “Color” property is set via the “Node settings” tab:

![](../../assets/b4b26ba89e30683e.png)

Make sure the “Exposed” checkbox is enabled so you can see the property in the material inspector.

### ASE

The same shader is very similar in ASE as well. We’ll have to use two “color” nodes and one “add” node to get the additive colors result.

![](../../assets/d6aeb63092cfd8d8.png)

Do note that “Color” here has its type set to “Property” in order to be exposed, while “Color 0” is set to constant.

![](../../assets/b30a9c79f1b24056.png)

### UE4

In order to get the same result in UE4 we’ll need an unlit material and, again, two nodes for the colors and a node to add the two.

To set the material to be unlit we have to set the shading model to “Unlit” from the material details tab:

![](../../assets/2060fe503ea8385a.png)

The final material graph looks like this:

![](../../assets/45cc0a0d045c8865.png)

In UE material editor, there’s no “Color” node; vector nodes are used for colors instead. The red color is made with a 3-dimensional vector node, while the Color parameter node is made with another 3-dimensional vector that has been converted to a parameter:

![](../../assets/9b847d80b6a5a18b.png)

The master node of the UE material editor enables and disables inputs based on the properties of the material (like the shading model). For unlit materials the “emissive color” input is used as the output color instead of “base color”, since unlit surfaces are usually treated as emissive to avoid getting any shading.

In order to change the value of the “Color” parameter keep in mind that you’ll have to make a material instance of the original material and adjust it from there:

![](../../assets/626e75e858e5615a.gif)

## Conclusion

That’s it for this one! While this first custom shader wasn’t complicated at all I wanted to start small to more easily see the similarities between the different node-based systems and the shaderlab code. Additionally, even if the first part was more code-specific, keeping in mind some of the inner workings of shader code will come in handy when working with visual interfaces as well.

Now that we started modifying and creating shaders from scratch we’ll start diving into more interesting subjects soon. Until then, see you in the[ next part of ShaderQuest](https://halisavakis.com/shaderquest-part-6-shaping-functions/) ❗