---
title: Love2d - first encounter
url: https://randomtower.blogspot.com/2012/09/love2d-first-encounter.html
author: Pubblicato da Marte
published: '2012-09-12'
source_blog: Random tower of games
source_site: https://randomtower.blogspot.com/
category: game programming
fetched: '2026-04-13'
---

Love2d is an awesome library to make games. In last few days I've experienced a bit with it and now I'm ready to present my thoughts about it.

**Getting started**

Just follow guide on the

[wiki](https://love2d.org/wiki/Getting_Started)and

[setup your notepad++](https://love2d.org/wiki/Notepad++). Installation is easy and painless: click, download, start. Once installed love, you can play love games from the web, just download ".love" files and run. This "magic" is possible just because love files are .zip files, with all game-related resources into it.

After some thinking I'm okay with this, but scanning amazing useful love2d

[forums](https://love2d.org/forums/)I've realized that this can be a side effect: anyone start from scratch, build something, then build a framework on top of Love2d.. it's crazy, right?

Anyway, just setup a fast-keyboard-run command on my notepad++ and I'm ready with HelloWorld Love2d program:

Not so exiting, but is the first step!function love.draw()

love.graphics.print("Hello World", 400, 300)

end

**Pros**

One good think about Love2d is you write with

[Lua](http://www.lua.org/), Is something different from Java or Actionscript, or even C# and I'm not here to teach you Lua. But with a scripted language is a way to change your way of thinking (maybe, I know!).

So first, forgot about classes and so on: you have functions, structs (like in the old c) and a lot of useful functions do deal with it.

**Cons**

Well.. Lua is not so easy. You want to remove something from a table? Is not possible, not in a way you like: you need to store index of element in table and then remove it.

Or again, you want to declare a new anonymous-type with some new properties? You can, but after few lines code could be a mess. You can, sure, use require to split your code in different files, but without an IDE (I mean, something like

[LuaEclipse](http://luaeclipse.luaforge.net/index.html)) dedicated to Love2d (and again I've tried

[some of them](https://love2d.org/forums/viewtopic.php?f=4&t=10207)) it's hard to handle big projects.

**Conclusion**

Love2d is great for small projects and challenge, to get something quick on screen. Lack of a decent IDE and knowledge of Lua can stop you from move from simpler examples to more complex games.

Distribution of games is really easy, something valuable this days.. so my suggestion is to take a look to love2d, because deserve it!

![]() |

## No comments:

## Post a Comment