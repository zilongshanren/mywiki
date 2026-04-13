---
title: Dual depth buffering for translucency rendering
url: https://interplayoflight.wordpress.com/2013/07/16/dual-depth-buffering-for-transluncency-rendering/
author: Kostas Anagnostou
published: '2013-07-16'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

A nice and cheap technique to [approximate translucency](http://www.slideshare.net/colinbb/colin-barrebrisebois-gdc-2011-approximating-translucency-for-a-fast-cheap-and-convincing-subsurfacescattering-look-7170855) was presented some time ago at GDC. The original algorithm depended on calculating the “thickness” of the model offline and baking it in a texture (or maybe vertices). Dynamically calculating thickness is often more appealing though since, as in reality, the perceived thickness of an object depends on the view point (or the light’s viewpoint) and also it is easier to capture the thickness of varying volumetric bodies such as smoke and hair.

An easy way to dynamically calculate thickness is render the same scene twice store the backfacing triangles’ depth in one buffer and the frontfacing ones’ in another and taking the difference of the values per pixel (implementing two-layer depth peeling in essence). This method works well but it has the disadvantage of rendering the scene at least one extra time.

Looking for ways to improve dynamic thickness calculation, I came across a dual depth buffering technique in ShaderX6 (“Computing Per-Pixel Object Thickness in a Single Render Pass” by Christopher Oat and Thorsten Scheuermann) which manages to calculate the thickness of an object/volume in one pass. The main idea behind this technique is to turn culling off, enable alpha blending by setting the source and destination blend to One and the blend operation to Min and store depth in the Red channel and 1-depth in the Green channel. That way we can calculate the thickness of an object in the main pass as thickness = (1 – Green) – Red. The depth can be either linear or perspectively divided (by w), although the latter will make the calculated thickness vary according to distance to the camera.

The following screenshots demonstrate this. The “whiter” the image the thicker it is. We can see that the thickness varies depending on the viewpoint (you can see that on the torso and the head for example)

This technique works nicely for calculating the thickness of volumetric bodies such as smoke and hair, but not that well for solid objects with large depth complexity as it tends to overestimate the thickness. You can see this in the above images (the leaves in front of the statue are very white) and the following couple of images demonstrate this problem in practice.

The model is rendered with the [“fake” translucency effect](http://www.slideshare.net/colinbb/colin-barrebrisebois-gdc-2011-approximating-translucency-for-a-fast-cheap-and-convincing-subsurfacescattering-look-7170855) mentioned above and by calculating the thickness dynamically with a dual depth buffer. We also placed a light source behind the statue. Viewing the statue from the front it looks ok and we can see the light propagating through the model at less thick areas (like the arm). If we rotate the statue so as to place the leaves between the body and the light we can see them through the statue (due to the overestimation of thickness it absorbs more light than it should and this areas appear darker).

This method is clearly not ideal for solid, complex, objects but we can modify slightly and improve it. Ideally I would like to know the thickness of the first solid part of the model as the ray travels from the camera into the scene.

So instead of storing (depth, 1-depth) in the thickness rendertarget for all rendered pixels I make a distinction between front facing the back facing samples and store the depth as such:

if ( frontfacing ) { return float4( depth, 1, 0, 1); } else { return float4( 1, depth, 0, 1); }

The blending mode remains the same (Min). This way I get the distance of the first front facing and the first backfacing triangle sample along the view ray and calculating the thickness is a matter of subtracting them: thickness = Green – Red.

The following two images demonstrate the effect:

The overall effect is the same as previously but now the leaves are no longer visible through the body of the statue since they are not taken into account when calculating the thickness at the specific pixels.

In summary, dual depth buffering is a nice technique to calculate the thickness of volumetric bodies and simple solid objects and with a slight modification it can be used to render more complicated models as well.