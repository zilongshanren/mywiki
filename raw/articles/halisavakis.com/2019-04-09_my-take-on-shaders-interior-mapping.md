---
title: 'My take on shaders: Interior mapping'
url: https://halisavakis.com/my-take-on-shaders-interior-mapping/
published: '2019-04-09'
source_blog: Technically Art – Harry Alisavakis
source_site: https://halisavakis.com
category: graphics
fetched: '2026-04-13'
---

As I mentioned in the [previous post](https://halisavakis.com/my-take-on-shaders-parallax-effect-part-ii/), there is a third part to the parallax effect series. However, I decided not to call this post “Parallax Effects (Part III)”, because this effect is widely known with its own name: Interior Mapping.

It’s an effect that’s been utilized for many years, to give the impression of depth mostly in the windows of buildings, without actually having to add any extra geometry. It was discussed a lot recently, thanks to the new Spider-Man game for the PS4, which sparked the interest for some closer examining and case studies, as shown here:

As well as in [Alan Zucconi’s shader showcase](https://www.alanzucconi.com/2018/09/10/shader-showcase-9/).

In the past, I had encountered this technique but couldn’t really grasp how it worked, and any code I found seemed way too complicated for me at the time.

However, I have the habit of revisiting effects I had seen before, and when I checked interior mapping again I had another “I know how that works!” moment. Kind of, at least. Basically, I studied the shader shown in this [unity forum post](https://forum.unity.com/threads/interior-mapping.424676/#post-2751518), inspired by [this demo](http://www.humus.name/index.php?page=3D&ID=80), and I tried dissecting it to the bare minimum. Some areas are still a bit fuzzy for me, but at least the shader is in a state where one can use it with a decent amount of freedom and versatility.

Let’s see the code:

Shader "Custom/InteriorMappingSurface" {
Properties {
_Color ("Color", Color) = (1,1,1,1)
_MainTex("Main texture", 2D) = "white" {}
_Normal("Normal", 2D) = "bump" {}
_InteriorMask("Interior mask", 2D) = "white" {}
_InteriorCubemap("Interior cubemap", Cube) = "white" {}
_Glossiness ("Smoothness", Range(0,1)) = 0.5
_Metallic ("Metallic", Range(0,1)) = 0.0
}
SubShader {
Tags { "RenderType"="Opaque" "DisableBatching"="True"}
LOD 200
CGPROGRAM
// Physically based Standard lighting model, and enable shadows on all light types
#pragma surface surf Standard fullforwardshadows vertex:vert
// Use shader model 3.0 target, to get nicer looking lighting
#pragma target 3.0
samplerCUBE _InteriorCubemap;
sampler2D _InteriorMask;
sampler2D _Normal;
sampler2D _MainTex;
struct Input {
float2 uv_InteriorCubemap;
float2 uv_MainTex;
float3 viewDirTangent;
};
half _Glossiness;
half _Metallic;
fixed4 _Color;
// Add instancing support for this shader. You need to check 'Enable Instancing' on materials that use the shader.
// See https://docs.unity3d.com/Manual/GPUInstancing.html for more information about instancing.
// #pragma instancing_options assumeuniformscaling
UNITY_INSTANCING_BUFFER_START(Props)
// put more per-instance properties here
UNITY_INSTANCING_BUFFER_END(Props)
void vert (inout appdata_full v, out Input o) {
UNITY_INITIALIZE_OUTPUT(Input,o);
float4 objCam = mul(unity_WorldToObject, float4(_WorldSpaceCameraPos, 1.0));
float3 viewDir = v.vertex.xyz - objCam.xyz;
float tangentSign = v.tangent.w * unity_WorldTransformParams.w;
float3 bitangent = cross(v.normal.xyz, v.tangent.xyz) * tangentSign;
o.viewDirTangent = float3(
dot(viewDir, v.tangent.xyz),
dot(viewDir, bitangent),
dot(viewDir, v.normal)
);
}
void surf (Input IN, inout SurfaceOutputStandard o) {
float2 uv = frac(IN.uv_InteriorCubemap);
float3 pos = float3(uv * 2.0 - 1.0, 1.0);
float3 id = 1.0 / IN.viewDirTangent;
float3 k = abs(id) - pos * id;
float kMin = min(min(k.x, k.y), k.z);
pos += kMin * IN.viewDirTangent;
fixed4 col = tex2D(_MainTex, IN.uv_MainTex);
half mask = tex2D(_InteriorMask, IN.uv_MainTex);
o.Albedo = lerp( col.rgb, texCUBE(_InteriorCubemap, pos.xyz).rgb, mask);
o.Normal = UnpackNormal(tex2D(_Normal, IN.uv_MainTex));
o.Metallic = _Metallic;
o.Smoothness = _Glossiness;
o.Alpha = 1.0;
}
ENDCG
}
FallBack "Diffuse"
}



## What

Before I go into the details, let me share a bit about what the shader does, on a higher level:

This is a surface shader (so it supports lights, shadows etc) which has the usual albedo and normal maps for the PBR workflow, as well as sliders for glossiness and metallicness (if that’s even a word). I’ve also added support for a mask texture which defines what part of the material will use interior mapping and which one won’t. Therefore, the material is actually **not** just the interior mapping effect, but it works as a building facade, where you have your usual material for the outside of the building’s wall and a window, for example, through which you watch the interior of the room.

For the interior I use a cubemap, on which you can add the textures of your liking for the walls, ceiling and floor. However, the shader can easily be modified to use separate textures instead of the cubemap.

It’s worth noting that I don’t take randomness into account in this simple version of the effect, therefore all the rooms will be the same. You’re free to try and figure out how to add some variation in both the texture selection and the overall color of each room 😉

## How

Now let’s dig into the code. As extra properties I added a Normal map (I could do without it for the purposes of the tutorial, but what the hell), the mask texture that defines what areas will use interior mapping and what won’t and the cubemap with the interior textures.

In line 12, I make sure to disable batching, just like in the [previous post](https://halisavakis.com/my-take-on-shaders-parallax-effect-part-ii/) and in lines 22-25 I redeclare the extra properties. In the input struct I add extra UV coordinates for the cubemap along with a field for the view direction in tangent space. I could also add UV coordinates for the mask and the normal map, but those can use the UV coordinates of the main texture.

Like before, one of the main things of this shader is calculating the view direction in tangent space. I’ll have to inform you, though, that the vertex function in lines 44 – 55 is **the exact same** as the one in the 2nd parallax post. Right down to the whitespaces. There are 2 main takeaways here: First, you now have a streamlined way of getting the view direction in tangent space. Second, I won’t have to explain what this part does because I’ve already done that in the previous post. Win-win.

The tangent space view direction is needed for the interior mapping effect, but all the actual calculations take place in lines 58-63. First of all, in line 58 I use the frac function on the UV coordinates, so that even if we adjust the scaling of the cubemap UVs, we have sets of coordinates going from 0 to 1, instead of one set of coordinates going from 0 to N (where N is whatever we set the scaling from within the material inspector). Then, in line 59 I map the UVs to the [-1, 1] range. Do note that the new UVs we use are a float3 instead of float2, because we use the z value as well to sample the cubemap.

Then.. the fuzziness starts. As I mentioned, this shader is basically a simplified version of the one in the aforementioned unity forum post, which was modified for Unity from a demo. I tried my best to dissect it and figure out how it works to no avail. So, by all means, if any of you has any idea on how that works, let me know here or on [twitter](https://twitter.com/HarryAlisavakis)!

Moving past the awkward part, in line 65 I sample the main texture as usual and in line 66 I sample the mask texture, which I then use in line 67 to determine the final albedo color. I use lerp to interpolate between then color of the main texture and the color that I get as a result from sampling the cubemap using the modified UV coordinates from line 63.

## Conclusion

You’re probably not much more informed about interior mapping than you were before reading this post. I just thought I should include this effect because it is deeply connected with the concept of the previous posts. Above all, this blog is an archive of different useful effects for both you and me. If I can explain how these effects work, which in most cases I can, that’s a plus. My main goal with this specific post was to provide the simplest version of interior mapping you can get to get started and to reduce the size of the black box of the technique as much as I can. Right now it’s down to the size of 4 lines of code. This shouldn’t stop you from using the shader and even modifying it as you wish, it certainly doesn’t stop me. I think I’ve mentioned it before, but using shaders as black boxes until you get how they work is one of the better ways of learning about them.

I’ll leave you with that and assure you that I’ll be better informed on how the next effect works 😉

See you in the [next one](https://halisavakis.com/my-take-on-shaders-vfx-master-shader-part-i/)!

P.S.: The textures I used for the featured image and gifs are from [textures.com](https://www.textures.com/download/pbr0353/137036). The textures for the interior were taken from the demo of the original effect, with which I made the cubemap I used.