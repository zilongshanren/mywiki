---
title: Graphics Programming weekly - Issue 109 — December 1, 2019
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-109/
author: Jendrik Illner
published: '2019-12-01'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- fork of the PerfDoc performance layer to detect performance issues on PowerVR hardware
- the article provides an overview of performance issues that the layer can detect and possible improvements

![](../../assets/7b8a97bbbeab8f4b.jpg)


- the article provides an overview of the lighting model used by SculptrVR
- designed for the hardware constraints of the occulus quest
- it’s based on the Phong lighting and supports clay, metal, and glowing materials

![](../../assets/6d810b8b704ac83b.jpg)


- the article provides an easy to understand overview of Variable Rate Shading
- shows what quality and performance can be expected with different modes

![](../../assets/e5871fbcc52f8c78.png)


- the tutorial explains the ddx and ddy shader functions
- provides a visualization of its effects
- shows how to use fwidth to antialias a cutoff transition from a gradient

![](../../assets/04c2afbaf4fe3fe5.png)


- the Unity tutorial shows how to use transparency to create a look through the object
- later uses a grab pass (copy of the screen buffer before a draw call starts) to implement a glass appearance material

![](../../assets/96ea926ee76cc0c5.png)


- part 2 of the shader glass material shader tutorial with Unity
- extends the standard lighting model to feature stringer rim lighting, stronger highlights, and a more cartoony overall look

![](../../assets/23e85a1e21268c4d.png)


- this Unity tutorial shows how to use the scriptable rendering pipeline to implement up to 4 directional lights
- the shading model is based on the default physically-based unity BRDF
- additionally shows how to deal with transparency and implement a custom material UI

![](../../assets/bd3ea34ea7a21faf.jpg)


- the article provides a brief overview of the YUV/YCbCr colorspace and a few complications with it
- then show how to use the ycbcr_sampler_conversion to sample YUV textures from a shader more efficiently

![](../../assets/059bab589a983ae8.png)


- brief unity tutorial that shows how to implement effects that are based on the player position
- such as flowers spawning around the player, or stones moving to form a path in front of the player

![](../../assets/62ae01be96947c8e.png)


- the article shows the matrices between XYZ colors and sRGB colors
- these numbers vary from the ones found in Real-Time Rendering and Physically Based Rendering
- the author explains how he derived the values and why they are correct

![](../../assets/48d7da9d33560dcf.png)

Thanks to [Graham Wihlidal](https://www.wihlidal.com) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.