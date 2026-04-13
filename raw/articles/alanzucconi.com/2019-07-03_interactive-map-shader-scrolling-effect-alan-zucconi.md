---
title: 'Interactive Map Shader: Scrolling Effect - Alan Zucconi'
url: https://www.alanzucconi.com/2019/07/03/interactive-map-02/
author: Alan Zucconi
published: '2019-07-03'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This is the second part of the online course dedicated to **interactive maps**.

![](../../assets/5fbb2a0e1309dd77.gif)

This is a tutorial in three parts:

- Part 1:
[Interactive Map Shader: Vertex Displacement](https://www.alanzucconi.com/?p=10641) **Part 2:**[Interactive Map Shader: Scrolling Effect](https://www.alanzucconi.com/?p=10778)- Part 3:
[Interactive Map Shader: Terrain Shading](https://www.alanzucconi.com/?p=10782)

A link to download the Unity package for this tutorial can be found at the end of this article.

In the previous lecture of this online course, we created a **vertex function** which extrudes the vertices of a mesh upwards. The intensity of the effect is controlled by a texture, the **height map**, so that brighter pixels are raised more, compared to darker ones.

void vert(inout appdata_base v) { float3 normal = float3(0, 1, 0); fixed height = tex2Dlod(_HeightMap, float4(v.texcoord.xy, 0, 0)).r; vertex.xyz += normal * height * _Amount; }

What we have done so far works relatively well. Before we continue, let’s also factor the code necessary to calculate the new vertex height into its own function, called `getVertex`

:

float4 getVertex(float4 vertex, float2 texcoord) { float3 normal = float3(0, 1, 0); fixed height = tex2Dlod(_HeightMap, float4(texcoord, 0, 0)).r; vertex.xyz += normal * height * _Amount; return vertex; }

Now, the entire `vert`

function becomes:

void vert(inout appdata_base v) { vertex = getVertex(v.vertex, v.texcoord.xy); }

The reason why we do this is that in the next sections we will need to calculate the height of multiple points. Having this functionality in its own separate function makes the code much easier.

## Calculating UV Coordinates

This, however, opens up another issue. The `getVertex`

function depends not only on the current vertex position (`v.vertex`

), but also on its UV coordinates (`v.texcoord`

).

When we want to calculate the height displacement of the vertex that the `vert`

function is currently processing, both pieces of information are available in the `appdata_base`

structure. However, what happens if we have to sample the position of a nearby point? In that case, we might know its xyz position in **model space**, but we have no access to its UV coordinates.

This means that the current solution is able to calculate the height displacement for the current vertex only. Such limitation would prevent us from moving forward, so we need to find a solution.

The most simple one is to find a way to calculate the UV coordinates of the 3D object, knowing its vertex position. Technically speaking, this is a very complex problem and there are several techniques that attempt to solve it (the **triplanar projection** being one of the most popular). In this specific case, however, we do not need to map UV to any geometry. If we assume that our shader is only ever going to be used on a flat mesh, then the problem becomes trivial.

What makes calculating *UV coordinates* (below, right) from *vertex positions* (below, left) possible is the fact that, on a flat mesh such as a plane, they are both mapped linearly.

![]() | ![]() |

This means that, in order to solve our problem, we need to remap the *XZ components* of the *vertex position* onto their respective *UV coordinates*.

![](../../assets/21fb3c920793bcc1.png)

This is known as **linear interpolation**, and is a topic that has been covered extensively on this website (for instance: [The Secrets Of Colour Interpolation](https://www.alanzucconi.com/2016/01/06/colour-interpolation/)).

Most UV values range from ![Rendered by QuickLaTeX.com 0](../../assets/621a9e9e59af40e4.png)

![Rendered by QuickLaTeX.com 1](../../assets/da6d507f7a2bceae.png)



, ![Rendered by QuickLaTeX.com X_{max}](../../assets/4958bd5faa62bca4.png)


, ![Rendered by QuickLaTeX.com Z_{max}](../../assets/96b257df7236f877.png)


, ![Rendered by QuickLaTeX.com U_{max}](../../assets/3e37968df43849b3.png)


, ![Rendered by QuickLaTeX.com V_{max}](../../assets/d953c3324afca6a8.png)


which can be seen below:

![](../../assets/68af0227b4a257da.png)

These values changes depending on the mesh used. On a Unity plane, the *UV coordinates* range from ![Rendered by QuickLaTeX.com 0](../../assets/621a9e9e59af40e4.png)

![Rendered by QuickLaTeX.com 1](../../assets/da6d507f7a2bceae.png)

*vertex coordinates* range from ![Rendered by QuickLaTeX.com -5](../../assets/b22515b450644301.png)

![Rendered by QuickLaTeX.com +5](../../assets/df8cf7dec9a5b089.png)


The equations that remap XZ onto UV are:

(1) ![Rendered by QuickLaTeX.com \begin{equation*} \begin{align}U & = \frac{X - X_{min}}{X_{max} - X_{min}} & \left(U_{max} - U_{min}\right) &+ U_{min} \\V & = \frac{Z - Z_{min}}{Z_{max} - Z_{min}} & \left(V_{max} - V_{min}\right) & + V_{min} \\\end{align}\end{equation*}](../../assets/8edce7d545172952.png)


These equations can be implemented like this:

float2 _VertexMin; float2 _VertexMax; float2 _UVMin; float2 _UVMax; float2 vertexToUV(float4 vertex) { return (vertex.xz - _VertexMin) / (_VertexMax - _VertexMin) * (_UVMax - _UVMin) + _UVMin; }

Now, we can invoke `getVertex`

without the need to pass `v.texcoord`

to it:

float4 getVertex(float4 vertex) { float3 normal = float3(0, 1, 0); float2 texcoord = vertexToUV(vertex); fixed height = tex2Dlod(_HeightMap, float4(texcoord, 0, 0)).r; vertex.xyz += normal * height * _Amount; return vertex; }

And the entire `vert`

function becomes:

void vert(inout appdata_base v) { v.vertex = getVertex(v.vertex); }

### ⭐ Recommended Unity Assets

### The Scrolling Effect

With the code that we have written so far, the entire map now appears on the mesh. If we want to improve this, we need to make some changes.

Let’s formalise this a bit more. First of all, we might want to zoom in on a specific part of the map, rather than seeing it in its entirety.

![](../../assets/8d4a44a6a82fca24.png)

We can define this region with two pieces of information: how large it is (`_CropSize`

) and where it is on the map (`_CropOffset`

), measured in *vertex space* (from `_VertexMin`

to `_VertexMax`

).

// Cropping float2 _CropSize; float2 _CropOffset;

Once we have these two values, we can use linear interpolation once again to make sure that `getVertex`

is not called on the actual vertex position of the 3D model, but on a rescaled, translated point.

![](../../assets/a1457c761b0ea104.png)

With the relative code:

void vert(inout appdata_base v) { float2 croppedMin = _CropOffset; float2 croppedMax = croppedMin + _CropSize; // v.vertex.xz: [_VertexMin, _VertexMax] // cropped.xz : [croppedMin, croppedMax] float4 cropped = v.vertex; cropped.xz = (v.vertex.xz - _VertexMin) / (_VertexMax - _VertexMin) * (croppedMax - croppedMin) + croppedMin; v.vertex.y = getVertex(cropped); }

If we want this to actually scroll, then we simply have to update `_CropOffset`

via a script. This moves the cropped area, de-facto scrolling over the landscape.

public class MoveMap : MonoBehaviour { public Material Material; public Vector2 Speed; public Vector2 Offset; private int CropOffsetID; void Start () { CropOffsetID = Shader.PropertyToID("_CropOffset"); } void Update () { Material.SetVector(CropOffsetID, Speed * Time.time + Offset); } }

In order for this to work, is very important that all the textures used have their **Wrap Mode** mode set to **Repeat**. If not, you will not be able to loop around the texture.

For a zoom-in/zoom-out effect, you can simply chance the `_CropSize`

.

## What’s Next…

One important aspect that we have overlooked, is the shading. The geometry appears, in fact, dull and flat. You can see how the model looks now (left) and how it should actually look (right).

We will fix this in the third, and final, part of this online course on interactive map shaders.

- Part 1:
[Interactive Map Shader: Vertex Displacement](https://www.alanzucconi.com/?p=10641) **Part 2:**[Interactive Map Shader: Scrolling Effect](https://www.alanzucconi.com/?p=10778)- Part 3:
[Interactive Map Shader: Terain Shading](https://www.alanzucconi.com/?p=10782)

### Unity Package Download

[Become a Patron!](https://www.patreon.com/bePatron?u=850572)

The full package for this tutorial is available on [Patreon](https://www.patreon.com/posts/28104018), and it includes all the assets necessary to reproduce the technique here presented.

## Leave a Reply Cancel reply