---
title: Testing Android controls on libGDX PC application using libGDX remote
url: https://blog.gemserk.com/2011/09/09/testing-android-controls-on-libgdx-pc-application-using-libgdx-remote/
published: '2011-09-09'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

When testing our games, sometimes we only need to test the game controls on the Android devices, not all the game, and deploying it on the device is always slower than running it on the PC.

The [LibGDX library provides a way](http://www.badlogicgames.com/wordpress/?p=1590) to send your Android device input data to through the network, one of the possible uses is to control your libGDX PC application with it.

Here is a demo video using the remote input, made by libGDX team:

(note: magic starts after minute 2)

In the case of Super Flying Thing, we need it when testing and debugging some controls that cannot be tested directly on PC like the TiltController for example (we need device orientation data). Recently, we starting using it also to test and customize other controls like the the ClassicController (despite it has a bit of lag in some cases).

Sadly, my camera is also my android phone so I can’t make a video of how we are using it.

One interesting point of this is that we could use multiple android devices (and probably other devices like iPod/iPhone/iPad/others) to create multiple wireless controllers for PC, and that, for example, could be funny if we want to make a local multiplayer game.

Another interesting point is that you could implement your own remote input server to read the device input data sent by the [GDX Remote Android Application](https://market.android.com/details?id=com.badlogic.gdx.remote), so you wouldn’t be forced to use libGDX in your server application.