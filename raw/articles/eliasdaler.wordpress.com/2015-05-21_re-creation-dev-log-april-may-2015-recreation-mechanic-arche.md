---
title: Re:creation dev log. April-May 2015. Recreation mechanic, archers, event system
  and more!
url: https://eliasdaler.wordpress.com/2015/05/21/recreation-dev-log-april-may-2015/
published: '2015-05-21'
source_blog: Elias Daler | Re:creation
source_site: https://eliasdaler.wordpress.com
category: game programming
fetched: '2026-04-13'
---

Last two months were pretty awesome. I had lots of free time and was able to implement lots of new stuff!

## Recreation mechanic

Let’s start with a gameplay gif:

![](../../assets/7ddb1d376e09a863.gif)


It’s another example of recreation mechanic.

For those who don’t know, recreation mechanic is the main mechanic in my game. When undead hero kills people, he can leave his body and control dead people with his ghost. He gains their abilities to progress through the game and solve various puzzles. But he can’t leave his body behind for a long time because he can’t carry the hammer while controlling other people. The hammer can do some stuff which normal weapons can’t. ([break some floors](https://i.imgur.com/rIWlMqT.gif), for example)

This hammer is very heavy so he can’t carry other weapons. So, for example, in order to shoot arrows, you need to kill archers and control them with your ghost.

He can also use his ghost to reach inaccessible areas. But this won’t be very useful if there are no corpses lying there because he won’t be able to interact with the world this way. But it has another use: you can look around and see what you have to deal with next. This will be very helpful when solving complex puzzles.


Here’s another example which I posted already but made look a bit prettier:

![](../../assets/78562e20bef43596.gif)


Corpses have weight, so you can use it to push buttons and some other stuff.

## SFML forums dev log

I’ve started [a dev log on SFML forums](http://en.sfml-dev.org/forums/index.php?topic=18062.0). This lets me post short notes about the stuff I’m working on. This also lets people discuss stuff about my game and engine. It also lets people provide in-depth feedback which I appreciate a lot.

There’s some awesome discussion about entity/component/system happening there, so make sure to check it out, if you’re interested.

I also plan to start dev log on TIGSource later which will mostly mirror dev log on SFML forums.

## Alan the Blasterous

Alan the Blasterous is a pyromaniac addicted to explosions and you need to rescue him from the cell where he is kept by evil humans. He’s very intelligent and humble person… when he’s not talking about explosions. See for yourself:

![](../../assets/fb3053815e34f634.png)


![](../../assets/828b6d461dd87c1b.png)


(Fun fact: this is the first character which has name now.)

## GUI

I’ve also redone GUI completely:

![](../../assets/784f3e95b9ffae55.png)


![](../../assets/41f6c49435f6e4ec.gif)

Inventory

GUI also displays contextual tips because main action button will have different uses depending on the context. (This was cleverly used in Anodyne in some moments. RIP, some people I’ve tried to talk with.)

![](../../assets/7cea3b31ec94b05e.png)


## Bitmap fonts

I’ve had a basic system for bitmap fonts for a while but it was too slow because I’ve used sf::Sprite for each letter which was a big waste.

Now I’m using sf::VertexArray for a whole string so I have to one draw call per string instead of tons of draw calls for each letter!

I’ve also discovered a very useful tool called [BMFont](http://www.angelcode.com/products/bmfont/) which can convert any font into a bitmap and add some outlines or other effects if necessary.

It produces a .png (and many other formats if you choose!) and a .fnt file which is a plain text file which is very easy to parse and then use it for drawing.

Maybe I’ll write a short tutorial about it. It’s a great tool.

## Events

This was a huge thing on programming side of my game.

Short example: GUI needs to know player’s hp at any given moment. It can check player’s hp in each frame but that’s not very efficient. I use Observer pattern. Systems and entities can subscribe to any other system or entity and receive messages from them. But I’ve done more than that. I’ve made callbacks so I can map system member function to event type and it will be called if entity sends that event.

So, when player entity sends HpChangedEvent, GUISystem::onHpChanged() is called. Here’s how it looks in the code:

gui->registerCallback<HpChangedEvent>(&GUIPlayingState::onHpChange); player->addObserver<HpChangedEvent>(gui); void GUIPlayingState::onHpChange(int senderId, const std::shared_ptr& e) { auto event = std::dynamic_pointer_cast(e); int hp = event->hp; ... // do some stuff! }

This made me rethink lots of stuff about system interaction and led to lots of decoupling which is great and made the code a lot better. For example. GUI system doesn’t need to know how HPComponent works anymore, it just gets the only thing it’s interested in: HP value. Systems which respond to user input don’t need to check input for themselves, InputSystem does it and sends ButtonPressedEvent for those systems who are interested. And there are a lot of more examples of decoupling which can happen.

I’ve made event system with some neat C++11 features like std::type_index and std::bind. There’s some possibility that I’ll write a complete tutorial about this event system because it works better than I’ve expected.

## Some animations

I’m also making basic human sprite, so I won’t have to redraw lots of stuff. This also led to a better walking and attack animation than I had before!

![](../../assets/3a6879114945b5ec.gif)

![](../../assets/dafbc97a7fbcf570.gif)


![](../../assets/d130263021fdbce1.gif)


## Archers

![](../../assets/a9237b1c0a9cf453.gif)


Archers are a great display of stuff I’ve done recently.

First of all, all items now have scripted functions called **use**. So, when you use a sword, script function is called and sword attack starts. When archer uses his bow, bow attacks starts. I’ll add more items in the future (potions, spells, etc.) and they’ll have scripted **use** functions too. This makes code a lot better than it have used to be (all items were hard-coded!)

And I’ve made scripted attacks. They works almost the same as script states (enter, execute, exit functions). I’ve also added pre/post attack animations which make attacks look a lot better visually.

Arrows are entities like any other but with some cool scripting. They are a great example of how awesome Lua scripting is! I had realized that I can implement arrows using scripts **without using C++ code**. And I did.

You can find more info and some scripts [here](http://en.sfml-dev.org/forums/index.php?topic=18062.msg130114#msg130114).

## Level chunks

![](../../assets/9e3c25316b37e3d4.png)


I’ve remade level rendering method. Instead of using lots of sprites for each tiles, I use chunks. Chunk is a collection of sprites which has sf::VertexArray. This lets me draw levels in chunks instead of drawing in tile by tile. A lot less draw calls! Draw calls are very expensive compared to other stuff so this is a big perfomance improvement and level rendering is **3 to 4 times** faster now!

Storing level in form of chunks is useful too, because I don’t need to store lots of empty areas in level file now. Previously, level was a big 2D array, so I needed to keep data about empty spaces to save its form. But looks how many empty spaces there may be in one level. And it’s just a small example. Now I don’t need to save empty chunks to file so it’s a lot more efficient method of storing level data.

## What’s next?

Not much in next month, unfortunately. I’ll have lots of exams and I need to spend lots of time studying to do good. But I’ll not forget about my game during this month. I’ll prototype some stuff, think about new puzzles and draw some concept art from time to time.

![](../../assets/5bc340047e0822b8.jpg)

My drawing sucks sometimes

And that’s it. When I was writing this post, I’ve realized that last two months were one of the most productive months in my life. So much stuff done! I hope you’ve enjoyed this post.

If you want to follow my gamedev process more closely, you can [follow me on twitter](http://twitter.com/eliasdaler) or read [my dev log on SFML forums](http://en.sfml-dev.org/forums/index.php?topic=18062.0)!

Hello! I love you project so much! Where can I find source code or demo for Linux? Egor

Oop! I’m sory! My english needs practice. Where can I find source code or demo for Linux?

No problem. This code is has closed source and demo will be coming out later this year (can’t tell when)

Was interesting in your screenshots but they don’t seem to be showing up…

Hmm, that’s strange. Maybe you should try different browser. They definitely are fine.

I tried again on the same browser, and they are working fine now. I guess just a loading problem.

Game looks great with classic retro visuals. Sure it’s a lot of fun to dev!

Thanks! Yeah, it’s the greatest thing I’ve ever created. :D

This looks great! The ghost abilities and the constraints at play make it really interesting. I also love the retro feel and creativity of your art. How long have you been doing this game?

Thanks a lot! :D

I’ve been doing this since October 2013!

Wow. And it seems a lot of work too. I’m looking forward to your demo! In which platforms will this be released?

Yeah, that’s a lot of work. :D

The game is coming out on Windows, Linux and Mac.

Hi! I’ve been referencing your LuaBridge tutorial and was looking at some of your example scripts and caught myself just checking out the entire project. Looks really good so far! I’m not sure if you’ve mentioned it any of the posts if you have a composer. If not, I’m looking for a project to compose for in between working on my own project. Not interested in any money/royalties/etc. if you’re selling the game; would be more than happy to just be in the credits :) Thanks for the LuaBridge reference resources and keep up the good work!

Hi! Thanks a lot. I have a potential composer, but I’m still don’t work with him (no need to write music for now), so I don’t mention it everywhere. If you have some cool music to show off, send it to me on my e-mail: eliasdaler@yandex.ru