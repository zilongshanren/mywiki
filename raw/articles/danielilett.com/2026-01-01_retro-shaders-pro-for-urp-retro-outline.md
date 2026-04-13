---
title: Retro Shaders Pro for URP - Retro Outline
url: https://danielilett.com/retro-shaders-pro/retro-outline/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

The Retro Outline effect uses the Inverted Hull method to render quick and cheap outlines on an object, with support for vertex snapping.

To use this effect, you’ll need to attach a secondary material to your object. This may not function properly with objects which already use multiple materials due to having several submeshes.

![Outlines](../../assets/b7c5a9d08972520b.gif)


# Properties

**Base Color**- Main albedo color of the object, i.e. the color when the object is fully lit.**Thickness**- How far the outline expands from the object’s surface, in world space units.**Snaps Per Unit**- How many points the vertices of the mesh will snap to within one Unity unit (a meter). Higher values result in a smoother appearance.