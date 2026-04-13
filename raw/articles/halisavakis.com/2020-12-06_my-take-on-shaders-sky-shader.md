---
title: 'My take on shaders: Sky shader'
url: https://halisavakis.com/my-take-on-shaders-sky-shader/
published: '2020-12-06'
source_blog: Technically Art – Harry Alisavakis
source_site: https://halisavakis.com
category: graphics
fetched: '2026-04-13'
---

## Patrons

This tutorials is brought to you by these awesome Patrons:

- orels1
- Tiph’ (DN)
- Not Invader Zim

## Introduction

This tutorial is long overdue, as the subject of a skybox shader is pretty common and useful. It’s also one of the shaders that can have so many different features and approaches, ranging from a simple 2-color gradient to a whole physically-accurate model of the earth’s atmosphere. This tutorial is much closer to the former than it is to the latter and its intended purpose is mostly for more stylized scenes; though you could maybe get some realistic-looking colors out of it too.

This shader has been inspired by other great shaders like the [sky shader](https://medium.com/@jannik_boysen/procedural-skybox-shader-137f6b0cb77c) by [Jannik Boysen](https://twitter.com/jannik_boysen) and the [stylized sky shader](https://www.patreon.com/posts/making-stylized-27402644) by [Minionsart](https://twitter.com/minionsart).

## Shader features

This shader basically has these features:

- Three color gradient going from the bottom of the skybox to the top, with adjustable blending smoothness and offset.
- Sun disc positioned based on the scene’s directional light.
- Moon with adjustable phase, again positioned based on the scene’s directional light.
- Small support for a stars texture that appears when the sun is down.
- Horizon clouds (the ones you can see far in the distance, not the ones above your head) with adjustable coverage, edge smoothness etc. The clouds also feature some emission based on the sun’s position, so there’s a silver lining effect as well as a glow when the clouds are covering the sun or are near it. These effects don’t apply to the moon, but you could easily expand the shader so that they do.

## Shader code

Let’s take a look at the shader then. Keep in mind that most of the stuff here are for the operations on the clouds/sun etc which might look a bit complicated; but hopefully stuff will make some sense.

```
Shader "Skybox/SkyShader"
{
Properties
{
[Header(Sky color)]
[HDR]_ColorTop("Color top", Color) = (1,1,1,1)
[HDR]_ColorMiddle("Color middle", Color) = (1,1,1,1)
[HDR]_ColorBottom("Color bottom", Color) = (1,1,1,1)
_MiddleSmoothness("Middle smoothness", Range(0.0,1.0)) = 1
_MiddleOffset("Middle offset", float) = 0
_TopSmoothness("Top smoothness", Range(0.0, 1.0)) = 1
_TopOffset("Top offset", float) = 0
[Header(Sun)]
_SunSize("Sun size", Range(0.0, 1.0)) = 0.1
[HDR]_SunColor("Sun color", Color) = (1,1,1,1)
[Header(Moon)]
_MoonSize("Moon size", Range(0,1)) = 0
[HDR]_MoonColor("Moon color", Color) = (1,1,1,1)
_MoonPhase("Moon phase", Range(0,1)) = 0
[Header(Stars)]
_Stars("Stars", 2D) = "black" {}
_StarsIntensity("Stars intensity", float) = 0
[Header(Clouds)]
[HDR]_CloudsColor("Clouds color", Color) = (1,1,1,1)
_CloudsTexture("Clouds texture", 2D) = "black" {}
_CloudsThreshold("Clouds threshold", Range(0.0, 1.0)) = 0
_CloudsSmoothness("Clouds smoothness", Range(0.0, 1.0)) = 0.1
_SunCloudIntensity("Sun behind clouds intensity", Range(0, 1)) = 0
_PanningSpeedX("Panning speed X", float) = 0
_PanningSpeedY("Panning speed Y", float) = 0
}
SubShader
{
Tags { "RenderType"="Background" "Queue"="Background" "PreviewType"="Quad"}
LOD 100
Pass
{
CGPROGRAM
#pragma vertex vert
#pragma fragment frag
#include "UnityCG.cginc"
struct appdata
{
float4 vertex : POSITION;
float3 uv : TEXCOORD0;
};
struct v2f
{
float3 uv : TEXCOORD0;
float4 vertex : SV_POSITION;
};
fixed4 _ColorBottom;
fixed4 _ColorMiddle;
fixed4 _ColorTop;
float _MiddleSmoothness;
float _MiddleOffset;
float _TopSmoothness;
float _TopOffset;
fixed4 _SunColor;
float _SunSize;
float _MoonSize;
fixed4 _MoonColor;
float _MoonPhase;
sampler2D _Stars;
float4 _Stars_ST;
float _StarsIntensity;
sampler2D _CloudsTexture;
float4 _CloudsTexture_ST;
fixed4 _CloudsColor;
float _CloudsSmoothness;
float _CloudsThreshold;
float _SunCloudIntensity;
float _PanningSpeedX;
float _PanningSpeedY;
v2f vert (appdata v)
{
v2f o;
o.vertex = UnityObjectToClipPos(v.vertex);
o.uv = v.uv;
return o;
}
fixed4 frag (v2f i) : SV_Target
{
float2 uv = float2(atan2(i.uv.x,i.uv.z) / UNITY_TWO_PI, asin(i.uv.y) / UNITY_HALF_PI);
float middleThreshold = smoothstep(0.0, 0.5 - (1.0 - _MiddleSmoothness) / 2.0, i.uv.y - _MiddleOffset);
float topThreshold = smoothstep(0.5, 1.0 - (1.0 - _TopSmoothness) / 2.0 , i.uv.y - _TopOffset);
fixed4 col = lerp(_ColorBottom, _ColorMiddle, middleThreshold);
col = lerp(col, _ColorTop, topThreshold);
float cloudsThreshold = i.uv.y - _CloudsThreshold;
float cloudsTex = tex2D(_CloudsTexture, uv * _CloudsTexture_ST.xy + _CloudsTexture_ST.zw + float2(_PanningSpeedX, _PanningSpeedY) * _Time.y);
float clouds = smoothstep(cloudsThreshold, cloudsThreshold + _CloudsSmoothness, cloudsTex);
float stars = tex2D(_Stars, (i.uv.xz / i.uv.y) * _Stars_ST.xy) * _StarsIntensity * saturate(-_WorldSpaceLightPos0.y) * (1.0 - clouds);
stars *= smoothstep(0.5, 1.0 , i.uv.y);
float sunSDF = distance(i.uv.xyz, _WorldSpaceLightPos0);
float sun = max(clouds * _CloudsColor.a, smoothstep(0, _SunSize, sunSDF));
float moonSDF = distance(i.uv.xyz, -_WorldSpaceLightPos0);
float moonPhaseSDF = distance(i.uv.xyz - float3(0.0, 0.0, 0.1) * _MoonPhase, -_WorldSpaceLightPos0);
float moon = step(moonSDF, _MoonSize);
moon -= step(moonPhaseSDF, _MoonSize);
moon = saturate(moon * -_WorldSpaceLightPos0.y - clouds);
float cloudShading = smoothstep(cloudsThreshold, cloudsThreshold + _CloudsSmoothness + 0.1, cloudsTex) -
smoothstep(cloudsThreshold + _CloudsSmoothness + 0.1, cloudsThreshold + _CloudsSmoothness + 0.4, cloudsTex);
clouds = lerp(clouds, cloudShading, 0.5) * middleThreshold * _CloudsColor.a;
float silverLining = (smoothstep(cloudsThreshold, cloudsThreshold + _CloudsSmoothness, cloudsTex)
- smoothstep(cloudsThreshold + 0.02, cloudsThreshold + _CloudsSmoothness + 0.02, cloudsTex));
silverLining *= smoothstep(_SunSize * 3.0, 0.0, sunSDF) * _CloudsColor.a;
col = lerp(_SunColor, col, sun);
fixed4 cloudsCol = lerp(_CloudsColor, _CloudsColor + _SunColor, cloudShading * smoothstep(0.3, 0.0, sunSDF) * _SunCloudIntensity);
col = lerp(col, cloudsCol, clouds);
col += silverLining * _SunColor;
col = lerp(col, _MoonColor, moon);
col += stars;
return col;
}
ENDCG
}
}
}
```

### Properties

Let’s talk a bit about the propeties:

Property | Description |
| _ColorTop | The HDR top color of the skybox. |
| _ColorMiddle | The HDR middle color of the skybox. |
| _ColorBottom | The HDR bottom color of the skybox. |
| _MiddleSmoothness | Determines how smoothly the bottom color will blend with the middle color. |
| _MiddleOffset | Offsets the start of the middle color in the Y axis. |
| _TopSmoothness | Determines how smoothly the middle color will blend with the top color. |
| _TopOffset | Offsets the start of the top color in the Y axis. |
| _SunSize | Adjusts the size of the sun disk. |
| _SunColor | The HDR color of the sun. |
| _MoonSize | Adjusts the size of the moon. |
| _MoonColor | The HDR color of the moon. |
| _MoonPhase | The phase of the moon; allows you to get a crescent moon shape instead of a solid disk. |
| _Stars | The texture used for the stars. Note that this property defaults to “black” instead of “white” like we’re used to with other textures; this is so that if you don’t provide a texture for the stars the sky won’t glow white (since the stars color is being added to the rest of the color). |
| _StarsIntensity | The intensity of the stars; gets multiplied with the color from the “_Stars” texture. |
| _CloudsColor | The HDR color of the clouds. The alpha channel defines the visibility of the clouds. |
| _CloudsTexture | The noise texture used for the clouds. FBM noise (or the Uniform Clouds from Photoshop) work best for more “realistic”-looking clouds. Again, this texture defaults to “black”. |
| _CloudsThreshold | Determines the height at which the clouds will be completely dissolved. |
| _CloudsSmoothness | The edge smoothness of the clouds; I usually keep it a low value so I get some smoothness at the edges without getting very wispy clouds. |
| _SunCloudIntensity | Determines the area where the sun’s color will be applied on the clouds, when they’re covering the sun. Something like a hacked version of translucency. |
| _PanningSpeedX | The panning speed of the clouds on the X axis. |
| _PanningSpeedY | The panning speed of the clouds on the Y axis. |

### The in-between stuff

One thing to note here is the tags in line 40; since this is a skybox shader and we want it to render behind everything, we have a special render type and queue to set, as you can see.

Another thing to keep in-mind also is the the UVs here are 3 dimensional instead of 2D. So both in the appdata struct and in the v2f struct, the “uv” field is a float3.

Lines 63-90 are just about redeclaration of the properties (along with some “_ST” field to adjust scaling and offset on some textures) and the vertex shader is the simplest it can be; just calculates the clip position as always and simply passes the UVs to the v2f object.

### The fragment shader

First up, in line 103 I’m calculating the UVs for the skybox in a manner that eliminates annoying stretching. This method is better described in [Jannik’s shader](https://medium.com/@jannik_boysen/procedural-skybox-shader-137f6b0cb77c).

Next up, in lines 104-107 I calculate the sky’s color by determining the different color zones on the skybox. In line 104 I get the start of the middle zone (called “middleThreshold”). i.uv.y goes from -1 to 1 and we want to manipulate the top half of our sky, so the middle part technically starts from the horizon and ends at the middle of the top hemisphere. To avoid having a hard cutoff, I’m using smoothstep, getting values from 0.0 to 0.5. I’m also using “_MiddleOffset” to adjust the height at which the middle zone starts.

The same procedure happens for the top threshold, and then the 3 colors are mixed together using the calculated thresholds. Do keep in mind that the whole bottom hemisphere uses the bottom color.

In lines 109-111 I calculate the main body of clouds on the skybox. I mainly sample the clouds texture (using _CloudsTexture_ST as well for the offset and scale of the texture) and pass it through a smoothstep using the y component of the sky’s UVs as the threshold. I’m also subtracting “_CloudsThreshold” from i.uv.y to adjust how dissolved the clouds get the further up they are.

In lines 113-114 I calculate the stars that will be visible at night time. Initially I sample the stars texture, though I’m using “i.uv.xz / i.uv.y” for the UV coordinates; this is to make sure the stars texture doesn’t get sampled on the shape of the skybox and gets stretched. This way, the stars will be sampled as if there was a big plane stretching about the ground.

The sampled texture gets multiplied with “_StarsIntensity” (though you could use an HDR color as well) and it’s then multiplied by the inverted _WorldSpaceLightPos0.y, which corresponds to the direction of the main directional light. When the directional light is looking upwards we basically have night-time and that’s when “saturate(-_WorldSpaceLightPos0.y)” is 1 and we can see the stars. The stars are also multiplied by “(1.0 – clouds)” so they don’t appear on top of the clouds. I also mostly wanted the stars to appear at the top part of the skybox, so I’m multiplying them by a smoothstep going from the middle of the top skybox hemisphere to its top.

In lines 116-117 I calculate the shape of the sun. Initially, I just get the distance of the main directional light from the current UV position on the skybox, which will give us a nice circular gradient that we can then clamp to our liking. For that reason, in line 117 I use smoothstep to clamp the aforementioned distance. Since I’m cranking up the HDR and bloom for the sun either way I don’t really care for harsher edges, otherwise a “step” could work as well. I want the sun to be blocked by clouds, though, so I also pass that smoothstep through a max function, so the sun is hidden when there are clouds in front of it.

Lines 119-123 are all about getting the shape of the moon. Since we want the moon to appear when the sun is down, we’re using the inverted world-space position of the main directional light (which btw corresponds to its direction, not its actual position, since the origin of a directional light is irrelevant). That being said, line 119 just gets the distance from the inverted world-space position of the light and the current UV position, like I did for the sun.

In line 120 I also get the distance from the inverted light direction to the current UV position, but I also offset it a bit so I can get another disc which I can subtract from the first one in order to get the shape of a crescent moon with adjustable phase. You can also expose the offset direction for more control, but for now I’m just offsetting in the z axis.

The main moon disc is calculated in line 121 using a step function; then in line 122 I subtract the solid disc of the second disc from the first one.

In line 123 I also multiply the final moon shape by the y axis of the inverted light position so that it fades in when the sun is down, and I subtract the clouds from it so that, again the moon hides behind the clouds.

In line 111 we got just the solid shape of the clouds, but in lines 125-127 I also do some small tricks to get some shading on the clouds. In lines 125-126 I just calculate two smoothsteps, with slightly higher thresholds to get a sense of depth. These values are again hard-coded after some trial and error, but feel free to play around with them to see how the effect changes.

In line 127 I blend between the original clouds shape and the shaded one and I also multiply that with the middle threshold so it’s only visible in that zone. I also use the alpha channel of the “_CloudsColor” property to control the overall opacity of the clouds.

In lines 129-130 I pretty much do the same with the shading, with different thresholds to get a sharper area on the edge of the clouds to simulate the effect of a silver lining when the sun is behind the clouds. For this reason, in line 131 I multiply the silver lining with the sun SDF passed through a smoothstep. This is also multiplied by the alpha channel of the clouds color so it fades out with the rest of the clouds.

Finally, I’m putting all the colors together. In line 134 I apply the sun color with a lerp using the “sun” shape, which was technically just a value from 0 to 1. In line 135 I get the color of the clouds, taking into account the “shading” as well as the sun color when it’s behind the clouds. The “_SunCloudIntensity” there is used to determine the area of the clouds that are lit up by the sun when it’s behind them.

The clouds color is then added to the previous color, along with the silver lining, the moon and the stars.

## Sky controller

In order to have control over the sky’s colors as the time of day changes, I made a small script that goes on the main directional light and provides overrides for the properties of the sky. The values change based on the direction the sun is looking towards, so you can get some nice day-night cycles by just rotating your sun light.

Specifically, it provides gradients for:

- The top, middle and bottom color of the skybox
- The sun disc color
- The directional light color
- The ambient sky color (if your ambient lighting mode is set to “Color”).
- The clouds color.

You can also debug how the overrides look by using a scrub slider instead of moving your directional light around.

### The code

```
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
[ExecuteInEditMode, RequireComponent(typeof(Light))]
public class SkyController : MonoBehaviour {
[Header("Sky colors")]
public bool overrideSkyColors;
[GradientUsage(true)]
public Gradient topColor;
[GradientUsage(true)]
public Gradient middleColor;
[GradientUsage(true)]
public Gradient bottomColor;
[Header("Sun color")]
public bool overrideSunColor;
[GradientUsage(true)]
public Gradient sunColor;
[Header("Sun light color")]
public bool overrideLightColor;
public Gradient lightColor;
[Header("Ambient sky color")]
public bool overrideAmbientSkyColor;
[GradientUsage(true)]
public Gradient ambientSkyColor;
[Header("Clouds color")]
public bool overrideCloudsColor;
[GradientUsage(true)]
public Gradient cloudsColor;
[Header("Debug scrub")]
public bool useSrub = false;
[Range(0.0f, 1.0f)]
public float scrub;
private Light sun;
public Light Sun {
get {
if (sun == null) {
sun = GetComponent<Light>();
}
return sun;
}
}
private Material skyMaterial;
public Material SkyMaterial {
get {
if (skyMaterial == null) {
skyMaterial = RenderSettings.skybox;
}
return skyMaterial;
}
}
public void OnValidate() {
if (useSrub) {
UpdateGradients(scrub);
}
}
private void Update() {
if (!useSrub && Sun.transform.hasChanged) {
float pos = Vector3.Dot(Sun.transform.forward.normalized, Vector3.up) * 0.5f + 0.5f;
UpdateGradients(pos);
}
}
public void UpdateGradients(float pos) {
if (overrideSkyColors) {
SkyMaterial.SetColor("_ColorTop", topColor.Evaluate(pos));
SkyMaterial.SetColor("_ColorMiddle", middleColor.Evaluate(pos));
SkyMaterial.SetColor("_ColorBottom", bottomColor.Evaluate(pos));
}
if (overrideSunColor) {
SkyMaterial.SetColor("_SunColor", sunColor.Evaluate(pos));
}
if (overrideLightColor) {
Sun.color = lightColor.Evaluate(pos);
}
if (overrideAmbientSkyColor) {
if (RenderSettings.ambientMode == UnityEngine.Rendering.AmbientMode.Trilight) {
RenderSettings.ambientSkyColor = topColor.Evaluate(pos);
RenderSettings.ambientEquatorColor = middleColor.Evaluate(pos);
RenderSettings.ambientGroundColor = bottomColor.Evaluate(pos);
} else if (RenderSettings.ambientMode == UnityEngine.Rendering.AmbientMode.Flat) {
RenderSettings.ambientSkyColor = ambientSkyColor.Evaluate(pos);
}
}
if (overrideCloudsColor) {
SkyMaterial.SetColor("_CloudsColor", cloudsColor.Evaluate(pos));
}
}
}
```

There’s not a lot to explain here tbh, just pop this onto your directional light while you’re using a sky material with the shader above and you’ll see stuff happening. If values are not updating in edit mode initially, going into play mode first should fix that.

## Unity package

Here’s a small package with a demo scene, to get a sense of how this can all be set up, and what kind of gradients the sky controller uses:

## Conclusion

As it’s evident by the time it took me, this tutorial kicked my butt. It was a tough one mainly because besides some nice tricks, most of it was a bunch of smoothsteps that were a result of a lot of trial and error.

I really wanted to get this out though, because a sky shader is always useful, and I’ve found myself using this one in so many different scenes. At least I hope that this tutorial has offered you some useful bits and maybe some small insight into my process of making stuff.

I’ve been thinking of changing my format for the next tutorials, so I’ll have to think how that’ll work in order for me to provide more content that’s more useful and straightforward.

See you in the next one, whatever that may be! =]