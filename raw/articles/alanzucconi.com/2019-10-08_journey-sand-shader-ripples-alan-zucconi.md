---
title: 'Journey Sand Shader: Ripples - Alan Zucconi'
url: https://www.alanzucconi.com/2019/10/08/journey-sand-shader-6/
author: Alan Zucconi
published: '2019-10-08'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This is the sixth part of the online series dedicated to Journey Sand Shader.

- Part 1.
[A Journey Into Journey’s Sand Shader](https://www.alanzucconi.com/?p=10050) - Part 2.
[Journey Sand Shader: Diffuse Colour](https://www.alanzucconi.com/?p=10052) - Part 3.
[Journey Sand Shader: Sand Normal](https://www.alanzucconi.com/?p=10054) - Part 4.
[Journey Sand Shader: Specular Reflection](https://www.alanzucconi.com/?p=10057) - Part 5.
[Journey Sand Shader: Glitter Reflection](https://www.alanzucconi.com/?p=10059) **Part 6.**[Journey Sand Shader: Sand Ripples](https://www.alanzucconi.com/?p=10061)

In this final post, we will recreate the typical sand ripples that appear due to the dune-wind interaction.

![](../../assets/b11a21c01c7746a6.png)

This last article is dedicated to sand ripples, which are commonly seen on dunes which have been exposed to wind.

Conceptually, it would have made sense having this tutorial after [Journey Sand Shader: Sand Normal](https://www.alanzucconi.com/?p=10054). The reason why it has been kept last, is because it is the most complex effect so far. Part of the complexity comes from the way in which normal maps are stored and processed in a Surface shader, which makes a lot of extra steps necessary.

## Normal Mapping

In a previous lecture of this online course, we have explored how the dishomogeneous look of the sand was achieved. In [Journey Sand Shader: Sand Normal](https://www.alanzucconi.com/?p=10054), a very common technique called **normal mapping** was used to alter how the light interacts with the geometry surface. This is often used in 3D graphics to give the illusion something has a more complex geometry, typically to make curved surfaces appear smoother (below).

![](../../assets/94dd95bb02f27828.png)

To achieve such an effect, each pixel is associated with a **normal direction**, that indicates its orientation. That, instead of the actual orientation of the mesh, is used in the light calculation.

By reading the normal directions from seemingly random texture, we were able to simulate a grainy look. While not physically accurate, it is still very believable.

## Sand Ripples

Sand dunes, however, exhibit another particular feature that cannot be ignored: ripples. Each dune features smaller dunes, which are caused by the interaction with the wind, and held together by the friction between the individual grains of sand.

![](../../assets/0d088be1f69863fa.jpg)

These ripples are very obvious, and can be seen in most dunes. In the image below, taken in Oman, you can see that the dune in the foreground has a strong wavey pattern.

These ripples change dramatically based not just on the shape of the dune, but also on its composition and the direction and speed of the wind. Most dunes that have a sharp peak, typically present ripples only on one side (below).![](../../assets/5d8d2cf13769d7e0.jpg)


The effect presented in this tutorial is designed for more softer dunes, that will have ripples on both sides. This is not always physically accurate, but is realistic enough to be believable and is a first good step towards more refined implementations.

## Implementing Ripples…

There are many ways in which these ripples could be added. The cheapest would be to draw then on a texture, but that is not what we will do in this tutorial. The reason is simple: the ripples are not “flat”, but should correctly interact with the light. Simply drawing them would not produce a realistic effect when the camera (or the sun) is moving.

Another way to add those ripples could be editing the geometry of the dune model. But increasing the model complexity is not recommended, as it can take a heavy toll on the overall performance.

As seen in [Journey Sand Shader: Sand Normal](https://www.alanzucconi.com/?p=10054), we can get around this problem using *normal maps*. They are effectively drawn onto the surface as a traditional texture would, but they are used in the lighting calculations to simulate a more complex geometry of the one actually present.

The problem has now shifted to a new one: creating these normal maps. Manually drawing them would be exceptionally time-consuming. On top of that, every time a dune is changed, the ripples would have to be re-drawn. This would significantly slow down the asset creation, and so it something that many technical artists try to avoid.

A much more efficient and effective solution is to add these ripples *procedurally*. This means that, based on the local geometry, the normal direction of a dune is altered to take into account not only the grains of sand, but also the ripples.

Since the ripples will need to simulate a 3D surface, it makes sense for them to be implemented altering the normal direction of each pixel. For this, the easier approach is to rely on a tileable normal map with a wavey pattern. This map will then be combined with the existing normal map previously used for the sand.

## Normal Mapping

Up to this point, we have encounter three different *normals*:

**Geometry normal**: the orientation of each face of the 3D model, which is stored directly in the vertices;**Sand normal**: calculated in[Journey Sand Shader: Sand Normal](https://www.alanzucconi.com/?p=10054)using a noisy texture;**Ripple normal**: the new effect that we are discussing in this article.

The example below, taken from Unity’s [Surface Shader examples](https://docs.unity3d.com/Manual/SL-SurfaceShaderExamples.html) page, show the typical way in which a 3D model’s normal can be overwritten. This requires to change the value of `o.Normal`

, which is usually done after sampling a texture (usually called a **normal map**).

Shader "Example/Diffuse Bump" { Properties { _MainTex ("Texture", 2D) = "white" {} _BumpMap ("Bumpmap", 2D) = "bump" {} } SubShader { Tags { "RenderType" = "Opaque" } CGPROGRAM #pragma surface surf Lambert struct Input { float2 uv_MainTex; float2 uv_BumpMap; }; sampler2D _MainTex; sampler2D _BumpMap; void surf (Input IN, inout SurfaceOutput o) { o.Albedo = tex2D (_MainTex, IN.uv_MainTex).rgb; o.Normal = UnpackNormal (tex2D (_BumpMap, IN.uv_BumpMap)); } ENDCG } Fallback "Diffuse" }

That is exactly the technique that we have used to replace the geometry normal with the sand normal in [Journey Sand Shader: Sand Normal](https://www.alanzucconi.com/?p=10054).

### ⭐ Recommended Unity Assets

## Dune Steepness

The first challenge, however, comes from the fact that the shape of the ripples changes based on the dune inclination. Shallow, flat dunes feature gentle ripples; steep dunes present more pronounced wavey patterns. This means that the *steepness* of a dune needs to be taken into consideration.

The easiest way to work around this is, to have two different normal maps, for shallow and steep dunes, respectively. The main idea behind this effect is to blend between these two normal maps, based on the steepness of a dune.

![]() Steep Normal Map | ![]() Shallow Normal Map |


![](../../assets/5e1afb99d3b81633.png)

The steepness can be calculated using the **dot product**, which is commonly used in shader coding to calculate how “aligned” two directions are. In this case, we can take the normal direction of the geometry (below, blue), and compare it with a vector that points towards the sky (below, yellow). The dot product between these two vectors will return values close to ![Rendered by QuickLaTeX.com 1](../../assets/da6d507f7a2bceae.png)

![Rendered by QuickLaTeX.com 0](../../assets/621a9e9e59af40e4.png)


![](../../assets/1159a6ddb7bc3bda.png)

The first problem that we encounter, however, is about the two vectors involved in the operation. The normal vector accessible from the `surf`

function via `o.Normal`

is expressed in **tangent space**. This means that the **frame of reference** used to encode the normal direction is relative to the local surface geometry (below). We have briefly touched this subject in [Journey Sand Shader: Sand Normal](https://www.alanzucconi.com/?p=10054).

The vector that points towards the sky, instead, is expressed in **world space**. In order for the dot product to work as expected, both the vectors need to be expressed in the same frame of reference. This means that we need to convert one of them, so that they are both expressed in the same space.

Luckily, Unity comes to the rescue with a function called `WorldNormalVector`

, which allows converting a normal vector from *tangent space* to *world space*. In order for this function to work, we need to change the `Input`

structure, so that it includes both `float3 worldNormal`

and `INTERNAL_DATA`

, as seen below:

struct Input { ... float3 worldNormal; INTERNAL_DATA };

This is explained in Unity’s [Writing Surface Shaders](https://docs.unity3d.com/Manual/SL-SurfaceShaders.html), where it stated that:

`float3 worldNormal; INTERNAL_DATA`

– contains world normal vector if surface shader writes to `o.Normal`

.

To get the normal vector based on per-pixel normal map, use `WorldNormalVector (IN, o.Normal)`

.

This is often a major source of confusion when writing surface shaders. Basically, the value of `o.Normal`

available in the `surf`

function *changes,* based on how it is used. If you are only reading it, `o.Normal`

contains the *normal vector *of the current pixel, in *world space*. If you are changing its value, `o.Normal`

is in *tangent space* instead.

If you are writing to `o.Normal`

but still need to access the normal in *world space* (like we do now), then you can use `WorldNormalVector (IN, o.Normal)`

. This, however, requires the small change to the `Input`

structure seen above.

### Implementation

The piece of code below converts the normal from *tangent* to *world space*, and calculates the steepness with respect to the *up direction*.

// Calculates normal in world space float3 N_WORLD = WorldNormalVector(IN, o.Normal); float3 UP_WORLD = float3(0, 1, 0); // Calculates "steepness" // => 0: steep (90 degrees surface) // => 1: shallow (flat surface) float steepness = saturate(dot(N_WORLD, UP_WORLD));

Now that the steepness of the dune is calculated, we can use it to blend the two normal maps. Both the shallow and steep normal maps (called `_ShallowTex`

and `_SteepTex`

in the snippet below) are sampled. Then, they are blended based on the value of `steepness`

:

float2 uv = W.xz; // [0,1]->[-1,+1] float3 shallow = UnpackNormal(tex2D(_ShallowTex, TRANSFORM_TEX(uv, _ShallowTex))); float3 steep = UnpackNormal(tex2D(_SteepTex, TRANSFORM_TEX(uv, _SteepTex ))); // Steepness normal float3 S = normalerp(steep, shallow, steepness);

As previously discussed in [Journey Sand Shader: Sand Normal](https://www.alanzucconi.com/?p=10054), correctly combining normal maps is rather tricky, and cannot be done using `lerp`

. While `slerp`

would be the correct function to use in this case, a cheaper version called `normalerp`

is used instead.

### Ripple Blending

If we use the code above, the results might be quite underwhelming. That is because dunes tend to have a very gentle steep, which causes the two normal textures to overmix. To correct that, we can apply a non-linear transformation to the steepness, which would increase the sharpness of the blending:

// Steepness to blending steepness = pow(steepness, _SteepnessSharpnessPower);

When blending two textures, `pow`

is often used to modulate their sharpness and contrast. We have how and why this works in an earlier tutorial dedicated to [Physically Based Rendering](https://www.alanzucconi.com/2015/06/24/physically-based-rendering/).

Below, you can see two gradients. The one on the top shows colours from black to white, linearly interpolated on the X axis using `c = uv.x`

. Below, the same gradient is presented but using `c = pow(uv.x*1.5)*3.0`

:

![]() |
![]() |

It is easy to see that `pow`

allows creating a sharper transition between black and white. When textures are involved, this reduces their overlapping, creating cleaner edges and producing.

## Dune Direction

Everything that has been done so far works perfectly. But there is one final issue that we need to address. The ripples change depending on the *steepness*, but not on the *direction*. As discussed before, ripples tend not to be symmetrical, due to the fact that the wind usually blows predominantly in one direction.

To make the ripples even more realistic, we should add other two normal maps (table below). They can be blended based on the relative alignment of the dune with respect to the X axis, or the Z axis.

Steep | Shallow | |
X | steep x | shallow x |
Z | steep z | shallow z |

What we need to implement this final change is to calculate the alignment of a dune with respect to the Z axis. This can be done similarly to the steepness calculation, but instead of using `float3 UP_WORLD = float3(0, 1, 0);`

, we can use `float3 Z_WORLD = float3(0, 0, 1);`

instead.

I will leave this final step to you. And if there is any issue, there is a link to download the complete Unity package at the end of this tutorial.

## Conclusion

This final part of the online series about the sand rendering in Journey, we have covered how ripples can be created on the dunes, based on their inclination.

Below, you can see how far we have gone with this series:

The rest of the series is also available on this blog:

- Part 1.
[A Journey Into Journey’s Sand Shader](https://www.alanzucconi.com/?p=10050) - Part 2.
[Journey Sand Shader: Diffuse Colour](https://www.alanzucconi.com/?p=10052) - Part 3.
[Journey Sand Shader: Sand Normal](https://www.alanzucconi.com/?p=10054) - Part 4.
[Journey Sand Shader: Specular Reflection](https://www.alanzucconi.com/?p=10057) - Part 5.
[Journey Sand Shader: Glitter Reflection](https://www.alanzucconi.com/?p=10059) **Part 6.**[Journey Sand Shader: Sand Ripples](https://www.alanzucconi.com/?p=10061)

I wanted to thank you all for sticking with this rather long series. I hope you had fun learning and reimplementing this shader. And if you end up using it in one of your games or project, please do not hesitate to get in touch with me.

### Credits

The videogame [Journey](http://thatgamecompany.com/journey/) is developed by **Thatgamecompany** and published by **Sony Computer Entertainment**. It is available for PC ([Epic Store](https://www.epicgames.com/store/en-US/product/journey/home)) and PS4 ([PS Store](https://www.playstation.com/en-gb/games/journey-ps4/)).

The 3D models of the dunes, backgrounds and lighting settings were made by [Jiadi Deng](https://github.com/AtwoodDeng/JourneySand).

The 3D model of the Journey’s player was found on the (now closed) FacePunch forum.

## Download Unity Package

[Become a Patron!](https://www.patreon.com/bePatron?u=850572)

If you want to recreate this effect, the full Unity package is available for download on [Patreon](https://www.patreon.com/posts/30540389/). It includes everything needed, from the shaders to the 3D models.

## Leave a Reply Cancel reply