---
title: Snapshot Shaders Pro - World Scan
url: https://danielilett.com/snapshot-shaders-pro/world-scan/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

The World Scan effect creates a scanline that enamates from a point in space and travels across the scene. The scanline is overlaid onto the original scene contents.

This effect requires the **Overlay Ramp Tex** to be set in order to work properly.

![World Scanner](../../assets/9dd54492812151ae.jpg)


# Parameters

**Scan Origin**- The world space origin of the scan.**Scan Distance**- How far, in world space units, that the scan has travelled from the origin.**Scan Width**- The distance, in world space units, that the scan is applied over.**Overlay Ramp Tex**- An x-by-1 ramp texture representing the scene color.**Overlay Color**- An additional HDR-enabled tint color applied to the scan.