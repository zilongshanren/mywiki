---
title: All the settings
url: http://joostdevblog.blogspot.com/2010/12/all-settings.html
author: Joost van Dongen
published: '2010-12-11'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Ronimo Games](http://www.ronimo-games.com)we have built a whole suite of tools for designers to work with, and I personally think the settings system is the most important. The nice part is that it was also the easiest to build.

At its core, this is a very simple thing. We have a text file with lots of values that our designers can tweak. For example, for each unit, the designers can set the health, price, walking speed, weapon's range, and a lot more. In

[Swords & Soldiers](http://www.swordsandsoldiers.com), we have some 600 gameplay settings like that.

![](../../assets/a5a437c0f50cdeb4.gif)

A programmer creates these settings, and then a designer experiments with them to choose the right value for each of them. To do that, the designer needs to see the results of his changes quickly. Now I would like our designers to work with that as fluently as possible, so I built the feature that by pressing F5 in the middle of the game, they can reload all the settings. So they can constantly switch between settings and game using alt+tab, and use F5 to reload on the fly. Usually there is no need to restart the game all the time.

Technically, this is very simple to do. The key aspect is to use a struct for the settings and keep pointing to that. Never copy a value from the struct, because the copy won't change if the struct does. Thus when F5 changes the values in the struct, all the gameplay immediately uses the new values.

Depending on your needs, lots of variations to such a settings system can be chosen. In

[Proun](http://www.proun-game.com)I don't have the F5 mechanism, but I do have the possibility to change all the settings per level. So in the third track, I could easily make boosts last twice as long as in the other tracks, which happened to fit the track design better.

One of my first implementations of this system was

[De Blob](http://student-kmt.hku.nl/~joost1/Oogst3D/index.php?file=GAMES/Blob.txt). There we even implemented sliders in the game to allow designers to quickly modify properties, but we learned that as the number of settings explodes, these sliders didn't work that well. Since they were also a lot of work to build, we have simply used Notepad to modify settings ever since.

I would like to also talk about Ronimo's Secret New Game here now, since we have a much more advanced settings system for that, but that will be for another day. After all, the game is still Secret (tm) right now.

A settings system like this is so simple to build, that I think you should even create something like it for the smallest student games. It is also something that you can build once and then reuse in all your games after that. In my opinion, fast gameplay tweaking options are an absolute requirement for good game design.

Something like HLSL UI annotations would be nice here for settings and UI integration. Being able to set the min max ranges for sliders, it could also be advanced by using tree grouping in a similar fashion to VS's #region.


ReplyDeleteYou could always run your main game in windowed mode, then run a second window with tweaking interfaces for these settings. I've done this in the past and it makes it so easy to work with.

This is where unity3D totally kicks arse! :P

ReplyDeleteI suppose they have a cool integrated system for this, then?

ReplyDeleteYeah, since it uses C# all it does is use reflection to expose any public variable as an editable parameter. No work on the programmer side, no work on the designer side. Most of these parameters can be tweaked while the game is running (careful about play mode vs edit mode though).

ReplyDeleteYou should grab the free version and do a basic tutorial. There really isn't much to it at all.

In fact, when I was using Ogre myself I made a unity like editor which did the same thing. It's really very easy when using .net or mono.

F5 is problematic when developing for ActiveX (Browser refresh, probably why you chose it in the first place). Tip: We use F7. It's the least-used key so you won't accdentally execute any functions in explorer, VC++, your favorite editor etc.

ReplyDelete