---
title: 'Volumetric Rendering: Raymarching - Alan Zucconi'
url: https://www.alanzucconi.com/2016/07/01/raymarching/
author: Alan Zucconi
published: '2016-07-01'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This post continues the tutorial on volumetric rendering, introducing one of the most used techniques: **raymarching**.

You can find here all the other posts in this series:

- Part 1:
[Volumetric Rendering](https://www.alanzucconi.com/?p=5159) **Part 2:**[Raymarching](https://www.alanzucconi.com/?p=5183)- Part 3:
[Surface Shading](https://www.alanzucconi.com/?p=5174) - Part 4:
[Signed Distance Fields](https://www.alanzucconi.com/?p=5186) - Part 5:
[Ambient Occlusion](https://www.alanzucconi.com/?p=5182) - 🚧 Part 6:
[Hard and Soft Shadows](https://www.alanzucconi.com/?p=5197)

The full Unity package is available at the end of this article. 📦

Loosely speaking, the standard behaviour of Unity 5’s lighting engine stops the rendering when a ray from the camera hits the surface of an object. There is no built-in mechanism for those rays to penetrate within the surface of an object. To compensate for this, we have introduced a technique called raymarch. What we have in a fragment shader is the position of the point we are rendering (in world coordinates), and the view direction from the camera. We can manually extend those rays, making them hit custom geometries that exist only within the shader code. The barebone shade that allows us to do this is:

struct v2f { float4 pos : SV_POSITION; // Clip space float3 wPos : TEXCOORD1; // World position }; // Vertex function v2f vert (appdata_full v) { v2f o; o.pos = mul(UNITY_MATRIX_MVP, v.vertex); o.wPos = mul(_Object2World, v.vertex).xyz; return o; } // Fragment function fixed4 frag (v2f i) : SV_Target { float3 worldPosition = i.wPos; float3 viewDirection = normalize(i.wPos - _WorldSpaceCameraPos); return raymarch (worldPosition, viewDirection); }

The rest of this post will provide different implementations for the `raymarch`

function.

The first implementation of raymarching introduced in [Volume Rendering](https://www.alanzucconi.com/?p=5159) used a constant step. Each ray is extended by `STEP_SIZE`

in the view direction, until it hits something. If that’s the case, we draw a red pixel, otherwise a white one.

![vol3](../../assets/a422ff467565e5e0.png)

Raymarching with constant step can be implemented with the following code:

fixed4 raymarch (float3 position, float3 direction) { for (int i = 0; i < STEPS; i++) { if ( sphereHit(position) ) return fixed4(1,0,0,1); // Red position += direction * STEP_SIZE; } return fixed4(0,0,0,1); // White }

As seen already, it renders unsexy, flat geometries:

![rotate](../../assets/55a050cd805eb9f1.gif)

The post [Surface Shading](https://www.alanzucconi.com/?p=5174) will be dedicated entirely to give three-dimensionality to volumetric geometries. Before that, need to focus on a better implementation of the `raymarch`

technique.

### ⭐ Recommended Unity Assets

What makes raymarching with constant step very inefficient is the fact that rays advance by the same amount every time, regardless of the geometry that fills the volumetric world. The performance of a shader suffers immensely by adding loops. If we want to use real-time volumetric rendering, we need to find better a more efficient solution.

We would like a way of estimating how far a ray can travel without hitting a piece of geometry. In order for this technique to work, we need to be able to estimate the distance from our geometry. In the previous post we used a function called `sphereHit`

which indicated whether a point was inside a sphere or not:

bool sphereHit (float3 p) { return distance(p,_Centre) < _Radius; }

We can change it in such a way that instead of a boolean value, it returns a distance:

float sphereDistance (float3 p) { return distance(p,_Centre) - _Radius; }

This now belongs to a family of functions called **signed distance functions**. As the name suggests, it provides a measure which can be positive or negative. When positive, we are outside the sphere; when negative we are inside and when zero we are exactly on its surface.

What `sphereDistance`

allows us is to have a conservative estimation of how far our ray can travel without hitting a sphere. Without any proper shading, volumetric rendering is fairly uninteresting. Even if this example might seem trivial with a single sphere, it becomes a valuable technique with more complex geometries. The following image (from [Distance Estimated 3D Fractals](http://blog.hvidtfeldts.net/index.php/2011/06/distance-estimated-3d-fractals-part-i/)) shows how raymarch works. Each ray travels for as long as its distance from the closest object. In such a way we can dramatically reduce the number of steps required to hit a volume.

![ray](../../assets/aa1a80c8087743c3.png)

This brings us to the distance-aided implementation of raymarching:

fixed4 raymarch (float3 position, float3 direction) { for (int i = 0; i < STEPS; i++) { float distance = sphereDistance(position); if (distance < MIN_DISTANCE) return i / (float) STEPS; position += distance * direction; } return 0; }

To better understand how it works, we replaced the surface rendering with a colour gradient that indicates how many steps were required for raymarch to hit a piece of geometry:

![vol11](../../assets/e1f697505b58c8c2.gif)

It’s immediately obvious that the flat geometry that faces the camera can be identified immediately. The edges, instead, are much trickier. This technique also estimates how close we are to any nearby geometry. We will see in a future instalment, [Ambient Occlusion](https://www.alanzucconi.com/?p=5182), how this can be helpful to add details to our volume.

This post introduces the de-facto standard technique used for real-time raymarching shaders. The rays advance in the volumetric medium according to a conservative estimation of the closest nearby geometry.

**The next post will focus on how to use distance functions to create geometrical primitives, and how they can be combined together to create whichever shape you want.**

You can find the full list of articles in the series here:

- Part 1:
[Volumetric Rendering](https://www.alanzucconi.com/?p=5159) **Part 2:**[Raymarching](https://www.alanzucconi.com/?p=5183)- Part 3:
[Surface Shading](https://www.alanzucconi.com/?p=5174) - Part 4:
[Signed Distance Fields](https://www.alanzucconi.com/?p=5186) - Part 5:
[Ambient Occlusion](https://www.alanzucconi.com/?p=5182) - 🚧 Part 6:
[Hard and Soft Shadows](https://www.alanzucconi.com/?p=5197)

⚠ Part 6 of this series is available for preview on Patreon, as its written content needs to be completed.

If you are interested in volumetric rendering for non-solid materials (clouds, smoke, …) or transparent ones (water, glass, …) the topic is resumed in detail in the [Atmospheric Volumetric Scattering](https://www.alanzucconi.com/?p=7374) series!

By the end of this series you’ll be able to create objects like this one, with just three lines of code and a volumetric shader:

![](../../assets/0c2233c90ba9f0fe.gif)

## Download Unity Package 📦

[Become a Patron!](https://www.patreon.com/bePatron?u=850572)

The [Unity package](https://www.patreon.com/posts/87378094) contains everything needed to replicate the visual seen in this tutorial, including the shader code, the assets and the scene.

## Leave a Reply Cancel reply