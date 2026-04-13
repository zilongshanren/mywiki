---
title: Snapshot Shaders 2 - Silhouette
url: https://danielilett.com/snapshot-shaders-2/silhouette/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

Draws each pixel of the screen differently based on its distance from the camera by blending between two colors or using a color ramp.

# Parameters

**Enabled**- When ticked, the effect will render.**Use Texture Ramp**- When ticked, the effect will provide a Unity color gradient which you can edit, and will create a texture and gradient sub-asset on your volume profile. Removing the**Silhouette**effect from your volume profile will destroy those sub-assets.**Texture Ramp**- The texture being used for the ramp (this setting is not editable).**Near Color**- When the texture ramp is not used, this is the color of objects at the camera’s near clip plane.**Far Color**- When the texture ramp is not used, this is the color of obejcts at the camera’s far clip plane.**Power Ramp**- A power curve applied to the image before mapping colors. Values below 1 will bias the image towards the far clip plane color, and values above 1 will bias the image towards the near clip plane color.