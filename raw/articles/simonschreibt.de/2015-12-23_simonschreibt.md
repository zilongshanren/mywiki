---
title: Simonschreibt.
url: https://simonschreibt.de/gat/fallout-4-the-mushroom-case/
author: Simon
published: '2015-12-23'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

![](../../assets/f76e996cea3b6e11.png)


![](../../assets/f76e996cea3b6e11.png)

I didn’t embed the video directly to avoid any tracking from Google and complications with the DSGVO.

![](../../assets/c4ff61a908538274.png)

We’ve got a new case to solve: How did

[Bethesda](http://bethsoft.com)do these fine mushroom-like explosion clouds?

If you **don’t** know what’s so hard doing such effects, just continue reading. If you **do** know the difficulties and just want to read the explanation, jump to the solution-section by ** clicking here**.

![](../../assets/c82bbd87a20e55aa.png)


![](../../assets/919caa1efdb14400.png)

The upper part of such an explosion consists of complex movement where the hot gases “roll” around the center of a “donut”-shape:

![](../../assets/183b99c0d6c17e35.png)


In addition there’s a transition from “only hot gas” to “only black smoke”:

![](../../assets/9f58b2bd8ff81aee.png)


As you see there is some complexity and below I’ll shorty conclude how games tried to solve the visualization in the past.

![](../../assets/c82bbd87a20e55aa.png)


![](../../assets/919caa1efdb14400.png)

Some older games didn’t show the whole “build up” process of the explosion cloud but used a bright fullscreen effect and when this was gone particles **had already** formed the typical tree-like shape but not much movement was going on anymore. Here’s an example from [Mercenaries 2: World in Flames](https://en.wikipedia.org/wiki/Mercenaries_2:_World_in_Flames)

It’s really not a simple task to make something like this with just simple particles and without any extra features like geometry or texture animation which will be explained below. But what was already achieved pretty well is the **form** of the cloud!

To get the movement a bit more interesting, you can rotate the particles in different speed & direction depending on the effects origin:

Here’s an example ([R.U.S.E.](https://en.wikipedia.org/wiki/R.U.S.E.)) where this works very well and shows some nice movement in the raising clouds:

But even now the hot gases **don’t** get “sucked” in again at the lower part of the “donut” like in real-life. That’s why you may use geometries as an addition to the particles – see the next page for details.

![](../../assets/c82bbd87a20e55aa.png)


![](../../assets/919caa1efdb14400.png)

In my eyes Fallout 3 did a great job in combining geometry and particles to get it right (at least for its time). Directly from the start you can see details of the movement because the explosion **isn’t** completely hidden by a big white flash:

This is done via UV Animation which basically means that you have some geometry and move a texture along. If you fade this in and out (at the beginning and ending of the effect) and combine it with some particle smoke, it works already really well.

Here’s an example how the Fallout-Texture looks on a test geometry with additive blending and some vertex color to avoid hard edges at the geometry border:

In Fallout 4 a similar texture animation was used on particles (not geometry like in Fallout 3) which works really well by using one texture as cloud shape and moving another tile-able texture in addition over the particle. It even looks like that the scrolling-direction points always towards the center of the explosion:

If you look closely you might still notice that it’s “just” a texture moving along a **flat** particle plane. Here I changed the second texture to show the mechanic a bit better:

Now we have not only a good tree-like form but also really nice movement. The only thing what’s missing is that the burning gas “convertes” to black smoke (in a more complex way than just fading the bright parts out and only leave some black particles).

Except from rendering explosions with a complex simulation program I wouldn’t have any idea of how something like this could be done in a game but then I saw a trailer with a stunning explosion:

Doesn’t it look great how the fire gets “eaten” by the black smoke – how it dissolves? Unfortunately I don’t own the game and can’t search for clues but at least it showed me that something like this is possible. But how?

![](../../assets/c82bbd87a20e55aa.png)


![](../../assets/919caa1efdb14400.png)

My only explanation would be that it’s pre-rendered somehow with e.g. FumeFx. Here’s an example of what you can simulate with the software (but of course **not** in real-time – [click here to see it in motion](https://www.afterworks.com/FumeFX/Shading.asp?ID=10)):

An in fact some studios like Epic use this approach and bake the result of the simulation frame by frame into textures. If you want to know more about this workflow, watch this great video:

![](../../assets/554ee067821144d1.png)


![](../../assets/554ee067821144d1.png)

I didn’t embed the video directly to avoid any tracking from Google and complications with the DSGVO.

Regarding our original question, I was sure that Fallout 4 did exactly the same thing: Pre-rendering the explosion and just showing a “playback” in the game. Just as a reminder: Here’s the Fallout explosion again:

![](../../assets/c82bbd87a20e55aa.png)


![](../../assets/919caa1efdb14400.png)

It **is** an atlas texture and it looks wonderful when played – and in addition it’s **loop-able**!

But there’s **no fire** at all! I thought something must be missing until I remembered the concept of **gradient mapping**. More details can be read in this [great article](http://technical-eden.blogspot.de/2012/01/gradient-mapping-awesome-way-to-get.html) and watched in this small example:

So you can colorize the grey smoke texture into something with color by re-mapping colors. Here I defined the black values as orange and what was white before is now black:

Looks great but there are two problems left:

- The fire/smoke proportion stay the same but we want to have a lot fire at the beginning and only black smoke at the end
- We
**don’t**see any cloud silhouette and if we apply the transparency information of the atlas texture (alpha channel) it looks like this:

I was confused because the alpha channel makes the whole texture mostly 50% transparent but in the game the clouds are almost **opaque**.

Again the solution seams to be gradient mapping: For cutting out the cloud shape, they **do use** the alpha channel of atlas texture **but** re-define its values via gradient mapping and achieve an opaque look:

Fallout stores its gradients in *tadaa* textures. What a surprise. Let’s have a look on it:

What’s that? For a standard gradient mapping you would only need a texture of **1 pixel height** so why do they use a quadratic texture?? The reason is, that they sample different pixel-“lines” (from bottom to top) depending on the **particles lifetime**!

This is genius! It makes it possible to colorize the smoke with a lot fire at the beginning and the longer the particle raises into the air it gets more and more black.

They even changed the cloud shape a bit by modifying the alpha channel over time.

This is so awesome! I love that they have a loop-able animation so that can set the particle lifetime really high without having to bake more pictures into the atlas since the color variation is handled separately.

I think it’s fair to say:

For those who are interested, I’ve prepared some more experiments for a better understanding and to note some observations.

Here I colored the lower and the upper part of the gradient texture in different colors and like expected at some point of the particles lifetime the color jumps:

Here I did the same but with different colors **right** and **left** which means that one color overwrites the grey-scale values from 0 to 127 and the other the values from 128 to 255:

This one is a bit **weird**. I changed the **alpha channel** of the gradient texture (everything is black except **one** pixel line at the bottom). I would have expected that the particles disappear very early. But see the result with your own eyes:

The color changes like before (which means the shader reads from the center-position of the diffuse channel where the color change happens) **but** the particle is still visible! I guess the shader handles the alpha channel in a different and non-linear way and sticks a longer time to the first pixel-line.

In my last example I made the alpha channel hide more and more of the visible texture the longer the cloud “lives”:

![](../../assets/d02355252862d069.png)


Thank you for following me through all these clues and reading this dossier. If you have any feedback feel free to contact me!

![](../../assets/c82bbd87a20e55aa.png)


![](../../assets/ba0680151067ebbc.png)

[Ravendarke](https://www.reddit.com/user/Ravendarke)showed examples from a game he’s working on (

[Wayward Terran Frontier](http://www.wtfrontier.com/)) where similar stuff is done with an interesting approach to make a non-seamless texture seem seamless (more about that below):

The color variations are done like in Fallout 4. The smoke texture is just grey.

The smoke texture in the game has 14 frames **but** the first and the last don’t match perfectly. The solution for them was to blend the frames into eachother instead of “just” playing the animation frame by frame:

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

[Florian Smolka](https://twitter.com/smou_)shows his shader-work from an

**unanncounced**game (World premiere!) from the great german developer

[Mimimi Productions](https://twitter.com/MimimiProd)! We even get a look at the textures and

[commented shader](https://data.simonschreibt.de/gat056/update3/Particle-GradientMapped-Animated.shader)code! How cool is that?

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

[thwix](https://bsky.app/profile/thwix.bsky.social)shared a nice trick in the

[realtime vfx discord](https://discord.com/channels/324301685105229835/797497600530055188/1312402453614039060)to add “camera corrected” motion to the particles to a shock wave but this could also be used to add a nice rolling motion like discussed above in the article. I will quote:

*“To mimic incompressibility in fluid dynamics, it’s often nice to have particles rotate counter to their velocity vector”*

![](../../assets/ad24184263b02296.gif)

*“but this starts to break down when viewed from another angle, due to the nature of sprites rotating relative to the camera”*

![](../../assets/1d8ad76b64524b75.gif)

*“a fun lil solution to this is to adjust the rotation based on the relationship between the viewing angle and the velocity vector”*

![](../../assets/9be39352fce191e7.png)

*“This gives us the same perceived rotation from both angles”*

![](../../assets/40dfe0070cf59ca9.gif)

*“Which is also really effective for shockwave effects.”*

![](../../assets/4c90cecb286c598e.gif)

Great explanation for a simple trick and great visual results. I looked at the video and the article. Good job ! :)

Thank you! :) Good to hear!

Great article and explanation! Very useful.

Amazing investigation, thanks a lot man !

Excellent article. I’ve thought about using color grading that changes over time. Ingenious!

I’m also very happy that you’re continuing to do video + full text for your articles, very helpful :)

Yeah I’ll try to do a video when I’ve the time for it :)

Amazing article. Do you mind if you share the texture you export from fallout 4? I would like to practice some programming

If you own Fallout 4 you can extract it by your own. If you don’t you can send me an E-Mail so I can help you. :)

I’ve done this, but I cannot find the alpha channel map for the smoke loop…

Thank you for the detailed breakdown! Really useful, especially because i’m currently working on something similar =) Although i used the remapping before i didn’t thought about using it in that case.

Did they use a extra texture for the alpha channel or just the alpha channel of the flipbook texture?

Would love to see your results if you’re done with out work :) The transparency information where in both cases (flipbook texture, color texture) stored in the alpha channel. :)

Thanks for this. Really appreciated. I tried the shader provided and it doesn’t give good results ? Is there something missing ? I’m not all that experienced in shader coding.

To be honest I didn’t try it out because I’m not that into shaders too. Currently I rely on the great material networks in the Unreal engine. :) But if you give a more detailed report about what’s not working, maybe Florian can help you?

Hey! Most likely its due to the texture settings. The ramp Textures have to be automatic truecolor formated, dont generate mip maps and the wrap mode should be set to clamp =) Hope that helps.

Thanks for your comment :) But to what point you’re refering at?

Oh damn, i thought i pressed the reply button. Was meant for dom’s question.

thanks for the reply. I’ll try it out :D

Really good!

I’m FX artist.

So I wonder how to find the source.

Can you give me the information?

Not sure what exactly you’re looking for. What source? :)

Both, but especially curious fallout 4!

How do I know that?

I meant what exactly you’re looking for? :)

Actually, Not a specific source. Just I want to know how . T.T

I guess you need to check out this free Unity3D shader – https://www.assetstore.unity3d.com/en/#!/content/10580

It looks really awsome, not using particles and looks pretty the same like mushroom explosion when you move the object up from the ground.

yeah these geometry explosions are soooo cool :) saw something likes this the first time in planet annihilation and love it. :)

Where is the alpha channel for the Fallout 4 smoke texture?

It does not appear to be contained within the DDS file…is it a separate image?

I don’t remember but I think it should be stored in the DDS. But I’m not 100% sure anymore and don’t have the data here right now. :(

Hi Simon,

I was wondering if you knew of a shader in Unity (or a tutorial on how to) set this sort of shader up in shader forge or in the new shader graph? Any help would be greatly appreciated.

Many thanks for your excellent resource.

Hi :) The basic technique you want to use is “Gradient Mapping” which you can find here: http://acegikmo.com/shaderforge/wiki/index.php?title=Gradient_Mapping

But instead of using a 1D-gradient, you need to use a 2D-gradient and change the pixel-line you read over time. Basically the lifetime of the particle is the V-Coordinate of the UVs. :) I hope that helped a bit!

Many thanks for your help Simon.