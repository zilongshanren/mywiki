---
title: 'My take on shaders: Vertical fog'
url: https://halisavakis.com/my-take-on-shaders-vertical-fog/
published: '2018-06-29'
source_blog: Technically Art – Harry Alisavakis
source_site: https://halisavakis.com
category: graphics
fetched: '2026-04-13'
---

Life’s been busy, so this effect won’t be anything too exciting or technical. However I got excited to make that, cause I’ve been trying for a while to create a convenient vertical fog effect. My first attempt was with unlit shaders, and that was pretty easy and straightforward. My second attempt was with surface shaders and I had trouble overriding all the lighting to give the objects the solid fog color. At the time I did that with 2 additional passes and playing with blend modes and it wasn’t pretty. I mean, the effect was pretty good-looking, but the implementation wasn’t. And after that I thought I’d go full-blown overkill and made the vertical fog as a screen-space effect that translated depth information to world-space coordinates to compare them with a fixed height etc. That worked, but even I knew it was ridiculous.

So, as I was playing around with the [water intersection shader from the last post](http://halisavakis.com/my-take-on-shaders-unlit-waterfall-part-2/), I got an idea: What if instead of fading downwards, the intersection was fading upwards and it had the same color all around? Wouldn’t that give me a fake fog effect? And I tried it, and I liked it, and I thought I’d name it “faug™ ” (get it? cause it’s faux fog). And what I mostly liked about it was that it panders to my lazy needs: it’s an effect that out-of-the-box affects other objects, without me having to create separate shaders or materials. I just apply the material on a big quad that covers all of my objects and doneso! That’s why I decided to share this one, as well as to demonstrate my way of thinking.

On to the faug™ code!

Shader "Custom/VerticalFogIntersection" { Properties { _Color("Main Color", Color) = (1, 1, 1, .5) _IntersectionThresholdMax("Intersection Threshold Max", float) = 1 } SubShader { Tags { "Queue" = "Transparent" "RenderType"="Transparent" } Pass { Blend SrcAlpha OneMinusSrcAlpha ZWrite Off CGPROGRAM #pragma vertex vert #pragma fragment frag #pragma multi_compile_fog #include "UnityCG.cginc" struct appdata { float4 vertex : POSITION; }; struct v2f { float4 scrPos : TEXCOORD0; UNITY_FOG_COORDS(1) float4 vertex : SV_POSITION; }; sampler2D _CameraDepthTexture; float4 _Color; float4 _IntersectionColor; float _IntersectionThresholdMax; v2f vert(appdata v) { v2f o; o.vertex = UnityObjectToClipPos(v.vertex); o.scrPos = ComputeScreenPos(o.vertex); UNITY_TRANSFER_FOG(o,o.vertex); return o; } half4 frag(v2f i) : SV_TARGET { float depth = LinearEyeDepth (tex2Dproj(_CameraDepthTexture, UNITY_PROJ_COORD(i.scrPos))); float diff = saturate(_IntersectionThresholdMax * (depth - i.scrPos.w)); fixed4 col = lerp(fixed4(_Color.rgb, 0.0), _Color, diff * diff * diff * (diff * (6 * diff - 15) + 10)); UNITY_APPLY_FOG(i.fogCoord, col); return col; } ENDCG } } }

A keen observer and devoted reader would notice that compared to the water intersection shader, this one is awfully close. And a keen observer **should **notice that, because the shaders are indeed very very similar. So let’s discuss the differences:

First of all, this shader utilizes only one solid color (though that could easily change) instead of coloring the areas where there is intersection. Therefore, in the properties block I only add the main color of the fog. Also, there is no need for any of the displacement stuff, so all of that’s gone.

Secondly, I removed the UV component from both the “appdata” struct and the “v2f” struct. It’s obviously not necessary, but since I’m not mapping anything to the fog quad and I just return a solid color, I thought I’d remove them. However, a cool idea I just thought while writing this would be to keep the UV coordinates to map some kind of noise on the quad, to get a less uniformly distributed fog. Let’s just pretend I’m leaving that as an exercise to the reader.

The vertex shader is pretty much identical to the water intersection one, but if you have any doubts about the screen position stuff, you can check my [shader bits post on that](http://halisavakis.com/shader-bits-world-and-screen-space-position/). Moving on to the fragment shader, in line 51 I get the linear eye depth of the given pixel, exactly as shown before, and in line 52 I calculate the difference between it’s screen space coordinates depth.

Line 54 is where the effect is differentiated from the water shader. There I interpolate the color I return from totally clear (though keeping the RGB values) to the original given color based on “diff”. Here’s something cool though: I could be saying “lerp(fixed4(_Color.rgb, 0.0), _Color, diff)” and still get something similar to the vertical faug™ effect. But interpolating linearly is so passé, nowadays lerping must have an extra “umph” to it. This is why I took a page out of a blog post called “[How to Lerp like a pro](https://chicounity3d.wordpress.com/2014/05/23/how-to-lerp-like-a-pro/)” and instead of just using “diff” I am using “diff * diff * diff * (diff * (6 * diff – 15) + 10)” which gives such a pretty curve, as the aforementiond blog post demonstrates.

Damn, that was short. But I wanted to get that cool effect out there either way. Do keep in mind that this simple implementation can be expanded in a bunch of ways (besides the noise I mentioned above). It’s pretty easy to throw in more colors for both the vertical and the distance fading. Also, I kept the fog stuff in the shader so you can actually [apply Unity’s built-in fog on top of the vertical fog effect](https://i.ytimg.com/vi/IK784WlAPhY/maxresdefault.jpg).

Hope you enjoyed this short post, there are more and more interesting effect breakdowns coming, so stay tuned and I’ll see you in the [next one](http://halisavakis.com/my-take-on-shaders-teleportation-dissolve/)!