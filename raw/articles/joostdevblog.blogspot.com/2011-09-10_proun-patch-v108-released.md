---
title: Proun patch v108 released!
url: http://joostdevblog.blogspot.com/2011/09/proun-patch-v106-released.html
author: Joost van Dongen
published: '2011-09-10'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Awesomenauts](http://www.awesomenauts.com), I finally found the time to fix a couple of bugs in

[Proun](http://www.proun-game.com)! This patch only fixes bugs and does not add new features, so no need to apply it you weren't encountering any bugs before. You can find the patch and info on how to use it here:

[Proun patch v108](http://www.ronimo-games.com/forum/viewtopic.php?f=7&t=1049)

These fixes are mainly for some specific videocards by Intel and Ati. Note however that I do not have these videocards myself, so I have not been able to test this patch well enough. So I hope some people who had trouble running Proun before can give it a try and let me know whether this fixes anything!

Quite a while ago, I wrote a blogpost about

[The horror that is PC development](http://joostdevblog.blogspot.com/2010/12/horror-that-is-pc-development.html). Some of the specific issues I fixed in this patch are definitely in that same category, so I find it interesting to discuss what went wrong:

**Bug 1: Crash on some ATI Radeon cards**

It turns out that ATI cards from around the time of the Radeon X1xxx series are officially liars. These are some pretty old cards, from around 2005. When the engine (

[Ogre 3D](http://www.ogre3d.org)) asks such a card whether it supports shader model 3.0 shaders, it happily says it does. Then when I feed it some really complex pixel shaders, it refuses and gives an error. Turns out these cards support most of 3.0, but not everything! So my depth of field blur crashed on this.

Here is the really frustrating part: I already had a simpler version of these shaders in the game, but because the videocard lies about its capabilities, Ogre tries to load the advanced shader. Crash! Knowing this, the solution was actually pretty simple: I have added rules to the materials that tell the engine that these specific cards need to use the simpler version, regardless of what they claim they can do.

**Bug 2: Crash on some Intel cards**

A somewhat similar crash happened on certain Intel cards. Intel cards from the GMA 3xxx series (released around 2006) can only do vertex shaders through software emulation. This is not a problem in itself: it just means you get a very low framerate, but everything would still work. However, DirectX handles this in a strange way: when you ask IDirect3D9 whether vertex shaders are supported, it says no. So the Ogre engine thinks these cards won't be able to run Proun at all. The IDirect3DDevice9 on the other hand will say yes. Quite weird, really, but someone discovered this and fixed the Ogre engine to ask both IDirect3D9 and IDirect3DDevice9 and use the best answer.

However, this fix was released around the same time when Proun was released. Since updating your engine version so near release is a bad idea (since it has not been tested well enough), that fix did not end up in Proun. So all I had to do now was add that fix to repair this crash.

**Bug 3: Broken math**

The final bug is exclusively my own mistake and not about weird PC graphics stuff. It turned out I had a math error somewhere that very rarely crashes the game. I already discovered this crash one week after launch, but because it happened so rarely, I was not able to find the cause. I have some data from the highscore server and I estimate this crash happened once every 10.000 runs through Composition #2. That is

*pretty rare*. But help came from an unexpected direction: the recent user track

[Cubed](http://www.ronimo-games.com/forum/viewtopic.php?f=7&t=1199)has a point where it almost always triggers this situation! So now I was finally able to find out what happened, and fixed it. Turned out this was a mistake in the vehicle math that I made

*six years ago*at the very start of the project!

(For those interested in the math: to get a vector perpendicular to the cable, I do a cross product somewhere with the vector [0,1,0]. When the direction of the cable itself is also exactly [0,1,0], this goes wrong.)

So, what have I learned here? That I should test on even more videocards before launching anything on PC!

*EDIT: To my eternal shame, it turned out that the fix for those Ati cards was still not working. Ogre happens to handle some material properties in a different manner than I thought. I fixed it in a more rigorous way now, and it works now!*

*EDIT 2: An even older Ati series, the Ati X8xx and X9xx turned out to have some other issues. I fixed those as well in patch v108.*

I like you. :)

ReplyDeleteMan, I remember the old Geforce 5 cards had something similar. They happily claimed to support Shader Model 3.0, but while it would happily accept branching statements, the cards in fact had no actual support for branching.


ReplyDeleteInstead, during the shader script compile time it made some form of 'best guess' code that predicted ahead of time what it thought the answer was going to be, resulting in some very strange code output and, on my behalf, weeks of hair pulling.

The Geforce 5 series, really? They introduced shader model 2.0, so 3.0 didn't even exist yet when they launched. Is this something they added into the drivers a year after launch then?

ReplyDeleteSince Pround is built on Ogre, any chance of a linux port ?


ReplyDeleteHave already tried the released version under wine but unfortunately does not work.

A Linux port wouldn't be too difficult, since indeed all the libraries used support Linux. But I don't know anything about Linux myself, so that makes it pretty difficult for me.

ReplyDelete