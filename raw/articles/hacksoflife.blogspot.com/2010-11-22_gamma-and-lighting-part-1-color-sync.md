---
title: 'Gamma and Lighting Part 1: Color Sync'
url: http://hacksoflife.blogspot.com/2010/11/gamma-and-lighting-part-1-color-sync.html
author: Benjamin Supnik
published: '2010-11-22'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[This FAQ](http://www.poynton.com/PDFs/GammaFAQ.pdf)explains Gamma infinitely better than I possibly can. I suggest reading it about eight times.

24-bit Color Spaces Are Pretty Much Never Linear

A color space defines the meaning of RGB colors (that is, triplets of 8-bit or more codes). How red is red? That's what your color space tells you. And the first thing I must point out is: no color space you'd ever use on an 8-bit-per-channel (24-bit color) display is ever going to have a linear mapping between RGB values and luminance. Why not? This

[Wikipedia](http://en.wikipedia.org/wiki/SRGB)article on sRGB puts it best:

This nonlinear conversion means that sRGB is a reasonably efficient use of the values in an integer-based image file to display human-discernible light levels.Here's what's going on:

- Our perception of color is non-linear. It's roughly logarithmic. This means we're more discerning of light level changes at low light levels. That's good - we can see in the dark, sort of, or at least this improves our dynamic range of light perception.
- 256 levels of gray isn't a lot, so it's important that the levels be spread out evenly in terms of what humans perceive. Otherwise we'd run out of distinct gray levels and see banding.
- Therefore, to make 24-bit images look good, pretty much every color space including sRGB is radically different from linear
[luminance](http://en.wikipedia.org/wiki/Luminance)levels.

Part of the confusion over gamma correction is that CRTs have non-linear response by nature of their electronics. People assume that this is bad and that gamma correction curves make the RGB->luminance response linear. In fact, that response is actually useful, and that's why the gamma correction curves on a computer typically undo some of the non-linear response. For example, Macs used to bring the gamma curve down to 1.8 (from 2.5 for a CRT) but not all the way down to 1.0. As mentioned above, if we really had linear response between our RGB colors and luminance, we would need more than 8 bits per channel.

Consistent Color

If we are going to develop a simulator that renders using OpenGL onto a PC or Mac, we're going to work in a color space, probably with 24-bit color most of the time. (We might use higher bit depths in advanced rendering modes, but we can't afford to store our entire texture set in a higher res. Heck, it's expensive to even turn off texture compression!)

So the important thing is that color is maintained consistently through the authoring pipeline to the end user. In practice that means:

Artists need to have their monitors correctly calibrated. If the artist's monitor isn't showing enough red, the artist paints everything to be too red, and the final results look Mars-tacular. So the artist needs good "monitoring."

The color space needs to be tracked through the entire production process. Whether this happens by simply declaring a global color space for the entire pipeline or by tagging assets, we need to make sure that red keeps meaning the same red, or that if we change it, we record that we've changed it and correctly adjust the image.

When working with PNG, we try to record the gamma curve on the PNG file. We encourage our artists to work entirely in sRGB.

The graphics engine needs to not trash the color on read-in. Similar to the pipeline, we need to either not mess up the colors, or track any change in color space. In X-Plane's space, X-Plane will try to run in approximately the color space of the end user's machine, so X-Plane's texture loader will change the color space of textures at load time.

The graphics engine needs to cope with a user whose display is atypical (or not). Finally, if the user's display is not in the same color space as the production pipeline, the engine needs to adjust its output. (Or not adjust its output and expect the user to fix it locally.) In X-plane's case we do this by using the user's machine's gamma curve and correcting images at load time.

This is not the best solution for color accuracy; it would be better to keep the images in their saved color space and convert color in-shader (where we have floating point instead of 8-bits per channel). Historically X-Plane does the cheap conversion to save fill rate. We may some day change this.


If all of these steps are taken, the end user should see textures just as the art team authored them. Before we had step four in X-Plane, PC users used to report that X-Plane was "too dark" because their monitor's color response wasn't the same as our art team's (who were using Macs). Now they report that X-Plane is too dark because it's dark. :-)

In my

[next post](http://hacksoflife.blogspot.com/2010/11/gamma-and-lighting-part-2-working-in.html)I'll discuss the relationship between non-linear color spaces (that work well in 24-bit color) and 3-d lighting models.

## No comments:

## Post a Comment