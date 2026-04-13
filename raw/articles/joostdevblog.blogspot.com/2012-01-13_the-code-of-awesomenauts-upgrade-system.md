---
title: The code of Awesomenauts' upgrade system
url: http://joostdevblog.blogspot.com/2012/01/code-of-awesomenauts-upgrade-system.html
author: Joost van Dongen
published: '2012-01-13'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[I explained](http://joostdevblog.blogspot.com/2012/01/building-hundreds-of-upgrades-for.html)how our designers can create tons of upgrades for

[Awesomenauts](http://www.awesomenauts.com)using our Settings system. However, I didn't say a thing about how we actually made that work. We used some fun template and functor tricks there, so I figured it would be nice to show how it was built to work elegantly, without making our code a big mess of checks for upgrades.

*Warning: this blogpost contains hardcore programming awesomeness! If you are an artist or game designer and fear templatised meta-programming functors might disintegrate your brains and/or explode your head, then I advice skipping this specific blogpost and coming back next week!*

First lets have a look at how things would work without upgrades. Note that to keep things readable, I only show the essential bits of code, and I have greatly simplified all the code examples here.

![](../../assets/ef47de311f9e37ae.gif)

The function

*loadSettings()*translates from a variable name to a string, so that we can actually load the variable from a text-file. Doing this for every setting in the game is a bit cumbersome, but necessary because variable names in C++ are not real things and become simple memory addresses when the code is compiled. Some spot is needed where we have the variable name as a string in code, and I chose to put all of those in a single place in the function

*loadSettings()*. I guess it might be possible to write a macro that does the same thing, but I don't know about that myself.

The key thing to notice here is how easy it is to use the settings in gameplay code, as can be seen in the function

*handleWalking()*. We are going to add upgrades to this and out most important goal for that, is to keep the gameplay code this simple.

Since the upgrade system requires each setting to be able to have several upgrades and combine them, we switch the settings from a simple

*float*or

*bool*to a real class.

I want basically the same behaviour from

*floats*,

*bools*,

*strings*and any other types that need to be upgradeable, so I used templates for this. Experienced programmers probably know what templates are, but for those who don't: in the code below the type

*T*is left open and it can be interpreted as whatever we say it is. So we can make an

*UpgradeableSetting*where

*T*is a

*float*, or where

*T*is a

*bool*, or something else. C++ can compile this code with any type we want it to.

![](../../assets/51feb707dd5db277.gif)

The

*load()*function fills

*baseValue*and

*upgrades*by looking for all the occurrences of the setting in the settings file.

The

*get()*function returns the value that this setting has for the

*Character*that is passed to it. The

*Character*is needed here, because we need to check which upgrades he has and return a different value depending on that. Its code is rather simple, but seeing it might help understanding how this works:

![](../../assets/be20c69c67d740c4.gif)

Note that this code only handles upgrades that replace the standard value, so upgrades that are marked with

**@**in the settings file. For simplicity, I have left out upgrades with

**+**(which add to the original value) that I discussed last week.

Now that we have this, we can make some slight modifications to our gameplay code to use the upgraded value:

![](../../assets/d50545540485c023.gif)

This all works fine, but I am not all too happy with that function

*get()*. Normally it would be perfect, but there are so many places in the gameplay code where settings are used, that I would rather not add

*get()*to all of those.

Now C++ happens to have a nice solution for this. I rarely see it used outside STL, but it has an absolutely awesome name: "functor". I love that name! Got to be a

[Decepticon](http://www.motifake.com/image/demotivational-poster/0904/decepticons-demotivational-poster-1239679582.jpg)! Anyway, a functor is a construction where you can call an object as if it is a function. With a functor, our little class looks like this:

![](../../assets/60367f3987f8ebef.gif)

Now we can do the exact same gameplay code as before, but we can simply leave out the

*get*call. For the rest, this code does the exact same stuff. Because we use the settings so often, this is a nice improvement.

![](../../assets/09dc4aeba67c03ab.gif)

Since we have so many settings in our game, typing the entire type every time is too much work, since that would be something like

*UpgradeableSetting*every time. We simply solved this using

*typedefs*. At Ronimo we normally try to avoid typedefs, because they hide the real type of a value and I would rather know exactly what I am dealing with. However, because there are thousands of settings, I consider this an exception and use typedefs anyway:

![](../../assets/5d54f830cdb6b04f.gif)

Now that we have this new class, let's have a look at the same code we had before, but now with the upgrade system added to it. Note how it has hardly changed, but can do so much more now!

![](../../assets/a021296bd50c3fd4.gif)

So, that's it. It's just a little bit if code, but this makes the settings system way more powerful and flexible. It is definitely a great improvement to the RoniTech (the engine we created here at

[Ronimo Games](http://www.ronimo-games.com)and that we used to build Awesomenauts). In fact, its uses are so diverse that we also use it for many other things than the upgrades that the player can buy in the shop. So let's conclude this blogpost with this nice example of that:

![](../../assets/1bed474643fbd83d.jpg)

Pretty neat.



ReplyDeleteYou could, if necessary, compare by ID rather than string in the get/functor call.

regards bk

Wow! Incredibly helpful example of great usage of C++ typedefs and function objects to create simple to use but highly expandable systems! I'll definitely keep this around for the next time I'm working with C++. Could you please submit this article to AltDevBlogADay so I can print it out?

ReplyDeleteI don't know what AltDevBlogADay is exactly, why would I want to submit something there?

ReplyDeleteFirst of all I want to tell you I love reading your posts, grate info.

ReplyDeleteI'm really intrigued why you have canWalk in settings .

For most characters, canWalk is indeed not relevant, but there are some useful applications for it: whenever Derpl switches to turret mode, he cannot walk any more and this setting is set to true through an upgrade, until he switches out of turret mode. Also, some summons in the game cannot walk, like Gnaw's plants and Voltar's healbot.

DeleteHi Joost,







ReplyDeleteI'm not a very experimented game programmer and I try to create a system as the one you describe in this post.

It works quite well and I really want to thank you to share this as this really inspire and motivate me to do something similar.

I struggle actually in something maybe obvious for you but I don't see the point, please can you help me ?

I tried to make a Dot system (as the one of Gnaw), I first thought about adding something like a "lifeIncrementCoef" setting (set to 0 as a base value) on the character.

The bullet will add an extra upgrade on the character touched and change this value to something like -5.

I have something like:

lifeMax = 100

lifeIncrementCoef = 0

lifeIncrementCoef+dotUpgradeA = -5

This works until I want to make some changes to this attack and add upgrades on it..

If I want something like lifeIncrementCoef+dotUpgradeB = -3

I'm not sure if my attack adding another extra upgrade called dotUpgradeB is the good way to go (even if, managing that using your great setting system seems tricky to me)

Do you think it's a good idea ? Maybe I try to do something really weird here ?

DoT is such a specific thing, that we simply implemented it separately, like all status effects we have. When it is 'hidden' in the upgrade system, it becomes very difficult to do things like cleansing DoT, showing how much damage the character is still going to take from the DoT, or handling stacking behaviour. With DoT in games, it is usually the case that one type of DoT cannot stack with itself. So receiving poison DoT twice at once will ignore the second poison DoT, while receiving a poison DoT and a burn DoT will apply both, since they are different types.




DeleteThings like that are just too specific to not implement specifically, in my way. Trying to hide them in something general makes tracking bugs and adding features very difficult.

When a character receives 'damage' in Awesomenauts it is actually a list of things. Some of those:

blindTime

damage

dotTotalDamage

dotDuration

dotNumberOfTicks

stunDuration

slowFactor

slowDuration

snareDuration

The Character who receives this has member variables (not settings) for each of those and just applies and updates them.

Thank you for this quick reply. You're right, I think it's the risk when discovering something new and great: want to use it everywhere even if it's not the most suitable in some case.



DeleteI will scavenge my old DoT system.

BTW, I forget to thank you for making such good games.

(I stopped play LoL since the release of Awesomenauts)

Thanks again and keep going on Celio fortress, the concept is awesome.

Yeah, I think one of the biggest challenges in good gameplay programming is the balance between generic solutions that can be used for many things but are difficult to code/debug/maintain/use, and more specific solutions that are much simpler, but also very limited. Its a constant struggle to find the right balance, in my experience.

Delete