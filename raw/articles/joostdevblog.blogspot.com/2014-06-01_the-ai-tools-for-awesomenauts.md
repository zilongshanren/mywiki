---
title: The AI tools for Awesomenauts
url: http://joostdevblog.blogspot.com/2014/06/the-ai-tools-for-awesomenauts.html
author: Joost van Dongen
published: '2014-06-01'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Awesomenauts](http://www.awesomenauts.com)patch (patch 2.5) we will release our AI editor and enable players to load modded AIs in Custom Games. The editor is in beta right now and a surprisingly large amount of new AIs have already popped up. Other game developers can also use our AI editor for non-commercial purposes, or contact us to discuss the possibility of using our tool in a commercial product. This all makes for a great occasion to discuss how we made the AIs and what kinds of tools we have developed for this.

![](../../assets/da293c4438760ad6.gif)

Anyone who wants to give making AIs for Awesomenauts a try can check this little

[starting guide](http://www.awesomenauts.com/forum/viewtopic.php?f=23&t=30440)that explains the basics.

I have previously discussed in two blogposts how we made the AI for

[Swords & Soldiers](http://www.swordsandsoldiers.com)(

[part 1](http://joostdevblog.blogspot.nl/2010/12/ai-in-swords-soldiers-part-1.html)and

[part 2](http://joostdevblog.blogspot.nl/2011/01/ai-in-swords-soldiers-part-2.html)). Since then we have changed some of the fundamentals and those blogposts are well over three years old now, so I will write this blogpost assuming you didn't read them.

When people think about "AI" they usually think about advanced self-learning systems, maybe even truly intelligent thinking computers. However, those are more theory than practice and attempts in that direction are rarely made for games. AI that really comes up with new solutions is incredibly difficult to build and even more difficult to control: what if it uses lame but efficient tactics and thus kills the game's fun? The goal of game AI is not to be intelligent, but to be

*fun to play against*. As a game developer you usually need control over what kinds of things the AI does. Nevertheless, some games have used techniques that can be described as real AI, especially Creatures and Black & White are known for this. I suppose for them it worked because the AI is at the very core of the game.

What almost all games use instead is an entirely scripted AI. The designer or programmer creates a big set of rules for how the AI should behave in specific circumstances and that's it. Add enough rules for enough situations, plus some randomness, and you can achieve a bot that seems to act very intelligently, although in reality it is nothing but a big rulebook written by the developer.

![](../../assets/72ec8caaee436861.jpg)

Awesomenauts is no different. The AI system is a highly evolved version of what we made for Swords & Soldiers. The inspiration for it came from an article Bungie wrote about their

[behaviour systems in Halo 2](http://www.gamasutra.com/view/feature/2250/gdc_2005_proceeding_handling_.php). Something similar was also presented at GDC years ago as being used in Spore and a couple of other games that I forgot the names of.

The basic idea in our AIs is that they are a big if-else tree, connecting

*conditions*and

*actions*. If certain conditions are met, certain actions are done. For example, if the player is low on health and enemies are near, he retreats to heal. If he also happens to have a lot of money, he buys a bunch of upgrades.

These big if-else structures are shaped like a tree and are quite easy to read. Certainly much easier than reading real code. The whole principle is best explained by a screenshot from the AI editor:

![](../../assets/bac8486c55a608a6.gif)

Before we made our AI editor we tried some other approaches as well. In an old school project I programmed the AI in C++, and for our cancelled 3D action adventure

[Snowball Earth](http://joostdevblog.blogspot.nl/2012/10/the-history-of-snowball-earth-now.html)we used LUA scripting. We were quite unhappy with both: although programming gives the most flexibility, creating such big sets of if-then-else rules is just very cumbersome in a real programming language. The endless exceptions and checks quickly become an enormous amount of confusing code.

So we set out to make a tool specifically for making AIs. Our AI editor is structured entirely around these combinations of conditions and actions and makes the problem a lot more workable. It is true that our AI editor is less flexible than code and cannot do certain things (most notably for-loops), but being faster and clearer to work with makes it possible for us to make much better AIs in the same amount of time.

Each type of action and condition in our AIs corresponds to a class in C++. For example, the condition "canPayUpgrade" corresponds to a C++ class called "ConditionCanPayUpgrade". This class looks up the price of the upgrade and the amount of money the player currently has to determine whether the player has enough money to buy the upgrade.

Since the blocks are programmed in C++ they can do very complex things. A core principle is that we try to hide the complexity and performance inside the blocks. If we need to do something in an AI tree that is not possible with simple if-else trees, then we can always add a new type of block that can do that. A great example of this is our block "isCharacterInArea", which under the hood does a collision query and checks for things like line of sight, class and health. There is quite a bit of code behind that block, but to the AI designer it is a simple and understandable block.

Our AI editor evolved and changed significantly from Swords & Soldiers to Awesomenauts. The two biggest differences are the debugging tools and the general structure. At the time of Swords & Soldiers our designers could not see any information on a running AI. To find and debug AI problems they just had to play the game and observe what the AI was doing. AIs in Awesomenauts contain thousands of blocks, so better debugging tools became necessary. Therefore we added the AI observer, internally known as "the F4 editor", since it is opened by pressing F4. The AI observer shows the state of the AI, and we even added a real debugger that can be used to step through AI updates and see the exact path through the AI.

![](../../assets/7862adf2b330fce5.jpg)

The structure of the AI changed as well when we adapted them for Awesomenauts. In Swords & Soldiers the AI trees where "priority trees", similar to those in Halo 2 and Spore. This means that the goal of the tree is to find one action to perform, for example "flee", "attack", "reload" or "seek cover". The top-most action that has all its conditions satisfied is always executed, and nothing else is.

Priority trees are great when an AI should do only one thing at a time, but they turned out to be way too rigid for us. In practice an AI might want to move somewhere

*and*shoot at whatever it passes

*and*observe the situation to make a choice later. Our designers wanted to perform more than one action per tick so badly that they ended up making all kinds of weird workarounds, so for Awesomenauts we ditched the whole concept of priority trees and instead turned it into simple if-else trees. These are not only more flexible, but also much easier to understand.

![](../../assets/be78000b93623161.gif)

The original version of our AI editor was programmed by Ted de Vries, who did an intership at the time and later joined us as a full-time programmer (he currently works on Assassin's Creed at Ubisoft). The AI observer and debugger were also programmed by an intern: Rick de Water.

Next week I will dive into a surprisingly complex aspect of AI: path finding and navigation in a 2D platformer. While standard path finding is pretty easy and can just use A* and that's mostly it, adding platforming mechanics and different movement mechanics per class made this topic much more interesting that we had expected beforehand. Double jumps, jetpacks, kites, moving platforms: we needed something that could handle all of it.

Hi, when you mention that you ditch the whole priority trees to allow more than one actions per tick, does that means it would evaluate all the remaining conditions even if any prior conditions evaluated to true?



ReplyDeleteInterestingly, I implemented a priority trees AI for a RTS game on J2ME mobile phone years back and i was trying to bring down the CPU processing cost of each unit per tick. So essentially each unit takes one tick to execute one action and it would evaluate the next condition in the next tick sorta like staggered processing.

And since we were under time constraint, a cheap and fake way to tweak the difficulty level of an AI is simply by increasing the number of ticks before it can process one action... Haha..

Yeah, we do the entire tree every tick, and we do 10 ticks per second. We spread the AIs out over the frames so they don't all do their tick in the same frame.



DeleteThe optimisation you propose works, but makes AI very unpredictable. If the AI contains a bug this scheme will make debugging a lot more difficult, so I would personally rather spread the individual units out over the frames than spread each AI out over various frames.

In my experience a system like this is very suitable for complex behaviour, but much less suitable for relatively simple behaviour like an individual unit in an RTS. It just takes too much performance for large numbers of units, and RTS units are simple enough to just program them. So for S&S2 the individual units are hardcoded, and the opponent is a behaviour tree.

This comment has been removed by the author.

ReplyDeleteReally inspiring post!

ReplyDeleteThis is a great post! Thank you for sharing these insights into how the AI works.





ReplyDeleteOne suggestion I have which I was wondering if you have considered, and/or wondering if it will be possible with the AI development tools: I think it's relatively easy to make an AI quite effective tactically, but much more difficult to make the AI think well strategically. It's also difficult to make the AI co-ordinate satisfying with human players.

I was wondering if it would be possible to make an AI bot that is the 'pet'/follower of a player. That is, the bot follows the player around, staying as close as possible (hopefully the two have similar movement capabilities). Then the bot assists the player in whatever they are doing -- if the player attacks a turret, the bot does the same, engages in a fight with enemy nauts, the bot does the same, etc.

It would be ideal if the bot could be given basic commands -- e.g. if the player uses the 'Defend' command it would indicate the bot should hold position while the player returns to base / goes get health -- and try to defend it from enemy nauts.

I was wondering what you think of this idea and if it had been considered before?

It is very well possible to create this with the current AI systems. It would mean setting up a new AI from scratch, but it can be done. I don't know whether it would be a good idea for a online matches though, since it might not always result in the best tactical decisions.

DeleteHa, I'm proud my AI made it in the first image onto this post. ^^

ReplyDeleteQuestion. Is it possible to bog the game's processing down by making infinite loops, even though AI runs at only 10 ticks per second?

Of course, if you make AI in the wrong way you can waste a lot of performance. Especially checking large areas is really slow. AIs should never do area collision checks over the entire map at once.

Delete