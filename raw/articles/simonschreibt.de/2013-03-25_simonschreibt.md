---
title: Simonschreibt.
url: https://simonschreibt.de/gat/diablo-3-resource-bubbles/
author: Simon
published: '2013-03-25'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

There are 3 things in the world I could look at forever: Fire, other People working and the [Diablo 3](http://diablo3.com/) resource bubbles. I already fell in love with Blizzards art style like you maybe noticed [in my article about their 2.5D trees](https://simonschreibt.de/simonschreibt.de/gat/diablo-3-trees/). But today we’ll have a deeeep look at Diablos crystal balls and search for the truth.

![](../../assets/7ba10f91cb59c77b.gif)

![](../../assets/c862ae8013aef393.gif)

![](../../assets/2dc0fe13e939916c.gif)


Source: [Diablo 3](http://diablo3.com/)

They look so deep. So round. A delicious mix of blur and sharpness. Let me state my initial thought how this could be achieved (long story short: they’re both wrong. I’m on the woodway like we say Germany):

**Woodway 1st**

Take a polysphere, cut it half and pull some textures over the surface. Why is it wrong? Because i checked the ingame wireframe of the “bubble”. Guess what? It’s *not* a bubble! Here you can see my approach (red sphere) and the Diablo 3 mesh (green) which btw. contains only 218 tris instead of my 960.

![](../../assets/b7d139d69bc136ac.gif)


**Woodway 2nd**

I asked [Neox](http://www.polyphobia.de/) and he suggested to take a sphere, bake it into a normal map and do the rest with a shader. This is a good idea but i couldn’t find such a texture in the Diablo files. So why the hull do i waste your time with this nonsense?

Because [mikiex](http://www.polycount.com/forum/member.php?u=75360) posted a [great example](http://www.polycount.com/forum/showpost.php?p=1802103&postcount=176) which is similar to Neox’ idea. I think this will be [my next article](http://simonschreibt.de/gat/007-legends-the-world/). For now, just look at the image and see how great the world is wrapping around the sphere. But it’s *not* the way the devil went.

So let’s talk about the right way.

**Hellway 1nd** “UV Layout”

I was able to extract the “bubble” mesh and had a look at the UVs. And here’s how they look like:

![](../../assets/60648b6540cd816e.jpg)


![](../../assets/5055ec8fb1d2c8bf.gif)


s


**Hellway 2nd** “Geometry”

But moving only *one* texture wouldn’t create this beautiful mix of motion & depth. Thanks to the [D3 model viewer](http://www.cainsarchive.com/) we can see that there’s not only *one* plane.

![](../../assets/418122b095cb96ca.gif)


But i think they re-use the Mana-Bubble-Mesh since i can’t find any special geometry for the arcane sphere.

[bb0x](http://www.bb0x.com/)had i great question about the line which appears when your resources aren’t 100% full. This line isn’t bent and he mentioned that they maybe used a 2nd UV layout for this.

![](../../assets/c067236d8193e569.jpg)

Lucky for us that

[Julian Love](http://www.diablowiki.net/Julian_Love)mentioned how it was done

[here](http://simonschreibt.de/gat/diablo-3-resource-bubbles/#update3).


**Hellway 3rd** “Textures”

The textures for the wizard resources look like this:

To be honest, i can’t say how exactly these are blended together. But i want to make some notes:

**#1**

**03** is the alpha channel of **02**. Except for **04** none of the other textures does have an alpha channel.

**#2**

I really dig how they let the fluid texture reach a bit *above* the actual filling level. **04** and the 3 other small textures are used for the level line.

**#3**

If you look at it drawcall by drawcall you see a transparent sphere and i think **01** is used as alpha for it. I don’t get why the other stuff is rendered later, but i guess this isn’t how the game handles it.

You reached the end of the article. Simon is too sad to write more because he doesn’t like that he couldn’t find more information about the texture blending. He hopes that Blizzard hires him as a sad angel sitting on the left side of the bubble. Then he could gather more awesome stuff directly from the art heart.

Thanks to these holy programs: [D3TexConv v0.9b](http://forum.xentax.com/viewtopic.php?f=10&t=7320&start=45) & [MPQ Extractor](http://www.zezula.net/en/mpq/download.html) & [Blender](http://blender.org/). Without i wouldn’t have been able to make this article.

![](../../assets/ba0680151067ebbc.png)

[Julian Love](http://www.diablowiki.net/Julian_Love):

“The textures are all being multiplied together. Not blended. This is where all the color motion complexity comes from. It’s also how the motion of the water line is handled. […] Here is the formula for the water line alpha mask:



a = tex1.a * tex2.a * 4


Also, the water line is being deformed by the UVs, but you can’t easily see that distortion when you look at sphere straight on…”

Because i have not much knowledge about shader code, i asked him if the “* 4” is for brighten up the textures since multiply darkens them pretty much. His reply:

Yes, the *4 at the end brightens it back up significantly. We do the same thing with the color as well, only using *2. The color formula is



rgb = ((tex1.rgb * text2.rgb * 2) * text3.rgb * 2)


Each texture is actually an instance of the same texture, but each stage has a different UV offset, UV scroll speed and UV scale.

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

[Update 8 on Twitter](https://twitter.com/simonschreibt/status/1233186262229626880)which I need to share with you.

1. Turns out,

[Zerin Labs presented the trick](https://twitter.com/ZerinLABS/status/1155025801714241536)(from Update 8) a long time ago and even with a full explanation how to create the geometry from scratch:

2. [Ben Golus showed how to use a pixel shader](https://twitter.com/bgolus/status/1233279164947451909) to deform the UVs and use only a single quad to get the same effect. And he even [shared the shader code](https://gist.github.com/bgolus/b340a0f37a9b27cf49bc4be1bb1feb39) for those how want to try it out!

![](../../assets/402bad60aff417bc.png)


Source: [Ben Golus on Twitter](https://twitter.com/bgolus/status/1233279164947451909)

3. We got another example, this time from Bruno Afonseca, [how to make the same effect in a shader](https://twitter.com/3dBrunoVFX/status/1233289304526508032) and we got a nice Unreal Material Graph! Super cool! :)

Source: [Bruno Afonseca on Twitter](https://twitter.com/3dBrunoVFX/status/1233289304526508032)

![](../../assets/ba0680151067ebbc.png)

We got a nice earthy planet from

[Stelios](https://twitter.com/stelabouras):

[Pete](https://twitter.com/pete78clark) sent a good example for this technique besides planets and magical orb-spheres. Also, there is a nice discussion on his Twitter-thread with words like “equirectangular projection” … need to check the dictionary! :D

[Klemen](https://twitter.com/klemen_lozar) shows some planets too :) Nice composition!

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

This looks like your typical perlin noise domain warping to me.

I used this kind of effect once in an android live wallpaper: https://play.google.com/store/apps/details?id=com.formisk.aliquidcloud.free

Hi Heuristics. Thanks for mentioning the name – i found this cool article with an nice explanation: http://www.iquilezles.org/www/articles/warp/warp.htm

I’m not sure if it’s that advanced in Diablo, but your wallpaper looks great :)

I’m wondering if it’s more efficient with 218 tris+UV layouts for each or with 2 tris and prerendered distorted UV-cooridinates texture.

here is my mock-up in blender http://www.pasteall.org/blend/20533

(animating mapping node doesn’t work but manual changes do)

i guess it depends on what is less busy vertex shader or fragment shader

just saw your new article that is exactly about it. nvm :)

Wow, thanks for taking the time to build this in Blender. How can i play the shader animation in Blender? I pressed the Play-Buttun, but nothing happened :,(

as I said, animation with “mapping” node doesn’t work (I don’t know why because it should), so only way to see this is to manually change in “mapping” node location x and y, probably with shift button for more gentle manipulation

http://www.pasteall.org/pic/show.php?id=48555

Nice Demo!

This comment has been removed by the author.

Hm…i deleted your comment because it looked like spam. Was i wrong?

Hi Simon!

I’m attempting a Wizard globe in UDK’s material editor. Right now I’ve just been working on the diffuse portion, playing with the UV animations, tints, and how they overlay.

Wanna check it out? It’s on my blog: http://solarnoise.tumblr.com/

Wow, awesome that i inspired someone :) Looks cool to me!

This article was Helpful.

I made this on unity3d.

http://goo.gl/O9Yu8w

This looks crazy good! Thanks for the link! Will it stay in your dropbox? If you allow, i would love to add a link to it into the article!

Glad that i could help you :)

Of course, go ahead.

But, link is not permanent.

If possible, please put the this resources directly on your site.

http://goo.gl/uUGyvY

Hello ! Can you share source code project Unity3d?

Unfortunately it’s not made by me. But you can ask Apex at Twitter (https://twitter.com/ApexJPN) if he would like to share the code. :)

Hello!

It is probably a bit late but I figured alternative way for UV layout.

Done in Blender (obviously). Right order of unwrapping is crucial.

1. I start with Icosphere mesh on any subdivision level I see fit (3 gives me 320 tris ball, I’m gonna use half of it so end result would have 160 triangles)

2. I delete bottom half (marked orange)

http://s25.postimg.org/ys8o6mnxr/icosphere.png

3. I unwrap sphere as it is. ( I get UVs like on left side of image)

4. I scale it to be flat circle without changing UVs

http://s25.postimg.org/5bt247hkd/uv_layout_sphere_good.png

Looks cool! I tried this with a standard-sphere but this resulted in too many polygons. The use of the Icosphere definitely saves severa of them. Thanks for sharing – and no, i don’t think it’s too late. Such knowledge never gets old and i’m sure future-readers will be happy that you shared it with us. Thanks :)

Did the same effect some time ago with ActionScript 3 and Adobe Flash. Just rotate some texture (or 2-3-4-5, whatever) and render it with displacement shader. Nothing special. Pretty simple.

Do you still have this? I could add it as an example :)

There is a solution for unity on the asset store.

https://www.assetstore.unity3d.com/en/#!/content/50666

oh nice! :) thank you for the link!

Hey Simon,

great article! There’s one thing I don’t understand though. How did Blizzard achieve the waterline/fill-mask effect with bent UVs? I read through the comments and noticed the one saying the waterline gets distorted as well but tbh I don’t think this is true. Just look at your .gif of the scrolling checker material, especially at the very top an bottom, no way that an almost-straight waterline texture won’t get distorted so that it isn’t noticable. I’m currently trying to recreate this effect in Unity and was successful with a 100% filled orb, but the waterline and below-100%-masking is boggling my mind – did you get any additional insight regarding this topic in particular?

I think they just place the waterline-mask (number 04 in the textures overview) on top of the hard cut between “nothing” and “fill”. Maybe they offset the UVs of the waterline a little but to give it some extra-movement … ?

Thanks for replying Simon! :)

I think you misunderstood my question/observation. What I was trying to explain was: They modified the mesh’s UVs in a way that a circular, flat mesh looks like a sphere. That works perfectly for the fluids/contents of the orb, since its scrolling textures get distorted on the outer borders of the mesh, indicating 3D roundness. However, if you apply a waterline texture using the same UV layout, it will (like the fluid textures) get bent and distorted as well. In the .GIF you provided you can see that Blizzard’s waterline is straight as an edge, no matter whether it is in the middle or near the end of the circle. However, I think I found out how they did it. I’ll implement this in Unity – if you’re interested I can give you an update and detailed explanations once I’m finished.

Oh yes, I think you have to add another layer with standard UVs just for the water-line. I don’t think that they used the same UVs there. And of course, I would love to see you results :)

I got it working the same evening, it’s possible to map multiple UV coordinates to each vertex and access them in the shader. Like you said, a second, undistorted UV layout was needed to get the mask and waterline working. I was just confused by Julian Love’s comment saying the waterline gets distorted as well, basically implying they did it on the same UV layout

Here’s the current state of my implementation. The textures etc are WIP, I just wanted to test out the shader and basic setup. I can provide a step by step tutorial on how to achieve this effect in Unity if anybody is interested.

https://media.giphy.com/media/3ov9jRrJ4xILutaoSc/giphy.gif

wow this looks awesome! if you do a tutorial or something like that i would love to link to it :)

Dude your resource sphere looks awesome. Can you make a tutorial for it? Maybe share some code to what make it work? I am new to the shaders and that kind of an example would definitely help me.

I have been trying to implement this for the last 3 days. So far I was able to get some results: http://tinyimg.io/i/bzOFaUl.jpg

However, there are a couple of things that I don’t understand.

1) Are we multiplying textures by their rgb channels? What happens to the alpha channels (03 for example)?

2) How do we actually create the waterline? I read the article so many times but I am still lost on that. When I multiply waterline with other textures I get weird solutions (there is no significant waterline like in diablo, but instead I get a bad gamma line) as you can see in the link above.

a = tex1.a * tex2.a * 4

What are tex1 and tex2? I think I am doing something wrong with multiplications and alpha channels. Any clarifications would be greatly appreciated.

Thanks.

Hi Berk. As far as I see I would use an additive blendmode for the waterline insteaf of multiplying. If you’re stick, you can have a look at the updates and ask the people who already made an implementation. I by myself didn’t do it so don’t really know :( Sorry for not being able to answer your questions :(