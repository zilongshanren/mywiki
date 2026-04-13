---
title: Re:creation dev log. January-February 2016. Better art, sounds, cutscenes and
  more!
url: https://eliasdaler.wordpress.com/2016/03/06/recreation-dev-log-january-february-2016/
published: '2016-03-06'
source_blog: Elias Daler | Re:creation
source_site: https://eliasdaler.wordpress.com
category: game programming
fetched: '2026-04-13'
---

Just a short info for those who have never heard about my game.

Hello, my name is **Elias Daler** and I’m a solo developer who is making **Re:creation** in my free time. It’s done in C++ with SFML and Lua!

**Re:creation** is an action adventure game about the undead knight who wants to free undeads from the humans who use undeads as slaves or practice dummies. The unique mechanic of the game is called recreation which allows you to control dead people with your ghost gaining their abilities to solve various puzzles. Here’s an example of this puzzle.

![u9cys5p](../../assets/4ee5a5bc16b134b9.gif)


Read more about the game [here.](https://forums.tigsource.com/index.php?topic=49336.0)


Back to the dev log…

Two months have passed since [the last dev log](https://eliasdaler.wordpress.com/2015/12/31/recreation-2015/). I had lots of time to work on the game and here’s what I’ve managed to work on.

#### Better art

Yet again, another graphics improvements! Change of the perspective was quite an improvement, but I’ve also realized that I can improve other stuff too.

There’s more depth to characters and surroundings, the colors are used better, etc.

There are more graphics improvements which I’ve done recently (for example, I’ve improved main hero’s sprite a lot), but I’ll show it off a bit later.

Here are some comparison screenshots!

![ku1rd35](../../assets/33b623b8a76ec5e4.png)


![izcnoc7](../../assets/1e382553e1f8ae4e.png)


There are also subtle things that made game look better!

![xdywsa3](../../assets/0d54ac5a59eb2ba8.png)


![rgrbjss](../../assets/59cc072bbaea2353.png)



#### Cutscenes / action lists

This one was a big progress for me. It’s pretty hard to do some actions in specified order in games. That’s because most of the time it cannot be expressed like this:

someCharacter.goToPoint(20.f, 30.f); someCharacter.playAnimation("waving"); someCharacter.say("Hello!") someCharacter.goToPoing(40.f, 50.f);

That’s because most of this actions can take more than one frame to complete, and some actions (like dialogue actions) can wait for user input, so we can’t just call those functions one after another.

That’s where action lists are useful. You create a list (or array) of actions (duh) that you need to execute one after another. When you start an action, you wait until it is finished and then start another action.

You can have multiple types of actions and each one may have a different finish condition.

For example, Go-To Action finishes when the entity arrives at the destination. Animation action finishes when the animation finishes, etc.

You can even go further and add “lanes” or tags for specified actions, so you can easily jump from one action to another instead of going to next action.

I’ve also made a multiple choice in dialogues which is just another form of Action lists. So, it’s pretty great!

![yb0hw90](../../assets/af246c41b04939e7.gif)


Action lists were originally made for cutscenes, but later I’ve realized that I can do much more with them. For example, I’ve created much better scripts for doors and going inside the door, which is just a short cutscene.

![jsacz3u](../../assets/87e324f5e599b28a.gif)


And there are lots of similar stuff which action lists made easier, I’ve made an entire boss battle with it! (Which I can’t show, spoilers!)

#### Sound

I’ve also started working with a composer! His nickname is **Kasper Hermsen** a.k.a. ** Torchkas** and he makes some really great stuff! He’ll also do all the sounds effects in the game.

One interesting aspect of the soundtrack will be its SNES sound. Torchkas writes stuff for the SPC and then records all the stuff through his SNES which gives 100% accurate and awesome sound. It’ll also be possible to create a SNES ROM of the soundtrack in the future! I’ll probably post some of the songs once they’re ready.

I’ve worked on audio for some time.

One of the coolest things was sounds sync with animation. Now I can specify which sounds should play at the specific frame of animation which makes stuff perfectly synchronizied with the stuff happening on the screen. Once I bind sound to a frame, I don’t need to call playSound function, it will play automatically, which makes sounds a lot easier to work with.

I’ve also made stereo sounds which is a pretty cool effect and which I’ll use now and then. I’ve made it automatical, so I can attach sounds to entities and it’ll play with the needed pan/volume depending on entity’s position on the screen.

I’ve also added ability to create collections of sounds, which play one after another with varying pitch and volume. For example, it’s works great for footstep sounds.

#### Lua / C++ interaction changes and observations

I’ve learned a lot about Lua/C++ interaction. For example, I’ve learned that calling Lua from C++ is very expensive and calling C++ from Lua is quite fast. So it’s better to pass an array of references to Lua functions to Lua function which will be call all of them in order than to call them one by one in C++!

The difference is pretty amazing and can significantly affect your performance.

I’ve realized that some of the stuff I did with Lua was pretty silly which led to lots of C++ -> Lua calls.

After a while I’ve realized that lots of stuff in Lua by one call from C++. For example, there are two ways to write event management for Lua.

1) Store info about callbacks (references to Lua functions) in C++ and if the corresponding event happens, call it from C++.

2) Store info about callbacks in Lua. Pass all the events which happened in the frame and process them in Lua, calling all Lua callbacks here

