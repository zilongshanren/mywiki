---
title: Re:creation dev log. 2015. The most productive year yet.
url: https://eliasdaler.wordpress.com/2015/12/31/recreation-2015/
published: '2015-12-31'
source_blog: Elias Daler | Re:creation
source_site: https://eliasdaler.wordpress.com
category: game programming
fetched: '2026-04-13'
---

It’s time to summarize what I’ve done during this year with Re:creation. It has been very good year, I’ve managed to do and learn lots of stuff.

Before I write about the stuff I’ve done I want to thank everyone who followed my progress and provided feedback. This stuff is really important for me and always keeps me motivated. With your support I never feel doubt about my game, I never want to stop making it. Thank you.

Special thanks to SFML community. It turned [my dev log thread](http://en.sfml-dev.org/forums/index.php?topic=18062.0) into a very cool discussion and helped me out with lots of stuff. This level of support is much more than I’ve ever expected and it’s very heartwarming.

I’ll show the most interesting stuff I’ve done and then explain some in more detail.

Some screenshots are taken at different parts of the year, so they may differ a lot!

Some gameplay gifs to get you started:

![](../../assets/88fd73a25135c526.gif)


![](https://i0.wp.com/i.imgur.com/u9CYS5p.gif)


This one is my favorite gif so far. It really shows a lot of stuff I’ve made this year.


#### Graphics/level design improvements

Undead City changed a lot!

![](../../assets/6a2a15648087e0c7.png)

November 2014

![](../../assets/ec707914971832e8.png)

December 2015


As well as the forest. Notice how brighter the stuff is now. And I’ve also drawn a lot of tiles to make it all look more organic and make tile grid less apparent.

![](../../assets/838b3852c54f404d.png)

October 2014

![](../../assets/83ff412ccd1eefad.png)

December 2015

Undead prison changed a lot too. Perspective changed and I’ve also added lots of lightning and details too it.

![](../../assets/1d6754f1830626e2.png)


![](../../assets/06853ecf18146f79.png)


I’ve also drawn indoors tileset and a cafe in Undead City. You’ll hear cool songs from musician and can read some books, or speak with this cute cat!

![](../../assets/76d703c9e58c70ea.png)


I’ve also made fog which provides creepy atmoshere and just looks cool.

![](../../assets/10ea66edbcb17e9b.gif)


I’ve created some new characters this year. Some of them are not yet ready to be showed off, some are just in concept and here are some I’ve shown:

![](../../assets/57b303a8d4c5d66e.png)


**Alan the Blasterous**

This guy really loves explosions! He’s smart and intelligent, but can get a little crazy when he thinks about explosive stuff.

![](../../assets/fb3053815e34f634.png)


![](../../assets/828b6d461dd87c1b.png)


**Master of Recreation**

This man really knows the art of recreation. He’ll teach you a lot of stuff and guide you along your path.

![](../../assets/aba3dc05f3313e7f.png)


**Mysterious cat**

This cat is not just an ordinary cat. Its past is mysterious and you’ll learn about it in the game later.

![](../../assets/4eafc6186e6dcd05.gif)


**Necromancer Grandma**

This old lady will help you greatly along the way. She’ll write down your progress, heal you and revive you when you’re dead.

![](../../assets/2b325dfd0275d562.png)


One big change that I’ve done is changing the perspective from Zelda-style to axonometric (which most SNES rpgs used)

The difference is great:

![](../../assets/cb18e9d327afdb0e.gif)


And here are some of my favourite animations I’ve made this year:

Archer attack animation

![xb8iaq7](../../assets/21a154615855113c.gif)


Side attack animation + death animation

![](../../assets/5830c9d4e250e3e2.gif)



#### Boss battle

I was making the first boss battle which was quite a challenge, because I didn’t want to feel it like an ordinary boss battle, but have some funny moments!

![](../../assets/6ead5614488a1cbf.gif)


![](../../assets/b93a7f1fb78c30e6.gif)



#### Advanced scripting

This witch has lots of script states which let her open the book, turn five pages and then close the book. This is three different animations which have some delays between them, and this is not hardcoded, it’s all in Lua!

![](../../assets/fb2e4ca410a93593.gif)


#### Contextual tips

This is just a small addition which will make stuff less confusing and show you what the interaction/attack button does.

![](../../assets/e6456bfc083ccdbd.png)


#### Archers

Archers were not so easy to make because I wanted to make them just with scripts without hardcoding stuff in C++ code. And I’ve managed to do it! This required lots of decoupling and making some things more abstract, but after all it made my code a lot better and improved scripting support. Now I can do much more with Lua that I could before.

![](../../assets/e73edf6509e0287b.gif)


#### The biggest refactoring/engine improvement in my life

I don’t let my code rot that’s why I always improve it by refactoring, restructuring and decoupling. But I don’t just sit down and start refactoring just for its sake. It happens naturally. Sometimes it’s caused by bugs, sometimes it’s caused by the potential bugs. Refactoring is started by awkward interfaces which let me make mistakes or slow me down a lot.

Some refactoring happens when you implement something cool and then see how it can improve your code. For example, I started making event manager just for gameplay purposes but later figured out that this can help me decouple lots of stuff which led to very positive changes in my code!

But sometimes refactoring is needed when you are stuck. This is what happened this November with my project. First of all, I’ve tried to make fixed delta time for smoother camera movement. I’ve also wanted to make input, collision and other stuff update more frequently than rendering. But this was not possible, because rendering wasn’t completely decoupled and some stuff was just not possible to make with the old system.

As I started to rewrite stuff, I’ve noticed that some global variables were not needed anymore, some loops were easily replaced with **std::find_if** or **std::remove_if**, some raw pointers could be replaced with **std::unique_ptr** and so on.

You can use about this stuff in more detail [here](http://en.sfml-dev.org/forums/index.php?topic=18062.msg139773#msg139773). This post has some modern C++ tips which will make your code better.

And then the other problem came… Compilation times increasingly became longer and longer. I’ve realized that this is not acceptable. But it took me two days of non-stop research to find out what caused long recompilation times. At first I thought that this was a result of coupling, but it wasn’t. (There isn’t much coupling in my engine anyway).

LuaBridge caused long recompilation times because of its template stuff. After some time I’ve managed to reduce them a lot and made some other awesome stuff with Lua. Read more about it [here](http://en.sfml-dev.org/forums/index.php?topic=18062.msg139957#msg139957)

#### Animation editor

Lately I’ve been working on animation editor

![](../../assets/de54aedd3632de41.gif)


This is much more complex than it looks.

First of all, this is Qt with SFML which took some time to set up. But after all, it wasn’t as hard as I expected. I think I will create a tutorial of how to do it later.

Secondly, I didn’t want to make it hardcoded, so I’ve created meta class system which lets me display and edit C++ variables. This is a very generic thing which required me to do lots of hard template programming, but I’ve learned a lot and it will also help me in the main project.

You can find most of the source code to meta system here:

[https://bitbucket.org/edaler/meta-stuff](https://bitbucket.org/edaler/meta-stuff)

I will continue to develop this tool and then it will become full entity editor which will let me easily create new types of entities. I will also use Qt to improve my level editor which was previously made just with SFML.

#### Conclusion

Here’s a diff between two commits which were 1 year apart

![](../../assets/c82c53ae9525d2e8.png)


After all, I think that I’ve spent most of the time programming this year.

Why did I spent so much time programming and not making game? As you can see, I’ve still managed to draw/make lots of stuff. But still, I could have done a lot more. You see, if I just wanted to make a game I would have picked a complete engine instead of using C++ and SFML. Learning programming stuff is important for me because I enjoy it a lot, I learn a lot of C++ and different programming stuff which can be applied to other areas of programming. Using existing engine… not so much.

#### Plans

I’m going to work much more on the game itself next year. The engine is almost done and there isn’t much stuff I really need to add.

I’m also going to spend time improving my drawing, so this will motivate me to devote more time to art and will make my pixel art cooler and character/level design more interesting.

Another thing I want to do is to make a small game to test my engine and make a small game I’ve wanted to make for a long time. It will be related to **Re:creation** and will be free. :D

What do you think of this year? Are you enjoying my progress so far? What do you think I should focus on more in my dev blogs? Leave comments, [write e-mails to me](mailto:eliasdaler@yandex.ru), I’m always interested to hear what you have to say.

See you next year! Cheers.