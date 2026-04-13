---
title: Mystery Dungeon Sketches in Unity URP
url: https://danielilett.com/2024-09-27-tut7-15-mystery-dungeon-sketch-urp/
author: Daniel Ilett
published: '2024-09-27'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

I’ve been replaying *Pokémon Mystery Dungeon: Rescue Team DX*, my favorite A button mashing simulator - this one can even play itself! I still love the striking visuals with the sketched shadows. You might be getting déjà vu, and yes, I have covered this game before in a tutorial, but I’ve evolved since 2020! This time, I’m going to create those shadows, and our journey is going to cover shadow maps, screen-space shadows, post processing, the normal and depth textures, and triplanar mapping. I’ll be doing everything in Unity 2022 URP, and here’s the shader I came up with:

![The result of applying sketched shadows to a sample scene. The result of applying sketched shadows to a sample scene.](../../assets/75a85ede310f82f3.png)


# Analysing the game

Let’s take a quick look at the game in action. When you’re in a dungeon, it looks like the scenery shader receives shadows from Pokémon moving through the dungeon, and those shadows act like a mask for the sketch texture. There appears to be a hard line between sketch and no sketch which matches the shadowed areas, nice and simple.

![A hard cutoff between lit and shadowed areas. A hard cutoff between lit and shadowed areas.](../../assets/e82508f6fa149a9e.png)


Near your Rescue Base and in town, however, the sketches overshoot the shadows a bit. At first, I thought the shadows around these trees were baked, but the trees do actually move in the wind slightly, and the Pokémon in town can move around too.

![A soft cutoff between lit and shadowed areas, with sketched overshooting. A soft cutoff between lit and shadowed areas, with sketched overshooting.](../../assets/9318808b75449f7e.png)


Clearly, our shader needs to dynamically generate the sketches, but still be able to overshoot the shadowed region. That means I’ll need to find a way to extend the shadows across surfaces slightly before I can use them as a mask.

# How Unity renders a frame

There’s a surprising amount of work that goes into just extending the shadows, and I’m sure you can find a simpler solution, but I think I came up with a fun way of doing things that touches a lot of different bits of Unity. Let’s start by cracking open the Frame Debugger and seeing how URP renders a frame.

This little gizmo breaks down each draw call issued to your GPU and gives you lots of useful information, such as the textures, matrices, variables, and keywords used for this draw call, what the output looks like, and even why the GPU couldn’t batch two draw calls together. If you’re getting thousands of draw calls and you have no clue where they’re coming from, the Frame Debugger is your friend. You can open it with *Window -> Analysis -> Frame Debugger* from the upper toolbar. You can click any of the draw calls on the left-hand list, then scroll down the part of the window which displays the output to see more information about the data used in that draw call.

![The frame debugger window with each draw call made by Unity. The frame debugger window with each draw call made by Unity.](../../assets/32a22f18495635c1.png)


Going down the list, the first operation is clearing a texture called `_MainLightShadowmapTexture`

, and then we draw the main light’s shadows to that texture with MainLightShadow. That sounds like it might be helpful for us! This shadow map texture contains the distance of the closest objects the directional light sees when it looks down at the scene, and we can use it later when drawing objects to the screen for realsies to check whether a given pixel is in shadow. Later in the rendering loop, you’ll see the DrawOpaqueObjects group of draw calls, which draws objects to the screen, and we can verify that these draw calls read from the `_MainLightShadowmapTexture`

in the Textures section, which implies we might be able to read this texture ourselves.

![Reading from the shadow map in the Lit shader passes. Reading from the shadow map in the Lit shader passes.](../../assets/11699248180ca747.png)


We can go one step further. I’m going to use post processing to apply my sketches, so it would be useful to have access to a shadow map relative to the screen. We can do just that by adding the `Screen Space Shadows`

Renderer Feature to URP. Dunno what this does under the hood - as far as I’m concerned, it’s magic. You can do this by finding the Universal Renderer Data asset (usually in Assets/Settings) and adding URP’s Screen Space Shadows feature from the drop-down list.

![Writing screen space shadows instead. Writing screen space shadows instead.](../../assets/7266f9bd3aedec76.png)


In the Frame Debugger, we can see that this feature runs after MainLightShadow, and it reads from `_MainLightShadowmapTexture`

