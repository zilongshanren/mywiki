---
title: Flashdevelop and debug
url: https://randomtower.blogspot.com/2010/02/flashdevelop-and-debug.html
author: Pubblicato da Marte
published: '2010-02-10'
source_blog: Random tower of games
source_site: https://randomtower.blogspot.com/
category: game programming
fetched: '2026-04-13'
---

[Flashdevelop](http://www.flashdevelop.org)(see my past thoughts about it ) you have been surely disappointed by a major lack of debug tool. You can build incredible, funny, little or big games, with incredible graphics, but without a debug support, your only ally is a poor trace command, that copy something in your log.

Finally I've discovered debug plugin that works fine Flashdevelop 3.0.0: you can found all information into

[project's forum](https://randomtower.blogspot.com/to http:/www.flashdevelop.org/community/viewtopic.php?f=4&t=4660&start=0&hilit=breakpoint)and

[wiki](http://www.flashdevelop.org/wikidocs/index.php?title=3rd_Party_Plugins)

*How to install debug plugin:*

Simply download zip, unpack it and copy dll in your

*How to use it:*

To place a breakpoint simple click with left button of your mouse holding shift in gray area between line number and editor area. No click on Debug -> Start to start!

When you start debugging, may notice that three windows appear

* Stack: show call stack before breakpoint, useful to understand what method called before your breakpoint,

* Breakpoints: show defined breakpoints and can be useful to disable breakpoints,

* Locals: show local variable in scope of current step

Now you can Step over your current line, step into or so on. Move mouse to a variable show it value runtime :D

*Some random notes about:*

1) Why is not part of flashdevelop? Because is a plugin, but IMHO this must be part of main distribution after some decent tests!

2) Why this plugin comes without some "standard" shortcuts? I know that standards are difficult to decide and maybe so many shortcuts are used by other plugins, but with

[Eclipse](http://eclipse.org/), for example, I have always see F6 to step, F8 to continue and so on. Users can always customize shortcuts, but newbie can really be less confused about use of this plugin, right?

3) Why moving toolbar and exit from Flashdevelop cause toolbar to be set in "default" position and not in "my" position?

Points 2) and 3) seems to be related to my habit with Eclipse and concept of perspective? I don't kwnow, but I think that position of views/toolbar and shortcuts could be related to debug working, not as "absolute" of Flashdevelop.

This plugin is open source, sure: I , like you, can improve it. Maybe one day, for now I'm learning as3, not C# ;D

## No comments:

## Post a Comment