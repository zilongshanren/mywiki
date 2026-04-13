---
title: BC7 optimal solid-color blocks
url: https://fgiesen.wordpress.com/2024/11/03/bc7-optimal-solid-color-blocks/
published: '2024-11-03'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# BC7 optimal solid-color blocks

That’s right, it’s another texture compression blog post! I’ll keep it short. By “solid-color block”, I mean a 4×4 block of pixels that all have the same color. ASTC has a dedicated encoding for these (“void-extent blocks”), BC7 does not. Therefore we have an 8-bit RGBA input color and want to figure out how to best encode that color with the encoding options we have. (The reason I’m writing this up now is because it came up in a private conversation.)

In BC1/3, hitting a single color exactly is not always possible, and we have the added complication of the decoder being under-specified. BC7 has neither problem. If we look at our options in [table 109](https://registry.khronos.org/DataFormat/specs/1.3/dataformat.1.3.html#table-bptcmodes) of the Khronos data format spec, we see that mode 5 stores color endpoints with 7 bits of precision per channel and alpha endpoints with a full 8 bits, so it’s a very solid candidate for getting our 8-bit colors through unharmed.

The alpha portion is trivial: we can send our alpha value as the first endpoint and just use index 0 for the alpha portion (mode 5 is one of the BC7 modes that code RGB and A separately, similar to BC3), which leaves the colors. Can we use the color interpolation to turn our 7 endpoint bits per channel into an effective 8?

We have 2 color index bits per pixel. Indices 0 and 3 are not useful for us, they return the dequantized endpoint value, and those are 7 bits, so that only gives us 128 out of 256 possible options for each color channel. Index 1 is interpolated between the two at a 21/64 fraction; index 2 is symmetric (exactly symmetric in BC7, unlike the situation in BC1), i.e. it’s the same as using index 1 with the two endpoints swapped, and therefore doesn’t give us any new options over just using index 1. That means we only need to consider the case where all index values are 1: if the value we need in a color channel happens to be one of the 128 values we can represent directly, we just set both endpoints to that value, otherwise we want select a pair of endpoints so that the value we actually want is between them, using that 21/64 interpolation factor (subject to the BC7 rounding rules).

For BC1, at this point, we would usually build a table where we search for ideal endpoint pairs for every possible target color. For BC7, we can do the same thing, but it turns out we don’t even need a table. Specifically, if we build that table (breaking ties to favor pairs that lie closer together) and look at it for a bit, it becomes quickly clear that we can not only hit each value in [0,255] exactly, but there’s a very simple endpoint pair that works:

```
// Determine e0, e1 such that (BC7 interpolation formula)
// target == (43*expand7(e0) + 21*expand7(e1) + 32) >> 6
// where expand7(x) = (x << 1) | (x >> 6)
e0 = target >> 1
e1 = ((target < 128) ? (target + 1) : (target - 1)) >> 1
```


And that’s it. Do this for each of the R, G, B channels of the input color, and set all the color indices to 1. As noted earlier, the A channel is trivial since we just get to send a 8-bit value there to begin with, so we just send it as one of the endpoints and leave all alpha index bits at 0.

This is exact and the encoding we’ve used in all our shipping BC7 encoders, regular and with rate-distortion optimization both. Often there are many other possible encodings using the other modes, especially for particularly easy cases like all-white or all-black. In our experiments it didn’t particularly matter which encoding is used, so we always use the above. The one thing that does matter is that whatever choice you make should be consistent, since solid-color blocks frequently occur in runs.