---
title: Dassault Dev Diary 1 - Using layers to compose images
url: https://blog.gemserk.com/2010/07/16/dassault-dev-diary-1/
published: '2010-07-16'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

Dassault is a game I started for the [Game Jolt Demake Contest](http://gamejolt.com/blog/indie-game-demake-contest/23/) and it is based on the excellent game [Droid Assault](http://www.puppygames.net/droid-assault/) from [Puppy Games](http://www.puppygames.net/). The contest is already finished but I will keep working on the game with the purpose of learning some techniques (some of them based on the original game) and to share my experience in doing so.

In the original game, the droids are rendered with two different colors if they are from player’s team or not, this is an example:

![player droid player droid](../../assets/1cf3216b4c5dcdd9.png)

![enemy droid enemy droid](../../assets/276a28158e02cd3e.png)


For Dassault I wanted the colors to be based on each team’s color but when having a lot of teams I don’t want to have one sprite sheet for each one and I don’t want to limit the teams quantity beforehand.

One solution is to have a base sprite sheet and then color it with some script, to generate a lot of sprite sheets. One problem is that it requires a lot of files and that I have to regenerate all of them if something has changed in the base sprite sheet. Also, the number of teams cannot be changed during the game.

Another solution, based on this [post](http://www.puppygames.net/blog/?p=178) from [Puppy Games Blog](http://www.puppygames.net/blog/), is to render the droids in several layers, each one with its own color. With this approach, I can paint some layers with one color and the others with default color to make them look just the way I wanted. Here is an example:

![droid shadow droid shadow](../../assets/5c8fb6abfe769066.png)

![droid legs droid legs](../../assets/f3ddbe03f5d7fe88.png)

![droid background droid background](../../assets/3d1a3ca2502ac257.png)

![droid eyes blur droid eyes blur](../../assets/eaf7cdb988ae93cf.png)

![droid eyes droid eyes](../../assets/7ac6b3777de4e462.png)

![droid result droid result](../../assets/56b4c1b166d378ef.png)


Now coloring some layers:

![droid shadow droid shadow](../../assets/5c8fb6abfe769066.png)

![droid legs colored droid legs colored](../../assets/2fa9cfa9fd92a818.png)

![droid background colored droid background colored](../../assets/3bb7c8e5e9f0f3a1.png)

![droid eyes blur colored droid eyes blur colored](../../assets/f5d9d5644664f21e.png)

![droid eyes droid eyes](../../assets/7ac6b3777de4e462.png)

![droid final colored droid final colored](../../assets/2b506b65477cbffc.png)


That was the solution used and it worked right. Inside the game we render the layers in order, to produce the correct result.

To design the images in several layers we are using [Gimp](http://www.gimp.org/). I try different color palettes to see how they’ll look inside the game. Then I save the layers in gray scale exporting each one in a different image file using [Export Layers as PNGs](http://registry.gimp.org/node/18440) python plug-in for Gimp. The images are ready to be colored inside the game.

Here are some screenshots showing how it looks inside the game:

And here you have a video:

You can try the game [here](http://www.gemserk.com/prototipos/dassault-webstart-release/launch-webstart.jnlp). That’s all for now, next time I am planning to talk about animations.