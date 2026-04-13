---
title: Re:creation dev log. June – October 2015. I’ve made lots of stuff.
url: https://eliasdaler.wordpress.com/2015/10/15/re-creation-dev-log-june-october-2015/
published: '2015-10-15'
source_blog: Elias Daler | Re:creation
source_site: https://eliasdaler.wordpress.com
category: game programming
fetched: '2026-04-13'
---

Almost five months passed since the last dev log on this blog.

Why? That’s because I created [SFML forums thread](http://en.sfml-dev.org/forums/index.php?topic=18062.0) and [TIGSource thread](http://forums.tigsource.com/index.php?topic=49336.0) and wrote most of the stuff about the game here! But I’ve realized that a monthly summary about what’s going on would be pretty helpful for those who don’t want to read long threads and search the most awesome stuff that’s been happening. Another plus is that I don’t have to write lots of in-depth style here. I will write in-depth stuff in SFML forums and TIGSource threads and link to those posts here, so you don’t have to scroll through stuff that you don’t want to read lots about.

Here’s the best screenshot I can show you at the moment to show where the things are right now.

![](../../assets/2dafef172d8a4b3a.png)


Okay, let’s start.


# June 2015

![](../../assets/e21459e4cb0a7bdf.png)


**Necromancer (healer?) grandma**. You’re undead, so you can’t die. But hero’s body may become too damaged and not being able to progress further. So, when you lose all your life, you’ll become a ghost and won’t be able to return to your original body. Grandma will heal you for some money. You’ll not lose any progress you’ve made previously, because the time won’t move back!

![](../../assets/96fdb834f8adc01a.gif)


I’ve worked on some **puzzles** which I’ll show from time to time, but not too much (don’t want to spoil everything!). It’s amazing how many puzzles I can achieve with a recreation mechanic.

I’ve had lots of exams this month so that’s pretty much all I’ve done this month.

But I’ve thought about gameplay and story a lot and had lots of interesting ideas which I later implemented.

# July 2015

![](../../assets/453c31dfeea304ad.png)


I’ve drawn better forest tiles. Now the forest looks a lot better and more nature-like. This wasn’t easy to achieve because there are lots of different tiles which make everything less blocky.

I’ve also created much better **Input** class. Now I store all bindings in a JSON and I don’t use specific keys in the code which deals input. I use enum with different tags for buttons. Input Manager can get a specific gamepad or keyboard key by enum value which let’s me write input code without caring about keyboards and gamepads separately. Oh yeah, **the game has native gamepad support now**!

I’ve implemented a better **Event manager** which lets me communicate between Lua and C++ objects easily. [More details about implementation](http://en.sfml-dev.org/forums/index.php?topic=18062.msg133631#msg133631)

I’ll explain it shortly. The main difference between new and old event managers is that objects which want to receive events or send them don’t have to inherit from **ISubject** or **IObserver** classes. Observers need to specify callback function which gets called when an event of specified type is sent. Observers receive all messages of a type they are subscribed to, but they can also subscribe to a particular entity if they’re interested in it and don’t care about anything else (for example, GUI doesn’t care about enemy’s HP as it only displays player’s HP).

Events can be triggered immediately or be added in the event queue. Most of the time there’s no need to call a callback function immediately and this may in fact lead to some bugs. So, event queue is a nice way to deal with events.

![](../../assets/aba3dc05f3313e7f.png)


And I want to introduce another awesome undead. This is **Master of Recreation** (he doesn’t have a name yet). He teaches you how to fight and how to use recreation to solve puzzles. But that’s not all that he’ll do. He’ll play much bigger part in the story later, though.

![](../../assets/33ff5b0d31bc31cc.gif)


Just a neat death animation.

![](../../assets/fa4cc9ee06e3d57b.png)


When you kill enemies, you can tell which type of the enemy lies in the grave by looking at the weapons lying next to them.

Picking up weapons to use them instead of becoming an enemy would be an easier way to solve puzzles. But not for our brave undead hero whose hammer is too heavy to carry other stuff!

# August 2015

Consider this my vacation month… I’ve studied some C++, algorithms, math and just spent lots of time spending time with my family. Those things are important!

I’ve spent some time working on the animation:

![](../../assets/35bd9b286763e719.gif)


![](../../assets/49cf24570046e318.gif)


Enemy design is also much better now!

![](../../assets/2503acd6793e4bf0.png)


And check out this awesome thing my GF made for me. I can’t express how awesome it is. <3

![](../../assets/a294452cbd2f1480.jpg)


![](../../assets/7cd022e833047515.png)


# September 2015

I was working on ECS and I’ve written a lot about it [here](http://en.sfml-dev.org/forums/index.php?topic=18062.msg136043#msg136043). There’s a pretty big conversation about it, so check it out if you’re interested!

Lots of people on SFML forums volunteered to make a translation for different language! This is very awesome and makes me very proud that some people appreciate my game so much.

Undead Cafe was an interesting location to work on. First I’ve drawn this concept art

![](../../assets/f8ec59be10fb2e09.png)


And here’s how it looks in the game

![](../../assets/16a1303415d2629e.gif)


Who is this **cute cat**? You’ll know more in the game!

I’ve also changed the dialogue font. It’s a lot more readable and lets me fit more text on the screen.

This made me think more about the dialogue windows and I’ve created a small tool for making dialogues. More details [here](http://en.sfml-dev.org/forums/index.php?topic=18062.msg137093#msg137093).

![](../../assets/c794cb0c52c515ee.gif)


I’ve moved animation descriptions from Lua to JSON and it made scripts a lot more readable!

There was no need to store them there as they are just plain data.

And then came the **perspective change**. I realized that axonometric perspective might work better… and it did.

I’ve also added more shadows to the scene, so everything looks even better.

![](../../assets/a71de761b7d02541.png)


GIF comparison:

![](../../assets/cb18e9d327afdb0e.gif)


Drawing in this perspective is a lot easier because most lines become straight in most objects. Here’s an example:

![](../../assets/8df1b3a7e26853f7.png)


Second one is much easier to draw and looks sharper!

![](../../assets/b147ca5e90e0074f.gif)


Fog really helps to create nice atmosphere in Undead Town. It’s not just a simple overlay. It has height and goes through objects.

More details about it [here](http://en.sfml-dev.org/forums/index.php?topic=18062.msg137743#msg137743).

# What am I doing now?

There’s a lot of stuff I’m working on in the moment which I want to share when it’s done.

I’ve been working on a combat a lot and it’s pretty fun! Hopefully it won’t be too repetitive (it sure is less repetitive that it has used to be.)

I’ve also been working on some base engine stuff, fixing bugs and writing better and safer code. Those are not the most fun to work on, but this is very important because I want to make a great demo which will leave a good first impression. Hopefully, I’ll fix most of the bugs and continue prototyping stuff soon. More about prototyping and future plans later!

I also have other cool announcements to make this month, so stay tuned!

Thank you for reading my dev blog. If you’re interested in getting the latest updates about the game, [follow me on twitter](https://twitter.com/EliasDaler) or read [SFML forums thread](http://en.sfml-dev.org/forums/index.php?topic=18062.0) or [TIGSource thread ](http://forums.tigsource.com/index.php?topic=49336.0)from time to time. See ya!

Great to know that there were many updates for the past months. The animation in recreating the archer and that fog effect looked good!

Thanks a lot!

I love Zelda: A link to the Past. I love your game without having played. Looks really amazing. Congrats!

Thanks a lot! I love ALttP too. I guess it shows :D

Hi! You were nominated for the One Lovely Blog Award – Game Maker’s Edition. You can read about it here. https://takingovertheworldwithgames.wordpress.com/2015/10/20/one-lovely-blog-award-game-makers-edition-7-games-you-loved/