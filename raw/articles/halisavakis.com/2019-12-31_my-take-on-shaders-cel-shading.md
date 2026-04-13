---
title: 'My take on shaders: Cel shading'
url: https://halisavakis.com/my-take-on-shaders-cel-shading/
published: '2019-12-31'
source_blog: Technically Art – Harry Alisavakis
source_site: https://halisavakis.com
category: graphics
fetched: '2026-04-13'
---

## Patrons

This post is brought to you by these awesome Patreon supporters:

- orels1
- Tiph’ (DN)

## Introduction

Ok, it’s finally time for this tutorial. This is a shader that I’ve been teasing for more than a year, but other tutorial ideas got in the way, so I never got around to making this until now.

And even now, I wasn’t supposed to do tutorial; I should be doing a tutorial on the shader I used for this tree:

However, even though Patrons and other people chose the tree shader as the next tutorial theme, I realized that this shader heavily relies on my cel shading shader, so it wouldn’t make a lot of sense to do it before I go through my cel shading process.

Over time I’ve revisited this shader *a lot* and tried a bunch of different stuff with it, but the version I’ll be showing here is probably more on the robust and versatile side.

It’s worth mentioning that some of the approaches and features of this shader I got from [Ronja’s awesome toon shader tutorial](https://www.ronja-tutorials.com/2018/10/27/improved-toon.html). Also, Roystan happens to also have [a cool toon shader tutorial](https://roystan.net/articles/toon-shader.html) as well, so I suggest you check that one out too.

## Shader overview and features

As you can imagine, there’s nothing too crazy going on here; what I’ll be showing is a pretty standard approach.

- I have created a custom lighting model that handles how the lighting and attenuation is displayed on the object.
- I also added support for:
- Normal mapping
- Specular highlights which can be affected by a specular map
- Rim (which can be visible only on lit surfaces)
- Shadow banding


## The code

The complexity of the shader really doesn’t justify the amount of introduction above, so let’s jump into it:

```
Shader "Custom/CelShaded"
{
Properties
{
_Color ("Color", Color) = (1,1,1,1)
_MainTex ("Albedo (RGB)", 2D) = "white" {}
[Normal]_Normal("Normal", 2D) = "bump" {}
_LightCutoff("Light cutoff", Range(0,1)) = 0.5
_ShadowBands("Shadow bands", Range(1,4)) = 1
[Header(Specular)]
_SpecularMap("Specular map", 2D) = "white" {}
_Glossiness ("Smoothness", Range(0,1)) = 0.5
[HDR]_SpecularColor("Specular color", Color) = (0,0,0,1)
[Header(Rim)]
_RimSize("Rim size", Range(0,1)) = 0
[HDR]_RimColor("Rim color", Color) = (0,0,0,1)
[Toggle(SHADOWED_RIM)]
_ShadowedRim("Rim affected by shadow", float) = 0
[Header(Emission)]
[HDR]_Emission("Emission", Color) = (0,0,0,1)
}
SubShader
{
Tags { "RenderType"="Opaque" }
LOD 200
CGPROGRAM
#pragma surface surf CelShaded fullforwardshadows
#pragma shader_feature SHADOWED_RIM
#pragma target 3.0
fixed4 _Color;
sampler2D _MainTex;
sampler2D _Normal;
float _LightCutoff;
float _ShadowBands;
sampler2D _SpecularMap;
half _Glossiness;
fixed4 _SpecularColor;
float _RimSize;
fixed4 _RimColor;
fixed4 _Emission;
struct Input
{
float2 uv_MainTex;
float2 uv_Normal;
float2 uv_SpecularMap;
};
struct SurfaceOutputCelShaded
{
fixed3 Albedo;
fixed3 Normal;
float Smoothness;
half3 Emission;
fixed Alpha;
};
half4 LightingCelShaded (SurfaceOutputCelShaded s, half3 lightDir, half3 viewDir, half atten) {
half nDotL = saturate(dot(s.Normal, normalize(lightDir)));
half diff = round(saturate(nDotL / _LightCutoff) * _ShadowBands) / _ShadowBands;
float3 refl = reflect(normalize(lightDir), s.Normal);
float vDotRefl = dot(viewDir, -refl);
float3 specular = _SpecularColor.rgb * step(1 - s.Smoothness, vDotRefl);
float3 rim = _RimColor * step(1 - _RimSize ,1 - saturate(dot(normalize(viewDir), s.Normal)));
half stepAtten = round(atten);
half shadow = diff * stepAtten;
half3 col = (s.Albedo + specular) * _LightColor0;
half4 c;
#ifdef SHADOWED_RIM
c.rgb = (col + rim) * shadow;
#else
c.rgb = col * shadow + rim;
#endif
c.a = s.Alpha;
return c;
}
// Add instancing support for this shader. You need to check 'Enable Instancing' on materials that use the shader.
// See https://docs.unity3d.com/Manual/GPUInstancing.html for more information about instancing.
// #pragma instancing_options assumeuniformscaling
UNITY_INSTANCING_BUFFER_START(Props)
// put more per-instance properties here
UNITY_INSTANCING_BUFFER_END(Props)
void surf (Input IN, inout SurfaceOutputCelShaded o)
{
fixed4 c = tex2D (_MainTex, IN.uv_MainTex) * _Color;
o.Albedo = c.rgb;
o.Normal = UnpackNormal(tex2D(_Normal, IN.uv_Normal));
o.Smoothness = tex2D(_SpecularMap, IN.uv_SpecularMap).x * _Glossiness;
o.Emission = o.Albedo * _Emission;
o.Alpha = c.a;
}
ENDCG
}
FallBack "Diffuse"
}
```

### Properties

There’s a fair amount of properties in this one, so let’s get the table out:

| Property | Description |
|---|---|
| _Color | The main color of the object. |
| _MainTex | The main albedo texture of the object. |
| _Normal | The normal map of the material. Again, notice the “[Normal]” tag which automagically changes the import type of a texture to “Normal” if it’s not already. Also, it defaults to “bump” instead of “white” so you don’t get weird lighting if you haven’t assigned a texture. |
| _LightCutoff | Adjusts how much light will the object have, basically functioning as a threshold for N•L (the dot product of the object’s normal vector and the light direction). |
| _ShadowBands | Adjusts the number of the shadow bands. I have set the upper limit to be 4, but that can be easily increased. I usually keep it at 1 though. |
| _SpecularMap | A texture to adjust how shiny the object will be. Leave it blank o just have a circular specular (that rhymes) spot. |
| _Glossiness | Defines how big the specular contribution will be. |
| _SpecularColor | HDR color of the specular contribution. |
| _RimSize | Defines the size of the rim around the object. |
| _RimColor | HDR color of the rim around the object. |
| _ShadowedRim | Property that toggles the “SHADOWED_RIM” keyword, based on which the shader decides whether the rim will be shown only on lit areas or not. |
| _Emission | HDR color of the emission of the model. The color is later multiplied with the albedo color, but you could add an extra emission texture to use whatever colors you want. |

You’ll also notice I’ve added some headers on some sections to keep the properties somewhat organized. I know that’s not really consistent with my previous shaders, but I thought they’d help a bit with readability.

### Structs and stuff

Moving into the actual shader, in line 31 I replaced “Standard” in the “surface surf” pragma with “CelShaded”, as this will be our custom lighting model for this shader. If you want to remember how custom lighting models work, I suggest checking [the tutorial post on surface shaders](https://halisavakis.com/my-take-on-shaders-whats-the-deal-with-surface-shaders/).

In line 32 I added the shader feature for the “SHADOWED_RIM” keyword, which, as I mentioned above, toggles between showing the rim on shadowed areas or not. This adds a new shader variant for Unity to compile, you can get more insight on shader variants and shader features from [the tutorial on the vfx master shader](https://halisavakis.com/my-take-on-shaders-vfx-master-shader-part-i/).

Lines 36-50 are just the redeclarations of the properties above (minus the “_ShadowedRim” as we don’t need it in the shader) and in lines 52-58 there’s the “Input” struct, containing the separate UV coordinates for each of our three textures: the _MainTex, _Normal and _SpecularMap.

Reminder: In surface shaders, just declaring coordinates as “uv_” followed by the texture’s name, automatically applies the tiling and offset on those coordinates as set by the material inspector. No need to declare “_MainTex_ST” and all that, surface shaders do that on the background.

Below the “Input” struct, there’s the “SurfaceOutputCelShaded” struct, which is a custom struct which passes information from the “surf” method to the lighting model. It just contains the bare minimum for the lighting model to work and all those fields actually exist in the “SurfaceOutputStandard” struct, but I chose to make a custom one in case you need to add more fields yourself later.

### The surf method 🏄♂️

I’ll go through this here, cause all the juice is obviously in the lighting model.

Nothing too exciting is going on here actually. One noteworthy thing, though, is that the second parameter of the method is a “SurfaceOutputCelShaded” struct object, instead of a “SurfaceOutputStandard” struct object which is the default. The struct type should match the one used in the lighting model.

In line 102 I just sample the main texture and multiply the result with the main color, and the whole thing’s RGB values are then assigned to the “Albedo” field in line 103.

Line 104 is where I sample the normal map and unpack its values to assign them to the “Normal” field and, in line 105, I get the red channel of specular map which I multiply by “_Glossiness” to get the overall amount of specularity of the object.

Then, in line 106 I just multiply the albedo color with “_Emission” and assign it to the corresponding field, and in line 107 I assign the alpha value of the calculated color to the “Alpha” field. That’s pretty much it.

### The lighting model 💡

In lines 68-91 I define the lighting model for the cel-shading, and here’s where things get exciting.

First of all, the name of the method should be “LightingCelShaded” because I mentioned in the #pragma above that the lighting model will be called “CelShaded”. The parameters of the method are:

- A SurfaceOutputCelShaded struct object.
- The light direction.
- The view direction.
- The light attenuation.

Starting up, in lines 69-70 I calculate the lighting based on the object’s normals and the light direction. I first calculate the classic N•L which I then modify in line 70. I first divide the result of the N•L value by “_LightCutoff” to adjust the area of the lit surface, then multiply the result by the amount of shadow bands we want, round the result and divide it by the number of shadow bands. So, if we were to use 4 bands, we’d first multiply the N•L by 4 (so it’s now in the [0,4] spectrum), round it (so the values we get are either 0,1,2,3 or 4) and divide it again by 4 so that the resulting values are either 0, 0.25, 0.5, 0.75 or 1.

In lines 72-74 I calculate the specular highlights of the material. First, in line 72 I get the direction in which the light hitting the object’s surface would be reflected, using the handy “reflect” method. Then I get the dot product of the view direction and the inverted reflection vector and I use the inverted “Smoothness” value of the struct object as a threshold for the resulting dot product. The whole thing is multiplied by the specular color to be used in the final color result.

In line 76 I calculate the rim color. I get the inverted fresnel value by subtracting the dot product of the view direction and the object’s normals from 1, then I use the inverted value of “_RimSize” as a threshold for the step method and multiply the whole thing by “_RimColor” to use it later.

In lines 78-79 I just round the attenuation value (so it’s either 0 or 1) and then make a “shadow” field which is made up by multiplying the rounded attenuation value with the shading value calculated in line 70.

In line 81 I calculate the main color by adding the specular color to the albedo and multiplying the whole thing by “_LightColor0”. This will basically multiply the color of the object with the color of the light that’s affecting the object, whether that’s a directional light or otherwise. There’s no limit on the lights affecting the objects on the shader, just the pixel lights limit of your project.

Finally, in lines 84-88 I assign the final color to the RGB channels of “c”. If the “SHADOWED_RIM” keyword has been enabled, the rim color is added to the main color before the whole thing is multiplied by the shadow value, so there’s no rim lighting on the dark areas of the model. Otherwise, the rim is added after the main color is multiplied by shadow, so it’s added on top.

## Conclusion

This is a quite fun shader to play around and experiment with. There are a bunch of factors than can affect the result, especially the environment lighting of your scene. This setting can essentially color your shadows, so you could end up with some quite interesting visual results!

See you in the next one!

## Comments

Hi, this is great. Please could you make this tutorial in shader graph.

Because, custom shaders doesn’t work anymore in HDRP.

Author

Hi! I’m not sure if I’ll be able to make a shader graph tutorial on this soon, as I’m not too well-versed in it. However, a great tutorial that’ll help you get started is this one which goes through some of the same concepts. Should you follow that tutorial, applying some of the techniques shown in this one should be somewhat easy!

Nice tutorial. I’ve seen a number of write-ups about cel shading but this covers it really well.

One thing you might want to consider is moving the light attenuation inside the diffuse lighting calculation, that way it will be affected by the number of shadow bands. It won’t really affect directional lights but Point lights use the attenuation for their range, so rounding it to 0,1 drastically reduces their effective range.

half diff = round(saturate(nDotL / _LightCutoff) * _ShadowBands * atten) / _ShadowBands;

Author

Hi! Thank you very much for the comment, I actually didn’t think to try that. I played around a lot with the rounding to have both a nice cutoff and some visible bands, but it didn’t occur to me to move the attenuation in there. I’m sure it’ll work better for some use cases