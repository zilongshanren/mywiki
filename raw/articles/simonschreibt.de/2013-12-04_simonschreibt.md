---
title: Simonschreibt.
url: https://simonschreibt.de/gat/handmade-normal-maps/
author: Simon
published: '2013-12-04'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

If a 3D artist would play a [memory game](https://www.google.de/search?q=memory+game&tbm=isch&tbo=u&source=univ&sa=X&ei=9KuLUuKlDMnJsgbtoYGQCw&ved=0CF0QsAQ&biw=661&bih=777) and he would uncover a card representing a **normal map** and another one showing a **high poly** model he would state that this is the perfect pair. It’s just totally common that normal maps get created out of a 3D mesh (or sometimes the [NVidia Photoshop Plugin](https://developer.nvidia.com/nvidia-texture-tools-adobe-photoshop)). Except from some exceptions it’s not the best idea to manually paint in a normal map since every pixel is a tiny light vector and it’s hard to imagine how the resulting shading will look like.

But sometimes people don’t think too much about issues or problems and just do it. And sometimes the result is just stunning. In my eyes, [this tool-project](http://spritelamp.com/) is a great example:

As you might know, a normal map stores one light vector per pixel and uses the R, B and G channel to store the X, Y and Z values of the vector. [Sprite Lamp](http://spritelamp.com/) enables you, to paint the channels of the normal map separately and (more important) see the results quickly.

Imagine you would have to model a highpoly-retro-character like that to generate the normal map out of 3D data… If you’re interested in this tool, feel free to checkout its [Kickstarter page](http://www.kickstarter.com/projects/finnmorgan/sprite-lamp-dynamic-lighting-for-2d-art).

Thanks to [Anna](https://twitter.com/iirelu) for bringing us another example for normal mapped pixel art on environments:

By the way, this whole thing reminds me of a very interesting tutorial of[ how to create a normal map from the real world with a camera](http://www.zarria.net/nrmphoto/nrmphoto.html). This is pretty much the same idea of creating the different channels by hand (but using a camera instead of painting them):

These examples showed me once more: Sometimes you need to think out of the box, stop worrying and just try it out.

Wow – the”make your own normal map” tutorial is both fantastic and deceptively simple! I never would’ve thought of using light sources like that to generate the textures required.

Also, given as you’re a designer who has experience with these things rather than an Internet denizen who may only knows about this stuff and thus likely has no practical knowledge on what they’ve read, I wanted to ask you something regarding Sprite Lamp. A fellow on Reddit had this to say about Sprite Lamp:

I suppose what I’m asking is: is the fellow I quoted right in your opinion? Is Sprite Lamp not really worth it given how (supposedly) simple it is to convert the four images used for Sprite Lamp into a normal map?

Sorry for the late reply, i had to check if my comment is valid and doesn’t contain wrong information :D

So as far as i know Sprite Lamp is basically a viewer which updates the source textures every time they changed. This means you can use whatever painting software you want but Sprite Lamp is the viewer which let you quickly see the result of your painting work. Also it contains ways to tweak your normal map and to create e.g. a depth map.

As far a i understand you can do this with other tools too. You could paint in Photoshop, tweak in CrazyBump and preview in Unity. But maybe the workflow will be easier with Sprite lamp. We’ll see :)

Yes, the guy saying that you don’t need to buy any third party programs is correct. You can take any image and use the bass relief filter on it from various programs, setting the lighting to the angles you need and pasting those into the R and G channels to achieve the same results those extra programs give.

I’m looking forward seeing people using this program (or any other) for creation of games and then tell us how they did it. Thanks for your comment!