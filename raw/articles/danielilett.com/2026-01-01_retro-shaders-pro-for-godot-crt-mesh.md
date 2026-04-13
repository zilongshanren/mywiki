---
title: Retro Shaders Pro for Godot - CRT (Mesh)
url: https://danielilett.com/retro-shaders-godot/crt-mesh/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

A variant of the CRT Post Process effect which can instead be applied to a regular mesh in your scene. It may be useful for creating effects such as a realtime CCTV view in your game, and I recommend attaching a detailed texture to the material for this effect.

![CRT Filter with VHS tracking artifacts](../../assets/34fe9c6380d59e47.gif)


# Retro Properties

## Color & Resolution

**Base Color**- The albedo color of the object.**Base Texture**- An albedo texture which can be used to apply more color detail than**Base Color**alone.**Pixel Size**- An integer value representing how pixelated the image becomes.

## Barrel Distortion

**Distortion Strength**- Controls how strongly the edges of the screen warp inwards to form the shape of a CRT glass screen.**Distortion Smoothing**- How much blending there is between the areas ‘inside’ and ‘outside’ the screen. Leave as 0 for a hard border.**Background Color**- Color of the areas outside the distorted CRT screen shape.

## RGB Subpixels & Scanlines

**Subpixel Texture**- Texture to use for the RGB subpixel effect. All pixels on the screen are multiplied by this texture such that the red, green, and blue screen colors appear separate to each other.- An example of a texture to use for this is contained in
*Retro Shaders Pro/Resources/Textures/RGBTexture.png*.

- An example of a texture to use for this is contained in
**Subpixel Strength**- How strongly the RGB subpixel effect is applied.**Scanline Texture**- Texture to use for the scanline effect. All pixels on the screen are multiplied by this texture such that scanlines appear scrolling over the image.- An example of a texture to use for this is contained in
*Retro Shaders Pro/Resources/Textures/ScanlineTexture.png*.

- An example of a texture to use for this is contained in
**Scanline Strength**- How strongly the scanline effect is applied.**Scanline/RGB Size**- Larger values make the scanlines (and RGB subpixels) appear larger on-screen.**Scanline Scroll Speed**- How quickly the scanline texture scrolls over the screen.

## VHS Artifacts

**Random Wear**- Adds small, noisy UV distortions horizontally to simulate the fuzzy look common with old VHS tapes.**Aberration Strength**- How strongly chromatic aberration (color channel separation) is applied at the screen edges.**Use VHS Tracking**- Should the shader apply the following VHS tracking artifacts?**Tracking Texture**- A control texture for tracking artifacts.- This should be an x-by-1 image.
- The red channel controls the strength of the tracking UV offsets.
- The green channel controls the presence of tracking lines overlaid onto the screen.
- An example of a texture to use for this is contained in
*Retro Shaders Pro/Resources/Textures/TrackingRamp.png*.

**Tracking Size**- How ‘zoomed in’ the tracking ramp is when scrolling over the screen.**Tracking Strength**- How strongly the tracking ramp red channel offsets the UVs of the screen horizontally.**Tracking Speed**- How quickly the tracking ramp scrolls across the screen. Use negative values to scroll upwards.**Tracking Jitter**- A random offset applied to the scrolling to make it appear jittery.**Tracking Color Damage**- Cycle the chrominance of the image slightly to look like the tape is damaged. The screen is converted to YIQ color space, and the offset is applied to the I and Q channels.**Tracking Lines Threshold**- A threshold for tracking lines to appear on screen. Higher values mean fewer lines.**Tracking Lines Color**- The color of the tracking lines, where the alpha channel acts as a global multiplier on the tracking line strength.

## Color Adjustments

**Tint Color**- A global tint applied to the entire CRT screen effect.**Brightness**- Global multiplier for the image colors before some effects are applied. A value of 1 preserves the image as-is.**Contrast**- Forces differences in colors to become more obvious. A value of 1 preserves the image as-is.