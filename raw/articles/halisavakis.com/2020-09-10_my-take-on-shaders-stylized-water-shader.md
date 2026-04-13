---
title: 'My take on shaders: Stylized water shader'
url: https://halisavakis.com/my-take-on-shaders-stylized-water-shader/
published: '2020-09-10'
source_blog: Technically Art – Harry Alisavakis
source_site: https://halisavakis.com
category: graphics
fetched: '2026-04-13'
---

## Patrons

This tutorials is brought to you by these amazing Patrons:

- orels1
- Tiph’ (DN)
- Not Invader Zim

## Introduction

By now you’ve already figured out that I’m quite fond of water shaders; both seeing them and making them. I have around 3-4 different water shader versions on my playground project and whenever I get new ideas to test out, I’ll make 3-4 more.

Now, I’ve already covered a water shader in [this older tutorial](https://halisavakis.com/my-take-on-shaders-water-shader/) though that one tends to be closer to a “realistic” look (even though it’s not really realistic) and features a bunch of bells and whistles. This shader, on the other hand, produces a simpler, more stylized water effect and, while it includes techniques from the previous water shader, it also introduces some other elements that could potentially inspire you for other effects as well.

## Shader features

This shader is a surface shader that once again uses that depth difference technique to calculate the intersection at three levels: the shoreline, the in-between intersection and the deep-water fog. This was designed to give us some nice color transitions and allow for more control over the color of the water based on depth.

There’s no vertex displacement, tessellation or height maps for this shader; it’s designed to be placed on a flat quad/plane and only uses two world-space-mapped normal maps that are blended together for more variety, but that’s about it.

Also, this shader has support for dynamic water ripples which use a separate orthograpic camera, a render texture and particles! Will also cover that here, but the core principle is the same as the one shown in [Minionsart’s](https://twitter.com/minionsart) [interactive water tutorial](https://www.patreon.com/posts/24192529).

## The (shader) code

Here’s the code for the shader:

```
Shader "Custom/StylizedWater"
{
Properties
{
[Header(Colors)]
[HDR]_Color ("Color", Color) = (1,1,1,1)
[HDR]_FogColor("Fog Color", Color) = (1,1,1,1)
[HDR]_IntersectionColor("Intersection color", Color) = (1,1,1,1)
[Header(Thresholds)]
_IntersectionThreshold("Intersction threshold", float) = 0
_FogThreshold("Fog threshold", float) = 0
_FoamThreshold("Foam threshold", float) = 0
[Header(Normal maps)]
[Normal]_NormalA("Normal A", 2D) = "bump" {}
[Normal]_NormalB("Normal B", 2D) = "bump" {}
_NormalStrength("Normal strength", float) = 1
_NormalPanningSpeeds("Normal panning speeds", Vector) = (0,0,0,0)
[Header(Foam)]
_FoamTexture("Foam texture", 2D) = "white" {}
_FoamTextureSpeedX("Foam texture speed X", float) = 0
_FoamTextureSpeedY("Foam texture speed Y", float) = 0
_FoamLinesSpeed("Foam lines speed", float) = 0
_FoamIntensity("Foam intensity", float) = 1
[Header(Misc)]
_RenderTexture("Render texture", 2D) = "black" {}
_Glossiness ("Smoothness", Range(0,1)) = 0.5
_FresnelPower("Fresnel power", float) = 1
}
SubShader
{
Tags { "RenderType"="Transparent" "Queue"="Transparent" }
Blend SrcAlpha OneMinusSrcAlpha
ZWrite Off
LOD 200
CGPROGRAM
#pragma surface surf Standard fullforwardshadows alpha:premul
#pragma target 3.0
struct Input
{
float4 screenPos;
float3 worldPos;
float3 viewDir;
};
fixed4 _Color;
fixed4 _FogColor;
fixed4 _IntersectionColor;
float _IntersectionThreshold;
float _FogThreshold;
float _FoamThreshold;
sampler2D _NormalA;
sampler2D _NormalB;
float4 _NormalA_ST;
float4 _NormalB_ST;
float _NormalStrength;
float4 _NormalPanningSpeeds;
sampler2D _FoamTexture;
float4 _FoamTexture_ST;
float _FoamTextureSpeedX;
float _FoamTextureSpeedY;
float _FoamLinesSpeed;
float _FoamIntensity;
sampler2D _RenderTexture;
half _Glossiness;
float _FresnelPower;
sampler2D _CameraDepthTexture;
float3 _CamPosition;
float _OrthographicCamSize;
// Add instancing support for this shader. You need to check 'Enable Instancing' on materials that use the shader.
// See https://docs.unity3d.com/Manual/GPUInstancing.html for more information about instancing.
// #pragma instancing_options assumeuniformscaling
UNITY_INSTANCING_BUFFER_START(Props)
// put more per-instance properties here
UNITY_INSTANCING_BUFFER_END(Props)
void surf (Input IN, inout SurfaceOutputStandard o)
{
float2 rtUV = IN.worldPos.xz - _CamPosition.xz;
rtUV = rtUV/(_OrthographicCamSize *2);
rtUV += 0.5;
fixed4 rt = tex2D(_RenderTexture, rtUV);
float depth = tex2Dproj(_CameraDepthTexture, UNITY_PROJ_COORD(IN.screenPos));
depth = LinearEyeDepth(depth);
float fogDiff = saturate((depth - IN.screenPos.w) / _FogThreshold);
float intersectionDiff = saturate((depth - IN.screenPos.w) / _IntersectionThreshold);
float foamDiff = saturate((depth - IN.screenPos.w) / _FoamThreshold);
foamDiff *= (1.0 - rt.b);
fixed4 c = lerp(lerp(_IntersectionColor, _Color, intersectionDiff), _FogColor, fogDiff);
float foamTex = tex2D(_FoamTexture, IN.worldPos.xz * _FoamTexture_ST.xy + _Time.y * float2(_FoamTextureSpeedX, _FoamTextureSpeedY));
float foam = step(foamDiff - (saturate(sin((foamDiff - _Time.y * _FoamLinesSpeed) * 8 * UNITY_PI)) * (1.0 - foamDiff)), foamTex);
float fresnel = pow(1.0 - saturate(dot(o.Normal, normalize(IN.viewDir))), _FresnelPower);
o.Albedo = c.rgb;
float3 normalA = UnpackNormalWithScale(tex2D(_NormalA, IN.worldPos.xz * _NormalA_ST.xy + _Time.y * _NormalPanningSpeeds.xy + rt.rg), _NormalStrength);
float3 normalB = UnpackNormalWithScale(tex2D(_NormalB, IN.worldPos.xz * _NormalB_ST.xy + _Time.y * _NormalPanningSpeeds.zw + rt.rg), _NormalStrength);
o.Normal = normalA + normalB;
o.Smoothness = _Glossiness;
o.Alpha = lerp(lerp(c.a * fresnel, 1.0, foam), _FogColor.a, fogDiff);
o.Emission = foam * _FoamIntensity;
}
ENDCG
}
FallBack "Diffuse"
}
```

### Properties

Name | Description |
| _Color | The color of the water when it’s not too close to the shore and not deep enough. |
| _FogColor | The color of the water when it’s deep enough. |
| _IntersectionColor | The color of the water close to the shore. |
| _IntersectionThreshold | The threshold that determines the size of the area close to the shore that will be colored as defined by “_IntersectionColor”. |
| _FogThreshold | The threshold that determines the depth at which the water will be colored as defined by “_FogColor”. |
| _FoamThreshold | The threshold that determines how far away from the shore the water will have foam/shorelines. |
| _NormalA | The first normal map texture. |
| _NormalB | The second normal map texture. |
| _NormalStrength | The strength of the normals (including those from the ripples). |
| _NormalPanningSpeeds | The panning speeds for each of the two normal maps. This is a vector4 field where: X – The speed of the NormalA texture in the X axis. Y – The speed of the NormalA texture in the Y axis. Z – The speed of the NormalB texture in the X axis. W – The speed of the NormalB texture in the Y axis. |
| _FoamTexture | The noise texture to be added to give some variation to the shoreline foam. |
| _FoamTextureSpeedX | The panning speed of the foam texture in the X axis. |
| _FoamTextureSpeedY | The panning speed of the foam texture in the Y axis. |
| _FoamLinesSpeed | The speed at which the lines of the foam move inwards. |
| _FoamIntensity | The intensity of the foam effects; mostly to be used with a bloom post-processing effect. |
| _RenderTexture | The render texture containing information about the water ripples. |
| _Glossiness | The smoothness of the water surface. |
| _FresnelPower | The power of the fresnel mask used to adjust the water’s transparency based on view direction. |

### The in-between stuff

First off, as you can imagine, this shader is for transparent objects, so lines 35-37 include the classic directives etc to declare that. This, however, is a surface shader so there’s an extra step we need to make transparency working.

In line 41 you’ll notice the “alpha:premul” at the end. You might have seen other transparent surface shaders that instead use “alpha:fade”. This is the different transparency mode that’s also offered in Unity’s standard shader.

![](../../assets/c12a6ca925a92706.png)

In the standard shader, the difference between “Fade” and “Transparent” is that when the material is set to “Fade”, elements like specular reflections or colors from reflection probes get faded out with alpha. On the contrary, “Trasparent” mode allows these elements to stay in even if your albedo color is completely clear.

That’s the difference between “alpha:fade” and “alpha:premul”. You’d expect the second mode to be called “alpha:transparent” but it’s “alpha:premul” instead.

![](../../assets/dd9a146c102b2b92.png)

![](../../assets/c7ae01b24ca565d7.png)

In the input struct we don’t need a whole lot of stuff, just the screen-space position for the depth difference, the world-space position for some planar texture mapping and the view direction for a fresnel effect to adjust the transparency. I’m not using any UV coordinates as I’ve chosen to map all textures using world-space position instead to help with tiling etc.

Lines 53-77 is just about redeclaring all the properties above, and in lines 79-81 I also declare some fields that aren’t featured in the properties block:

- _CameraDepthTexture: The depth texture of the camera, used to get the the depth difference for the intersection effects.
- _CamPosition: The position of the orthographic camera that’s used for the water ripples. This is passed to the shader through a script.
- _OrthographicCamSize: The orthographic size of the aforementioned camera. Again, the value for this field is set by a script.

### The surf method 🏄♀️

First off, in lines 93-96 I get the color of the render texture upon which the orthographic camera for the water ripples writes. The first three lines are just about getting proper UVs to sample the render texture. You can imagine this process as projecting what the orthograpic camera sees onto the plain, in the exact size and position of the camera’s frustum.

For that reason, we need to get a vector from the camera’s position to the pixel’s position in world-space. We only care about the X and Z axes so we don’t take Y into account. The vector is then divided by the width of the camera’s frustum (which equals to two times its orthographic size) so we eventually get values going from 0 to 1 to properly sample the render texture. The UVs then get increased by 0.5 so they can be properly centered.

Lines 98 and 99 are about getting the camera’s linear eye space depth, so I can use it for the different intersections.

In lines 101-103 I get the depth differences for the fog color, the intersection color and the shore foam respectively. I use the same process of subtracting the world-space view depth (the w component of the screen position field) from the camera’s depth value and then dividing the whole thing by a different threshold for different effects.

In line 104 I also multiply the field for the shore foam depth difference by the inverse of the render texture’s blue channel in order to add some more foam based where the water ripples spawn, for visual flare.

In line 106 I interpolate between the normal color, the intersection color and the fog color based on the respective depth difference values to get the final albedo color.

Lines 108 and 109 are where I calculate the foam for the shore and the ripples. First I sample the noise texture I use for some variation on the foam. I use the x and z components of the world space position and multiply them by the “_FoamTexture_ST.xy” which is the scaling of the texture that can be adjusted via the material inspector. I also offset the foam noise texture over time based on “_FoamTextureSpeedX” and “_FoamTextureSpeedY”.

Line 109 is a bit interesting; normally I’d be doing something like “step(foamTex, foamDiff)” which would give a result like this:

![](../../assets/2db4c22235efa075.png)

Which is nice and cool and all that, but I wanted to actually have some lines going inwards that get distorted with the noise texture and have a more stylized look overall, which is why I harnessed the power of the sine wave.

Let’s break down what’s going on here:

“foamDiff” is a value going from 0 to 1, where 0 is where the water touches the shore and then it interpolates to 1 as we get away from the shore. Adjusting the “_FoamThreshold” increases or decreases the area that “foamDiff” interpolates from 0 to 1. If we use a sine method with “foamDiff” as input we can get a result like that:

![](../../assets/6e6014972ef37b93.png)

This is done with this bit of code:

foam = saturate(sin((foamDiff - _Time.y * _FoamLinesSpeed) * 8 * UNITY_PI));

Basically, I’m offsetting “foamDiff” over time, multiplying it by 8π (or 4τ) , passing it through a sine method (making the lines going inwards), and clamping that from 0 to 1. We get 4 lines cause with a period of 4τ you get 4 times where you get a value of 1 with an input value going from 0 to 1. I’ve hardcoded it to 8 as I saw it worked best, but you can change it or expose it to a property.

Since “foamDiff” is 1 for the rest of the body of water, as the sine wave moves we get this annoying effect:

![](../../assets/affc0dbb58e22edd.png)

To counter that, I subtract the whole sine thing from “foamDiff” after I’ve first multiplied it with 1 – foamDiff to restrict it in the area around the shoreline. This was after a bit of trial and error but it both gets rid of the effect above and also gives some more noise right on the shore, looking like this:

![](../../assets/22fe57f464283203.png)

In line 111 I just calculate a bit of a fresnel mask to be used with transparency. This is just as a small detail to make the water more transparent when you’re looking straight down at it.

In line 113 I assign the rgb value of the color to the albedo color and in lines 114 and 115 I sample the two normal maps with their corresponding panning speeds and unpack them using “_NormalStrength” as the scale, to adjust their strength. Notice that I’m also displacing the UVs using the red and green channel of the render texture color; that’s so that the ripples can displace the normals of the water surface.

Then, in line 116 I add the two values from the normal maps together and I assign the result to the “Normal” field of the “SurfaceOutputStandard” object.

In line 117 I just assign the smoothness value and in line 118 I calculate the transparency of the water. I basically want to take into account the fresnel, the alpha from the different colors and the deeper areas (the “fog”) as these should work a bit independently. Firstly, I didn’t want any transparency on the places where there’s foam, so after I multiply the alpha channel of the color with the fresnel mask, I interpolate between that value and 1 using the foam as a parameter, so the alpha would be 1 where there’s foam. Then, I interpolate between that alpha value and the fog’s color alpha channel based on “fogDiff”, so that I can have no transparency in deeper waters.

Finally, in line 119 I apply the foam to the emission field, after I multiply it by “_FoamIntensity”. Here I assume that the foam will just be white (that can also be emissive and glowing) but you can add a color there if you want.

## Water ripples

The water ripples effect needs some specific setup to work along with a small custom C# script. I’ll include a unity package with a small demo scene in the end of the post so that you can see how everything is set up.

Firstly, you’re going to need an orthographic camera looking towards the surface of the water. This camera should render only what’s on a specific layer, I’m using the “water” layer.

![](../../assets/ae7d6c125c2dd2d7.png)

That camera should write on a square render texture which will be passed on to the stylized water shader.

The orthographic camera should also have this script attached to it:

```
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
[RequireComponent(typeof(Camera))]
public class WaterRippleCamera : MonoBehaviour {
private Camera cam;
public MeshRenderer waterPlane;
private void Awake() {
cam = GetComponent<Camera>();
}
private void Update() {
waterPlane.sharedMaterial.SetVector("_CamPosition", transform.position);
waterPlane.sharedMaterial.SetFloat("_OrthographicCamSize", cam.orthographicSize);
}
}
```

This script just passes the position of the camera and its orthographic size to the material of the water plane.

For the water ripples I’m using a particle system that has a material with this custom shader:

```
Shader "Unlit/WaterRipples"
{
Properties
{
[Normal]_MainTex ("Texture", 2D) = "bump" {}
_MaskRadiusOuter("Mask radius outer", Range(0,.5)) = 0
_MaskRadiusInner("Mask radius inner", Range(0,.5)) = 0
_MaskSoftnessOuter("Mask softness outer", Range(0,1)) = 0
_MaskSoftnessInner("Mask softness inner", Range(0,1)) = 0
}
SubShader
{
Tags { "RenderType"="Transparent" "Queue"="Transparent" "PreviewType"="Plane"}
Blend SrcAlpha OneMinusSrcAlpha
ZWrite Off
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
float2 uv : TEXCOORD0;
float4 color : COLOR;
};
struct v2f
{
float2 uv : TEXCOORD0;
float4 vertex : SV_POSITION;
float4 color : COLOR;
};
sampler2D _MainTex;
float4 _MainTex_ST;
sampler2D _Mask;
float _MaskSoftnessOuter;
float _MaskRadiusOuter;
float _MaskRadiusInner;
float _MaskSoftnessInner;
v2f vert (appdata v)
{
v2f o;
o.vertex = UnityObjectToClipPos(v.vertex);
o.uv = TRANSFORM_TEX(v.uv, _MainTex);
o.color = v.color;
return o;
}
fixed4 frag (v2f i) : SV_Target
{
float circleSDF = distance(i.uv, float2(0.5,0.5));
float outerMask = 1.0 - smoothstep(_MaskRadiusOuter, saturate(_MaskRadiusOuter + _MaskSoftnessOuter), circleSDF);
float innerMask = smoothstep(_MaskRadiusInner, saturate(_MaskRadiusInner + _MaskSoftnessInner), circleSDF);
float mask = outerMask * innerMask;
fixed4 col = fixed4(UnpackNormal(tex2D(_MainTex, i.uv)), mask) * i.color;
return col;
}
ENDCG
}
}
}
```

I’m not going to do a detailed breakdown of this shader; it’s just taking a normal map texture and masks it in a ring fashion so that it only renders the normal ring instead of the whole quad. It also multiplies the final color with the vertex color, so that you can make them ripple particles fade over time.

For the ripples in the demo I use a normal map that looks like this:

![](../../assets/831553298ce77278.png)

Feel free to experiment with other textures as well though.

The particle system should be in the layer that the orthographic camera sees (“Water” in my case). It’s also a good idea to exclude that layer from your main camera, so your particles don’t get rendered as usual.

## The package

You can download a unity package with a demo scene to get a sense of the overall setup in this link:

## Conclusion

This is a very basic implementation of a stylized water effect, as you have probably guessed already. There’s a bunch than can be added on top, like refraction, chromatic aberration, caustics etc. Maybe I’ll cover some of these in a future post, but for now I mostly wanted a basic version that you can adjust as you please.

It’s worth noting that the whole setup with the orthographic camera and the particles can be used for many other effects as well; like vertex displacement on grass for example. It’s quite a versatile setup and I bet you can find some more cool uses for it!

See you in the [next one](https://halisavakis.com/my-take-on-shaders-sky-shader/)!!