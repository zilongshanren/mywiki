---
title: 3D Printer Shader Effect - Part 1 - Alan Zucconi
url: https://www.alanzucconi.com/2016/10/02/3d-printer-shader-effect-part-1/
author: Alan Zucconi
published: '2016-10-02'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This tutorial will recreate the 3D printer effect seen in games such as [Astroneer](http://astroneer.space/) and [Planetary Annihilation](http://www.uberent.com/pa/). It’s an interesting effect that shows an object in the process of being created. Despite looking simple, there are many challenges that are far from being trivial.

![a1](../../assets/95a9c5ac09c6a92a.gif)

- Introduction:
[A First Attempt](https://www.alanzucconi.com#introduction) - Part 1.
[Unlit Shader Surface](https://www.alanzucconi.com#part1) - Part 2.
[Passing Paramters to the Lighting Function](https://www.alanzucconi.com#part2) - Part 3.
[Extending the Standard Lighting Function](https://www.alanzucconi.com#part3) [Conclusion](https://www.alanzucconi.com#conclusion)

This is a two part tutorials:

**3D Printer Shader Effect – Part 1**[3D Printer Shader Effect – Part 2](https://www.alanzucconi.com/?p=5668)

A link to download the Unity package (code, shader and 3D models) is provided at the end of the tutorial.

In order to replicate this effect, let’s start with something simpler. A shader that colours an object differently, depending on its position. To achieve this, we need to access the world position of the pixels being drawn. This is possible by adding the field `worldPos`

to the `Input`

structure of a Unity 5 surface shader.

struct Input { float2 uv_MainTex; float3 worldPos; };

In the surface function, we can then use the Y coordinate of the world position to change the colour of the object. This is done by changing the `Albedo`

property of the `SurfaceOutputStandard`

structure.

float _ConstructY; fixed4 _ConstructColor; void surf (Input IN, inout SurfaceOutputStandard o) { if (IN.worldPos.y < _ConstructY) { fixed4 c = tex2D(_MainTex, IN.uv_MainTex) * _Color; o.Albedo = c.rgb; o.Alpha = c.a; } else { o.Albedo = _ConstructColor.rgb; o.Alpha = _ConstructColor.a; } o.Metallic = _Metallic; o.Smoothness = _Glossiness; }

The result is a first approximation to the effect seen in Astroneer. The main problem is that the coloured part is still shaded.

![01](../../assets/14659f5a76061f7f.png)

In a previous tutorial, [PBR and Lighting Models](https://www.alanzucconi.com/?p=1964), we have explored how to create custom lighting models for surface shaders. An unlit shader always produces the same colour, regardless of external lighting and view direction. We can implement it as follow:

#pragma surface surf Unlit fullforwardshadows inline half4 LightingUnlit (SurfaceOutput s, half3 lightDir, half atten) { return _ConstructColor; }

It’s only purpose is to return a single, solid colour. As we can see, it refers to `SurfaceOutput`

, which is used in Unity 4. If we want to create a custom lighting model that works with PBR and global illumination, we need to implement a function that takes `SurfaceOutputStandard`

as an input. In Unity 5, it is the following function:

inline half4 LightingUnlit (SurfaceOutputStandard s, half3 lightDir, UnityGI gi) { return _ConstructColor; }

The `gi`

parameter is there for the global illumination; but it serves no purpose in our unlit shader. Despite working, there is a big problem with this approach. Unity does not allow surface shader to selectively change lighting function. We cannot use the standard Lambertian lighting to the bottom part of the object, and the unlit for the top part. We can only specify a single lighting function for the entire object. It’s up to us to change the way the object is rendered depending on its position.

![02](../../assets/af389c94b021ea48.png)

Unfortunately, the lighting function has no access to the object position. The easiest way to provide that information is to use a boolean variable (called `building`

) that we set in the surface function. The variable can then be queried by our new lighting function.

int building; void surf (Input IN, inout SurfaceOutputStandard o) { if (IN.worldPos.y < _ConstructY) { fixed4 c = tex2D(_MainTex, IN.uv_MainTex) * _Color; o.Albedo = c.rgb; o.Alpha = c.a; building = 0; } else { o.Albedo = _ConstructColor.rgb; o.Alpha = _ConstructColor.a; building = 1; } o.Metallic = _Metallic; o.Smoothness = _Glossiness; }

### ⭐ Recommended Unity Assets

The last challenge that we have to face is a tricky one. As explained in the previous paragraph, we can use `building`

to change the way lighting is calculated. The section of the object that is currently being built will be unlit, while the other should have proper lighting. If we our material to use PBR, we cannot possibly re-write the entire code for photorealistic lighting. The only reasonable solution is to invoke the standard lighting function that Unity has already implemented.

In a traditional standard surface shader, the `#pragma`

directive that specifies to use the PBR lighting function is the follow:

#pragma surface surf Standard fullforwardshadows

Following Unity’s naming convention, it’s easy to see that the function that they use should be called `LightingStandard`

. This function is found in a file called `UnityPBSLighting.cginc`

, which can be included if necessary.

The plan is to create a custom lighting function called `LightingCustom`

. In normal conditions it simply invokes the Unity standard PBR `LightingStandard`

. When necessary, however, it adopts the previously defined `LightingUnlit`

.

inline half4 LightingCustom(SurfaceOutputStandard s, half3 lightDir, UnityGI gi) { if (!building) return LightingStandard(s, lightDir, gi); // Unity5 PBR return _ConstructColor; // Unlit }

In order for this code to compile, Unity 5 requires an additional function to be defined:

inline void LightingCustom_GI(SurfaceOutputStandard s, UnityGIInput data, inout UnityGI gi) { LightingStandard_GI(s, data, gi); }

That is used to calculate the lighting contributions for global illumination, but is unnecessary for the purposes of this tutorial.

The result is exactly what we expect:

![03](../../assets/0cc12477f5e5e96c.png)

This first post focused on how to use two different lighting models in the same shader. This allowed us to have half of the model rendered with PBR, while the other half uses is unlit. The next post will conclude this tutorial, showing how to animate and improve the effect.

**3D Printer Shader Effect – Part 1**[3D Printer Shader Effect – Part 2](https://www.alanzucconi.com/?p=5668)

![08](../../assets/93e7123782b8ed46.gif)

A big thanks goes to the guys at [System Era](http://systemera.net/), and in particular to [Jacob Liechty](https://twitter.com/SparseJacobian).

## Leave a Reply Cancel reply