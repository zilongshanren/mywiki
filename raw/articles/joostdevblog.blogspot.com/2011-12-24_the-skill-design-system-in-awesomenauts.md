---
title: The skill design system in Awesomenauts
url: http://joostdevblog.blogspot.com/2011/12/skill-design-system-in-awesomenauts.html
author: Joost van Dongen
published: '2011-12-24'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

*Note: Swords & Soldiers is currently on sale on Steam! 50% discount!*^_^ )

At

[Ronimo Games](http://www.ronimo-games.com/)we always try to make innovative games, and in my opinion one of the biggest challenges when doing so is how to enable the game designers to do their work. Game designers work with things like game mechanics and control schemes, but you cannot know whether what you designed on paper is a good idea, until you played it and experimented with. It requires programming to create something playable, so unless a game designer is also a programmer, he cannot really do much on his own.

For artists, this problem has pretty much been solved: graphics tools are so powerful that artists can create most things without need of a programmer (except maybe for polish and performance). For game design however, this is essentially an open problem. There are many methods to empower game designers, but none are ideal. To name a few: scripting lanuages, event based systems, tools like Gamemaker and Virtools, and the most used of them all: just copying

*everything*from existing games and not even trying to be innovative in any way (this also solves a lot of other issues, like the problem of being creative and taking pride in your work).

The approach we use to enabling game designers to create stuff is not ideal either, but it does work really well for us, so I'd like to write a couple of blog posts about the systems that allow our game designers to create game mechanics. Today is the first, and it is about our skill system.

To us it all starts with the coders and the game designers working together closely. Now whenever a programmer builds something, we set it up as flexible as possible, and make settings to control it. Things like speed, size, health, cooldowns and whatever else we can think of are put in settings and our game designers can edit those. Last year I wrote

[a post](http://joostdevblog.blogspot.com/2010/12/all-settings.html)about our settings system in

[Swords & Soldiers](http://www.swordsandsoldiers.com/)that explains the basic idea further.

However, the way we approached this in Swords & Soldiers was also quite limited. All actual behaviour was programmed specifically per unit, so the only thing our designers could do, was tweak them. If they wanted to create a new unit, or even combine properties from existing units, they had to ask the programmer (me) to implement this for them.

![](../../assets/9c18adc6bab66c3f.jpg)

In

[Awesomenauts](http://www.awesomenauts.com/)we set out to make things more flexible. A character in Awesomenauts mainly consists of a list of skills, and which button needs to be pressed to use that skill. We have programmed around 20 skills (things like

*Shoot*,

*Hit*,

*Jump*,

*Dash*and

*Shield*), and designers can create new versions of each skill with separate settings. Designers can also attach several skills to one button to create combinations, so maybe there is a combo skill that shoots a bullet and starts a shield at the same time.

![](../../assets/554ed7bfdc556807.gif)

In this trailer you can see how Sheriff Lonestar's set of skills works out in the actual game:

Each of the skills refer to a group of settings that define the exact properties of that skill. So there can be many different

*Shoot*skills, each with different settings. This way some become grenades, other bullets, lasers or mines, and some even spawn new creeps.

![](../../assets/b1889c92470cc3af.gif)

Now this is really flexible, and I guess it is quite obvious that building it like this works much better than hardcoding the entire character as we did in Swords & Soldiers. The trick to making this really flexible, though, is to make

*lots*of settings. Throughout development of Awesomenauts, we have constantly been adding new settings to make the existing skills more flexible, so that more things could be made with them.

However, it may seem so, but working like this is not an Obvious Good Idea (tm). It has some serious downsides as well, which all boil down to one thing: skills can be combined in any way and this makes all character code infinitely more complex. If you have 20 skills, then designers can already make 400 combinations of two skills happening at the same time. You can see where this goes once every character has 10 skills...

So implementing this system cost us an enormous amount of time to get all the combinations to behave correctly. A good example of the complexity here is animations. How to choose which animation to play when several skills are active at the same time? There are so many combinations that we kept bumping into situations where an animation did not look good or work correctly because some other skill interrupted it in the wrong way. This is very solid in the final game, but it took us a lot of work to get there. Unfortunately, it is still very fragile code (i.e. it is easy to introduce bugs when working with it).

Another downside of this system is that if you want it to be really flexible, then you need dozens of settings for each skill. The more settings there are, the more difficult it becomes for the game designer to keep track of what each does exactly. During development it happened quite often that our designers asked for a feature that was already there.

Of course, the upside of this is that with so many settings, there are many combinations that achieve totally unique things. Especially the

*Shoot*and

*Shield*skills have been applied by our game designers to do totally different things than what I expected when we programmed them.

So choosing between the flexibility in Awesomenauts and the very inflexible system in Swords & Soldiers, I actually don't think the flexible system always wins. I would even say the system in Awesomenauts might be up to

*three times as much work*.

However, if, like we did in Awesomenauts, you want to spend a lot of time iterating on the game design to find the most fun and varied units, then more flexibility is definitely necessary. So I think we made the right choice for Awesomenauts. It is a choice that cost us a lot of development time, but that also improved the game's quality enormously.

Great blogpost!



ReplyDeleteSometimes I wonder how other devs would tackel different problems. The main problem described here is very familiair and its good to hear you solved it like I would. Though that still doesn't mean its the right (or wrong) way to do it ;)

I think its important to do just that what works for you. The next time you would probably do some things different and thats what its all about; you live you learn.

I don't know whether this is the best solution either, but a nice side-effect of that it is so flexible, is that we can use the entire system for future games. For example, if we would make Swords & Soldiers now, we would just use the Awesomenauts character code and make them behave like S&S characters. :)

ReplyDeleteAren´t these the kind of things that would be really handy to always have inplemented in your engine? Or would that be a silly question?

ReplyDeleteDepends on the kind of game. Many games don't need a skill system. And for most games, you would want something that fits the game you are making quite closely. So no, I don't think this is part of a game engine. I think this is more part of your gameplay code than your engine code.

ReplyDeleteAt GameHouse, we did the same thing for the Delicious series. I know they look like 'simple' games but our appliances can get pretty hectic, you can combine any product queue and cancel it etc.



ReplyDeleteWe also have to 'additive' settings you describe in your other post. We also do 'multiplicative' in our upgrade system.

Using our very flexible Lua binding, it all becomes a bit easier though :-)

Interesting, another studio that does something like this! Thanks for replying, Luc!


ReplyDeleteWhat do the Lua bindings do exactly for the upgrade system? And what happens when a single upgrade has both multiplicative and additive upgrades? Do you have a fixed order for how to combine those, so that your designers know what is going to happen?