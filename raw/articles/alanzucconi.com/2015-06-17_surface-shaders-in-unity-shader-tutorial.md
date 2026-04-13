---
title: Surface shaders in Unity - Shader tutorial
url: https://www.alanzucconi.com/2015/06/17/surface-shaders-in-unity3d/
author: Alan Zucconi
published: '2015-06-17'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

[Part 1](https://www.alanzucconi.com/2015/06/10/a-gentle-introduction-to-shaders-in-unity3d/), **Part 2**, [Part 3](https://www.alanzucconi.com/2015/06/24/physically-based-rendering-and-lighting-models-in-unity3d/), [Part 4](https://www.alanzucconi.com/2015/07/01/vertex-and-fragment-shaders-in-unity3d/), [Part 5](https://www.alanzucconi.com/2015/07/08/screen-shaders-and-postprocessing-effects-in-unity3d/)

This is the second part of a series of posts on Unity3D shaders, and it will focus on [surface shaders](http://This is the second part of a series of posts on Unity3D shaders,). As previously mentioned, shaders are special programs written in a language called Cg / HLSL which is executed by GPUs. They are used to draw triangles of your 3D models on the screen. Shaders are, in a nutshell, the code which represents how different materials are rendered. Surface shaders are introduced in Unity3D to simplify the way developers can define the look of their materials.

![Surface shader](../../assets/f208a8066b6e85db.png)

The diagram above *loosely* shows how a surface shader works. The 3D model is firstly passed to a function which can alter its geometry. Then, it is passed (together with other information) to a function which defines its “look” using some intuitive properties. Finally, these properties are used by a lighting model to determine how the geometry will be affected by the nearby light sources. The result are the RGBA colours of every pixel of the model.

### The surface function

The heart of a surface shader is its *surface function*. It takes data from the 3D model as input, and outputs its rendering properties. The following surface shader gives an object a diffuse white colour:

Shader "Example/Diffuse Simple" { SubShader { Tags { "RenderType" = "Opaque" } CGPROGRAM #pragma surface surf Lambert struct Input { float4 color : COLOR; }; void surf (Input IN, inout SurfaceOutput o) { o.Albedo = 1; // 1 = (1,1,1,1) = white } ENDCG } Fallback "Diffuse" }

![shader_01](../../assets/4a3ff89ae99fbe81.png)

**Line 5** specifies that the surface function for this shader is `surf`

and that a [Lambertian lighting model](https://en.wikipedia.org/wiki/Lambertian_reflectance) should be used. **Line 10** indicates that the *albedo* of the material, that is its base colour, should be white. The surface function doesn’t use any data from the original 3D model; despite this, Cg / HLSL requires a input struct to be defined.

#### Surface output

The struct `SurfaceOutput`

has several other properties which can be used to determine the final aspect of a material:

`fixed3 Albedo`

: the base colour / texture of an object,`fixed3 Normal`

: the direction of the face, which determines its reflection angle,`fixed3 Emission`

: how much light this object is generating by itself,`half Specular`

: how well the material reflects lights from 0 to 1,`fixed Gloss`

: how diffuse the specular reflection is,`fixed Alpha`

: how transparent the material is.

Cg / HLSL supports the traditional `float`

type, but you’ll rarely need a 32 bit precision for your calculations. When 16 bits are enough, the `half`

type is usually preferred. Since the majority of parameters have a range which goes from 0 to 1, or -1 to +1, Cg supports the `fixed`

type. It spans at least from -2 to +2, and it uses 10 bits.

For all these types, Cg / HLSL also supports *packed arrays:* `fixed2`

, `fixed3`

, and `fixed4`

. These types are optimised for parallel computation, so that most of the common operations can be performed in just one instruction. These four, for examples, are equivalent:

// Traditional C# Albedo.r = 1; Albedo.g = 1; Albedo.b = 1; // Packed arrays Albedo.rgb = fixed3(1,1,1); Albedo.rgb = 1; Albedo = 1;

### Sampling textures

Adding a texture to to a model is slightly more complicated. Before showing the code, we need to understand how texture mapping works in 3D objects. Every textured model is made up of several triangles, each one made of three vertices. Data can be stored in these vertices. They typically contain *UV* and *color data*. UV is a 2D vector which indicates which point of the texture is mapped to that vertex.

![soldier](../../assets/386d0519e08501de.png)

In the picture above you can see the model of a soldier from the Unity3D Bootcamp demo. It is rendered as shaded wireframe. Two triangles have been highlighted on the model: their vertices yield a couple of numbers. They are the Cartesian coordinates, normalised from 0 to 1, which map to the texture on the right. These numbers are the UV coordinates.

If we want to associate a texture to a 3D object, we need the UV data of its vertices. The following shader maps a texture onto a model, according its UV model.

Shader "Example/Diffuse Texture" { Properties { _MainTex ("Texture", 2D) = "white" {} } SubShader { Tags { "RenderType" = "Opaque" } CGPROGRAM #pragma surface surf Lambert struct Input { float2 uv_MainTex; }; sampler2D _MainTex; void surf (Input IN, inout SurfaceOutput o) { o.Albedo = tex2D (_MainTex, IN.uv_MainTex).rgb; } ENDCG } Fallback "Diffuse" }

![shader_02](../../assets/798519f1512caf7d.png)

The property `_MainText`

is a texture which is declared in **line 12** and made accessible from the material inspector in **line 3**. The UV data of the current pixel is gathered in **line 10**; this is done by naming a field of the `Input`

struct as `uv`

followed by the name of the texture (`uv_MainText`

, in this case).

The next step is to find the part of the texture which UV refers to. Cg / HLSL provides a useful function for this, called `tex2D`

: given a texture and some UV coordinate, it returns the RGBA colour. `tex2D`

takes into account other parameters which can be set directly from Unity3D, when importing the texture.

It is important to remember that the UV coordinate are stored only in the vertices. When the shader evaluates a pixel which is not a vertex, the function `tex2D`

interpolates the UV coordinates of the three closest vertices.

### ⭐ Recommended Unity Assets

### Surface input

Cg / HLSL has some other interesting, non-obvious features. The surface input, `Input`

, can be filled with values which Unity3D will calculate for us. For instance, adding `float3 worldPos`

will be initialised with the world position of the point `surf`

is elaborating. This is often used to creates effects which depends on the distance from a particular point.

Shader "Example/Diffuse Distance" { Properties { _MainTex ("Texture", 2D) = "white" {} _Center ("Center", Vector) = (0,0,0,0) _Radius ("Radius", Float) = 0.5 } SubShader { Tags { "RenderType" = "Opaque" } CGPROGRAM #pragma surface surf Lambert struct Input { float2 uv_MainTex; float3 worldPos; }; sampler2D _MainTex; float3 _Center; float _Radius; void surf (Input IN, inout SurfaceOutput o) { float d = distance(_Center, IN.worldPos); float dN = 1 - saturate(d / _Radius); if (dN > 0.25 && dN < 0.3) o.Albedo = half3(1,1,1); else o.Albedo = tex2D (_MainTex, IN.uv_MainTex).rgb; } ENDCG } Fallback "Diffuse" }

![shader_03](../../assets/a7831d47e4ccca03.png)

**Lines 20-21** calculated the distance of the pixel being drawn, `IN.worldPos`

, from the point we’ve defined in the material inspector, `_Center`

. Then, it clamps it between zero and one, so that is one in `_Center`

and fades to zero at `_Radius`

. If the distance falls within a certain range, pixels are coloured white.

Is worth noting that shaders are executed on GPUs, which are highly optimised for sequential code. Adding branches to a shader can dramatically lower its performance. It is often more efficient to calculate both branches and mixing the results:

float d = distance(_Center, IN.worldPos); float dN = 1 - saturate(d / _Radius); dN = step(0.25, dN) * step(dN, 0.3); o.Albedo = tex2D (_MainTex, IN.uv_MainTex).rgb * (1-dN) + half3(1,1,1) * dN;

Cg / HLSL has lot of built-in functions, such as [saturate](http://http.developer.nvidia.com/Cg/saturate.html) and [step](http://http.developer.nvidia.com/Cg/step.html), which can easily replace the majority of if statements.

#### Other inputs

Cg allows to use several other special fields such as `worldPos`

; here’s a list of the most used according to Unity3D [official documentation](http://docs.unity3d.com/Manual/SL-SurfaceShaders.html):

`float3 viewDir`

: the direction of the camera (*view direction*);`float4 name : COLOR`

: by using this syntax, the variable`name`

will contain the colour of the vertex;`float4 screenPos`

: the position on the current pixel on the screen;`float3 worldPos`

: the position of the current pixel, in world coordinates.

### Vertex function

Another interesting feature of surface shaders is the ability to change vertices before sending them to `surf`

. While `surf`

manipulates colours in the RGBA space, to use a *vertex modifier* function you need to learn how to manipulate 3D points in space. Let’s start with an easy example: a shader which makes a 3D model …chubbier. To do this, we have to expand the triangles along the direction they’re facing (think about a balloon which is inflated). The direction of a triangle it’s given by its *normal*, which is a unit vector perpendicular to the surface of the triangle itself. If we want to extend its vertices in the direction of its normal, what we have to do it:

![Rendered by QuickLaTeX.com \[newVertex = vertex + normal * amount\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-6d685b03ae4a3ba06584321027b379d8_l3.png)


where ![Rendered by QuickLaTeX.com amount](../../assets/fbae367133bba178.png)

*normal extrusion*.

Shader "Example/Normal Extrusion" { Properties { _MainTex ("Texture", 2D) = "white" {} _Amount ("Extrusion Amount", Range(-0.0001,0.0001)) = 0 } SubShader { Tags { "RenderType" = "Opaque" } CGPROGRAM #pragma surface surf Lambert vertex:vert struct Input { float2 uv_MainTex; }; float _Amount; void vert (inout appdata_full v) { v.vertex.xyz += v.normal * _Amount; } sampler2D _MainTex; void surf (Input IN, inout SurfaceOutput o) { o.Albedo = tex2D (_MainTex, IN.uv_MainTex).rgb; } ENDCG } Fallback "Diffuse" }

![soldier.gif](../../assets/63a6c9d359aa8e9c.gif)

**Line 9** specifies that there is a *vertex modifier*, called `vert`

. It takes the position of a vertex and it projects it along its normal. `appdata_full`

is a struct which contains all the data of the current vertex.

### Putting all together: the snow shader

A typical surface shader which uses both `surf`

and `vert`

is the ~~in~~famous snow effect, which appeared in [several blogs](http://studio.openxcell.com/create-snow-effect-using-shaders-unity.html), each time with a slightly different flavour. It simulates the accumulation of snow on the triangles of a model. Initially only the triangles directly facing `_SnowDirection`

are affected. By increasing `_Snow`

, even the triangles which are not oriented towards the sky are eventually affected.

![dot product (2)](../../assets/46f67f5a6ad9f382.png)

First of all, we need to understand when a triangle is oriented towards the sky. The direction the snow is coming from, `_SnowDirection`

, will be a unit vector as well. There are many ways in which we can check how aligned they are, but the easiest one is projecting the normal onto the snow direction. Since both vectors have length one, the resulting quantity will be bounded between +1 (same direction) and -1 (opposite direction). We’ll encounter this quantity again in the next tutorial, but for now you just have to know that is known as *dot* product and equal to ![Rendered by QuickLaTeX.com cos(\theta)](../../assets/61e99a4f133d1bf0.png)

`_Snow`

, means that we are only interested in the normals which differ, in direction, less then ![Rendered by QuickLaTeX.com \theta](../../assets/b55496429621e4ab.png)



is true only when the two directions are the same;

is true when

is less then 90 degrees;

is always true.

There’s another little piece of information which is needed. While `_SnowDirection`

represents a direction expressed in *world coordinates*, normals are generally expressed in *object coordinates*. We cannot compare these two quantities directly, because they are mapped to different coordinate systems. Unity3D provides a function called `WorldNormalVector`

which can be used to map normals into world coordinates.

Shader "Example/SnowShader" { Properties { _MainColor ("Main Color", Color) = (1.0,1.0,1.0,1.0) _MainTex ("Base (RGB)", 2D) = "white" {} _Bump ("Bump", 2D) = "bump" {} _Snow ("Level of snow", Range(-1, 1)) = 1 _SnowColor ("Color of snow", Color) = (1.0,1.0,1.0,1.0) _SnowDirection ("Direction of snow", Vector) = (0,1,0) _SnowDepth ("Depth of snow", Range(0,0.0001)) = 0 } SubShader { Tags { "RenderType"="Opaque" } LOD 200 CGPROGRAM #pragma surface surf Lambert vertex:vert sampler2D _MainTex; sampler2D _Bump; float _Snow; float4 _SnowColor; float4 _MainColor; float4 _SnowDirection; float _SnowDepth; struct Input { float2 uv_MainTex; float2 uv_Bump; float3 worldNormal; INTERNAL_DATA }; void vert (inout appdata_full v) { // Convert _SnowDirection from world space to object space float4 sn = mul(_SnowDirection, _World2Object); if(dot(v.normal, sn.xyz) >= _Snow) v.vertex.xyz += (sn.xyz + v.normal) * _SnowDepth * _Snow; } void surf (Input IN, inout SurfaceOutput o) { half4 c = tex2D (_MainTex, IN.uv_MainTex); o.Normal = UnpackNormal (tex2D (_Bump, IN.uv_Bump)); if(dot(WorldNormalVector(IN, o.Normal), _SnowDirection.xyz)>=_Snow) o.Albedo = _SnowColor.rgb; else o.Albedo = c.rgb * _MainColor; o.Alpha = 1; } ENDCG } FallBack "Diffuse" }

![soldier_4](../../assets/6fa93369e1c07833.png)

Rather the manually calculating the cosine of the angle between the vector, Cg has a very efficient implementation of the dot product called `dot`

.

**Line 36** utilises a different method to convert the normal into world coordinates. The function `WorldNormalVector`

is in fact not available in the vertex modifier.

If you really need snow in your game, consider buying something more advanced, like this:

### Conclusion

This post introduces surface shaders and shows how they can be used for a variety of effects. This post was inspired by the [Surface Shader Examples](http://docs.unity3d.com/Manual/SL-SurfaceShaderExamples.html) page in the Unity3D manual. There is also another page which explains in details how to implement [other lighting models](http://docs.unity3d.com/Manual/SL-SurfaceShaderLightingExamples.html). That topic will be explored in details in the third part of this tutorial.

- Part 1:
[A gentle introduction to shaders in Unity3D](https://www.alanzucconi.com/2015/06/10/a-gentle-introduction-to-shaders-in-unity3d/) - Part 2:
**Surface shaders in Unity3D** - Part 3:
[Physically Based Rendering and lighting models in Unity3D](https://www.alanzucconi.com/2015/06/24/physically-based-rendering-and-lighting-models-in-unity3d/) - Part 4:
[Vertex and fragment shader in Unity3D](https://www.alanzucconi.com/2015/07/01/vertex-and-fragment-shaders-in-unity3d/) - Part 5:
[Screen shaders and postprocessing effects in Unity3D](https://www.alanzucconi.com/2015/07/08/screen-shaders-and-postprocessing-effects-in-unity3d/)

## Leave a Reply Cancel reply