---
title: Archers Vs Zombies - Dev Log - 02
url: https://blog.gemserk.com/2011/04/27/archer-vs-zombies-dev-log-02/
published: '2011-04-27'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

The game is progressing really slow, I am a bit stuck deciding what to do next.

One of the things I was on was testing a new bow controller where you press over a circular area and fire direction is calculated based on the pressed point and the center of the circle.

There are two versions to control the bow power, one is based on the pressed time, if you press and release quickly it will shoot a weak arrow, if you press and maintain it will fire a strong one.

The other one controls the bow power by the distance of between the pressed position and the circle center:

Another thing I was working on was a camera controller, a way to move and zoom the screen easily. The idea is to press over the screen and move the pointer to move the camera, also if you maintain pressed it will let you zoom in/out. In order to do that, I had to limit some areas where the controllers are enabled or not to avoid both controllers acting at the same time. That is one of the reasons I added the circle bow controller.

As you can see, this new controller is mainly for touch devices, in PC I believe the game could be adapted to use all mouse buttons instead and shoot by pressing wherever you want to press, not only over the circle. To control the camera, you could use another mouse button (or even the keyboard).

### What I should do next

I have a couple of bugs where some zombies die without a reason, also game crashes some times. I believe it must be something in how I process the game entities (zombies, arrows, etc) and I have to fix them in a near future.

### What I really want to do

Putting stuff on the scene right now is quite annoying, I keep modifying some code and run the game to see how it looks, then modify again and again and again until it looks acceptable. To simplify working with the scenes and improve the work done, I am thinking to use/make some graphical editor, something like the [Aquaria Scene Editor](http://gametuto.com/in-game-c-map-editor-tutorial-with-indielib-engine-that-dosent-use-tiles-but-pieced-images-like-in-braid-or-aquaria-games/) is what I have in mind. With that, I could easily test stuff until something nice comes out.

Related with previous point, making bodies for the physics engine matching the sprites shapes is quite complex by putting values directly in game code. The next image shows how the physics body doesn’t match the sprite shape:

So another stuff I want to work on is to have an editor where you can open a sprite and create a physics body graphically. I don’t know if there is a common file format or structure to specify this relationship and/or if there is editors for this stuff.

Finally, as we suck at making 2D graphics, we suck more at making 2D animations (by drawing frame by frame). So, to improve this, I was thinking to use animations made by skeletons like games like [Aquaria](http://www.bit-blot.com/aquaria/) does. By this approach, we could test and create a lot of animations using only some graphics (maybe from a real artist). To accomplish this, I was looking into some 2d skeleton animations editors like the [Aquaria Animation Editor](http://gametuto.com/in-game-c-map-editor-tutorial-with-indielib-engine-that-dosent-use-tiles-but-pieced-images-like-in-braid-or-aquaria-games/), [Demina](http://demina.codeplex.com/) (only XNA), [Grim editor](http://www.allegro.cc/forums/thread/589864) and [Crimson Legend Skeletal Animation System](http://crimsonlegend.marctenbosch.com/manual/sas.html) but I can’t find clear information, there are a lot of custom implementations with custom formats or they are platform dependent (like editors only for Game Maker or XNA). Dunno which is the common solution, maybe using a 3d format like MD5 or something like this but I have to find out yet.

If you are a game developer, how are you making this stuff? I am really interested in learning from other game developers and to use common solutions, I don’t believe I should implement my own unless there is no option (cant deny I am really interested in developing my own).

UPDATE: Some other game developers suggested me to use [Inkscape](http://inkscape.org/) as Scene definition, I could also use it for physics bodies definitions as well adding some meta data to shapes. Could be a great solution, I will test it right now :D.

Thanks.