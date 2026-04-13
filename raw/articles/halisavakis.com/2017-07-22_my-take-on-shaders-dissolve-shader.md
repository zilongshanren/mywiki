---
title: 'My take on shaders: Dissolve shader'
url: https://halisavakis.com/my-take-on-shaders-dissolve-shader/
published: '2017-07-22'
source_blog: Technically Art – Harry Alisavakis
source_site: https://halisavakis.com
category: graphics
fetched: '2026-04-13'
---

Before I got into shaders, I used to think that I had a good amount of insight for the techniques used in video games, and that I could think of how somebody would approach an effect or a mechanic. However, for a long time I just could not put my finger on how somebody would make an effect like the one I had seen in many games, where an item or character would dissolve in little pieces and disappear. Since I had no understanding of the shader side of things, it just eluded my logic. Not long after that time, I got into the dark arts of shader programming and realized that this effect is part of a shader, that is of course combined with other effects and particle systems. Here we are now, and the subject of this post is the creation of a dissolve shader.

This shader is not for a post processing effect, however it can be used as such to make some cool transitions, like the ones in Pokemon when the player entered a battle. The resulting effect is mostly for items and characters, but it’s pretty versatile and I believe one can find some really cool uses for it.

Before I share the code I also want to go through some of the weirder stuff. First of all, this shader is not a vertex/fragment shader but a surface shader, like the ones shown in the [stencil shader post](http://halisavakis.com/my-take-on-shaders-stencil-shader-antichamber-effect/). That means that we don’t have complete control over the object since the shader takes care of most of the important stuff (like lighting etc). But we can manipulate the final color of the object, which is what we need. Also, it’s important to note that this shader is composed of 2 parts: the part that handles the actual dissolving and the part that is responsible to display some cool emission around the holes created by the dissolving. That emission can either be a single color (controlled by a property) or it can derive from a color ramp. By using a color ramp we can achieve more awesome effects, like giving the impression of burning, as seen in this example:

Enough stallin’, here’s the code:

Shader "Custom/Dissolve" { Properties { _Color ("Color", Color) = (1,1,1,1) _MainTex ("Albedo (RGB)", 2D) = "white" {} _SliceGuide("Slice Guide (RGB)", 2D) = "white" {} _SliceAmount("Slice Amount", Range(0.0, 1.0)) = 0 _BurnSize("Burn Size", Range(0.0, 1.0)) = 0.15 _BurnRamp("Burn Ramp (RGB)", 2D) = "white" {} _BurnColor("Burn Color", Color) = (1,1,1,1) _EmissionAmount("Emission amount", float) = 2.0 } SubShader { Tags { "RenderType"="Opaque" } LOD 200 Cull Off CGPROGRAM #pragma surface surf Lambert addshadow #pragma target 3.0 fixed4 _Color; sampler2D _MainTex; sampler2D _SliceGuide; sampler2D _BumpMap; sampler2D _BurnRamp; fixed4 _BurnColor; float _BurnSize; float _SliceAmount; float _EmissionAmount; struct Input { float2 uv_MainTex; }; void surf (Input IN, inout SurfaceOutput o) { fixed4 c = tex2D (_MainTex, IN.uv_MainTex) * _Color; half test = tex2D(_SliceGuide, IN.uv_MainTex).rgb - _SliceAmount; clip(test); if (test < _BurnSize && _SliceAmount > 0) { o.Emission = tex2D(_BurnRamp, float2(test * (1 / _BurnSize), 0)) * _BurnColor * _EmissionAmount; } o.Albedo = c.rgb; o.Alpha = c.a; } ENDCG } FallBack "Diffuse" }

You can tell that the code in the surf function (which does all the work) is not all that much or complicated. However, there are a few catches that are worth mentioning. But let’s take things from the start.

## Properties

There are quite a lot of them. The first two, _Color and _MainTex are the generic properties needed to add a texture and a color overlay on our object.

The _SliceGuide and _SliceAmount are responsible for the dissolving of our model. The first is a texture that will be used to determine the overall shape of the dissolving, while the latter is how much will the object be dissolved, where 0 means that the object is unaffected from the dissolving and 1 means that the object is completely dissolved.

The _BurnSize, _BurnRamp and _BurnColor properties are used to make the burning effect around the dissolved areas that I mentioned above. The first one dictates how large the burn areas around the holes will be. _BurnRamp is a texture that the burn colors can follow and _BurnColor is a color that is multiplied with the _BurnRamp to change the colors to our liking without the need of many multiple ramps. Plus, if we don’t want to use a ramp texture for the ramp, we can just have an adjustable solid color!

## Shader info and notations

In line 17 I add a “Cull Off” notation, which is used to tell to the shader not to cull (or hide) the back of the model’s faces, as it usually happens. We need it to be like that since we’ll be looking at the “insides” of our model as it’s dissolving. Otherwise the effect won’t look too good.

Furthermore, in line 19 there’s a subtle change from the default surface shader that I had to make: change the lighting model from “Standard fullforwardshadows” to “Lambert addshadow”. I figured that out after quite a lot of time experimenting. The reason for that change is to make the shadows actually follow the dissolving of the model. Otherwise, the shadow of the object would be as if it was whole, even with the “_SliceAmount” set to 1! I definitely did not want that to happen.

## Surf function

After we’re done redeclaring the properties we move on to the interesting part! Let’s see what’s happening here. First of all, as per usual, I get the color of the object by using the “tex2D” function and multiplying the result by the _Color property. The actual dissolving happens in lines 39 and 40. In line 39 I use “tex2D” again to get the colors of the _SliceGuide texture after it’s mapped on the model using the same UV coordinates as the main texture. Then, I subtract _SliceAmount from the result of the “tex2D” function, and store the difference in a variable named “test”. For that technique, the _SliceGuide texture should be a grayscale image with a repeating pattern. For this example I used a standard uniform cloud texture like this:

Since the values of the “tex2D” function will be in the spectrum of [0.0, 1.0], subtracting by the _SliceAmount which is also in the same spectrum will return a floating point value in the spectrum of [-1.0, 1.0]. If we were to cut out the values below 0, it would be safe to assume that the darker areas of the texture would be removed with a lower value of _SliceAmount. That means that if we were to increment “_SliceAmount” over time, the darker areas would be cut out first. And this is where line 40 comes in. The “clip” function basically tells the shader to discard the pixel that it’s processing at the moment if the parameter of the function, in this case “step”, is lower than zero. And this is how the dissolve effect is achieved! Now, let’s move on to the “burn” effect.

We want to apply the burning effect around the dissolved areas. This is why in line 42 I check if the “test” variable is smaller than _BurnSize. Think about it like this: the burn effect is basically the same as the dissolving effect, only instead of making holes on the object, we add emission to the areas marked by the _SliceGuide. However, we don’t want the emission areas to match the dissolving ones, we want them to be wider so we can actually see the burning effect. That’s the point of “if (test < _BurnSize)”, which can be also written as “if (test – _BurnSize < 0)”. If we were to dissolve the extended area instead of applying the emission on it, we’d just say “clip(test – _BurnSize)”. I also check if _SliceAmount is greater than 0 so that we don’t apply the burning effect if there’s no dissolving on the object.

In line 43 I apply the emission. I map the color ramp to some custom UV coordinates in order to achieve the following effect: the leftmost color of the ramp is returned on the edges of the hole, and for the rest of the area that the burning covers the emission fades towards the rightmost color. It may make more sense on this example:


Where these textures were used as _SliceGuid and _BurnRamp respectively:

After I get the result from “tex2D”, I multiply with _BurnColor and _EmissionAmount to make it a bit more custom.

In lines 46-47 I apply the Albedo color and the Alpha and that’s about it!

Also, here are some more burn ramps you can play with:

You can try many others, so go nuts!

## Epilogue

There is not really much more to say, so I’ll leave you with a cool gif of this effect along with some screen space reflections and hella lot of bloom:


See you in the [next one](http://halisavakis.com/my-take-on-shaders-random-stripes-mask/)!