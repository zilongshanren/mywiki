---
title: JNLP Applet Loader
url: https://blog.gemserk.com/2011/02/20/jnlp-applet-loader/
published: '2011-02-20'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

Now that we talked about the [LWJGL Applet Loader](https://blog.gemserk.com/2011/02/17/lwjgl-applet-loader/), we want to talk a bit about the JNLP Applet Loader. In a quick description, the JNLP Applet Loader is an adapter of the LWJGL Applet Loader to make it work with JNLP files.

### Motivation

All of our games were previously released through Web Start and New Generation Plug-In Applets using JNLP files and we wanted to use LWJGL Applet Loader in an easy and seamlessly way.

### Solution

Our solution was to create an Applet to parse the JNLP file and with that information, create the parameters needed in order to run the LWJGL Applet Loader.

Right now, it works with two parameters:

`al_jnlp`

: an URL used for telling it where to find the JNLP file to use in order to launch the game. First, it downloads and parses the JNLP file and with the information provided, and with that, it creates all LWJGL Applet Loader parameters (al_jars, al_main, etc).`appendedJarExtension`

: a String suffix appended to all jar and natives dependencies in order to let the LWJGL Applet Loader to download optimized with pack200 and gzip files while it doesn’t process the[content encoding for pack200 and gzip](http://download.oracle.com/javase/6/docs/technotes/guides/deployment/deployment-guide/pack200.html)stuff.

You can find the project on github with the name of [jnlpappletloader](https://github.com/gemserk/jnlpappletloader). It is a maven project, and right now, as it depends on a custom distribution of the LWJGL, it will not compile for you at least you configure your local maven repo with the required dependencies. Once the LWJGL is on maven central repo, the idea is to depend on it directly.

The best part is that now we can run any of our already deployed games by making a simple applet like this:

<applet code="com.gemserk.jnlpappletloader.util.jnlp.applet.JnlpAppletLoader" archive="jnlpappletloader-full-0.0.4-jar-with-dependencies.jar" codebase="http://someplace.net/jnlpappletloader/" width="640" height="480"> <param name="al_jnlp" value="http://someplace.net/somegame/launch.jnlp"> <param name="appendedJarExtension" value=".pack.gz"> </applet>

[Here](http://www.gemserk.com/test/) is a working example of one of our games using the JNLP Applet Loader (it will look exactly as any other game using LWJGL Applet Loder).

One disadvantage of using the JNLP Applet Loader is the extra time consumed to make the JNLP file request and to parse it vs just using the regular LWJGL Applet Loader. However, using the JNLP Applet Loader lets you to use one centralised JNLP file for all your game’s launch configurations through different deployment options. Also, if you deploy your game in several portals like Games4j, GameJolt, your own page, etc, and you make a change of your game’s launch configuration, your change is automatically replicated because all of them use the same configuration file.

Note that the project is highly coupled to LWJGL Applet Loader, it will not work for any Applet (it should be named something like JNLP Adapter for LWJGL Applet Loader).