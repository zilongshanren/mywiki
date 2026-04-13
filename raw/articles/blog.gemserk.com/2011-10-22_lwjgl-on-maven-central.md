---
title: LWJGL on Maven central
url: https://blog.gemserk.com/2011/10/22/lwjgl-on-maven-central/
published: '2011-10-22'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

Hi we are happy to announce that [LWJGL](http://lwjgl.org) is available in [Maven](http://search.maven.org/#search%7Cga%7C1%7Clwjgl) central. We worked hard with the [@LWJGL](https://twitter.com/#!/LWJGL) people to make this possible.

### Why was it important to get LWJGL into central?

Well, one of the biggest pains when using maven is having your dependencies available from central, if they are, you just need to add a little snippet of XML and you are done, if they aren’t, then you need to install them manually to your local repo or to a private maven repo.

This is a problem in itself but this also means that projects that depend on something that isn’t available in central, can’t get into central themselves, making the work needed to use it grow exponentially.

### Previous work

In order to get LWJGL into central we had to work first with [@Endolf](https://twitter.com/#!/endolf) to get [JInput](http://search.maven.org/#search%7Cga%7C1%7Cjinput) into central so a huge thanks to him as well.

### Future plans

Now that we got LWJGL into maven central, we can start thinking about trying to convince the authors of other useful libs that use LWJGL like [Slick2D](http://slick.cokeandcode.com/), [libGDX](http://libgdx.badlogicgames.com/), [nifty-gui](http://nifty-gui.lessvoid.com/), etc to make their libs also available on central (of course we would love to help make this a reality as well).

If you use [LWJGL with maven](http://lwjgl.org/wiki/index.php?title=LWJGL_use_in_Maven), we would love to hear from you and feel free to ask us anything.

More information:

[LWJGL Forum post](http://lwjgl.org/forum/index.php/topic,3707.0.html)where we worked with the LWJGL guys to get it to central, mainly for reference and historical purposes[LWJGL use in Maven](http://lwjgl.org/wiki/index.php?title=LWJGL_use_in_Maven)- One of our posts explaining the
[Maven Natives plugin](https://blog.gemserk.com/2011/03/02/maven-natives-dependencies-project/)for using natives with maven projects