and writes to a new `_ScreenSpaceShadowmapTexture`

. Then, if we check a draw call within DrawOpaqueObjects, it now reads from `_ScreenSpaceShadowmapTexture`

instead of `_MainLightShadowmapTexture`

. Nice.

![Reading from the shadow map and writing a new one in screen-space. Reading from the shadow map and writing a new one in screen-space.](../../assets/12f925191ba41f60.png)


# Post-processing in URP

Let’s finally boot up a code editor and start putting together a post process effect - the full source code is [available on GitHub](https://github.com/daniel-ilett/shaders-sketched), along with the test scene. This post process will take the screen space shadow map and blur it a little to make it cover a larger area, then we’ll use that as a mask for applying the sketch texture.

I covered URP post processing in a previous tutorial about Gaussian blur - oh, that’s useful - and to recap, we use **Renderer Features** to inject a custom pass somewhere into URP’s rendering loop. There are four parts to such an effect:

- A
`Settings`

file which contains all the shader variables we want to tweak using the Inspector. - A
`RenderPass`

which manages sending data to the GPU and running the shader. - A
`RendererFeature`

which creates the pass and injects it into the URP render loop. - And finally, a shader file which defines how we want to mangle the screen pixels.

## SketchSettings.cs

Let’s start with the `SketchSettings`

C# class. This class needs to extend from `VolumeComponent`

and `IPostProcessComponent`

, which makes our effect compatible with URP’s volume system, the same one used by the out-of-the-box effects. The `System.Serializable`

attribute is crucial for saving any values we change, and the `VolumeComponentMenu`

attribute defines the name we see in the menu when we add this effect to a volume.

```
namespace DanielIlett.Sketch
{
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.Universal;
[System.Serializable, VolumeComponentMenu("Daniel Ilett/Sketch")]
public class SketchSettings : VolumeComponent, IPostProcessComponent
{
// Class contents go here.
}
}
```


The settings class is largely just a container for the shader variables we want to tweak, and we can list them here using different `Parameter`

types. These are wrappers around basic types like floats and textures, with corresponding names like `FloatParameter`

and `TextureParameter`

, plus `NoInterp`

versions which don’t interpolate values as the camera approaches a volume. [Here’s the full list](https://docs.unity3d.com/Packages/com.unity.render-pipelines.core@10.4/api/UnityEngine.Rendering.VolumeParameter-1.html). We’re gonna need variables for the sketch texture itself, which looks something like this, a tint color, a tiling amount for the texture, a pair of thresholds to define a falloff region for the edges of the sketches, an option to apply the sketches twice in a cross-hatched pattern, and a few settings for the blurring that I’ll explore later.

```
public SketchSettings()
{
displayName = "Sketch";
}
[Tooltip("Texture to use for the sketch pattern.")]
public TextureParameter sketchTexture = new TextureParameter(null);
[Tooltip("Color used to tint the sketch texture.")]
public ColorParameter sketchColor = new ColorParameter(Color.black);
[Tooltip("How much the sketch texture should be tiled in each direction.")]
public Vector2Parameter sketchTiling = new Vector2Parameter(Vector2.one);
[Tooltip("First value = shadow value where sketches start.\nSecond value = shadow value where sketches are at full opacity.")]
public Vector2Parameter sketchThresholds = new Vector2Parameter(new Vector2(0.0f, 0.1f));
[Tooltip("Controls whether to sample the sketch texture twice.")]
public BoolParameter crossHatching = new BoolParameter(false);
[Tooltip("How strongly the shadow map is blurred. Higher values mean the sketches extend further outside the shadowed regions.")]
public ClampedIntParameter blurAmount = new ClampedIntParameter(3, 3, 500);
[Tooltip("Higher values will skip pixels during blur passes. Increase for better performance.")]
public ClampedIntParameter blurStepSize = new ClampedIntParameter(1, 1, 16);
[Tooltip("Sensitivity of the function which prevents sketches appearing improperly on some objects.")]
public ClampedFloatParameter extendDepthSensitivity = new ClampedFloatParameter(0.002f, 0.0001f, 0.01f);
public bool IsActive()
{
return sketchTexture.value != null && active;
}
public bool IsTileCompatible()
{
return false;
}
```


We also need to provide an `IsActive`

method which lets us run the effect only when the parameters are set to sensible values. We’ll say the sketch texture must not be null. The `IsTileCompatible`

method is probably something to do with tiled rendering, but one year on from the Gaussian Blur tutorial, it’s still marked as obsolete from Unity 2023 onwards, which is now called Unity 6, so I still don’t really care, and I still just return false, and it still hasn’t broken everything, so we Gucci. That’s all for the `SketchSettings`

file.

Subscribe to my Patreon for perks including early access, your name in the credits of my videos, and bonus access to several premium shader packs!

## Sketch Renderer Feature

The second file is called `Sketch.cs`

. This class extends `ScriptableRendererFeature`

, which means it needs to include `Create`

, `AddRenderPasses`

, and `Dispose`

methods, and it’ll also contain the whole `SketchRenderPass`

class.

```
namespace DanielIlett.Sketch
{
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.Universal;
public class Sketch : ScriptableRendererFeature
{
// Renderer Feature code goes here.
class SketchRenderPass : ScriptableRenderPass
{
// SketchRenderPass code goes here.
}
}
}
```


The Renderer Feature itself is pretty bare-bones - it just contains an instance of the pass, which it creates in `Create`

(revolutionary I know) and then injects it into the URP render loop in `AddRenderPasses`

if there’s a valid, active pass attached to a volume. Otherwise, we save on resources by not processing the pass at all. `Dispose`

will just call a helper method I’m going to define in `SketchRenderPass`

.

```
SketchRenderPass sketchPass;
public override void Create()
{
sketchPass = new SketchRenderPass();
name = "Sketch";
}
public override void AddRenderPasses(ScriptableRenderer renderer, ref RenderingData renderingData)
{
var settings = VolumeManager.instance.stack.GetComponent<SketchSettings>();
if (settings != null && settings.IsActive())
{
renderer.EnqueuePass(sketchPass);
}
}
protected override void Dispose(bool disposing)
{
sketchPass.Dispose();
base.Dispose(disposing);
}
class SketchRenderPass : ScriptableRenderPass
{
// SketchRenderPass code goes here.
}
```


## Sketch Render Pass

Speaking of which, let’s write the pass now. It extends `ScriptableRenderPass`

and overrides the `Configure`

and `Execute`

methods, plus a few convenience methods, namely `CreateMaterial`

and `Dispose`

.

```
class SketchRenderPass : ScriptableRenderPass
{
// Instance variables here.
public SketchRenderPass()
{
// Constructor code here.
}
private void CreateMaterial()
{
// CreateMaterial code here.
}
public override void Configure(CommandBuffer cmd, RenderTextureDescriptor cameraTextureDescriptor)
{
// Configure code here.
}
public override void Execute(ScriptableRenderContext context, ref RenderingData renderingData)
{
// Execute code here.
}
public void Dispose()
{
// Dispose code here.
}
}
```


The constructor sets up a `ProfilingSampler`

which gives us a way to accurately profile the effect, and then we can set where to inject this pass into the rendering loop. There are [many, many places we can choose](https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@12.0/api/UnityEngine.Rendering.Universal.RenderPassEvent.html), but I settled on `BeforeRenderingPostProcessing`

, which might be a misleading name since we are doing post processing, but the “before” refers to URP’s internal post processing, things like `Bloom`

, `Vignetting`

, and `Color Adjustments`

which are included out of the box.

```
public SketchRenderPass()
{
profilingSampler = new ProfilingSampler("Sketch");
renderPassEvent = RenderPassEvent.BeforeRenderingPostProcessing;
}
```


The `CreateMaterial`

helper method I wrote tries to find the shader file and creates a material instance, throwing up an error if the file is missing. Pretty simple.

```
private void CreateMaterial()
{
var shader = Shader.Find("DanielIlett/Sketch");
if (shader == null)
{
Debug.LogError("Cannot find shader: \"DanielIlett/Sketch\".");
return;
}
material = new Material(shader);
}
```


Then, the `Configure`

method is for setting up resources required for the pass. The class has four member variables: the material, which we just dealt with, and three render textures. That’s a lot of textures, but they’re all crucial.

Okay, there’s lots going on here.

The `RTHandle`

type is a wrapper around the old `RenderTexture`

type which is meant to work better with URP. We’re going to copy the screen contents to `tempTexHandle`

for reasons I’ll explore later, so it uses the same render texture descriptor as the camera texture, with a couple of tweaks. Next, we set up two more `RTHandles`

, which I’ve named `shadowmapHandle1`

and `2`

. The shadowmap only uses the red color channel because it’s greyscale, and uses a precision of 8 bits, so we use the `R8`

texture format to save on texture memory over the camera texture, which apparently uses the `RGB111110Float`

format. `ReAllocateIfNeeded`

is meant to scale your textures automatically if you resize the screen, so that’s nice! We’re going to need the depth and normals textures later, so we will configure both of those here too.

```
private Material material;
private RTHandle tempTexHandle;
private RTHandle shadowmapHandle1;
private RTHandle shadowmapHandle2;
public SketchRenderPass()
{
// Constructor code here.
}
private void CreateMaterial()
{
// CreateMaterial code here.
}
public override void Configure(CommandBuffer cmd, RenderTextureDescriptor cameraTextureDescriptor)
{
ResetTarget();
var descriptor = cameraTextureDescriptor;
descriptor.msaaSamples = 1;
descriptor.depthBufferBits = (int)DepthBits.None;
RenderingUtils.ReAllocateIfNeeded(ref tempTexHandle, descriptor);
descriptor.colorFormat = RenderTextureFormat.R8;
RenderingUtils.ReAllocateIfNeeded(ref shadowmapHandle1, descriptor);
RenderingUtils.ReAllocateIfNeeded(ref shadowmapHandle2, descriptor);
ConfigureInput(ScriptableRenderPassInput.Depth);
ConfigureInput(ScriptableRenderPassInput.Normal);
base.Configure(cmd, cameraTextureDescriptor);
}
```


Now let’s `Execute`

some frames. This is the juicy, meaty bit where we start telling Unity to draw some stuff. First, stop running immediately if this is running on a preview camera - you know, the little preview window which pops up when you select a camera. Otherwise, the heavens open up and a flood of errors will saturate your console window.

![The preview camera shouldn't run the effect. The preview camera shouldn't run the effect.](../../assets/66259b8007a810a2.png)


Next, let’s make sure the material exists and then start to set up a `CommandBuffer`

. As the name suggests, this is a list of GPU commands which will be executed in order. We’ll grab the `SketchSettings`

values from our volume and pass most of them directly to the shader via the `Set`

methods on the material, although there are a couple of properties we’ll tweak before sending them: first, we’ll send over not only the `blurAmount`

, which is the size of the blur kernel, but also an extra `_Spread`

property which is the `blurAmount`

divided by six. We use six because it’s the standard deviation I chose to used in the Gaussian value calculations - my previous Blur tutorial goes into more detail about that. Second, we’ll convert the cross-hatching Boolean to a float value that’s 0 or 1, because even though HLSL supports bool types, the material doesn’t.

```
public override void Execute(ScriptableRenderContext context, ref RenderingData renderingData)
{
if (renderingData.cameraData.isPreviewCamera)
{
return;
}
if (material == null)
{
CreateMaterial();
}
CommandBuffer cmd = CommandBufferPool.Get();
// Set Sketch effect properties.
var settings = VolumeManager.instance.stack.GetComponent<SketchSettings>();
material.SetTexture("_SketchTexture", settings.sketchTexture.value);
material.SetColor("_SketchColor", settings.sketchColor.value);
material.SetVector("_SketchTiling", settings.sketchTiling.value);
material.SetVector("_SketchThresholds", settings.sketchThresholds.value);
material.SetFloat("_DepthSensitivity", settings.extendDepthSensitivity.value);
material.SetFloat("_CrossHatching", settings.crossHatching.value ? 1 : 0);
material.SetInt("_KernelSize", settings.blurAmount.value);
material.SetFloat("_Spread", settings.blurAmount.value / 6.0f);
material.SetInt("_BlurStepSize", settings.blurStepSize.value);
// Second half of the Execute method goes here.
}
```


Now it’s time for some texture-fu. Let’s open up a profiling scope and then do a bunch of `Blit`

operations - that means copying from one texture to another, optionally applying a shader pass while doing so. We can find the `_ScreenSpaceShadowmapTexture`

using its internal ID, and then grab the camera’s output so far into a variable called `cameraTargetHandle`

. The `cameraTargetHandle`

variable is crucial - the texture data contained inside it by the end of the `Execute`

method will be drawn to the screen. Using the Frame Debugger, we can see that the texture looks something like this directly before we run the post process:

![The camera contents before post processing. The camera contents before post processing.](../../assets/92ff77dc56733522.png)


Then, let’s copy the shadowmap into one of the `RTHandles`

, the one named `shadowmapHandle1`

, using the `Blit`

method.

```
// Perform the Blit operations for the Sketch effect.
using (new ProfilingScope(cmd, profilingSampler))
{
var shadowmapTextureID = Shader.PropertyToID("_ScreenSpaceShadowmapTexture");
var shadowmapTexture = (RenderTexture)Shader.GetGlobalTexture(shadowmapTextureID);
RTHandle cameraTargetHandle = renderingData.cameraData.renderer.cameraColorTargetHandle;
Blit(cmd, shadowmapTexture, shadowmapHandle1);
// More texture operations go here.
}
// Finishing up the Execute method goes here.
```


I’m gonna go off on a bit of a side rant here. When you do this `Blit`

between `shadowmapTexture`

and `shadowmapHandle1`

, the compiler will complain. Uh-oh. This is one of my gripes with URP’s post processing APIs - where we have the old `RenderTexture`

APIs and the new `RTHandle`

-based ecosystem, which clash a lot. You’re meant to use the new `Blitter`

API, but there didn’t seem to be a way to get this texture copy working unless I used the old, deprecated `Blit`

method. A lot of Unity’s newer APIs, especially related to graphics, tend to be poorly documented in my opinion. However, it looks as though the effect works, and that’s good enough for me - just be prepared for this to all break in some future Unity version. On that note, I didn’t finish adding Unity 6 compatability to this effect, so you may need to put in a little work to do that.

Now it’s time to run the blur shader (which of course, we haven’t written yet). The shader will contain three passes: the first is for applying the sketch pattern using a blurred shadowmap, and the other two contain hoirozontal and vertical blur passes respectively. We use a two-pass blur because its computational complexity increases linearly with image size, whereas a single-pass blur increases quadratically. Two-pass is vastly more efficient. I have also included an extra blur step size parameter, which is an optimization I devised since my Gaussian Blur tutorial. Essentially, we can skip out some pixels from the blur kernel, so we end up with a sparse kernel which still operates on far-away pixels, but with gaps to increase efficiency. The reduction in the number of calculations is quite drastic for large blur kernels, and many times, the difference is imperceptible.

We’ll only run the blur shader if the kernel size if strictly greater than double the step size, and then to do the blur we play some ping-pong. That’s the process of `Blit`

ting from one texture to another, then back again, often performing different shader passes during each `Blit`

.

For the first `Blit`

from `shadowmapHandle`

1 to 2, we’ll run the horizontal pass, which has an index of 1 because it’s the second pass in the file, and like all good programmers we’re using zero-based indexing. Then, we’ll blur from 2 to 1 with the vertical pass, with index 2. Here, we’re using the new `Blitter`

API, which Unity intends you to use from now on. This API contains many methods for copying textures of different formats and for different use cases - since we are working with post process effects, `BlitCameraTexture`

works well. We can then attach the result, a fully blurred texture, to the material under the name `_ShadowmapTexture`

, which will make it available for use in the sketch pass.

```
// Perform the Blit operations for the Sketch effect.
using (new ProfilingScope(cmd, profilingSampler))
{
var shadowmapTextureID = Shader.PropertyToID("_ScreenSpaceShadowmapTexture");
var shadowmapTexture = (RenderTexture)Shader.GetGlobalTexture(shadowmapTextureID);
RTHandle cameraTargetHandle = renderingData.cameraData.renderer.cameraColorTargetHandle;
Blit(cmd, shadowmapTexture, shadowmapHandle1);
if (settings.blurAmount.value > settings.blurStepSize.value * 2)
{
// Blur the shadowmap texture.
Blitter.BlitCameraTexture(cmd, shadowmapHandle1, shadowmapHandle2, material, 1);
Blitter.BlitCameraTexture(cmd, shadowmapHandle2, shadowmapHandle1, material, 2);
}
material.SetTexture("_ShadowmapTexture", shadowmapHandle1);
// Apply the sketch effect to the world.
Blitter.BlitCameraTexture(cmd, cameraTargetHandle, tempTexHandle);
Blitter.BlitCameraTexture(cmd, tempTexHandle, cameraTargetHandle, material, 0);
}
// Finishing up the Execute method goes here.
```


And finally, we can run the sketch pass. We can’t blur from `cameraTargetHandle`

to itself, so we’ll go for another game of ping-pong and copy `cameraTargetHandle`

to `tempTexHandle`

without using a material, then back again, this time specifying the 0th shader pass. Fun fact: ping-pong used to be called “whiff-whaff” - no wonder so many people celebrate independence from Britain. After closing the `ProfilingScope`

, we can execute the command buffer and release it back to the command buffer pool.

```
// After ProfilingScope has been closed.
context.ExecuteCommandBuffer(cmd);
cmd.Clear();
CommandBufferPool.Release(cmd);
```


All that’s left is the `Dispose`

method, which releases the memory used by the three `RTHandles`

. We’re all done on the C# scripting side, and all that’s left is the shader file.

```
public void Dispose()
{
tempTexHandle?.Release();
shadowmapHandle1?.Release();
shadowmapHandle2?.Release();
}
```


Subscribe to my Patreon for perks including early access, your name in the credits of my videos, and bonus access to several premium shader packs!

## Sketch shader

Here’s how I’ll structure the shader. First, there’s a `ShaderLab`

wrapper around everything, with associated boilerplate. Inside that, I’ll have an `HLSLINCLUDE`

block containing everything that’s needed by multiple passes - no point in declaring stuff twice. Then, I will have the sketch pass, horizontal blur pass and vertical blur pass, in that order.

```
Shader "DanielIlett/Sketch"
{
SubShader
{
Tags
{
"RenderType" = "Opaque"
"RenderPipeline" = "UniversalPipeline"
}
HLSLINCLUDE
// Shared code here.
ENDHLSL
Pass
{
Name "Sketch Main"
HLSLPROGRAM
// Sketch code here.
ENDHLSL
}
Pass
{
Name "Horizontal Blur"
HLSLPROGRAM
// Horizontal blur here.
ENDHLSL
}
Pass
{
Name "Vertical Blur"
HLSLPROGRAM
// Vertical blur here.
ENDHLSL
}
}
}
```


`HLSLINCLUDE`

will contain some include files from Unity’s shader APIs, notably the `DeclareDepthTexture`

file, which sets up the `_CameraDepthTexture`

and associated helper functions, and the `Blit`

file, which sets up a `_BlitTexture`

variable containing the source texture whenever we use one of these shader passes in a C# `Blit`

operation. It also gives us a pre-written vertex shader for rendering a full-screen quad, so we can focus entirely on writing the fragment shader, which is where the wizardry happens in post processing.

I’ll also pack in a few blur-related variables we passed from `SketchSettings`

, a `Gaussian`

function, and define the `e`

constant, then wrap up the `HLSLINCLUDE`

block with a helper function for sampling the depth texture.

```
HLSLINCLUDE
#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/DeclareDepthTexture.hlsl"
#include "Packages/com.unity.render-pipelines.core/Runtime/Utilities/Blit.hlsl"
#define E 2.71828f
uint _KernelSize;
float _Spread;
float _DepthSensitivity;
uint _BlurStepSize;
float gaussian(int x)
{
float sigmaSqu = _Spread * _Spread;
return (1 / sqrt(TWO_PI * sigmaSqu)) * pow(E, -(x * x) / (2 * sigmaSqu));
}
float sampleDepth(float2 uv)
{
#if UNITY_REVERSED_Z
return SampleSceneDepth(uv);
#else
return lerp(UNITY_NEAR_CLIP_VALUE, 1, SampleSceneDepth(uv));
#endif
}
ENDHLSL
```


Let’s write the horizontal blur pass first - the second pass in the file. I explored this in the Gaussian Blur tutorial, so I’ll explain this one only briefly: it’s generating a Gaussian kernel and multiplying the contribution from nearby pixels. This time, it’s also factoring in the blur step size for an efficiency boost.

```
Pass
{
Name "Horizontal Blur"
HLSLPROGRAM
#pragma vertex Vert
#pragma fragment frag_horizontal
float4 frag_horizontal (Varyings i) : SV_Target
{
float depth = sampleDepth(i.texcoord);
float3 col = 0.0f;
float kernelSum = 0.001f;
int upper = ((_KernelSize - 1) / 2);
int lower = -upper;
float2 uv;
for (int x = lower; x <= upper; x += _BlurStepSize)
{
uv = i.texcoord + float2(_BlitTexture_TexelSize.x * x, 0.0f);
float newDepth = sampleDepth(uv);
if(newDepth > 0.001f && abs(depth - newDepth) < _DepthSensitivity)
{
float gauss = gaussian(x);
kernelSum += gauss;
col += gauss * SAMPLE_TEXTURE2D(_BlitTexture, sampler_LinearClamp, uv);
}
}
col /= kernelSum;
return float4(col, 1.0f);
}
ENDHLSL
}
```


I’ve also made one other change. Let’s see what happens if we run a regular blur on the shadowmap and apply the sketches:

![Extending shadows works, but looks poor at object boundaries. Extending shadows works, but looks poor at object boundaries.](../../assets/969a44a5781a2a24.png)


The sketches nicely extend past the shadowed areas, which is great, but they also extend past object boundaries, which is not so great. I ended up fixing this by calculating the depth of the center pixel - the distance from the camera - and then I compare it with the depth of the kernel pixels and only consider them as part of the blur calculations if there is a small depth difference. Otherwise, the comparison pixel is past the object boundary, and we don’t want to blur into that pixel, so we ignore it.

The vertical pass is very similar to the horizontal pass, except I’m blurring along the y-axis instead of the x.

```
Pass
{
Name "Vertical Blur"
HLSLPROGRAM
#pragma vertex Vert
#pragma fragment frag_vertical
float4 frag_vertical (Varyings i) : SV_Target
{
float depth = sampleDepth(i.texcoord);
float3 col = 0.0f;
float kernelSum = 0.001f;
int upper = ((_KernelSize - 1) / 2);
int lower = -upper;
float2 uv;
for (int y = lower; y <= upper; y += _BlurStepSize)
{
uv = i.texcoord + float2(0.0f, _BlitTexture_TexelSize.y * y);
float newDepth = sampleDepth(uv);
if(newDepth > 0.001f && abs(depth - newDepth) < _DepthSensitivity)
{
float gauss = gaussian(y);
kernelSum += gauss;
col += gauss * SAMPLE_TEXTURE2D(_BlitTexture, sampler_LinearClamp, uv);
}
}
col /= kernelSum;
return float4(col, 1.0f);
}
ENDHLSL
}
```


That leaves the sketch pass. This one needs access to the normals texture, which we can get with the `DeclareNormalsTexture`

include file, plus the remaining shader variables from `SketchSettings`

which I will list here. I’m also going to define a triplanar sampling function based on Catlike Coding’s implementation - thanks, Jasper!

```
Pass
{
Name "Sketch Main"
HLSLPROGRAM
#pragma vertex Vert
#pragma fragment frag
#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/DeclareNormalsTexture.hlsl"
TEXTURE2D(_SketchTexture);
TEXTURE2D(_ShadowmapTexture);
float4 _SketchColor;
float2 _SketchThresholds;
float2 _SketchTiling;
float _CrossHatching;
// Based on https://catlikecoding.com/unity/tutorials/advanced-rendering/triplanar-mapping/:
float4 triplanarSample(Texture2D tex, SamplerState texSampler, float2x2 rotation, float3 uv, float3 normals, float blend)
{
float2 uvX = mul(rotation, uv.zy * _SketchTiling);
float2 uvY = mul(rotation, uv.xz * _SketchTiling);
float2 uvZ = mul(rotation, uv.xy * _SketchTiling);
if (normals.x < 0)
{
uvX.x = -uvX.x;
}
if (normals.y < 0)
{
uvY.x = -uvY.x;
}
if (normals.z >= 0)
{
uvZ.x = -uvZ.x;
}
float4 colX = SAMPLE_TEXTURE2D(tex, texSampler, uvX);
float4 colY = SAMPLE_TEXTURE2D(tex, texSampler, uvY);
float4 colZ = SAMPLE_TEXTURE2D(tex, texSampler, uvZ);
float3 blending = pow(abs(normals), blend);
blending /= dot(blending, 1.0f);
return (colX * blending.x + colY * blending.y + colZ * blending.z);
}
float4 frag (Varyings i) : SV_Target
{
// Fragment shader code here.
}
ENDHLSL
}
```


I decided triplanar mapping would be a good way to apply the sketch texture. Since we don’t have access to mesh UVs because we’re doing a post process, I’ll need to use other information. Applying the sketches in screen-space doesn’t look great. So instead, I can derive the world coordinates of each pixel using the information in the depth texture, and then use triplanar sampling to sample the sketch texture three times, using the xy, yz, and xz planes of the world position as three sets of UV coordinates, and then choose the sample which most closely corresponds to direction the pixel’s normal vector faces. That’s why we needed the normals texture too!

![World positions and normals, available to the post process shader. World positions and normals, available to the post process shader.](../../assets/071bf57717977dbe.png)


If we’re cross-hatching, then I’ll rotate 90 degrees and do a second triplanar sample. Sure, doing this many samples for each pixel is excessive, and you can probably optimize out these matrix multiplications, but I’ll leave that as homework if you want a more efficient shader.

```
float4 frag (Varyings i) : SV_Target
{
float4 col = SAMPLE_TEXTURE2D(_BlitTexture, sampler_LinearClamp, i.texcoord);
float depth = sampleDepth(i.texcoord);
float3 worldPos = ComputeWorldSpacePosition(i.texcoord, depth, UNITY_MATRIX_I_VP);
float3 worldNormal = normalize(SAMPLE_TEXTURE2D(_CameraNormalsTexture, sampler_LinearClamp, i.texcoord));
float2x2 rotationMatrix = float2x2(1, 0, 0, 1);
float4 sketchTexture = saturate(triplanarSample(_SketchTexture, sampler_LinearRepeat, rotationMatrix, worldPos, worldNormal, 10.0f));
if(_CrossHatching > 0.5f)
{
rotationMatrix = float2x2(1, 0, 0, 1);
float4 sketchTexture2 = saturate(triplanarSample(_SketchTexture, sampler_LinearRepeat, rotationMatrix, worldPos, worldNormal, 10.0f));
sketchTexture.rgb = saturate(sketchTexture + sketchTexture2).rgb;
sketchTexture.a = max(sketchTexture.a, sketchTexture2.a);
}
// End of fragment shader code here.
}
```


Finally, let’s grab the shadows from `_ShadowmapTexture`

- if you recall, we sent the blurred shadowmap result via this texture - and use `smoothstep`

to blend the edge regions of the shadows using the thresholds we defined in `SketchSettings`

, and use the resulting value as a mask for applying the sketches.

```
float4 frag (Varyings i) : SV_Target
{
// Start of fragment shader code here.
sketchTexture *= _SketchColor;
float shadows = 1.0f - SAMPLE_TEXTURE2D(_ShadowmapTexture, sampler_LinearClamp, i.texcoord).r;
shadows = smoothstep(_SketchThresholds.x, _SketchThresholds.y, shadows);
return lerp(col, sketchTexture, shadows * sketchTexture.a);
}
```


Phew! That was a lot of code, but here we are - a slightly fancy way of applying the sketches, the way Mr. Pokémon, John Pokémon himself, intended.

![The result of applying sketched shadows to a sample scene. The result of applying sketched shadows to a sample scene.](../../assets/75a85ede310f82f3.png)


To recap, we learned about shadow maps, screen-space shadow mapping, the Frame Debugger, Renderer Features, the new Blitter API, the normals and depth textures, and triplanar mapping to create this effect. As I said, probably and overcomplicated way to do all of this, but I wanted to do this in a fun way that also gave me an excuse to explore lots of different Unity features all in once effect. I’m happy with the result, and it has decent performance, even with large blur kernels.

I hope you found this tutorial useful or interesting, and I’ll see you in the next one! Until then, have fun making shaders!