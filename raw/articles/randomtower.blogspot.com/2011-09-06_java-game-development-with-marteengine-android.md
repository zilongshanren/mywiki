---
title: Java game development with MarteEngine/Android
url: https://randomtower.blogspot.com/2011/09/java-game-development-with.html
author: Pubblicato da Marte
published: '2011-09-06'
source_blog: Random tower of games
source_site: https://randomtower.blogspot.com/
category: game programming
fetched: '2026-04-13'
---

|

This is a code story, so be ready :D

The story so far

On

[slick forum user](http://slick.javaunlimited.net/viewtopic.php?t=2702&postdays=0&postorder=asc&start=90)ask me for an example project for

[MarteEngine](https://github.com/Gornova/MarteEngine/)(adding version 0.3 in development on Github, see dev branch) n

[Android](http://www.android.com/)and thanks of his efforts I was able to build and example project. To do this I've started from Slick-AE Template project (

[you can download it here](http://slick.javaunlimited.net/viewtopic.php?t=3713)).

[You can download from here](http://jpacman.googlecode.com/files/MarteEngineandroidDemo.zip)and import into your Eclipse workspace (tested with Eclipse Indigo and Helios, works fine )

Into zip file you can find two projects:

**MarteEngineDemo-Desktop**: base project with desktop launcher and all your game files,

|

**MarteEngineDemo-Android**: just a wrapper project to launch your game on android phone ,

![]() |

I want it too!

For make it work you need to

[setup your enviroment](http://developer.android.com/guide/developing/index.html)like every Android application and then download

[this example](http://jpacman.googlecode.com/files/MarteEngineandroidDemo.zip).

Be sure to change target android sdk for both projects, so it will compile on your enviroment too ( for me is api sdk 8, for android 2.2).

You can play a bit launching Desktop launcher, maybe following

[MarteEngine tutorials](https://github.com/Gornova/MarteEngine/wiki), but what you want is see action, so just launch Android project as Android application (don't try to use virtual device, try on a real Android phone, works better).

I've not tested everything, but integration is good and works fine on my Android 2.2 phone

Conclusion

Get working MarteEngine games on Android is possible and easy, if you start from a template project.

There are some flaws, like understanding how to use new input capabilities, but you can start from that.

## No comments:

## Post a Comment