---
title: Simonschreibt.
url: https://simonschreibt.de/gat/stylized-vfx-in-rime/
author: Simon
published: '2017-06-07'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

This is a talk I gave on the [ADDON Conference](https://addon.events/en-UK/) about three stylized effects in [RIME](http://www.tequilaworks.com/proyectos/rime/). Since it wasn’t based on an article, this time I can only offer a video and no text-version.

**Tips for better listening**

- Play the
**video in 1.5x speed**(saves time & reduces echo/reverb a little bit) - I placed the mic right next to the laptop fan like a pro. A little “loading bar” shows when the noise will be gone.
- This is the
[Diablo/Blizzard-Talk](https://archive.org/details/GDC2013Love)I mention in the talk. Watch. It. Now!

![](../../assets/e8bf722a6e910433.png)


![](../../assets/e8bf722a6e910433.png)

I didn’t embed the video directly to avoid any tracking from Google and complications with the DSGVO.

I hope you’ll like it and I’m looking forward talking to you in the comments or via mail/twitter about similar effects or improving the ones I just presented. :)

Thanks to Alain from [Alkemi](https://twitter.com/alkemigames) and the organizers of the conference ([Elsa](https://www.linkedin.com/in/elsa-charrier-b3704531/), [Amélie](https://www.linkedin.com/in/am%C3%A9lie-wannyn-35075b85/) and [Eddy](https://www.linkedin.com/in/eddy-celestine-951b922)) for inviting me, [Tequila Works](http://www.tequilaworks.com/) for letting me speak about the effects and all the nice people I had the opportunity to speak to at the event. It was awesome!

![](../../assets/20bcf881098293ab.jpg)

The panels where happening in this old fire-watch.

![](../../assets/d228486cab6a2011.jpg)

Talks where given in this conference center.

![](../../assets/2198458317747e50.jpg)

In the conference center I found the longest door-opener-thingie ever.

![](../../assets/169d314e19014386.jpeg)

Eating Crepes. Nom Nom Nom!

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

[Tequila Works](http://www.tequilaworks.com/)allowed me to share the RIME Fire Material (created by

[David Miranda](https://twitter.com/BetaVersionOfMe)).

[Download this uasset file](https://data.simonschreibt.de/gat065/update3/rimeFire.uasset) (“Right click” and “Save as”) and copy the file into your Unreal project directory (note: you’ve to add your own noise/mask textures). This picture shows how the material network looks like:

Two guys asked me for help with their material- and particle-setup. I created two little videos for them using their assets as example. The videos weren’t meant to be public but it fits here well and maybe it helps other as well. :) Thanks to Brandon for allowing me to use and show his materials/particles he sent me!

The first video goes about the fire material and how to set it up correctly (on the example on Brandons material):

![](../../assets/8956af43eca1e0c4.png)


![](../../assets/8956af43eca1e0c4.png)

I didn’t embed the video directly to avoid any tracking from Google and complications with the DSGVO.

The second video is about how to setup the material and the particle system for the dust/smoke VFX (on the example on Brandons material/particles):


![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

[Alexandre Van Halteren](https://www.artstation.com/artist/alexandrevanhalteren)in Unity!

Oh and someone asked about how to avoid the linear vertex-color-transition. I made a little example for that:

![](../../assets/5e1a0659d42ccb71.gif)

Here you can see how the edge is modified by an Unreal material. At the top you see the original linear transition. This gets modified by some nodes. You can let it like it is or use one of the two examples below to “sharpen” the edge a little bit.

[Charles Thomas](https://twitter.com/Xerxes1138) mentioned another way to do this and here it’s even possible to scale the hardness of the border:

![](../../assets/35b478febcef446f.gif)

And here’s the Unreal-Nodes:

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

I just noticed this smoke in [The Showdown Effect](https://www.paradoxplaza.com/the-showdown-effect/SESE01GSKtse0001.html) which does not only fade-out nicely (by Alpha-Erosion/Threshold) but the particles are actually lit which gives them a similar appeal to what we achieved in RiME.

Here is a zoom-in on the lit particles which proudly present their nice volume:

So I had a look on the textures and it wasn’t surprising to find some normal-maps (only with RG channel stored, the B channel gets re-calculated in real-time).

More interesting are the diffuse textures. A little detail which I really like: The alpha of the diffuse texture is responsible for the alpha fading/erosion/threshold – that is a common technique.

But the structure of the alpha is **not** randomly painted. It fits perfectly well to the normal-map! My guess: They used a sculpting-program to create the normal-map and then rendered out a height-map of the same sculpted geometry. This serves as a perfect alpha-fade mask.

It’s a subtle thing but in the **left** version you see a alpha-mask which does **not** fit to the normal-map. On the right you can see the version where everything fits:

![](../../assets/1378d9d5526a7484.gif)


As you can see, when everything fits together, the impression of volume is preserved even during the fading-out. On the left the fading happens with a alpha channel which does **not** fit to the normal-map which destroys the illusion of volume:

![](../../assets/29664f68e095d348.png)


In case you’re interested in the material, here I created something in Unreal:

![](../../assets/ba0680151067ebbc.png)

[MathsGameArt](https://twitter.com/MathsGameArt)just released a

[very detailed tutorial](https://www.artstation.com/mathroodhuizen/blog/ZEgV/stylized-vfx-in-unity-a-rime-inspired-waterfall-full-breakdown-part-1)about making a stylized cascade with water-ripples in Unity.

Here are several other really cool creations of water, smoke and fire :) Thanks guys! You’re awesome!![](../../assets/592c21bc752ac68d.gif)


![](../../assets/ba0680151067ebbc.png)

[Alex Vinogradov](https://twitter.com/yarpoplar) gives the world [this great break-down](https://twitter.com/yarpoplar/status/1012245778423742464) of the stylized water-foam. Thanks! :)
![](../../assets/ab5ddd38ac0aae9f.gif)


![](../../assets/ba0680151067ebbc.png)

[The C.reator](https://twitter.com/cayou66) just [tweeted](https://twitter.com/cayou66/status/1044638512455331840) this awesome waterfall :) He’s even making it interactive, you can see that on his twitter timeline.

Hey Simon! Pherify in Maya? Aka PolySmooth? ;]

Hi Simon!

Amazing talk! Thanks for sharing. Didn’t know this stuff was possible with shaders in UE4 :)

I got a little lost in the presentation of the flame-effect. Would you be able to draw a quick node-graph-representation from UE4 so its easier to follow along? I really want to understand all this.

Wow! Thanks for sharing node-graph for the fire…and for all the extra examples! This page is SO bookmarked!

All the credit goes to Felix Menendez and Tequila Works :) It’s awesome that I was allowed to share all this and that we get all these cool little flames now :)

Thanks for sharing, great talk!

Omg this is awesome ! I’m actually working on a stylized scene in Unreal Engine for my demo reel. This is so gonna help me :D Thanks a mil !

Feel free to share your work when you’re done :)

Hey Simon, great video ( except the noise :D )

The homogenous sphere is using a noise texture for “alpha erosion” – did you bake the Noise texture in a different program or used UE to bake it using RenderToTexture baking?

I have huge problems with noise & seams ( not using Absolute World Space ) on spheres. Do you might have any further advice on that topic?

By noise I meant environment noise :x

Hi I am having huge problems with the package from Update3. When using opace moge it looks good but it’s a little to transparent. When I change the material mode to the one using Opaciti Mask It’s no longer opace but there are black artifacts … could it be becouse of mine gradient texture or just I need to subtract something more?

Hm…could you show some images as example? It’s a little bit hard to guess how the artefacts looks like.

Sorry silly me … I was testing it on scene with Post Process that added outlines :( Anyway great stuff! I learned so much on the way!

Dear master Simon,

I’m so so so so appreciate for your sharing. Your articles are inspired me a super lot.

I made a small torch that refer your articles. (The Fire in RIME and The wing in Diablo III)

Here is the link :

https://youtu.be/Dp5tea-rdH4

Specially thanks for you!!!

Je sens grand heureux sur la langue de shader parce que tu!!

Merci beaucoup!!

Oh, that torch is really cool! :) Have to add it later to the examples of the article! <3

I’ve just added it :)

https://simonschreibt.de/gat/stylized-vfx-in-rime/#update12

Hi Simon, your blog post inspired me a lot, thanks for sharing this very precious knowledge, specially on such a cool game ! I’ve tried to reproduce the waterfall (with ripples, splashes) and the water (not exactly the one in RiME, as I don’t have the same needs right now). You can check the result here:

https://twitter.com/cayou66/status/1044638512455331840

Any feedback will be appreciated !

Thanks again, I’ve learned a lot :)

Thanks man, that’s awesome! I’ve just made a tweet mentioning your waterfall. Also, feel free to share how you made it interactive :)