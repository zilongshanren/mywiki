---
title: Snapshot Shaders Pro - Neon (Fancy)
url: https://danielilett.com/snapshot-shaders-pro/neon-fancy/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

An improved neon effect where the edge detection parameters can be altered to use image colours, depth or normals (or a combination).

![Neon](../../assets/26892346a884687d.jpg)


# Parameters

**Color Sensitivity**- The threshold for colour-based edge detection.**Color Strength**- The strength of colour-based edges, where detected.**Depth Sensitivity**- The threshold for depth-based edge detection.**Depth Strength**- The strength of depth-based edges, where detected.**Normal Sensitivity**- The threshold for normal-based edge detection.**Normal Strength**- The strength of normal-based edges, where detected.**Depth Threshold**- Pixels past this depth (normalised between 0 and 1) will not be edge-detected.**Saturation Floor**- Any pixel with a saturation below this (in HSL colour space) gets clamped to this value.**Lightness Floor**- Any pixel with a lightness below this (in HSL colour space) gets clamped to this value.