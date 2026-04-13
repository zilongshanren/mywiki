---
title: 'Journey Sand Shader: Sand Normal - Alan Zucconi'
url: https://www.alanzucconi.com/2019/10/08/journey-sand-shader-3/
author: Alan Zucconi
published: '2019-10-08'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This is the third part of the online series dedicated to Journey Sand Shader.

- Part 1.
[A Journey Into Journey’s Sand Shader](https://www.alanzucconi.com/?p=10050) - Part 2.
[Journey Sand Shader: Diffuse Colour](https://www.alanzucconi.com/?p=10052) **Part 3.**[Journey Sand Shader: Sand Normal](https://www.alanzucconi.com/?p=10054)- Part 4.
[Journey Sand Shader: Specular Reflection](https://www.alanzucconi.com/?p=10057) - Part 5.
[Journey Sand Shader: Glitter Reflection](https://www.alanzucconi.com/?p=10059) - Part 6.
[Journey Sand Shader: Sand Ripples](https://www.alanzucconi.com/?p=10061)

In this third post, we will focus on the normal mapping that will turn smooth 3D models into sandy dunes.

In the previous part of this online course, we have implemented the diffuse lighting of Journey’s sand. With that effect alone, the desert dunes would appear rather flat and dull.

![](../../assets/8a24ed742f7e173c.png)

One of the most intriguing effects that can be seen in Journey is the granularity of the sand. By looking at any screenshot, we have the impression that the dunes are not smooth and homogeneous; they are made out of millions of microscopic grains of sand.

![](../../assets/8d0dd409d4badb51.jpg)

This effect can be achieved using a technique called **bump mapping**, which allows light to reflect on a flat surface as it would on a more complex one. You can see how this effect changes the rendering below:

You can appreciate the subtle differences in the zoomed boxes below:

![]() | ![]() |

## Understanding Normal Mapping

Sand is made out of countless grains, all different in shape and composition (below). Each individual grain reflects light in a potentially random direction. One way to achieve such an effect would be to create a 3D model that contains all of those microscopic grains. That is infeasible, due to the immense number of polygons it would require.

There is another solution, which is often used to simulate a more complex geometry than the one that a 3D model actually has. Each vertex or face of a 3D model is associated with a parameter called its **normal direction**. This is a vector of length one, that is used to calculate how light reflects on the surface of the 3D model. Modelling sand means modelling the seemingly random distribution of those grains and, consequently, the way they affect the surface normals.

![](../../assets/652b00327d04f187.jpg)

There are countless ways in which this could be done. The most simple is to author a texture to alter the original normal directions of the dune’s model.

The **surface normal**, ![Rendered by QuickLaTeX.com N](../../assets/76bbbd804dc6db36.png)

**normal map**. Normal maps are textures that allow simulating a more complex geometry than the one actually present, by changing the local orientation of the surface normals. This technique is often called **bump mapping**.

Altering the normals is a relatively easy task, that can be done in the `surf`

function of a **surface shader**. This function receives two parameters, one of which is a `struct`

called `SurfaceOutput`

. It contains all the properties necessary to draw a part of the 3D model, from its colour (`o.Albedo`

) to its transparency (`o.Alpha`

). Another parameter it contains is the normal direction (`o.Normal`

), which can be overwritten to alter how light will reflect on the model.

Following Unity’s documentation on surface shaders ([Writing Surface Shaders](https://docs.unity3d.com/Manual/SL-SurfaceShaders.html)), all normals written to the `o.Normal`

field of `SurfaceOutput`

must be expressed in **tangent space**:

struct SurfaceOutput { fixed3 Albedo; // diffuse color fixed3 Normal; // tangent space normal, if written fixed3 Emission; half Specular; // specular power in 0..1 range fixed Gloss; // specular intensity fixed Alpha; // alpha for transparencies };

This is a way of saying that the unit vectors must be expressed in a coordinate system that is relative to the actual normal of the mesh. For instance, writing `float3(0, 0, 1)`

to `o.Normal`

leaves the normal unchanged.

void surf (Input IN, inout SurfaceOutput o) { o.Albedo = _SandColor; o.Alpha = 1; o.Normal = float3(0, 0, 1); }

That is because the vector `float3(0, 0, 1)`

is indeed the normal vector, expressed relative to the 3D model geometry.

So, all we need to do to alter the surface normal in a **surface shader** is to write the new vector to `o.Normal`

in the **surface function**:

void surf (Input IN, inout SurfaceOutput o) { o.Albedo = _SandColor; o.Alpha = 1; o.Normal = ... // change the normal here }

The rest of this post will provide an initial approximation, which will be further expanded in the sixth instalment of this series: [Journey Sand Shader #6: Sand Ripples](https://www.alanzucconi.com/?p=10061).

### ⭐ Recommended Unity Assets

## Sand Normal

The most problematic part is to understand *how* the grains of sand are altering the surface normal. While it is true that, individually, each grain can scatter light in any direction, this is not what happens overall. Any physically-based approach should study the distribution of normal vectors on a patch of sand, and modelling that mathematically. While there are indeed models that do that, the solution presented in this course is much simpler, yet very effective.

For each point on the model, a **random unit vector **is sampled from a texture. Then, the surface normal is tilted towards that vector by a certain amount. By carefully authoring the random texture and choosing an appropriate blending amount, we can perturb the surface normal just enough to add a grainy feeling to it, without losing the overall curvature of the dunes.

Random values can be sampled using a texture filled with random colours. The R, G and B components of each pixel are used as the X, Y and Z components of a normal vector. Colour components are in the range ![Rendered by QuickLaTeX.com \left[0, 1\right]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-ac0ef5000a04390b73f0f437f914143d_l3.png)

![Rendered by QuickLaTeX.com \left[-1,+1\right]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-ae9ff7abb09a3e5a1f27ed8b3ef28b87_l3.png)

![Rendered by QuickLaTeX.com 1](../../assets/da6d507f7a2bceae.png)


![](../../assets/f071d312b461d988.png)

## Implementation

The previous part of this course introduced the concept of normal mapping when it presented the very first draft for the **surface function** `surf`

. Recalling the diagram presented at the beginning of this article, you can see that there are two effects that are necessary to reproduce Journey’s sand rendering. The first one (the *sand normal*) is discussed in this article, while the other one (the *sand ripples*) will be explored in [Journey Sand Shader #6: Sand Ripples](https://www.alanzucconi.com/?p=10061).

void surf (Input IN, inout SurfaceOutput o) { o.Albedo = _SandColor; o.Alpha = 1; float3 N = float3(0, 0, 1); N = RipplesNormal(N); // Covered in Journey Sand Shader #6 N = SandNormal (N); // Covered in this article o.Normal = N; }

In the section above we have introduced the idea of bump mapping, indicating that part of the effect will require to sample a texture (referred to, in the code, as `uv_SandTex`

).

One problem of the code above is that the calculations require to know the actual position of the point we are currently drawing. In fact, sampling a texture requires a **UV coordinate**, which indicates which pixel to read from. If the 3D model that we are using is relatively flat and is UV mapped, it possible to use its UV to sample the random texture

N = WavesNormal(IN.uv_SandTex.xy, N); N = SandNormal (IN.uv_SandTex.xy, N);

Alternatively, one could also use the world position (`IN.worldPos`

) of the point rendered.

We can now finally focus on `SandNormal`

, and its implementation. As said in the previous sections, the idea is to sample a pixel from a random texture, and using that (once appropriately transformed into a unit vector) as the new normal.

sampler2D_float _SandTex; float3 SandNormal (float2 uv, float3 N) { // Random vector float3 random = tex2D(_SandTex, uv).rgb; // Random direction // [0,1]->[-1,+1] float3 S = normalize(random * 2 - 1); return S; }

## Tilting the Normal

The snipped presented in the section above works, but does not yield very good results. The reason is simple: if we simply return a completely random normal, we are effectively losing the perception of curvature. In fact, the normal direction is used to calculate how light should reflect on a surface, and its primary use is to shade the model according to its curvature.

You can see the difference in the images below. On the left, the normals of the dunes are completely random, and is impossible to see where one ends and the next one starts. On the right, only the normal of the model is used, resulting in an aesthetics that is too smooth.

![](../../assets/31461c7de24c012d.png)

Both solutions are inadequate. What we need is a blend of the two. The random direction sampled from the texture should be used to *tilt* the normal direction by some amount, as seen below:

The operation described in the diagram above is known as **slerp**, which stands for **spherical linear interpolation**. *Slerp* works exactly like lerp, with the difference that it can be used to safely interpolate between unit vectors, producing other unit vectors.

Unfortunately, the proper implementation of slerp is rather expensive. And for an effect that is mostly based on randomness, it makes little sense to use it.

It is important to notice that if we use the traditional **linear interpolation**, the resulting vector would look quite different:

![](../../assets/e35ac5caaa0419b4.png)

Lerping between two distinct unit vectors is not guaranteed to produce another unit vectors. In fact, it never does except when the coefficient is either ![Rendered by QuickLaTeX.com 1](../../assets/da6d507f7a2bceae.png)

![Rendered by QuickLaTeX.com 0](../../assets/621a9e9e59af40e4.png)


That being said, normalising the result of lerp indeed produces a unit vector that is surprisingly close to the actual result that slerp would produce:

float3 nlerp(float3 n1, float3 n2, float t) { return normalize(lerp(n1, n2, t)); }

This technique, called **nlerp**, has been proposed a close approximation of slerp. Its usage has been popularised by [Casey Muratori](https://twitter.com/cmuratori), one of the developers behind [The Witness](https://store.steampowered.com/app/210970/The_Witness/). If you are interested in reading more about these topics, I suggest [Understanding Slerp. Then Not Using It](http://number-none.com/product/Understanding%20Slerp,%20Then%20Not%20Using%20It/) by [Jonathan Blow](https://twitter.com/jonathan_blow), and [Math Magician – Lerp, Slerp, and Nlerp](https://keithmaggio.wordpress.com/2011/02/15/math-magician-lerp-slerp-and-nlerp/).

Using nlerp, we can now efficiently tilt the normal vectors towards the randomised direction that was sampled from `_SandTex`

:

sampler2D_float _SandTex; float _SandStrength; float3 SandNormal (float2 uv, float3 N) { // Random vector float3 random = tex2D(_SandTex, uv).rgb; // Random direction // [0,1]->[-1,+1] float3 S = normalize(random * 2 - 1); // Rotates N towards Ns based on _SandStrength float3 Ns = nlerp(N, S, _SandStrength); return Ns; }

The result can be seen below:

## What’s Next…

In this third part of the online series about the sand rendering in Journey, we focused on how its dishomogeneous look was achieved using random textures and normal maps.

In the next part, [Journey Sand Shader: Specular Reflection](https://www.alanzucconi.com/?p=10057), we focus on the shimmering reflections that make Journey’s dunes appear almost like an ocean.

- Part 1.
[A Journey Into Journey’s Sand Shader](https://www.alanzucconi.com/?p=10050) - Part 2.
[Journey Sand Shader: Diffuse Colour](https://www.alanzucconi.com/?p=10052) **Part 3.**[Journey Sand Shader: Sand Normal](https://www.alanzucconi.com/?p=10054)- Part 4.
[Journey Sand Shader: Specular Reflection](https://www.alanzucconi.com/?p=10057) - Part 5.
[Journey Sand Shader: Glitter Reflection](https://www.alanzucconi.com/?p=10059) - Part 6.
[Journey Sand Shader: Sand Ripples](https://www.alanzucconi.com/?p=10061)

### Credits

The videogame [Journey](http://thatgamecompany.com/journey/) is developed by **Thatgamecompany** and published by **Sony Computer Entertainment**. It is available for PC ([Epic Store](https://www.epicgames.com/store/en-US/product/journey/home)) and PS4 ([PS Store](https://www.playstation.com/en-gb/games/journey-ps4/)).

The 3D models of the dunes, backgrounds and lighting settings were made by [Jiadi Deng](https://github.com/AtwoodDeng/JourneySand).

The 3D model of the Journey’s player was found on the (now closed) FacePunch forum.

## Download Unity Package

[Become a Patron!](https://www.patreon.com/bePatron?u=850572)

If you want to recreate this effect, the full Unity package is available for download on [Patreon](https://www.patreon.com/posts/30540389/). It includes everything needed, from the shaders to the 3D models.

## Leave a Reply Cancel reply