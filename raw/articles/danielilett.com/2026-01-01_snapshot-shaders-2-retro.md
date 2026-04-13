---
title: Snapshot Shaders 2 - Retro
url: https://danielilett.com/snapshot-shaders-2/retro/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

A range of retro graphics in the style of old videogame consoles:

**Game Boy**- Quantizes the image based on luminance and applies four configurable colors to those luminance bands.**SNES (Posterize)**- Quantizes individual color channels with individual bit depths (the SNES used different values in different circumstances, up to 8).

# Parameters

**Enabled**- When ticked, the effect will render.**Drawing Mode**- Which algorithm to use to draw the screen. Choose between*Game Boy*and*SNES (Posterize)*.**Power Ramp**- Applies a power scaler to each color channel prior to performing any color transformations. Values higher than one will darken the image, while values lower than 1 will brighten it.

## Game Boy

**Darkest Color**- Color to apply to the darkest luminance band.**Dark Color**- Color to apply to the second darkest luminance band.**Light Color**- Color to apply to the second lightest luminance band.**Lightest Color**- Color to apply to the lightest luminance band.

## SNES (Posterize)

**Red Levels**- How many quantization levels to apply to the red color channel.**Green Levels**- How many quantization levels to apply to the green color channel.**Blue Levels**- How many quantization levels to apply to the blue color channel.