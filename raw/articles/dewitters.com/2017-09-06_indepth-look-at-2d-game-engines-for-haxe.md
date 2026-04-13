---
title: Indepth look at 2D game engines for Haxe
url: https://dewitters.com/indepth-look-at-2d-game-engines-for-haxe/
published: '2017-09-06'
source_blog: deWiTTERS
source_site: https://dewitters.com
category: game programming
fetched: '2026-04-13'
---

*(Updated on 16/9/2017, after receiving more info at the Haxe Summit)*

So you want to make a cross platform 2D game using [Haxe](http://haxe.org/). Good choice! But what will you choose as game library?

# Preamble

There are a tremendous amount of Haxe game engines out there, so I’m limiting my discussion to the most alive and kicking 2D engines. So I won’t be covering [Flambe](https://github.com/aduros/flambe) for example, which has its last commit in 2015.

Remark that Haxe is open source, and so are all the game engines mentioned here.

I’m not the first one to cover game engines for Haxe. And if you didn’t do any research yet, here are other overviews of Haxe game engines. However, none of them is as up-to-date as mine :). While they list more game engines, I focus on the most popular ones.

## Disclaimer

Although I have lots of experience with game development and multiplatform game libraries, I don’t have a lot of experience with Haxe. Which means I have no in-depth experience with any of the libraries mentioned below.

But since I need to decide to which library I will port my ActionScript3 based [RPG Playground](http://rpgplayground.com), I’m gathering all the information I can find in this post.

If I made false claims below, or incomplete, please let me know so I can update it. This will make me smarter (thanks!), and doesn’t give wrong information to anyone reading this.

# How close to the metal?

Haxe game engines can be divided into 2 broad categories:

- High level game engine
- Hardware Abstraction Layer for multimedia purposes

The high level game engine includes all bells and whistles such as collision detection, scene management, animated sprites, game loop, etc, … . If you want to quickly get into making your own game, you should choose this kind of game engine.

The hardware abstraction layer (HAL) focuses on providing you with a consistent API to access system calls, events and rendering abilities. This is closer to the hardware and probably features a simpler interface. If you are used to building game engines, you can probably get a lot of mileage out of these kind of engines.

# Which Haxe target to reach which platform?

Haxe cross-compiles to various languages. And because of this, different platforms can be targeted by the game engines.

However, the documentation of the game engines is pretty sparse on which target language is used for which platform. So I decided to include this in the overview if possible.

For example, a HTML5 target can be reached by compiling to JavaScript, but it is also possible to compile to C++ and use [emscripten](http://kripken.github.io/emscripten-site/) to reach HTML5. It is not always clear which one they are using.

# Game development frameworks, not libraries!

As an old school developer, I thought Haxe was the programming language, which comes with its own compiler and build tools. And the “game engines” are just haxe libraries.

But to my surprise, this is not the case!

In reality, the game frameworks use Haxe as the cross compiler, and then do their own thing to package the application and resources into whatever you are targeting.

So in that sense, the game engines discussed here include their own build and package tools. Kha even takes it a step further and provides a custom IDE called [KodeStudio](https://github.com/Kode/KodeStudio).

# Meet the families

In the Haxe game development ecosystem, there seem to be a lot of high level game engines that use an underlying Hardware Abstraction Layer (or even multiple). We can distinguish 3 families of game engines that are each based on the same HAL:

- Lime
- Kha
- Snow

# The Lime family

The Lime family is by far the most popular one. There is an obvious reason for this. OpenFL and NME expose a Flash API. So for all the Flash based libraries that were ported to Haxe, it made sense to use the same API calls. Flixel, FlashPunk and Starling are such examples.

The game architecture family tree looks like this:

HaxeFlixel Starling awe6 HaxePunk ... |_____________|___________|_________| | | | OpenFL (HAL with Flash API) | | NME (HAL with Flash API) Lime (HAL)

[NME](https://github.com/haxenme/nme) (Native Media Engine)

The API of NME is based on Flash, but sometimes diverts a bit from it.

The main focus is on native targets for Android, Windows, Mac and Linux. It doesn’t have any HTML5 Targets.

NME is the predecessor of OpenFL and Lime.

It is mainly written in C++.

Very sparse documentation, but does offer a lot of sample projects.

[Lime](https://github.com/openfl/lime) (Light Media Engine)

Lime offers Haxe developers a cross platform API for windowing, events, audio, network access and rendering.

For rendering, it doesn’t have a generic layer, but exposes the current context of the platform: HTML5 Canvas, WebGL, Flash, … .

So it basically comes down to Lime offering a unified interface for all system stuff, except for the rendering.

You will have to take care whether you are on a platform that supports OpenGL or Canvas or something else.

For HTML5 and Flash Player, the abstraction layer is implemented 100% in Haxe.

For native targets, it uses a custom C++ library that makes use of underlying libraries such as SDL2, Freetype, libogg/jpeg/png, zlib and OpenAL.

Lime started as a fork of the lower layers of NME, but was rewritten in Lime 2. The higher layers were forked to OpenFL.

Lime outputs to JavaScript, C++, Neko, Flash/AIR, Emscripten, and as a proof-of-concept, ran on C# and Java.

### Thoughts

Weird that they use SDL2 underneath, but didn’t bother to use this same interface to unify the other rendering targets such as HTML5 Canvas and Flash.

OpenFL uses Lime as a base, and puts a Flash API on top of it. For the system calls it doesn’t add much to Lime in that sense.

But if you look at rendering, OpenFL is able to put a unified API for different underlying rendering contexts.

Impressive showcase with games such as [Papers, Please](http://papersplea.se/), [Defenders Quest](http://www.defendersquest.com/index.html) and [many others](http://www.openfl.org/showcase/).

100% Haxe code.

Lot of community support.

OpenFL started as a fork of the higher layers of NME (OpenFL Legacy), but since OpenFL 3 the API is all original.

And [effort](http://community.openfl.org/t/smm-power-rangers-mega-battle-ps4-xbox-one/8481) was [made](http://www.fortressofdoors.com/openfl-for-home-game-consoles/) to support consoles with some customization. But it seemed to never reached the goal. Although I saw a tweet from [Lars Doucet](https://twitter.com/larsiusprime) that OpenFL now [runs on consoles](https://twitter.com/larsiusprime/status/626580221760786432).

Port of the Flash Flixel engine, which now surpassed its ancestor. Lots of documentation, big community. Lots of functionality included.

Not as active as HaxeFlixel, but for the rest seems very much alike.

Haxe port of the (Flash) Starling game engine.

The main selling point of Starling is that everything is rendered on the GPU. But for Haxe Starling, it is unclear what remains of this advantage, since multiple other Haxe games engines do this.

Awe6 is a game development tool focused on Future Proofing.

I categorized it in the Lime family, but awe6 tries to support different underlying libraries.

The website mentions that a Kha driver is currently in development, but after [a discussion on twitter](https://twitter.com/Hexvalues/status/905544835024777217), it seems nobody really had the time to work on it.

It primary targets casual games for the web via HTML5 or Flash / SWF and mobile via HTML5 or Flash / AIR.

Made by Nicolas Cannasse, the masterbrain behind Haxe. He needed an engine for his game [Evoland 2](http://www.evoland2.com/), so decided to write his own.

Heaps is a cross platform graphics engine designed for high performance games. It’s designed to leverage modern GPUs that are commonly available on both desktop and mobile devices.

The framework currently supports HTML5 WebGL, Flash Stage3D, native Mobile (iOS and Android) and Desktop with OpenGL.

Heaps was used by the stunning indie game [Dead Cells](https://dead-cells.com/), which definitely proves that it is a production ready game engine.

- Pure Haxe
- GPU based, no fallback on Canvas for example
- HXSL Shaders
- PS4 support

# The Kha family

The Kha family has the following structure:

KhaPunk Kha2D[Other lesser known engines]| | | |_______|______________| | Kha (HAL)

Even some 3D engines use Kha as a base, such as [Armory](http://armory3d.org/). This is possible because Kha supports both 2D and 3D rendering.

Kha favors speed and maximum portability. It can even run on top of Unity3D because it can also target C# (unlike the lime family members). Or target Java.

For native targets, Kha uses [Kore](https://github.com/Kode/Kore), a C++ library. Kore seems to use either Direct3D or OpenGL, and wants to be a 3D capable alternative to SDL.

And as mentioned at the 2017 Haxe summit, the main developer of Kha now has access to console kits. So Kha currently supports all mayor consoles, without going through any intermediate layer such as Unity3D or Unreal. And it’s free, just send [Robert Konrad](https://twitter.com/robdangerous) an email.

I ripped the above image from the Kha wiki, but it seems to forget something. Kore is able to target HTML5 by using [Emscripten](http://kripken.github.io/emscripten-site/). So it would seem to me that Kha can go to HTML5 straight away by using JavaScript, or through Kore/Emscipten by using C++.

# The Snow family

This family gathers around the [snõwkit](http://snowkit.org/), a community, libraries, tools and documentation for Haxe.

Luxe | Snow (HAL) | Linc (Haxe wrapper to native libs)

Light, pure and clean toolkit for building frameworks, applications and games.

Runs natively on Mac, Windows, Linux desktops, as well as iOS and Android devices. It also runs directly in the Web browser using webgl.

Focus on Native & WebGL. No Flash target.

Minimalistic in core and design.

# Conclusion

So what game engine should you pick? To be honest, I have no idea. And I probably made it even more confusing for you now. Sorry! 😉

But let me give you some guidelines to go by, picking the engines that stand out the most.

## HaxeFlixel for new web or mobile games

If you want to make a casual web or mobile game, and don’t want to bother with all the technical stuff, then [HaxeFlixel](http://haxeflixel.com/) is your engine.

It comes with most game functionality included, so you can focus on programming your game. Probably the easiest engine to get started.

## OpenFL for porting over Flash games

If you already have a Flash game in ActionScript3 that you want to port, then [OpenFL](http://www.openfl.org/) is probably the way to go. It offers the same API that you are used to.

## Heaps for high performance native games

If you want to make high performance native games, which you want to sell on Steam or consoles, [Heaps](https://github.com/HeapsIO/heaps) is probably your pick.

It offers more game functionality than Kha, but is unfortunately not as portable.

## Kha for multiplatform game frameworks

If multiplatform is an absolute necessity for you, and you don’t mind giving up basic game functionality for that, then [Kha](http://kha.tech/) is the way to go.

Or if you want to write your own game framework, go with Kha.

But remark that this library is a hardware abstraction layer, not a full blown game engine. So you get a fast, multiplatform API, but you will have to do a lot of things yourself.

## My pick for RPG Playground: Kha

But for me, I will go with Kha. I like a simple, unified API with lots of speed behind it, supporting a ridiculous range of platforms.

Since I’m writing my own game framework anyway, the lack of functionality is not a show stopper.

Hope this helped you out.

Regards,

deWiTTERS.



## 1 Comment

## Ra · September 30, 2020 at 01:54

Thanks so much for this write up!

Although now old, it really helped me understand the Haxe world. With so many libraries trying to accomplish the same damn thing—make a flash-like game engine—it’s reallly damn confusing!

Kha seems to be the one for me too. 🙂

Luxe v1 is dead. Luxe v2 is closed source. Haven’t heard from the snowkit people in years.

HaxePunk, though not updated in years might still work… I’d personally start with KhaPunk though, as HaxePunk seems to have become a bit bloated.

Heaps is indeed a game engine, but it seems to follow the HaxeFlixel line of making a bloaty, customized engine, as opposed to a minimal general one. I also personally don’t like the base game object tree structure. It seems to copy the display ojbect tree from Flash, wherein every gameobject can have a parent or children gameObjects. I’d rather that not be built-in.

For 2020, I’d say DIY starting with Kha, or DIY starting with MonoGame, or DIY starting with a C/C++ media framework (SDL, BGFX, sokol, etc.). Forget all the Flash crap (OpenFL, NME, HaxePunk, HaxeFlixel, etc.).