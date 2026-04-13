---
title: Archers Vs Zombies - Dev Log - 03
url: https://blog.gemserk.com/2011/04/28/archers-vs-zombies-dev-log-03/
published: '2011-04-28'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

In the previous post, I was looking for a tool to edit game scenes information in an easy way. Talking with [kevglass](http://www.cokeandcode.com/) at [LWJGL irc channel](http://lwjgl.org/forum/index.php?topic=1044.0) he told me he was using [Inkscape](http://www.inkscape.org/) for that purpose. I also read some time ago that [Rocket Bear Games](http://www.indiebird.com/blog/?p=928) was using it for as level editor as well but I forgot about it.

Inkscape is very interesting for game development because it has a lot of useful features which you could use in different ways in order to achieve what you want. It works mainly with [SVG](http://www.w3.org/Graphics/SVG/) files which are XML.

In this post I will comment some of the features I am using from Inkscape. As I am new with the program, feel free to correct me if I say something wrong about it or if there are better ways or doing stuff.

### Working with different layers

The editor lets you work with different layers. These layers will be exported as different groups which could be parsed later in your game to decide different behavior. In my case, I am using two layers for now, one to put the tools (some tiles) and the other one to define the game world, as the next image shows. This is to avoid processing the tools layer when importing the SVG into the game.

### Custom XML data

Also, as mentioned in the Rocket Bear Games post, Inkscape provides an easy way to add custom XML data to the file so you can add information you will need later to build the scene in your game. Right now, I am adding information to specify the tile type of each element so they could be correctly imported later in the game.

### Parsing the SVG

Parsing the SVG is not an easy task, each node contains a lot of stuff you have to parse in order to get all the information you need. Inkscape adds extra information with its own attributes like labels or the custom XML Data we said before.

Some time ago we used a tiny SVG Java parser named [SVG Salamander](http://svgsalamander.java.net/) to make the [paths](https://blog.gemserk.com/2011/03/03/svg-path-traversal-in-java/) for [Zombie Rockers](https://blog.gemserk.com/games/zombie-rockers/) .

I tried using it again to parse Inkscape generated SVG files but I couldn’t force it to avoid trying to automatically load images when parsing the XML. The project doesn’t contain good documentation about customizing behavior when parsing the file (maybe it even doesn’t let you) and the page is a bit outdated, also [SVN for the project](http://svgsalamander.java.net/projects/svgsalamander/sources/svn/show) was not working when I tried to reach it yesterday.

After that, I found [Batik](http://xmlgraphics.apache.org/batik/) from [The Apache XML Graphics Project](http://xmlgraphics.apache.org/). At first glance, it looked a lot better than the other one, also it is on Maven Central.

Using it wasn’t so easy as I thought, I was using the latest version deployed in the Maven central repository but when I took a look at the [online documentation](http://xmlgraphics.apache.org/batik/using/dom-api.html) it wasn’t the same version, the examples were outdated. Another problem of the library is that it seems AWT dependent and that could be a [problem](https://groups.google.com/group/android-beginners/browse_thread/thread/fc4acc83186274ea?pli=1) if I want to use it on Android.

Also, there were no sources nor javadocs on Maven central so I couldn’t explore the library to understand the behavior easily. I was getting a bit bored and anxious to have something working, so I left the library.

At the end, I am parsing the SVG by hand but I plan to give another opportunity to both libraries.

I will talk more about Inkscape and how I am using it in the next posts.

### Some comments about last post

About the camera zoom I mentioned the last post, Rubén asked me why not using multi touch well known gestures (it seems natural), I thought about adding them but I remembered some people have single touch devices so they wouldn’t be able to use the zoom feature. I end making a single touch implementation, however, I have the idea to implement both solutions in the near future.