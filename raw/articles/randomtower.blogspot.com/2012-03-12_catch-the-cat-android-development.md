---
title: Catch the cat Android development
url: https://randomtower.blogspot.com/2012/03/catch-cat-android-development.html
author: Pubblicato da Marte
published: '2012-03-12'
source_blog: Random tower of games
source_site: https://randomtower.blogspot.com/
category: game programming
fetched: '2026-04-13'
---

[catch the cat](http://randomtower.blogspot.com/2012/03/catch-cat.html), it's time to get some info about Android development

**IDE, coding and time**

Working with android is pain without a real device: emulator isn't comparable with Android device so keep in mind this. Eclipse is a first class IDE, many many plugins and more important

[Android Development Tools](http://developer.android.com/sdk/eclipse-adt.html)! With this tools, Eclipse and your phone you can start android development for free, simple right? Many tutorial around so I will not waste time setup all things.

**Library for making games with Android**

I've worked a bit with Slick (

[Fuzzy](http://randomtower.blogspot.com/2011/09/fuzzy-is-out.html),

[Escape from colors](http://randomtower.blogspot.com/2010/10/escape-from-colors.html),

[Pong clone](http://randomtower.blogspot.com/2010/09/pong-clone.html),

[You cant' win](http://randomtower.blogspot.com/2009/09/you-cant-win-release.html),

[Cute tower defense](http://randomtower.blogspot.com/2009/03/cute-tower-defense.html),

[Jpacman](http://randomtower.blogspot.com/2009/02/jpacman.html)are some examples) so when Slick creator

[announced](http://slick.javaunlimited.net/viewtopic.php?f=21&t=2834)an adaptor for using it into Android I've been interested in it.

Main problem with Slick AE is no information :( just a

[forum here](http://slick.javaunlimited.net/viewforum.php?f=21)where ask ) and a

[svn repository here](https://bob.newdawnsoftware.com/repos/slick/trunk/Slick-AE/)with an

[example here](https://bob.newdawnsoftware.com/repos/slick/trunk/Slick-Android-Test/).

So working with Slick AE is in first instance a matter of faith and deveotion to Slick: if you never played a bit with Slick, don't try Slick AE, because you have to understand a little bit about Slick before continue.

Slick AE is only a wrapper around Libgdx calls to Android so you can program games with Slick, try it and deploy into Android, cool right?

There are a lot of alternative for example

[Libgdx](http://code.google.com/p/libgdx/): it's different from Slick, but not so much and you can do same things!

[Gemserk](http://blog.gemserk.com/)for example use it a lot for

[their games](https://market.android.com/developer?pub=Gemserk+Studios)

**Downsides**

Bad thins happens sometimes: for example when you have a beta library like SlickAE and a no real layer for separate desktop version from Android version. So input game name is a thing that in desktop version is not possible. It's just an example how much difficult could be working in a mixed enviroment Android/Desktop, without a preparation for this. My suggestion is to write little games, try different libraries and then move to bigger projects!

**Conclusion**

Catch the cat it's a small game, build with no todo list, no plan and no objective than learn how to build and deploy a little game on Android. And this experiment, despite some flaws (code is a mess, one big class for everything, one for storing information into sql lite android memory and so on..) I've learned a lot.

Games could be a nice way to learn how to develop in a new platform and any Java programmer must try to do something for Android: it's easy, fast and cool!

## No comments:

## Post a Comment