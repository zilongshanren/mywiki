---
title: 3D Printer Shader Effect - Part 2 - Alan Zucconi
url: https://www.alanzucconi.com/2016/10/02/3d-printer-shader-effect-part-2/
author: Alan Zucconi
published: '2016-10-02'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This is the second part of the tutorial that will recreate the 3D printer effect seen in games such as [Astroneer](http://astroneer.space/) and [Planetary Annihilation](http://www.uberent.com/pa/).

![a1](../../assets/95a9c5ac09c6a92a.gif)

[Introduction](https://www.alanzucconi.com#introduction)- Part 1.
[Cutting the Geometry](https://www.alanzucconi.com#part1) - Part 2.
[Wobbly Effect](https://www.alanzucconi.com#part2) - Part 3.
[Animate](https://www.alanzucconi.com#part3) [Conclusion](https://www.alanzucconi.com#conclusion)

This is a two part tutorials:

[3D Printer Shader Effect – Part 1](https://www.alanzucconi.com/2016/10/02/3d-printer-shader-effect-part-1/)**3D Printer Shader Effect – Part 2**

A link to download the Unity package (code, shader and 3D models) is provided at the end of the tutorial.

The first part of this tutorial shown how to render part of an object with an unlit lighting model (picture below). There are few other things that are yet to be achieved to fully recreate the beautiful style seen in Astroneer.

![03](../../assets/0cc12477f5e5e96c.png)

The easiest effect to add to our shader is to stop drawing the upper part of the geometry. The keyword `discard`

can be used to arbitrarily prevent a pixel from being drawn in a shader. We can use it to ensure that only a rim around the top part out model is drawn:

void surf (Input IN, inout SurfaceOutputStandard o) { if (IN.worldPos.y > _ConstructY + _ConstructGap) discard; ... }

It is important to remember that this potentially leaves “holes” in out geometry. You should disable face culling, so that even the back of an object can be fully drawn.

Cull Off

![04](../../assets/68c0ef348f9d93bb.png)

Now, the most striking thing is that the object looks hollow. This is not just an impression: all 3D models are actually hollow. What we want to convey, however, is the illusion that the object is actually solid. This can be done easily by colouring the inside of an object with the same unlit shader. The object is still hollow, but it will be perceived as full.

To achieve this, we simply colour the triangles that are facing back to the camera. If you are unfamiliar with vector algebra, this might seen a rather complex condition to achieve. In reality, it can be done quite easily using the [dot product](https://en.wikipedia.org/wiki/Dot_product). The dot product between two vectors indicates how “aligned” they are. Which is directly related with their angle. When the dot product between two vectors is negative, it means there is more than 90 degrees of separation between them. We can test for our original condition by taking the dot product between the view direction of the camera (`viewDir`

in a surface shader) and the normal of a triangle. If it is negative, it means that the triangle is not facing the camera. Hence, we are seeing his “back” side; we can then render it with a solid colour.

struct Input { float2 uv_MainTex; float3 worldPos; float3 viewDir; }; void surf (Input IN, inout SurfaceOutputStandard o) { viewDir = IN.viewDir; ... } inline half4 LightingCustom(SurfaceOutputStandard s, half3 lightDir, UnityGI gi) { if (building) return _ConstructColor; if (dot(s.Normal, viewDir) < 0) return _ConstructColor; return LightingStandard(s, lightDir, gi); }

The result is shown in the following pictures. On the left, the “back geometry” is rendered in red. When we use the same colour for the top part of the object, it doesn’t look hollow anymore.

![05](../../assets/39600e43bbee60ab.png)

### ⭐ Recommended Unity Assets

![pa2](../../assets/cae24987d649ffa5.gif)

If you have played Planetary Annihilation, you know that the 3D printer shader it uses has a gentle wobbly effect. We can add this as well, by adding some noise to the world position of the pixels we are drawing. This can be achieved either with a noise texture, or by using some continuous, periodic function. In the piece of code below, I have use a sinusoid function with some arbitrary parameters.

void surf (Input IN, inout SurfaceOutputStandard o) { float s = +sin((IN.worldPos.x * IN.worldPos.z) * 60 + _Time[3] + o.Normal) / 120; if (IN.worldPos.y > _ConstructY + s + _ConstructGap) discard; ... }

These parameters have been tweaked manually until I obtained a pleasant wobbly effect.

![07](../../assets/ddde6be16e1c8a7d.gif)

The final part of this effect is the animation. This is achieved simply by changing the `_ConstructY`

parameter of the material. The shader will take care of the rest. You can control the speed of the effect either via code, or using an animation curve. The former has the advantage that you can fully customise its speed.

public class BuildingTimer : MonoBehaviour { public Material material; public float minY = 0; public float maxY = 2; public float duration = 5; // Update is called once per frame void Update () { float y = Mathf.Lerp(minY, maxY, Time.time / duration); material.SetFloat("_ConstructY", y); } }

![08](../../assets/93e7123782b8ed46.gif)

As a final note, the model used in this picture looks hollow for few seconds because the bottom part of the boosters is not closed. Hence, it is *actually* hollow.

This concludes the 3D printer shader effect.

[3D Printer Shader Effect – Part 1](https://www.alanzucconi.com/?p=5660)**3D Printer Shader Effect – Part 2**

A big thanks goes to the guys at [System Era](http://systemera.net/), and in particular to [Jacob Liechty](https://twitter.com/SparseJacobian).

## Leave a Reply Cancel reply