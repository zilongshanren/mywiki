---
title: Binding C++ with Lua, Squirrel, Game Monkey and Ocaml
url: https://gamedevcoder.wordpress.com/2013/05/09/binding-c-with-lua-squirrel-game-monkey-and-ocaml/
published: '2013-05-09'
source_blog: Gamedev Coder Diary
source_site: https://gamedevcoder.wordpress.com
category: game programming
fetched: '2026-04-13'
---

This isn’t anything new I did recently but I thought it’s worth putting up on my blog anyway. I was once interested how easy it is to implement binding between C++ and several popular, mostly scripting, languages.

If you search on the internet there’s heaps of libraries that make the process of binding of various scripting languages with C++ easier – check out [this](http://lua-users.org/wiki/BindingCodeToLua) for lua or [this](http://wiki.squirrel-lang.org/default.aspx/SquirrelWiki/-1'.html) for Squirrel binding options.

So, why did I make another one? The first reason was I wanted to learn more about scripting languages and the second one was I wanted the same interface for use with all languages.

**C++ library**

The result of all that is my [MultiScript library](https://code.google.com/p/multi-script/) that:

- allows script code to access C++ classes and functions and
- allows C++ code to access script functions

The library has a very simple C++ interface with 4 different implementations for the following languages:

[Lua](http://www.lua.org/)[Squirrel](http://squirrel-lang.org/)[Game Monkey](http://www.somedude.net/gamemonkey/)[Ocaml](http://caml.inria.fr/)(no binding of classes as this isn’t easily doable with Ocaml vm)

The interface itself consists of:

*ScriptContext*– responsible for maintaining script execution context; registers classes and functions*ScriptStack*– used to handle function calls including pushing and popping values on stack*ScriptObject*– base C++ class for objects to be visible from script*ClassDesc*,*FunctionDesc*etc. – helper structs used to describe classes and functions to be registered

The library comes with a simple test project that runs test programs for all languages and prints out their output along with some statistics. The source code of all these languages is included.

**Ocaml**

Ocaml binding implementation deserves separate paragraph or two as it wasn’t as straightforward as I had hoped originally and I ended up modifying source code of the Ocaml VM (virtual machine) so I could easily load-from-string and run multiple times a chunk of Ocaml code as well as dynamically register C++ functions with Ocaml runtime. Apparently Ocaml VM wasn’t meant to be used as an embedded scripting language the way Lua is.

Binding C++ classes would most likely require a lot more work to get done, so I gave up on that. All of the modifications are clearly marked with “*msawitus*” in the comments.

In order to be able to run Ocaml tests you have to install Ocaml binary distribution from [Inria download site](http://caml.inria.fr/download.en.html). It is necessary to compile (not execute) Ocaml code.

**Summary**

Implementation for both Lua and Squirrel are very similar – after all Squirrel is heavily based on Lua. Getting my head around Lua concepts required a little bit of effort at first but it was straightforward after all. Game Monkey binding was straightforward to do from the very beginning, even without docs and Ocaml was a bit of trial and error experimentation.

I should also point out that this was just an experimental project and it’s nowhere near production quality code. But it’s probably worth looking at if you’re wondering which scripting language to choose for your next project.

Project source code is hosted [here](https://code.google.com/p/multi-script/).

🙂 I’ve just downloaded this for a project I am working on 🙂 I think if classes could be fully added it would be 100% perfect but unfortunatly i am struggling myself. Hopefully it can be added 🙂 but this is a big help 🙂

Actually just saw you have Class support 🙂 this is perfect 🙂