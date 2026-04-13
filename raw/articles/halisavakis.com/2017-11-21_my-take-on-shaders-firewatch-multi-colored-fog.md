---
title: 'My take on shaders: Firewatch multi-colored fog'
url: https://halisavakis.com/my-take-on-shaders-firewatch-multi-colored-fog/
published: '2017-11-21'
source_blog: Technically Art – Harry Alisavakis
source_site: https://halisavakis.com
category: graphics
fetched: '2026-04-13'
---

Recently, I started fiddling around with the depth texture of the camera and came across some interesting discoveries. Of course, those discoveries would probably be pretty obvious to any other shader enthusiast, but for me it was something new and exciting. My favorite element of camera depth texture usage is the fact that you get the depth mapped from 0 to 1. And by now I guess you’ve figured out that as long as you get something going in the [0.0,1.0] spectrum, you can do all kinds of tricks. Whether it is UV coordinates, colors, distance or anything for that matter. For me, however, the effect that I wanted to replicate was obvious: the multi-colored fog from Firewatch. After watching a very intriguing [GDC talk](https://www.youtube.com/watch?v=ZYnS3kKTcGg) about the art of Firewatch, I got a pretty good idea of how the effect works and some guesses as to how I could implement it. And then I did. And although it has some issues, I can say I’m pretty content with the results.

Also, yes, this post could easily go in the “How I’d do it” category alone, but since I’m using it as an excuse to show some stuff about camera depth I thought it would be more fitting to set it as a tutorial post.

## Breakdown

It’s not like I did some mastermind work here, it’s all pretty much explained in the video. They used color ramp textures to map the colors of the fog to the corresponding depth. However, something that intrigued me more was the fact that they also had varying opacity for the fog which was stored on the alpha channel of the texture. Therefore, my simplistic approach was to take the depth texture of the camera, use it as the x UV coordinate of the color ramp, and use lerp to fade from the original color to the ramp texture based on it’s opacity value. After that, I added some controls for the overall contribution of the fog effect.

By the way, in order to apply the effect to the camera you’ll need a script like the one shown in the [introduction to image effects](http://halisavakis.com/my-take-on-shaders-introduction-to-image-effects/) but you’ll also have to change the [camera’s depth texture mode](https://docs.unity3d.com/ScriptReference/Camera-depthTextureMode.html) to DepthTextureMode.Depth.

## The code

Here’s the code:

Shader "Custom/FirewatchFog" { Properties { _MainTex ("Texture", 2D) = "white" {} _FogAmount("Fog amount", float) = 1 _ColorRamp("Color ramp", 2D) = "white" {} _FogIntensity("Fog intensity", float) = 1 } SubShader { // No culling or depth Cull Off ZWrite Off ZTest Always Pass { CGPROGRAM #pragma vertex vert #pragma fragment frag #include "UnityCG.cginc" struct appdata { float4 vertex : POSITION; float2 uv : TEXCOORD0; }; struct v2f { float2 uv : TEXCOORD0; float4 vertex : SV_POSITION; float4 scrPos : TEXCOORD1; }; v2f vert (appdata v) { v2f o; o.vertex = UnityObjectToClipPos(v.vertex); o.uv = v.uv; o.scrPos = ComputeScreenPos(o.vertex); return o; } sampler2D _MainTex; sampler2D _CameraDepthTexture; sampler2D _ColorRamp; float _FogAmount; float _FogIntensity; fixed4 frag (v2f i) : SV_Target { fixed4 orCol = tex2D(_MainTex, i.uv); float depthValue = Linear01Depth (tex2Dproj(_CameraDepthTexture, UNITY_PROJ_COORD(i.scrPos))); float depthValueMul = depthValue * _FogAmount; fixed4 fogCol = tex2D(_ColorRamp, (float2(depthValueMul, 0))); return (depthValue < 1) ? lerp(orCol, fogCol, fogCol.a * _FogIntensity) : orCol; } ENDCG } } }

## In *depth* explanation

### (get it? because I use the camera’s depth in the shader, and I just wrote “in depth explanation”. I love explaining puns.)

So, right off the bat, we have some properties. “_MainTex” is a classic, “_FogAmount” moves the fog closer or further away from the camera, “_ColorRamp” is the ramp texture used to get the multiple colors and opacities in our fog and “_FogIntensity” is a global multiplier for the fog’s opacity. Leave at 1 if you want the opacity to be determined solely by the color ramp. All of those are then redeclared in lines 46-50. However, amongst them lurks a sampler2D which has not been declared in the properties. But whomst could have added that there without declaring it in the properties first??? Well, me, obviously, but this is because it is one of Unity’s built-in variables. Yes, getting the camera depth texture is so simple. More on these kind of built-in variables can be found in [this manual](https://docs.unity3d.com/Manual/SL-CameraDepthTexture.html).

Later on, we see something a bit strange in line 34 and then in line 42. I declare a variable named “scrPos” and then I get the position in screen space and store it in “scrPos”, just as it was shown on [that shader bits post](http://halisavakis.com/shader-bits-world-and-screen-space-position/). Why is that weird though? Because this is an image effect shader, which means there is no “direct” point in getting the vertices position in screen space. We don’t have an actual model besides the “quad” which represents our screen. The reason we need the screen coordinates, though, is to get the linear depth of the camera later on.

Specifically, in probably the weirdest-looking line here, line 55. I won’t go into what’s going on here, for now it’s just sufficient to say that this is how you extract the camera’s depth from it’s depth texture to a value in the [0,1] spectrum. More information on using depth maps can be found in [this manual page](https://docs.unity3d.com/Manual/SL-DepthTextures.html). In line 56 the depth value is multiplied with the “_FogAmount” parameter in order to “make it go from 0 to 1 faster”, to put it in very simplistic terms.

In line 57 I calculate the color of the fog, without taking the opacity in consideration. I just take the color from the ramp texture using “float2(depthValueMul, 0)” as the UV coordinates. Therefore, as the multiplied depth goes from 0 to 1, the “tex2D” function will return the corresponding color of the ramp, considering 0 is the left end, and 1 is the right end of the ramp. Also a great example of how values in the [0,1] spectrum can be manipulated at one’s will.

Finally, in line 58 I check whether the depth value is smaller than 1 or not. This is a hacky solution to prevent the effect from drawing on the skybox, however it has some drawbacks: it can lead to some weird aliasing around the furthest of the geometry, and it can also leave in some other elements if they are far enough. My hacky solution on top of that hacky solution is to add a bit of linear fog that uses the furthest of colors to cover up the aliasing artifacts and the rest of the opaque geometry. Boom, fogged. Nevertheless, in case the depth is smaller than 1, I return a color which interpolates between the original color and the fog color using the ramp’s opacity at that point as the lerping parameter. I also multiply that parameter by “_FogIntensity” in case I want a lighter fog effect.

## Conclusion

Camera depth is awesome. One can do really unique and cool effects just with the depth texture and some gradient colors. You can rest assured that there will be more posts for similar image effects, as well as more experiments and tests posted on [my Twitter account](https://twitter.com/HarryAlisavakis). Until those get uploaded though, see you in the [next one](http://halisavakis.com/my-take-on-shaders-directional-coloring/)!

P.S.: Have some color ramps to play with! But don’t forget to turn on transparency and to set the wrap mode to clamp!!!