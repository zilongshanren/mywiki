---
title: Animated Dotted Outline Shader in Unity
url: https://lindenreidblog.com/2017/12/24/animated-dotted-outline-shader-in-unity/
author: View all posts by Linden Reid
published: '2017-12-24'
source_blog: Linden Reid
source_site: https://lindenreid.wordpress.com
category: graphics
fetched: '2026-04-13'
---

Earlier, I wrote a [tutorial on how to create a cel shader with an outline effect](https://lindenreid.wordpress.com/2017/12/19/cel-shader-with-outline-in-unity/). For the sake of not repeating that explanation, refer to that tutorial to learn how to draw the basic outline.

You can apply this outline effect to any kind of lighting or other shader properties, since it’s in its own pass.

Here’s the final code for you to reference:


## Dotted Outline

The dotted shader is achieved with two techniques:

- Using a
**distance field**to skip pixels when drawing the outline **Scrolling**the ‘position’ of each pixel with Time to animate

So, let’s say we’ve already got our shader drawing the outline. We can leave the regular lighting & texture pass alone for this shader. We’re going to focus completely on the **fragment shader** of the outline pass.

First, let’s learn how to draw the lines.

If you’re unfamiliar with distance fields, the basic premise is that you can determine what to render for a pixel based on its **distance** from a particular point. In this shader, we **discard every other set of X pixels** in a **radius** around a point. If we take away the regular lighting pass, and only draw the outline pass, the curve to the lines becomes more apparent:

![lines](../../assets/9e3d515b3a0f40ba.png)


Here’s what the fragment shader code to break up the outline looks like:

// _OutlineDot = width of solid portion // _OutlineDot2 = width of transparent portion float skip = sin(_OutlineDot*abs(distance(_SourcePos.xy, pos))) + _OutlineDot2; // clip stops rendering a pixel if 'skip' is negative clip(skip); return _OutlineColor;

Let’s break this down.

- We measure the distance of every pixel from _SourcePos.xy with the call distance(_SourcePos.xy, pos).
- We then take the sin of the absolute value of that distance, which oscillates between negative and positive values.
- We use _OutlineDot and _OutlineDot2 (lazy names, I know) to modify the frequency of the negative and positive values.
- Then, the call to clip(skip) will discard any pixels where the value of skip is negative.
- Finally, we return the basic, flat _OutlineColor for every pixel that wasn’t discarded.

So that’s how we get the dotted outline! Try doing that before moving on to animation.

Here’s the animation code:

float2 pos = input.pos.xy + _Time * _OutlineSpeed;

This is quite a bit simpler.

- We get the current position with input.pos.xy (this was passed in from the vertex shader)
- We multiply the position by _Time and _OutlineSpeed in order to translate the position over time.

Here’s the full fragment shader together:

// if you want to remove the animation, remove "+ _Time * _OutlineSpeed" float2 pos = input.pos.xy + _Time * _OutlineSpeed; // _OutlineDot = width of solid portion // _OutlineDot2 = width of transparent portion float skip = sin(_OutlineDot*abs(distance(_SourcePos.xy, pos))) + _OutlineDot2; // stops rendering a pixel if 'skip' is negative clip(skip); return _OutlineColor;


## Extra Reference


Ramp shader used for lighting:

![ramp](../../assets/080ee2f85c7c2419.png)


Tuning used in the header gif:

![dottedMaterialProperties](../../assets/4c58f9f850c51253.png)


### Fin

Here’s a link to the [final code for the dotted outline shader](https://github.com/thelindseyreid/Unity-Shader-Tutorials/blob/master/Assets/Materials/Shaders/celEffectsDottedOutline.shader), including a pass for cel-shaded lighting and a pass for shadows.

I hope y’all found this useful! If y’all have any questions about writing shaders in Unity, I’m happy to share as much as I know. I’m not an expert, but I’m always willing to help other indie devs 🙂

Good luck,

Lindsey Reid [@so_good_lin](https://twitter.com/so_good_lin)


The outline works but the rest of the model turns orange.

LikeLike

Can you please make a tutorial on the fog shader like the one in Alto’s Odyssey.

LikeLike