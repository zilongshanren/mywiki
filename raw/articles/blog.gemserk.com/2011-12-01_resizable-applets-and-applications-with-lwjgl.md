---
title: Resizable Applets and Applications with LWJGL
url: https://blog.gemserk.com/2011/12/01/resizable-applets-with-lwjgl/
published: '2011-12-01'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

Some posts before, in the [comments section](https://blog.gemserk.com/2011/10/10/detecting-collisions-using-libgdx-pixmap/), [Gornova](https://randomtower.blogspot.com/) asked me to write about resizable Applets if I had some time. As I never used resizable LWJGL Applets, I had to do some research. This post is to show what I found.

(note: LWJGL version 2.8.2 was used for all the tests I made).

### Introduction

LWJGL Applets are similar to LWJGL Applications, they work using a class named [Display](http://lwjgl.org/javadoc/org/lwjgl/opengl/Display.html) which uses an AWT [Canvas](http://docs.oracle.com/javase/6/docs/api/java/awt/Canvas.html) component. On desktop, you create a JFrame or similar and add inside a Canvas, on Applet you just create the Canvas and add it to the Applet. Unless you want some custom behavior, I believe that is the common usage.

(note: using fullscreen is a different case but has no meaning for this post)

### How to resize an Applet

To resize an Applet on the browser, two possible ways are, use Javascript to change the applet tag sizes or just configure the HTML applet tag to adapt to its container size, so if you resize the browser window then all corresponding HTML components are resized.

The other way around, suppose you have a way inside your game to choose the game resolution, you will have to communicate that to the Browser, probably calling a Javascript function from your Applet to let the Browser react to the change.

### How to handle Applet resize

If you are working with LWJGL directly, then it depends a lot of how which kind of layout are you using for the container of the Canvas object. For example, if you chose a layout which grows to the parent container size, then each time you resize the container, the Canvas will be resized. If you chose another layout, then maybe you will call Canvas.setSize() by hand.

However, you need to react to that change in your game, to do that the best way (imho) is use a similar approach LibGDX does. What LibGDX does is, its stores the current Canvas size on each iteration of the main application loop, on the next iteration, if the Canvas size is different to the stored, then it calls a resize() method to tell your game the screen size changed.

Another way is to create a [ComponentListener](http://docs.oracle.com/javase/tutorial/uiswing/events/componentlistener.html) and add that to the Canvas component so each time the componentResized() method is called you resize your game. However as all the AWT stuff runs in another thread you need to store the new size and process the resize in your LWJGL thread to avoid problems.

### What to do inside your game

The very basic approach is to just modify the OpenGL viewport of your game, then the game is scaled to the new size and, in some cases, that should be enough.

glViewport(0, 0, width, height);

However, You may want to take care about aspect ratio since just scaling the game could look ugly. One option is to modify the viewport in values to maintain the aspect ratio you want, for example:

glViewport(0, 0, width, width / aspectRatio);

You could also provide different common aspect ratios (4:3, 16:10, 16:9, etc). However, I believe the best option is to provide fixed commonly used resolutions like 640x480 or 800x600 instead.

In some cases you could want to adapt your game elements, for example GUI stuff, where you may want to maintain the element sizes and move them accordingly over the screen instead just scaling them.

Then, you have to take care of the user input. As mouse location is dependent on the viewport size, you will have to take that in mind when interacting with part of your application, like the GUI stuff, after a size change. For example, LibGDX [Camera](https://code.google.com/p/libgdx/source/browse/trunk/gdx/src/com/badlogic/gdx/graphics/Camera.java) uses the current viewport size when using project and unproject methods (which allow you to transform world coordinates to viewport coordinates and vice versa).

~~Not so sure as I am not an OpenGL expert but if you work different cameras (model + projection matrices) you probably need to update them in order to render everything in the correct way. I have to go deeper in this issue.~~

Optionally, you may want make other changes when reacting to the resize like loading HD assets if you go to a higher resolution and vice versa.

### Some issues

- You have some glitches if you do resize in real time (tested myself, but cant find references right now). However, in general nobody does this so it is not a big problem.
- I believe Applet resizing
[is not working on mac](http://lwjgl.org/forum/index.php/topic,4267.msg23199.html#msg23199)yet.

### Conclusion

Handling all the mentioned things when resizing LWJGL Applets and LWJGL Applications depends a lot on the game you are making, in some cases the basic approach work fine and should be easy to implement.

Despite the article was focused mainly on LWJGL Applets, great part of the findings can be applied to LWJGL Applications as well.

This post is only to show some basic experimentation I made on the subject, as I said before, I am not an OpenGL nor LWJGL expert, so some assertions could be wrong. If you have more experience and want to contribute your opinion, feel free to do it.

Thanks and hope you like the post.