I’ve used 1 for a long time, but then I’ve noticed a noticeable performance hit when lots of events called Lua callbacks. That’s because there were lots of C++ -> Lua calls happening. I now use 2) and there’s only one C++ -> Lua call. If there are callbacks which need to be called, they’re called from Lua. And calling Lua functions from Lua is much faster than calling Lua from C++.

In fact, writing Lua code can be much easier that writing the same code in C++. I rewrote entity state machine in Lua and here are the results: -387 lines of C++ code, +95 lines of Lua code. The code is much simpler, easier to modify and it’s easier and faster to call all the Lua stuff from here!

In fact, it made possible to transfer almost all of the game logic to Lua which is pretty neat because it allows me to modify more stuff in the shorter amount of time.

It also allows me to reuse the same code for multiple entities.

(I’ll talk about the issue more in some Using Lua with C++ article!)

![szai57l](../../assets/38a4586a3af2c698.png)

Some cutscenes will look like this…

#### Improved stability

One cool thing about having another person working on the game is that you become more critical to the game and try to make it stable.

Most of the time I know what breaks the game and what stuff I shouldn’t do. I know about it and put it on my TODO list, but it’s hard to fix all the bugs and sometimes adding new feature breaks a lot of stuff. But now I have responsibility to make the game stable again as fast as possible to make it possible for composer to play the game and test all the stuff he needs at the moment.

I also try to work on the game-y stuff a bit more, which is also great.

#### Prototyping

I’ve also learned how important prototyping is. Lots of stuff changes from initial design, so drawing polished art and animations before making stuff playable is no a great idea. I’ve realized this when I was making a boss battle. Once I started to test it, I’ve figured out which stuff needs to change to make it better and more interesting. In the end I’ve learned that some previously planned animations were not needed and that some would need to be a bit different from what I previously imagined.

It was also such a nice feeling, to be able to work on the game, not on the engine. :)


#### Future plans


There’s a lot more engine stuff I’ve done and there’s also some game-y stuff I really want to show. But I’ll probably show it later because I need to finish lots of the art and make it really neat. There are also some cool puzzles I want to show off.

My biggest goal is to make a playable demo which seems so big as if it’s comparable to making a complete game… There’s a lot of stuff to be done and once the demo is ready, it’ll be much easier to complete the game because most of the time I’ll be working with the game content, not the engine.

The demo will be kind of a vertical slice of the game, so if it’s completed, it means that there’s not much left for me to add in the engine code.

It’s really hard to predict when the demo is going to happen. To be fair, I want to release it as soon as possible, but at the same time I want to make something really great and memorable.

There’s also a lot of work which still needs to be done, but I feel like the core of the engine is almost complete. Once I get that I have enough tools to make a game, I’ll write a big post explaining all that stuff. It’ll be a pretty good milestone. Don’t worry, I’m not one of the programmers who write engine stuff “just for the future”. **YAGNI** is an important principle. :)

Thank you for reading the dev log! If you want to hear more about Re:creation in the future, subscribe to [my twitter](https://twitter.com/EliasDaler), follow my blog or read [SFML](http://en.sfml-dev.org/forums/index.php?topic=18062.0) or [TIGSource ](https://forums.tigsource.com/index.php?topic=49336.0)dev log thread from time to time!

See ya!