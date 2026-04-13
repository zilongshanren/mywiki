---
title: 'My take on shaders: UI SDF Icon shader'
url: https://halisavakis.com/my-take-on-shaders-ui-sdf-icon-shader/
published: '2019-02-09'
source_blog: Technically Art – Harry Alisavakis
source_site: https://halisavakis.com
category: graphics
fetched: '2026-04-13'
---

Recently I came across this wonderful tip by [Mike Black](https://twitter.com/kurtruslfanclub) about making signed distance fields as icons for decals to get crisper results without increasing the size of your sprites:

I really enjoyed the simplicity of the process and it made me want to use the concept in Unity as well. The motive for me, though, was mostly about UI elements that got hella blurry while scaling. That, plus the realization that I don’t think I have shown any UI shaders here lead me to writing this short post.

There are 3 main segments to this tutorial:

- An intro to UI shaders and in what sense they’re different
- The actual shader for the SDF icons
- A short tutorial about creating SDFs of existing icon images in Photoshop to use with the shader

## UI Shaders Setup

Let’s get something clear from the start: UI Shaders are just plain shaders. They’re not working in a fundamentally different way, and they still look like default unlit shaders in their code’s architecture.

However, in order for them to work the way they do, with the scaling, and the masks and all the features Unity’s UI system provides, they have to include some adjustments in their vertex and fragment shader parts.

Do we care about this though? No, not really. Besides, this is not the subject of the post. So what I did for this shader, what I usually do and what I encourage you to do when you want to work with UI shaders is just get the zip folder of Unity’s built-in shaders from [Unity’s archive](https://unity3d.com/get-unity/download/archive), grab the default UI shader and work from there. Same thing goes for sprite shaders and pretty much for every weird shader Unity has and you want to see what makes it tick.

That being said, I will completely ignore the weird, unusual stuff that UI shaders include and just focus on the parts we’re interested in.

## The shader

Let’s check out the shader code:

Shader "UI/SDFIcon"
{
Properties
{
[PerRendererData] _MainTex ("Sprite Texture", 2D) = "white" {}
_Color ("Tint", Color) = (1,1,1,1)
_SDFThreshold("SDF Threshold", Range(0, 1)) = 0.5
_Smoothness("Smoothness", Range(0, 1)) = 0.2
_StencilComp ("Stencil Comparison", Float) = 8
_Stencil ("Stencil ID", Float) = 0
_StencilOp ("Stencil Operation", Float) = 0
_StencilWriteMask ("Stencil Write Mask", Float) = 255
_StencilReadMask ("Stencil Read Mask", Float) = 255
_ColorMask ("Color Mask", Float) = 15
[Toggle(UNITY_UI_ALPHACLIP)] _UseUIAlphaClip ("Use Alpha Clip", Float) = 0
}
SubShader
{
Tags
{
"Queue"="Transparent"
"IgnoreProjector"="True"
"RenderType"="Transparent"
"PreviewType"="Plane"
"CanUseSpriteAtlas"="True"
}
Stencil
{
Ref [_Stencil]
Comp [_StencilComp]
Pass [_StencilOp]
ReadMask [_StencilReadMask]
WriteMask [_StencilWriteMask]
}
Cull Off
Lighting Off
ZWrite Off
ZTest [unity_GUIZTestMode]
Blend SrcAlpha OneMinusSrcAlpha
ColorMask [_ColorMask]
Pass
{
Name "Default"
CGPROGRAM
#pragma vertex vert
#pragma fragment frag
#pragma target 2.0
#include "UnityCG.cginc"
#include "UnityUI.cginc"
#pragma multi_compile __ UNITY_UI_CLIP_RECT
#pragma multi_compile __ UNITY_UI_ALPHACLIP
struct appdata_t
{
float4 vertex : POSITION;
float4 color : COLOR;
float2 texcoord : TEXCOORD0;
UNITY_VERTEX_INPUT_INSTANCE_ID
};
struct v2f
{
float4 vertex : SV_POSITION;
fixed4 color : COLOR;
float2 texcoord : TEXCOORD0;
float4 worldPosition : TEXCOORD1;
UNITY_VERTEX_OUTPUT_STEREO
};
sampler2D _MainTex;
fixed4 _Color;
fixed4 _TextureSampleAdd;
float4 _ClipRect;
float4 _MainTex_ST;
float _SDFThreshold;
float _Smoothness;
v2f vert(appdata_t v)
{
v2f OUT;
UNITY_SETUP_INSTANCE_ID(v);
UNITY_INITIALIZE_VERTEX_OUTPUT_STEREO(OUT);
OUT.worldPosition = v.vertex;
OUT.vertex = UnityObjectToClipPos(OUT.worldPosition);
OUT.texcoord = TRANSFORM_TEX(v.texcoord, _MainTex);
OUT.color = v.color * _Color;
return OUT;
}
fixed4 frag(v2f IN) : SV_Target
{
fixed col = tex2D(_MainTex, IN.texcoord).x;
half4 color = _TextureSampleAdd + IN.color;
color.a *= smoothstep(_SDFThreshold, saturate(_SDFThreshold + _Smoothness), col);
#ifdef UNITY_UI_CLIP_RECT
color.a *= UnityGet2DClipping(IN.worldPosition.xy, _ClipRect);
#endif
#ifdef UNITY_UI_ALPHACLIP
clip (color.a - 0.001);
#endif
return color;
}
ENDCG
}
}
}



There’s a bunch of stuff going on in here, but as I said above, we don’t have to worry about most of it. In the properties block, I added 2 fields in lines 7 and 8: “_SDFThreshold” which determines the cutoff amount of the texture and “_Smoothness” which controls how smooth the icon will be around the edges.

The properties are redeclared in lines 84 and 85 and I then gently ignore whatever’s going on in the vertex shader.

As far as the fragment shader is concerned, my changes only take place in lines 103-105. First of all, since our input image will be an icon in SDF form, hence in grayscale, we don’t need any chromatic information besides the value of the texture in any channel. Therefore, in line 103, I sample the texture but only keep the value of the red channel in the “col” field.

Originally, in line 104 the default UI shader sampled the texture, added “_TextureSampleAdd” to it and multiplied the whole thing by “IN.color”. Here, however, we have no need to sample the texture and we just need the vertex color and the tint which is assigned on the material, so leaving it as ” half4 color = _TextureSampleAdd + IN.color; ” works for us.

Finally, in line 105 I perform a smoothstep function on the value I got from sampling the texture and with this function I basically say this: if the value of the SDF (“col”) is smaller than “_SDFThreshold”, return 0. If it’s bigger than “_SDFThreshold” but smaller than “_SDFThreshold + _Smoothness”, return the corresponding in-between value ranging from 0 to 1. If “col” is bigger than “_SDFThreshold + _Smoothness” then the method returns 1. Therefore, increasing the value of the threshold results in a smaller “slice” of the SDF, as it gets closer to the center.

## SDF Generation

Mike’s tweet above contains a tutorial on how to use Photoshop to generate signed distance fields with an icon, and the gist is this:

Add a stroke in the blending options of the icon’s layer and make sure the settings look something like this:

![](../../assets/29f4537627d0814a.png)

You might want to play around with the size depending on the image size, but if your result looks kinda like the featured image, you’re good to go!

## Conclusion

So this is it I believe. It’s a quite short and simple tutorial, but a good opportunity to also show some UI shaders. Hope you find this one useful enough to get some nice and crispy UI elements for your game!

See you in the [next one](https://halisavakis.com/my-take-on-shaders-parallax-effect-part-i/)!