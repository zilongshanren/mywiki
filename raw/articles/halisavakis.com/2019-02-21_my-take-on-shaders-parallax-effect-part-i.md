---
title: 'My take on shaders: Parallax effect (Part I)'
url: https://halisavakis.com/my-take-on-shaders-parallax-effect-part-i/
published: '2019-02-21'
source_blog: Technically Art – Harry Alisavakis
source_site: https://halisavakis.com
category: graphics
fetched: '2026-04-13'
---

This two-part tutorial is revolved around the “parallax” effect, which is basically the process of faking depth by performing some magic math on the view direction of the camera. It’s an effect that Unity’s standard shader has enabled by default and is activated by using the height texture field in the material inspector.

In this, the first part of the parallax tutorial, I’ll focus on that effect that Unity has enabled by default, before moving on to a sexier parallax effect. The reason for the structure of these tutorials will be obvious after I mention some backstory of how I figured out the whole parallax business. I will mention the backstory here, since, as you’ll see, the effect itself is really, not big a deal. You can obviously skip the backstory if you want to go right to the shader, but I figured that describing my learning process can be beneficial to other beginners.

## Backstory

Ever since I got more into shaders I was fascinated by the concept of parallax to cheat depth and achieve awesome effects like this one:

This recently led me to a rabbit hole involving raymarching and other similar techniques with which I’m still struggling. However, some days ago I came across this amazing tutorial by [Binary Impact](https://twitter.com/BinaryImpactG):

I was smitten by the simplicity of the shader graph that resulted in this effect, which was pretty much what I was trying to achieve to get the look of Schaeffer’s materials.

The tutorial was really easy to follow and I had results immediately. Problem is, the tutorial was about Shader Graph, and I don’t do Shader Graph. I followed it to get the overall logic and got that the key component to this effect, the thing missing from all my past parallax efforts was a single vector: The view direction **in tangent space**.

Now me not being too keen on some of the aspects of shader coding, I wasn’t sure how to go about to calculating that. In Shader Graph it’s just a dropdown menu and boom- tangent space view direction.

Long story short, it took a lot of Googling around, more than it should take, trying to figure out how to get the view direction in tangent space. I did end up finding out how to calculate it, but this will be revealed in the next part.

After being desperate enough, I did a last search at Unity’s [built-in shader functions](https://docs.unity3d.com/Manual/SL-BuiltinFunctions.html) only to be greeted by this:

![](../../assets/34576039e03017c7.png)

Luckily, I had my phone camera on, and took a snapshot of my reaction when seeing this:

So, while this function didn’t do exactly what I wanted, trying it gave me the default parallax effect, which I have the joy to present you in this post.

## Actually interesting part

Now that we sorted how I got here, let’s dive into the code:

Shader "Custom/ParallaxShader" {
Properties {
_Color ("Color", Color) = (1,1,1,1)
_MainTex ("Albedo (RGB)", 2D) = "white" {}
_Normal ("Normal", 2D) = "bump" {}
_Height("Height", 2D) = "white" {}
_Glossiness ("Smoothness", Range(0,1)) = 0.5
_Metallic ("Metallic", Range(0,1)) = 0.0
_Parallax("Parallax", float) = 0
}
SubShader {
Tags { "RenderType"="Opaque" }
LOD 200
CGPROGRAM
// Physically based Standard lighting model, and enable shadows on all light types
#pragma surface surf Standard fullforwardshadows
// Use shader model 3.0 target, to get nicer looking lighting
#pragma target 3.0
sampler2D _MainTex;
sampler2D _Normal;
sampler2D _Height;
struct Input {
float2 uv_MainTex;
float2 uv_Normal;
float2 uv_Height;
float3 viewDir;
};
half _Glossiness;
half _Metallic;
fixed4 _Color;
float _Parallax;
// Add instancing support for this shader. You need to check 'Enable Instancing' on materials that use the shader.
// See https://docs.unity3d.com/Manual/GPUInstancing.html for more information about instancing.
// #pragma instancing_options assumeuniformscaling
UNITY_INSTANCING_BUFFER_START(Props)
// put more per-instance properties here
UNITY_INSTANCING_BUFFER_END(Props)
void surf (Input IN, inout SurfaceOutputStandard o) {
// Albedo comes from a texture tinted by color
float heightTex = tex2D(_Height, IN.uv_Height).r;
float2 parallaxOffset = ParallaxOffset(heightTex, _Parallax, IN.viewDir);
fixed4 c = tex2D (_MainTex, IN.uv_MainTex + parallaxOffset) * _Color;
o.Normal = UnpackNormal(tex2D(_Normal, IN.uv_Normal + parallaxOffset));
o.Albedo = c.rgb;
// Metallic and smoothness come from slider variables
o.Metallic = _Metallic;
o.Smoothness = _Glossiness;
o.Alpha = c.a;
}
ENDCG
}
FallBack "Diffuse"
}



Let’s check the properties first. As you can see, this is a surface shader, so most of them were filled out already. I only added 2 sampler properties for the additional textures I use, “_Normal” and “_Height”, as well as the float property “_Parallax” that controls the amount of, well, the parallax.

The samplers are redeclared in lines 23 and 24, and in the Input struct I add UV coordinates corresponding to each sampler.

Now, I don’t remember if I mentioned this before, so I’ll say it here just in case: to get the offset and tiling from the material inspector to work on specific samplers in surface shaders, you just need to add a float2 “uv_SAMPLERNAME” in your input struct. If you sample the texture using the corresponding UV coordinates, the offset and tiling will just work automagically.

I also add the view direction in the Input struct in line 30, the way I mentioned in [this older shader bits post](https://halisavakis.com/shader-bits-camera-distance-view-direction-and-normal-vectors/). The “_Parallax” float is then redeclared in line 36 and we move on to the surf function.

In line 47 I just sample the “_Height” texture and get its red channel to use as a mask for the parallax distortion.

As you can imagine, the star of the show is in line 48: There I just get the parallax offset using the function I mentioned above. Here’s a good opportunity to check what this function actually does.

Going to Unity’s archives you can get the built-in shaders and along with them, the famous “UnityCG.cginc” file that is included in all CG shaders. In there we can find the magical function that calculates the parallax offset. Prepare to be underwhelmed:

// Calculates UV offset for parallax bump mapping
inline float2 ParallaxOffset( half h, half height, half3 viewDir )
{
h = h * height - height/2.0;
float3 v = normalize(viewDir);
v.z += 0.42;
return h * (v.xy / v.z);
}



Seriously, this is it. It maps the height value from [0,1] to [-height/2, height/2] to also displace the texture with negative values, then perform some weird calculations on the normalized view direction and that’s it. If anyone has any idea as to why they add 0.42 to v.z (besides it being 0.the answer to life the universe and everything), by all means, let me know.

After I calculate the parallax offset, I simply add it to both the main texture’s UV coordinates as well as the normal map’s UV coordinates, to offset the textures accordingly.

And this is it. This is just it. You can now bask in the glory of pixel displacement and use it in your custom surface or unlit shaders, maybe in more creative ways too! Do keep in mind though that you don’t want to crank the “_Parallax” value too high and also look the model from steep angles, cause the effect just loses all of its fidelity.

I hope this is of some use to you, I was definitely very happy to stumble into it and wanted to share my findings as soon as possible. The next part will be even more exciting, so I’d stay tuned for that!

See you in the[ next one](https://halisavakis.com/my-take-on-shaders-parallax-effect-part-ii/)!

## Comments

Any chance you could upload some texture maps? I’m having trouble understanding what each map needs to do to give a decent parallax look. (Even better – could you upload a Unity project with a material and an example scene! :0)

Author

You’re right, I forgot to mention the type of textures to use! Since the height amount is determined by a float, the height texture is usually just a grayscale picture. I always have some uniform clouds texture (generated easily from Photoshop) in my projects, which usually lets me see whether my effect is working or not.

For the gif I made for Twitter I used a set of brick textures from textures.com (this one specifically: https://www.textures.com/download/pbr0072/133107?q=brick ). Most of these sets have a “height” texture which is used for exactly this kind of effects.

It’s true that for some more complex effects having an example project with the material and scene would be really useful. It’s kind of a small hassle for simple effects like this, but it’s a solid idea for more complex shaders!

Nice, concise take on the subject and good links! To keep things as simple as possible, I try to get away with just a single normal / height texture. When you use a greyscale height map and declare it a normal map type in unity, the original height value is stored in the .w component of the generated normal map. This way you can look up the height for parallax and subsequent normal (with offset texcoords) from the same map. The fidelity of the generated normals is not necessarily as good (they are for me), but you save a sampler. I also use the height value for controlling occlusion a bit.

Author

Thanks for your comments! That’s indeed smart, but as you mentioned, height-generated normals usually don’t look as good. The concept of combining the two textures is interesting though, and if you can’t fit the height map in the normal texture, you could probably use it in the alpha channel of the albedo texture.

You can check my simple texture combiner tool ( https://twitter.com/HarryAlisavakis/status/1094710888362373127 ) to see how you would go about that. Your comment is correct, it’s better to have as few texture reads as possible!

Heh, this tool is great! 8) Simple and useful. I can’t believe how the channel / alpha workflow can still be so awkward in most editors.

Actually you still need two reads from the same texture, since the normals are read with the parallax offset applied. So, there’s no performance benefit. Come to think of it, it probably thrashes the texture cache since the reads jump around on the same unit. Oh well… It makes for a simpler material inspector anyway. 🙂