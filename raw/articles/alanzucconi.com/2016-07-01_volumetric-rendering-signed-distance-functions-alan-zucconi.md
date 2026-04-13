---
title: 'Volumetric Rendering: Signed Distance Functions - Alan Zucconi'
url: https://www.alanzucconi.com/2016/07/01/signed-distance-functions/
author: Alan Zucconi
published: '2016-07-01'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This tutorial explains how to create complex 3D shapes inside volumetric shaders. **Signed Distance Functions** (often referred to as Fields) are mathematical tools used to describe geometrical shapes such as spheres, boxes and tori. Compared to traditional 3D models made out of triangles, signed distance functions provide virtually **infinite resolution**, and are amenable to geometric manipulation. The following animation, from [formulanimation tutorial :: making a snail](https://www.youtube.com/watch?v=XuSnLbB1j6E), shows how a snail can be created using simpler shapes:

![A snail created by Signed Distance Fields.](../../assets/d0cc2aac0faa8c2c.gif)

[Introduction](https://www.alanzucconi.com#introduction)- Part 1.
[SDF Sphere](https://www.alanzucconi.com#part1) - Part 2.
[Union and Intersection](https://www.alanzucconi.com#part2) - Part 3.
[SDF Box](https://www.alanzucconi.com#part3) - Part 4.
[Shape Blending](https://www.alanzucconi.com#part4) - Part 5.
[Smooth Union](https://www.alanzucconi.com#part5) - Part 6.
[SDF Algebra](https://www.alanzucconi.com#part6) [Conclusion](https://www.alanzucconi.com#conclusion)

You can find here all the other posts in this series:

- Part 1:
[Volumetric Rendering](https://www.alanzucconi.com/?p=5159) - Part 2:
[Raymarching](https://www.alanzucconi.com/?p=5183) - Part 3:
[Surface Shading](https://www.alanzucconi.com/?p=5174) **Part 4:**[Signed Distance Fields](https://www.alanzucconi.com/?p=5186)- Part 5:
[Ambient Occlusion](https://www.alanzucconi.com/?p=5182) - 🚧 Part 6:
[Hard and Soft Shadows](https://www.alanzucconi.com/?p=5197)

The full Unity package is available at the end of this article. 📦

The way most modern 3D engines – such as Unity – handle geometries is by using triangles. Every object, no matter how complex, must be composed of those primitive triangles. Despite being the de-facto standard in computer graphics, there are objects which cannot be represented with triangles. Spheres, and all other curved geometries, are impossible to tessellate with flat entities. It is indeed true that we can approximate a sphere by covering its surface with a lot of small triangles, but this comes at the cost of adding more primitives to draw.

Alternative ways to represent geometries exist. One of these uses signed distance functions, which are mathematical descriptions of the objects we want to represent. When you replace the geometry of a sphere with its very equation, you have suddenly removed any approximation error from your 3D engine. You can think of signed distance fields as the SVG equivalent of triangles. You can scale up and zoom SDF geometries without ever losing detail. A sphere will always be smooth, regardless of how close you are to its edges.

Signed-distance functions are based on the idea that every primitive object must be represented with a function. It takes a 3D point as a parameter and returns a value that indicates how distant that point is to the object surface.

In the first post of this series, [Volumetric Rendering](https://www.alanzucconi.com/?p=5159), we’ve seen a hit function that indicates if we are inside a sphere or not:

bool sphereHit (float3 p) { return distance(p,_Centre) < _Radius; }

We can change this function so that it returns the distance from the sphere surface instead:

float sdf_sphere (float3 p, float3 c, float r) { return distance(p,c) - r; }

If `sdf_sphere`

returns a positive distance, we’re not hitting the sphere. A negative distance indicates that we are inside the sphere, while zero is reserved for the points of the space which actually make up the surface.

The concept of signed distance function was briefly introduced in [Raymarching](https://www.alanzucconi.com/?p=5183) tutorial, where it guided the advancement of the camera rays into the material. There is another reason why SDFs are used. And it is because they are amenable to composition. Given the SDFs of two different spheres, how can we merge them into a single SDF?

We can think about this from the perspective of a camera ray, advancing into the material. At each step, the ray must find its closest obstacle. If there are two spheres, we should evaluate the distance from both and get the smallest. We don’t want to overshoot the sphere, so we must advance by the most conservative estimation.

This toy example can be extended to any two SDFs. Taking the minimum value between them returns another SDF which corresponds to their union:

float map (float3 p) { return min ( sdf_sphere(p, - float3 (1.5, 0, 0), 2), // Left sphere sdf_sphere(p, + float3 (1.5, 0, 0), 2) // Right sphere ); }

The result can be seen in the following picture (which also features a few other visual enhancements that will be discussed in the next post on [Ambient Occlusion](https://www.alanzucconi.com/?p=5182)):

![sdf1](../../assets/527ba8307c77c48f.png)

With the same reasoning, it’s easy to see that taking the maximum value between two SDFs returns their intersection:

float map (float3 p) { return max ( sdf_sphere(p, - float3 (1.5, 0, 0), 2), // Left sphere sdf_sphere(p, + float3 (1.5, 0, 0), 2) // Right sphere ); }

![sdf2](../../assets/f4adc1b3e65cc520.png)

### ⭐ Recommended Unity Assets

## SDF Box

Many geometries can be constructed with what we already know. If we want to push out knowledge further, we need to introduce a new SDF primitive: the [half-space](https://en.wikipedia.org/wiki/Half-space_(geometry)). As the name suggests, it is nothing more than just a primitive that occupies half of the 3D space.

// X Axis d = + p.x - c.x; // Left half-space full d = - p.x + c.x; // Right half-space full // Y Axis d = + p.y - c.y; // Left half-space full d = - p.y + c.y; // Right half-space full // Z Axis d = + p.z - c.z; // Left half-space full d = - p.z + c.z; // Right half-space full

The trick is to intersect six planes in order to create a box with the given size `s`

, like shown in the animation below:

float sdf_box (float3 p, float3 c, float3 s) { float x = max ( p.x - c.x - float3(s.x / 2., 0, 0), c.x - p.x - float3(s.x / 2., 0, 0) ); float y = max ( p.y - c.y - float3(s.y / 2., 0, 0), c.y - p.y - float3(s.y / 2., 0, 0) ); float z = max ( p.z - c.z - float3(s.z / 2., 0, 0), c.z - p.z - float3(s.z / 2., 0, 0) ); float d = x; d = max(d,y); d = max(d,z); return d; }

![sdf3](../../assets/a300e0ff400c0c6a.gif)

There are more compact (yet less precise) ways to create a box, which take advantage of the symmetries around the centre:

float vmax(float3 v) { return max(max(v.x, v.y), v.z); } float sdf_boxcheap(float3 p, float3 c, float3 s) { return vmax(abs(p-c) - s); }

If you are familiar with the concept of **alpha blending**, you will probably recognise the following piece of code:

float sdf_blend(float d1, float d2, float a) { return a * d1 + (1 - a) * d2; }

Its purpose is to create a blending between two values, d1 and d2 , controlled by a value a (from zero to one). The exact same code used to blend colours can also be used to blend shapes. For instance, the following code blends a sphere into a cube:

d = sdf_blend ( sdf_sphere(p, 0, r), sdf_box(p, 0, r), (_SinTime[3] + 1.) / 2. );

![sdf5](../../assets/4e8cdcdbe8d5460d.gif)

In a previous section, we’ve seen how two SDFs can be merged together using min. If it is true that the SDF union is indeed effective, it is also true that its results are rather unnatural. Working with SDFs allows for many ways in which primitives can be blended together. One of these techniques, exponential smoothing (link: Smooth Minimum), has been used extensively in the original animations of this tutorial.

float sdf_smin(float a, float b, float k = 32) { float res = exp(-k*a) + exp(-k*b); return -log(max(0.0001,res)) / k; }

![sdf10](../../assets/6bc3e3ba0574cfe6.gif)

When two shapes are joined using this new operator, they merge softly, creating a gentle step that removes any sharp edge. In the following animation, you can see how the spheres merge together:

As you can anticipate, all those SDF primitives and operators are part of a signed distance function algebra. Rotations, scaling, bending, twisting… all those operations can be performed with signed distance functions.

In his article titled Modeling With Distance Functions, Íñigo Quílez has worked on a vast collection of SDFs that can be used as primitive for the construction of more complex geometries. You can see some of them by clicking on the interactive **ShaderToy** below:

An even larger collection of primitives and operators is available in the library **hg_sdf** (link [here](http://mercury.sexy/hg_sdf/)) curated by the [MERCURY](https://twitter.com/mercury_labs) group. Despite being written in GLSL, the functions are easily portable to Unity’s Cg/HLSL.

The number of transformations that can be performed with SDFs is virtually endless. This post provided just a quick introduction to the topic. If you really want to master volumetric rendering, improving your knowledge of SDFs is a good starting point.

You can find the full list of articles in the series here:

- Part 1:
[Volumetric Rendering](https://www.alanzucconi.com/?p=5159) - Part 2:
[Raymarching](https://www.alanzucconi.com/?p=5183) - Part 3:
[Surface Shading](https://www.alanzucconi.com/?p=5174) **Part 4:**[Signed Distance Fields](https://www.alanzucconi.com/?p=5186)- Part 5:
[Ambient Occlusion](https://www.alanzucconi.com/?p=5182) - 🚧 Part 6:
[Hard and Soft Shadows](https://www.alanzucconi.com/?p=5197)

⚠ Part 6 of this series is available for preview on Patreon, as its written content needs to be completed.

If you are interested in volumetric rendering for non-solid materials (clouds, smoke, …) or transparent ones (water, glass, …) the topic is resumed in detail in the [Atmospheric Volumetric Scattering](https://www.alanzucconi.com/?p=7374) series!

By the end of this series you’ll be able to create objects like this one, with just three lines of code and a volumetric shader:

![](../../assets/0c2233c90ba9f0fe.gif)

### Additional resources

## Download Unity Package 📦

[Become a Patron!](https://www.patreon.com/bePatron?u=850572)

The [Unity package](https://www.patreon.com/posts/87378094) contains everything needed to replicate the visual seen in this tutorial, including the shader code, the assets and the scene.

## Leave a Reply Cancel reply