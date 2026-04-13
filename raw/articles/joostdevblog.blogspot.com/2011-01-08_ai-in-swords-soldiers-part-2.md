---
title: AI in Swords & Soldiers (part 2)
url: http://joostdevblog.blogspot.com/2011/01/ai-in-swords-soldiers-part-2.html
author: Joost van Dongen
published: '2011-01-08'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Swords & Soldiers](http://www.swordsandsoldiers.com), but I didn't really dive into how they actually work. So now let's have a closer look at how we worked with them.

![](../../assets/b7ca0b4e9e9eee5d.gif)

The small AI above gives a nice example of how our AIs work. The first thing to note here, is that behaviour trees are based on priorities. It is assumed that the AI will always want to perform the top-most action and will not look any further if that action can be executed. In this case, the action at the top is shooting lightning at a Necromancer (

*useAbility*). Necromancers create lots of skeletons, so killing them first is usually a good idea.

To make this priority system work, the action at the top must have strong requirements, for otherwise the actions below it will never be executed. In this example, this is indeed the case: lightning is only used if an enemy Necromancer is actually near, and if you have enough mana to shoot lightning.

Since the AI must also mine gold, the action below that is building workers (

*createUnit*). In Swords & Soldiers, players cannot have more than 10 workers, so as long as the AI has less then 10 workers (

*unitCount*), and it has enough gold (

*goldAmount*), it will build one worker every ten seconds (

*timeSinceLastUnit*).

Finally, whenever not shooting lightning or building workers, this AI will just pump out as many Berserkers as possible (

*createUnit*, at the bottom).

Now the fun of this system is that these behaviour trees are quite simple to work with, so you don't need a programmer to make them. You do need a designer who is good a logical thinking, but that is something I think every designer worth his salt should be good at in the first place.

The key to make keep these trees manageable, is to have enough blocks to work with, and to hide all complexities inside these blocks. A simple example is the

*unitNear*block. The C++ code for this block looks for all the enemy Necromancers in the level and calculates the distance to each of them, to see whether there is a Necromancer near. The complexities of finding the Necromancers and such are hidden in a C++ class, and the designer doesn't have to know anything about that.

In Swords & Soldiers, I think we did not do this very well, though: our skirmish AI is incredibly large and complex. By having more and smarter conditions and actions to work with, I think our designers could have made some trees in half the size.

![](../../assets/c8724b5ad03e6fd1.gif)

An interesting side-effect of these trees, is that they are also excellent for story scripting. Swords & Soldiers often triggers little cut-scenes with dialogues and such in the middle of a level. Deciding when the trigger those, can easily be done inside the behaviour tree, since the behaviour tree already has all these actions and conditions.

Initially, I was strongly against this idea, because I wanted to keep the AI clean and not mix it with cut-scenes. I thought this would get too messy and unclear. However, our designers convinced me to do it that way anyway. In retrospect they were completely right: it is very simple to trigger and play cutscenes with this system.

![](../../assets/2f8c038b08885369.gif)

Finally, let's have a short look at a big change we made to the behaviour tree system for Ronimo's Secret New Game. While working on Swords & Soldiers, we struggled with how to make an AI do several things at once. It makes sense for an AI to build units while also casting spells at the same time. Because of the priority system, doing this kind of thing gets very messy. The priority system really only works if you always want to do exactly one thing at a time.

Working around this made the AIs pretty unreadable at some points, so for Ronimo's Secret New Game, we removed the priority system altogether. Instead, we now simply have a big if-else tree. It still has conditions and actions and looks very similar, but the AI does not stop when it has found an action it can execute. This is a lot more readable and also made it easier to add else-structures. In Swords & Soldiers, we essentially only had if-then structures, while we now also have if-then-else structures.

Let me conclude by saying that we are incredibly happy with our behaviour tree system and our own editor for it, and we will keep using this for several games to come.

In the end, this also means that the actual behaviour of our AIs is scripted by our game designers. For Swords & Soldiers this was mainly Jasper, but also a lot of it by Fabian and Tom. For me as a programmer, it is great to see how designers can make all kinds of awesome things with the tools we provide. Our designers constantly surprise me with how much more they can do with those tools than I myself considered even possible! So the real credit for the great AIs in Swords & Soldiers of course goes to our designers! ^-^

Good work, AI is a tough job

ReplyDeleteReally fascinating. Any chance you'll release your tools so we can use them? :P

ReplyDeleteThanks for sharing! Just curious what UI library did you use for tree editing interface?

ReplyDeletewxWidgets in C++. I guess it would be better to do this kind of thing in C#, though. C# seems like the standard for tools these days. People tell me it's a lot faster for these kinds of things.

ReplyDeleteAt the same time .Net means you can run your editor on Windows only which is sometimes unacceptable :)

ReplyDeletepachanga: Use Mono

ReplyDelete