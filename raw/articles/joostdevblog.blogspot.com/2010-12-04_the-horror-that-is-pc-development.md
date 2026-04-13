---
title: The horror that is PC development
url: http://joostdevblog.blogspot.com/2010/12/horror-that-is-pc-development.html
author: Joost van Dongen
published: '2010-12-04'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

*Swords & Soldiers is now out on PC and Mac on Steam! Buy it from*

[SwordsAndSoldiers.com](http://www.swordsandsoldiers.com)and use the coupon-code "sinterklaas" before December 5th to get a 30% discount!In the past two years I have released my first games as a programmer on the Playstation 3 and Nintendo Wii. As I was told beforehand, the most evil part of console development are the certification requirements. Sony, Nintendo and Microsoft have long lists with hundreds of demands that you must meet in order to be allowed to release your game on their platform. These are all purely technical and are about topics like: "Pause the game if the controller runs out of batteries", or: "Show this message when the harddisc is corrupted."

Going through those lists and implementing all of it is incredibly boring work and has little to do with making cool games. However, last week I learned that PC development is actually a lot worse! On consoles, at least all of the requirements make sense, and since you know exactly on what hardware your game will run (all Playstation 3s are essentially the same), it is quite easy to test for. How unlike PC development...

Last week we launched

[Swords & Soldiers](http://www.swordsandsoldiers.com)on the PC and the amount of things that can go wrong on all these different combinations of videocards, drivers, Windows versions and user settings is just terrible. Knowing the hardware on consoles suddenly makes them seem incredibly simple to develop for!

![](../../assets/4f8abe9a4c783a27.jpg)

The main culprit on PC is the videocard, so I figured it would be interesting to have a little look at the kind of issues we came across during development of various games.

One thing most graphics programmers know, is that you should use power of two (

*PoT*) textures, so resolutions should be like 128, 256, 512, 1024 and 2048. However, this is only relevant for pretty old videocards, since all modern videocards can handle other resolutions as well. Because of our animation system, we often have to round values up, so an animation sheet of 600*512 pixels becomes 1024*512 pixels. That is a huge waste! So to save a lot of space, we don't use power of two textures in HD. Since older computers also need to run Swords & Soldiers, we added a low-res SD mode where all textures are power of two.

Now I would like to detect whether the videocard can run in HD, and then hide that setting if the videocard cannot handle non power of two textures. But how do we detect that? There are some OpenGL extensions related to it, so I tried checking for those. However, some videocards don't have these extensions, yet they can run in HD anyway. I wasn't able to find a definite way to detect this (although I guess greater minds will know one), so I ended up allowing everyone to select HD and showing a message that tells the user to play in SD if the game looks broken otherwise. Pretty lame, but at least it is a clear solution!

![](../../assets/1ee38bc756e6b5fd.jpg)

A weird issue I came accross while working on

[Proun](http://www.proun-game.com), is that certain really old onboard Intel videocards cannot handle objects with more than 65536 vertices. This only happens on some very specific old Intel cards and is okay anywhere else. Since Proun is a hobby project and splitting meshes for this would be quite some work, I ended up not fixing this one.

One of the simpler hardware differences to work with is shader versions. Vertex and pixel shaders can have all kinds of features, depending on the videocard and the DirectX version. However, programming for these isn't that difficult, because shader versions are always backwards compatible. So if for example you would write a shader for version 2.0, then it will definitely also run on 2.x, 3.0 and 4.0. There are no weird combinations here!

![](../../assets/ba1b3c771604fed9.jpg)

However, there are those videocards who think it is okay to

*lie*. While developing

[De Blob](http://student-kmt.hku.nl/~joost1/Oogst3D/index.php?file=GAMES/Blob.txt), I learned that there are videocards that claim to be able to do shader 2.0, while they really don't. So I asked that videocard, "Can you do shader 2.0?" and the videocard said: "Yeah, sure, no problem!" I then tried to load the shader, and the videocard simply refused. How is one to program for that kind of weirdness?

![](../../assets/c710ac7b03e27077.jpg)

The final example I would like to discuss here is one that I am a bit ashamed of, because Swords & Soldiers actually launched with this issue and I had to release a patch on Steam yesterday to fix it. Swords & Soldiers has a dynamic font rendering system, which means that we only load those characters that the game actually uses into video memory. This way we can handle the enormous number of characters needed for languages like Japanese and Chinese. Now we only implemented this

*after*we did extensive tests on all kinds of videocards and we totally forgot to test again, so it turned out about 1% of users could not see any texts in the game at all. Pretty lame.

I haven't been able to figure out

*why*this happened on those videocards, but I do know that the OpenGL function glTexSubImage2D was the cause. So in yesterday's patch I built a workaround that doesn't use that function. For more technical details on this problem, have a look

[here](http://www.gamedev.net/community/forums/topic.asp?topic_id=589390).

So, I conclude that PC development is actually

*more*difficult than console development!

If you have any fun or interesting examples of rare hardware/driver/OS differences that break games, then please share them by commenting beneath this post. I'd love to hear about your experiences! ^-^

I've had a heck of a time with Intel GMA integrated video and some ATI cards (new and old) that show only 1/4 of the world terrain (Ogre TSM) unless I turn off terrain vertex normals. I've also had an issue with the nVidia 6800 not supporting something as fundamental as gl_ModelViewMatrixInverseTranspose in a vertex program.

ReplyDeleteTo be honest i think you could just safely disregard any shader 1.0 video card since they are that old and really limiting ;p Nowadays games like EVE online require you to have at least a shader 3.0 card: http://www.eveonline.com/devblog.asp?a=blog&bid=800 So its not a sin to disregard the old, and makes life easier ;)

ReplyDeleteI seem to remember having a similar issue with subimage on Wolfenstein mp, I ended up switching the texture format from a8 to rgba or argb ( can't remember exactly ) then all was well. This was also OpenGL and also dynamic font rendering.



ReplyDeleteMore memory but hope it helps.

Mike

It's really sad to read about how painful OpenGL programming must be :) In DirectX you have no such issues. You just query GPU for particular capabilities and you can be pretty sure what features are supported and what are your limits. The table of capabilities is bundled with DirectX SDK or can be found at http://zp.amsnet.pl/cdragan/ For example, D3DPTEXTURECAPS_POW2 along with D3DPTEXTURECAPS_NONPOW2CONDITIONAL tell whether non-power-of-2 textures are supported. D3DCAPS9::MaxPrimitiveCount and MaxVertexIndex tell about the maximum number of primitives that can be rendered with single call. About the old laptop Intel chips, they've supported Pixel Shader 2.0 but no Vertex Shader at all - here's the whole mystery, just do not to look only at overall "Shader Model".

ReplyDelete@Fish:




ReplyDeleteHow did you solve that terrain issue? I guess you do need those vertex normals, right? ;)

@Anonymous:

I personally think just saying you only support shader model 3.0 is only an option if you make something really high-tech next-gen. For a game like Swords & Soldiers, which should be able to run on almost everything, it's a bit lame. I think it's lame in Eve too, but I can understand their choice there.

@Mike:

We were using IA8 for the font texture, so the colour scheme may have indeed be the problem. Considering what the OpenGL standard said about colour schemes in glTexSubImage2D, it does seem like that should have worked.

@Reg:

It is the exact same in OpenGL as what you describe in DirectX. The problem is not that it is impossible to know these things, the problem is the enormous amount of things to take care of and videocards that don't keep to the standard. For example, MaxVertexIndex informs you of how many vertices you can have, but if your mesh is too large, then you still need to write code to split it and still present it as one mesh outside the engine to the game.

I wrote my own render engine for DirectX. For fullscreen mode, everything became juddery and choppy if I had two monitors plugged in that had different refresh rates. Unplug the the second monitor and problem goes away. Interestingly enough, windowed mode didn't have the same issue.

ReplyDeleteThe DirectX SDK has a file called CardCaps.xls in Samples\C++\Direct3D\ConfigSystem.



ReplyDeleteIt tells a lowest value of 65,534 for the MaxVertexIndex for video cards Intel 915/910, Intel 945, Intel G33/G31 and Intel Q35.

So you should stay below that value and you should be safe from this problem. I don't think a small game with simple graphics should break this limit. These kinds of graphics cards are in wide-spread use and I don't think it's a good idea to ignore them all when the game is otherwise not very demanding for hardware.

I'm just wondering, as a game programmer, what is your opinion of the programming language Processing (processing.org)? I was able to get a simple space shooter game up and running fairly quickly, and a simple tile based 2D platform engine up and running in a few days after that.

ReplyDeleteI have never used Processing myself, but I heard from some friends that it is a nice prototyping system. :)

ReplyDeleteI've found it quite useful. The main draw for me is that (a) unlike Game Maker, "real" programmers don't scorn you for using it (as much), (b) unlike Game Maker, it's 100% free, and (c), unlike Game Maker, it supports Windows, Mac, Linux, and Android.* Also, from what I've heard, it has a much better set of graphics commands than most other languages. Anyway, I know (well, I'm pretty sure) that the industry standards are C++ and C#, so I might have to learn those. My main hope is that I can make a few games with Processing and then go on to one of those.


ReplyDelete*YoYo Games is planning a product called "Game Maker Studio" for release in early 2012, which can export executables for Windows, Mac, iOS, Android, and PSP, but it will likely cost several hundred dollars.

Also, I already knew some Processing from programming my Arduino (arduino.cc), which uses a variant of Processing.


ReplyDeleteAlso, I want to reiterate how big a fan of Proun I am, even though I've said it before. Proun is freaking awesome!!!!!!

Interestingly, YoYo Games is kind of presenting itself as a publisher now, so if you make something awesome with Gamemaker, you can let them publish it on the iPhone. I don't know how many games they do this with, but I know they have released quite a few by now.


ReplyDeleteAs for C++ and C#: larger games and console games in general are 99% C++. C# is practically only used for tools, prototyping and smaller games. Especially since C# doesn't work on PS3, Wii, PSP, DS and Mac.

I'm thinking about buying Swords and Soldiers, and I am trying to decide between the PC and iOS versions. I'd prefer to have Swords and Soldiers in a portable form, but I'm worried that the iOS version may be missing some of the features of the PC version. Is that true, and, if so, what is it missing? Thanks!

ReplyDeleteBoth are excellent versions of the game! :)


ReplyDeleteThe PC version has online multiplayer and no splitscreen, while the iPad version has splitscreen multiplayer and no online. I think the iPhone version has no multiplayer. Also, I am not sure whether the iOS versions have achievements. I think that's it! :)

Great! With the iOS version on sale at $0.99 and the Steam's Awesome Indie Bundle on sale for $19.99, I may just buy both! Besides Swords and Soldiers, the only other game in the Awesome Indie Bundle that I really want is Sideway: New York, but at $19.99, who wouldn't buy the whole thing.

ReplyDeleteI just bought the Awesome Indie Bundle on Steam, and with it, Swords and Soldiers! I haven't gotten a chance to play it yet, but I will as soon as I can!

ReplyDeleteI've been playing Swords and Soldiers on both my PC and iPod Touch for the last few days, and I have to say that I'm very happy with it. Ronimo did an excellent job making the PC version, and Two Tribes did an excellent job on the iOS port. It's a carbon copy of the PC version, minus multiplayer! Anyway, excellent game, I am thoroughly enjoying it. It's even better than Proun!

ReplyDeleteGood to hear you like it! :)

ReplyDeleteHey Joost, it's quite an old blog but still I have a question..



ReplyDeleteHow do you test your game on all the different GPUs ? Do you have some kind of services you can use ? In particular if someone with an unreproducible hardware shows up, how do you debug ?

Thanks for this cool and interesting blog :)

potterman

That's actually a really difficult thing to do well.






DeleteOur approach so far is to test on old GPUs, since those are likely to have most issues. For example, before launch of Awesomenauts we had an old netbook in the office with a horrible GPU, so most problems any GPU can have showed up there already.

We also usually do a beta (closed or open) on Steam before a release to catch more issues before launch.

If any issues still appear after launch, then Steam allows you to patch really quickly (same day if you've set up your build systems well enough), so it's still doable.

In cases where users reported issues that I couldn't reproduce I've sent them custom executables with lots of logging to pinpoint the issue, or even with some experiments for possible solutions to see whether they work. Players are generally super helpful if they see that you're really putting in effort to fix their issue. :)

Note that there are QA companies that have lots of different hardware and can test for compatibility specifically. We haven't used those ourselves, but if you have some budget then that's likely also a really good idea.