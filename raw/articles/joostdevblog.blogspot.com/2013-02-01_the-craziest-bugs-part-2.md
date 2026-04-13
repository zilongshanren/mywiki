---
title: The craziest bugs, part 2
url: http://joostdevblog.blogspot.com/2013/02/my-favourite-bugs-top-7-part-2-3-to-1.html
author: Joost van Dongen
published: '2013-02-01'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Click here for numbers 7 to 4](http://joostdevblog.blogspot.nl/2013/01/my-favourite-bugs-top-7-7-to-4.html)

**3. Hidden functionality to turn off bugs**

On one of the platforms

[Awesomenauts](http://www.awesomenauts.com)launched on, we had a lot of trouble getting the internet connection between players to remain stable. After a while the ping would always start slowly increasing, until in the end it got too high and the game disconnected. Sometimes this took a couple of minutes to start, sometimes half an hour, but in the end this always happened.

We contacted the support team for the platform-specific networking library that we were using, and their answer was that we used too much bandwidth and sent too many packages. So we spent a lot of time optimising, and we managed to half the number of packages and half the bandwidth. However, the problem remained, and they again told us we used too much bandwidth. Again we halved the bandwidth and the number of packages, but the problem remained. At this point we were well below what they said was the ideal bandwidth usage and we couldn't optimise much more, so we were getting pretty desperate and contacted them again.

And then it happened...

Their answer was that their bandwidth throttling code was quite buggy, so there was a hidden enum that we could use to turn that code off. We used that and... the problem was instantly fixed! So they knew they had a bug, they even had an option to turn that bug off, but they didn't tell us for two months! I spent all that time doing extra bandwidth optimisations and it wasn't even necessary! Blargh!

Of course, using less bandwidth is always an important improvement for a multiplayer game, but we were already enormously behind on schedule at that point and this took a lot of time for a small indie studio...

![](../../assets/36357b7ece9661ce.jpg)

**2. Lying videocards**

This has been a personal gripe of mine for years. Some videocards simply

*lie*about their specs. Your game asks the videocard what it can do, and it will proudly brag about features it doesn't actually have!

I have not yet used any of the newer videocard features like geometry shaders, hull shaders and compute shaders, so I have not encountered any lying videocards recently, but I would be surprised if this doesn't still happen when you try to use state-of-the-art videocard features. It sure did a lot around the appearance of shader models 2 and 3. (Note that I haven't used the new shader types because I think they are uninteresting, but that's a long story that I will not go into today. Instead, I will just leave it at the short and controversial statement that they are

*irrelevant*.)

I had to work around such lying videocards in both

[Proun](http://www.proun-game.com)and

[De Blob](http://blob.oogst3d.net). What happens is that I make special versions of my shaders for different shader models, so that older videocards can still run the game, but with less special effects. The

[Ogre-engine](http://www.ogre3d.org)has a very elegant system to handle this, and thus Proun features proper materials for shader models 1, 2.0, 2.x and 3.0.

The core of this solution, however, is that you ask the videocard which shader models it supports, and then pick the highest allowed for the best quality. This works very well, unless the videocard

*lies*. It might claim to support 3.0, but doesn't really work with it. In the worst case, the videocard doesn't even give a compile error when being fed a 3.0 shader and simply outputs black pixels!

Several older Ati videocards turned out to do this in a horrible way. The solution ended up to hardcode the names of such videocards and feed them different shaders based on their name. If you look in the Proun folder structure, you can see folders with the same materials, but for different videocards, with beautiful names like "NotX8orX9". That last one contains materials that cannot be used on Ati X8** and X9** cards. I even have

*another*set of materials for Ati X1*** and X2*** cards, because they lie in a different way...

![](../../assets/22271b714c5c72bc.jpg)

**1. "If I buy the game, it isn't the demo any more"**

Yes, you read that title correctly. This is by far the most hilarious bug report I have ever seen, and easily claims the number 1 spot in this list, despite not even being a real bug. It was reported to us through the bug database though, so it qualifies for this list!

A professional QA testing company that was testing one of our games for us, at some point reported to us that if they bought the full game from the demo, then when they came back to the game, it wasn't the demo any more. It was instead... the full game!

Oh really?

That happens to be the point of buying the game, now isn't it?

When I replied in the bug database that either I didn't understand what they meant, or this bug report was a slight mistake from the tester, a producer quickly removed the bug from the database, so I never received an actual answer to that.

I think the reason they reported this, is that that particular shop (outside the game, not made by us) concluded the buying process with a question like "Do you want to go back to the game?" Whether you chose "Okay" or "Cancel", the shop always brought you back to the game, and apparently the tester concluded from the fact that there were two options that one of them ought to bring you back to the

*demo*, even though the game had just been bought. This is some pretty broken reasoning, but I can imagine where it came from.

(As crazy as this bug report may be, though, I would like to emphasize that this is the only silly report this testing company wrote to us. The rest of the reports made perfect sense, so this one mistake really shouldn't be held against them! That doesn't make it any less hilarious, though...)

That's it, folks! The 7 weirdest bugs I have encountered! Come back next week when I will discussion the Awesomenauts animation pipeline or visual effects performance (I haven't really made up my mind yet which it is going to be...)

Instead of figuring out capabilities of a graphics device one may also try to 'just' compile a shader. If it fails, fall back to one that has been given up as fall back shader. If the fallback shader fails, fall back to the fallback shader of the fallback shader continue this process until you have fallen back to the ffp.

ReplyDeleteNo need to test any capabilities, hurray :D

That works up to a point: as I said in the post, some videocards compile certain shaders without giving an error, and then simply output bogus vertex positions or pixel colours...

DeleteAh, THAT ol' throttling problem... I wonder how many games shipped with a bad multiplayer feature because of that. Well, at least they're admitting there might be a problem on their side now. That's progress, I guess. :-)



ReplyDeleteHaha, I didn't expect anyone would read this who actually had the same problem! Nice! Did you guys end up using a different library, figured out a workaround, or just shipped with the bug?

DeleteIt says a lot about the programming profession that when you write about your "favourite" bugs, you actually end up writing about your least favourite.

ReplyDeleteThe worst bugs are the fondest memories... ;)

DeleteAs someone interested in eventually making commercial PC games... do people still have to do this sort of trial-and-error BS with video cards, or are there ways around it? (Pre-existing lists of actual card features, for example.) I can't say I look forward to it...

ReplyDeleteYes, you still have to do that kind of stuff if you want your game to work on _every_ PC. If you can accept 98%, it gets a lot easier. Even for a game like Awesomenauts, which doesn't use a whole lot of videocard features since it is a 2D game, I still spent a whole lot of time making it work on odd configurations.

DeleteHaha, lots of fun reading this 7 bugs posts (several months later...)





ReplyDeleteRegarding cards lying, yes. Some cards lie big. But most of the time, it's not a lie, but rather a very twisted version of loopholes. Fortunately since DX10 generation cards, this is less of an issue

ATI Radeon X1000 models are specially hard to support. They say to support SM 3.0; this is technically true, but morally wrong.

That's because they accept the minimum execution instruction count (which is 512 IIRC) while all other gpus support at least 4096. So if your shader fails to run on their cards, the instruction count is probably the reason.

Note that even though SM 3.0 supports dynamic flow, many loops get unrolled. Furthermore in Pixel Shaders, the compiler *must* unroll the loop if you index a constant register.

A simple pixel shader with some gaussian blur filter and other post processing (i.e. DoF) can easily get to the 512 landmark, because of the number of taps.

As for VTF (vertex texture fetch), support is mandatory in SM 3.0; however MS left to freewill which formats to support. And ATI decided to support... 0 formats (but they "support vtf"!!!). A cheap trick to circumvent the specs and launch a GPU that claims SM 3.0 compliance.

Ogre checks for this and sets the RSC flags appropriately.

These are examples of the cheap tricks the X1000 did in order to claim SM 3.0 compliance. Who knows what other "lies" they do. Fortunately AMD is past those practices.

That's why in my games I just list the X1000 generation of cards as unsupported (which is something I couldn't do 4 years ago).

Yeah, I'm aware that most of these problems are because they use loopholes in the definition, but I don't think there is a relevant difference between that and straight out lying. Especially supporting-vertex-texture-fetch-but-without-supporting-any-texture-formats-for-it is the exact same thing as not supporting it. Technically it might be compliant with the specs and thus not a straight lie, but they knew very well that it didn't actually work, so it isn't any better than a lie.

DeleteOops! I Forgot to comment about bug #1





ReplyDeleteWhat I think that may be possible is that the tester was expecting that, after buying the demo, another version is installed.

While this may have some "experience" reasons (i.e. relive the demo missions); it is quite possible it was from a piracy perspective.

Demos that can be converted into full version means pirates can use your server bandwidth to download it, then apply a crack/patcher/fix to unlock the full version.

While there are divergent opinions of this (i.e. on the other hand the customer gets the full version automatically, rather than having to wait downloading

again); it is generally accepted that stealing bandwidth & server resources is more scumbag than just pirating.But that depends on your architecture (i.e. if the demo is distributed through 3rd party servers you don't pay) and demo size.

Since I know what game and platform this was, I know this was not the case. This is simply how demos work on that specific platform... :)

Delete