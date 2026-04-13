---
title: The craziest bugs, part 1
url: http://joostdevblog.blogspot.com/2013/01/my-favourite-bugs-top-7-7-to-4.html
author: Joost van Dongen
published: '2013-01-25'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[very out-of-the-box bug](http://joostdevblog.blogspot.nl/2011/12/lamest-bug-we-ever-encountered.html)and a

[painful oversight bug](http://joostdevblog.blogspot.nl/2012/03/weird-cause-of-swords-soldiers-network.html)before, and since then I have encountered hundreds (or was it thousands?) of other bugs. Today I would like to give you my favourites.

These bugs are from various categories: from funny, to surprising, to dumb library design. Most we have been able to solve, but for some the exact cause still remains a mystery. The one thing they have in common, is that I remember them fondly. Or frowning. Or while gritting my teeth...

[Click here for numbers 3 to 1](http://joostdevblog.blogspot.nl/2013/02/my-favourite-bugs-top-7-part-2-3-to-1.html)

**7. Std::abs differs between compilers**

This is one I encountered recently in

[Awesomenauts](http://www.awesomenauts.com). We thought hardly any Mac users would have gamepads, so we had initially decided not to support those on Mac. After launching Awesomenauts on Mac, this turned out differently, and a lot of Mac users requested proper controller support. We decided to try to patch this in quickly before Christmas, but one particular bugs almost kept Mac joystick support from making it into that patch.

It turned out that the sticks would only work if they had full output. Pressing them to anything but fully right or fully left had no effect in the game whatsoever. Somehow, our joystick class outputted proper

*floats*in the complete [-1, 1] range, but once they got to our gameplay code, they were only 0, -1, or 1. I didn't see any spots where they were turned into

*ints*, so how was this happening?

The reason turned out to be

*std::abs()*. Normally, this function only works on integer types, and

*fabs()*is used for floating point numbers. However, in Visual Studio

*abs()*also works fine on

*floats*, and we had used it in that way on a joystick axis value somewhere. This version of

*abs()*does not exist on Mac! When we tried to use gamepads on Mac, the compiler did not print a warning and instead simply rounded the decimal axis value to an

*int*and applied

*abs()*to that. Since at that point the axis value was already in the range [-1,1], this meant that everything but -1 and 1 were rounded to 0...

Luckily, we found this one in time and were able to patch in Mac gamepad support before Christmas. And our Mac users lived happily ever after... (or so I hope!) However, I still find the combination of Visual Studio having extra functionality and the Mac compiler not printing a warning pretty nasty!

**6. Editor framerate extremely low around centre of world**

This is a bug that our artists at some point started complaining about. When using our in-house

[animation editor](http://youtu.be/41CCE3BFiqA?t=25s), the framerate became incredibly low, unless they moved the camera away so that the centre of the world was not in view any more. I didn't have time to look into this right away, but strangely over time the bug seemed to grow worse and worse, until the editor was hardly usable any more.

![](../../assets/84678116e5af28f8.jpg)

Quite puzzled, I dove in. I quickly discovered that the renderer was responsible for the framedrop, so I started gathering data on what exactly was being rendered. The cause proved to be quite... interesting.

[Awesomenauts](http://www.awesomenauts.com)in total has over 4000 animations at the moment, and these contain some 5500 particle systems. It turned out that in the editor, all of these particles were always rendered, but with 0 particles each. The renderer did not check for this, and set up shaders, textures and matrices for these particle systems, and then proceeded to feed the videocard a whopping 0 polygons to render. Doing this 5500 times per frame is not a good idea... The solution was twofold: the renderer should check for polygon count before rendering, and the editor should hide these empty particle systems to keep them from reaching the renderer at all.

I tested the results of fixing this on two computers, and on one the framerate went from 28fps to 115fps in the editor, while on the other it went from 36fps to 273fps. Those are the nicer optimisations!

But why did this only happen at the centre of the world, and why did it grow worse over time? This is because most animations are quite small, and all their objects are near the centre of the animation, including the particles. After some more experimentation, it turned out that since the particles are not all exactly at the centre of the world, scrolling around would gradually increase the framerate as more of the area near the centre went out of view. Finally, the reason it grew worse over time, was that our artists were quickly producing more and more animations for the skins we were adding to Awesomenauts, adding more and more particles to destroy the framerate...

**5. Disappearing textures**

This is an issue that I actually haven't been able to pinpoint and solve, but it is so bizarre, that it deserved a place on this list. A user

[reported](http://www.awesomenauts.com/forum/viewtopic.php?f=13&t=7872)that at some point,

[Awesomenauts](http://www.awesomenauts.com)suddenly started looking like this:

![](../../assets/87880d0bfd9d6ed8.gif)

He also posted a

[video](http://www.youtube.com/watch?v=Y_jWGbZMzR8)of this event. What you are seeing here, is that the main view of Awesomenauts has been replaced by a small portion of the Steam overlay. The letters are names and the lowest line even mentions Steam's standard shortcut: shift+tab. On top of that, the Awesomenauts HUD is visible, as it should.

The reason I have so far not been able to find the cause of this bug, is that it is extremely rare: it has only been reported to us twice. One of my colleagues also had something similar once: a Steam icon had somehow replaced an icon in our own scoreboard. None of these cases ever happened again. Without any way to reproduce or test, I cannot solve this weird bug.

I can guess what is happening, though: somehow a texture from Steam replaced one of my own textures. The reason this replaces the entire screen in the image above, is that apparently the texture being replaced is the rendertexture that is used to apply post effects to the screen. The other report I saw confirmed this: there a different rendertexture was broken, causing only the background to look black (the background is rendered separately to apply depth of field blur, as I previously wrote about in

[this blogpost](http://joostdevblog.blogspot.nl/2012/04/depth-of-field-blur-swiss-army-knife.html)).

This makes me suspect that the problem might not even be in our own code: to render their overlay, Steam pretty much hacks into my rendering process every frame. I imagine the problem might for example be that something in Steam's code is problematic with the way I handle threading in my renderer. So this might not even be a bug in my own code... In the meanwhile, since this bug is extremely rare, I have decided to just leave it be.

**4. Random programs interfere with my game**

I don't know exactly how they manage to do this, but sometimes random programs manage to break

[Awesomenauts](http://www.awesomenauts.com)on PC. The worst offender is Adobe Air: this sometimes completely obliterates a player's internet, causing unplayably high ping in Awesomenauts. This doesn't happen for most users, but I have seen a dozen or so reports from players who managed to fix their high ping in Awesomenauts by uninstalling Adobe Air. This isn't just in Awesomenauts: I have also seen reports of the exact same thing in another game by a different developer.

Another example of random other programs messing up our game, was

[reported by a player](http://www.awesomenauts.com/forum/viewtopic.php?f=13&t=3403). This user had a very laggy, uncontrollable mouse cursor, but only during gameplay. I had no idea what caused this, but at some point the victim reported that the problem had went away. What had he done? He had updated... Java! Java!? What does that have to do with Awesomenauts? Awesomenauts is written in C++ and doesn't use any JAVA components! I still don't know how JAVA is able to break the mouse cursor in Awesomenauts, but it is a nice example of how completely unpredictable PC development can sometimes be. Consoles may be much more complex to develop for, and they may have all kinds of certification requirements, but at least they are always the same! Hurray for that!

That was it for the bugs today! The four bugs above were still somewhat sane, but the rest of this list won't be. Visit back next week for the top 3, where the real insanity happens!

As far as I can tell, std::abs(double), or float for that matter, was not in the C++03 standard. It seems to be included in the C++11 standard.




ReplyDeleteMy g++ gives me "error: call of overloaded 'abs(double)' is ambiguous" offering int, long int and long long int.

If there are no overloads, I get "warning: passing 'double' for argument 1 to 'int foo(int)'"

Definitely an annoying experience, but next time this happens you'll know immediately ;).

On std::abs - actually there is an overload that accepts float, and not just in C++11... you just have to look in cmath instead of cstdlib! For some reason cstdlib declares all the integer versions and cmath declares the floating point versions.



ReplyDeleteStill, your Mac compiler should have given an error for the ambiguous call if the float overload wasn't visible - Visual C++ 10 and 11 both do.

Nice article, I like hearing of other people's crazy bugs :)

Cool post Joost, looking forward to reading about the top 3!

ReplyDelete