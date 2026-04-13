---
title: Optimisation lessons learned (part 3)
url: http://joostdevblog.blogspot.com/2012/07/optimisation-lessons-learned-part-3.html
author: Joost van Dongen
published: '2012-07-21'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[part 1](http://joostdevblog.blogspot.nl/2012/07/optimisation-lessons-learned-part-1.html)and

[part 2](http://joostdevblog.blogspot.nl/2012/07/optimisation-lessons-learned-part-2.html), today I bring out the big guns: threading and timing! This is where optimisation really shines as a form of pure entertainment and delight. I can honestly hardly imagine why anyone ever does Sudokus or crosswords. Puzzling to find the best optimisations is so much more fun!

![](../../assets/e5d5a281af095e7b.jpg)

**Hiccups are horrible without the right tools**

Framerate hiccups are a special case. This is when the game is running at a high enough framerate, but once in a while a single frame takes a lot longer. Hiccups cause that a game running at 55fps might look a lot less fluent than one running at 30fps, if every second the 55fps consists of 54 smooth frames and one really long one.

The difficulty here is that when you gather performance data, the time spent in each function will usually be averaged. This means that if a function runs really fast most of the time and is really slow only once per second, then it will look like a normal function in a profiler. So to fix hiccups, you will need an overview of all the frames captured, and the option to analyse them individually. Not all profilers are capable of doing this, but if you have one that does (like the excellent Playstation 3 profiler), then finding the cause of hiccups isn't all that difficult.

The important thing here is the realisation that preventing hiccups is at least as important for having a smooth feel to the game as having a high framerate, so you really need to make sure hiccups are rare enough. In the

[Awesomenauts](http://www.awesomenauts.com)Beta that is currently running, the most important hiccups are when new players join (both when they enter character select and when they enter the actual game). We are working on decreasing those hiccups, but the good thing here is that they only happen once every few minutes. Beware of hiccups that happen once every second!

**CPU time versus real time**

This is an oddity in some profilers that caused me to make some seriously wrong judgements on where performance was going. An extreme example is the following. I was calling

*SDL_GL_SwapBuffers*, which finishes rendering a frame and shows it on the screen. According to my profiler, 0% of the time was spent there, so I concluded I didn't have to worry about it. This was totally wrong. It turned out that the profiler measured actual time spent using the CPU, so when a function simply waits or sleeps, then this profiler would not count that. When I discovered this, I quickly learned that

*SDL_GL_SwapBuffers*was actually using 50% of the time in my game. This function was waiting for the videocard to finish rendering, and the solution was to massively decrease the overdraw. (Note that the videocard usually does not wait for the

*last*frame to finish, but an earlier one, as I explained in

[this previous blogpost](http://joostdevblog.blogspot.nl/2011/10/what-no-one-told-you-about-videocard.html).)

So be aware that sometimes profilers show the time spent using the CPU, and sometimes they show the actual time on the clock that it took for a function to finish. Keep this in mind!

**Multi-threading makes everything very complex**

This also brings us to the one thing that makes optimisation truly complex: multi-threading. Again, this is best explained through an example. The Ronitech (our 2D multi-platform game engine) has two main threads running: the rendering thread and the game thread. At the end of every frame, these threads wait for each other to finish. The threads never take exactly the same amount of time, so in practice one thread waits a bit every frame. This means that on a multi-core processor, optimising the fastest thread does not increase the framerate

*at all*.

So before optimising a multi-threaded game, you should always get a clear view of who is waiting where and for what, and then you should only optimise the things that cause the waiting.

![](../../assets/2dd9ba9fe1ba9a28.gif)

Luckily, modern consoles are so fast that for smaller games, you often won't need a lot of multi-threading. Everything relevant in

[Swords & Soldiers](http://www.swordsandsoldiers.com)was done in just one thread. Awesomenauts is a lot larger and more complex, though, so we now have three threads running at all times. In general, unless you are making something relatively big and are in a larger coding team (

[Ronimo](http://www.ronimo-games.com/)currently has five programmers), you won't need a lot of threading and can thus skip this kind of complexity.

Which brings us to the end of this series of the most interesting lessons I learned while doing optimisation! For posts somewhere in the future I still have two more optimisation topics that I would like to discuss: one with practical examples of (simple) optimisations that worked well for me, and the other with a detailed look at our memory manager, which turned out to improve the framerate a lot without being very complex to make. For now, I hope this was an interesting wall of text about the sensual joys of optimisation!

I solved the sudoku :)

ReplyDeleteReading this blog is thrilling as always :)

ReplyDeleteI saw that you often mention the method SDL_GL_SwapBuffers. Are you using SDL on game consoles? If so that's pretty cool, i didn't know sdl would work on them

Oh, no, that function is called differently on PS3, but it does the exact same thing. PS3 also supports OpenGL after all. 360 is DirectX, but it also has an equivalent of SDL_GL_SwapBuffers.

DeleteHé Joost,



ReplyDeleteZiet er goed uit, pimpin'.

When you're running a rendering and a "game" thread – as you call it – which tactic do you use to ensure that the modification by the latter does not affect the state the former is rendering? Do you "clone" the state before every cycle?

There is indeed a synchronisation phase. I am not super happy with the time that takes, but I wrote a blogpost about how that roughly works in the Ronitech (our own engine): http://joostdevblog.blogspot.nl/2012/03/question-how-to-synchronise-between.html

Delete