---
title: 'My take on shaders: VFX Master Shader (Part II)'
url: https://halisavakis.com/my-take-on-shaders-vfx-master-shader-part-ii/
published: '2019-06-16'
source_blog: Technically Art – Harry Alisavakis
source_site: https://halisavakis.com
category: graphics
fetched: '2026-04-13'
---

## Introduction

Welcome to the second part of the VFX Master Shader tutorial! In this part, we’ll add more features to the “VFX Apprentice Shader”, to actually upgrade it to the status of “Master”. The second part is still focusing on the opaque version of the shader, and while I’ll include the shader code for the whole thing, I’ll only go through the new features.

Therefore, it is quite important to also check [the first part of the tutorial](https://halisavakis.com/my-take-on-shaders-vfx-master-shader-part-i/) in case you have any questions concerning the existing features.

First, let’s go through the elements of the shader. In the first part we covered:

- Using a grayscale noise texture as the main controlling texture
- Applying color via a gradient map (for which you can see more in
[the post on gradient mapping](https://halisavakis.com/my-take-on-shaders-gradient-mapper/)) - Adding contrast and a power factor to modify the levels of the input texture
- Clipping the object’s pixels based on a cutoff value, while also using a property to color the edges around the dissolved areas for a burning effect
- Vertex offset based on the noise texture
- UV displacement for more variation
- Panning of the main texture and the displacement texture based on different values per-axis

Here’s the list of features this post will cover:

- Variable culling mode, in order to change whether the back/front faces are showing or hiding
- Secondary grayscale noise texture with separate panning speeds for a lot of extra effect variety
- Support for vertex colors, where we’ll use the alpha channel to also control the cutoff value for the clipping
- Support for color banding / posterization for more stylized effects
- Support for polar coordinates
- Support for a circular/ring-shaped mask

For the extra stuff I also added more shader features, thus creating several more shader variants (if you don’t remember what those are, check the [first part](https://halisavakis.com/my-take-on-shaders-vfx-master-shader-part-i/)).

With all the new features you’ll be ably to achieve effects like the following:

These are separate use cases on their own, but if you layer different meshes with the materials you can get a much better result, depending on your needs.

Also, with just this shader you’ll be able to recreate the majority of the anime laser beam I recently shared. You can find the break down in [this link](https://80.lv/articles/crafting-a-kamehameha-like-vfx-001agt/).

## Code

Let’s take a look at the code:

Shader "VFX/VFXMasterShader"
{
Properties
{
_MainTex ("Texture", 2D) = "white" {}
_GradientMap("Gradient map", 2D) = "white" {}
//Secondary texture
[Space(20)]
[Toggle(SECONDARY_TEX)]
_HasSecondaryTexture("Has secondary texture", float) = 0
_SecondaryTex("Secondary texture", 2D) = "white" {}
_SecondaryPanningSpeed("Secondary panning speed", Vector) = (0,0,0,0)
[Space(20)]
[HDR]_Color("Color", Color) = (1,1,1,1)
_PanningSpeed("Panning speed (XY main texture - ZW displacement texture)", Vector) = (0,0,0,0)
_Contrast("Contrast", float) = 1
_Power("Power", float) = 1
//Clipping
[Space(20)]
_Cutoff("Cutoff", Range(0, 1)) = 0
[HDR]_BurnCol("Burn color", Color) = (1,1,1,1)
_BurnSize("Burn size", float) = 0
//Vertex offset
[Space(20)]
[Toggle(VERTEX_OFFSET)]
_VertexOffset("Vertex offset", float) = 0
_VertexOffsetAmount("Vertex offset amount", float) = 0
//Displacement
[Space(20)]
_DisplacementAmount("Displacement", float) = 0
_DisplacementGuide("DisplacementGuide", 2D) = "white" {}
//Culling
[Enum(UnityEngine.Rendering.CullMode)]
_Culling ("Cull Mode", Int) = 2
//Banding
[Space(20)]
[Toggle(BANDING)]
_Banding("Color banding", float) = 0
_Bands("Number of bands", float) = 3
//Polar coordinates
[Space(20)]
[Toggle(POLAR)]
_PolarCoords("Polar coordinates", float) = 0
//Mask
[Space(20)]
[Toggle(CIRCLE_MASK)]
_CircleMask("Circle mask", float) = 0
_OuterRadius("Outer radius", Range(0,1)) = 0.5
_InnerRadius("Inner radius", Range(-1,1)) = 0
_Smoothness("Smoothness", Range(0,1)) = 0.2
}
SubShader
{
Tags { "RenderType"="Opaque"}
Offset -1, -1
Cull [_Culling]
LOD 100
Pass
{
CGPROGRAM
#pragma vertex vert
#pragma fragment frag
#pragma shader_feature VERTEX_OFFSET
#pragma shader_feature SECONDARY_TEX
#pragma shader_feature BANDING
#pragma shader_feature POLAR
#pragma shader_feature CIRCLE_MASK
// make fog work
#pragma multi_compile_fog
#include "UnityCG.cginc"
struct appdata
{
float4 vertex : POSITION;
float2 uv : TEXCOORD0;
fixed4 color : COLOR;
float3 normal : NORMAL;
};
struct v2f
{
float2 uv : TEXCOORD0;
UNITY_FOG_COORDS(1)
float2 displUV : TEXCOORD2;
float2 secondaryUV : TEXCOORD3;
float4 vertex : SV_POSITION;
fixed4 color : COLOR;
};
sampler2D _MainTex;
sampler2D _SecondaryTex;
float4 _SecondaryTex_ST;
float4 _MainTex_ST;
sampler2D _GradientMap;
float _Contrast;
float _Power;
fixed4 _Color;
float _Bands;
float4 _PanningSpeed;
float4 _SecondaryPanningSpeed;
float _Cutoff;
fixed4 _BurnCol;
float _BurnSize;
float _VertexOffsetAmount;
sampler2D _DisplacementGuide;
float4 _DisplacementGuide_ST;
float _DisplacementAmount;
float _Smoothness;
float _OuterRadius;
float _InnerRadius;
v2f vert (appdata v)
{
v2f o;
o.uv = TRANSFORM_TEX(v.uv, _MainTex);
o.secondaryUV = TRANSFORM_TEX(v.uv, _SecondaryTex);
#ifdef VERTEX_OFFSET
float vertOffset = tex2Dlod(_MainTex, float4(o.uv + _Time.y * _PanningSpeed.xy, 1, 1)).x;
#ifdef SECONDARY_TEX
float secondTex = tex2Dlod(_SecondaryTex, float4(o.secondaryUV + _Time.y * _SecondaryPanningSpeed.xy, 1, 1)).x;
vertOffset = vertOffset * secondTex * 2;
#endif
vertOffset = ((vertOffset * 2) - 1) * _VertexOffsetAmount;
v.vertex.xyz += vertOffset * v.normal;
#endif
o.vertex = UnityObjectToClipPos(v.vertex);
o.displUV = TRANSFORM_TEX(v.uv, _DisplacementGuide);
o.color = v.color;
UNITY_TRANSFER_FOG(o,o.vertex);
return o;
}
fixed4 frag (v2f i) : SV_Target
{
// sample the texture
float2 uv = i.uv;
float2 displUV = i.displUV;
float2 secondaryUV = i.secondaryUV;
//Polar coords
#ifdef POLAR
float2 mappedUV = (i.uv * 2) - 1;
uv = float2(atan2(mappedUV.y, mappedUV.x) / UNITY_PI / 2.0 + 0.5, length(mappedUV));
mappedUV = (i.displUV * 2) - 1;
displUV = float2(atan2(mappedUV.y, mappedUV.x) / UNITY_PI / 2.0 + 0.5, length(mappedUV));
mappedUV = (i.secondaryUV * 2) - 1;
secondaryUV = float2(atan2(mappedUV.y, mappedUV.x) / UNITY_PI / 2.0 + 0.5, length(mappedUV));
#endif
//UV Panning
uv += _Time.y * _PanningSpeed.xy;
displUV += _Time.y * _PanningSpeed.zw;
secondaryUV += _Time.y * _SecondaryPanningSpeed.xy;
//Displacement
float2 displ = tex2D(_DisplacementGuide, displUV).xy;
displ = ((displ * 2) - 1) * _DisplacementAmount;
float col = pow(saturate(lerp(0.5, tex2D(_MainTex, uv + displ).x, _Contrast)), _Power);
#ifdef SECONDARY_TEX
col = col * pow(saturate(lerp(0.5, tex2D(_SecondaryTex, secondaryUV + displ).x, _Contrast)), _Power) * 2;
#endif
//Masking
#ifdef CIRCLE_MASK
float circle = distance(i.uv, float2(0.5, 0.5));
col *= 1 - smoothstep(_OuterRadius, _OuterRadius + _Smoothness, circle);
col *= smoothstep(_InnerRadius, _InnerRadius + _Smoothness, circle);
#endif
float orCol = col;
//Banding
#ifdef BANDING
col = round(col * _Bands) / _Bands;
#endif
//Clipping
float cutoff = saturate(_Cutoff + (1 - i.color.a));
half test = orCol - cutoff;
clip(test);
//Coloring
fixed4 rampCol = tex2D(_GradientMap, float2(col, 0));
fixed4 finalCol = fixed4(rampCol.rgb * _Color.rgb * rampCol.a, 1) + _BurnCol * step(test, _BurnSize) * smoothstep(0.001, 0.5, cutoff);
// apply fog
UNITY_APPLY_FOG(i.fogCoord, finalCol);
return finalCol;
}
ENDCG
}
}
}



You can already see that the whole thing is getting pretty chaotic, but worry not; we’ll go through all the stuff step by step. Except of the stuff I’ve already covered, that is.

### Properties

#### Secondary Texture

For all the new features there’s a bunch of properties we need to add to the shader, obviously. First and foremost, we have the properties concerning the secondary texture in lines 11-13. In lines 9-10 I add 2 attributes, one to leave a small space before the properties in the material inspector and one to declare that the “_HasSecondaryTexture” property is being used solely as a toggle to enable and disable the “SECONDARY_TEX” keyword. Again, more on that in the previous part.

In line 12 I declare the actual texture and in line 13 I add another vector holding the panning speeds of the secondary texture in the X and Y component (for the horizontal and vertical axis respectively). In this case, I’m not using the Z and W components, I could probably use them in the future for something else.

#### Culling

Moving on to lines 39-40, I declare a property for the cull mode. While in the past I’ve shown shaders using different cull options than the default “Cull Back”, I think I’ve never actually shown this nifty little trick before.

By using the “Enum(UnityEngine.Rendering.CullMode)” attribute, I use a built-in enum Unity has to add a dropdown menu of the available cull modes (Off, Front and Back, in this order). I set the default value of the property to be equal to 2, because it corresponds to “Cull Back”, which is the default behavior we usually might want. If you go to the material inspector, you’ll see that the property is actually rendered like so:

![](../../assets/f4a10302b39f3d38.png)

The way we’ll use it is also quite interesting, but I’ll go through that later on.

#### Color banding

In lines 45-46 I add the properties related to the color banding/ posterization effect. First of all a toggle with a shader feature keyword dictating whether or not the banding will be active, and afterwards a property determining how many bands will the end result have.

#### Polar coordinates

In line 51 I have a single toggle property (with its shader feature keyword on top) that determines whether or not the main, secondary and displacement texture will be sampled using polar coordinates instead of normal, Cartesian coordinates. There’s not really any settings for that, it’s just a toggle.

#### Circular mask

Finally, in lines 56-59, we have all the properties that affect the circular masking. First there’s a toggle, like above, and then, in lines 57-58 there’s properties for the radii of the mask, the outer and the inner one respectively. For their values I use a range slider. At the end, in line 59 I have a property that defines the smoothness of the mask.

You have two questions, I can see it in your eyes. At least you **should** have these two questions:

- Why is the inner radius going from -1 to 1 while the outer one goes from 0 to 1? Hell, why are the radii clamped to values below 1 either way?
- This is an opaque shader, how can you have “smoothness” in your mask? Since the shader is using “clip”, a pixel is either render or it’s not rendered, there’s no transparency whatsoever.

I’m so glad you asked these wonderfully worded questions. I’ll try to provide some equally wonderfully worded answers:

- For this mask I use the UV coordinates of the object, based on the consensus that the object will use the full square of the UV coordinates. It mostly works for planes/quads, because their surface matches perfectly their UV coordinates. Since I calculate the mask based on the UVs, the radius will be related to the UV space, so it’ll go from 0 to 1. As far as the (-1,1) range of the inner radius, this is because of the way I use the “smoothness” property. As you’ll see later on, I’m using a smoothstep function and I add the smoothness to each radius to actually get a smoother mask. Therefore, even if the inner radius is 0, if you have a smoothness value of above 0, you’d get some inner masking too, which you probably don’t want.
- In case you don’t remember from the first part, the clipping happens based on the lower values of the color deriving from the main noise texture, the displacement, the contrast etc. You’ll see later on that I use the mask by multiplying it with that color before clipping, therefore, if there’s any smoothness, it gets blended with the noise instead of cutting a perfectly circular shape.

### The in-between stuff

The first stuff before the vertex/fragment shaders look more or less the same, but there are some new elements to notice. First of all, in line 65, after the cool offset trick, I use the “Cull” directive to define the cull mode. Here, I use the “_Culling” property I declared before, and to get its value I write it as “[_Culling]”. This is how you can use ShaderLab properties inside the subshader. This is a pretty good use case of that feature. The cool kids will probably remember seeing that in a previous [blog post on stencil masking](https://halisavakis.com/my-take-on-shaders-stencil-shader-antichamber-effect/).

In lines 74-77 I add the new shader features to create different shader variants, just as I did in the first part.

In the appdata struct, I also added the “color” field, which is to read the vertex color of the mesh. As I mentioned in the introduction, we’ll use that to adjust the clipping cutoff.

In the v2f struct I added two more fields: another float2 to store the modified UV coordinates of the secondary texture and the color field that will store the vertex colors so that I can read them in the fragment shader.

Lines 101-128 is my redeclaring all the properties as usual. Again, keep in mind that I also have a float4 called “_SecondaryTex_ST” so that I can use the “TRANSFORM_TEX” macro in the vertex shader.

### Vertex shader

First thing I add in the vertex shader is in line 134, where I use the “TRANSFORM_TEX” macro to store the modified UVs corresponding to the secondary texture. I also want the secondary texture (if used) to modify the vertex offset (again, if used). Therefore, in lines 138-141 I check if the “SECONDARY_TEX” keyword is defined (via the “_HasSecondaryTexture” toggle) and, if so, I sample it while also taking into consideration any UV coordinates panning and I multiply its value with the value from the main texture. I also multiply by 2, inspired by [one of the best VFX talks out there](https://www.youtube.com/watch?v=YPy2hytwDLM).

Finally, in line 148 I just pass the vertex color to the “color” property of the v2f struct.

### Fragment shader

Ok, bear with me now, most of the hard part is gone. This is fun stuff now.

Remember in the first part where I stored the different UV coordinates to local variables for basically no good reason? This time I have a good reason, and I mentioned it in the previous part. This is called foreshadowing, or, in this case, foreshadering.

#### Polar coordinates

After I store the secondary UV coordinates into a local variable too, called “secondaryUV”, in lines 162-169 I perform all the necessary calculations to translate the UVs from Cartesian to polar coordinates, **if** the “POLAR” keyword has been defined by the corresponding toggle.

There’s a simple formula to go from Cartesian to polar coordinates, which here I apply thrice, one for the main texture’s, one for the displacement texture’s and one for the secondary texture’s coordinates. The formula is as follows, and I suggest you keep it handy:

float2 mappedUV = uv * 2.0 - 1.0; float2 polarUV = (atan2(mappedUV.y, mappedUV.x) / PI / 2.0 + 0.5, length(mappedUV));

Basically, considering the Cartesian UV coordinates as a 2D vector, after we map them to the (-1, 1) range, the X component of the polar coordinates is the angle of the vector (in relation to the horizontal axis) while the Y component is it’s magnitude.

Try applying that to a texture (like a noise texture) and pan it across the X and Y axis and see what happens! Panning across the X axis makes the texture rotate around, while panning across the Y axis makes the texture go inwards or outwards, creating an instant portal effect!

#### Secondary texture

The panning of the secondary texture is being handled in line 174, along with the other two UV textures.

In line 180 I get the main texture’s grayscale value exactly like in the first part, and, in lines 181-183 I do something similar for the secondary texture (if used). I actually use the exact same formula with the contrast and power and such and I apply the displacement to the UV sampling. The difference her is that I multiply the result with the previous value to apply it, and then by 2 because Diablo VFX talk.

#### Circular mask

Lines 186-190 is where I handle the masking. Basically I don’t do any actual clipping here, I just multiply the color with the mask, and let the clipping later do the job, as it clips based on the lightness of the values.

I take as granted here that the circle mask will start from the center of the UV coordinates, therefore I calculate the circle SDF using the distance of the current UV coordinates from (0.5, 0.5).

There’s something to note here, along with a slight problem: I don’t use the local variable “uv”, as this could’ve been translated to polar coordinates, and I want the masking to be independent from that. The slight problem here is that if I wanted it to be completely independent, I wouldn’t use “i.uv” either, but another field that has the UV coordinates from the vertex information **unmodified**. The way the shader is now, if you adjust the offset/tiling of the main texture, the mask will be modified too, in ways you probably don’t want. I’m leaving it like this for now, because I want to avoid adding more vertex streams to the shader, but if it’s something you’d like to fix, just add another field in the v2f struct (for example “unscaledUV”) which will be equal to “v.uv” in the vertex shader and use that.

In lines 188-189 I multiply the color with the mask after I apply smoothstep on it, like I mentioned in the properties section. I take the inversed result for the outer circle (as I want the circle in the middle to be white, since I’m multiplying) and then multiply that with the inner circle mask which I don’t invert since I want the circle in the middle to be black.

#### Color banding

This is an easy one. In lines 195-197, if the keyword “BANDING” is defined, I simply multiply the value of “col” by the number of color bands I want, round that and then divide it by the number of bands. It’s the same exact trick I used for [the waterfall shader](https://halisavakis.com/my-take-on-shaders-unlit-waterfall-part-1/).

The end result of the color banding is a pretty nice stylized effect, the likes of which you might have seen in games like Risk of Rain 2!

#### Vertex color alpha clipping

Due to the added support for vertex colors, there are some changes in the clipping code from the first part. Instead of using “_Cutoff” for determining the clipping test and the “burning” effect, I create a field called “cutoff” which is equal to the value of “_Cutoff” plus the inverted value of the vertex color’s alpha channel, and all that is clamped from 0 to 1. Therefore, you can either adjust the dissolve amount via the “_Cutoff” property or through the alpha channel of the vertex colors. This is primarily useful if you want to use the shader on a particle system.

## Conclusion

Wow this was a long one! I wouldn’t say the effects are complicated, it’s just that there’s so much stuff here. That’s what makes this shader so useful though.

Keep in mind that there are other approaches (and more correct ones in some cases) and other details you can consider. For example, I calculate the polar coordinates for the secondary texture without checking if the “SECONDARY_TEX” keyword is defined, mostly because I didn’t want the shader to be even more bloated. The main takeaway here is the overall approach of all the different features and their combination.

With all these features the shader is getting fairly big and complicated, so I’m thinking of releasing a post on a custom material editor that will make the user experience a bit better. The next part, however, will be focusing on the transparent version of the shader, which has a few more features. So stay tuned for that!

See you in the [next one](https://halisavakis.com/my-take-on-shaders-vfx-master-shader-part-iii/)!