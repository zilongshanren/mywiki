---
title: Snapshot Shaders Pro - Scanlines
url: https://danielilett.com/snapshot-shaders-pro/scanlines/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

Renders horizontal scanlines across the screen based on the input texture.

This effect requires the **Scanline Texture** to be set in order to work properly. Examples are provided at **Resources/Textures/ScanlineBasic.png** and **Resources/Textures/ScanlineColor.png**.

![Scanlines](../../assets/3c9a64876330d018.jpg)


# Parameters

**Scanline Texture**- The texture used to denote how scanlines appear. This is typically a very small texture which will be tiled across the screen many times.**Strength**- How noticeable the scanlines are.**Size**- How large the scanlines are.**Scroll Speed**- How quickly the scanlines move across the screen. Set to zero if you want the scanlines to stay stationary.