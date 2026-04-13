---
title: sRGB, Pre-Multiplied Alpha, and Compression
url: http://hacksoflife.blogspot.com/2022/06/srgb-pre-multiplied-alpha-and.html
author: Benjamin Supnik
published: '2022-06-11'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

How do sRGB color-space textures (especially compressed ones) interact with blending? First, let's define some terms:

An image is "sRGB encoded" if the linear colors have been remapped using the sRGB encoding. This encoding is meant for 8-bit storage of the textures and normalized colors from 0.0 to 1.0. The "win" of sRGB encoding is that it uses more of our precious 8 bits on the dark side of the 0..1 distribution, and humans have weird non-linear vision where we see more detail in that range.

Thus sRGB "spends our bits where they are needed" and limits banding artifacts. If we just viewed an 8-bit color ramp from 0 to 1 linearly, we'd see stripes in the darks and perceive a smooth color wash in the hilights.

Alpha values are always considered linear, e.g. 50% is 50% and is stored as 127 (or maybe 128, consult your IHV?) in an 8-bit texture. But how that alpha is applied depends on the color space where blending is performed.

- If we decode all of our sRGB textures to linear values (stored in more than 8 bits) and then blend in this linear space, we have "linear blending" (sometimes called "gamma-correct" blending - the terminology is confusing no matter how you slice it). With linear blending, translucent surfaces blend the way light blends - a mix of red and green will make a nice bright yellow. Most game engines now work this way, it's pretty much mandatory for HDR (because we're not in a 0..1 range, we can't be in sRGB) and it makes lighting effects look good.
- If we stay in the 8-bit sRGB color space and just blend there, we get "sRGB blending". Between red and green we'll see a sort of dark mustard color and perceive a loss of light energy. Lighting effects blended in sRGB look terrible, but sometimes artists want sRGB blending. The two reasons I've heard from my art team are (1) "that's what Photoshop does" and (2) they are trying to simulate
*partial coverage*(e.g. this surface has rusted paint and so half of the visible pixel area is not showing the paint) and blending in a perceptual space makes the coverage feel right.

- You can save computing power - not exciting for today's GPUs, but back when NeXT first demonstrated workstations with real-time alpha compositing on the CPU (in integer of coarse), premultiplication was critical for cutting ALU by removing half the multiplies from the blending equation.
- Premultiplied alpha can be filtered (e.g. two samples can be blended together) without any artifacts. The black under clear pixels (because they are multiplied with 0) is the correct thing to blend into a neighboring opaque pixel to make it "more transparent" - the math Just Works™. With non-premultiplied textures, the color behind clear pixels appears in intermediate samples - tool chains must make sure to "stuff" those clear texels with nearby colors.

### Pre-Multiplication and sRGB

- Decode our colors to linear (and use more than eight bits to do the following intermediate calculations).
- Multiply the alpha value by the linear color.
- Re-encode the resulting darkened color back to sRGB.

## No comments:

## Post a Comment