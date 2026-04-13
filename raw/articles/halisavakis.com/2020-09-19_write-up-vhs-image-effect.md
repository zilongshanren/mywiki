---
title: 'Write-up: VHS Image Effect'
url: https://halisavakis.com/write-up-vhs-image-effect/
published: '2020-09-19'
source_blog: Technically Art – Harry Alisavakis
source_site: https://halisavakis.com
category: graphics
fetched: '2026-04-13'
---

## Introduction

Recently, in [my Discord server](https://discord.gg/e9XnPFv), some members had the idea of starting a small and chill tech-art jam event, with different themes, to produce results around anything in tech-art; be it tools, VFX, shaders etc. More on these challenges on the first tech-art challenge digest, which should be coming soon.

This week’s theme was “Retro shaders”, given by [Simon Trümpler](https://simonschreibt.de), and was a very neat and open-ended theme that gave a lot of food for thought to the participants.

I, being quite a big procrastinator, started working on the challenge the night of the last day, and thought I’d try a VHS video image effect, which I wanted to try for quite a while. My main inspiration was the game “[September 1999](https://98demake.itch.io/september1999)” that had a really intense and realistic VHS effect and I really wanted to see how close I could get to that feel and to basically erase the pristine details of a normal 3D scene.

## The result

My result, in motion, looks like this:

![](../../assets/7cd4d643834acd60.gif)

## Setup

I started by setting up a small room in Blender using the pretty awesome “Archimesh” add-on, which looked like this:

![](../../assets/089a665bad9d5a94.png)

As I wanted to get a similar look to this moment from “September 1999”:

![](../../assets/c23f9f99557bd641.png)

I brought the scene into Unity and, using some textures from [textures.com](https://textures.com) and some minor post-processing from Unity’s PPv2 (mainly bloom, AO and Vignette), I got this little scene:

![](../../assets/c113de957b26e873.png)

Needless to say, I got a bit over-excited with real-time GI and bounced light, as this is all lit just using a single point-light, not even using any ambient lighting here.

## Effect elements

First off, I gathered a bunch of references to understand what makes a video look like it’s from the 90’s, while also looking very closely at the screenshots from “September 1999”. The main thing that stood out to me was the color bleeding at the edges:

![](../../assets/c0c9a602cf9a220d.jpg)

In old video footage the edges aren’t very sharp and it seemed as if the colors bleeded into each other.

A great reference was also [this shader](https://www.shadertoy.com/view/ldjGzV) from shadertoy:

![](../../assets/90e0c53829c2392f.png)

from which I also got the UV distortion code.

The rest of the effects were mainly UV distortion with some random lines moving along the Y axis and some additional noise on top in various forms; a subtle grain noise on top of the whole thing, some noise lines going up and down and some more noise on the top and bottom edges of the screen.

## The implementation

Initially I started with the UV distortion from the aforementioned shadertoy. This gave me an interesting fish-eye-like effect that looked like this:

![](../../assets/f0989fb78f92eb12.png)

Then, I tried to tackle the color bleed effect, as I thought it was the most important. I’m sure there are proper ways to do it, but I basically combined some chromatic aberration with some blurring caused by sampling the main texture a bunch of times with a small offset on the X axis and dividing by the number of samples.

This gave me this result:

![](../../assets/9d7ca6e07f1e958c.png)

It’s a bit excessive, especially upclose, but it could be adjusted by depth so that closer objects are a bit sharper. I also decided to go with a blue-yellow chromatic aberration effect here instead of the classic red/green/blue; thought it’d feel more ol’-timey.

I also added a bunch of lines displacing the colors in a different way, inspired by the many fine lines that are visible in “September 1999”. Up close, the lines look like this:

![](../../assets/388e3b894ad840f2.png)

So, at this point I had something that looked like this:

![](../../assets/1b81d93af99896ff.png)

I thought it was going towards the right direction, but it kinda bothered me how intense the contrast was on the colors, especially comparing the floor to the walls. So, the next thing I did was to reduce the contrast a bit, by shifting the colors a little bit towards (0.5,0.5,0.5):

![](../../assets/38b90da624fe1b00.png)

Then it was time for more displacements! First there were these lines that went up and down randomly with semi-random speeds and displaced the image based on a sine method.

![](../../assets/73e2cf6e99bb51ac.png)

Then, there is the periodic displacement that moved the whole screen downwards and wraps around like so:

![](../../assets/92a0600176899612.png)

Finally, the noise! I used a classic random method to generate some random noise, which is used both for randomizing the timing of the displacement effects and for a slight grain effect on the image. Then I also used a noise texture for the top and bottom noise as well as for the passing lines. Those lines actually are based on the same sine lines used for the displacement, but use a different random threshold to determine when they’ll show up.

The whole thing looks like this now:

![](../../assets/8af1be28d0c45dd4.png)

I then added the obligatory text elements on a UI and that’s how we got the featured image!

![](../../assets/6e23121458362f3c.png)

## The code

Here’s the shader for the image effect:

```
Shader "Hidden/VHSShader"
{
Properties
{
_MainTex ("Texture", 2D) = "white" {}
_LensDistortion("Lens distortion", float) = 1.2
_ChromaticAberration("Chromatic aberration", float) = 0
_ColorBleedIterations("Color bleed iterations", float) = 0
_ColorBleedAmount("Color bleed amount", float) = 0
_LineAmount("Line amount", float) = 1
_LinesDisplacement("Lines displacement", float) = 0
_LinesSpeed("Lines speed", float) = 0
_Contrast("Contrast", Range(0,1)) = 1
_SineLinesAmount("Sine lines amount", float) = 1
_SineLinesSpeed("Sine lines speed", float) = 0
_SineLinesThreshold("Sine lines threshold", Range(0,1)) = 0
_SineLinesDisplacement("Sine lines displacement", float) = 0
_NoiseTexture("Noise texture", 2D) = "white" {}
}
SubShader
{
// No culling or depth
Cull Off ZWrite Off ZTest Always
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
};
struct v2f
{
float2 uv : TEXCOORD0;
float4 vertex : SV_POSITION;
};
v2f vert (appdata v)
{
v2f o;
o.vertex = UnityObjectToClipPos(v.vertex);
o.uv = v.uv;
return o;
}
sampler2D _MainTex;
float4 _MainTex_TexelSize;
float _ChromaticAberration;
float _ColorBleedAmount;
float _ColorBleedIterations;
float _LineAmount;
float _LinesDisplacement;
float _Contrast;
float _Vignette;
float _LensDistortion;
float _LinesSpeed;
float _SineLinesAmount;
float _SineLinesDisplacement;
float _SineLinesThreshold;
float _SineLinesSpeed;
sampler2D _NoiseTexture;
float4 _NoiseTexture_ST;
//from https://www.shadertoy.com/view/ldjGzV
float2 screenDistort(float2 uv) {
uv -= 0.5;
uv = uv*_LensDistortion*(1./1.2+2.*uv.x*uv.x*uv.y*uv.y);
uv += .5;
return uv;
}
float rand (in float2 st) {
return frac(sin(dot(st.xy, float2(12.9898,78.233)))*43758.5453123);
}
fixed4 frag (v2f i) : SV_Target
{
float2 uv = i.uv;
//UV distortion
uv = screenDistort(uv);
fixed colR = 0;
fixed colG = 0;
fixed colB = 0;
float offset = 0;
//Getting solid lines
float lines = step(0.5, frac(uv.y * _LineAmount + _Time.y * _LinesSpeed)) * 2.0 - 1.0;
float linesDispl = lines * _LinesDisplacement;
//Offsetting and wrapping the whole screen overtime
uv.y = frac(uv.y + lerp(0.0, 0.4, frac(_Time.z * 2.0) * step(0.97, rand(floor(_Time.z * 2.0)))));
//Constantly changing random noise values
float random = rand(uv + _Time.x);
//Sampling the noise texture while also making it move constantly
float noise = tex2D(_NoiseTexture, uv * _NoiseTexture_ST.xy + rand(_Time.x)).x;
//Getting random values from -1 to 1 every few frames to randomly change the speed and direction of the sine lines
float sineLinesTime = _Time.y * _SineLinesSpeed * (rand(floor(_Time.y)) * 2.0 - 1.0);
float sineLines = sin(uv.y * _SineLinesAmount * UNITY_PI * 2.0 + sineLinesTime) * 0.5 + 0.5;
//Lines with a random 0-1 value, to be used as mask
float randLines = rand(round(uv.y * _SineLinesAmount + sineLinesTime));
float sineLinesMask = step(randLines, _SineLinesThreshold);
float sineLinesDispl = sineLines * sineLinesMask * _SineLinesDisplacement;
//Multiple sampling for color bleeding
for (int k = 0; k < _ColorBleedIterations; k++) {
offset += lerp(0.8, _ColorBleedAmount, sin(_Time.y) * 0.5 + 0.5);
colR += tex2D(_MainTex, uv + float2(offset + _ChromaticAberration + linesDispl + sineLinesDispl, 0) * _MainTex_TexelSize.xy).r;
colG += tex2D(_MainTex, uv + float2(offset + _ChromaticAberration - linesDispl + sineLinesDispl, 0) * _MainTex_TexelSize.xy).g;
colB += tex2D(_MainTex, uv + float2(offset + linesDispl + sineLinesDispl, 0) * _MainTex_TexelSize.xy).b;
}
colR /= _ColorBleedIterations;
colG /= _ColorBleedIterations;
colB /= _ColorBleedIterations;
fixed4 col = fixed4(colR, colG, colB, 1.0);
//Reducing contrast
col = lerp(0.5, col, _Contrast);
//Grain noise
col *= max(0.7, random);
//Top and bottom noise
col += smoothstep(abs(uv.y * 2.0 - 1.0) - 0.8, abs(uv.y * 2.0 - 1.0) - 0.99, noise);
//Passing lines noise
col += step(0.99, 1.0 - randLines) * step(sineLines, noise) * 0.2;
return col;
}
ENDCG
}
}
}
```

Most of the code here is pretty rushed and, while straightforward, it looks a bit messy, cause it’s like, game jam shader code, consisting of a lot of trial and error. Feel free to play with stuff yourself to see how it feels!

## The package

Since the point of these challenges is to share as much as we can, I am linking here a unity package with the complete scene shown here, so you can play around with the effect and the shader yourself! Hope it proves useful to you! 😀

## Conclusion

The point of these challenges is to take place every two weeks, so hopefully I’ll have more write-ups to share soon! If you’re interested, don’t forget to pop on the [Discord server](https://discord.gg/e9XnPFv) to see progress on the challenge in real time or even participate yourself! The more the merrier! 😀