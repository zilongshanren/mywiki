---
title: 'Physically Based Rendering: PBR in Unity - Shader tutorial'
url: https://www.alanzucconi.com/2015/06/24/physically-based-rendering/
author: Alan Zucconi
published: '2015-06-24'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

[Part 1](https://www.alanzucconi.com/2015/06/10/a-gentle-introduction-to-shaders-in-unity3d/), [Part 2](https://www.alanzucconi.com/2015/06/17/surface-shaders-in-unity3d/), **Part 3**, [Part 4](https://www.alanzucconi.com/2015/07/01/vertex-and-fragment-shaders-in-unity3d/), [Part 5](https://www.alanzucconi.com/2015/07/08/screen-shaders-and-postprocessing-effects-in-unity3d/), [[download the Unity3D package](https://drive.google.com/file/d/0B4nCcaMlgxV2eEVkV250MGFVLWM/view?usp=sharing)]

Why is it colder at the poles and hotter on the equator? This question, which seems completely unrelated to shaders, is actually fundamental to understand how lighting models work. As explained in the previous part of this tutorial, surface shaders use a mathematical model to predict how light will reflect on triangles. Generally speaking, Unity supports two types of shading techniques, one for matte and one for specular materials. The former ones are perfect for opaque surfaces, while the latter ones simulate objects which reflections. The Maths behind these lighting models can get quite complicated, but understanding how they work is essential if you want to create your own, custom lighting effect. Up to Unity4.x, the default diffuse lighting model was based on the [Lambertian reflectance](https://en.wikipedia.org/wiki/Lambertian_reflectance).

### Diffuse surfaces: the Lambertian model

Going back to the initial question, the reason why the poles are colder, is because they receive less sunlight compared to the equator. This happens because of their relative inclination from the sun. The following diagram shows how the polar edges of the octagon receive sensibly less light compared the frontal one:

![Light Geometry2](../../assets/0d25d28b908754c3.png)

The blue line represents the normal of the face, which is an orthogonal vector of unit length. The orange one represents the direction of the light. The amount of light ![Rendered by QuickLaTeX.com I](../../assets/c2ab42bcab55cee7.png)

![Rendered by QuickLaTeX.com N](../../assets/76bbbd804dc6db36.png)

![Rendered by QuickLaTeX.com L](../../assets/6046f3c7b4bcbd21.png)


![light cos](../../assets/4c95f6057e6cecc2.png)

Which can be expressed as:

![Rendered by QuickLaTeX.com \[I= \left \| L \right \| \, cos \alpha = cos \alpha\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-a2d6032349198b10191f4cb508b5af34_l3.png)


where ![Rendered by QuickLaTeX.com \left \| L \right \|](../../assets/daca21be98661edc.png)

![Rendered by QuickLaTeX.com L](../../assets/6046f3c7b4bcbd21.png)

![Rendered by QuickLaTeX.com \alpha](../../assets/2f6dd9acb6fbfd6a.png)

![Rendered by QuickLaTeX.com N](../../assets/76bbbd804dc6db36.png)

![Rendered by QuickLaTeX.com L](../../assets/6046f3c7b4bcbd21.png)

[dot product](https://en.wikipedia.org/wiki/Dot_product) as was briefly introduced in the previous post. Formally, it is defined as the follow:

![Rendered by QuickLaTeX.com \[A \cdot B = \left \| A \right \| \, \left \| B \right \| \, cos \alpha\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-d5dccf6a0d964ce21a12a26ecefa9cdd_l3.png)


and is available in Cg / HLSL using the function `dot`

. It returns a number ranging from -1 to +1 which is zero when the vectors are orthogonal, and ![Rendered by QuickLaTeX.com \pm](../../assets/32cd95adb1ea97ec.png)


### The Lambertian shader

We now have all the necessary background to understand how a Lambertian model can be implemented in a shader. Cg / HLSL allows to replace the standard Lambertian model with a custom function. In **line 8**, using `SimpleLambert`

in the directive `#pragma surface`

forces the shader to search for a function called `LightingSimpleLambert`

:

Shader "Example/SimpleLambert" { Properties { _MainTex ("Texture", 2D) = "white" {} } SubShader { Tags { "RenderType" = "Opaque" } CGPROGRAM #pragma surface surf SimpleLambert struct Input { float2 uv_MainTex; }; sampler2D _MainTex; void surf (Input IN, inout SurfaceOutput o) { o.Albedo = tex2D (_MainTex, IN.uv_MainTex).rgb; } half4 LightingSimpleLambert (SurfaceOutput s, half3 lightDir, half atten) { half NdotL = dot (s.Normal, lightDir); half4 c; c.rgb = s.Albedo * _LightColor0.rgb * (NdotL * atten * 2); c.a = s.Alpha; return c; } ENDCG } Fallback "Diffuse" }

**Lines 19-25** shows how the Lambertian model can be naively re-implemented in a surface shader. `NdotL`

represents the coefficient of intensity, which is then multiplied to the colour of the light. The parameters `atten`

is used to modulate the intensity of the light. The reason why it is multiplied by two is… a trick initially used by Unity3D to simulate certain effects. As explained by [Aras Pranckevičius](http://forum.unity3d.com/threads/why-atten-2.94711/), it has been kept in Unity4 for backward compatibility. This has been finally fixed in Unity5, so if you’re reimplementing a Lambertian model for Unity5, just multiply by one.

Understanding how the standard lighting model works is an essential step if we want to change it. Many alternative shading techniques, in fact, still use the Lambertian model as their first step.

### ⭐ Recommended Unity Assets

### ⭐ Recommended Unity Assets

### Toon shading

One of the most used styles in games lately is the toon shading (also known as [cel shading](https://en.wikipedia.org/wiki/Cel_shading)). It’s a non photorealistic rendering style which changes the way light reflects on a model to give the illusion it has been hand drawn. To implement this style, we need to replace the standard lighting model used so far with a custom one. The most common technique to achieve this style is to use an additional texture, called `_RampTex`

in the shader below.

Shader "Example/Toon Shading" { Properties { _MainTex ("Texture", 2D) = "white" {} _RampTex ("Ramp", 2D) = "white" {} } SubShader { Tags { "RenderType" = "Opaque" } CGPROGRAM #pragma surface surf Toon struct Input { float2 uv_MainTex; }; sampler2D _MainTex; void surf (Input IN, inout SurfaceOutput o) { o.Albedo = tex2D (_MainTex, IN.uv_MainTex).rgb; } sampler2D _RampTex; fixed4 LightingToon (SurfaceOutput s, fixed3 lightDir, fixed atten) { half NdotL = dot(s.Normal, lightDir); NdotL = tex2D(_RampTex, fixed2(NdotL, 0.5)); fixed4 c; c.rgb = s.Albedo * _LightColor0.rgb * NdotL * atten * 2; c.a = s.Alpha; return c; } ENDCG } Fallback "Diffuse" }

![toon](../../assets/a18a16b2ea9e1d32.png)

The `LightingToon`

model calculates the Lambertian coefficient of intensity `NdotL`

and uses the ramp texture to re-map it onto a different set of values. In this case, to restrict the intensity to four values only. Different ramp textures will achieve slightly different variants of toon shading.

![ramp](../../assets/61a2dea1abc1e353.png)

### Specular surfaces: the Blinn-Phong model

The Lambertian model cannot simulate materials which have specular reflections. For them, another technique is necessary; Unity4.x adopts the *Blinn-Phong model. *Rather than calculating the dot product between the normal ![Rendered by QuickLaTeX.com N](../../assets/76bbbd804dc6db36.png)

![Rendered by QuickLaTeX.com L](../../assets/6046f3c7b4bcbd21.png)

![Rendered by QuickLaTeX.com H](../../assets/21b7e9a6311e544d.png)

![Rendered by QuickLaTeX.com L](../../assets/6046f3c7b4bcbd21.png)

![Rendered by QuickLaTeX.com V](../../assets/c746ecbc0d34d082.png)


![BlinnPhong](../../assets/8e37a57b6fec10a4.png)

![Rendered by QuickLaTeX.com \[\mathrm{Lambertian\,model:} \,\,\,\ I = N \cdot L\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-e0232f9d7e828ecc2fe9bc27212fcbf5_l3.png)


![Rendered by QuickLaTeX.com \[\mathrm{Blinn-Phong\,model:} \,\,\,\ I = \left ( N \cdot H \right )^{specular} \cdot gloss\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-494dbb98240fe1a6bd0dad6386a192b9_l3.png)


![Rendered by QuickLaTeX.com \[H = \frac{L+V}{\left| L +V\right|}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-02c51d83a8480875ad62ce8369a2b85e_l3.png)


The quantity ![Rendered by QuickLaTeX.com N \cdot H](../../assets/17cf2f3eda0a26a5.png)

![Rendered by QuickLaTeX.com specular](../../assets/0d4d6bc92962449b.png)

![Rendered by QuickLaTeX.com gloss](../../assets/342beac720098734.png)

[source for its built-in shaders](https://unity3d.com/get-unity/download/archive). Both the Lambertian and Blinn-Phong surface functions are calculated in the file *Lighting.cginc*. In Unity5 they’re available as Legacy shaders.

### Physically Based Rendering in Unity5

As mentioned at the beginning of this post, Uniy4.x was using the Lambertian lighting model as its default shader. Unity5 has changed that, introducing the [Physically Based Rendering](http://blogs.unity3d.com/2014/10/29/physically-based-shading-in-unity-5-a-primer/) (PBR). The name sounds very intriguing, but is nothing more then another lighting model. Compared to the Lambertian reflectange, PBR provides a more realistic interaction between lights and objects. The term *physically* refers to the fact that PBR takes into account physical properties of materials, such as conservation of energy and light scatter. Unity5 provides two different ways for artists and developers to create their PBR materials: the *Metallic workflow* and the *Specular workflow*. In the first one, the way a material reflects light depends on how metallic it is. A cheap explanation is that light is an electromagnetic wave, and it behaves differently when in contact with a *conductor* or an *insulator*. In the Specular workflow, a specular map is provided instead. Despite being presented as two different things, Metallic and Specular materials are actually different ways to initialise the same shader; [Marmoset](http://www.marmoset.co/toolbag/learn/pbr-practice) has a very well done tutorial in which it shows how the same material can be created both with the Metallic and Specular workflows. Having two workflows for the same thing is one of the main sources of misunderstanding when approaching Unity5 shaders for the first time. [Joe Wilson](http://www.marmoset.co/toolbag/learn/pbr-practice) made an incredibly clear tutorial oriented to artists: it’s a good starting point if you want to learn how to use PBR to create highly realistic materials. If you need some more technical information, there’s [a very well done primer](http://blogs.unity3d.com/2015/02/18/working-with-physically-based-shading-a-practical-approach/) on PBR on the Unity5 blog.

![metallic](../../assets/033d775d2912c939.png)

The name of Unity5’s new lighting model is, simply, `Standard`

. The reason behind this name is that PBR is now the default material for every new object created in Unity3D. Moreover, every new shader file created is automatically configured as a PBR surface shader:

Shader "Custom/NewShader" { Properties { _Color ("Color", Color) = (1,1,1,1) _MainTex ("Albedo (RGB)", 2D) = "white" {} _Glossiness ("Smoothness", Range(0,1)) = 0.5 _Metallic ("Metallic", Range(0,1)) = 0.0 } SubShader { Tags { "RenderType"="Opaque" } LOD 200 CGPROGRAM // Physically based Standard lighting model, and enable shadows on all light types #pragma surface surf Standard fullforwardshadows // Use shader model 3.0 target, to get nicer looking lighting #pragma target 3.0 sampler2D _MainTex; struct Input { float2 uv_MainTex; }; half _Glossiness; half _Metallic; fixed4 _Color; void surf (Input IN, inout SurfaceOutputStandard o) { // Albedo comes from a texture tinted by color fixed4 c = tex2D (_MainTex, IN.uv_MainTex) * _Color; o.Albedo = c.rgb; // Metallic and smoothness come from slider variables o.Metallic = _Metallic; o.Smoothness = _Glossiness; o.Alpha = c.a; } ENDCG } FallBack "Diffuse" }

![soldier standard](../../assets/bd39ca9c2d3629f1.png)

**Line 14** tells Unity3D that this surface shader will use the PBR lighting model. **Line 17** signals that advanced features are being used in this shader, hence it won’t be able to run on outdated hardwares. For the same reason, `SurfaceOutput`

can’t be used with PBR; `SurfaceOutputStandard`

must be used instead.

#### PBR surface outputs

Along `Albedo`

, `Normal`

, `Emission`

and `Alpha`

, there are three new properties available in `SurfaceOutputStandard`

:

`half Metallic`

: how metallic the object is. It’s usually either 0 or 1, but intermediate values can be used for bizarre materials. It will determine how light reflects on the material;`half Smoothness`

: indicates how smooth the surface is, from 0 to 1;`half Occlusion`

: indicates the amount of ambient occlusion.

If you want to use the Specular workflow, you should use `SurfaceOutputStandardSpecular`

which replaces `half Metallic`

with `float3 Specular`

. Note that while the Lambertian reflectance has a specular field which is `half`

, the specular property in PBR is a `float3`

. It corresponds to the RGB colour of the specularly reflected light.

### Shading technique used in Unity

So far, four different shading techniques have been introduced. To avoid confusion, you can refer to the table below which indicates, in order: shading technique, surface shader name, surface output structure name and the name of the respective built-in shader.

| Unity 4 and below | Unity 5 and above | |
|---|---|---|
Diffuse | Lambertian reflectance | Physically Based Rendering (Metallic) |
`Lambert` `Surface Output` | `Standard` `SurfaceOutputStandard` | |
| Bumped Diffuse | Standard | |
| ||
Specular | Blinn-Phong reflectance | Physically Based Rendering (Specular) |
`BlinnPhong` `SurfaceOutput` | `StandardSpecular` `SurfaceOutputStandardSpecular` | |
| Bumped Specular | Standard (Specular setup) | |
|

The equations behind PBR are rather complicated. If you are interested in understanding the Maths behind it, both the Wikipedia page for [Rendering equation](https://en.wikipedia.org/wiki/Rendering_equation) and [this article](http://www.codinglabs.net/article_physically_based_rendering.aspx) are good starting points.

If you imported the [Unity3D package](https://drive.google.com/file/d/0B4nCcaMlgxV2eEVkV250MGFVLWM/view?usp=sharing) (which includes the shader used in this tutorial), you’ll notice how the built-in “Bumped Diffuse” shader yields a very different result compared to its naive implementation “Simple Lambert”. This is because Unity3D’s shader adds additional features, such as normal maps.

### Conclusion

This post introduced custom lighting models for surface shaders. The Lambertian and Blinn-Phong models are briefly explained, with a real example of how they can be changed to obtain different effects. It is important to notice that purely diffuse materials don’t really exist in real life: even [the most dull material](http://filmicgames.com/archives/547) you can think of will have some specular reflection. Diffuse materials were very common in the past, when calculating specular reflections was too expensive.

The post also shows what physically based rendering is, and how it can be used in Unity5. PBR shaders are nothing more then surface shaders with a very advanced lighting model.

- Part 1:
[A gentle introduction to shaders in Unity3D](https://www.alanzucconi.com/2015/06/10/a-gentle-introduction-to-shaders-in-unity3d/) - Part 2:
[Surface shaders in Unity3D](https://www.alanzucconi.com/2015/06/17/surface-shaders-in-unity3d/) - Part 3:
**Physically Based Rendering and lighting models in Unity3D** - Part 4:
[Vertex and fragment shader in Unity3D](https://www.alanzucconi.com/2015/07/01/vertex-and-fragment-shaders-in-unity3d/) - Part 5:
[Screen shaders and postprocessing effects in Unity3D](https://www.alanzucconi.com/2015/07/08/screen-shaders-and-postprocessing-effects-in-unity3d/)

## Leave a Reply Cancel reply