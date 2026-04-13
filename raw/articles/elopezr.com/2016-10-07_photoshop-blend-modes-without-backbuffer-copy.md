---
title: Photoshop Blend Modes Without Backbuffer Copy
url: https://www.elopezr.com/photoshop-blend-modes-in-unity/
author: Redorav
published: '2016-10-07'
source_blog: The Code Corsair
source_site: http://www.elopezr.com
category: game programming
fetched: '2026-04-13'
---

For the past couple of weeks, I have been trying to replicate the Photoshop blend modes in Unity. It is no easy task; despite the advances of modern graphics hardware, the blend unit still resists being programmable and will probably remain fixed for some time. Some OpenGL ES extensions implement this functionality, but most hardware and APIs don’t. So what options do we have?

1) Backbuffer copy

A common approach is to copy the entire backbuffer before doing the blending. This is what Unity does. After that it’s trivial to implement any blending you want in shader code. The obvious problem with this approach is that you need to do a full backbuffer copy before you do the blending operation. There are certainly some possible optimizations like only copying what you need to a smaller texture of some sort, but it gets complicated once you have many objects using blend modes. You can also do just a single backbuffer copy and re-use it, but then you can’t stack different blended objects on top of each other. In Unity, this is done via a GrabPass. It is the approach used by the Blend Modes plugin.

2) Leveraging the Blend Unit

Modern GPUs have a little unit at the end of the graphics pipeline called the Output Merger. It’s the hardware responsible for getting the output of a pixel shader and blending it with the backbuffer. It’s not programmable, as to do so has quite a lot of complications (you can read about it here) so current GPUs don’t have one.

The blend mode formulas were obtained here and here. Use it as reference to compare it with what I provide. There are many other sources. One thing I’ve noticed is that provided formulas often neglect to mention that Photoshop actually uses modified formulas and clamps quantities in a different manner, especially when dealing with alpha. Gimp does the same. This is my experience recreating the Photoshop blend modes exclusively using a combination of blend unit and shaders. The first few blend modes are simple, but as we progress we’ll have to resort to more and more tricks to get what we want.

Two caveats before we start. First off, Photoshop blend modes do their blending in sRGB space, which means if you do them in linear space they will look wrong. Generally this isn’t a problem, but due to the amount of trickery we’ll be doing for these blend modes, many of the values need to go beyond the 0 – 1 range, which means we need an HDR buffer to do the calculations. Unity can do this by setting the camera to be HDR in the camera settings, and also setting Gamma for the color space in the Player Settings. This is clearly undesirable if you do your lighting calculations in linear space. In a custom engine you would probably be able to set this up in a different manner (to allow for linear lighting).

If you want to try the code out while you read ahead, download it here.

A) Darken

Formula

min(SrcColor, DstColor)

Shader Output

1

color.rgb=lerp(float3(1,1,1),color.rgb,color.a);

Blend Unit

Min(SrcColor · One, DstColor · One)

As alpha approaches 0, we need to tend the minimum value to DstColor, by forcing SrcColor to be the maximum possible color float3(1, 1, 1)

B) Multiply

Formula

SrcColor · DstColor

Shader Output

1

color.rgb=color.rgb *color.a;

Blend Unit

SrcColor · DstColor+ DstColor · OneMinusSrcAlpha

C) Color Burn

Formula

1 – (1 – DstColor) / SrcColor

Shader Output

1

color.rgb=1.0-(1.0/max(0.001,color.rgb *color.a+1.0-color.a));// max to avoid infinity

You can see discrepancies between the Photoshop and the Unity version in the alpha blending, especially at the edges.

H) Linear Dodge

Formula

SrcColor + DstColor

Shader Output

1

color.rgb=color.rgb;

Blend Unit

SrcColor · SrcAlpha+ DstColor · One

This one also exhibits color “bleeding” at the edges. To be honest I prefer the one to the right just because it looks more “alive” than the other one. Same goes for Color Dodge. However this limits the 1-to-1 mapping to Photoshop/Gimp.

