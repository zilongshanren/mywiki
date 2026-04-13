---
title: 'My take on shaders: What’s the deal with surface shaders?'
url: https://halisavakis.com/my-take-on-shaders-whats-the-deal-with-surface-shaders/
published: '2018-11-09'
source_blog: Technically Art – Harry Alisavakis
source_site: https://halisavakis.com
category: graphics
fetched: '2026-04-13'
---

Hi there. This is a quite different tutorial post than what you’re probably used to. As the featured image suggests, this shader is about making realistic stock images of people surfing with Unity’s shader file icon as a head. It’s oddly specific, but you’d be surprised how many people actually asked for this.

Ok, enough silliness. However, it actually **is** a different post than previous ones. The whole concept of this tutorial is to peel off a small layer of Unity’s surface shaders and see what makes them tick (up to a certain level, that is). The goal here is to go one abstraction level deeper into this special type of shaders and, by doing so, learn how to inject more custom stuff into this pipeline and override others. Before starting though, let me clear some things up: This post is **not** a practical effect tutorial and it’s **not **a custom lighting model tutorial. However, it is the **base **that will later allow me to (hopefully) show more practical effects and some custom lighting models, so having an intro like this will hopefully make the learning curve a bit smoother.

Let’s start off by going through the default surface shader that shows up when you make a new surface shader file:


