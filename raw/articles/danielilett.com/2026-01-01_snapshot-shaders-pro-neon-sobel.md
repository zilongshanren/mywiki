---
title: Snapshot Shaders Pro - Neon (Sobel)
url: https://danielilett.com/snapshot-shaders-pro/neon-sobel/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

Runs a Sobel edge-detection filter over the image. Then, it saturates and lightens the original pixel color up to a threshold and multiples by the edge-detect image.

![Sobel Neon](../../assets/efce29f90f2cf957.jpg)


# Parameters

**Saturation Floor**- Any pixel with a saturation below this (in HSL colour space) gets clamped to this value.**Lightness Floor**- Any pixel with a lightness below this (in HSL colour space) gets clamped to this value.