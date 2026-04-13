---
title: AI in Swords & Soldiers (part 1)
url: http://joostdevblog.blogspot.com/2010/12/ai-in-swords-soldiers-part-1.html
author: Joost van Dongen
published: '2010-12-31'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

*My blog has passed the 12,500 visitors mark! Awesome! And that in just the first four months! Thank you for visiting, and I hope my posts will remain interesting enough to visit here! ^-^*

Creating good AI for a strategy game is a notoriously difficult task. AI design is of course never easy, but for strategy games, the complexity of options and situations is incredibly high. I think

[Swords & Soldiers](http://www.swordsandsoldiers.com)is the first game for which we achieved really good AI in one of our games, so I figured it would be interesting to see how we got there.

![](../../assets/1ae79cf89fc920ac.jpg)

When I was studying computer science, I had high expectations of how AIs worked. I expected there would be these awesome learning and analysis algorithms, and AIs would make incredibly smart decisions. Then I finally got to an actual AI course...

It turned out that the field of AI either solves really simple problems, like chess (yes, chess is incredibly simple in comparison to a realtime strategy game, let alone in comparison to the real world!), or only offers a huge number of nice and efficient helper algorithms, like pathfinding. Real decision making in complex situations is in essence an unsolved problem and as far as I can tell, it won't be solved any time soon.

Totally disappointed, I wondered how actual game AI was made. It turned out that most game AI is completely scripted. There is nothing intelligent about it. Just long rows of if-then-else-if-then-else. To spice it up and add some variation, some randomness may be put in, but that is not worth the term artificial

*intelligence*either. Games where an AI can really make smart decisions, which were not explicitly scripted by an AI designer, are very rare (Black & White's Decision Trees spring to mind).

So, scripting. Swords & Soldiers is no exception. The trick to scripting an AI is to simply add as many specific situations as possible, and script a smart reaction to each of them. If you can define hundreds of different situations and their reactions, then you can achieve the quality of AI that is seen in most games today.

Now the trick is to script in a smart and manageable way. For a school project I have at some point scripted AI by programming long if-then-else structures in C++, but this was terrible. It takes a long time to program and it is incredibly difficult to have a good overview of this, so it is also very difficult to keep it free of bugs.

![](../../assets/9fbb0e2d8cfc22a2.jpg)

So for Ronimo's first official game as a company (which was cancelled, by the way), we wanted to do things differently, so we put in the LUA scripting language. Adding scripting to your games is all the hype and big games like World of Warcraft contain tons of script code like this. Scripting has the benefit that you don't have to compile any more, and that a game designer can write the AI scripts.

However, I have concluded that LUA is terrible for this purpose. Scripting complex AI in LUA is just as difficult as in C++, so you basically still need a good programmer to do it. Luckily, though, one of our designers has some serious scripting skills. But you still don't have any overview of the structure of your AI, and it is a lot of work to expose all the necessary data from C++ to LUA. As our enemies became more complex, it became more and more difficult to find and fix bugs in them. So that didn't work out either.

Around the time that I was totally fed up with LUA, I discovered a great article by Bungie on how they had built a

[Behaviour Tree system for Halo 2](http://www.gamasutra.com/view/feature/2250/gdc_2005_proceeding_handling_.php). At the time, Halo 2 was well known for its great AI, which would do things like flanking the player and working together as a team.

![](../../assets/72ec8caaee436861.jpg)

The basic idea of behaviour trees is that you have conditions and actions. If conditions are met, then certain actions are executed. In many ways, they are just a graphical representation of an if-then-else structure.

So, we set out to build a graphical behaviour tree editor. (Note that in this case, when I say "we built", I actually mean "an intern built". ;) )

![](../../assets/6153330624ab4f5f.gif)

We are really happy with using behaviour trees. Our designers make the coolest things with them, and as a programmer, I don't need to be involved in everything they want to make anymore. We are using them again in our Secret New Game, even though that is a game in a totally different genre than Swords & Soldiers!

Next week, I'm going to zoom in a bit further on how those Behaviour Trees work exactly in Swords & Soldiers and how they accidentally also became our story event scripting system.

*Edit: here is part 2 of this blogpost:*

[AI in Swords & Soldiers (part 2)](http://joostdevblog.blogspot.nl/2011/01/ai-in-swords-soldiers-part-2.html)

Just wanted to thank you for keeping this blog! As a recent college grad and beginning game designer, this sort of information is invaluable.

ReplyDeleteYou're welcome! :) Good to hear people like reading this! :)

ReplyDeleteThanks for the AI post, very informative.


ReplyDeleteKeep it up ! :)

Very interesting post. I am curious to see how you expand on the topic in the next post. Looking forward to that. ;)

ReplyDelete