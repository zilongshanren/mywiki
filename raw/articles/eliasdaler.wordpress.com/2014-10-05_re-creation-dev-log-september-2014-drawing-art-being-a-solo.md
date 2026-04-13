---
title: Re:creation dev log. September 2014. Drawing art, being a solo dev, fixing
  bugs.
url: https://eliasdaler.wordpress.com/2014/10/05/recreation-dev-log-september-2014/
published: '2014-10-05'
source_blog: Elias Daler | Re:creation
source_site: https://eliasdaler.wordpress.com
category: game programming
fetched: '2026-04-13'
---

Lots of time passed since the last dev log. How’s the game? It’s doing pretty well.

Some things changed, the most notable thing is that I’ve become a solo gamedev now, because the artist abandoned the project. Every sprite you see in the latest screenshots was drawn by me.

![](../../assets/3467bfaa8a4a93b5.img)


Being solo dev is hard, very hard. I spend lots of time practicing art, drawing sprites, animating them and trying to make them as good-looking as possible without spending too much time. And I still have to do programming, scripting, designing and story writing!


But it’s great I’m able to draw something that looks pretty decent. Some people said my game looks awesome and this is very nice to hear. I’m still trying to improve my art skills and the difference is very noticeable. Look at the progress yourself:

![](../../assets/663911527977c077.png)


![](../../assets/821e90ede6a05e07.png)


Switching from 2-frame walking animation to four frames was pretty neat too!

![](../../assets/6368f9e24cdaa0f8.gif)

![](../../assets/71966dfd9995a44e.gif)


![](../../assets/3a6b6626d647c9a0.gif)


Now for programming side. I spend lots of time fixing memory leaks. I used **Valgrind** and was pleasantly surprised to find out that there weren’t too many memory issues and most of them are fixed now. One of the reasons I don’t have lots of problems with memory is because I use smart pointers most of the time. They do a great job and I don’t have to worry about deallocating memory manually most of the time. Resource manager is working great too. I don’t have to manage resources manually, they just get loaded when some objects need texture or sound. Smart pointers to this resources are stored in ResourceManager class and I can check how many object uses some particular resource at the moment. If it’s reference count is one (ResourceManager reference) I can safely deallocate this resource. Pretty neat.

I also worked on documentation for some time. Some C++ functions can be called from Lua scripts (something like setAnimation, setHealth, etc.). This will be useful when game comes out. People will be able to write their own scripts. The game is very data-driven so it’s quite moddable. It’ll be interesting to see what people can do with my game!

Lots of time was put into scaling for different resolutions. Original resolution my game uses is 256×240. But if was problematic to run my game in 800×600 resolution, so I implemented letterboxing. Turns out, some things don’t work properly for some resolutions and I needed to fix them. And I did it (though there are some left).

And then I worked a little on the level editor. When I run my game in 800×600 the game still runs in 256×240 but scales up to this resolution. But when I switch to editor, resolution is 800×600 which means, I can zoom in and out which makes levels easier to modify.

![](../../assets/600955f362595264.gif)


I also implemented undo! This took me a while, but it’s totally worth it. Undo was implemented with [Command Pattern](http://en.wikipedia.org/wiki/Command_pattern) and even made my code cleaner!

![](../../assets/89135cb47d22dea5.gif)


It’s not that hard to implement and I think I’ll write an article explaining how I did this. But writing article about this is pretty hard, because some things depend on the structure of my engine, on entity/component system particularly, but I’ll try to make some clear examples.

And this is pretty much it. I now have most things I need to build fully playable demo! The only thing I need is content: art, mostly. That’s what I’ll do for the most of the time now. But it’s pretty cool because the progress is more noticeable for me and other people. More screenshots, more interesting things to show! Pretty great! This things take time. I value quality more than quantity.

[Follow me on twitter](https://twitter.com/eliasdaler) for more updates! See ya.