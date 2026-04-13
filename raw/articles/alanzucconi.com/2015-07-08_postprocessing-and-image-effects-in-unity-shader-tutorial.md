---
title: Postprocessing and image effects in Unity - Shader Tutorial
url: https://www.alanzucconi.com/2015/07/08/screen-shaders-and-postprocessing-effects-in-unity3d/
author: Alan Zucconi
published: '2015-07-08'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

[Part 1](https://www.alanzucconi.com/2015/06/10/a-gentle-introduction-to-shaders-in-unity3d/), [Part 2](https://www.alanzucconi.com/2015/06/17/surface-shaders-in-unity3d/), [Part 3](https://www.alanzucconi.com/2015/06/24/physically-based-rendering-and-lighting-models-in-unity3d/), ** Part 4**,

**Part 5**, [

[download the Unity3D package](https://www.patreon.com/posts/2881298)]

If you are using Unity3D you may be familiar with [image effects](http://docs.unity3d.com/Manual/comp-ImageEffects.html). They are scripts which, once attached to a camera, alter its rendering output. Despite being presented as standard C# scripts, the actual computation is done using shaders. So far, materials have been applied directly to geometry; they can also be used to render offscreen textures, making them ideal for postprocessing techniques. When shaders are used in this fashion, they are often referred as *screen shaders*.

### Step 1: The shader

Let’s start with a simple example: a postprocessing effect which can be used to turn a coloured image to greyscale.

![bw](../../assets/91f0e8d9d566e153.gif)

The way to approach this problem is assuming the shader is provided with a texture, and we want to output its grayscaled version.

Shader "Hidden/BWDiffuse" { Properties { _MainTex ("Base (RGB)", 2D) = "white" {} _bwBlend ("Black & White blend", Range (0, 1)) = 0 } SubShader { Pass { CGPROGRAM #pragma vertex vert_img #pragma fragment frag #include "UnityCG.cginc" uniform sampler2D _MainTex; uniform float _bwBlend; float4 frag(v2f_img i) : COLOR { float4 c = tex2D(_MainTex, i.uv); float lum = c.r*.3 + c.g*.59 + c.b*.11; float3 bw = float3( lum, lum, lum ); float4 result = c; result.rgb = lerp(c.rgb, bw, _bwBlend); return result; } ENDCG } } }

This shader won’t alter the geometry, so there is no need for a vertex function; there’s a standard, “empty” vertex function is called `vert_img`

. We also don’t define any input or output structure, using the standard one provided by Unity3D which is called `v2f_img`

.

**Line 20** takes the colour of the current pixel, sampled from `_MainTex`

, and calculate its greyscaled version. As nicely explained by [Brandon Cannaday](https://twitter.com/thereddest) in a [post](http://tech.pro/tutorial/660/csharp-tutorial-convert-a-color-image-to-grayscale) with a similar topic, the magic numbers `.3`

, `.59`

and `.11`

used represent the sensitivity of the Human eye to the R, G and B components. Long story short: they’ll make a nicer greyscale image, based on the perceived luminosity. You can also just average the R, G and B channels, but you won’t get a result as nicer as this one.

**Line 24** interpolates the original colour and the new one using `_bwBlend`

as a blending coefficient.

This shader is not really intended to be used for 3D models; for this reason its name starts with `Hidden/`

, which won’t make it appear in the drop-down menu of the material inspector.

### Step 2: The C# script

The next step is to make this shader working as a postprocessing effect. `MonoBehaviour`

s have an event called `OnRenderImage`

which is invoked every time a new frame has to be rendered on the camera they are attached to. We can use this event to intercept the current frame and edit it, before it’s rendered on the screen.

using UnityEngine; using System.Collections; [ExecuteInEditMode] public class BWEffect : MonoBehaviour { public float intensity; private Material material; // Creates a private material used to the effect void Awake () { material = new Material( Shader.Find("Hidden/BWDiffuse") ); } // Postprocess the image void OnRenderImage (RenderTexture source, RenderTexture destination) { if (intensity == 0) { Graphics.Blit (source, destination); return; } material.SetFloat("_bwBlend", intensity); Graphics.Blit (source, destination, material); } }

**Line 13** creates a private material. We could have provided a material directly from the inspector, but there’s the risk of that being shared between other instances of `BWEffect`

. Perhaps a better option would be to provide the script with the shader itself, rather than using its name as a string.

**Line 26** is where the magic happens. The function `Blit`

takes a source `RenderTexture`

, process it with the provided material and renders it onto the specified destination. Since `Blit`

is typically used for postprocessing effects, it already initialises the property `_MainTex`

of the shader with what the camera has rendered so far. The only parameters which has to be initialised manually is the blending coefficient. **Line 19** skips the usage of the shader, if the effect has been disabled.

### ⭐ Recommended Unity Assets

### The CRT effect

One of the most used effects in games today is the CRT. Whether you grew up with old monitors or not, games are constantly using them to give that good vibe of old and retro. Games such as *Alien Isolation* and *ROUTINE*, for instance, owe lot of their charm to CRT monitors. This section will show how is possible to recreate a very simple CRT effect using screen shaders.

![crt](../../assets/00f89bae60c98132.gif)

First of all, let’s look at what makes CRT monitors:

![texture](../../assets/772207e83a04a4f5.png)

- White noise
- Scanlines
- Distortion
- Fading

Rather then using a single shader, we’ll use four of them. This is not very efficient, but it shows how post processing effects can be stacked one on top of the other. For the white noise and the fading effect we will rely on [Noise and Grain](http://docs.unity3d.com/Manual/script-NoiseAndGrain.html) and [Vignette and Chromatic Aberration](http://docs.unity3d.com/Manual/script-VignettingAndChromaticAberration.html) filters.

#### Scanlines

The effect will have RGB lines, which will appear in screen space. As seen before, it has two components: a shader, and a script which is attached to the camera. This time, however, we also need an external material (`BWEffect`

creates its own material in `Awake`

). This is because the scanline effect requires a texture which is easier to pass to a material, rather than to a script.

Shader "Hidden/CRTDiffuse" { Properties { _MainTex ("Base (RGB)", 2D) = "white" {} _MaskTex ("Mask texture", 2D) = "white" {} _maskBlend ("Mask blending", Float) = 0.5 _maskSize ("Mask Size", Float) = 1 } SubShader { Pass { CGPROGRAM #pragma vertex vert_img #pragma fragment frag #include "UnityCG.cginc" uniform sampler2D _MainTex; uniform sampler2D _MaskTex; fixed _maskBlend; fixed _maskSize; fixed4 frag (v2f_img i) : COLOR { fixed4 mask = tex2D(_MaskTex, i.uv * _maskSize); fixed4 base = tex2D(_MainTex, i.uv); return lerp(base, mask, _maskBlend ); } ENDCG } } }

The scanlines are sampled from a texture, which has be imported in the inspector with *Wrap Mode: Repeat*. This will repeat the texture over the entire screen. Thanks to the variable `_maskSize`

it is possible to decide how big the texture will be.

Fianlly, the script:

using UnityEngine; using System.Collections; [ExecuteInEditMode] public class CRTEffect : MonoBehaviour { public Material material; // Postprocess the image void OnRenderImage(RenderTexture source, RenderTexture destination) { Graphics.Blit(source, destination, material); } }

You should notice that if you are planning to use this effect on multiple cameras, you should make a copy of the material in the `Awake`

method. This will ensure every script has its own instance and you can tweak them individually without any problem.

#### Distortion

The distortion on CRT monitors is due to the curvature of the glass where the image is projected. To replicate the effect we’ll need an extra texture called `_DisplacementTex`

. It’s red and green channels will indicate how to displace pixels on the X and Y axes, respectively. Since colours in an image go from 0 to 1, we’ll rescale them to -1 to +1.

float4 frag(v2f_img i) : COLOR { half2 n = tex2D(_DisplacementTex, i.uv); half2 d = n * 2 -1; i.uv += d * _Strength; i.uv = saturate(i.uv); float4 c = tex2D(_MainTex, i.uv); return c; }

The quality of the CRT distortion heavily depends on the displacement texture which is provided. A ~~very bad~~ possible one is, for instance:

![4668-normal](../../assets/5b9b00f3e06f6778.jpg)

### Conclusion

This post shows how vertex and fragment shaders can be used to create post processing effects in Unity3D.

This post concludes the basic tutorial about shaders. More posts will follow, with more advanced techniques such as [fur shading](https://www.alanzucconi.com/2015/06/28/fur-shading-in-unity3d/), [heatmaps](https://www.alanzucconi.com/2016/10/24/arrays-shaders-unity-5-4/), water shading and volumetric explosions. Many of these posts are already available on [Patreon](https://www.patreon.com/AlanZucconi).

- Part 1:
[A gentle introduction to shaders in Unity3D](https://www.alanzucconi.com/2015/06/10/a-gentle-introduction-to-shaders-in-unity3d/) - Part 2:
[Surface shaders in Unity3D](https://www.alanzucconi.com/2015/06/17/surface-shaders-in-unity3d/) - Part 3:
[Physically Based Rendering and lighting models in Unity3D](https://www.alanzucconi.com/2015/06/24/physically-based-rendering-and-lighting-models-in-unity3d/) - Part 4:
[Vertex and fragment shader in Unity3D](https://www.alanzucconi.com/2015/07/01/vertex-and-fragment-shaders-in-unity3d/) - Part 5:
**Screen shaders and postprocessing effects in Unity3D**

## Leave a Reply Cancel reply