---
title: 'My take on shaders: Grab pass distortion'
url: https://halisavakis.com/my-take-on-shaders-grab-pass-distortion/
published: '2019-07-21'
source_blog: Technically Art – Harry Alisavakis
source_site: https://halisavakis.com
category: graphics
fetched: '2026-04-13'
---

## Patrons

This shader tutorial post was brought to you by:

Erich Binder, Minh Triết Đỗ

## Introduction

I was quite surprised to see that while I had a tutorial on [grab pass shaders](https://halisavakis.com/my-take-on-shaders-grabpass/) and on [UV distortion](https://halisavakis.com/my-take-on-shaders-waving-displacement/), I didn’t actually have a tutorial on grab pass distortion. And I probably should have one, cause it’s a really useful effect, especially for VFX.

However, as I’m writing this I remembered why I didn’t make a tutorial on the effect. Unity used to have a shader for that effect in its “Effects” packages, the one with the refracting glass. But these effects are not as accessible anymore, and I recently had to remake the effect from scratch, so I figured I should add it to my archive.

This shader is quite short and simple: it takes an optional texture as the mask for the distortion and a normal map, and distorts the image behind the object to which the material is applied based on those two textures and a value that determines the amount of distortion.

## Code

The code looks like this:

Shader "Unlit/GrabPassDistortion"
{
Properties
{
_MaskTexture ("Mask texture", 2D) = "white" {}
[Normal]_DistortionGuide("Distortion guide", 2D) = "bump" {}
_DistortionAmount("Distortion amount", float) = 0
}
SubShader
{
Tags { "RenderType"="Transparent" "Queue"="Transparent"}
Cull Off
ZWrite Off
LOD 100
GrabPass
{
"_GrabTexture"
}
Pass
{
CGPROGRAM
#pragma vertex vert
#pragma fragment frag
#include "UnityCG.cginc"
struct appdata
{
float4 vertex : POSITION;
float2 uv : TEXCOORD0;
float4 color : COLOR;
};
struct v2f
{
float2 uv : TEXCOORD0;
float2 distortionUV : TEXCOORD1;
float4 grabPassUV : TEXCOORD2;
float4 vertex : SV_POSITION;
float4 color : COLOR;
};
float _DistortionAmount;
sampler2D _DistortionGuide;
float4 _DistortionGuide_ST;
sampler2D _MaskTexture;
float4 _MaskTexture_ST;
sampler2D _GrabTexture;
v2f vert (appdata v)
{
v2f o;
o.vertex = UnityObjectToClipPos(v.vertex);
o.uv = TRANSFORM_TEX(v.uv, _MaskTexture);
o.distortionUV = TRANSFORM_TEX(v.uv, _DistortionGuide);
o.grabPassUV = ComputeGrabScreenPos(o.vertex);
o.color = v.color;
return o;
}
fixed4 frag (v2f i) : SV_Target
{
fixed mask = tex2D(_MaskTexture, i.uv).x;
float2 distortion = UnpackNormal(tex2D(_DistortionGuide, i.distortionUV)).xy;
distortion *= _DistortionAmount * mask * i.color.a;
i.grabPassUV.xy += distortion * i.grabPassUV.z;
fixed4 col = tex2Dproj(_GrabTexture, i.grabPassUV);
return col;
}
ENDCG
}
}
}



## Properties

There are no surprises in the properties, there are only the stuff I mentioned in the introduction. The “_MaskTexture” texture contains the mask (duh), the “_DistortionGuide” is the normal map based on which the distortion will occure and “_DistortionAmount” is, well, the amount of the distortion. Pretty standard stuff.

Do note the “[Normal]” tag before “_DistortionGuide” though; it’s so that Unity shows you that “Fix Now” button when you add a texture that’s not imported as a normal map. Also, the default value of that texture is “bump” instead of white, so that there won’t be any funky behavior if you haven’t assigned a texture to the property.

## The in-between stuff

Due to its behavior, this shader needs to be declared as transparent. Therefore, I use the appropriate tags in lines 11 and 13. In line 12 I also use “Cull Off” so that the effect works when we look at the object from the back, but that’s not really necessary to have. Notice though that I haven’t included “Blend SrcAlpha OneMinusSrcAlpha” (which is standard for transparency), because it causes some uncool artifacts in combination with “Cull Off”.

In lines 16-19 there’s the very straightforward of getting the Grab pass information and storing it to a texture called “_GrabTexture”.

Since I’ve been using the effect with VFX and particle systems, I again decided to take advantage of the object’s vertex colors to control the amount of the distortion. This is why in the “appdata” struct I added the field to get the vertex color (line 33). In the “v2f” struct I also added the color field, along with 2 more fields: one for the UV coordinates of the normal map and one for the UVs of the grab pass (notice that it’s a float4 instead of a float2).

After all that, I just redeclare the properties, also adding a float4 “_MaskTexture_ST” to apply the scale/offset of the texture to its UVs. Also, note that I’m declaring a “_GrabTexture” sampler, cause even though there wasn’t one in the properties, we got it from the GrabPass block and need to access it.

## Vertex shader

Nothing too fancy going on in the vertex shader either. In lines 56 and 57 I use the “TRANSFORM_TEX” macro to apply the texture’s scaling and offset to the corresponding UVs. In line 58 I compute the Grab pass UV coordinates using the “ComputeGrabScreenPos” macro, and finally, in line 59 I pass the vertex color onto the fragment shader.

## Fragment shader

In the fragment shader I first sample the mask texture and store its red channel to a value called “mask”. Then, in line 66 I sample the distortion normal map, while also using “UnpackNormal” which maps the values of the texture to the [-1,1] range for us.

The result of the sampling is then multiplied by “_DistortionAmount”, the mask and the alpha channel of the vertex color (to be used with particle systems).

The way the distortion is applied is shown in line 68: the distortion value is added to the X and Y components of the grab pass UV coordinates, after it gets multiplied by the Z component of the grab pass texture coordinates.

After that, I just get the color of the grab pass texture with “tex2Dproj” and return it!

## Conclusion

That was a rather short post, but it’s definitely an effect that I’d like to keep in my archive. And it’s a really fun effect to use with VFX to add a lot of impact, like explosions and shockwaves.

The normal maps you’d probably want to use look something like this:

![](../../assets/9a1de8deec2c1dee.png)

You might not want any information on the edges, so the cutoff point wouldn’t be too obvious, but I think that with the mask texture there’s enough flexibility in that area.

I hope you find this effect useful, and I’ll see you in the [next one](https://halisavakis.com/my-take-on-shaders-simple-subsurface-scattering/)!