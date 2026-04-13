---
title: 'A droid story: from desktop to android'
url: https://randomtower.blogspot.com/2017/05/a-droid-story-from-desktop-to-android.html
author: Pubblicato da Marte
published: '2017-05-12'
source_blog: Random tower of games
source_site: https://randomtower.blogspot.com/
category: game programming
fetched: '2026-04-13'
---

I've been able to add android support for my game "A droid story", thanks to libgdx awesome support on that side.

The roadmap was really simple, after

[initial setup](https://github.com/libgdx/libgdx/wiki/Setting-up-your-Development-Environment-(Eclipse,-Intellij-IDEA,-NetBeans)):

1) create a new project with android support

2) move all source file into new project

3) compile & run

The pain point here is the support for touch on android device, in particular my game was keyboard controlled, so add a new type of input was a learning path.

First I studied the api on that side, found an example and build an "invisible" interface, so the player can move the little droid without any controls on screen. The result was.. not so nice in my opinion! Mainly because the input was strange and not so precise.

So I switched to a more clear interface with button on phone screen and after realize that reinvent the wheel is not the right choice, I've opted in use the

[ui buttons](https://github.com/libgdx/libgdx/wiki/Scene2d.ui)to do the dirty job.

![]() |

As you can see the result is just a starting point, but works! I'm happy also on support for the back button, something easy that every android developer should consider for theirs apps!

More info ( and a runnable build) soon, after some tests!

## No comments:

## Post a Comment