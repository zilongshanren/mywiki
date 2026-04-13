---
title: 'My take on shaders: Simple Subsurface Scattering'
url: https://halisavakis.com/my-take-on-shaders-simple-subsurface-scattering/
published: '2019-08-15'
source_blog: Technically Art – Harry Alisavakis
source_site: https://halisavakis.com
category: graphics
fetched: '2026-04-13'
---

## Patrons

This tutorial post is brought to you by:

erich binder

Djinnlord

## Introduction

For quite a long time I wanted to do something like SSS for some neat effects, and I had this shader ready for some time too. However, it’s needless to say that I feel weird covering this subject in a tutorial. Mostly because, as with a bunch of my approaches, this one is fairly straightforward and not too physically correct. I’ve shown other effects that are also not physically correct, but this one feels weirder cause it’s a very real effect in nature, so going at it with such a simple approach feels like trying to simulate gravity by moving objects downwards with a constant speed of 9 m/s.

Nevertheless, while one can argue that all objects incorporate some form of SSS, this one effect can be useful in more specific use cases and for certain specific effects. I personally enjoy using it by having lights **inside** some objects, like lamps or paper lanterns.

## Important note

This shader uses a custom lighting model with all the bells and whistles. It’s quite important to have a sense of how all that stuff works. Luckily, I have a post explaining some stuff around custom lighting models in surface shaders. You can give it a read here:

I won’t go through the surface shader details I explain there. So if you have any questions about how all the lighting stuff works, I’d highly suggest going through that post first. If it doesn’t cover your questions, don’t hesitate to reach out!

## Le code

Let’s take a look at the code then:

Shader "Custom/SSSShader" {
Properties {
_Color ("Color", Color) = (1,1,1,1)
_MainTex ("Albedo (RGB)", 2D) = "white" {}
[Normal]_Normal("Normal", 2D) = "bump" {}
_Glossiness ("Smoothness", Range(0,1)) = 0.5
_Metallic ("Metallic", Range(0,1)) = 0.0
_ThicknessMap("Thickness map", 2D) = "black" {}
_Distortion("Normal Distortion", float) = 0
_SSSConcentration("SSS Area Concentration", float) = 0
_SSSScale("SSS Scale", float) = 0
[HDR]_SSSColor("SSS color", Color) = (1,1,1,1)
}
SubShader {
Tags { "RenderType"="Opaque" }
LOD 200
CGPROGRAM
#pragma surface surf SSS fullforwardshadows
#include "UnityPBSLighting.cginc"
// Use shader model 3.0 target, to get nicer looking lighting
#pragma target 3.0
sampler2D _MainTex;
sampler2D _Normal;
struct Input {
float2 uv_MainTex;
float2 uv_Normal;
};
struct SurfaceOutputSSS
{
fixed3 Albedo;
fixed3 Normal;
half3 Emission;
half Metallic;
half Smoothness;
half Occlusion;
fixed Alpha;
float Thickness;
};
half _Glossiness;
half _Metallic;
fixed4 _Color;
sampler2D _ThicknessMap;
float _Distortion;
float _SSSConcentration;
float _SSSScale;
fixed4 _SSSColor;
half4 LightingSSS(SurfaceOutputSSS s, half3 viewDir, UnityGI gi){
float3 lightColor = gi.light.color;
float3 lightDir = gi.light.dir + s.Normal * _Distortion;
half sssAmount = pow(saturate(dot(normalize(viewDir), -normalize(lightDir))), _SSSConcentration) * _SSSScale * (1.0 - s.Thickness);
fixed4 sssColor = sssAmount * _SSSColor * fixed4(lightColor, 1);
SurfaceOutputStandard r;
r.Albedo = s.Albedo;
r.Normal = s.Normal;
r.Emission = s.Emission;
r.Metallic = s.Metallic;
r.Smoothness = s.Smoothness;
r.Occlusion = s.Occlusion;
r.Alpha = s.Alpha;
return LightingStandard(r, viewDir, gi) + sssColor;
}
inline void LightingSSS_GI(SurfaceOutputSSS s, UnityGIInput data, inout UnityGI gi )
{
UNITY_GI(gi, s, data);
}
// Add instancing support for this shader. You need to check 'Enable Instancing' on materials that use the shader.
// See https://docs.unity3d.com/Manual/GPUInstancing.html for more information about instancing.
// #pragma instancing_options assumeuniformscaling
UNITY_INSTANCING_BUFFER_START(Props)
// put more per-instance properties here
UNITY_INSTANCING_BUFFER_END(Props)
void surf (Input IN, inout SurfaceOutputSSS o) {
// Albedo comes from a texture tinted by color
fixed4 c = tex2D (_MainTex, IN.uv_MainTex) * _Color;
o.Thickness = tex2D(_ThicknessMap, IN.uv_MainTex);
o.Albedo = c.rgb;
o.Normal = UnpackNormal(tex2D(_Normal, IN.uv_Normal));
// Metallic and smoothness come from slider variables
o.Metallic = _Metallic;
o.Smoothness = _Glossiness;
o.Alpha = c.a;
}
ENDCG
}
FallBack "Diffuse"
}



### Properties

The shader is basically the default surface shader with standard lighting, only adding the SSS to the final color. Therefore, it has the properties of the standard surface shader, along with some extras:

