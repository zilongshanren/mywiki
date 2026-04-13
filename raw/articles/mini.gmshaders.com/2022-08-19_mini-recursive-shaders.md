---
title: 'Mini: Recursive shaders'
url: https://mini.gmshaders.com/p/gm-shaders-mini-recursive-shaders-1308459
author: Xor
published: '2022-08-19'
source_blog: GM Shaders
source_site: https://mini.gmshaders.com
category: graphics
fetched: '2026-04-13'
---

# Mini: Recursive shaders

### How to layer multiple shader passes together for more advanced effects

Good afternoon. Today's mini tutorial is about recursive shader effects as a way of layering multiple passes of shaders together.

## Recursive Shader Usage

You might be wondering why you'd want to apply a shader effect over and over again. Obviously, you wouldn't need to apply a grayscale effect multiple times, but it can be incredibly powerful with blur shaders.

Say you want to do a 9x9 pixel blur. That is 81 texture samples, which is a lot to ask for, especially on low-end hardware. A slightly better method would be to apply a 5x5 blur 2 times.

## Feedback shader

You could imagine much more significant gains with even larger blurs (17x17 = 289 samples versus 25 samples in 4 iterations). [There are](https://github.com/XorDev/Dual-Kawase) even faster methods, but it's good general advice to ask yourself if your effect would be better split into multiple passes. This may also apply to outlines or even glow effects, so it's not just for blur shaders.

## Recursive Setup

So, we know how it can be handy, but how do you set it up?

The naive approach is to create a bunch of surfaces for each pass of the shader. So, if you have a 4-pass effect, you might create 4 surfaces (A, B, C, D).

You'll draw whatever you want to surface A with a shader, then draw surface A to surface B with a shader, then B to C, and C to D.

This definitely will work, but it can use a lot of VRAM with every pass (especially if you have [surface depth enabled](https://twitter.com/XorDev/status/1423396882798231563)). I've written bloom effects that work best with 10 passes, and I don't want to have 10 full-resolution surfaces lying around. So the trick I like to use is known as "Ping-Pong" buffers (in our case, surfaces). All you need is two surfaces, no matter how many shader passes, and you simply draw A to B and B to A as many times as necessary.

Definitely, something that every graphics coder should be aware of

## Feedback Shaders

Sometimes, you'll want to feed the last frame into the shader to produce the next frame. This is called feedback and can produce some wild results!

Here's one of my own [feedback shaders](https://twitter.com/XorDev/status/1514074470075580420):

To create effects like this in GM, you'll need a Boolean variable to toggle which surface is drawing to which. So maybe A to B in the first frame, then B to A the next, and alternate every frame like this

`surface_swap = !surface_swap;`


Then you can use variables like this to alternate:

`var _surf1 = surface_swap ? surface_a : surface_b;`


`var _surf2 = surface_swap ? surface_b : surface_a;`


And when you set the surface, you'll use _surf1 and always draw _surf2. This little code handles all the rest for you!

## Conclusion

So, in conclusion, it's useful to recognize when multiple shader passes would produce faster or higher quality results and, in those cases, try using ping-pong surfaces. It's easy to set up and can be very powerful!

## Bonus!

First, if you somehow missed it, @kraifpatrik released a super powerful 3D global illumination system for GameMaker Studio 2! It's completely open-source, and I did a whole [video about it here](https://youtu.be/_vCrYIlyFwU).

Second, I just released a halftone effect for GameMaker!

You can claim it for free on Itch.

Thanks!

-@XorDev