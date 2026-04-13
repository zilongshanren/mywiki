---
title: Textured Shadows Trick in Unreal Engine
url: https://tomlooman.com/unreal-engine-textured-shadow/
author: Tom Looman
published: '2017-03-12'
source_blog: Tom Looman
source_site: https://www.tomlooman.com/
category: unreal engine
fetched: '2026-04-13'
---

This weekend I stumbled upon a [reddit post](https://www.reddit.com/r/movies/comments/5yvf23/in_disneys_the_princess_and_the_frog_the_shadow/) about Dr. Facilier’s interesting shadow in The Princess and the Frog and it inspired me to experiment with Forward shading in Unreal Engine 4 to re-create a similar effect in real-time shading. OP pointed out that The Shadow Man’s shadow changes the wallpaper his shadow is cast on. A subtle but quite interesting effect!

![](../../assets/8c82460de0dce9ab.jpg)


With Forward rendering enabled we have a different shading pipeline to play with instead of UE4’s default deferred pipeline, the one I was interested in is the LightAttenuation buffer. The exact available data with Epic’s new Forward rendering is still mostly unknown to me, a good reason to try this new shading pipeline as a Sunday tech-doodle!

This trick was made possible due to a graphics binding bug where the LightAttenuationTexture was available in a pass it should not have been. This has since been fixed making this original implementation no longer possible. I have not looked into an alternative method for this trick.

**The result, note the skull texture only rendered within the shadow bounds:**

![](../../assets/75924062c8495c93.gif)


The implementation is really quite basic, I used the LightAttenuationTexture available only in Forward-rendering of the engine to find which part of affected by light. To access this buffer you need to use the Custom-node in the material editor, and apply the following code:

```
return Square(Texture2DSampleLevel(LightAttenuationTexture, LightAttenuationTextureSampler, UV, 0));
```


“UV” is an input parameter (so make sure it’s added to the param list of the custom node) in which we feed the ScreenAlignedUVs node output.

For those interested, I found this snippet in the engine’s shader folder at …/4.14/Engine/Shaders/Common.usf and contains the function GetPerPixelLightAttenuation(float2 UV);

Below is the crude sample of the material used in the GIF:

![](../../assets/07cab2d3d2ae1c28.png)


There is not a whole lot going on, simply blending between the wallpaper and the skull pattern based on the light attenuation value of that pixel is screenspace. The texture samplers use my WorldUVs material function which I’ve posted about some time ago.

**The effect visualized with two-tone instead of textures:**

![](../../assets/0df5c6600feb39c8.jpg)


This LightAttenuationTexture may not be the perfect source for detailed lighting information, but did the trick for this simple effect recreation. Baked light for example needs to sample the lightmap data (as light attenuation is available from dynamic lights only) But this proved good enough for my specific case of the shadowed wallpaper.

## Outlined Shadows

I’ve done multiple blog posts about rendering [outlines in Unreal Engine](https://tomlooman.com/unreal-engine-outline-multi-color-post-process) in the past. So when I had this idea of **outlining shadows** instead of objects, I figured it would be fun to build it as a quick experiment.

To figure out where to draw the outline I use an approach very similar to my prior outline implementation, instead I sample the LightAttenuation buffer instead of the CustomDepth buffer and compare it to the light attenuation value or nearby pixel. This effect does NOT work in Deferred rendering!

![](../../assets/95d89846d9813b73.gif)