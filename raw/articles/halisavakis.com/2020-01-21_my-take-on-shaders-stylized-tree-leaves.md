---
title: 'My take on shaders: Stylized tree leaves'
url: https://halisavakis.com/my-take-on-shaders-stylized-tree-leaves/
published: '2020-01-21'
source_blog: Technically Art – Harry Alisavakis
source_site: https://halisavakis.com
category: graphics
fetched: '2026-04-13'
---

## Patrons

This post is brought to you by these awesome Patreon supporters:

- Dario ‘Desarius’ Visaggio
- orels1
- Tiph’ (DN)

## Introduction

As I mentioned in the cel shading post, I was bound to make a shader tutorial on this subject, but the problem is that it heavily relied on the cel-shading one, as it’s basically the same shader with a couple of modifications.

That being said, it’s kinda important that you first had a look at [the cel shading tutorial post](https://halisavakis.com/my-take-on-shaders-cel-shading/) first, as I won’t be going too much into the custom lighting stuff.

It’s also important to note that this shader was kinda hard to make in a somewhat versatile manner. One can take many approaches when it comes to making trees, and since most tools out there take a procedural approach, it’s not easy to set the models up manually to achieve certain effects. I’ve tested most of the features of the shader using an approach like the one discussed in [Habrador’s blog post](https://blog.habrador.com/2018/05/how-to-make-stylized-witness-trees-in.html). However, I’ve applied the shader on trees produced by the [MTree Unity plugin](https://assetstore.unity.com/packages/tools/modeling/mtree-tree-creation-132433), and I can say it works well in most cases. But again, every approach is different, so your mileage may vary.

## Shader overview

This shader has a small amount of extra features from the original cel shading shader, but here’s what’s been added and removed:

Added:

- A texture cutoff property to clip the texture based on it’s Alpha value.
- UV displacement on the leaves to add some wind jitter, very much like
[the technique used by Dragos Matkovski](https://twitter.com/matkovskid/status/1175318154966384640). - Some fake Subsurface Scattering (SSS) to get some lighter colors when the light is shining from the back side of the leaves. The approach will be pretty much what has been shown in
[the SSS tutorial](https://halisavakis.com/my-take-on-shaders-simple-subsurface-scattering/). - Disabled culling due to the randomness of the leaves placement.

Removed:

- Shadow banding, as it was barely visible (or possible useful) in most cases.
- Specular lighting: didn’t feel like I’d personally use it, cause it mostly looked weird, but if you want to keep it nobody’s stopping ya!
- Normal map: for the stylized variant of this effect, normal maps were just adding noise, so I outright removed them. Again, if you think you’ll need them, you can easily add them!

## The code

```
Shader "Custom/TreeLeafShader"
{
Properties
{
_Color ("Color", Color) = (1,1,1,1)
_MainTex ("Albedo (RGB)", 2D) = "white" {}
_LightCutoff("Light cutoff", Range(0,1)) = 0.5
_TextureCutoff("Texture Cutoff", Range(0,1)) = 0.5
[Header(Rim)]
_RimSize("Rim size", Range(0,1)) = 0
[HDR]_RimColor("Rim color", Color) = (0,0,0,1)
[Toggle(SHADOWED_RIM)]
_ShadowedRim("Rim affected by shadow", float) = 0
[Header(Emission)]
[HDR]_Emission("Emission", Color) = (0,0,0,1)
[Header(Displacement)]
_DisplacementGuide("Displacement guide", 2D) = "white" {}
_DisplacementAmount("Displacement amount", float) = 0
_DisplacementSpeed("Displacement speed", float) = 0
[Header(SSS)]
_SSSConcentration("SSS Area Concentration", float) = 0
[HDR]_SSSColor("SSS color", Color) = (1,1,1,1)
}
SubShader
{
Tags { "RenderType"="Opaque" }
Cull Off
LOD 200
CGPROGRAM
#pragma surface surf Tree fullforwardshadows addshadow
#pragma shader_feature SHADOWED_RIM
#pragma target 3.0
fixed4 _Color;
sampler2D _MainTex;
float _LightCutoff;
float _TextureCutoff;
float _RimSize;
fixed4 _RimColor;
fixed4 _Emission;
float _SSSConcentration;
fixed4 _SSSColor;
sampler2D _DisplacementGuide;
float _DisplacementAmount;
float _DisplacementSpeed;
struct Input
{
float2 uv_MainTex;
float2 uv_DisplacementGuide;
};
struct SurfaceOutputTree
{
fixed3 Albedo;
fixed3 Normal;
float Smoothness;
half3 Emission;
float4 SSS;
fixed Alpha;
};
half4 LightingTree (SurfaceOutputTree s, half3 lightDir, half3 viewDir, half atten) {
half nDotL = saturate(dot(s.Normal, normalize(lightDir)));
half diff = step(_LightCutoff, nDotL);
half sssAmount = pow(saturate(dot(normalize(viewDir), -normalize(lightDir))), _SSSConcentration);
fixed4 sssColor = sssAmount * s.SSS;
float rimArea = step(1 - _RimSize ,1 - saturate(dot(normalize(viewDir), s.Normal)));
float3 rim = _RimColor * rimArea;
half stepAtten = round(atten);
half shadow = diff * stepAtten;
half3 col = s.Albedo * _LightColor0;
half4 c;
#ifdef SHADOWED_RIM
c.rgb = (col + rim) * shadow;
#else
c.rgb = col * shadow + rim;
#endif
c.rgb += sssColor.rgb * stepAtten * diff;
c.a = s.Alpha;
return c;
}
// Add instancing support for this shader. You need to check 'Enable Instancing' on materials that use the shader.
// See https://docs.unity3d.com/Manual/GPUInstancing.html for more information about instancing.
// #pragma instancing_options assumeuniformscaling
UNITY_INSTANCING_BUFFER_START(Props)
// put more per-instance properties here
UNITY_INSTANCING_BUFFER_END(Props)
void surf (Input IN, inout SurfaceOutputTree o)
{
float2 displ = (tex2D(_DisplacementGuide, IN.uv_DisplacementGuide + _Time.y * _DisplacementSpeed).xy * 2.0 - 1.0) * _DisplacementAmount;
fixed4 tex = tex2D(_MainTex, IN.uv_MainTex + displ);
fixed4 c = _Color;
o.Albedo = c.rgb;
clip(tex.a - _TextureCutoff);
o.Emission = o.Albedo * _Emission;
o.SSS = _SSSColor;
o.Alpha = c.a;
}
ENDCG
}
FallBack "Diffuse"
}
```

## Properties

I’m only going to cover the ones that aren’t included in the cel shading tutorial for brevity:

| Property | Description |
|---|---|
| _TextureCutoff | The value based on which the leaves texture is clipped. |
| _DisplacementGuide | The displacement texture used for the UV jitter to simulate wind. |
| _DisplacementAmount | The amount of the displacement happening to simulate wind. |
| _DisplacementSpeed | The speed of the panning of the displacement texture. |
| _SSSConcentration | Determines how spread out the SSS will be. |
| _SSSColor | The HDR color of the SSS. |

## Structs and stuff

Firstly, as mentioned, I have disabled the culling of the back faces by using “Cull Off” in line 31. Also, in line 35 I added “addshadow” so that when the leaves are clipped the cast a matching shadow. After that, there’s the “SHADOWED_RIM” keyword from the cel shading shader and then the redeclaration of all the properties. I named this lighting model as simply “Tree” so that there wouldn’t be any confusion with the cel shading one, so the struct used is accordingly named “SurfaceOutputTree” and the lighting method is called “LightingTree”. Simple enough.

Of course, in the “Input” struct, I just have the two uv coordinates set; one for the main texture and one for the displacement texture. Small note here: you probably want a larger scale noise when displacing the leaves to simulate wind, otherwise it’ll look like the leaves are distorting (unless that’s what you want 🤷♂️). I usually set the scale of the displacement texture to something like 0.1 in order to have larger waves.

## The surf method 🏄♀️

There’s some interesting bits in the surf method here and there, but nothing too exciting really.

In line 109 I just sample the displacement guide and apply the speed on the panning of the UVs, then map it from -1 to 1 and multiplying it by the amount. It’s the same thing I’ve done in a bunch of other posts, but here it’s in one line.

In line 114 I just use the “_TextureCutoff” property in a “clip” method by subtracting its value from the alpha value of the main texture channel. I also just pass in the color of the SSS in the struct to be used by the lighting method. At this point you might ask, why pass it in the struct if it’s just a property? And you’d be right, I could be using “_SSSColor” directly in the lighting method, however in the future you might want to add some extra control to the SSS, like, for example, using a mask to give more variation to the SSS effect. That’s up to you, but I just left that there so you can easily play around with it should you want to.

## The lighting 💡

This is the most “complex” part, though again, it’s mostly the same as the lighting model in the cel shading tutorial.

Firstly I get the N•L and then, in line 75, since I got rid of the shadow bands, I just use “_LightCutoff” as a threshold in a stepping function.

In lines 78-79 I do all the calculations for that fake SSS effect, firstly getting the dot product of the view direction vector and the inverted light direction and raising it to the power of “_SSSConcentration” to control the spread of it. After that I just multiply it with whatever I have in the “SSS” field of the SurfaceOutputTree object.

In lines 81-82 I kept the stuff about the rim, even if the rim is a bit peculiar when it comes to trees. Using a rim on a tree made with the technique shared above, will give some nice color variation on the edges, because of the spherized normals. However, with generated trees, like those from MTree for example, you’ll have weird cutoff artifacts with the rim effect. I just left it there if you need it, but keep in mind that this is a point where your tree-building approach matters. If you won’t use it as much, I suggest making another shader feature and a toggle to have a separate variant using rim, if you don’t want the calculations to happen all the time.

No specular here, so the color in line 87 is calculated just by multiplying the albedo with the color of the light.

Finally, in line 95 I just add the SSS color to the final color before returning it. Notice that I also multiply SSS by the attenuation and shading. This will limit the SSS to be visible only on the somewhat lit areas of the tree, which would be mostly on the edges. The difference can be seen here:

![](../../assets/2873d33e0c4f168c.png)

But again, if you use some other tricks, like masks etc to better fit your needs, go ahead and fiddle with that.

## Conclusion

Honestly, this is not as much a tutorial as it is a breakdown, as most (if not all) the features discussed here have been covered in previous tutorials as well. But I guess combining different features for a specific use case can be useful too.

I really hope you can get something out of this tutorial and fit into your workflow, while also extending it to your needs. You could add a bunch of stuff I didn’t, like some vertex displacement for more intense wind. However, don’t dream about using Unity’s Wind Zone properties to make it work out of the box without a separate script though; ironically enough, the global parameters of the wind zone are airtightly inaccessible via shader.

See you in the [next one](https://halisavakis.com/my-take-on-shaders-cliff-terrain-shader/)!