---
title: Re:creation dev log. December 2014 – February 2015. Bigger levels, boss and
  heavy attack
url: https://eliasdaler.wordpress.com/2015/03/07/recreation-dev-log-december-2014/
published: '2015-03-07'
source_blog: Elias Daler | Re:creation
source_site: https://eliasdaler.wordpress.com
category: game programming
fetched: '2026-04-13'
---

A long time has passed since I’ve written the last dev log! Is Re:creation dead? Is it stagnating? No, not at all. It’s more alive than ever now!

I haven’t written a new part of dev log because I had to study a lot in December and January. I had some time to develop some stuff during these month and had a lot of stuff done in February.

I’ve decided to write the dev log in two forms

**First one**will be about the features I’ve implemented recently and it will have a lot of pretty screenshots and gifs. (You’re reading this part right now).**Second one**will be more specific and I’ll focus more on technical parts of the game and implementation details of some interesting features. This part is a lot harder to write so it’ll be less frequent than the first one.

*If you’re wondering about how I’ve implemented one or another feature of the game or its engine, feel free to write an email and ask about it! I’m always glad to answer.*

Well, let’s start.


## Graphics improvements

![](../../assets/ff3bfce3dcc12a2a.png)

Before

![](../../assets/016f64f127f318e5.png)

After!

It’s pretty amazing how some small differences can make your game look better. I’ve fixed colors of grass tiles and made a second grass tile to give grass more variety and make tile grid less noticeable. It worked pretty well! Grass is now visible in gifs which is also great. (It wasn’t because of the low contrast between primary and secondary tiles)

![](../../assets/b290a6bf9518aadc.jpg)

Grid is noticeable on the right side of the road. Not visible on the left side!

## Working on the boss

![](../../assets/989d4ec645b861ca.gif)

Cave Story reference


Working on the boss was pretty hard but very rewarding at the same time. It required lots of new things to be added and there’s still some work left to do, but right now it looks pretty good!

![](../../assets/795f218724f1a7ff.gif)

Little help from above

![](../../assets/725f1032519ee41b.gif)

When you turn into a ghost, boss reacts to this!

The boss cannot be killed with a brute force and involve some [ recreation mechanic](https://eliasdaler.wordpress.com/2014/11/30/recreation-dev-log-november-2014/) usage to be used to defeat him.

The coolest thing is that boss is an entity like any other. It’s behaviour is very specific but can be entirely scripted in Lua! This is very cool because I don’t need to hardcode bosses behaviour into C++ code and can easily modify it with some scripts! I’ll show how it’s done in the next part. For now, here’s an example how Lua script for different boss states looks:

ScriptStateMachineComponent = { States = { { name = "BossChaseState", enter = function(this) setAIState(this, "AIChaseState") end, execute = function(this) end, exit = function(this) end }, { name = "BossDefendState", enter = function(this) setAIState(this, "AIIdleFollowState") setAnimation(this, "boss.animations.defend.Down") setCollisionType(this, "solid") setBoolVariable("saidGhostTalk", false) saySpecialTalk(getEntityId("ENEMY_FALL"), "HELP") end, execute = function(this) if(getPlayerName() == "ghost" and not getBoolVariable("saidGhostTalk")) then saySpecialTalk(this, "GHOST") setScriptState(this, "BossConfusedState") setBoolVariable("saidGhostTalk", true) end end, exit = function(this) end }, { name = "BossConfusedState", enter = function(this) setAIState(this, "AIIdleState") setBoolVariable("saidReviveTalk", false) end, execute = function(this) if(getPlayerName() == "hero" and not getBoolVariable("saidReviveTalk")) then saySpecialTalk(this, "REVIVE") setScriptState(this, "BossChaseState") setBoolVariable("saidReviveTalk", true) end end, exit = function(this) end } } }


## Heavy attack

![](../../assets/678ef8e77a646b50.gif)


Heavy attack will be used to knock enemies a lot easier. It can also be used to stun some enemies and crack holes in some floors!

**Game design stuff**

It’s also useful from game design perspective. I need to be sure that the player is his original form when he is at the certain point of the map. So I place a crack on the floor, the player cracks it with heavy attack and falls down immediately. I can now be sure that he’ll be there in his undead form now. Easy!

People said screen shake looked cool, ha-ha. But it gave me some headaches. For example, I now need to create more tiles and objects on the edges of the maps because you could see where the map ends when the screen is shaking! I also disable all objects except from the objects which are in the room the player is currently in. It makes the game run a lot smoother and faster. But you can see objects from other rooms when the screen shakes! These problems were easily fixed though.

The crack which appears on the floor after the hit disappears after some time. This is done thanks to new** TimerComponent **which lets me add as many timers to entities as I want and then when the time is up, it calls their **onTick** functions.

![](../../assets/c7fef69e4cb018ff.gif)

Chest opening


## Big rooms and bigger maps

![](../../assets/dde3003fbe5a2abc.gif)


Some levels have bigger areas now which can scroll in any direction. This is how it’s done in Link to the Past. There are rooms that don’t scroll which are the size of the screen. And there are rooms which are bigger than one screen which require scrolling. This is how it’s done in my game now. Levels can be bigger and more interesting now!

## Bug fixes and optimizations

A lot of work was put into bug fixing and optimization. A lot of bugs were fixed and the game runs smoother now. I’ve also worked on level reloading. There’s a cool and easy way to determine which resources are needed and which can be released when you reload the level. I’ll talk about it in detail in the next part!

![](../../assets/28113a07673347bf.gif)

Level reloading

## What’s next?

Re:creation is becoming more and more playable each day. At this stage I’ll polish everything the game has and add some new content. I plan to focus on three levels which are almost ready and try to finish a small playable demo for people to test and provide the feedback. I still have to draw lots of stuff and I’ll probably look for an artist very soon.


That’s all for now, thanks for reading!

[Follow me on twitter](https://twitter.com/EliasDaler) to get the most recent updates about Re:creation.

It was almost like reading about Courier of the Crypts system, especially about that Timer component. You gave me some motivation to try using LUA scripting language as well for some stuff. That hardcoded stuff really isn’t the best way to do thing.

Anyway, you’re doing great! Keep writing those blogs, you have one reader here ;)

Ha-ha, great minds think alike, huh? ;D

Ask me stuff about Lua if you need some help. I’ll puslish a new post soon about script state machines which show how awesome they are (they’re even more awesome now then they were at the time I was writing this dev log)

And thanks.