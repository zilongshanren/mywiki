---
title: FlashPunk Hello World (Shooter)
url: https://randomtower.blogspot.com/2010/01/flashpunk-hello-world-shooter.html
author: Pubblicato da Marte
published: '2010-01-19'
source_blog: Random tower of games
source_site: https://randomtower.blogspot.com/
category: game programming
fetched: '2026-04-13'
---

[Last post](http://randomtower.blogspot.com/2010/01/flashpunk-seems-to-be-jung-good.html)was about

[FlashPunk](http://flashpunk.net/)framework for Flash (Actionscript 3) games.

I wrote about pro and cons of framework and reading punk's code was really interesting. Following good-written basic tutorial i was able to build a little piece of code (after so many critics, try a framework is key factor to understand something), you can found here:

![](https://lh3.googleusercontent.com/blogger_img_proxy/AEn0k_sH_J3agZdO5wAtqQEGpLtS5XSPIGagipzWycOuOQsO5xmnpzGbHFuttHHbkxK6wdNFyOqUkc27STBzadJIOeC21qhkaY7ZLyfWBRIPHZT_N9Rtel24b35IqT_EkCv7GJ9PijL-iiFFiPlswmDg4a9kJheTd9JNe2k=s0-d)


click on image to play

As you can see there are many "basic" piece for a game:

- multiple sprite loading (embedded into final swf),

- player movements using arrows,

- player shoot with Z key (that create terrible "plasma" shot),

- basic collision detection (working with one line!) and basic response (plasma shot will be destroyed after hit an enemy),

- moving enemy (not so interesting, but helpful for newbie, I'll hope),

- very basic GUI,

So, after playing with it, what are judgment?

Very good, so easy to build a flash game with (see

[my last article](http://randomtower.blogspot.com/2010/01/flashpunk-seems-to-be-jung-good.html))

[FlashDevelop](http://www.flashdevelop.org/): it's so surprising that I've done source zip of my example. You can download and use freely, just see License.txt (I'll redistribute it with same license of Flashpunk)

Some hint about source code (I'll reefer to Flashpunk terminology, see my last post about it), all into it.randomtower.flashPunkHelloWorld package

- Main.as : load main "world" (or state) is HelloWorld,

- HelloWorld.as : load resources and embed them into final swf, add "actors" to "world", draw gui,

- Player.as : render player to screen, move it and let it shoot (creating new instances of Rocket.as),

- Enemy.as : render a static or moving enemy (moving = true by constructor)

- Explosion.as : render an explosion with using animation,

Some hint:

- disable Flashpunk splash logo changing in Main. as from:

public function Main()

{

super(400, 300, 60, 2, HelloWorld, false, true);

}

to

public function Main()

{

super(400, 300, 60, 2, HelloWorld, false, false);

}

- watch out for FP static class usage: it's interesting use of this utility class to access to all world-entities related stuff,

- into example's Actors code, you can see this line:

setCollisionType("test");

is a good choice to divide entities into group so for example colliding enemies doesn't explode or something like that,

- in Rocket.as see this code:

if (collide("enemy", x, y)) {

trace("collision");

FP.world.remove(this);

}

collision detection in one line! This is a good point to flashPunk: developer doesn't have to care of it so much. Sure, need of more testing with many, many entities, but is surely interesting, right?

This is all for now, here

![](../../assets/949c35dab153f515.png)


![](../../assets/949c35dab153f515.png)

you can find source code of this example, let me know if for you is interesting!

## No comments:

## Post a Comment