---
title: 'A Subtle shader: making an invisible thing visible'
url: https://www.gamedeveloper.com/art/a-subtle-shader-making-an-invisible-thing-visible
author: Mauricio Perin
published: '2015-12-14'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# A Subtle shader: making an invisible thing visible

How one game artist learned a bit of shader coding with the Unity community and created a custom solution for an invisible character. **Shader code included**!

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

When we fisrt started working on [Tsar Project](http://visdev.com.br/tag/tsar-project/), the game that would eventually evolve into [Qasri al-Wasat](http://qasirgame.com), one of the few things the team knew for certain was that our protagonist, called Subtle, would be invisible. And for that we needed a visual way to convey this to players, but without compromising playabily and navigation with well, a fully invisible character in the middle of the screen. It was then that I learned about shaders.

## A newbie approach to shading

First things first: working with Unity is super great because of the community. When we began working on Qasir I had absolutely know clue about shader coding. No clue about programming whatsoever to be honest. So it all started with [Unity’s shader documentation](http://docs.unity3d.com/Manual/Shaders.html) and lurking on the [Unity Answers database](http://answers.unity3d.com/). I still very much recommend those as good starting points — even though I wouldn't be any surprised if somebody with more programming experience (not to say ANY) would recommend something else.

## When it started to get shady

After deciding the kind of effect we needed to achieve (I had something between [Ghost in the Shell’s cloaking](http://qasirgame.com/content/kusanagi.gif) and that [Mortal Kombat Movie's Reptile](http://qasirgame.com/content/reptile.jpg) in mind) the best shader to start from seemed to be the Stained Glass/Heat Wave available in many variations throughout Unity’s forums. The fine tuning consisted of adding highlights and shadow to the bump map based distortion.

## Three shades of invisible

The final result consists of a greyscale bump map, a slider to fine tune the amount of distortion, a black texture with highlights and a white texture with shadings. Here are the three components, rendered as separated unlit materials, side by side with the combined result:

![Liquid Liquid](../../assets/5ce36819365241a8.gif)

![Venom Venom](../../assets/f2acd28546db56a6.gif)

![Venom Venom](../../assets/c0efc3186641c4ce.gif)

![Sublte Sublte](http://31.media.tumblr.com/675601ad85c0c8b2a1f02affede5c170/tumblr_inline_nz3wx4Hb0k1s2rynl_500.gif?width=1280&auto=webp&quality=80&disable=upscale)


I’ve made all the textures with alpha here, just so they’d work properly as standalones, but the first one is grey around the character, the second black and the third white. In the case of Qasir, with the use of sprite based animation, every individual texture is actually a 2048px sprite map, but the shader sould also work for other kinds of 2D and 3D techniques.

You can get the .shader file here:

http://visdev.com.br/ftp/qasir/Glass-Subtle_Custom.shader

And if you have any questions please come say hello on [twitter](https://twitter.com/maperns)!

Cheers!

PS: By the way, the individual textures used in the game are named Liquid, Venom and Solidus. And in case you’re wondering, the texture used when Subtle is visible is named Solid.