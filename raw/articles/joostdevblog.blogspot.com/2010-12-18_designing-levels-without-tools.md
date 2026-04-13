---
title: Designing levels without tools
url: http://joostdevblog.blogspot.com/2010/12/designing-levels-without-tools.html
author: Joost van Dongen
published: '2010-12-18'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Proun](http://www.proun-game.com)I am all alone and at

[Ronimo Games](http://www.ronimo-games.com)we have relatively too few coders to really work comfortably. So getting the maximum result out of a minimum effort is incredibly important.

When we built

[Swords & Soldiers](http://www.swordsandsoldiers.com), we didn't have a level editor yet. We have our own 2D engine at Ronimo Games, the RoniTech, but the RoniTech 1 that is used in Swords & Soldiers was still very bare bones at the time. We are currently working with and on the RoniTech 2 and have lots of cool in-game level editing and graphics editing tools, but for Swords & Soldiers we had to come up with some smart workarounds to design level graphics without having a real tool to do it with.

The core information of a level is where goldmines and towers are, what the height of the landscape is, and what type of ground it is (rock, snow, grass, etc.). We made designing this possible in a crude and simple way: in a Notepad file, each line contains information about one of these categories. Since the game essentially plays on a line, this is actually very simple to understand and edit and worked really quick for our designers.

![](../../assets/aeaf25b49e591d70.jpg)

To give our artists some room to create places of interest in the level, I gave them the possibility to define the exact position of props as well. They had a couple more lines for this and a prop sheet with a character per prop. By typing these characters in Notepad, they placed props in the level. This has an incredibly hardcore hacking feel to it, but I simply didn't have the time to create anything better (creating an entire console game with only one full-time programmer is, euhm, interesting...). It did give our artists enough freedom to make some fun areas, though, so the results were good.

![](../../assets/22512e4bf0b00c1b.jpg)

The final part of the levels is the backgrounds (and foregrounds). We have lots of parallax layers and each layer is at a different distance from the camera. Also, the background layers often contain loads of objects per level. Since perspective is involved here, Notepad was out of the question. And without a graphical tool to design that, we had to choose a different solution here.

We came up with a procedural system where artists would create background elements for different layers, and the game would place these elements at random positions in their layers. Artists described to me which layers they wanted (nearby trees waving in the wind, medium distance hills, far away mountains, clouds, etc.) and I created code to place them. I did give our artists the possibility to remove layers or make them extremely dense, so that they could create deserts, mountain areas and forests.

![](../../assets/4d4f99050e9f15df.jpg)

The obvious downside of this approach is that it is very difficult to create unique places per level. With a real graphics level editor, artists could have placed specific eye-catchers in certain levels, like a city in the distance, or a palace just behind the field of war. This was impossible with the lack of tools for Swords & Soldiers.

Since we have a limited amount of background elements to generate levels from, repetition looms. So the artists requested two forms of control over that: one is simply a background gradient per level. The other is an atmospheric fog gradient, also per level, that is overlayed over the objects that are further in the background.

![](../../assets/90963ddea0493ae2.jpg)

Despite the limitations, we managed to create a game with rich graphics that got great review scores. The smart choices described above made it possible to achieve that with only one programmer, which I am really proud of. Obviously, though, the real credit goes to our art team, who made some really compelling artwork. To quote IGN: "One of the best-looking games on Wii."

(Did I already mention I feel very proud of Swords & Soldiers? ;) )

*PS. For those interested in some of the most hardcore programming topics: Jelle van der Beek, lead engine programmer at*

Your posts always give me the tricks I need when I need them. Good luck and thank you very much !

ReplyDeleteVery interesting post. It's always good to see the simple stuff still works!

ReplyDeleteThe challenge is to find those simple things that don't totally destroy your game by having too few options, I suppose. :)

ReplyDeleteJoost, could you tell me how you managed to programmatically create the curves in the ground so smoothly?

ReplyDeleteIt's a triangle strip. So there are lots of polygons there to achieve that effect.



ReplyDeleteAlso, to achieve a smooth curve, I don't use the heights that the level designer set directly, but first blur them. So each height value is averaged with the values near to it.

Finally, our artists drew small hills and height differences and such in the tiling texture that is applied to the landscape. This hides the smoothness of the curve and makes it look a lot more natural.