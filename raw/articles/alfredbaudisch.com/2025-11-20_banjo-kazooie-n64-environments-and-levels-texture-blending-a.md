---
title: 'Banjo-Kazooie (N64) environments and levels: texture blending and vertex color
  usage'
url: https://alfredbaudisch.com/experiment-logs/banjo-kazooie-n64-environments-and-levels-texture-blending-and-vertex-color-usage/
published: '2025-11-20'
source_blog: Alfred Reinold Baudisch
source_site: https://alfredbaudisch.com
category: game programming
fetched: '2026-04-13'
---

Banjo-Kazooie from the Nintendo 64 had environment and terrain details with blended textures (it is also called [decal blending](https://tcrf.net/Prerelease:Banjo-Kazooie/Banjo_Kazoo#Technology) in some sources):

This contrasts with Super Mario 64 where there was a clear separation between each texture:

Banjo Kazooie environments and levels also faked light, shadow and ambient occlusion with vertex colors:

![](../../assets/f3e9596fca02eaf5.jpeg)


![](../../assets/f3e9596fca02eaf5.jpeg)

![](../../assets/de4e6ef6820e5035.jpeg)


![](../../assets/de4e6ef6820e5035.jpeg)

## How did they achieve texture blending?

In Banjo Kazooie, surfaces might have two texture channels, and the blending factor between them is decided by the vertex color alpha.

When disabling vertex colors from the same scene from the first screenshot, this is what the scene looks like:

![](../../assets/cfb51de52736b2a5.jpeg)


![](../../assets/cfb51de52736b2a5.jpeg)

[noclip.website](https://noclip.website/#bk/01;ShareData=ASKuP9oEUGUFA+H9u%5E1eWmP;%7BQUSUaUnOqPUms%7BKV%5Eky%5DUgFD+UOsHx9h_gu+%5E) allows inspecting the vertex color alpha. This is what it looks like for the same scene:

Now for a comparison of everything side by side. Notice how the vertex alpha blends the farm plot texture and the terrain texture:

## Vertex Colors: details, fake light, shadow and ambient occlusion

An inspection of the vertex colors reveals the grass color and the yellow path, as well faked lights, shadows and ambient occlusion (again, thanks to [noclip.website](https://noclip.website/#bk/72;ShareData=ALEeIUY6e5UPE*j97~Pz=t?(UPz5V6UV%5EM%5ET*,P/V!jc?Uc!lp8%5DOC1UsDbWV%5B)):

In a closed environment, this is what the vertex color looks like:

## Textures

Banjo Kazooie makes use of all the Nintendo 64's [texture capabilities](https://n64squid.com/homebrew/n64-sdk/textures/image-formats/) and [formats](https://youtu.be/xwls5SpNn1s?si=Y7lcHdTwm1x2xFzb&t=103), but from my quick observations, the majority of textures used in the game's environments are:

- 32×32 (32-bit)
- 64×64 (16 colors)
- 32×64

In order to show more details, it also makes heavy usage of multi-segment 64×64 textures:

![](../../assets/ea7fbfe963cd9370.png)


![](../../assets/ea7fbfe963cd9370.png)

There's also the usage of noise and alpha textures. If we go back again to the first screenshot example, the game uses a 32×32 noise texture for most of Spiral Mountain:

And then it makes heavy use of vertex colors to shape the path:

![](../../assets/f38b8e9b9aa151d3.png)


![](../../assets/f38b8e9b9aa151d3.png)

[In the next post](https://alfredbaudisch.com/experiment-logs/how-to-make-a-banjo-kazooie-n64-style-terrain-material-in-blender-blended-textures-with-vertex-colors/), I show how to create environments like this with Blender, replicating the same techniques.