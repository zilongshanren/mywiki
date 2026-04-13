---
title: Snapshot Shaders 2 - Blur
url: https://danielilett.com/snapshot-shaders-2/blur/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

A multi-featured blur effect with several modes:

**Gaussian**- Blur each pixel according to a Gaussian distribution, where pixels further away from the center pixel have a lower contribution to the center pixel output.**Box**- Blur each pixel by taking an unweighted average of the nearby pixel colors.**Radial**- Blur each pixel by taking a Gaussian-weighted average of a line of pixels radiating from the center of the image.**Light Streaks**- Blur pixels horizontally after taking a threshold of image brightness. Works especially well with HDR images, where some objects use high-intensity emissive colors or the scene contains extremely bright lights.

# Parameters

Note that some parameters only appear under some blur modes.

**Blur Mode**- Which blurring algorithm to use. Choose between*Gaussian*,*Box*,*Radial*, and*Light Streaks*.**Strength**- How strongly the image is blurred. This impacts the size of the blurring kernel, so each effect is less efficient when strength is increased.**Blur Step Size**- For*Gaussian*,*Box*, and*Light Streaks*, this adds gaps in the blurring kernel, resulting in a “sparse” blur where far-away pixels may be considered without sacrificing performance. For*Radial*, this impacts the gap between each texture sample.**Luminance Threshold**- For*Light Streaks*, this is the brightness level which a pixel must exceed to produce streaks. For a non-HDR image, a completely white pixel has brightness 1.