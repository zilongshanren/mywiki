---
title: 'My take on shaders: Edge detection image effect'
url: https://halisavakis.com/my-take-on-shaders-edge-detection-image-effect/
published: '2018-02-09'
source_blog: Technically Art – Harry Alisavakis
source_site: https://halisavakis.com
category: graphics
fetched: '2026-04-13'
---

Ever since I got into post-process effects, I was really curious to implement effects that do more complicated stuff than just change the color of the whole screen or play with depth. One such effect was an edge detection image effect, which seemed pretty simple, but the concept of detecting an edge eluded my simplistic way of thinking. Recently, however, I came across this really cool [blog post](http://williamchyr.com/2015/08/edge-detection-shader-deep-dive-part-1-even-or-thinner-edges/) by [William Chyr](http://williamchyr.com), describing his experiments with the edge detection effect for [Manifold Garden](http://manifold.garden). There I noticed his 3-bullet algorithm for the edge detection shader and I thought “Huh, I know how to do that. But can it actually work so simply?”. And apparently it can.

Let’s see some code:

Shader "Hidden/EdgeDetectionShader" { Properties { _MainTex ("Texture", 2D) = "white" {} _Threshold("Threshold", float) = 0.01 _EdgeColor("Edge color", Color) = (0,0,0,1) } SubShader { // No culling or depth Cull Off ZWrite Off ZTest Always Pass { CGPROGRAM #pragma vertex vert #pragma fragment frag #include "UnityCG.cginc" struct appdata { float4 vertex : POSITION; float2 uv : TEXCOORD0; }; struct v2f { float2 uv : TEXCOORD0; float4 vertex : SV_POSITION; }; sampler2D _CameraDepthNormalsTexture; v2f vert (appdata v) { v2f o; o.vertex = UnityObjectToClipPos(v.vertex); o.uv = v.uv; return o; } sampler2D _MainTex; float4 _MainTex_TexelSize; float _Threshold; fixed4 _EdgeColor; float4 GetPixelValue(in float2 uv) { half3 normal; float depth; DecodeDepthNormal(tex2D(_CameraDepthNormalsTexture, uv), depth, normal); return fixed4(normal, depth); } fixed4 frag (v2f i) : SV_Target { fixed4 col = tex2D(_MainTex, i.uv); fixed4 orValue = GetPixelValue(i.uv); float2 offsets[8] = { float2(-1, -1), float2(-1, 0), float2(-1, 1), float2(0, -1), float2(0, 1), float2(1, -1), float2(1, 0), float2(1, 1) }; fixed4 sampledValue = fixed4(0,0,0,0); for(int j = 0; j < 8; j++) { sampledValue += GetPixelValue(i.uv + offsets[j] * _MainTex_TexelSize.xy); } sampledValue /= 8; return lerp(col, _EdgeColor, step(_Threshold, length(orValue - sampledValue))); } ENDCG } } }

So, this shader is an implementation of the second algorithm described in William’s blog:

– sample surrounding pixels

– combine depth and normal values to form a color

– compare the values of the new combined color in surrounding pixels (if values are close, it’s not an edge, else it is)

Firstly, I add a property to use as a threshold to detect whether the values of the surrounding pixels differ significantly from the values of the sampled pixel. I also added a color property in case I wan’t to change the edge outline color.

In line 34 I declare the Camera depth and normal texture, since I need to use it to get, well, the depth and normal values of the scene. More information on that can be found in [this older blog post](http://halisavakis.com/shader-bits-camera-depth-texture/). Instead of having the decoding of the _CameraDepthNormalsTexture in the fragment shader, as shown in the aforementioned post, I create a separate function, since this process will not just be done for the sampling pixel, but also for every pixel surrounding it. Therefore, in lines 49-54 I declare a function, which, given a UV coordinate, returns a color that uses the normals as the RGB values, and the depth as the Alpha value.

Like always, the fragment shader is the true star of the show. In line 58 I get the color as per usual and in line 59 I also get the normal-depth value of the current pixel using the function mentioned above. In lines 60-69 I declare an array of float2 values going from (-1,-1) to (1,1), excluding (0,0). These values will be used to calculate the position of each of the 8 surrounding pixels. Later, in lines 70-74, I get the normal-depth value for each surrounding pixel by offsetting the uv coordinates. This is where I use that array of float2 values which I multiply with the texel size of the main texture (this case the screen). I declared that field in line 45, and it’s instantly accessing the texel size just because of the added “_TexelSize” string. More on accessing those properties can be found in [this link](https://docs.unity3d.com/Manual/SL-PropertiesInPrograms.html). Afterwards, I add each value to a field called “sampledValue” which was initialized to zero and I finally divide the result by 8 to get the mean value.

As the algorithm suggested, if the difference of the normal-depth value of the current pixel and that of the surrounding pixels is bigger than the threshold, the current pixel is an edge, otherwise it is not an edge. The difference of the values is expressed as the length of the vector resulting from the subtraction of the two normal-depth values. If that length is larger than the threshold, the shader should return the edge color, otherwise it should return the original color. That’s how the combination of the lerp and step functions works in line 76.

By the way, in order to apply the effect to the camera you’ll need a script like the one shown in the [introduction to image effects](http://halisavakis.com/my-take-on-shaders-introduction-to-image-effects/) but you’ll also have to change the [camera’s depth texture mode](https://docs.unity3d.com/ScriptReference/Camera-depthTextureMode.html) to DepthTextureMode.DepthNormals.

## Conclusion

The shader is pretty straightforward, as it’s just an implementation of the algorithm in William’s blog. Do keep in mind, however, that the effect on it’s own can be quite aliased, and you would probably need to add some anti-aliasing from Unity’s post-processing stack. In some cases, the first version of the new post-processing stack won’t work correctly with this shader, however the second version of the stack should work pretty well with the effect.

Well, that’s that. See you in the [next one](http://halisavakis.com/my-take-on-shaders-gradient-mapper/)!