- “_Normal” for the normal map. Notice the “[Normal]” tag here, used to add the “Fix now” button if the texture is not imported as a normal map.
- ” _ThicknessMap”: A texture that defines the thickness of the object, to add variety to the SSS effect. The darker the texture is, the less thick the object is at that point, therefore the SSS is more visible. The texture is initialized to “black” instead of “white”, so if there’s no thickness map provided, the SSS will be visible uniformly.
- “_Distortion”: This is not the classic distortion/displacement we’re used to. It’s a property that adjusts the distortion of the SSS based on the object’s normals. Without it (or with it set to 0), the additional lighting from SSS will completely ignore the object’s normals.
- “_SSSConcentration”: A property that adjusts how spread out the SSS contribution will be.
- “_SSSScale”: Determines the contribution of the SSS.
- “_SSSColor”: The HDR color that will be multiplied with the light color for the SSS effect.

### The in-between stuff

In line 20 I declare that this is a surface shader using the “SSS” lighting model. As discussed in the [post about surface shaders](https://halisavakis.com/my-take-on-shaders-whats-the-deal-with-surface-shaders/), since the lighting model is something other than the built-in ones (e.g. Standard), we’ll have to define the lighting model. While the lighting model is technically in the “in-between” stuff, I’ll cover it last, since it’s the most “complex” one.

In line 21 I also include a cginc file called “UnityPBSLighting.cginc”. It’s necessary to use some lighting functions later on.

In lines 25-31 I redeclare the “_MainTex”, and “_Normal” properties while also defining the “Input” struct. For each of the two aforementioned samplers I add the corresponding UV coordinates, so that the tiling and offset from the material inspector works separately for the albedo and the normal texture respectively. I could add another one for the thickness map, but since the thickness map will probably be pretty specific to the object and similar to the albedo texture, I’m using the UV coordinates of the _MainTex to sample it later.

For our custom lighting model we’ll need a custom structure that expands on the “SurfaceOutputStandard” struct. That’s why, in lines 33-43 I declare the “SurfaceOutputSSS” struct. It contains all the field of the “SurfaceOutputStandard” struct while also adding a “Thickness” field that we’ll need pass to our lighting function.

In lines 45-53 I redeclare the rest of the properties and afterwards I move on to defining the lighting model, which I’ll explain in a bit.

### The surf function 🏄♂️

No, I’ll never stop with the surfing puns.

The “surf” function is at most indifferent. It’s almost identical to the default one, with some minor additions:

- In line 88 I “calculate” the object’s thickness by sampling the thickness texture. I store the result to the “Thickness” property of the “SurfaceOutputSSS” object “o”, which is passed as an argument to the “surf” method. Do notice that in the arguments “o” is “SurfaceOutputSSS” instead of “SurfaceOutputStandard”.
- In line 90 I sample the normal map for the object’s normals.

That’s it, really.

### The lighting model

In lines 55-70 I define the custom lighting model function called “LightingSSS”. It’s important that it’s named that way, since in the “#pragma surface surf” directive we mentioned that our lighting model will be called “SSS”. If we called it “SubsurfaceScattering”, the function should be called “LightingSubsurfaceScattering”.

Since we use the color of the lights affecting our object, in the arguments of “LightingSSS” I include a field called “UnityGI gi” along with “SurfaceOutputSSS s” and “half3 viewDir”. To access the global illumination struct, we need to declare a custom GI function called “LightingSSS_GI”, even if it does nothing besides its default function. As you have probably guessed, this is what lines 72-75 are for. For now, don’t worry about its arguments and what those structs contain.

Moving into the lighting model function, in line 56 I get the light color to use it with the SSS. I could just use the “_SSSColor” property, but that way the SSS color would only depend on the material and not on the lights, and we wouldn’t be able to have multiple light colors per object.

In line 57 I get the light’s direction/position. If the light is a directional light, this stores the direction, otherwise it stores the position of the light. The result of “gi.light.dir” is then offset along the normals of the object, based on the “_Distortion” property.

The amount of SSS is calculated in line 58. Let’s break it down a bit:

- Firstly I calculate the dot product of the view direction and the inverted “direction” of the light, as we want the light to contribute to SSS if it’s
**behind**the object. That’s what “dot(normalize(viewDir), -normalize(lightDir))” does. - The result is then clamped from 0 to 1 with “saturate”.
- The clamped result is raised to a power of “_SSSConcentration”. The higher the value of the property, the more smaller the “circle” of SSS will be.
- The result is multiplied by “_SSSScale” to adjust its intensity.
- The multiplied result is then multiplied by 1 minus the thickness of the object, as passed in the “SurfaceOutputSSS” struct. This value was not stored in a property of the shader as it differs from pixel to pixel based on the thickness texture. This is the only real reason we needed a custom surface output struct.

After the amount of SSS is calculated, in line 59 I calculate the overall color that I’ll add to the standard lighting. The result comes from multiplying the SSS amount with the “_SSSColor” property and the color of the light.

Lines 61-68 are pretty straightforward. Since we want to calculate the lighting the object would have with the standard lighting model, we need to call the “LightingStandard” function, which takes a “SurfaceOutputStandard” struct as an argument. Therefore, I create an object of that struct in line 61 and copy all the values in it from my “SurfaceOutputSSS” struct.

Finally, in line 69 I call “LightingStandard” to get all the sweet PBR lighting goodness, and add my SSS color to it before returning it.

## Conclusion

That’s it for this one! It might not be the most accurate or flexible SSS implementation out there, but I hope if gives you a good idea about things you can do with custom lighting models.

Also, try making some lamps or paper lanterns with it and I hope you’ll like it as much as I did.

See you in the [next one](https://halisavakis.com/my-take-on-shaders-water-shader/)!