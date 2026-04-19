---
title: Local UVs for Sprites in Sprite Sheet/Atlas
url: https://www.cyanilux.com/tutorials/sprite-local-uv/
author: Cyanilux
published: '2024-03-13'
source_blog: Cyanilux Shader Tutorials
source_site: https://www.cyanilux.com/
category: graphics
fetched: '2026-04-19'
---

# Local UVs for Sprites in Sprite Sheet/Atlas

## Intro

Some shader effects can rely on having a 0-1 UV coord across the sprite, but this breaks if the sprite is part of a larger sprite sheet (i.e. Sprite Mode set to Multiple) or if sprites are automatically packed via a Sprite Atlas asset.

With those, the UV coords of the sprite mesh is a smaller section of the whole 0-1 range, in order to display only that sprite from the larger texture. For example, here is the UV coordinates for a sprite sheet that I’ve made (used in [this game jam project from 2022](https://cyanilux.itch.io/dungeon))

But we may also want coordinates specific to each sprite for certain effects…

The first section below results in coordinates that behave exactly like if the sprite mode was “Single” and not packed, and should work in all pipelines/versions. But it requires adding a C# Script to the sprite object.

There is also some later sections providing alternatives, intended more for URP. But these have some slightly buggy behaviours (as explained in notice boxes)

- The
[second method](https://www.cyanilux.com#object-pos)uses object space positions, offset by the pivot point (intended for Unity 2023.1+) - The
[third method](https://www.cyanilux.com#world-aligned)remaps world position coordinates based on bounds data (provided as of Unity 2022.2+). This creates some similar 0-1 coords across the sprite, except they stay aligned to the world and do not rotate or flip with the sprite. Could be useful.

## Remapping UV

In order to convert to this “local UV” (0-1 coordinates across the sprite), we need to know the location and size of the sprite in the sheet/atlas texture.

We’ll need to pass that into the shader/material by using the following C# script (applied to GameObject containing the SpriteRenderer).

- For URP 2022 and earlier, and Built-in RP, have
`usePropertyBlock = true`

to avoid breaking dynamic batching for Unity 2022 and earlier. - For URP 2023+ you may want
`usePropertyBlock = false`

, as sprites can use SRP Batcher instead. - (For HDRP may need to experiment and check Frame Debugger - I don’t know if it handles sprite batching in the same way)

|
|

In the shader, we can use this `_UVRemap`

Vector4 property to remap the mesh UV coordinates.

#### Shader Code (CG/HLSL) :

```
// In Properties :
_UVRemap ("Sprite UV Rect", Vector) = (0, 0, 1, 1)
// In Global HLSL Scope / UnityPerMaterial CBUFFER :
float4 _UVRemap;
// In Vertex/Fragment Shader :
float2 spriteRectPos = _UVRemap.xy;
float2 spriteRectSize = _UVRemap.zw;
float2 localUV = (IN.uv - spriteRectPos) / spriteRectSize;
```


#### Shader Graph :

## Small optimisation (optional)

You could also change the script to set `uvRemap`

to this instead :

|
|

Then in the shader/graph :

`IN.uv * _UVRemap.zw + _UVRemap.xy`

**Multiply**and**Add**(or just**Tiling And Offset**which does the same thing)

In the compiled shader I think this would end up a single instruction (MAD)

## Object Position

As of Unity 2023.1, sprites seem to use the SRP Batcher in URP (during play mode at least), so an easy method to obtain relative coordinates is by using the **Position** node, set to **Object** space. You may also want to **Swizzle** this down to a Vector2 (using “xy” in the text field).

- While easy, this method can lead to some odd results if sprites use dynamic batching instead (“Draw Dynamic” under frame debugger). That occurs in the Built-in RP and URP prior to 2023, and even in URP 2023+ while not in play mode (kinda annoying, but works if you can ignore that)

The **Position** has a value of **(0,0)** at the pivot of the sprite. So for sprites using a **Center** pivot (the default), you’d want to **Add** **(0.5, 0.5)** to this to obtain the usual 0-1 coordinates like the UVs of a quad. If you use a different pivot can hardcode a different value, or if you use multiple pivots, could use a **Vector2 property** instead and create multiple materials with the values you need.

## World-Aligned Local UV

As of Unity 2022.2, bounding box info from the renderer is now automatically passed to the shader (in URP and HDRP at least). It passes this into `unity_RendererBounds_Min`

and `unity_RendererBounds_Max`

- part of the UnityPerDraw cbuffer in [UnityInput.hlsl](https://github.com/Unity-Technologies/Graphics/blob/master/Packages/com.unity.render-pipelines.universal/ShaderLibrary/UnityInput.hlsl))

This won’t work for Built-in or older versions, (unless you were to manually pass `Renderer.bounds.min and .max`

into your own shader properties via a C# script)

- Appears to be a very odd bug where the
**first sprite**(with shader using bounds) rendered after a**Tilemap**will contain incorrect bounds info. So can render incorrectly for that sprite.- Only affects the sprite if rendered as “Dynamic Draw” (in frame debugger). Using the bounds also breaks dynamic batches (so each of these draw calls will be a single sprite)
- SRP batches are fine! (Requires URP 2023.1+. But they also only srp-batch during play mode, not during edit mode, so not ideal…)


We can use this bounds info to remap the world position (of vertices/fragments). As mentioned in the intro the resulting coordinates stay aligned to the world so do not rotate or flip with the sprite. (0, 0) is always towards the bottom left of the screen and (1, 1) towards the top right.

#### Shader Graph :

Use the **World Bounds Min** and **World Bounds Max** outputs from the **Object** node into an **Inverse Lerp**, with **T** set to **Position** node (**World** space)

Sadly this seems to break node previews as the default values for those results in a division by zero, so the additional group here with a **Comparison** and **Branch** prevents that, by using the **UV** when the **Bounds Size** is 0.

I’ve also selected that **Branch** node, and under the **Node Settings** tab changed it to preview as **2D**.

Note that we also assume sprites are aligned to **XY** axis. If aligned to a different axis, may need to change the swizzle (e.g. use XZ instead) or if not axis-aligned, apply rotation to Vector3 before truncating to Vector2.

#### Shader Code :

For HLSL this would translate to something like :

```
// In Vertex Shader :
VertexPositionInputs positionInputs = GetVertexPositionInputs(IN.positionOS.xyz);
float3 positionWS = positionInputs.positionWS;
float3 worldBoundsMin = GetCameraRelativePositionWS(unity_RendererBounds_Min.xyz);
float3 worldBoundsMax = GetCameraRelativePositionWS(unity_RendererBounds_Max.xyz);
// note these "unity_RendererBounds_" variables are part of the
// UnityPerDraw cbuffer defined in the ShaderLibrary files
// Inverse Lerp
float3 positionBS = (positionWS - worldBoundsMin) / (worldBoundsMax - worldBoundsMin);
// "Bounds Space"
OUT.localUV = positionBS.xy;
```


## Thanks for reading! 😊

If you find this post helpful, please consider sharing it with others / on socials

Donations are also **greatly** appreciated! 🙏✨

(Keeps this site free from ads and allows me to focus more on tutorials)