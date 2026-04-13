---
title: The many faces of balance in an RTS
url: http://joostdevblog.blogspot.com/2011/01/many-faces-of-balance-in-rts.html
author: Joost van Dongen
published: '2011-01-13'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

*We are growing our team a bit further and are looking for yet another programmer at Ronimo, to write platform-specific code for the Xbox 360 and Playstation 3! This time someone with good knowledge of C++ and a couple of years of programming experience (though not necessarily in the games industry). Click*^-^

[here](http://www.control-online.nl/jobs/job/445/programmer-for-console-game-development-at-ronimo/)for more info!I guess anyone who has ever played a strategy game, has an idea of how complex balancing the powers of three very different factions is. However, while we were developing

[Swords & Soldiers](http://www.swordsandsoldiers.com), I learned that there are several other forms of balance, and an RTS needs to achieve them all at once.

The balancing was done by my colleagues Olivier, Jasper, Fabian and Tom and I learned a lot of this from them. Especially Olivier is a hardcore Starcraft player and he brought in a lot of knowledge of what he had learned by following Blizzard's patches and articles on the topic over the years.

So, let's have a look at some of the many forms of balance in an RTS!

**1. Faction balance**

This is the standard balance that most people mean when they talk about balancing an RTS. Swords & Soldiers has three very different factions: the Vikings, Aztecs and Chinese each have different units and spells and even collect mana for their magic in different ways. The factions may be very different, but if you are a good player, then you should be able to win with each of them. So who wins is decided by your skill, not by which faction you play.

![](../../assets/15c11581e1927c3d.gif)

**2. Beginner balance**

While standard balancing looks at the situation for good players, it is also interesting to look at beginners. How difficult is it to play with a faction at all? In Swords & Soldiers, we deliberately chose to not make the game balanced for beginners. The Vikings are our easiest faction to understand the basic strategies, while the Chinese are a lot more difficult to play with. We wanted to add variation and spice to the game by making the factions different in complexity of the core strategies.

Interestingly, becoming really good is most difficult with the Vikings. Although their basic strategies are easy to understand, their pro strategies are probably the most complex, requiring more skills and units to be combined.

**3. Balance between tactics**

Each faction should have many different useful tactics, and most of the time, several viable options should be there for the user to choose from. If a faction is only strong with one specific tactic, then you always play that and the game gets boring. Also, the opponent will know exactly what to expect. So there is not just the balance between factions, but also the balance inside a single faction, where all units and many tactics should be of use.

**4. Balance on different maps**

When the game is balanced on one map, the balance might be broken on another. For example, in Swords & Soldiers, the Chinese need towers to get mana, so a large map with lots of room to build and defend towers makes them stronger. To reduce the complexity of balancing, we balanced for one particular map (the first medium map) and added the other maps for flavour and variation. In online multiplayer, we only allow for 4 of the 9 skirmish maps, because we think the balance is best on those 4 maps.

**5. Early game balance versus late game balance**

At the start of a match, you don't have a lot of upgrades yet and your choices are limited. The balance at this point is totally different from late in the game, when both players have upgraded all their spells and units. A balance where one faction is stronger early and the other late is not good: if the early rushes are over, you will already know who is probably going to win. That's pretty boring. On the other hand: having some variation in how fast you can rush does add variation between the factions, so making this completely equal might make the game boring as well!

**6. The amount of fun in the balance**

This type of balancing is really difficult to measure, but quite easy to feel: some tactics are just lame. Spamming a single unit all the time is really boring, so that better not be a good tactic! The following Viking tactic is an example of how things should be: a very strong combo the Vikings can do is to build Frosthammer units (who do area of effect damage and stun), then freeze a large group of enemies with Snowstorm, and then ram the Frosthammers into the frozen enemies with Rage. Doing this requires skill, speed and knowledge, and is pretty strong, so the player will probably feel great doing this!

**7. The amount of luck in the balance**

A Chinese player can start out with melee units or ranged units. At one point we had a balance in which, depending on the opponent's opening move, this would mean a certain win or a certain loose. This is balanced: you have a 50% chance that the enemy happens to choose the opening move that lets you win. However, this is based purely on luck and thus requires no skill at all. So even though the faction balance was good at this point, this balance was broken!

A little bit of luck is a good thing to have in a game, though. Players who loose a match tend to feel a lot worse if they know it is entirely their fault. If there is also a little bit of luck involved, then they can blame their bad luck and feel less bad about their skills. Taken to its extreme, luck is why a game like Mario Kart (which features tons of luck through the upgrades) is so enjoyable for beginners: it still lets them win once in a while against better players.

**Complexinat0ring!**

As you can see, balance has many faces. The biggest problem with it, is that even the smallest change might affect all of the types of balance at the same time, plus it probably affects several match-ups of factions as well. Even for a small change, it is practically impossible to predict what effects it will have on the whole. Therefore, it is incredibly difficult to get the balance right for all of these aspects at the same time.

In terms of balancing, Ronimo's Secret New Game is a lot more complex than Swords & Soldiers, so I am really curious to see how well we can pull it off there!

Since balance is such an interesting and complex topic, next week I am going to talk about some of the pitfals of analysing it, both for developers, and for players and reviewers.

Thanks for the insight! You brought up a number of valid balance considerations that aren't readily apparent on the problem surface.

ReplyDelete