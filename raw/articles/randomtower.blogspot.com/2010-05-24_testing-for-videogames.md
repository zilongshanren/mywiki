---
title: Testing for videogames
url: https://randomtower.blogspot.com/2010/04/testing-for-videogames.html
author: Pubblicato da Marte
published: '2010-05-24'
source_blog: Random tower of games
source_site: https://randomtower.blogspot.com/
category: game programming
fetched: '2026-04-13'
---

Today I'm here to talk about testing in videogames. We all know what is it Unit Testing, Integration Testing and so on.. but with videogame all is different.

Central point of a videogame is player, how you can test something that everyone see in different ways?

First make a step back: player is a factor in videogame, interacting with it using User Interface (UI), so first thing is a UI-testing. Enough simple to do and iterate many time you want.

As videogame developer, maybe (lol) you want to keep your gameplay consistent through many iteration of your game. Isn't matter of programming: simply you want to ensure your Mario when hit a turtle jump a little higher: unit testing is not possible here.. but you can always use the good-old-approach (tm) : case testing (CT). Simply write down a level of your game, let Mario fall on a turtle... then let months pass.. after many iteration of your work, will your test case react as planned or not?

Another possible testing is Level Testing (LT): just keep your player (or Mario) at start of each level, and make sure that your player can end every level. Is a tedious testing, before you must play your own game every time, but make you sure that game react as you planned.

-

**UI**: user interface testing,-

**CT**: case testing,-

**LT**: level testing,After this point you can publish something on net, get feedback from players and so on :D

## No comments:

## Post a Comment