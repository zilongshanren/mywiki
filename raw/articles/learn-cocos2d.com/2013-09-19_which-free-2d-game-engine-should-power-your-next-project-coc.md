---
title: 'Which Free 2D Game Engine Should Power Your Next Project: Cocos2D, Sprite
  Kit or..?'
url: http://www.learn-cocos2d.com/2013/09/cocos2d-sprite-kit-game-engine-power-next-project/
author: Doug Davies says
published: '2013-09-19'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

With yesterday’s release of iOS 7 and hence Sprite Kit, many cocos2d developers will face this question sooner or later: switch to Sprite Kit or [Kobold Kit](http://koboldkit.com/) or stick with cocos2d-iphone or perhaps move on to cocos2d-x?

I’ll give you some guidance and things to consider …

### Sprite Kit / Kobold Kit

Sprite Kit made quite the splash. There are new tutorials coming out by the minute. Two books will be available within days after release. Several high profile tutorial & starterkit authors have jumped on the bandwagon. Tool developers are hard at work adding Sprite Kit support. Instructors are already offering new mobile game development courses based on Sprite Kit. Heck I even started a new game engine based on Sprite Kit: [ Kobold Kit](http://koboldkit.com/).

With almost everyone jumping ship, it seems a safe bet to jump ship, too. You’re guaranteed to get excellent documentation from Apple, plus a stability of the framework until at least iOS 7.1 and even then Apple is known to carry on supporting deprecated methods for several versions. It’s easy to learn, and once learned you won’t be thrown off guard by new releases. And the developer community will soon surpass that of cocos2d-iphone.


For beginning and intermediate developers there should be no second question about using Sprite Kit. It’s easy to learn and use, it has everything you’ll need, plus the stuff in Kobold Kit in case you do miss something - tilemaps for instance. New projects are created with developer-friendly ARC memory management, something cocos2d won’t do until v3.0.

Seasoned developers familiar with OpenGL and shader programming will not be so easily convinced, because Sprite Kit currently offers no way of adding custom GL code. However, peeking into the private API of the SpriteKit.framework you’ll find, among others, a SKOpenGLNode plus tilemap and bitmap font nodes. Perhaps these are a future addition, or perhaps they’re just for testing.

Either way, many OpenGL effects can also be achieved in Sprite Kit by simply applying Core Image filters to parts of the scene or a texture. So it’s not completely static, and in fact applying visual effects has never been more approachable in a 2D renderer made for game development.

Sprite Kit runs on iOS 7 and Mac OS X 10.9. While some see the requirement of the latest OS as a disadvantage, it really won’t be anymore a couple months from now. Given how long it takes to make a decent game if you were to start now, it means you can safely ignore this “disadvantage”. And [Apportable](http://apportable.com/) is hard at work making Sprite Kit apps portable to Android.

**Summary**: Unless you absolutely have to write OpenGL code or custom shaders, Sprite Kit is a safe bet. Even if you want the option to deploy to Android.

### cocos2d-iphone

[Cocos2d-iphone](http://cocos2d-iphone.org/) is the top dog - for now. You can’t really go wrong with it, at least not with v2.1. That is, if you don’t mind fixing many odd project details (including not supporting ARC out of the box) and build issues due to non-default build settings and problems caused by tutorials because they’re typically outdated, targeting older cocos2d-iphone versions. Those are not serious issues for experienced developers, but frequently are frustrating showstoppers for beginning developers.

I fixed many of these issues in [Kobold2D](https://github.com/kobold2d/kobold2d) (free) and provide a mature MVC architecture for experienced developers with [KoboldTouch](http://www.koboldtouch.com/). But I won’t continue to support Kobold2D, and KoboldTouch is actually a framework on top of cocos2d.

Cocos2d has some odd runtime behavior that ought to be warned about. For example unlike Sprite Kit true type font labels incur a huge performance penalty when the string changes. And the default tilemap renderer is limited to 65k tiles, and it’s always rendering the entire map resulting in gruesome performance issues. The physics integration is half-baked, giving you a sprite with physics body but leaving memory management of the C/C++ body up to you.

Sprite Kit was a catalyst for cocos2d-iphone to start developing the version 3 with the lead developer refocusing on cocos2d-x. We won’t know where exactly cocos2d-iphone v3 is heading and when it will be production-ready until way into 2014. Until then v2.1 remains as a project with dust mites and little to offer over Sprite Kit, except for being open source and enabling you to write OpenGL code and shaders.

Like Sprite Kit cocos2d-iphone supports iOS and OS X, though you can build apps that run on iOS 5 and Mac OS X 10.6. Likewise cocos2d-iphone is Apportable to Android.

**Summary**: if you have to write OpenGL code or shaders, and you prefer to do so with Objective-C rather than C++, then use cocos2d-iphone v2.1. If you know C++ well you’re probably better off going straight to cocos2d-x.

### cocos2d-x

[Cocos2d-x](http://cocos2d-x.org/) has come a long way since it started in mid-2010. It is now not only on par with cocos2d-iphone, feature-wise, but it also exceeds it. Many classes have seen improvements over their cocos2d-iphone counterpart, while some features are completely new including a game component system and the ability to write apps in Lua.

Of course cocos2d-x’ cross-platform approach comes at a price: it has by far the most complex project setup of all cocos2d projects, mainly due to supporting such a great variety of platforms and IDEs. Plus it requires a fair amount of C++ knowledge - if you’re just learning C++ you’re probably better off at using a platform-specific C++ library or learning Objective-C instead or perhaps considering Unity with C#.

Speaking of which: the interesting bit about cocos2d-x is that it sports two spin-offs targeting HTML5 (Javascript) and XNA (C#). The HTML5 solution is for web development, and it’s a good one though it’s just [one of many](http://html5gameengine.com/) and certainly not the best. Problem is that it shares the same API with cocos2d-iphone and cocos2d-x, which naturally slows down development and requires making compromises.

As is inherent in cross-platform development just doing one platform right will take longer than with a native engine. Keep this in mind before blindly following into the pit that is cross-platform development with C++. Also consider that most development happens in China, which means documentation and forum responses sport the occasional grammatical mishap ranging from enjoyable to misleading.

**Summary**: if you’re married to C++ or you want to build for platforms other than iOS and Android then by all means use cocos2d-x. Otherwise you may be better off using Sprite Kit and perhaps later port your hit app via Apportable.

### Other solutions for making 2D mobile games

[ Sparrow Framework](http://gamua.com/sparrow/) - I love its clean, modular design. It’s probably closer to Sprite Kit than cocos2d-iphone itself, and many seem to miss that point. That only shows how oblivious developers are to this undeservedly niche cocos2d competitor. Which is also why you probably don’t want to look into it. As far as I understand the developers have moved on to the Starling Framework, same concept but in Flash.

** Corona SDK** - it’s free for Indies ($100k yearly revenue) and beginner friendly thanks to Lua. I like the code sharing section, many prebuilt templates available. However you can’t do any native API or custom C/C++/ObjC programming without the unlimited Enterprise plan which costs $2,388 annually, per seat.

** Unity** - hey it’s free … no, it’s not! They give away their free version with severe strings attached (forced splash screen, no batch drawing) and once you’re locked into the Unity ecosystem your only options are to move back out or pay $3,000 just for iOS support (Android adds another $1,500 price tag). That said, Unity is a great tool if you can afford it and the new 2D toolset should help establish Unity as a tour de force even for 2D games.

Then there’s a whole range of game making tools, all catering to more or less absolute beginners and/or non-programmers. They are: [Stencyl](http://www.stencyl.com/), [Game Maker](http://www.yoyogames.com/studio), [Game Salad](http://gamesalad.com/), [Game Editor](http://game-editor.com/) and probably some more that I don’t know of.

Stencyl boasts an impressive visual programming interface and is widely adopted as learning, prototyping and actual development tool. I’m a big fan of Game Maker, at least I was until I stopped using it ~5 years ago. Worth checking it out, though I can’t say anything about their mobile ports. Game Salad I never tried, but they did some questionable business strategy changes which rubbed users the wrong way. It may be worth giving it a try, but in my book it’s only a third choice. Game Editor is sort of an underdog, underground tool with some wackiness to it. Not surprisingly and in its defence it is open source.

**Summary**: if you’re just starting out as a programmer and want to make a game, then definitely look into using a game making tool before you go down the pure programming route. For one, you’ll pick up a lot of programming logic experience that way and you stand a fighting chance of completing your game. Progress with a game making tool is much easier to come by, more visual and ultimately more rewarding for someone who is just starting out.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Corona is free

Good point, I’ll edit.

[…] also recently did compare Sprite Kit with cocos2d-iphone and cocos2d-x and other game […]

Nice collection of 2D mobile games tool solution. I also tried to collect few tools and made a blog post: http://www.xcubegames.com/blog/5-must-mobile-game-development-tools/