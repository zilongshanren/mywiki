---
title: LWJGL Applet Loader
url: https://blog.gemserk.com/2011/02/17/lwjgl-applet-loader/
published: '2011-02-17'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

In a previous post we talked about Java Games deployment options, in this post we want to talk about one custom solution provided by the [LWJGL](http://lwjgl.org/): the [LWJGL Applet Loader](http://lwjgl.org/wiki/index.php?title=Deploying_with_the_LWJGL_Applet_Loader_-_Introduction).

The LWJGL Applet Loader is an Applet which performs a lot of common deployment tasks:

- It shows a nice and customizable loading screen when deployment is being processed, with detailed messages for each task: downloading file.jar, extracting file.jar.gz, etc.
- It downloads all required dependencies. If they are compressed using gzip, LZMA or Pack200, it extracts them.
- It has a cache for all your dependencies so if one dependency is not modified on the server, then it is not downloaded again.
- It configures the Java library path to load all your native dependencies.
- Finally, it runs your game’s applet.

A feature in mind when developing the LWJGL Applet Loader is that it should start as fast as possible, for that, the jar of the Applet Loader should be really small. The idea is to speed up all the Java loading screen so it can show quickly your custom loading screen.

It provides a lot of parameters in order to let you customize deployment stuff, like which natives dependencies you need for a specific platform, the logo and progress bar, etc. Full documentation of the parameters is on the [API docs](http://www.lwjgl.org/javadoc/org/lwjgl/util/applet/AppletLoader.html) and you also have a great tutorial at [LWJGL Wiki](http://lwjgl.org/wiki/index.php?title=Deploying_with_the_LWJGL_Applet_Loader_-_Introduction).

This is how it looks when loading an Applet using the LWJGL Applet Loader with the default loading screen:

![](../../assets/baf3a659ea82a05f.png)


note: Even without customization, it looks much nicer than Java default loading screen.

#### Pros

- It lets you customize loading screen, and create Applet using natives support in an easy way.
- It starts fast. This avoids some browser
[freeze bug](https://bugs.launchpad.net/ubuntu/+source/sun-java6/+bug/288642)when starting a Java Applet, like Firefox on Linux platforms. - It handles different compression options like gzip and LZMA, it also handles Pack200 jars.
- It works on Mac OS, that is a big difference versus running New Generation Plug-In Java Applets, because they are disabled on Mac OS.
- It is open source and the guys maintaining it are always open to receive patches and improvement ideas.

#### Cons

[Pack200 and compression](http://download.oracle.com/javase/6/docs/technotes/guides/deployment/deployment-guide/pack200.html)stuff is not done automatically, you have to specify exactly which file you want to download (example: you have to specify that you want to download somedependency.jar.pack.gz instead of having the Applet Loader to detect automatically which version to download by receiving the content encoding from the server).- Assumes you need native dependencies, so you need to fill some Applet parameters even if you don’t need them. (we want to add an RFE for that)
- It doesn’t use the same cache other Java Applets or Java Web Start use. That means you have to download twice one Applet distributed using LWJGL Applet loader and Java Web Start, and it will cost you double space.

To see LWJGL Applet Loader working you can try one of our games [here](http://www.gemserk.com/zombierockers-jnlp.html) (warning: link could be broken in the future) or you can try a working and stable version of a game using LWJGL Applet Loader [here](http://www.minecraft.net/play.jsp), its name is [Minecraft](http://www.minecraft.net/), don’t know if you know about it.

In one of the next posts we want to talk in detail about another deployment option we mentioned before, now that we have some experience using it: getdown.

## References

[https://bugs.launchpad.net/ubuntu/+source/sun-java6/+bug/288642](https://bugs.launchpad.net/ubuntu/+source/sun-java6/+bug/288642)

- LWJGL API Documentation -
[http://www.lwjgl.org/javadoc/](http://www.lwjgl.org/javadoc/) - LWJGL Wiki -
[http://lwjgl.org/wiki/index.php](http://lwjgl.org/wiki/index.php) - Pack200 and Compression for Network Deployment -
[http://download.oracle.com/javase/6/docs/technotes/guides/deployment/deployment-guide/pack200.html](http://download.oracle.com/javase/6/docs/technotes/guides/deployment/deployment-guide/pack200.html)