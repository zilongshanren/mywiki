---
title: Scripting in RPG Playground
url: https://dewitters.com/scripting-in-rpg-playground/
published: '2014-07-28'
source_blog: deWiTTERS
source_site: https://dewitters.com
category: game programming
fetched: '2026-04-13'
---

My [RPG creation software](http://rpgplayground.com) will allow you to create an entire online role playing game, but as you probably know, it is still in early development. Currently you can let characters say something, but this is of course not enough. You want the player to have entire conversations with characters, and to have cut-scenes that reveal a part of the story.

My first thought on allowing you to create this extra functionality is by using ‘screenplays’. These screenplays would allow you to define conversations and animations in an easy, straight forward way. Screenplays are created entirely by using a point-and-click GUI. You basically can’t do anything wrong.

![screenplay02 screenplay02](../../assets/879a869e94866d68.png)


But programming such a screenplay system takes a lot of time for me. And unfortunately, I’m currently not working full-time on RPG Playground. I have a full-time job, and a family with 3 small kids. So as you can imagine my time is very limited. Therefore, I’m going for the second option, which is allowing you to create text based scripts. It was already part of my plan that RPG Playground would include scripting at some point. But I consider this more of an advanced feature. So previously I thought that scripting wouldn’t be added in the near future. But that has changed.

I’m currently shifting scripting to one of the next features to implement, and the easy to use screenplays will be pushed back to a (much) later release.

Both systems have their advantages and disadvantages. Let me list them here just for clarity:

GUI Screenplay scripting advantages:

- Easy to use for a beginner
- Visually clear by using images and fancy GUI widgets
- Intuitive creation of conversations and cut-scenes

but:

- Takes a lot of time for me to implement
- Limited functionality

Let’s compare this to the text based scripting. As scripting language, I’m going to use [LUA](http://www.lua.org/). It’s a simple scripting language, and has a proven track record because many games already use it.

LUA Scripting advantages:

- Very powerful
- I can enable new functionality fast
- Doesn’t require as much programming on my side

Disadvantages:

- Not easy for beginners
- Visually not as great because all is in text

So because it takes a lot of work off my shoulders, and is very powerful for you to add functionality to your game, I’m going for LUA scripting. The downside is that it’s a bit harder to get into. But I will create a document that makes it easy for beginners on how to script certain things like conversations and cut-scenes.

So how with this actually look like? Well, let me give you some examples. First a simple conversation in LUA script:

character.talk.say("hi") response = hero.talk.respond({"hi, how are you?", "sorry, no time for chitchat"}) if response == 1 then character.talk.say("fine, thanks!") elseif response == 2 then character.talk.say("Alright, bye!") end

A more complex script for a conversation with cut-scene would look like this:

character.talk.say("The end of the world is near!") camera.effect.shake(5) weather.effect.lightning() response = hero.talk.respond( {"How do you know this is the end of the world?", "This is not the end, it's just an earthquake"}) if response == 1 then character.walk.go_to(3, 4) character.talk.say( "Take a look in this book, the prophecy is clear") if hero.inventory.has('prophecy book') then hero.talk.say("I already have that book") else hero.talk.say("Let me see!") end elseif response == 2 then character.talk.say("Unbeliever!") character.walk.go_to(0, -6) door1_house.latch.open() character.walk.go_to(0, -1) end

I hope these examples don’t scare you too much. I will definitely write a document with easy examples that you can copy/paste into your own scripts.

Currently I’m working hard to get this scripting thing in the next release. In the mean time, [continue making your own RPG](http://rpgplayground.com)!

## 6 Comments

## Infinicorn · April 9, 2015 at 11:22

When will you be releasing the new update? I would really like to use the new interactive speech coding, but as of now, it’s unavailable for use with the older version.

## Koen Witters · April 9, 2015 at 23:04

I’m now testing and bugfixing the new release. But it only includes adding additional levels. After that I’m starting on the conversations again.

## Dawnette · November 12, 2015 at 14:42

Have you changed the option to add scripting? I cannot modify any script, nor add it for characters.

## DiamondMob04 · August 25, 2016 at 18:34

Please add moving, so that my characters can go to different places and so they can disappear and stuff! Without it, mysterious maps or horror maps are very hard to do.

## Galactic · June 29, 2017 at 08:17

Hey! Could you possibly add an option to use the old and the new scripting? So you could choose to use the original or the new LUA scripting for screenplay?

THAT WOULD BE AWESOME!

## Koen Witters · June 29, 2017 at 11:43

What do you mean with old and new? There never was LUA scripting.