---
title: 'My take on shaders : Random stripes mask'
url: https://halisavakis.com/my-take-on-shaders-random-stripes-mask/
published: '2017-08-26'
source_blog: Technically Art – Harry Alisavakis
source_site: https://halisavakis.com
category: graphics
fetched: '2026-04-13'
---

It may seem silly, but when I first started working on image effects, I could not wrap my head around something as simple as stripes on a shader. I started by messing around with the color of the whole image and I couldn’t really think of how to use the coordinates of the screen to achieve a pattern like that. This will seem even more silly when you take a look at how simple the shader is. My inspiration for this post comes from me messing around with the examples from “The Book of Shaders” ( [http://thebookofshaders.com ](http://thebookofshaders.com)) which I suggest you check. Besides, I’m fairly confident that there will be more posts inspired by that great site.

Let’s talk about the shader. The reason behind the simplicity of the code is that it generates a mask, so it just fills the screen with a black and white texture. That texture can then be reused as you wish. An obvious use case for it could be a glitch shader, or some kind of CRT screen simulation. However, despite its level of difficulty, this shader will be a good opportunity to mention some new concepts, such as randomness in shaders.

It’s time to check some code:

Shader "Custom/StripesMaskShader" { Properties { _MainTex ("Texture", 2D) = "white" {} _Frequency ("Frequency", float) = 20 _Fill ("Fill", Range(0, 1)) = 0.8 } SubShader { // No culling or depth Cull Off ZWrite Off ZTest Always Pass { CGPROGRAM #pragma vertex vert #pragma fragment frag #include "UnityCG.cginc" struct appdata { float4 vertex : POSITION; float2 uv : TEXCOORD0; }; struct v2f { float2 uv : TEXCOORD0; float4 vertex : SV_POSITION; }; v2f vert (appdata v) { v2f o; o.vertex = UnityObjectToClipPos(v.vertex); o.uv = v.uv; return o; } sampler2D _MainTex; float _Frequency; float _Fill; float random (float2 input) { return frac(sin(dot(input, float2(12.9898,78.233)))* 43758.5453123); } fixed4 frag (v2f i) : SV_Target { float stripes = 1 - step(_Fill, random( floor(i.uv.y * _Frequency))); return float4(stripes, stripes, stripes, 1); } ENDCG } } }

As you can see, there are only 2 properties besides the _MainTex one. The one is for the frequency, which basically determines the thickness of the lines, while the second one is for the fill, which determines how many lines of the same width will be in the screen. If the fill is set to 1, the mask will be completely white. After I redeclare those fields in lines 43-44, I also declare a function called “random”. This function gets a float2 parameter and returns a pseudo-random number based on that vector. I’d advise you to ignore how it works and just focus on the fact that that it does. If you’re really interested in figuring it out, you can check the explanation given here: [http://thebookofshaders.com/10/](http://thebookofshaders.com/10/). I also encourage you to see for yourself what are the effects of the “random” function by playing around with the function in the fragment shader.

The rest happens in the fragment shader. First, I take the Y coordinate of the UV of the screen and multiply it by the frequency, which will give me a number from 0.0 to whatever “_Frequency” is set to. I pass this number to a “floor” function which will return the number rounded down to the nearest integer value. The result is then passed as a second parameter to a “step” function, which will return 0 if the second value is smaller than “_Fill”, or 1 otherwise. I then reverse the result by subtracting it to 1, to get white stripes on black background.

I mentioned that it would be really simple and quick, and I delivered. I believe, however, that it is a good entry point to other cool effects using randomness and a bit of math. Hopefully, I will come up with more soon.

See you in the [next one](http://halisavakis.com/my-take-on-shaders-custom-wavey-displacement/)!