---
title: 'My take on shaders: Spherical mask dissolve'
url: https://halisavakis.com/my-take-on-shaders-spherical-mask-dissolve/
published: '2018-05-13'
source_blog: Technically Art – Harry Alisavakis
source_site: https://halisavakis.com
category: graphics
fetched: '2026-04-13'
---

I told you another dissolve effect was coming. I was also struggling with the name of this effect, I considered labeling it “proximity dissolve” but that wouldn’t be so accurate. In any case, the concept is simple: it’s a surface shader that dissolves parts of an object that are inside a sphere. The effect can end up looking like this:

Before we get into the code parts, let’s give a high-level concept of what’s going on here: A single material using this shader is applied to every object. That shader clips every pixel that is outside a sphere mask which has a radius and a softness property. These are determined as global shader properties through a script attached to that glowing sphere.

This spherical mask technique is actually really useful, as it can be used in a plethora of effects. In this case, I’m using it with a dissolve effect similar to the one described in the [previous dissolve post](http://halisavakis.com/my-take-on-shaders-directional-dissolve/). Another awesome use of the spherical mask is shown in [this great tutorial](https://www.youtube.com/watch?v=Ws4ukvCgTOU&list=PL3POsQzaCw52iu1_P6CnM7oTctPuPu2MV) by [Peer Play](https://www.youtube.com/channel/UCBkub2TsbCFIfdhuxRr2Lrw). However, this shader does not come without its restrictions: in its current form, it works according to just one spherical mask, and therefore you can’t have multiple spheres and take their intersection or something. Also, not that much of a restriction as it is something that bugs my lazy attitude, is the fact that you need to apply this material to every object you want to use the spherical mask on, and it would be awesome to use it as a screen space effect. Maybe not as a dissolve effect, but, for example, to turn every color to grayscale inside an area. That is an interesting shader, and, if I were you, I’d stay tuned for a post on that. (EDIT: the post about that shader is out and can be found [here](http://halisavakis.com/my-take-on-shaders-spherical-mask-post-processing-effect/))

Anyway, less talky, more code-y:

Shader "Custom/SphericalMaskDissolve" { Properties { _Color ("Color", Color) = (1,1,1,1) _MainTex ("Albedo (RGB)", 2D) = "white" {} _Glossiness ("Smoothness", Range(0,1)) = 0.5 _Metallic ("Metallic", Range(0,1)) = 0.0 [HDR]_Emission("Emission", Color) = (1,1,1,1) _NoiseSize("Noise size", float ) = 1 } SubShader { Tags { "RenderType"="Opaque" } Cull off LOD 200 CGPROGRAM // Physically based Standard lighting model, and enable shadows on all light types #pragma surface surf Standard fullforwardshadows // Use shader model 3.0 target, to get nicer looking lighting #pragma target 3.0 sampler2D _MainTex; struct Input { float2 uv_MainTex; float3 worldPos; }; half _Glossiness; half _Metallic; fixed4 _Color; fixed4 _Emission; float _NoiseSize; float3 _GLOBALMaskPosition; half _GLOBALMaskRadius; half _GLOBALMaskSoftness; // Add instancing support for this shader. You need to check 'Enable Instancing' on materials that use the shader. // See https://docs.unity3d.com/Manual/GPUInstancing.html for more information about instancing. // #pragma instancing_options assumeuniformscaling UNITY_INSTANCING_BUFFER_START(Props) // put more per-instance properties here UNITY_INSTANCING_BUFFER_END(Props) float random (float2 input) { return frac(sin(dot(input, float2(12.9898,78.233)))* 43758.5453123); } void surf (Input IN, inout SurfaceOutputStandard o) { fixed4 c = tex2D (_MainTex, IN.uv_MainTex) * _Color; half dist = distance(_GLOBALMaskPosition, IN.worldPos); half sphere = 1 - saturate((dist - _GLOBALMaskRadius) / _GLOBALMaskSoftness); clip(sphere - 0.1); float squares = step(0.5, random(floor(IN.uv_MainTex * _NoiseSize))); half emissionRing = step(sphere - 0.1, 0.1) * squares; o.Emission = _Emission * emissionRing; o.Albedo = c.rgb; o.Metallic = _Metallic; o.Smoothness = _Glossiness; o.Alpha = c.a; } ENDCG } FallBack "Diffuse" }

The concept is very similar to the previous dissolve effect, if not even simpler. In this case, as properties I just add an HDR color for the emission and the size of the pixelated emissive noise on the edges. Since this is a dissolve effect, I also use the “Cull off” directive, so that I can see the back faces of an object that’s not completely dissolved. However, in this one I don’t change the lighting model since the way I used it was on a floor-like surface and didn’t care about correctly clipped shadows. If that’s not the case with what you want to use the shader on, you can change the lighting model to Lambert the same way it was changed in the [previous post](http://halisavakis.com/my-take-on-shaders-directional-dissolve/).

Similarly, in this case I don’t need to disable batching or add a vertex shader, since I don’t need the vertex position for anything. In the Input struct, I also add a property for the world position (as shown in this [Shader Bits post](http://halisavakis.com/shader-bits-world-and-screen-space-position/)), since I will have to compare that with the sphere’s location.

After that, in lines 33-38, I declare the additional necessary fields for the effect. However, in lines 36-38, these fields are not declared in the properties block. That is because these are the properties associated with the spherical mask, and they’re controlled from an outside source. As the “GLOBAL” directive subtly hints, these are controlled globally from a script, instead of that script having to get each material with that shader and change it manually. That’s good and also kinda bad, because that means that every other material which uses this shader but has other properties will also get affected by the same spherical mask. On the other hand, you don’t have to search for all the materials with that shader and change the mask properties individually. So, it really depends on your situation and your needs. Also, let it be noted that the “GLOBAL” directive is not any mandatory keyword or something, it’s just to indicate that this property is controlled globally.

In lines 47-49 there’s our well-known random function that I’ve been copying and pasting everywhere ever since I saw it in [the book of shaders](http://thebookofshaders.com/). After that, in the surface shader, all the magic happens:

Firstly, in line 53 I get the distance between the center of our spherical mask and the world position of the current pixel. Then, I calculate the sphere with that handy formula: Distance – Radius / Softness, which I use in line 54, after I saturate the result (to keep it in a [0,1] spectrum) and subtract it from 1 to invert it. Then, I do the actual dissolving in line 55 using the “clip” function. In case you forgot, clip(x) is basically saying “If x is smaller than 0, discard that whole pixel, don’t even bother drawing it. Otherwise, it’s cool, keep going”. The actual CG documentation doesn’t state it like so, but you get the point. So, since the mask would give me a value from 0 to 1 (and if the softness was 0, it would actually give me either 0 or 1 and I wouldn’t really be bothered about dividing by 0) , just clipping the mask would not do much. That’s why I subtract 0.1 from it. This is the equivalent of the dissolve amount in other shaders, but since we control that with the radius and softness, it might as well be a hard-coded value. If you want more control, of course, you could expose it as another property.

The next segment is about that cute emissive noise we saw in the previous effect. First, I calculate the squares from the noise using the random function, based on the object’s UV coordinates and the noise size. Then the emission ring is calculated by checking if 0.1 is larger than the sphere mask – 0.1. If it is, then there should be emission, otherwise there shouldn’t be any emission. That’s where the spherical mask’s softness comes into play. Since there’s no such thing as a “soft” dissolve (the pixel either gets rendered or not) in our context, the softness is used to give us more values from 0 to 0.1 so that the emission ring can get adjusted. It might look weird, but if you play a bit with the mask values it will get more clear. That ring is then multiplied with the squares from the noise and the whole thing is multiplied with the emission color and assigned to the output’s emission value. In this case, the only emission we “allow” in our shader is the one from the emissive ring, but obviously you could combine that with other emission values (like a texture for example).

## The spherical mask controller

In order to modify the mask’s values, a script like this is used:

using System.Collections; using System.Collections.Generic; using UnityEngine; [ExecuteInEditMode] public class SphereMaskController : MonoBehaviour { public float radius = 0.5f; public float softness = 0.5f; void Update () { Shader.SetGlobalVector ("_GLOBALMaskPosition", transform.position); Shader.SetGlobalFloat ("_GLOBALMaskRadius", radius); Shader.SetGlobalFloat ("_GLOBALMaskSoftness", softness); } }

The script gets some public fields and the position of the object it’s attached to and passes them to the corresponding global shader properties. Notice that there’s no specific material or shader involved in this script, and the assignment of values is via the static function “SetGlobalVector/Float” of the “Shader” class. You can play with the mask’s values and see how they affect the material. For example, here’s a neat thing that happens if your softness is below zero:

The mask gets inverted and everything around the sphere disappears! I found that to be pretty cool, but I get easily excited either way ¯\_(ツ)_/¯

## Conclusion

That’s all there is to that shader, I think. Spherical masks are a neat effect to explore and can lead to really interesting visual effects in your game, so I hope you’ll put them to good use!

See you in the [next one](http://halisavakis.com/my-take-on-shaders-unlit-waterfall-part-1/)!

## Comments

Yo!

Thanks! I recently got into shaders and this helped put a lot of concepts I knew off into actual code I can look at anytime I try things now. Will definitly be looking at more of your tutorials!

Subbed on email and thanks again!

Author

I’m so glad to hear that! I’m here if you need anything! 😀

Sub

Hi,

I just found out about your blog and i gotta say i am REALLY impressed!

Shaders were always one of my weakness in game dev, i always had them in my “to-learn” list but never found the time to do (or that’s the lie i keep telling to myself lol)

Anyway,

now that Unity Shader Graph is out i honestly think there is no excuse to delay this anymore, and am wondering if you’re planning to make any Shader Graph tutorials, thanks a lot!

Author

Thanks for your comments, I really appreciate it ^^

While I haven’t used the new Shader Graph a lot, for now at least I prefer writing shaders by hand since some of my projects are still in Unity 2017 and the Shader Graph is not as versatile and only works with the LWRP.

On the other hand, if you can somewhat understand shader code, moving to systems like Shader Graph, UE4’s material editor or any node-based shader system can be way easier.

So, to sum up, I don’t really know if I’ll do Shader Graph tutorials any time soon (since that would also suggest coming up with more ideas), but with some playing around you could probably match the code with the nodes. And actually that gave me an idea for a post on translating code to Shader Graph nodes. So stay tuned for that 😛

Wow the result is amazing. I’m studing shaders shince the last weekend and I’m advancing so much thanks to your tutorials. I already studied 3 of them and hope to make my own soon. Thanks for share.

Author

I’m so glad to hear that =] Always happy to introduce more people into the world of shaders 😀 Keep it up, I can’t wait to see your own creations ^^