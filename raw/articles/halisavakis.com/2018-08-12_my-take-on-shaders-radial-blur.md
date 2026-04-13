---
title: 'My take on shaders: Radial blur'
url: https://halisavakis.com/my-take-on-shaders-radial-blur/
published: '2018-08-12'
source_blog: Technically Art – Harry Alisavakis
source_site: https://halisavakis.com
category: graphics
fetched: '2026-04-13'
---

It’s been a while since I made a post about an image effect (over 6 months actually, wtf). So here’s an oddly specific one: Radial blur! It’s a simple and straightforward implementation of that effect, but it’s actually amazingly useful and can offer a lot to the look and feel of your game. It can be used to accompany a dash effect or to make a hit feel more impactful. Or simply to make dank memes, I don’t know what you’re into.

The core concept is pretty simple basically: We sample the camera’s texture a bunch of times, and on each one, depending on the screen-space position of the pixel, we adjust the sampling UV coordinates accordingly, basically offsetting them outwards. So, if a pixel is up and to the right of the center, for example, in each iteration it would be offset more towards that direction. I suck at explaining it, but it will probably make more sense in code.

So let’s see it:

Shader "Hidden/RadialBlur" { Properties { _MainTex ("Texture", 2D) = "white" {} _Samples("Samples", Range(4, 32)) = 16 _EffectAmount("Effect amount", float) = 1 _CenterX("Center X", float) = 0.5 _CenterY("Center Y", float) = 0.5 _Radius("Radius", float) = 0.1 } SubShader { // No culling or depth Cull Off ZWrite Off ZTest Always Pass { CGPROGRAM #pragma vertex vert #pragma fragment frag #include "UnityCG.cginc" struct appdata { float4 vertex : POSITION; float2 uv : TEXCOORD0; }; struct v2f { float2 uv : TEXCOORD0; float4 vertex : SV_POSITION; }; v2f vert (appdata v) { v2f o; o.vertex = UnityObjectToClipPos(v.vertex); o.uv = v.uv; return o; } sampler2D _MainTex; float _Samples; float _EffectAmount; float _CenterX; float _CenterY; float _Radius; fixed4 frag (v2f i) : SV_Target { fixed4 col = fixed4(0,0,0,0); float2 dist = i.uv - float2(_CenterX, _CenterY); for(int j = 0; j < _Samples; j++) { float scale = 1 - _EffectAmount * (j / _Samples)* (saturate(length(dist) / _Radius)); col += tex2D(_MainTex, dist * scale + float2(_CenterX, _CenterY)); } col /= _Samples; return col; } ENDCG } } }

Let’s go through the properties first. Besides the obvious “_MainTex” sampler, we have “_Samples” which determines, well, how many times the main texture will be sampled. As you can probably guess, you don’t want that to be too high. Also, just to clarify, I’m aware that there are definitely better solutions out there that do not sample the main texture 32 times per frame and, thus, are way better and more performant. I don’t really care about that. I’m just here to demonstrate the way of thinking and the process of approaching an effect like that.

Moving on, the “_EffectAmount” property determines how intense the effect is going to be. “_CenterX” and “_CenterY” determine the center around which the radial blur will occur, in screen space coordinates. Not hard-coding it to be always at the center is useful in case we want to use the effect to highlight a specific position in the screen or better illustrate a specific movement direction. Finally, “_Radius” determines the radius of the area that is unaffected by the blur. This property gives us more control over what’s blurred and what’s not, in case we don’t want to just have a single pixel to be the center point of the radial blur.

Let’s dig in the juicy stuff now. For once, we don’t have anything to modify in the structs or the vertex shader. Yay for us! Moving onto the fragment shader! Since we’ll be sampling the camera’s main texture a bunch of times, we’ll basically add the result of each sampling to a field and we’ll just divide the result with the number of samples. Therefore, in line 54 I initialize “col” with zeros, so that I can add all the sampling results to it.

For the current pixel I’m examining, I need to find it’s distance from the defined center. So, in line 55 I subtract the center of my blur from the uv coordinates of the current pixel. This will give me a vector the direction of which will indicate which way to offset each sample. In lines 56-59 there’s the main loop which does everything. It repeats as many times as the given samples number and for each one, in line 57 it calculates the amount that each sample needs to be offset. This is calculated like so:

- In each iteration, the sample will be offset by a fraction of the total offset. So, for example, if we had four samples, the first one would be offset by 1/4 of the total amount, the second by 2/4 and so on, and so forth. This is expressed by the “_EffectAmount * (j / _Samples)” expression.
- To take the radius into account, we calculate the distance of the current pixel from the center and divide it by the radius. The smaller the result (the closest the pixel is to the center in relation to the radius), the lesser the offset amount.
- The subtraction from 1 makes sense for line 58.

In line 58 we actually get the sample by using “tex2D” for the “_MainTexture” and as UV coordinates we use the amount calculated in line 57 multiplied by the direction determined by the “dist” vector and everything is added to the center of the radial blur. If the overall blurring amount is 0, the “scale” field will be 1 and the UV coordinates of the sample will be just “dist + float2(_CenterX, _CenterY)” which is just “i.uv”, since “dist = i.uv – float2(_CenterX, _CenterY)”. The sample is then added to “col”, which, in line 60 gets divided by the number of samples to get the average color.

Hopefully all of this made some sense as to how the effect works. It’s rather simple really, that’s why the post is so short too, but I enjoyed making it and wanted to share it anyway. In any case, see you in [the next one](http://halisavakis.com/my-take-on-shaders-spherical-mask-post-processing-effect/)!