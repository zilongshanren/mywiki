---
title: 'Shader bits: Camera depth textures'
url: https://halisavakis.com/shader-bits-camera-depth-texture/
published: '2018-01-18'
source_blog: Technically Art – Harry Alisavakis
source_site: https://halisavakis.com
category: graphics
fetched: '2026-04-13'
---

Lately I’ve been working more with depth-based image effects and I often had to search through my archive to find examples of using the camera’s depth texture. Therefore, this Shader Bits post will be a bit different from the other ones. Since the subject is more relevant to image effects, this post won’t have the same format with the different code for vertex-fragment and surface shaders. Instead, I will present some shader code snippets to make use of the camera’s depth and normal textures.

More information on depth textures can be found in this [manual from unity](https://docs.unity3d.com/Manual/SL-DepthTextures.html). You should also take a look at this [manual page](https://docs.unity3d.com/Manual/SL-CameraDepthTexture.html) as well.

Also, keep in mind that in order for some of the stuff here to work you may have to change your camera’s depth texture mode.

## Linear eye depth

Getting the linear eye depth is made easy using Unity’s built-in methods and macros. All you have to do basically is this:

sampler2D _CameraDepthTexture; fixed4 frag (v2f i) : SV_Target { fixed4 col = tex2D(_MainTex, i.uv); float depth = SAMPLE_DEPTH_TEXTURE(_CameraDepthTexture, i.uv); depth = LinearEyeDepth(depth); return col; }

I think it’s pretty straightforward. Obviously lines 6 and 7 could be combined but they’re like that for the sake of clarity.

## Linear 0-1 depth

As mentioned before, having things in the [0,1] spectrum is amazingly useful. In order to get the camera’s depth in a [0,1] spectrum Unity gives us the “Linear01Depth” method, which was shown in the [Firewatch fog post](http://halisavakis.com/my-take-on-shaders-firewatch-multi-colored-fog/). Fun fact: you can use the EXACT same code snippet as the linear eye depth, but instead of “LinearEyeDepth(depth)” in line 7 you use “Linear01Depth(depth)”. It’s that simple. However, as in the Firewatch fog post, you might come across a different implementation of the same method, which I will present here, just so you have it and know that it exists:

sampler2D _CameraDepthTexture; struct v2f { float2 uv : TEXCOORD0; float4 vertex : SV_POSITION; float4 scrPos : TEXCOORD1; }; v2f vert (appdata v) { v2f o; o.vertex = UnityObjectToClipPos(v.vertex); o.uv = v.uv; o.scrPos = ComputeScreenPos(o.vertex); return o; } fixed4 frag (v2f i) : SV_Target { fixed4 col = tex2D(_MainTex, i.uv); float depth = (tex2Dproj(_CameraDepthTexture, UNITY_PROJ_COORD(i.scrPos))); depth = Linear01Depth(depth); return col; }

This has a bit more hassle, as you have to also calculate the screen position, so I’d use the aforementioned way. But that works too.

## Depth and normals

There is also a way to get the camera’s depth along with the normal information for each pixel, which could be useful for SO many effects. Here’s it:

sampler2D _CameraDepthNormalsTexture; fixed4 frag (v2f i) : SV_Target { fixed4 col = tex2D(_MainTex, i.uv); half3 normal; float depth; DecodeDepthNormal(tex2D(_CameraDepthNormalsTexture, i.uv), depth, normal); return col; }

The “DecodeDepthNormal” method when called will change the values of the “depth” and “normal” parameters, similarly to what a method would do to parameters with the “ref” or “out” keyword. Do keep in mind that these normal vectors could need some kind of matrix transformation.


That’s about it! Hopefully you’ll put those bits to good use, cause depth based effects can be hella awesome! See you in the next one!

P.S.: Recently came across Ryan Brucks’ amazing work in his site, [http://shaderbits.com](http://shaderbits.com). Awkwardly enough, I found out about the site after I posted the first two “Shader Bits” posts. Nevertheless, while his work is relative to UE4, it’s still awesome and I’d suggest you give it a look, even just for the inspiration.