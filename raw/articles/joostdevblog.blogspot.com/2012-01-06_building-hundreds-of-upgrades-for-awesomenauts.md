---
title: Building hundreds of upgrades for Awesomenauts
url: http://joostdevblog.blogspot.com/2012/01/building-hundreds-of-upgrades-for.html
author: Joost van Dongen
published: '2012-01-06'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Awesomenauts](http://www.awesomenauts.com), players can buy hundreds of different upgrades. There are around 150 unique ones, and most have two or three upgrade levels, so in total there are probably around 300 upgrades in the game. We wanted our designers to be able to create those themselves, without any work from the programming team for specific upgrades. At the same time, we also wanted the upgrade system to be super flexible, so that the upgrades would be very diverse, and not just all be cooldown reductions and damage increases.

![](../../assets/4f217b3a776bbb4a.jpg)

When we first started looking for a way to build this, I was really at a loss. How to add a flexible system for upgrades to

[our settings system](http://joostdevblog.blogspot.com/2010/12/all-settings.html)? It took some time, but coding intern Daan and I came up with a system that is easy to use and so flexible, that we ended up not just using it for upgrades, but also for temporary boosts and areas with modified mechanics, like low-gravity areas.

![](../../assets/a0ec0f66a451863f.jpg)

The idea is that for every setting, our designers can create modified versions for when a character has certain upgrades. Each setting always has one base value. Then as many modified versions can be added as desired, simply by copying the setting and adding

**@**and the name of the upgrade.

![](../../assets/0ee77de43c10d1ad.gif)

The

**@**sign works for many things, but it has the problem that it is problematic to have different upgrades for the same setting: what should happen if you have both upgrades? So we also introduced the

**+**sign, which means that that upgrade's value is added to the original value. This way several upgrades can influence the same value.

![](../../assets/e0feebb0735f3d1f.gif)

This system does not just allow for simple upgrades that upgrade a single value, but can also be used for more complex stuff. Especially since our designers can give a player a temporary upgrade when he presses a button. So let's say we want to create a skill that temporarily makes the player deal twice as much damage, but also make him half as fast and twice as big. A designer could simply use the name of a single upgrade to modify all of these values at the same time.

Of course, the more flexible and complex things get, the easier it is for our designers to mess up. We have had quite a few bugs where certain combinations of upgrades behaved in a different way than our designer intended, simply because they chose the wrong values. The plus side of these kinds of bugs is that our designers can fix them themselves, so as a programmer I am okay with that... ;)

The upgrade system also gives our artists a lot of flexibility. For example, if a bullet does more damage, our artists can upgrade its graphic and its explosion to use a different animation.

![](../../assets/0edc809a0d8145af.jpg)

The upgrade system described in this blogpost looks pretty obvious to me now, but it definitely was a revelation to us when we came up with it two years ago, and I still think it is the most elegant solution we came up with for any problem at

[Ronimo Games](http://www.ronimo-games.com)so far (although I suppose this system is not unique and other RPGs probably use something very similar). It is incredibly flexible and really easy to use, and allows our game designers to make almost any upgrade they want. And the good thing is that it is not specific to any games, so anything we make with the Ronitech (our engine) will have this feature for our designers! ^_^

Next week, I'll explain the technical side of how we made this upgrade work in C++!

Looking forward to the next post to (finally!) see some code :-)


ReplyDeleteJust curious, have you guys, at some point, considered using an engine like Unity?

Unity gives you a lot of tools to create custom editors for these kind of programmer/game designer issues.

When we started on Swords & Soldiers, Unity wasn't on consoles yet (it even hardly is now), and for Awesomenauts we just continued on the code of Swords & Soldiers. So no, we never considered Unity.



ReplyDeleteAnyway, Unity is not specifically a 2D engine and a proper 2D engine is pretty different than a 3D engine, so we wouldn't use Unity anyway, I think.

I also personally enjoy hardcore programming too much to want to use something like Unity, but that is just personal bias and not a reasonable argument for anything... ;)

Can't argu about that, kinda forgot missing (native) 2D support ;-)


ReplyDeleteIt is posible with 3th party plugins or writing it yourself (as you do have a bit low level acces) but I wouldn't recommand it and stick to what you got.

Just because it is such an awesome mindblowing gametrailer:

Time Ducks (a Unity 2D game ;)

http://youtu.be/evAcp7SX-9A

Interesting article for an awesome game (can't wait anymore!). But I don't understand the @ sign for numeric values, why can't you use only + sign ?




ReplyDeleteIn your example:

shootCowboy_damage = 5

shootCowboy_damage@damageUpgrade = 7

you can also use:

shootCowboy_damage+damageUpgrade = 2

or I misunderstood something ?

In the case of numbers, they indeed do the same thing. The designer can just choose which he prefers. :)

ReplyDelete