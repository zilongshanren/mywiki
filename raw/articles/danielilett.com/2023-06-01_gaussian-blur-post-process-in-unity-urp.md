---
title: Gaussian Blur Post Process in Unity URP
url: https://danielilett.com/2023-06-01-tut6-6-gaussian-blur/
author: Daniel Ilett
published: '2023-06-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

Gaussian Blur is an extremely useful trick that all technical artists should keep in their box of tricks. Surprisingly, Unity doesn’t come with its own blur effect, besides a Depth of Field effect, which is a blur based on distance from the camera. Sometimes, you want to blur the entire screen uniformly, so it’s up to us to build that effect ourselves. In this tutorial, I’ll create a post processing effect in URP for Unity 2021.

![Blur Result. Blur Result.](../../assets/f3cd1ff70b13b392.png)


In a previous article, I used Unity 2022’s new Fullscreen Shader Graph to create an outline post process. However, it doesn’t support multi-pass effects (spoiler alert: I’ll be using a two-pass blur technique), nor can you use Fullscreen Shader Graph in Unity 2021. So here we are, with URP’s code-based Scriptable Renderer Features as our best option.

# Gaussian Blur Basics

You may have heard of the Gaussian curve being described as a “bell curve”. It has a distinctive shape, controlled by two parameters: the `standard deviation`

, σ, which controls how spread out the curve shape is, and the `mean`

, μ, which controls the positioning of the curve away from 0 along the x-axis. The ‘tails’ of the curve never quite reach zero, although they get very close.

![Gaussian Equation. Gaussian Equation.](../../assets/db724450ee2dc9a4.png)


![Gaussian Curve. Gaussian Curve.](../../assets/76ac4b64eccaaa03.png)


It’s possible to extend the Gaussian function into an extra dimension, which sort of looks like you’ve draped a tablecloth over something, but it’s the same idea: a mean, which is now two-dimensional, and a spread value.

![2D Gaussian Curve. 2D Gaussian Curve.](../../assets/15b1271043a418d0.png)

