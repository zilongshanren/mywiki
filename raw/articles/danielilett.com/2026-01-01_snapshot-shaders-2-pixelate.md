---
title: Snapshot Shaders 2 - Pixelate
url: https://danielilett.com/snapshot-shaders-2/pixelate/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

Reduces the screen resolution, with an option to use bilinear or nearest-neighbor filtering.

# Parameters

**Downsample Size**- The factor by which to downsample the image. If this is set to 8, then a ‘pixel’ in the new image will take up 8 pixels on the screen.**Use Point Filtering**- When enabled, the shader uses crisp nearest-neighbor filtering. Otherwise, the shader will use bilinear filtering, resulting in a blurry image.**Expand Mask**- If you are using a mask, you can expand it slightly to ensure the entire mask contents fall within the blur. Enabling this setting will cause some minor elements outside of the mask boundaries to become pixelated, and is slightly slower, but usually looks nicer. If this setting is turned off, you will find parts of an image where some edges of the original object are still visible and not pixelated, due to unavoidable pixelation artefacts.