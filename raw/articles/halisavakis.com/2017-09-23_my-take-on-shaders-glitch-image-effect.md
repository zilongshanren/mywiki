---
title: 'My take on shaders: Glitch image effect'
url: https://halisavakis.com/my-take-on-shaders-glitch-image-effect/
published: '2017-09-23'
source_blog: Technically Art – Harry Alisavakis
source_site: https://halisavakis.com
category: graphics
fetched: '2026-04-13'
---

I always loved the look of a nice glitch effect in games. For a while now, I’ve been researching different implementations of glitch effects in various media, because I just could not wrap my head around how it’s done. The reason for that, is that in many cases it was implemented differently, and it was usually a combination of different effects. For my effect, I went with a combination of 3 effects: displacement in random stripes, wavy displacement, and, of course, chromatic aberration. This is also why I covered random stripes and wavy displacement in the last 2 posts; it was all part of my master plan to write about the glitch effect without having to go through everything from scratch.

So, let’s talk implementation. For the random stripes displacement I used a set of two random stripes masks, one to displace the image right and one to displace it left. For the wavy displacement I just used the technique mentioned in the previous post. And the chromatic aberration effect is pretty standard, as it’s the same I covered in an older post. The way I wrote the shader follows the way I will present it below: First I just added the effects and played around with them until I could find something pretty glitchy and messed up that I liked. Then, I added a control parameter inside the shader. Since most glitch image effects are not static images and they shift and change their values for some seconds, it’s very useful to have a way to control all the important parameters of your effect via a simple value.

Here’s the shader without the control stuff:

