---
title: Fast Subsurface Scattering in Unity (Part 2) - Alan Zucconi
url: https://www.alanzucconi.com/2017/08/30/fast-subsurface-scattering-2/
author: Alan Zucconi
published: '2017-08-30'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This is the second part of the tutorial on Fast Subsurface Scattering in Unity. This post will show a working implementation of this effect.

This is a two part series:

At the end of this post, you will find a link to **download** the **Unity project**.

#### Introduction

The previous part of this tutorial explained the mechanism that allows approximating the look of translucent materials. Traditional surfaces are shaded based on the light coming from a direction ![Rendered by QuickLaTeX.com L](../../assets/6046f3c7b4bcbd21.png)

![Rendered by QuickLaTeX.com -L](../../assets/755f228504eecf64.png)

![Rendered by QuickLaTeX.com L](../../assets/6046f3c7b4bcbd21.png)


![](../../assets/65febbcfc8a901bc.png)

Finally, we have derived a view-dependent equation to model the reflectance of the back lighting:

![Rendered by QuickLaTeX.com \[I_{back} = saturate\left(V \cdot - \left \langle L+N\delta \right \rangle \right )^{p} \cdot {s}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-577e07757a85aaf42b85235abb657979_l3.png)


where:


is direction the light comes from (**light direction**),

is the direction the camera is looking at the material (**view direction**),

is the orientation of the surface at the point we have to render (**surface normal**).

There are additional parameters which can be used to control the final look of the material. ![Rendered by QuickLaTeX.com \delta](../../assets/1fdc42f3f5bf3559.png)


![](../../assets/8517a17df05a56c9.png)

Finally, ![Rendered by QuickLaTeX.com p](../../assets/fd0a1880d4f5faaf.png)

![Rendered by QuickLaTeX.com s](../../assets/864f28b25521f331.png)

*power* and *scale*) determine how to the backlight spread, and work in a similar way to the homonym parameters in the **Blinn-Phong reflectance**.

What’s left now is to implement this in a shader.

#### Extending the Standard Shader

As discussed before, we want this effect to be as realistic as possible. Our best choice is to extend Unity’s **Standard shader**, which already provides very good results for non-translucent materials.

Let’s call the new lighting function to be used for this effect `StandardTranslucent`

. The backlight will have the same colour of the original light. What we can control is its intensity, `I`

:

#pragma surface surf StandardTranslucent fullforwardshadows #include "UnityPBSLighting.cginc" inline fixed4 LightingStandardTranslucent(SurfaceOutputStandard s, fixed3 viewDir, UnityGI gi) { // Original colour fixed4 pbr = LightingStandard(s, viewDir, gi); // Calculate intensity of backlight (light translucent) float I = ... pbr.rgb = pbr.rgb + gi.light.color * I; return pbr; }

### ⭐ Recommended Unity Assets

#### Back Lighting

Following the equations described in the first section of this tutorial, we can proceed to write the following code:

inline fixed4 LightingStandardTranslucent(SurfaceOutputStandard s, fixed3 viewDir, UnityGI gi) { // Original colour fixed4 pbr = LightingStandard(s, viewDir, gi); // --- Translucency --- float3 L = gi.light.dir; float3 V = viewDir; float3 N = s.Normal; float3 H = normalize(L + N * _Distortion); float I = pow(saturate(dot(V, -H)), _Power) * _Scale; // Final add pbr.rgb = pbr.rgb + gi.light.color * I; return pbr; }

The code above is a direct translation of the equations from the first part of this post. The translucency effect that results is believable (below), but does is not related in any way to the thickness of the material. This makes it very hard to control.

![](../../assets/a7b26e9e6fe4d567.png)

#### Local Thickness

It is obvious that the amount of back light strongly depends on the density and thickness of the material. Ideally, we would need to know the distance light travelled inside the material, and attenuating it accordingly. You can see in the image below how three different light rays with the same incident angle travel very different lengths through the material.

![](../../assets/3ac0a53af49eb1be.png)

From the point of view of a shader, however, we do not have access to either the local geometry or the history of the light rays. Unfortunately, there is no way of solving this problem locally. The best approach proposed is to rely on an external **local thickness map**. That is a texture, mapped onto our surface, which indicates how “thick” that part of the material is. The concept of “thickness” is used loosely, as real thickness actually depends on the angle the light is coming from.

![](../../assets/46b7d3e6575e9315.png)

The diagram above shows how there is no unique concept of “thickness” associated with the red point on the circle. The amount of material the light is travelling through indeed depends on the light angle ![Rendered by QuickLaTeX.com L](../../assets/6046f3c7b4bcbd21.png)


That being said, we have to remember that this entire approach to translucency is not about being physically accurate, but just realistic enough to fool the player’s eye. Below ([credits](https://colinbarrebrisebois.com/2011/03/07/gdc-2011-approximating-translucency-for-a-fast-cheap-and-convincing-subsurface-scattering-look/)), you can see a good local thickness map visualised on the model of a statue. White colours correspond to parts of the model where the translucent effect will be stronger, approximating the concept of thickness.

![](../../assets/55fee7e61b3c2b42.png)

#### The Final Version

We now know that we need to take into account the local thickness of the material. The easiest way is to provide a texture map that we can sample. While not physically accurate, it can produce believable results. Additionally, the local thickness is encoded in a way that allows artists to retain full control on the effect.

In this implementation, the local thickness is provided in the red channel of an additional texture, sampled in the **surf** function:

float thickness; void surf (Input IN, inout SurfaceOutputStandard o) { // Albedo comes from a texture tinted by color fixed4 c = tex2D (_MainTex, IN.uv_MainTex) * _Color; o.Albedo = c.rgb; // Metallic and smoothness come from slider variables o.Metallic = _Metallic; o.Smoothness = _Glossiness; o.Alpha = c.a; thickness = tex2D (_LocalThickness, IN.uv_MainTex).r; }

Colin and Mark proposed a slightly different equation to calculate the final intensity of the backlight. This takes into account both the thickness and an additional **attenuation parameter**. Also, they allow for an additional **ambient component** that is present at all time:

inline fixed4 LightingStandardTranslucent(SurfaceOutputStandard s, fixed3 viewDir, UnityGI gi) { // Original colour fixed4 pbr = LightingStandard(s, viewDir, gi); // --- Translucency --- float3 L = gi.light.dir; float3 V = viewDir; float3 N = s.Normal; float3 H = normalize(L + N * _Distortion); float VdotH = pow(saturate(dot(V, -H)), _Power) * _Scale; float3 I = _Attenuation * (VdotH + _Ambient) * thickness; // Final add pbr.rgb = pbr.rgb + gi.light.color * I; return pbr; }

This is the final result:

![](../../assets/9a73db260e20454d.png)

#### Conclusion

This post concludes the series on fast subsurface scattering. The approach described in this tutorial is based on the solution presented at GDC 2011 by Colin Barré-Brisebois and Marc Bouchard in a talk called [Approximating Translucency for a Fast, Cheap and Convincing Subsurface Scattering Look](https://colinbarrebrisebois.com/2011/03/07/gdc-2011-approximating-translucency-for-a-fast-cheap-and-convincing-subsurface-scattering-look/).

You can read the entire series here:

- Part 1.
[Fast Subsurface Scattering in Unity](https://www.alanzucconi.com/?p=7053) - Part 2.
**Fast Subsurface Scattering in Unity**

[Become a Patron!](https://www.patreon.com/bePatron?u=850572)

You can download all the necessary files to run this project (shader, textures, models, scenes) on [ Patreon](https://www.patreon.com/posts/14122322).

## Leave a Reply Cancel reply