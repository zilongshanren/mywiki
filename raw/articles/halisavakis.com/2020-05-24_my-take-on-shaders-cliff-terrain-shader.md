---
title: 'My take on shaders: Cliff terrain shader'
url: https://halisavakis.com/my-take-on-shaders-cliff-terrain-shader/
published: '2020-05-24'
source_blog: Technically Art – Harry Alisavakis
source_site: https://halisavakis.com
category: graphics
fetched: '2026-04-13'
---

## Patrons

This tutorial is brought to you by these awesome patrons:

- orels1
- Tiph’ (DN)

## Introduction

Something that wasn’t very obvious to me for a while was how to take advantage of the splat-maps in Unity’s terrain system. As I played more with my grass shader I thought about leveraging it to specify areas that I wanted to have grass, instead of just applying it in the whole terrain, so I decided to look into how to sample splat-maps and the texture information that’s being passed into Unity’s default terrain shader.

Along with that and inspired by [adamgryu](https://twitter.com/adamgryu)‘s terrain work in “A short hike”, I also decided to add some biplanar texturing to automatically apply a cliff texture (along with all its PBR properties) on steep areas of the terrain.

I thought that both splat-map using and biplanar terrain mapping can be an interesting item for a tutorial, as you can use them as a base for a lot more cool stuff! Since this shader is a surface shader too, you could easily expand it by making custom lighting models for example!

Most of the stuff shown here are fairly straightforward but there are some interesting points to note. The overall process is fairly simple though, so I’ll just jump into the code!

## The code

```
Shader "Custom/CliffTerrainShader"
{
Properties
{
_CliffTexture("Cliff texture", 2D) = "white" {}
[Normal]_CliffNormal("Cliff normal", 2D) = "bump" {}
_CliffNormalStrength("Cliff normal strength", float) = 1
_CliffSmoothness("Cliff smoothness", Range(0,1)) = 0
_CliffMetallic("Cliff metallic", Range(0,1)) = 0
}
SubShader
{
Tags { "RenderType"="Opaque" }
LOD 200
CGPROGRAM
// Physically based Standard lighting model, and enable shadows on all light types
#pragma surface surf Standard fullforwardshadows
// Use shader model 3.0 target, to get nicer looking lighting
#pragma target 3.0
sampler2D _CliffTexture;
float4 _CliffTexture_ST;
sampler2D _CliffNormal;
float _CliffNormalStrength;
float _CliffMetallic;
float _CliffSmoothness;
sampler2D _Control;
// Textures
sampler2D _Splat0, _Splat1, _Splat2, _Splat3;
float4 _Splat0_ST, _Splat1_ST, _Splat2_ST, _Splat3_ST;
//Normal Textures
sampler2D _Normal0, _Normal1, _Normal2, _Normal3;
//Normal scales
float _NormalScale0, _NormalScale1, _NormalScale2, _NormalScale3;
//Smoothness
float _Smoothness0, _Smoothness1, _Smoothness2, _Smoothness3;
//Metallic
float _Metallic0, _Metallic1, _Metallic2, _Metallic3;
struct Input
{
float2 uv_Control;
float3 worldPos;
float3 worldNormal;
INTERNAL_DATA
};
// Add instancing support for this shader. You need to check 'Enable Instancing' on materials that use the shader.
// See https://docs.unity3d.com/Manual/GPUInstancing.html for more information about instancing.
// #pragma instancing_options assumeuniformscaling
UNITY_INSTANCING_BUFFER_START(Props)
// put more per-instance properties here
UNITY_INSTANCING_BUFFER_END(Props)
void surf (Input IN, inout SurfaceOutputStandard o)
{
fixed4 splatControl = tex2D(_Control, IN.uv_Control);
fixed4 col = splatControl.r * tex2D (_Splat0, IN.uv_Control * _Splat0_ST.xy);
col += splatControl.g * tex2D(_Splat1, IN.uv_Control * _Splat1_ST.xy);
col += splatControl.b * tex2D (_Splat2, IN.uv_Control * _Splat2_ST.xy);
col += splatControl.a * tex2D (_Splat3, IN.uv_Control * _Splat3_ST.xy);
o.Normal = splatControl.r * UnpackNormalWithScale(tex2D(_Normal0, IN.uv_Control * _Splat0_ST.xy), _NormalScale0);
o.Normal += splatControl.g * UnpackNormalWithScale(tex2D(_Normal1, IN.uv_Control * _Splat1_ST.xy), _NormalScale1);
o.Normal += splatControl.b * UnpackNormalWithScale(tex2D(_Normal2, IN.uv_Control * _Splat2_ST.xy), _NormalScale2);
o.Normal += splatControl.a * UnpackNormalWithScale(tex2D(_Normal3, IN.uv_Control * _Splat3_ST.xy), _NormalScale3);
o.Smoothness = splatControl.r * _Smoothness0;
o.Smoothness += splatControl.g * _Smoothness1;
o.Smoothness += splatControl.b * _Smoothness2;
o.Smoothness += splatControl.a * _Smoothness3;
o.Metallic = splatControl.r * _Metallic0;
o.Metallic += splatControl.g * _Metallic1;
o.Metallic += splatControl.b * _Metallic2;
o.Metallic += splatControl.a * _Metallic3;
float3 vec = abs(WorldNormalVector (IN, o.Normal));
float threshold = smoothstep(0.5, 0.9, abs(dot(vec, float3(0, 1, 0))));
fixed4 cliffColorXY = tex2D(_CliffTexture, IN.worldPos.xy * _CliffTexture_ST.xy);
fixed4 cliffColorYZ = tex2D(_CliffTexture, IN.worldPos.yz * _CliffTexture_ST.xy);
fixed4 cliffColor = vec.x * cliffColorYZ + vec.z * cliffColorXY;
float3 cliffNormalXY = UnpackNormalWithScale(tex2D(_CliffNormal, IN.worldPos.xy * _CliffTexture_ST.xy), _CliffNormalStrength);
float3 cliffNormalYZ = UnpackNormalWithScale(tex2D(_CliffNormal, IN.worldPos.yz * _CliffTexture_ST.xy), _CliffNormalStrength);
float3 cliffNormal = vec.x * cliffNormalYZ + vec.z * cliffNormalXY;
col = lerp(cliffColor, col, threshold);
o.Normal = lerp(cliffNormal, o.Normal, threshold);
o.Smoothness = lerp(_CliffSmoothness, o.Smoothness, threshold);
o.Metallic = lerp(_CliffMetallic, o.Metallic, threshold);
o.Albedo = col.rgb;
o.Alpha = col.a;
}
ENDCG
}
FallBack "Diffuse"
}
```

### Properties

The exposed properties here only the ones concerning the cliffs and this is because all the other properties are being passed in the shader via the terrain system and the terrain layer objects. So there’s no need to clutter our properties block, I’ll just go through these 5 properties quickly:

- _CliffTexture: The albedo texture for the cliffs.
- _CliffNormal: The normals texture for the cliffs. Once again, notice the “[Normal]” tag on the left and the “bump” default value on the right.
- _CliffNormalStrength: How strong the normals of the cliffs will be. I’m not sure if I’ve shown how to adjust normals strength before, but this is a good opportunity to do so.
- _CliffSmoothness: Determines how glossy the cliffs will be.
- _CliffMetallic: Determines how metallic the cliffs will be. Which usually isn’t a lot, but I through that in there for the sake of PBR.

You could obviously add more properties here, like roughness/metallic maps etc. It’s like assembling properties for a normal PBR material at this point.

### The in-between stuff

Moving on into the shader we have all the properties we declared in the “Properties” block, but there’s also a bunch more that we didn’t add above; the ones passed to the shader from the terrain itself. Let’s check that out:

Lines 23-28 are all the stuff we added in the “Properties” block, along with the “_ST” field for the cliff albedo texture, in order to scale and offset the textures. I didn’t add one for the normal texture, based on the convention that the normal texture will have the same tiling as the albedo.

Line 30 is where the most important field of all is declared: the simply named “_Control” texture. This is in fact the texture that gets drawn upon when you paint in the “Paint Texture” tab of your terrain. It gets filled with colors corresponding to different color channels (red for the first terrain layer, green for the second, blue for the third, alpha for the forth) and it’s used to mask out the different terrain layers that get painted on the terrain.

The actual properties of each terrain layer are declared in lines 33-46. This shader supports up to 4 of these layers, so each set of properties has a number at the end, going from 0 to 3.

In lines 33 & 34 there’s the albedo texture of each terrain layer and the corresponding tiling/offset value.

In lines 37 and 40 you have the normal texture of each terrain layer and the corresponding normal strength.

Then, in lines 43 and 46 you have the smoothness and metallic values for each terrain layer respectively.

Note that these names (“_Control”, “_Splat0” etc) are **not** arbitrary; they are named like that to communicate with the terrain system, so changing them to your liking won’t work.

You can also see the properties of a terrain layer via the inspector to get a better sense of what you can access:

![](https://i0.wp.com/halisavakis.com/wp-content/uploads/2020/05/image.png?resize=438%2C396&ssl=1)

We didn’t add the specular color here, but the properties for each terrain layer would be called “_SpecularX” where X is a number going from 0 to 3 in this shader. I personally used the specular color to multiply it with the albedo and get more control out of the colors of each layer, but you could use it any way you want really.

Finally, there’s the “Input” struct in lines 49-55. You’ll notice that we have UVs for the “Control” texture but not for the cliff texture. That’s because the texturing will be in world space to avoid stretching in steep surfaces. This is also why I’ve included “worldPos” in the struct; to get the world position of the pixels and sample the cliff texture biplanarly.

You’ll also notice the “worldNormal” field in line 53 as well as a weird macro in line 54 – “INTERNAL_DATA”. This is necessary to get the world-space normal vector of the mesh while also being able to apply a normal texture to the SurfaceOutputStandard object. It isn’t very clear, but you apparently need those if you want to do both.

### The surf method 🏄♀️

This is a lengthy one, but you’ll see there’s a lot of repetition because of the multiple PBR properties per terrain layer. So let’s break this down:

In line 67 I simply sample the “_Control” texture which will give me the masks for each of the layer.

Lines 68-71 is where I sample the albedo textures of the terrain layers. Firstly I sample the “_Splat0” albedo texture and I multiply it by the red channel of the control texture to mask it out. Notice that I use the “uv_Control” coordinates, multiplied by the “_Splat0_ST” field. I could have added a “uv_Splat0” field in the “Input” structure, but I’d also have “uv_Splat1”, “uv_Splat2” and “uv_Splat3” and it’s not too elegant to clutter the “Input” struct.

After I sample the first albedo texture, I do the same for the other 3 using the corresponding channels of the control texture as masks.

In lines 73-76 I perform the same process with the normal textures. However, since these are normal maps, the result of the sampling needs to be encapsulated in a “UnpackNormal” method. Since we also have the normal strength of each terrain layer here, I’m using the “UnpackNormalWithScale” method, which takes the normal strength as an extra parameter and automatically applies it.

Lines 78-81 repeat the process in a simpler manner; using the smoothness values of each layer and lines 83-86 do the same with the metallic values.

After that, it’s time for the biplanar mapping calculations. First off, in line 88 I get the absolute value of the world-space normal vector using the “WorldNormalVector” method. Based on that, I get a threshold value to determine the steep areas of the terrain in line 89, using a smoothstep to adjust the dot product of the normal vector and the world up vector (0,1,0). I found that the values 0.5 – 0.9 work well for some nice blending, but you can play around with them to achieve different effects.

In lines 90-91 I sample the cliff albedo texture twice, once for the XY plane and once for the YZ plane, by using the xy and yz components of the world position respectively. I also multiply the world position by “_CliffTexture_ST.xy” to adjust the scale of the textures from the inspector.

The final color is determined in line 92 by multiplying the color of the YZ plane with the X component of the world-space normal vector and adding that to the color of the XY plane multiplied by the Z component of the normal vector. If the texturing were triplanar instead of biplanar, I’d do the same for the XZ plane with the Y component of the normal vector, but I’m using the terrain layers for that.

In lines 94-96 I’m doing the exact same process for the normal textures, again using “UnpackNormalWithScale” to both unpack the normal value and apply the normal strength.

Finally, it’s time to mix the values from the terrain layers and the biplanar mapping, which is handled by a bunch of “lerp” calls in lines 98-101. In each line I just mix each of the cliff values and the corresponding terrain layer values based on the threshold value calculated in line 89. This process is done for the albedo color, the normals, the smoothness and the metallic values.

After that, I pass the final color and the alpha value to the SurfaceOutputStandard object and I’m done!

## Conclusion

I initially forgot to write the conclusion section, damn 😐

In any case, this is a very simple shader that doesn’t do anything too novel, but it just showcases how you can access the terrain splat maps and possibly get some custom effects out of that! I also hope this tutorial kinda demystifies how Unity works behind the scenes and shows you that you can dive a little deeper in and make stuff that work hand in hand with the editor.

See you in the [next one](https://halisavakis.com/my-take-on-shaders-stylized-water-shader/)!