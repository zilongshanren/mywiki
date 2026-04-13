---
title: Volumetric Rendering - Alan Zucconi
url: https://www.alanzucconi.com/2016/07/01/volumetric-rendering/
author: Alan Zucconi
published: '2016-07-01'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This is the first part of a Unity tutorial dedicated to Volumetric Rendering, raymarching and signed distance fields. These techniques allow us to overcome the biggest limitation of modern 3D engines, which only let us render the outer shell of an object. Volumetric rendering enables the creation of realistic materials that interact with light in a complex way, such as fog, smoke, water and glass. Beautifully crafted effects such as [NMZ](https://twitter.com/stormoid)‘s [Plasma Globe](https://www.shadertoy.com/view/XsjXRm) (below) would simply be impossible without volumetric rendering.

![v1](../../assets/2195592116592931.gif)

These techniques are not complicated, but require a lot of steps in order to replicate the aforementioned effects. This tutorial has got you covered.

**Part 1:**| An introduction to what rendering volume means, and how it can be done in Unity;[Volumetric Rendering](https://www.alanzucconi.com/?p=5159)**Part 2:**| Focuses on the implementation of distance-aided raymarching, the de-fact standard technique to render volumes;[Raymarching](https://www.alanzucconi.com/?p=5183)**Part 3:**| A comprehensive guide on how to shade volumes realistically;[Surface Shading](https://www.alanzucconi.com/?p=5174)**Part 4:**| An in-depth discussion of the mathematical tools that allow us to generate and combine arbitrary volumes;[Signed Distance Functions](https://www.alanzucconi.com/?p=5186)**Part 5:**| How to implement realistic and efficient ambient occlusion in your volumes;[Ambient Occlusion](https://www.alanzucconi.com/?p=5182)**🚧 Part 6:**| How to add real shadows to your volumes;[Hard and Soft Shadows](https://www.alanzucconi.com/?p=5197)

This first part will provide a general introduction to volumetric rendering, and end with a simple shader that will be the base of all our future iterations:

[Introduction](https://www.alanzucconi.com#introduction)- Part 1.
[Volumetric Rendering](https://www.alanzucconi.com#part1) - Part 2.
[Volumetric Raycasting](https://www.alanzucconi.com#part2) - Part 3.
[Volumetric Raymarching with Constant Step](https://www.alanzucconi.com#part3) [Conclusion](https://www.alanzucconi.com#conclusion)

The full Unity package is available at the end of this article. 📦

Spheres, cubes and all the other complex geometries are made out of triangles in 3D game engines, which are flat by definition. The real-time lighting systems adopted by Unity are only capable of rendering flat surfaces. When you are rendering a sphere, for instance, Unity only draws the triangles that make its surface. Even for materials that are semi-transparent, only the outer shell is actually drawn and its colour is blended with the one of the objects behind it. There is no attempt in the lighting system to probe into a material’s volume. For the GPU, the world is made out of empty shells.

A broad range of techniques exists, in order to overcome this strong limitation. Even though is true that a traditional shader ultimately stops at the very surface of an object, it doesn’t mean we can’t go deeper. **Volume rendering techniques** simulate the propagation of light rays into a material’s volume, allowing for stunning and sophisticated visual effects.

The fragment shader of an unlit textured object looks like this:

fixed4 frag (v2f i) : SV_Target { fixed4 col = tex2D(_MainTex, i.texcoord); return col; }

![vol1](../../assets/e112e460263c5d14.png)

Loosely speaking, that piece of code is invoked for every potential pixel (fragment) in the final rendered image. When the GPU invokes that fragment shader, it is because there is a triangle that is intersecting the camera frustum. In other words, the camera sees the object. Unity needs to know the exact colour of the object, so that it can assign it to the respective pixel in the rendered image.

Fragment shaders ultimately return the colour of an object at a specific location, as seen from a specific angle. The way this colour is calculated is entirely arbitrary. Nothing forbids us to “cheat” and to return something that does not necessarily match the geometry that we are rendering realistically. The following diagram shows an example of this when rendering a 3D cube. When the fragment shader is queried to get the colour of the cube’s face, we are returning the same colours we could see on a sphere. The geometry is a cube, but from the camera’s perspective it looks and feels exactly like a sphere.

![vol2](../../assets/4108e8c427749df6.png)

This is the basic concept behind volumetric rendering: simulating how light would propagate within the volume of an object.

If we want to emulate the effect shown in the previous diagram we need to describe it more precisely. Let’s say that our main geometry is a cube, and we want to volumetrically render a sphere inside it. There is actually no geometry associated with the sphere, as we will render it entirely via shader code. Our sphere is centred at _Center and has radius _Radius, both expressed in world coordinates. Moving the cube won’t affect the position of the sphere, since it is expressed in absolute world coordinates. It’s also worth noting that the external geometry serves no purpose and won’t change the rest of the tutorial. The triangles of the outer shell of the cube become portals that allow us to see inside the geometry. We could save triangles by using a quad, but a cube allows us to see the volumetric sphere from every angle.

### ⭐ Recommended Unity Assets

The first approach to volumetric rendering works exactly like the previous diagram. The fragment shader receives the point we are rendering (`worldPosition`

) and the direction we are looking at (`viewDirection`

); it then uses a function called `raycastHit`

that indicates whether we are hitting the red sphere or not. This technique is called **volumetric raycasting**, as it extends the rays cast from the camera into the geometry.

We can now write a stub for our fragment shader:

float3 _Centre; float _Radius; fixed4 frag (v2f i) : SV_Target { float3 worldPosition = ... float3 viewDirection = ... if ( raycastHit(worldPosition, viewDirection) ) return fixed4(1,0,0,1); // Red if hit the ball else return fixed4(1,1,1,1); // White otherwise }

Let’s tackle each one of those missing components.

### World Position

Firstly, the world position of the fragment is the point where the rays generated from the camera hit the geometry. We have seen in [Vertex and Fragment Shader](https://www.alanzucconi.com/?p=2001) how to retrieve the world position in a fragment shader:

struct v2f { float4 pos : SV_POSITION; // Clip space float3 wPos : TEXCOORD1; // World position }; v2f vert (appdata_full v) { v2f o; o.pos = mul(UNITY_MATRIX_MVP, v.vertex); o.wPos = mul(_Object2World, v.vertex).xyz; return o; }

### View Direction

Secondly, the view direction is the direction of the ray that comes from the camera and hits the geometry at the point we are rendering. It requires us to know the position of the camera; which Unity includes in the built-in variable `_WorldSpaceCameraPos`

. The direction of a segment that passes through these two points can be calculated as follows:

float3 viewDirection = normalize(i.wPos - _WorldSpaceCameraPos);

### Raycast Hit Function

What we need now is a function `raycastHit`

that, given the point we are rendering and the direction we are looking at it from, determines if we are hitting the virtual red sphere or not. This is the problem of intersecting a sphere with a segment. Formulae for this problem exist (link), but they are generally very inefficient. If you want to go for an analytic approach, you will need to derive formulae to intersect segments with custom geometries. This solution strongly constrains the models you can create; consequently it is rarely adopted.

As explained in the previous section, pure analytical volumetric raycasting is not a feasible approach to our problem. If we want to simulate arbitrary volumes, we need to find a more flexible technique that does not rely on intersecting equations. A common solution is called **volumetric raymarching**, and it is based on an iterative approach.

Volumetric raymarching slowly extends the ray into the volume of the cube. At each step, it queries whether the ray is currently hitting the sphere or not.

![vol3](../../assets/a422ff467565e5e0.png)

Each ray starts from the fragment position `worldPosition`

, and is iteratively extended by `STEP_SIZE`

units into the direction defined by `viewDirection`

. This can be done algebraically by adding `STEP_SIZE * viewDirection`

to the `worldPosition`

after each iteration.

We can now replace `raycastHit`

with the following `raymarchHit`

function:

#define STEPS 64 #define STEP_SIZE 0.01 bool raymarchHit (float3 position, float3 direction) { for (int i = 0; i < STEPS; i++) { if ( sphereHit(position) ) return true; position += direction * STEP_SIZE; } return false; }

The remaining piece of Maths required for this technique is to test whether a point `p`

is inside a sphere:

bool sphereHit (float3 p) { return distance(p,_Centre) < _Radius; }

Intersecting rays with spheres is hard, but iteratively checking if a point is inside a sphere is easy.

The result is this rather unsexy red sphere. Despite looking like a plain circle, this is actually an unlit sphere.

![rotate](../../assets/55a050cd805eb9f1.gif)

## What’s next…

This post introduces the concept of Volumetric Rendering. Even if a traditional shader stops at the outer shell of a material, it is possible to keep projecting those rays inside a material’s volume to create the illusion of depth. Raymarching is one of the most commonly used techniques. We have used it to draw an unlit red sphere. We will see in the following tutorials how to shade it realistically (Part 3. [Surface Shading](https://www.alanzucconi.com/?p=5174)), how to make interesting shapes (Part 3. [Signed Distance Fields](https://www.alanzucconi.com/?p=5186)) and even how to add shadows (Part 6. [Hard and Soft Shadows](https://www.alanzucconi.com/?p=5197)).

**The next part of this tutorial will cover distance-aided raymaching, which is the de-facto standard technique used for volumetric rendering.**

You can find the full list of articles in the series here:

**Part 1:**[Volumetric Rendering](https://www.alanzucconi.com/?p=5159)- Part 2:
[Raymarching](https://www.alanzucconi.com/?p=5183) - Part 3:
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

### Additional Resources

This tutorial would have not been possible without the invaluable contribution of many other talented developers and artists, such as [Íñigo Quílez](https://twitter.com/iquilezles) and [Mikael Hvidtfeldt Christensen](https://twitter.com/#!/syntopiadk).

[Rendering Worlds with Two Triangles with raytracing on the GPU in 4096 bytes](http://www.iquilezles.org/www/material/nvscene2008/rwwtt.pdf)[Distance Estimated 3D Fractals](http://blog.hvidtfeldts.net/index.php/2011/06/distance-estimated-3d-fractals-part-i/)[HOW TO: Ray Marching](https://www.shadertoy.com/view/XllGW4)[Raymarching Distance Fields: Concepts and Implementation in Unity](http://flafla2.github.io/2016/10/01/raymarching.html)[Fullscreen Raymarching for Unity’s Post Processing V2 stack (PostFX V2)](http://hventura.com/unity-post-process-v2-raymarching.html)

The cover for this tutorial features [Clouds](https://www.shadertoy.com/view/XslGRr), by Íñigo Quílez.

## Leave a Reply Cancel reply