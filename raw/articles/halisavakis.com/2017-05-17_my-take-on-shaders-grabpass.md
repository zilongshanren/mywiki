---
title: 'My take on shaders: GrabPass'
url: https://halisavakis.com/my-take-on-shaders-grabpass/
published: '2017-05-17'
source_blog: Technically Art – Harry Alisavakis
source_site: https://halisavakis.com
category: graphics
fetched: '2026-04-13'
---

Moving just a bit away from image effects, this post, as the title betrays, is about GrabPass in shaders. GrabPass is a special pass of a shader that is used to get the contents of the screen in the place where an object would be rendered. So, basically its purpose is to project whatever’s “behind” the object as a texture within the shader. This texture can then be modified and tweaked just like an image effect. Which makes sense, since the end result is like applying an image effect in a portion of the screen, but this portion is bound to an object in world space, instead of a fixed area of the screen space. This kind of effect has a plethora of applications. Imagine seeing through a house window and everything outside looks distorted, you see through another one and everything outside is upside down. These are just from the top of my not so creative head.

The shader I will go through here is really nothing special; it’s basically the default image effect with the color inversion as a shader for a material using GrabPass. A shader with the exact same functionality can be found [here](https://docs.unity3d.com/Manual/SL-GrabPass.html), graciously provided by Unity. But I will also have my version of it here, mostly for the sake of consistency. Any image effects I have shown so far or will show in the future can be applied in the same way to a shader that uses GrabPass, hence I thought it would be proper to have that here too.

So, without further ado, here’s the shader code:

Shader "Custom/GrabPassInvertColors" { SubShader { Tags { "Queue" = "Transparent" } GrabPass { "_GrabTexture" } Pass { CGPROGRAM #pragma vertex vert #pragma fragment frag #include "UnityCG.cginc" struct appdata { float4 vertex : POSITION; float2 uv : TEXCOORD0; }; struct v2f { float4 uv : TEXCOORD0; float4 vertex : SV_POSITION; }; v2f vert (appdata v) { v2f o; o.vertex = UnityObjectToClipPos(v.vertex); o.uv = ComputeGrabScreenPos(o.vertex); return o; } sampler2D _GrabTexture; fixed4 frag (v2f i) : SV_Target { fixed4 col = tex2Dproj(_GrabTexture, i.uv); col = 1 - col; return col; } ENDCG } } }

There are some things going on here that are pretty different from what I’ve shown so far. But don’t fret, we’ll go through the weird/interesting parts together!

The first thing that’s out of the ordinary here is that there is no properties block. That means that there is nothing to be exposed for tweaking from the editor. Which, for our example, makes a lot of sense. There is no texture or color applied to our object. Just the GrabPass texture, which is generated from within the shader. So, we don’t need anything in the properties block, and we can just remove the whole thing.

Next is the tag in line 5, which states that the object will behave as a transparent object as long as the render queue is concerned. While our object won’t be technically transparent per se, it’s necessary to declare it as such in order to make sure that it is rendered after all opaque geometry. Otherwise, elements with a larger render queue number won’t be visible through our object.

The next thing to check is the GrabPass block in line 7. Your intuition might tell you that this block is pretty important to the whole “GrabPass” concept, and it would be correct! Before our main pass of rendering our object with it’s color and geometry, we first make the GrabPass that will get whatever’s “behind”* the object. We don’t need to do anything else about that process, everything else is done automatically. We just specify the name of the texture inside the block to store whatever the GrabPass gets and we’re good to go!

The appdata struct is exactly as we knew it, no differences there. However, in the v2f struct there is one small but real important difference: instead of float2, the UV coordinates are stored in a float4. This is done because the function that calculates the portion of the screen to grab returns a float4. This function is named ComputeGrabScreenPos and it’s called in line 36, assigning the result to the “uv” field of the v2f object.

Similarly to the textures in the properties, it’s necessary to redeclare the grab texture inside the pass of the subshader, as it’s shown in line 40.

Finally, the frag function is almost identical to all the previous shaders shown. However, instead of using the tex2D function I use the tex2Dproj function in line 44. This is done because our UV coordinates are stored in a float4 instead of a float2, because we need the coordinates of our mesh as well as information about the GrabPass. After we get the color in a fixed4, we can manipulate it as per usual.

I hope this wasn’t too hard to follow, especially since it was something different than what has been discussed so far. But I thought it’s something really interesting and some cool effects can be done with this. So go make something cool with this! I’ll wait.

See you in the [next one](http://halisavakis.com/my-take-on-shaders-simple-displacement/)!

*I keep using “” around the word “behind” because, while this is the intuitive way to look at it, it’s not completely accurate. Whatever is being grabbed by the GrabPass is not necessarily behind the object in a sense of distance. All GrabPass does is to replace the area the object would cover in the screen with what the screen would render in that area if the object wasn’t there. I hope that makes sense :S