All of the previous blend modes have simple formulas and one way or another they can be implemented via a few instructions and the correct blending mode. However, some blend modes have conditional behavior or complex expressions (complex relative to the blend unit) that need a bit of re-thinking. Most of the blend modes that follow needed a two-pass approach (using the Pass syntax in your shader). Two-pass shaders in Unity have a limitation in that the two passes aren’t guaranteed to render one after the other for a given material. These blend modes rely on the previous pass, so you’ll get weird artifacts. If you have two overlapping sprites (as in a 2D game, such as our use case) the sorting will be undefined. The workaround around this is to move the Order in Layer property to force them to sort properly.

How I ended up with Overlay requires an explanation. We take the original formula and approximate via a linear blend:

We simplify as much as we can and end up with this

The only way I found to get DstColor · DstColor is to isolate the term and do it in two passes, therefore we extract the same factor in both sides:

However this formula doesn’t take alpha into account. We still need to linearly interpolate this big formula with alpha, where an alpha of 0 should return Dst. Therefore

If we include the last term into the original formula, we can still do it in 2 passes. We need to be careful to clamp the alpha value with max(0.001, a) because we’re now potentially dividing by 0. The final formula is

For the Soft Light we apply a very similar reasoning to Overlay, which in the end leads us to Pegtop’s formula. Both are different from Photoshop’s version in that they don’t have discontinuities. This one also has a darker fringe when alpha blending.

Hard Light has a very delicate hack that allows it to work and blend with alpha. In the first pass we divide by some magic number, only to multiply it back in the second pass! That’s because when alpha is 0 it needs to result in DstColor, but it was resulting in black.

[29/04/2019] Roman in the comments below reports that he couldn’t get Linear Light to work using the proposed method and found an alternative. His reasoning is that the output color becomes negative which gets clamped. I’m not sure what changed in Unity between when I did it and now but perhaps it relied on having an RGBA16F render target which may have changed since then to some other HDR format such as RG11B10F or RGB10A2 which do not support negative values. His alternative becomes (using RevSub as the blend op):

Hi Roman, thanks for your input! I should have made note of what version of Unity I was using to know whether something changed since then that makes it not work anymore. In any case I’ve added a note to the Linear Light explaining what I think is the problem and your solution.

Amazing technique. Thanks a lot for sharing! However I encountered a weird behaviour of Unity. In some cases (I guess this happens during rendering into a render texture) it calls each shader pass twice. Obviously it breaks the majority of blend modes (not to mention it affects the performance). Here are some extra details https://forum.unity.com/threads/shader-pass-called-twice.1112719/ Have you encountered this ugliness?

I wonder if there are alternatives for all blend modes to support the HDR format that does not support negative value such as R11G11B10. I couldn’t make it out for Overlay, SoftLight, and Hardlight. Others semes to be possible.

Linear Light didn’t work for me in game view, only in scene view. I had to change the calculation this way

Blend options:

BlendOp RevSub

Blend One One

Code:

color.rgb = -(2 * color.rgb – 1);

Probably it was because color becomes negative and unity clamps the output of frag shader.

Hi Roman, thanks for your input! I should have made note of what version of Unity I was using to know whether something changed since then that makes it not work anymore. In any case I’ve added a note to the Linear Light explaining what I think is the problem and your solution.

Amazing technique. Thanks a lot for sharing!

However I encountered a weird behaviour of Unity. In some cases (I guess this happens during rendering into a render texture) it calls each shader pass twice. Obviously it breaks the majority of blend modes (not to mention it affects the performance).

Here are some extra details https://forum.unity.com/threads/shader-pass-called-twice.1112719/

Have you encountered this ugliness?

Never mind. Turned out, it’s a bug in Unity Frame Debugger.

I wonder if there are alternatives for all blend modes to support the HDR format that does not support negative value such as R11G11B10.

I couldn’t make it out for Overlay, SoftLight, and Hardlight. Others semes to be possible.