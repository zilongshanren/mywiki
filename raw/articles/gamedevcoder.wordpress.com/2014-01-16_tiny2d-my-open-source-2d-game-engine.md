---
title: Tiny2D – my open source 2D game engine
url: https://gamedevcoder.wordpress.com/2014/01/16/tiny2d/
published: '2014-01-16'
source_blog: Gamedev Coder Diary
source_site: https://gamedevcoder.wordpress.com
category: game programming
fetched: '2026-04-13'
---

Today I have finally managed to open source my after hours project called [Tiny2D](http://www.pixelelephant.com/tiny2d).

It’s development started roughly 4 months ago as I decided to resurrect an old puzzle game I did 5 years ago but never got to finish it. I wanted to port it quickly to new engine (previously used my own tech) that would work well on desktop and mobile platforms and I wanted to improve some of the things too.

Also, having done a couple of 2D game prototypes recently I really wanted something easy to use. Something that would translate my gameplay ideas into working game with as little effort as possible. Minimum code, maximum effect.

And now, here it is – Tiny2D is the fruit of my work, mostly developed while my wife was putting my baby to sleep. It is very simple to use and – as the name suggests – tiny library.

Currently Tiny2D only supports Windows and Android but since it’s using [SDL](http://www.libsdl.org/) under the hood (and implementing Tiny2D on top of other libs – e.g. [Marmalade](https://www.madewithmarmalade.com/) – would be trivial) it should be easily portable to other platforms such as Linux, MacOS or iOS.

Here’s current list of features:

* Textures (png, jpg and more)

* Materials with Techniques and (GLSL) Shaders

* Animated Sprites

* Particle Effects

* Render Targets

* Several built-in Post-Processing Filters

* Asynchronous Resource Loading

* Virtual Resolution Rendering

* True Type Fonts

* Audio (wav, ogg, mp3 and more)

* Input (keyboard, mouse, touchpad)

* Files

* XML

* Localization

* Multithreaded Job System

* Timer

* Random Numbers

For more details head over to [Tiny2D project homepage](http://www.pixelelephant.com/tiny2d) or check it out on [GitHub](https://github.com/macieks/Tiny2D).

Curious why I made [yet another](http://www.moddb.com/engines) 2D game engine?

a) Because I haven’t found any 2D game engine with as simple, yet powerful, interface. I consider [Unity](http://unity3d.com/) or [Marmalade](https://www.madewithmarmalade.com/) too complex for rapid prototyping, [DragonFireSDK](http://www.dragonfiresdk.com/) far too limited (btw, [here](https://gamedevcoder.wordpress.com/2012/02/01/ios-and-android-game-development-on-windows/) is my comparison of Marmalade, DragonFireSDK and Unity) and I prefer C++ from [Lua](http://www.lua.org/), so [LÖVE](https://love2d.org/) is out of question too. Sure, there’s many other game engines, but I haven’t found one that would fully satisfy my needs.

b) For fun. After all I really enjoy coding 🙂

Great stuff, Maciej! Do you have or are you working on any tools like a level editor or atlas/sprite sheet creator? You mentioned you thought Unity was too complex for rapid prototyping but don’t you think it’s pretty convenient for layout out game objects quickly? Just curious.

Hi Sam, nice to hear from you 🙂

1) No, I don’t currently have a plan to do any kind of level editor which is because I wouldn’t want to assume too much about games/apps being created with Tiny2D (how are objects textured / rendered? can they have children and if so, how are they attached to each other? can some of the objects use physics? – these are example questions I want to avoid).

2) Atlas/sprite sheet creator is something I’m still considering but ideally I’d like to make sure any sprite sheet creator can (with some extra code) be used with Tiny2D. So, some generic support for specifying UVs within individual sprite animation frames is more likely than the actual tool for generating these UVs.

3) Unity is great for many games but not all of the games require static layout of the game objects. Think about procedural graphics or other crazy non-layoutable visuals.

Generally my thinking is, if you need level editor, either use any of the freely available ones (and there are many, check this: http://codeboje.de/list-of-2d-map-editors/) or make one that suits best your game.

Having said this and after answering a couple of other questions on reddit (http://www.reddit.com/r/gamedev/comments/1vazn8/my_new_2d_game_engine_tiny2d/) I realized I need FAQ, so here it is:

http://tiny2d.pixelelephant.com/faq.html

Hey, have you tried Cocos2D? They have all sorts of support, and especially recently there is a lot of cross-platform integration. Just wondering if there was a reason why you haven’t tried it, or why you haven’t mentioned it. I used it for my last game, and it worked really well – I plan on using it again for my next iOS game.

Hey there! Maybe I should have looked into that more but a quick look at Cocos2D API gives me an impression that it’s not super easy to use – mainly due to having to deal with heaps of classes and seemingly inconsistent API. However, seeing how it’s popular among folks it’s probably great in a way too. With Tiny2D one of my goals was to be able to get things working with very minimum code and simple API.