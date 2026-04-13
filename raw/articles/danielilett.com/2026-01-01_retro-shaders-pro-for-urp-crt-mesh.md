---
title: Retro Shaders Pro for URP - CRT (Mesh)
url: https://danielilett.com/retro-shaders-pro/crt-mesh/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

A variant of the CRT Post Process effect which can instead be applied to a regular mesh in your scene. It may be useful for creating effects such as a realtime CCTV view in your game, and I recommend attaching a detailed texture to the material for this effect.

![CRT Filter with VHS tracking artifacts](../../assets/34fe9c6380d59e47.gif)


# Parameters

## Basic Properties

**Base Color**- The albedo color of the object.**Base Texture**- An albedo texture which can be used to apply more color detail than**Base Color**alone.**Pixel Size**- An integer value representing how pixelated the image becomes.**Force Point Filtering**- Use nearest-neighbor filtering when upscaling the pixelated image back to full screen size. Disable to use bilinear filtering instead.

## Barrel Distortion

**Distortion Strength**- Controls how strongly the edges of the screen warp inwards to form the shape of a CRT glass screen.**Distortion Smoothing**- How much blending there is between the areas ‘inside’ and ‘outside’ the screen. Leave as 0 for a hard border.**Background Color**- Color of the areas outside the distorted CRT screen shape.

## RGB Subpixels & Scanlines

**RGB Subpixel Texture**- Texture to use for the RGB subpixel effect. All pixels on the screen are multiplied by this texture such that the red, green, and blue screen colors appear separate to each other.- An example of a texture to use for this is contained in
*Retro Shaders Pro/Resources/Textures/RGBTexture.png*.

- An example of a texture to use for this is contained in
**RGB Subpixel Strength**- How strongly the RGB subpixel effect is applied.**Scanline Texture**- Texture to use for the scanline effect. All pixels on the screen are multiplied by this texture such that scanlines appear scrolling over the image.- An example of a texture to use for this is contained in
*Retro Shaders Pro/Resources/Textures/ScanlineTexture.png*.

- An example of a texture to use for this is contained in
**Scanline Strength**- How strongly the scanline effect is applied.**Scanline/RGB Size**- Larger values make the scanlines (and RGB subpixels) appear larger on-screen.**Scanline Scroll Speed**- How quickly the scanline texture scrolls over the screen.

## VHS Artifacts

**Random Wear**- Adds small, noisy UV distortions horizontally to simulate the fuzzy look common with old VHS tapes.**Aberration Strength**- How strongly chromatic aberration (color channel separation) is applied at the screen edges.**Tracking Texture**- A control texture for tracking artifacts.- This should be an x-by-1 image.
- The red channel controls the strength of the tracking UV offsets.
- The green channel controls the presence of tracking lines overlaid onto the screen.
- An example of a texture to use for this is contained in
*Retro Shaders Pro/Resources/Textures/TrackingRamp.png*.

**Tracking Size**- How ‘zoomed in’ the tracking ramp is when scrolling over the screen.**Tracking Strength**- How strongly the tracking ramp red channel offsets the UVs of the screen horizontally.**Tracking Speed**- How quickly the tracking ramp scrolls across the screen. Use negative values to scroll upwards.**Tracking Jitter**- A random offset applied to the scrolling to make it appear jittery.**Tracking Color Damage**- Cycle the chrominance of the image slightly to look like the tape is damaged. The screen is converted to YIQ color space, and the offset is applied to the I and Q channels.**Tracking Lines Threshold**- A threshold for tracking lines to appear on screen. Higher values mean fewer lines.**Tracking Lines Color**- The color of the tracking lines, where the alpha channel acts as a global multiplier on the tracking line strength.

## Color Adjustments

**Tint Color**- A global tint applied to the entire CRT screen effect.**Brightness**- Global multiplier for the image colors before some effects are applied. A value of 1 preserves the image as-is.**Contrast**- Forces differences in colors to become more obvious. A value of 1 preserves the image as-is.**Color Ramp Mode**- Should the shader apply a color mapping to approximate the color palette of a retro console or computer? This setting comes with several presets.**Color Ramp Texture**- The ramp texture used to map screen input colors to new shader output colors.

# Color Ramp Presets

The color ramp functionality of the CRT effect only *approximates* the color palettes found in retro consoles and computers. For example, the SNES had a 15-bit RGB palette, but it could only display 256 colors simultaneously; this color mapper only implements the *palette restrictions*, not the simultaneous color restrictions, and some consoles only use a crude approximation.

The included presets implement the following:

*None*– Don’t apply any mapping.*Game and Watch*– A 1-bit monochrome effect.*Game Boy*– Restricts the color to a 2-bit greyscale, tinted green.*Game Boy Advance*– Uses 5 bits per channel (15 total bits, 32,768 total colors).*Nintendo DS*– Uses 6 bits per channel (18 total bits, 262,144 total colors).*Greyscale*– Converts the image to greyscale based on pixel luminance.*NES*– Crude approximation, 3 available values for each channel (27 total colors).*SNES*– Same as GBA: uses 5 bits per channel (15 total bits, 32,768 total colors).*MSX2*– Uses 3 bits for red and green, 2 bits for blue (8 total bits, 256 total colors).*IBM PS/2*– Uses 5 bits for red and blue, 6 bits for green (16 total bits, 65,536 total colors).*Amstrad CPC*– Uses 3 levels for each channel (27 total colors).*Teletext*– Uses 1 bit per channel (3 total bits, 8 total eye-destroying colors).*ZX Spectrum*– Uses one bit per channel, plus additional ‘intensity’ bit (4 total bits, 16 total colors).*Sega Master System*– Uses 2 bits per channel (6 total bits, 64 total colors).*Sega Genesis*– Uses 3 bits per channel (9 total bits, 512 total colors).*Sega Game Gear*– Uses 4 bits per channel (12 total bits, 4096 colors).