---
title: 'My take on shaders: Night time shader (Introduction to image effects part
  II)'
url: https://halisavakis.com/my-take-on-shaders-night-time-shader-introduction-to-image-effects-part-ii/
published: '2017-04-19'
source_blog: Technically Art – Harry Alisavakis
source_site: https://halisavakis.com
category: graphics
fetched: '2026-04-13'
---

You might (but probably not) have seen my newest game named “Sling Toss” for which you can find information on my projects page. Besides shamelessly promoting my game, I am mentioning it for a simple image effect it features. It’s really nothing special in a technical aspect. But it is something different from the default image effect. So, I thought it could be useful for all of the beginners out there.

So, this image effect is responsible for the change you see below:

I wanted to change the environment a bit so that it wasn’t boring, and I also didn’t want to make new assets. Because I’m lazy. Therefore, I made this simple image effect to somewhat modify the feel of the environment and accompanied it with some tricks, like toggling the sun, moon and stars.

This shader is made to work on Unity 5.6, thought I should mention it because apparently there are some changes. So, let’s jump straight to the code!

Shader "Custom/NightTime" { Properties { _MainTex ("Texture", 2D) = "white" {} _NightTime("Night time", Range(0.001, 1)) = 1 } SubShader { // No culling or depth Cull Off ZWrite Off ZTest Always Pass { CGPROGRAM #pragma vertex vert #pragma fragment frag #include "UnityCG.cginc" struct appdata { float4 vertex : POSITION; float2 uv : TEXCOORD0; }; struct v2f { float2 uv : TEXCOORD0; float4 vertex : SV_POSITION; }; v2f vert (appdata v) { v2f o; o.vertex = UnityObjectToClipPos(v.vertex); o.uv = v.uv; return o; } sampler2D _MainTex; float _NightTime; fixed4 frag (v2f i) : SV_Target { fixed4 col = tex2D(_MainTex, i.uv); fixed lum = Luminance(col.rgb); fixed4 output; output.rgb = lerp(col.rgb, fixed3(lum,lum,lum), _NightTime); output.a = col.a; return (output + _NightTime * fixed4(0, 0, 0.8, 1)) * (1 - _NightTime); } ENDCG } } }

As you can see, the setup is pretty similar to the one we saw in the first part. The obvious changes are 2: one more property in the “Properties” block, and also some black magic in the fragment shader.

More specifically: In the “Properties” block I added another property (duh) named “_NightTime” that’s a float that takes values from 0.001 to 1 and it’s being initialized with 1. As mentioned in the first part, I have to re-declare it inside the shader, hence the declaration in line 42.

Alright, that’s out of the way so let’s move to the fun part: what’s happening in the fragment shader. The whole concept of the shader was to manipulate the colors in such a way so that it looked “night-ish”. To do that, I had to do three things: add some blue to the overall color, decrease the saturation a bit and make the scene a bit darker. Just one of those options doesn’t work, in order to look somewhat good, it had to be all three of them. And this is what the shader does!

As always, first it gets the default, unprocessed color from the camera, stores it in a field named “col”. After that, we get grayscale version of the fragment, and store it in a field named “lum”. The Luminance function is given by Unity and it returns the grayscale values of a color.

The fun part is at line 49. After making another field named “output”, for its red, green and blue values we give it the result of a lerp function. In case you’re unfamiliar with it, lerp stands for linear interpolation and it’s usually in the form of “lerp(a, b, t)”. If the t is 0, it will return a. If it’s 1 it will return b. If it’s anything in between, it will return (1 – t)* a + t * b. So, in this case, if the “_NightTime” value is 0, the output color will be the regular, unprocessed color of the scene. If, however, it’s 1, the output color will be one that has “lum” as it’s value for red, green and blue. That means that the output color will be in grayscale. So, the lerping function basically is modifying the saturation of the scene based on “_NightTime”.

Finally, in line 51 we also have a bunch of stuff going on. Basically, we take the “output” and we add some blue to it. The amount of blue is too managed by “_NightTime”. Then, we take the result and multiply it by “1 – _NightTime”. This multiplication is responsible for making the overall color darker.

By using the script of the [first part](http://halisavakis.com/my-take-on-shaders-introduction-to-image-effects/) you can attach the image effect to your camera. And, in case you were wondering, the orange player thingy is unaffected by the image effect because I’m using separate cameras and different layers.

See you in the [next one](http://halisavakis.com/my-take-on-shaders-simple-masks-introduction-to-image-effects-part-iii/)!