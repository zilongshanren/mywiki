---
title: 'Opinion: CRT Emulation For Pixel Art'
url: https://www.gamedeveloper.com/art/opinion-crt-emulation-for-pixel-art
author: Stuart Riffle
published: '2011-07-21'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

[In this reprinted [#altdevblogaday](http://altdevblogaday.com/)-opinion piece, EA veteran and Pure Energy Games founder Stuart Riffle examines various approaches you can take when emulating CRT idiosyncrasies with your game's pixel art for a retro feel.] A good way to get an authentic look for retro-pixel art is to simulate the distortion caused by encoding the image into an NTSC signal, decoding it again (as a TV would), and projecting it onto a virtual CRT. This gives you natural-looking artifacts, like fringing and color bleeding. Console emulators do this sometimes, and if you're old enough to have actually played games on a CRT TV, it really helps with the sense of immersion. This post gives a quick overview of the process, in case you'd like to try it for yourself. All of these steps are texture operations performed by pixel shaders.

We start by encoding the low resolution input image as an NTSC signal. Each input line is converted into voltage over time, in the same format an NTSC signal would be sent across a wire (except for the sync and color pulse stuff).

A 'cable reflection' shader smears the signal out a little to the right. I'm not sure how much it looks like cable reflection, but it does kind of evoke the streaking artifacts you see on some old TVs.

The luma is split out of the signal, and then used in the NTSC decoding process. This is also where the standard OSD parameters (brightness, contrast, sharpness, etc) are applied. Now our image is RGB again.

The image is projected onto a curved tube. This step also takes care of tracing the scan lines and applying the phosphor pattern.

The phosphors from the previous frame are decayed, and the new values are accumulated. This allows for ghosting of moving images.

A standard post-processing stack is applied (bloom, glare, and tone mapping). This give users a taste of the eye-burning glow produced by a real CRT. (Do you remember when staying up late to play games caused physical pain? Kids these days are soft.)


These techniques can be used to make the copyrighted hedgehogs look even more dashing:![Tube simulator example Tube simulator example](../../assets/c1a13c8c43b86ecc.img)

![Moire artifacts Moire artifacts](../../assets/c09230f8e81dbb03.img)

![Tuning crosstalk Tuning crosstalk](../../assets/d735d5d9a54dcdf2.img)

![Phosphor patterns at different scales Phosphor patterns at different scales](http://gamesetwatch.com/TubePhosphor.bmp?width=1280&auto=webp&quality=80&disable=upscale)

![Effect tuning parameters Effect tuning parameters](http://gamesetwatch.com/TubeTuningSmall.bmp?width=1280&auto=webp&quality=80&disable=upscale)

[pureenergygames.com](http://pureenergygames.com) and subscribe to the RSS feed! [This piece was reprinted from [#AltDevBlogADay](http://altdevblogaday.com/), a shared blog initiative started by [@mike_acton](http://www.twitter.com/mike_acton) devoted to giving game developers of all disciplines a place to motivate each other to write regularly about their personal game development passions.]