[Wikipedia](https://en.wikipedia.org/wiki/Gaussian_function#/media/File:Gaussian_2d_surface.png))

How does this help us create a blur effect? If we take an image, for each pixel, we can overlay a small grid of weight values based on Gaussian curve values - there’s a large weight value in the center which gets smaller as you go towards the edge of the grid. If we multiply each pixel color by its associated weight value, sum the new colors, and assign the result back to the center pixel on a fresh new image, then carry out the same process on every pixel of the source image, we end up with a blurred image. This process is called convolution, and the idea is that the weights add up to about 1 so we end up mixing lots of the center pixel color with smaller bits of the nearby pixels’ colors, so pixels bleed into each other a bit.

![Convolution. Convolution.](/img/tut6/part6-convolution.png)


The resultant image depends on the shape of the Gaussian curve - higher spread means a more blurred image. There’s an alternative called box blur which instead uses 1 over the number of grid pixels as the weight for every pixel, but you end up with slightly uglier ‘boxy’ artifacts along edges with this method.

![Box Blur. Box Blur.](../../assets/0c9e4c8b599e73ba.png)


A nice property of the Gaussian blur (and the box blur, actually) is that it is *linearly separable*. Instead of using an n-by-n grid over each pixel, which requires n^2 operations, we can use a 1-by-n grid and run it across the image horizontally, then use an n-by-1 grid with the same values and run it across the resulting image vertically. With those two passes, you end up with an identical result with only 2n operations. The savings you get going from n^2 to 2n are huge, and the savings only get better when n increases.

![rable Blur (Horizontal). Separable Blur (Horizontal).](../../assets/c491409f76d280f8.png)


![rable Blur (Vertical). Separable Blur (Vertical).](../../assets/4a76bd8111adc822.png)


In theory, the grid would have to be infinitely large (or at least the same size as the image) because the Gaussian curve never touches the axis so pixels far from the center pixel have tiny, but non-zero, weights. In practice, most of those weights are so close to zero that they can be ignored. I found that a grid size of about 6σ works well (and Wikipedia agrees), then I’ll round up to the next pixel so the grid has a center pixel.

# Creating the Blur Effect

Post processing effects in URP are a bit overly complicated in code, but it’s all we have if we need more control than Unity 2022’s Fullscreen Shader Graph. URP Renderer Features are the magic sauce that power post processing effects in Unity, including those in my premium [Snapshot Shaders Pro](https://assetstore.unity.com/packages/vfx/shaders/fullscreen-camera-effects/snapshot-shaders-pro-for-urp-hdrp-160556?aid=1101lfDLn) asset pack. We’ll need three scripts for this effect: `BlurSettings`

holds the shader properties that we can tweak to our liking, `BlurRendererFeature`

handles injecting our custom code into the rendering loop, and `BlurRenderPass`

which deals with creating render textures and actually running a material over the image, then of course there’s the `Blur`

shader file which contains the horizontal and vertical passes. That’s a lot to get through!

## BlurSettings

Start by creating a new C# script by right-clicking and going to *Create -> C# Script*, and name it `BlurSettings`

. First, we’ll need to import a couple of extra namespaces: `UnityEngine.Rendering`

, and `UnityEngine.Rendering.Universal`

, which I hope are self-explanatory. Then, I’ll change the inheritance of the script from `MonoBehavior`

to `VolumeComponent`

and `IPostProcessComponent`

. `VolumeComponent`

is going to make our effect compatible with the volume system whereby we can choose to make the effect run globally or only within a certain collider; without it, the blur would just run constantly with no easy option to turn it off. We’ll need to add a couple of attributes so that we’re able to choose our blur effect in the volume effect drop-down, so add `System.Serializable`

and `VolumeComponentMenu`

with whatever path you want. You can include folders in the name, but I’m going to stick with just “Blur”.

```
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.Universal;
[System.Serializable, VolumeComponentMenu("Blur")]
public class BlurSettings : VolumeComponent, IPostProcessComponent
{
}
```


This script is where we will add our properties that control the behavior of the blur effect. We only need one property to control the shape of the Gaussian curve: a public `ClampedFloatParameter`

named strength. This takes three parameters: the initial float value, and minimum and maximum values. In the Inspector, this will be represented as a slider that can only take on values between the min and max. I’ll set the default as 0 and clamp it between 0 and 10. It’s good practice to set your properties to a neutral default value so you don’t add the effects to your game and suddenly get a jarring visual change. There are other kinds of `Parameter`

type if you need them, `Clamped`

or otherwise, like `IntParameter`

, `ColorParameter`

, `TextureParameter`

and so on. Try and clamp them if you can so you don’t get people trying to set a strength value of 5 million. I’ve also added a `Tooltip`

attribute that will pop up whenever someone hovers over this field in the Inspector.

```
public class BlurSettings : VolumeComponent, IPostProcessComponent
{
[Tooltip("Standard deviation (spread) of the blur. Grid size is approx. 3x larger.")]
public ClampedFloatParameter strength = new ClampedFloatParameter(0.0f, 0.0f, 15.0f);
}
```


The `IPostProcessComponent`

interface requires us to add two methods called `IsActive`

and `IsTileCompatible`

. `IsActive`

is used to determine whether the effect uses valid variable values, so in this case, the effect should run only if the strength is above 0. We also have access to a Boolean called `active`

which is true if the effect is ticked on and false if not, so we’ll include that here.

The other method is called `IsTileCompatible`

, and I’m not entirely sure what it does. Unity says “if it can run on-tile” which I figured might have something to do with tile-based rendering on certain GPUs, but it’s also marked `Obsolete`

for Unity 2023 onwards - if Unity are planning on throwing it in the bin, then it can’t be that important. I just return false and don’t look back, it hasn’t broken anything so far.

```
public class BlurSettings : VolumeComponent, IPostProcessComponent
{
[Tooltip("Standard deviation (spread) of the blur. Grid size is approx. 3x larger.")]
public ClampedFloatParameter strength = new ClampedFloatParameter(0.0f, 0.0f, 15.0f);
public bool IsActive()
{
return (strength.value > 0.0f) && active;
}
public bool IsTileCompatible()
{
return false;
}
}
```


That’s the `BlurSettings`

script done, so we can move on to the largest of the three scripts, `BlurRenderPass`

.

## BlurRenderPass

We need to import the same namespaces as before, and this time, the inherited type is `ScriptableRenderPass`

. This script is the “brain” of our effect, as it handles creating textures and materials, and tells Unity how to apply the effect. This class requires us to override just one method called `Execute`

, but we will optionally also override `Configure`

and `FrameCleanup`

. I’m also going to add my own method called `Setup`

.

This script will require a few variables, all of which can stay private: a `Material`

, which will hold our blur shader, a reference to our `BlurSettings`

, a `RenderTargetIdentifier`

called `source`

, which is basically the screen texture before we apply our shader, a `RenderTargetHandle`

called `blurTex`

, which is an intermediate texture that holds the result of the first of two blur passes, and an `int`

called `blurTexID`

which I’ll explain shortly.

```
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.Universal;
public class BlurRenderPass : ScriptableRenderPass
{
private Material material;
private BlurSettings blurSettings;
private RenderTargetIdentifier source;
private RenderTargetHandle blurTex;
private int blurTexID;
public bool Setup(ScriptableRenderer renderer)
{
}
public override void Configure(CommandBuffer cmd, RenderTextureDescriptor cameraTextureDescriptor)
{
}
public override void Execute(ScriptableRenderContext context, ref RenderingData renderingData)
{
}
public override void FrameCleanup(CommandBuffer cmd)
{
}
}
```


The `Setup`

method comes first. It does some one-time setup for things that need to be ready before `BlurRenderPass`

can do anything, but it needs access to a `ScriptableRenderer`

object, which is the glue that holds together all the features supported by the renderer, the lighting, and the textures output by the camera. Christ, there’s so many types to keep track of with similar names. This isn’t automatically called by Unity, so we will end up calling this method manually later.

In our `Setup`

method, we’ll retrieve the `cameraColorTarget`

from the `renderer`

, which is the camera output texture. We’ll grab a reference to our `BlurSettings`

script from the `VolumeManager`

- if you have several volumes in your scene using a `Blur`

effect, then this `GetComponent`

method gets the correct one. Next, we’ll set the `renderPassEvent`

. Essentially, we can make our Blur effect run at a handful of predetermined points in the rendering loop. For a post-processing effect, like we’re making, you’ll pick either `BeforeRenderingPostProcessing`

or `AfterRenderingPostProcessing`

, which are confusing names because we *are* doing post processing. The `Before`

and `After`

in these names are referring to URP’s already-included post processing effects like `Bloom`

or `Depth of Field`

. I’m choosing `Before`

, but if you’re ever writing an effect and it doesn’t work, swap it to `After`

and that sometimes makes all the scary bugs go away.

Lastly, we’ll create a material to run our shader, but first, we need to check that `blurSettings`

is not null, meaning the camera is inside a volume that contains a Blur effect, and that the effect is active - it has a strength above 0. If so, we’ll find the shader using its name. Obviously, we haven’t written the shader yet, but `PostProcessing/Blur`

is the name I will be using. You might have noticed that the return type of the method is `bool`

, so I’ll return true if we successfully created a material, and false if not.

```
public bool Setup(ScriptableRenderer renderer)
{
source = renderer.cameraColorTarget;
blurSettings = VolumeManager.instance.stack.GetComponent<BlurSettings>();
renderPassEvent = RenderPassEvent.BeforeRenderingPostProcessing;
if (blurSettings != null && blurSettings.IsActive())
{
material = new Material(Shader.Find("PostProcessing/Blur"));
return true;
}
return false;
}
```


Next up is the `Configure`

method override. This gets called each frame just before applying the effect, and we use it to set up any temporary resources required during this frame. It takes in a `CommandBuffer`

and a `RenderTextureDescriptor`

as parameters; the `CommandBuffer`

is a list of instructions for the GPU to carry out, and the `RenderTextureDescriptor`

describes the size of and sort of information stored in a texture, in this case the camera texture. Inside the method, I’ll stop running any code immediately if there’s no valid blur effect. If there is, I’ll create a temporary texture with an ID `_BlurTex`

and exactly the same properties as the camera texture. Lastly, we’ll call `base.Configure`

, which runs whatever code the base `ScriptableRenderPass`

class has in its `Configure`

method.

```
public override void Configure(CommandBuffer cmd, RenderTextureDescriptor cameraTextureDescriptor)
{
if (blurSettings == null || !blurSettings.IsActive())
{
return;
}
blurTexID = Shader.PropertyToID("_BlurTex");
blurTex = new RenderTargetHandle();
blurTex.id = blurTexID;
cmd.GetTemporaryRT(blurTex.id, cameraTextureDescriptor);
base.Configure(cmd, cameraTextureDescriptor);
}
```


Next up we have the `Execute`

method, which has nothing to do with capital punishment - this is the core bit of code across our three classes. This method runs once per frame, and we use it to set up shader properties and apply the shader to the camera texture. It takes a `ScriptableRenderContext`

and a `RenderingData`

as parameters; the `ScriptableRenderContext`

is a conduit for passing our instructions to the renderer, and the `RenderingData`

… it’s sort of in the name, I guess!

Inside the method, I’ll check again that we have valid blur effect. Then, I’ll create a command buffer using `CommandBufferPool.Get`

and pass in a profiler tag named “Blur Post Process” - this identifier is used by the Profiler to track the performance of our code. Next, we need to set up the shader properties that will be used for our effect. Our `BlurSettings`

script dealt with one property: the strength of the effect. From this, we’ll derive two shader properties. If you remember my description of the Gaussian function earlier, I mentioned that a grid size of 6σ works well. I’ll round it up to the next integer value, and then add one if the result is even so that our grid has a central pixel. Then, to set our shader properties, it’s a matter of using the `Set`

methods on the material. There’s a `Set`

method for each type, so for the grid size I’ll use `SetInteger`

with the `_GridSize`

property, and for the spread I’ll use `SetFloat`

with the `_Spread`

property. We haven’t written the shader yet, but those are the property names I’ll be using.

Now we can run the effect over the screen. For that, we use a method called `Blit`

, which takes an input texture that we can read color data from, a texture we’ll write the result to, and optionally, a material to run over the first texture, and also optionally, a number representing which pass inside the material’s shader to use. Our shader will use two passes, so we’re going to `Blit`

from the source texture (the camera texture) to our temporary blur texture using a horizontal blur pass, which has a pass index of 0, then from the blur texture back to the source texture with a vertical blur pass with an index of 1. These `Blit`

commands get added to our command buffer, and to actually get URP to process those commands, we use `context.ExecuteCommandBuffer`

and pass in the command buffer as an argument. After that, we can clear the command buffer and then call `CommandBufferPool.Release`

to clean up resources related to the command buffer, since we’re now done with it for this frame.

```
public override void Execute(ScriptableRenderContext context, ref RenderingData renderingData)
{
if (blurSettings == null || !blurSettings.IsActive())
{
return;
}
CommandBuffer cmd = CommandBufferPool.Get("Blur Post Process");
// Set Blur effect properties.
int gridSize = Mathf.CeilToInt(blurSettings.strength.value * 6.0f);
if (gridSize % 2 == 0)
{
gridSize++;
}
material.SetInteger("_GridSize", gridSize);
material.SetFloat("_Spread", blurSettings.strength.value);
// Execute effect using effect material with two passes.
cmd.Blit(source, blurTex.id, material, 0);
cmd.Blit(blurTex.id, source, material, 1);
context.ExecuteCommandBuffer(cmd);
cmd.Clear();
CommandBufferPool.Release(cmd);
}
```


The only method left is `FrameCleanup`

, which we use to free up any resources we created during this frame. It’s called at the end of the frame. You don’t often need to deal with manual memory management like this in Unity, but be warned that if you don’t clean up things like temporary textures after using them, you may encounter memory leaks and Unity will get upset with you. The only thing we need to free is the temporary `blurTex`

, which we can do with `cmd.ReleaseTemporaryRT`

- we need to pass in the texture’s ID rather than the texture itself. Then we can call `base.FrameCleanup`

to run the default cleanup code.

```
public override void FrameCleanup(CommandBuffer cmd)
{
cmd.ReleaseTemporaryRT(blurTexID);
base.FrameCleanup(cmd);
}
```


And that’s the `BlurRenderPass`

script complete!

## BlurRendererFeature

Now we’ll tackle the third and final script, `BlurRendererFeature`

. This one only needs to import the `UnityEngine.Rendering.Universal`

namespace. The inherited type this time is `ScriptableRendererFeature`

, which needs us to override two methods called `Create`

and `AddRenderPasses`

. Before those, add a variable of type `BlurRenderPass`

to hold our pass.

```
using UnityEngine.Rendering.Universal;
public class BlurRendererFeature : ScriptableRendererFeature
{
BlurRenderPass blurRenderPass;
public override void Create()
{
}
public override void AddRenderPasses(ScriptableRenderer renderer, ref RenderingData renderingData)
{
}
}
```


The `Create`

method deals with creating any passes and other resources your effect requires to work. In our case, we just need to create one `blurRenderPass`

, but you might end up making complex effects with several passes. I’ll also change the `name`

variable to “Blur”, which sets the default name of the Renderer Feature when we add it to our Renderer Features list.

```
public override void Create()
{
blurRenderPass = new BlurRenderPass();
name = "Blur";
}
```


The `AddRenderPasses`

method handles everything to do with inserting passes into the URP rendering loop. It takes a `ScriptableRenderer`

and a `RenderingData`

as parameters - these are both types we’ve seen before. This is also where I’m going to call the `Setup`

method on `BlurRenderPass`

, because this `AddRenderPasses`

method gets called before the `Configure`

and `Execute`

methods on `BlurRenderPass`

. `Setup`

also requires a `ScriptableRenderer`

as a parameter, and we conveniently have one right here. If you remember, `Setup`

returns `true`

if everything got setup successfully and `false`

otherwise, so we’ll check the result with an `if`

statement, and inside the `if`

statement we’ll use `EnqueuePass`

to add `blurRenderPass`

to our `renderer`

.

```
public override void AddRenderPasses(ScriptableRenderer renderer, ref RenderingData renderingData)
{
if (blurRenderPass.Setup(renderer))
{
renderer.EnqueuePass(blurRenderPass);
}
}
```


With that, all the C# scripting is done and we can look at how the shader works.

# The Blur Shader

In the Unity Editor, I’ll create a Resources folder inside my Assets folder, then create a shader inside it via *Create -> Shader -> Unlit Shader*. These presets were created for the built-in pipeline so we won’t actually use the boilerplate code provided, but we need a shader file to work with. I’ll name it `Blur`

. The Resources folder guarantees that anything placed within will be included in a game build, which sometimes won’t happen if you don’t directly reference your shader in any asset contained within a scene. Using `Shader.Find`

doesn’t count as referencing it, so inside the Resources folder it goes.

This shader file has a few key parts: the name of the shader is `PostProcessing/Blur`

, then we have the `Properties`

block which contains all the information we send to the shader and the `SubShader`

that includes most of the code. Inside the `SubShader`

, we have a `Tags`

list, a `HLSLINCLUDE`

block where we write shader code that gets placed inside every shader pass, then after the `HLSLINCLUDE`

block we have the horizontal shader pass, then the vertical shader pass, and that’s it. Here’s the basic code that we’re going to fill in from top to bottom.

```
Shader "PostProcessing/Blur"
{
Properties
{
}
SubShader
{
Tags
{
"RenderType" = "Opaque"
"RenderPipeline" = "UniversalPipeline"
}
HLSLINCLUDE
ENDHLSL
Pass
{
}
Pass
{
}
}
}
```


The `Properties`

block contains three properties: `_MainTex`

is the input texture that gets passed to the shader with the `Blit`

method, then `_Spread`

and `_GridSize`

are the two values we set on the material. I’m going to gloss over some of the shader syntax a bit because I’ve covered it in previous tutorials and there’s a lot to get through, so if you’re completely new to shaders I would recommend reading my [introduction guide to vertex and fragment shaders](https://danielilett.com/2021-04-02-basics-3-shaders-in-urp/), then coming back here.

```
Properties
{
_MainTex("Texture", 2D) = "white" {}
_Spread("Standard Deviation (Spread)", Float) = 0
_GridSize("Grid Size", Integer) = 1
}
```


In the `Tags`

block I’ll set the `RenderType`

to `Opaque`

and the `RenderPipeline`

to `UniversalPipeline`

to prevent the shader being used on other pipelines.

```
Tags
{
"RenderType" = "Opaque"
"RenderPipeline" = "UniversalPipeline"
}
```


The `HLSLINCLUDE`

block will contain everything common to both passes of the blur effect. On top of importing the `Core.hlsl`

shader file and defining the `e`

constant (2.718 and so on), we’ll have the standard `appdata`

and `v2f`

structs plus a basic `vert`

shader. We’ll need to define all of our variables again, including the texel size of `_MainTex`

. Then, I’ll write a `gaussian`

function which will calculate our grid values. This version of the function always assumes the mean of the Gaussian curve is zero.

```
HLSLINCLUDE
#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
#define E 2.71828f
sampler2D _MainTex;
CBUFFER_START(UnityPerMaterial)
float4 _MainTex_TexelSize;
uint _GridSize;
float _Spread;
CBUFFER_END
float gaussian(int x)
{
float sigmaSqu = _Spread * _Spread;
return (1 / sqrt(TWO_PI * sigmaSqu)) * pow(E, -(x * x) / (2 * sigmaSqu));
}
struct appdata
{
float4 positionOS : Position;
float2 uv : TEXCOORD0;
};
struct v2f
{
float4 positionCS : SV_Position;
float2 uv : TEXCOORD0;
};
v2f vert(appdata v)
{
v2f o;
o.positionCS = TransformObjectToHClip(v.positionOS.xyz);
o.uv = v.uv;
return o;
}
ENDHLSL
```


Now we can write our two shader passes. We’ll start with the `Horizontal`

pass by opening up an `HLSLPROGRAM`

block and using #pragma statements to specify the `vert`

function for the vertex shader and the `frag_horizontal`

function (which we need to now write) for the fragment shader.

```
Pass
{
Name "Horizontal"
HLSLPROGRAM
#pragma vertex vert
#pragma fragment frag_horizontal
float4 frag_horizontal (v2f i) : SV_Target
{
}
ENDHLSL
}
```


Inside the function, I’ll define a `color`

variable which will accumulate the weighted color values from each grid pixel, and a `gridSum`

value that will accumulate the weights themselves. Then, I’ll work out the `upper`

and `lower`

bounds for the grid - basically, how many pixels to the left and right I’ll sample based on the grid size.

Now I can loop over each of the pixels, and for each one, I’ll use the `gaussian`

function to calculate the weight, then work out a UV offset from the center pixel and use those new UVs to sample one of the grid pixels, multiply its color by the weight, and update the `color`

and `gridSum`

variables with those values. Once the loop has finished, I’ll divide `color`

by `gridSum`

because sometimes the grid weights do not sum to 1. That `color`

value can then be output by the shader.

```
float4 frag_horizontal (v2f i) : SV_Target
{
float3 col = float3(0.0f, 0.0f, 0.0f);
float gridSum = 0.0f;
int upper = ((_GridSize - 1) / 2);
int lower = -upper;
for (int x = lower; x <= upper; ++x)
{
float gauss = gaussian(x);
gridSum += gauss;
float2 uv = i.uv + float2(_MainTex_TexelSize.x * x, 0.0f);
col += gauss * tex2D(_MainTex, uv).xyz;
}
col /= gridSum;
return float4(col, 1.0f);
}
```


The second pass is basically identical, except the name is now `Vertical`

, the fragment function is now called `frag_vertical`

, and everything that operated in the x-direction now goes in the y-direction - especially keep an eye on the UV offset.

```
Pass
{
Name "Vertical"
HLSLPROGRAM
#pragma vertex vert
#pragma fragment frag_vertical
float4 frag_vertical (v2f i) : SV_Target
{
float3 col = float3(0.0f, 0.0f, 0.0f);
float gridSum = 0.0f;
int upper = ((_GridSize - 1) / 2);
int lower = -upper;
for (int y = lower; y <= upper; ++y)
{
float gauss = gaussian(y);
gridSum += gauss;
float2 uv = i.uv + float2(0.0f, _MainTex_TexelSize.y * y);
col += gauss * tex2D(_MainTex, uv).xyz;
}
col /= gridSum;
return float4(col, 1.0f);
}
ENDHLSL
}
```


That’s the shader complete! Now let’s set up a scene to use everything we’ve created.

# Adding Volumes

First, find your Universal Renderer asset. In a brand new URP project, you will find a few of these inside the *Assets/Settings* folder. My game uses the one named “HighFidelity” by default but yours might be different. At the bottom, click the *Add Renderer Feature* button and find your Blur effect. This step is important - it essentially enables the effect, although we don’t yet have any volumes in the scene which run the effect.

![Add Renderer Feature. Add Renderer Feature.](../../assets/98d32578a2955d15.png)


You can add a volume via *GameObject -> Volume -> Box Volume* (there are other options available). There is no volume profile attached to the volume, so click the *New* button and Unity will create one somewhere in your Assets folder. We can add effects to the volume directly from this Inspector window via the *Add Override* button, so once again, find your Blur effect in this menu and select it. Finally, tick the override option next to the `strength`

setting and increase it to something above 0, then whenever your camera passes through the box volume in either the Scene View of Game View, your screen will blur!

![Add Volume Override. Add Volume Override.](../../assets/59d61ff5d67ca770.png)


Subscribe to my Patreon for perks including early access, your name in the credits of my videos, and bonus access to several premium shader packs!