Shader "Custom/GlitchEffectShader" { Properties { _MainTex ("Texture", 2D) = "white" {} _ChromAberrAmountX("Chromatic aberration amount X", float) = 0 _ChromAberrAmountY("Chromatic aberration amount Y", float) = 0 _RightStripesAmount("Right stripes amount", float) = 1 _RightStripesFill("Right stripes fill", range(0, 1)) = 0.7 _LeftStripesAmount("Left stripes amount", float) = 1 _LeftStripesFill("Left stripes fill", range(0, 1)) = 0.7 _DisplacementAmount("Displacement amount", vector) = (0, 0, 0, 0) _WavyDisplFreq("Wavy displacement frequency", float) = 10 } SubShader { // No culling or depth Cull Off ZWrite Off ZTest Always Pass { CGPROGRAM #pragma vertex vert #pragma fragment frag #include "UnityCG.cginc" struct appdata { float4 vertex : POSITION; float2 uv : TEXCOORD0; }; struct v2f { float2 uv : TEXCOORD0; float4 vertex : SV_POSITION; }; v2f vert (appdata v) { v2f o; o.vertex = UnityObjectToClipPos(v.vertex); o.uv = v.uv; return o; } sampler2D _MainTex; float _ChromAberrAmountX; float _ChromAberrAmountY; fixed4 _DisplacementAmount; float _DesaturationAmount; float _RightStripesAmount; float _RightStripesFill; float _LeftStripesAmount; float _LeftStripesFill; float _WavyDisplFreq; float rand(float2 co){ return frac(sin( dot(co ,float2(12.9898,78.233))) * 43758.5453 ); } fixed4 frag (v2f i) : SV_Target { fixed2 _ChromAberrAmount = fixed2(_ChromAberrAmountX, _ChromAberrAmountY); //Stripes section float stripesRight = floor(i.uv.y * _RightStripesAmount); stripesRight = step(_RightStripesFill, rand(float2(stripesRight, stripesRight))); float stripesLeft = floor(i.uv.y * _LeftStripesAmount); stripesLeft = step(_LeftStripesFill, rand(float2(stripesLeft, stripesLeft))); //Stripes section fixed4 wavyDispl = lerp(fixed4(1,0,0,1), fixed4(0,1,0,1), (sin(i.uv.y * _WavyDisplFreq) + 1) / 2); //Displacement section fixed2 displUV = (_DisplacementAmount.xy * stripesRight) - (_DisplacementAmount.xy * stripesLeft); displUV += (_DisplacementAmount.zw * wavyDispl.r) - (_DisplacementAmount.zw * wavyDispl.g); //Displacement section //Chromatic aberration section float chromR = tex2D(_MainTex, i.uv + displUV + _ChromAberrAmount).r; float chromG = tex2D(_MainTex, i.uv + displUV).g; float chromB = tex2D(_MainTex, i.uv + displUV - _ChromAberrAmount).b; //Chromatic aberration section fixed4 finalCol = fixed4(chromR, chromG, chromB, 1); return finalCol; } ENDCG } } }

Since most of the effects have been covered before, this shouldn’t look too weird. However, I don’t have the delusion that every single one that reads this post has read all of my other posts and remember all of them. So here are the links to the previous posts I mentioned:

Now let’s move to the break down:

## Properties

There’s a bunch of them. And that makes sense, I mean, there are parameters for 3 different kind of effects in there! First off, there’s “_ChromAberrAmountX” and “_ChromAberrAmountY” which determine the maximum displacement on the X and Y axis respectively for the different color channels.

Then, there’s “_RightStripesAmount”, “_RightStripesFill”, “_LeftStripesAmount” and “_LeftStripesFill”. As you’ve probable already guessed, those are the parameters for the 2 random stripes masks. The “Amount” is basically the frequency, while the “Fill” is how many stripes will be visible. We have 2 sets of those fields, one for the stripes that will displace the image in one direction, and one for those that will displace the image in the other direction.

After that, there’s “_DisplacementAmount”, which is a vector that keeps 4 values. I use the x and y as the displacement amount for the stripes (in each axis), and the z and w as the displacement amount for the wavy displacement effect (again in each axis).

Finally, (for now) there’s the “_WavyDisplFreq” which, of course, determines the frequency of our wavy mask, as discussed in the previous post.

Again, those properties are all redeclared, and the fun begins!

## Fragment shader

In line 64 I create a fixed2 to store the chromatic aberration amount for the 2 axes, just to make it a bit easier to use. Then, in lines 68-72, I create the stripes to use for the displacement, exactly as shown previously. Note that I’m using the “rand” function again, which I have defined above the fragment shader.

In line 75 I create the red-green mask for the wavy displacement.

In lines 78-79 I use the stripes generated, as well as the wavy mask to create a fixed2 parameter which will hold the final displacement for the image. Specifically, in line 78 I multiply each of the stripes masks with the x and y components of the “_DisplacementAmount” and subtract the left stripes displacement from the right stripes displacement. This is because I wanted the image to displace upwards and to the right wherever there are “right stripes” and downwards and to the left wherever there are “left stripes”. Hopefully that makes sense. In line 79 I do the same with the red and green channel of the “wavyDispl” mask, and I add the result to the final displacement.

Finally, in lines 83-85 I get each color channel of the image, displaced by the final displacement amount. I also add or subtract the “_ChromaticAberrationAmount”, in order to displace the color channels for the chromatic aberration effect. Then I make the color and return it!

## Adding control

While the core of the shader is the one shown above, it is essential to have some form of control over the “glitchiness” of the effect. My suggestion would be to first add the shader above as it is, play with the values, and then add the control. You’ll see why soon. For now, let’s review the updated code:

Shader "Custom/GlitchEffectShader" { Properties { _MainTex ("Texture", 2D) = "white" {} _ChromAberrAmountX("Chromatic aberration amount X", float) = 0 _ChromAberrAmountY("Chromatic aberration amount Y", float) = 0 _RightStripesAmount("Right stripes amount", float) = 1 _RightStripesFill("Right stripes fill", range(0, 1)) = 0.7 _LeftStripesAmount("Left stripes amount", float) = 1 _LeftStripesFill("Left stripes fill", range(0, 1)) = 0.7 _DisplacementAmount("Displacement amount", vector) = (0, 0, 0, 0) _WavyDisplFreq("Wavy displacement frequency", float) = 10 _GlitchEffect("Glitch effect", float) = 0 } SubShader { // No culling or depth Cull Off ZWrite Off ZTest Always Pass { CGPROGRAM #pragma vertex vert #pragma fragment frag #include "UnityCG.cginc" struct appdata { float4 vertex : POSITION; float2 uv : TEXCOORD0; }; struct v2f { float2 uv : TEXCOORD0; float4 vertex : SV_POSITION; }; v2f vert (appdata v) { v2f o; o.vertex = UnityObjectToClipPos(v.vertex); o.uv = v.uv; return o; } sampler2D _MainTex; float _ChromAberrAmountX; float _ChromAberrAmountY; fixed4 _DisplacementAmount; float _DesaturationAmount; float _RightStripesAmount; float _RightStripesFill; float _LeftStripesAmount; float _LeftStripesFill; float _WavyDisplFreq; float _GlitchEffect; float rand(float2 co){ return frac(sin( dot(co ,float2(12.9898,78.233))) * 43758.5453 ); } fixed4 frag (v2f i) : SV_Target { fixed2 _ChromAberrAmount = fixed2(_ChromAberrAmountX, _ChromAberrAmountY); fixed4 displAmount = fixed4(0, 0, 0, 0); fixed2 chromAberrAmount = fixed2(0, 0); float rightStripesFill = 0; float leftStripesFill = 0; //Glitch control if (frac(_GlitchEffect) < 0.8) { rightStripesFill = lerp(0, _RightStripesFill, frac(_GlitchEffect) * 2); leftStripesFill = lerp(0, _LeftStripesFill, frac(_GlitchEffect) * 2); } if (frac(_GlitchEffect) < 0.5) { chromAberrAmount = lerp(fixed2(0, 0), _ChromAberrAmount.xy, frac(_GlitchEffect) * 2); } if (frac(_GlitchEffect) < 0.33) { displAmount = lerp(fixed4(0,0,0,0), _DisplacementAmount, frac(_GlitchEffect) * 3); } //Stripes section float stripesRight = floor(i.uv.y * _RightStripesAmount); stripesRight = step(rightStripesFill, rand(float2(stripesRight, stripesRight))); float stripesLeft = floor(i.uv.y * _LeftStripesAmount); stripesLeft = step(leftStripesFill, rand(float2(stripesLeft, stripesLeft))); //Stripes section fixed4 wavyDispl = lerp(fixed4(1,0,0,1), fixed4(0,1,0,1), (sin(i.uv.y * _WavyDisplFreq) + 1) / 2); //Displacement section fixed2 displUV = (displAmount.xy * stripesRight) - (displAmount.xy * stripesLeft); displUV += (displAmount.zw * wavyDispl.r) - (displAmount.zw * wavyDispl.g); //Displacement section //Chromatic aberration section float chromR = tex2D(_MainTex, i.uv + displUV + chromAberrAmount).r; float chromG = tex2D(_MainTex, i.uv + displUV).g; float chromB = tex2D(_MainTex, i.uv + displUV - chromAberrAmount).b; //Chromatic aberration section fixed4 finalCol = fixed4(chromR, chromG, chromB, 1); return finalCol; } ENDCG } } }

The highlighted lines are the lines that have been added or changed. So let’s see what happened here: I added a new float field named “_GlitchEffect” which will serve as the controlling parameter. The concept behind that parameter is that when it has a value below some different thresholds, different parameters of the effect will be activated and changed. To be more specific, the parameters that will be modified with this controller will be the displacement amount, the chromatic aberration amount, and the fill for both sets of stripes. For that reason, in lines 68-71 I declare some fields that are initialized as zeros. Then, in lines 73-82, I check if the fractional part of the controller is below 3 different thresholds: 0.8, 0.5, 0.33. Those values are completely arbitrary, but I found out they worked for me. If frac(_GlitchEffect) was less than those thresholds, then the corresponding values where lerping from 0 to the value set from the Unity editor.

Finally, I replaced the parameters from the properties with their matching fields, in order to apply the lerping effect to the image effect.

## Conclusion

That’s about it! I personally don’t think it’s a complex shader, considering one has a grasp on the separate effects. For me, the most confusing part could be the controller, but that’s just something I figured out after playing around for a while. The cool thing, though, is that now you can change the controller’s value to a random value, or increment it linearly via a script, and it can produce some interesting effects!

## Bonus

Here’s a similar implementation as a material for Unreal Engine 4:


That’s it for now, see you in the [next one](http://halisavakis.com/my-take-on-shaders-firewatch-multi-colored-fog/)!