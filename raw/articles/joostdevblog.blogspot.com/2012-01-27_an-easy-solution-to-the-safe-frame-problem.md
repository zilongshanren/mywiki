---
title: An easy solution to the safe frame problem
url: http://joostdevblog.blogspot.com/2012/01/easy-solution-to-safe-frame-problem.html
author: Joost van Dongen
published: '2012-01-27'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Swords & Soldiers](http://www.swordsandsoldiers.com)for the Wii, was the safe frame. CRT televisions (you know, those old, big televisions that some people still have) don't show the entire screen: they simply leave out the screen's edges. I don't know exactly why this is traditionally done, but the amount of screen that is left out varies per television and can be pretty large on some of the worst TVs.

![](../../assets/c18c64b3e9afc1f9.jpg)

Surprisingly, many modern LCD/LED/Plasma televisions are by default set to also leave out the edges. They just zoom in a bit. However, since there is no technical reason why this is, these televisions come with a setting to turn that irritating behaviour off.

Now the good thing, is that there is a limit to how much of the edges a television actually cuts off. The area that you can be sure will be shown on every television, is called the

*safe frame*or

*safe area*.

![](../../assets/9253560eec65370b.jpg)

Since games need to be playable on any television, Xbox, Playstation and Wii all have requirements that the game should be playable even if everything outside the safe frame is cut off. So crucial information or interface elements can not be positioned outside the safe frame. It is of course a good thing that Microsoft, Sony and Nintendo force developers to make games that are playable for everyone, but this is pretty horrible for us as developers: usually you want the interface to be as far to the sides of the screen as possible to leave lots of playing field, but that is not possible any more.

![](../../assets/cb0500905a232fcc.jpg)

Luckily for me, our art team had to deal with this and not me. So they moved the interface elements further from the edges of the screen. Now the total screen (as is seen on televisions that don't cut off the edges), looks like this:

![](../../assets/b87bf1fe2cf4468b.jpg)

Note that it actually takes quite a lot of time and effort to do this correctly: in our office we have no television that has the worst possible safe frame, so instead we made a paper frame to put in front of the screen and 'emulate' the worst possible safe frame. Everything needed to be tested with this piece of paper in front of the screen.

Moving the interface away from the edges works, but it is pretty limiting for interface design, and it is also irritating work. While making Swords & Soldiers, we thought we had to do this, but right after the game was done, we discovered that some games solve this in a much easier way. So easy, that at the time it almost felt like a trick.

So, to keep you, the reader, from spending a lot of time on the safe frame, here is the simple trick that our new game

[Awesomenauts](http://www.awesomenauts.com)and some other games use instead:

Allow the user to set the zoom of the screen.

![](../../assets/5292ecd00a9f1220.jpg)

That's it. In OpenGL and DirectX, you can just create smaller viewports and leave the borders of the screen black. So on televisions that cut off a lot of pixels at the borders, you just render the game to a smaller part of the screen. Everything outside that is black. As long as the user sets this correctly (which he is forced to do when he starts the game for the first time), everything will always be shown, so you can put your interface elements wherever you like.

![](../../assets/445d721d81becd4f.jpg)

The only real downside this solution has, is that the resolution of the game is now pretty much dynamic. So rendering pixel-precise effects becomes a bit more difficult now. On the other hand, it also has a hidden benefit: since you render to a smaller portion of the screen, people with CRT televisions might get a better framerate...

This really is a simple trick, but for those who didn't know it yet: be glad you do now! ^_^

I have noticed a lot of titles have started to take this approach. I used to game on a CRT but it's been 2 or years since I got my LCD...Makes gaming so much more enjoyable. Always interesting to hear some behind the scenes from devs.

ReplyDeleteThe ps3 of me and my brothers, we still play games with it on an almost 20 years old (older than I am) crt television.


ReplyDeleteThe reason we do this is because the good television in the living room is from my parents, which means they use it in the evening.

My brothers don't have the money to buy a new television and I play games on my pc anyway, so it's more their problem than mine.

And it still works fine, only annoying thing is that it sometimes is hard to read text, for example with fifa 12.

Good to see you guys still think of gamers like my brothers with old televisions :)