Shader "Custom/NewSurfaceShader" { Properties { _Color ("Color", Color) = (1,1,1,1) _MainTex ("Albedo (RGB)", 2D) = "white" {} _Glossiness ("Smoothness", Range(0,1)) = 0.5 _Metallic ("Metallic", Range(0,1)) = 0.0 } SubShader { Tags { "RenderType"="Opaque" } LOD 200 CGPROGRAM // Physically based Standard lighting model, and enable shadows on all light types #pragma surface surf Standard fullforwardshadows // Use shader model 3.0 target, to get nicer looking lighting #pragma target 3.0 sampler2D _MainTex; struct Input { float2 uv_MainTex; }; half _Glossiness; half _Metallic; fixed4 _Color; // Add instancing support for this shader. You need to check 'Enable Instancing' on materials that use the shader. // See https://docs.unity3d.com/Manual/GPUInstancing.html for more information about instancing. // #pragma instancing_options assumeuniformscaling UNITY_INSTANCING_BUFFER_START(Props) // put more per-instance properties here UNITY_INSTANCING_BUFFER_END(Props) void surf (Input IN, inout SurfaceOutputStandard o) { // Albedo comes from a texture tinted by color fixed4 c = tex2D (_MainTex, IN.uv_MainTex) * _Color; o.Albedo = c.rgb; // Metallic and smoothness come from slider variables o.Metallic = _Metallic; o.Smoothness = _Glossiness; o.Alpha = c.a; } ENDCG } FallBack "Diffuse" }

Up until line 12 things are looking more or less normal. And, I mean, you’ve seen that before, I’ve had lots of posts with surface shaders in the past. But haven’t you ever wondered something along the lines of “Wait, where is this shader actually **returning** a color?”. In vertex-fragment shaders you’ve seen that by the very end of the whole shader processing a color is return as a (usually) fixed4 vector representing the color of the pixel in a RGBA format. But what about that “surf” function? Why changing “o.Albedo” changes the color when the function returns “void”? That’s what we’re talking about today.

As you can imagine, there’s a bunch of stuff in surface shaders that are hidden from us; and that’s a good thing usually! Surface shaders are awesome cause they abstract all the technical stuff in which you might not be interested, and lets you focus on achieving a cool effect and having all your PBR stuff working out of the box.

The PBR lighting stuff are applied to the shader when it uses the “Standard” lighting model. In line 14 you can see just the word “Standard” inside that tag, and it might look innocent, but that’s really what does the trick: it lets the engine know that this shader uses the “Standard” lighting model, which has all the bells and whistles we like (PBR, GI, reflection probe support etc etc). Since the definition of “Standard” lighting is hidden somewhere internally, it doesn’t need to show up in every surface shader, and, thus, it doesn’t. We’ll go more into that later when I start talking about the lighting models.

Another inconspicuous detail is the “SurfaceOutputStandard” struct that is passed in the “surf” function, in line 36. It seems like it’s some kind of magical interface, where changing one field like “o.Albedo” the whole thing changes! Boy, you’re gonna be disappointed if you thought something like that. As you can imagine, and as it’s the case with the “frag” and “vert” functions from vertex-fragment shaders, the “surf” function’s purpose is to pass values to a struct that will then be used by the lighting function to return the final color. The keywords “Albedo”, “Normal” etc are indeed needed to be called like that because of the internal conversion of the shader to a vertex-fragment shader (I assume) but besides that, it’s just a normal struct like the “Input” struct. Again, I’ll get into that more in a bit.

Finally, while the “surf” shader doesn’t actually return the struct, the “SurfaceOutputStandard” struct is passed into the function as an “inout” parameter (shown in line 36). As you know, or can guess, this basically means that the struct is passed as a reference, hence the changes that happen on its fields affect the overall result.

So, to keep a pin on something simple we can do with all that (without going deeper), we’ll do the most basic of effects with this setup: Inverse the colors. As, supposedly, we don’t know any better, inversing the final color would just need me to turn “o.Albedo = c.rgb” to “o.Albedo = 1 – c.rgb”. And that would lead from this:

To this:

You’ll notice that yeah, the colors are inversed, but the lighting stays the same, because all I changed was the Albedo, the color before lighting is applied to the material. Stick a pin on this fact, we’ll revisit it in a bit.

## Lighting Models in Surface Shaders

As I mentioned, this tutorial is not about making new lighting models. There will be posts for this, but this is not one of them. In this one, I’ll just go through a bit superficially how the shader “understands” custom lighting models.

Basically, when you add a tag next to the “surf” tag in line 14 of the first shader, you declare the name of your lighting model, in this case it’s called “Standard”. As [Unity’s manual](https://docs.unity3d.com/Manual/SL-SurfaceShaderLighting.html) suggests, if you name your lighting model “X”, you’ll have to define a function that’s called “LightingX” that can have some useful parameters for your lighting model. If you also need to write some custom GI for your lighting model, you’ll name that function “LightingX_GI”. That leads us to believe that there’s a “LightingStandard” function lying around, and that’s actually true.

Also, keep in mind you can learn more about custom lighting models from [this manual from Unity](https://docs.unity3d.com/Manual/SL-SurfaceShaderLightingExamples.html).

## Unwrapped Surface Shader

To get a more clear sense of what the standard surface shader does, I “unwrapped” it a bit to get this shader right here:

Shader "Custom/SurfaceShaderOverride" { Properties { _Color ("Color", Color) = (1,1,1,1) _MainTex ("Albedo (RGB)", 2D) = "white" {} _Glossiness ("Smoothness", Range(0,1)) = 0.5 _Metallic ("Metallic", Range(0,1)) = 0.0 } SubShader { Tags { "RenderType"="Opaque" } LOD 200 CGPROGRAM // Physically based Standard lighting model, and enable shadows on all light types #pragma surface surf StandardOverride fullforwardshadows #include "UnityPBSLighting.cginc" // Use shader model 3.0 target, to get nicer looking lighting #pragma target 3.0 sampler2D _MainTex; struct Input { float2 uv_MainTex; }; struct SurfaceOutputOverride { fixed3 Albedo; fixed3 Normal; half3 Emission; half Metallic; half Smoothness; half Occlusion; fixed Alpha; }; half _Glossiness; half _Metallic; fixed4 _Color; fixed4 LightingStandardOverride(SurfaceOutputOverride s, half3 viewDir, UnityGI gi) { SurfaceOutputStandard r; r.Albedo = s.Albedo; r.Normal = s.Normal; r.Emission = s.Emission; r.Metallic = s.Metallic; r.Smoothness = s.Smoothness; r.Occlusion = s.Occlusion; r.Alpha = s.Alpha; return LightingStandard(r, viewDir, gi); } inline void LightingStandardOverride_GI(SurfaceOutputOverride s, UnityGIInput data, inout UnityGI gi ) { UNITY_GI(gi, s, data); } // Add instancing support for this shader. You need to check 'Enable Instancing' on materials that use the shader. // See https://docs.unity3d.com/Manual/GPUInstancing.html for more information about instancing. // #pragma instancing_options assumeuniformscaling UNITY_INSTANCING_BUFFER_START(Props) // put more per-instance properties here UNITY_INSTANCING_BUFFER_END(Props) void surf (Input IN, inout SurfaceOutputOverride o) { // Albedo comes from a texture tinted by color fixed4 c = tex2D (_MainTex, IN.uv_MainTex) * _Color; o.Albedo = c.rgb; // Metallic and smoothness come from slider variables o.Metallic = _Metallic; o.Smoothness = _Glossiness; o.Alpha = c.a; } ENDCG } FallBack "Diffuse" }

Just to clarify, this shader does exactly the same stuff as the previous one, but it has some key points exposed for us to modify and override.

For this example, I’m using a “custom lighting model” (which just does whatever the standard does) called “StandardOverride”, as shown in line 14, next to the “surf” tag. You’ll also notice that I included an internal “.cginc” file in line 14 called “UnityPBSLighting.cginc”, which is needed to access the “Standard” lighting model stuff.

In lines 25-34 I declare my own “SurfaceOutput” struct called “SurfaceOutputOverride”. As I mentioned, it has only the fields found in the “SurfaceOutputStandard” struct (as shown [here](https://docs.unity3d.com/Manual/SL-SurfaceShaders.html)). However, I didn’t have to add the “SurfaceOutput” to the name, it might as well be called “Potato”. Interesting things happen when you don’t use the correct name in the fields (for instance “Albedos” instead of “Albedo”), where you’ll get an error about it on a line that doesn’t even exist in the shader file, most likely cause, as I speculated above, there’s a problem with the conversion of the shader to a vertex-fragment format. I could easily add more fields to the struct and name them as I please, though.

Before getting into the lighting stuff, let me not that in line 65, the parameter of the “surf” function is of the type “SurfaceOutputOverride”, because it’s the one I use in my lighting model as well. Also, since it’s the same as “SurfaceOutputStandard”, I could use that instead, doesn’t make a difference in this example.

Going backwards, in line 40 there’s our custom lighting function, “LightingStandardOverride”. For the needed parameters, it takes a “SurfaceOutputOverride”, as modified by the “surf” function, the camera’s view direction (for specular calculations etc) as well as Unity’s GI. The last one wouldn’t be necessary in a custom lighting model, but since all I do is using the original lighting function, I need the GI to call “LightingStandard”.

On the inside, the lighting function really doesn’t do anything spectacular. Sine “LightingStandard” needs a SurfaceOutputStandard struct, I make one and just pass the values of each field from my SurfaceOutputOverride struct. Then, in line 50, **it** happens. The Return of The Color™. After the final color is calculated using the properties of the SurfaceOutput struct and the lighting function, it is then returned and **that’s** what ends up being our lovely little pixel. And what happens inside “LightingStandard”? A bunch of stuff that we won’t go into right now. I told you, this is just **one** abstraction level closer to how these shaders work, not the whole story.

You might have also noticed that weird function in lines 53-56. This is the function that calculates the GI data of the shader and it was needed for me to add the “UnityGI gi” parameter in the lighting function. You could also mess with those properties too.

So now we have gone one level deeper into surface shaders. Returning to that pin from the end of the previous part, let’s try and invert the object’s colors again, this time taking advantage of the exposed parts of surface shader. We can now not only invert the albedo color, but the final color too, after lighting has been calculated. Don’t know why you’d want to do that, but you can! And the final result, if I change “return LightingStandard(r, viewDir, gi);” to “return 1 – LightingStandard(r, viewDir, gi);” in line 50 is going from this:

To this abomination:

Certainly doesn’t look good, but it’s an interesting example nonetheless.

## Conclusion

I don’t really expect that anyone sat down and read all of this, since it doesn’t really have any interesting practical effect. But I really hope some of you found this post useful and I also hope it gave you some insight on how surface shaders work under the hood. In later tutorials I’ll probably reference this one a few times, so that custom lighting models and such make more sense. Until then though, I’ll see you in the next one!

## Comments

Its worth noting Surface Shaders wont work with the new scriptable render pipeline stuff!

Author

Yes, that’s true! Instead Unity recommends using the Shader Graph that can get the job done. Tbh though, I’ve never been a huge fan of it! :S