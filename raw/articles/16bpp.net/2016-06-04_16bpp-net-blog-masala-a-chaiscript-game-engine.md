---
title: '16BPP.net: Blog / Masala, A ChaiScript game engine'
url: https://16bpp.net/blog/post/masala-a-chaiscript-game-engine
published: '2016-06-04'
source_blog: '16BPP.net: Blog / Page 1'
source_site: https://16bpp.net/
category: graphics
fetched: '2026-04-19'
---

Over the last semester, I've been working on a game engine. It was meant to be a personal challenge for myself, to see if I could make my own game engine with some bare materials. Those being C++, OpenGL, and Qt. I wanted it to be more though. Seeing as most professional game engines these days (developed by community or company) feature some sort of scripting engine, I decided to make my own scriptable game engine.

After some troubles with trying to embed Python & Lua inside of a C++ dummy projects, I discovered this thing called [ChaiScript](http://chaiscript.com/). The tl;dr is that it's a scripting language for C++ that's dead simple to use. I decided to use it for my project since it gave me a no hassle way to add scripting features to my project. It was dead simple as "include the headers," and "give me a pointer to your C++ function/variable, and tell me what you want to call it."

Of course with simplicity, comes some cost. One of the first things for example are the long build times. If you statically include ChaiScript (which is the simplest way of using it), expect to take a small break when compiling. This can be easily remedied by dynamically linking ChaiScript's standard library and including a .dll/.so file alongside your executable. I did this when developing Masala.

I also ran into performance issues with ChaiScript. At the current version (5.8.1), the language is executed using an [Abstract Syntax Tree](https://en.wikipedia.org/wiki/Abstract_syntax_tree). While this is necessary for parsing a language, using it to run code is much slower than it could be.

Enough about ChaiScript, let's talk about the engine itself, Masala!

Masala was built using C++ (14), Qt 5.x, ChaiScript, and OpenGL. I had the goal of trying to create a reusable game engine where you write all of your logic inside of ChaiScript files. It follows a very lose XNA/MonoGame-like pattern. Right now it features:

- 2D
- Cross platform (Built with Linux)
- Featureful sprite object (with animations!)
- Tilemaps (Flare maps)
- Basic sound effects
- Keyboard Input
- Interactive debugging terminal

It's pretty simple. I mean, *very *simple. I don't think it stands up well to other engines that are out there, so I really consider it to be an experiment in using ChaiScript for a game engine.

I implemented two simple games, one being a clone of the classic Atari Pong:

![Pong is (c) Atari Inc.](../../assets/aa13069011d507e7.png)


And another more original one I've dubbed "Grab n' Dodge:"

![It's more difficult than it looks, but not too fun.](../../assets/6a1554c5b7ed8d7b.gif)


I would say that I accomplished my goal in writing a game engine. Something that I have never done. As for the cross-platform part, I was able to get the code to compile on OS X and Windows, but had some trouble upon running it. One of my friends said that he was able to get it working on OS X, but I haven't seen the proof.

**If anyone wants to help me getting this running on Windows or OS X, contact me.** Since it was made using cross platform tools, it should work on all of the OSes Qt & OpenGL support.

And last, you can find the official [code repository over here on GitLab](https://gitlab.com/define-private-public/Masala). It's GPLv3 licensed.