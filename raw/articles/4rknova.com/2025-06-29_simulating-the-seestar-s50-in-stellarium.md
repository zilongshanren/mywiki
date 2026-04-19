---
title: Simulating the Seestar S50 in Stellarium
url: https://www.4rknova.com/blog/2025/06/29/seestar-s50-stellarium
author: Nikolaos Papadopoulos
published: '2025-06-29'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

The **Seestar S50** smart telescope can be accurately simulated in **Stellarium** by configuring custom sensor and telescope profiles. Stellarium’s *Oculars* plugin allows for precise visualization of the field of view (FOV), making it a valuable tool for astrophotography planning and target framing.

Below are the specifications for both the standard **1x1 mode** and the expanded **2x2 mosaic mode** used by the Seestar S50.

# Sensor Settings

| Mode | Resolution (px) | Chip Width (mm) | Chip Height (mm) | Binning | Rotation Angle |
|---|---|---|---|---|---|
| Seestar 1x1 | 1080 x 1920 | 3.20 | 5.60 | 1 x 1 | 0° |
| Seestar 2x2 | 2160 x 3840 | 6.26 | 11.14 | 1 x 1 | 0° |

# Telescope Settings

| Parameter | Value |
|---|---|
| Name | Seestar |
| Focal Length | 250.00 mm |
| Diameter | 50.00 mm |

# Configuration

To set up the Seestar S50 profile in Stellarium:

- Launch
**Stellarium**and activate the*Oculars*plugin in the settings menu, if not already enabled. - Open the Oculars configuration panel by clicking the wrench icon.
- In the
**Sensors**tab, add two sensor profiles using the parameters provided above for 1x1 and 2x2 modes. - Navigate to the
**Telescopes**tab and create a new telescope entry with the Seestar’s specifications. - Once saved, the Seestar profiles can be selected to preview the FOV when observing celestial objects in Stellarium.

This setup provides an accurate simulation environment for planning imaging sessions with the Seestar S50.

![Seestar s50 in Stellarium](../../assets/835aeb5f5028eac9.jpg)