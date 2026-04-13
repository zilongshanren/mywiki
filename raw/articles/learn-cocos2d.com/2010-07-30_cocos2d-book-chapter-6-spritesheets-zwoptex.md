---
title: 'cocos2d Book, Chapter 6: Spritesheets & Zwoptex'
url: http://www.learn-cocos2d.com/2010/07/cocos2d-book-chapter-6-spritesheets-zwoptex/
author: Rcbowser Says
published: '2010-07-30'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

### Chapter 6 - Spritesheets and Zwoptex

In this chapter the focus will be on Spritesheets (Texture Atlas), what they are and when, where and why to use them. Of course a chapter about Spritesheets wouldn’t be complete without introducing the Zwoptex tool. The graphics added in this chapter will then be used for the game created in the following chapter.

The chapter will be submitted on Friday, August 6th.

### Anything about Spritesheets you always wanted to know?

Just let me know. I’ll be researching what kind of issues people were and are having regarding Spritesheets. I want to make sure that they are all covered in the book.

Please leave a comment or write me an email.

### Summary of working on Chapter 5 - Game Building Blocks

I finally found a better title for the chapter. A big part is about working with Scenes and Layers. A LoadingScene class is implemented to avoid the memory overlap when transitioning between two scenes. Layers are used to modify the game objects seperately from the static UI. I explain how to use targeted touch handlers to handle touch input for each individual layer, either swallowing touches or not.![2010-07-30_12.07.04](../../../wordpress/wp-content/uploads/2010-07-30_12.07.04-150x150.png)


The issue of whether to subclass CCSprite or not is discussed and an example is given how to create game objects using composition and without subclassing from CCNode and how that changes touch input and scheduling.

At the end the remaining specialized CCNode classes such as CCProgressTimer, CCParallaxNode and the CCRibbon class with the CCMotionStreak are given a treatment.

![figure5-4](../../../wordpress/wp-content/uploads/figure5-4-150x150.png)


As you can see from the pictures, I’m also making good progress at becoming a great pixel artist. Only I have a looooooong way ahead of me still. But I admit, the little I know about art and how much less I’ve practiced it, I’m pretty happy about the results and having fun with it. The cool aspect of it is that this should be instructive art. It doesn’t have to be good. So I just go ahead and do it and tend to be positively surprised by the results. I’ll probably touch this subject in the next chapter about Spritesheets: doing your own art. It’s better than nothing, it’s still creative work even if it may be ugly to others, and it’s a lot more satisfying to do everything yourself, even if it takes a bit longer and doesn’t look as good. At least it’s all yours, you’re having fun, and learn something along the way. And you can always find an artist sometime later who will just draw over your existing images or who replaces your fart sound effects with something more appropriate.

Btw, if you’re looking for a decent and free image editing program for the Mac, I’ve been using [Seashore](http://seashore.sourceforge.net/) for about a year now and I’m pretty happy with it.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Hey Steffen have you checked out this nice little freeware program?

It’s called Pencil and I think it might have a lot of potential for game development.

http://pencil-animation.org/

Keep those chapters coming! I’m saving all my pretty little pennies up so I can get a copy. :o)

Thanks,

RON

Thanks!

I checked out pencil. For comic drawings it seems to be interesting, not so much for pixel art though. But I’ll spend some time with it and see if i can animate something with it.

Pixen is another cool program to use for pixel art. One of the features it has is ‘Tile View’ which shows a repeat of your artwork as you’re working on it, making seamless tiles a cinch!

http://opensword.org/pixen/

Thanks for the tip! As it so happens I stumbled across Pixen today, downloaded it and found out I had already downloaded it. Tried it, really nice, I just wish I could somehow overlap anim frames to see better what changes I’m making to the underlying previous frame.

Yeah, it’s not perfect for everything but the only graphics program I know of so far that has the view for repeating tiles. Seems like that would fill a great need if one of the other graphics programs could add that since it seems like Pixen isn’t really supported that much either.

Nothing to do with spritesheets but Multiplayer integration over local wifi or bluetooth would be a nice add to your book. A lot of peolpe are asking about it on many forums including cocos2d.

Endless scrolling backgrounds for flying or racing sidescroller and other scroller games where you play the game in “birds view” would be nice.

David

For Multiplayer there are so many approaches and none specific to cocos2d. But Chapter 7 explains how to do an endless scrolling parallax background with all the tricks.

I don’t know if you address this in this chapter yet, but here is something I have been battling with, the difference between a spritesheet and a texture. I feel that there are so many ways to get an image up onto the screen and I am trying to find the best approach. I feel that using a spritesheet loaded with a texture that has been loaded might be the best, but who knows. Maybe you can shed some light on this area.

Also, possibly including optimal times to load textures…possibly a loading screen implementation?

You do some great work and I enjoy all the tutorials / help you give, thanks!

I believe the difference between textures, sprites and spritesheets (now called sprite batches) will become clearer by reading the book. In short, the spritesheet (or sprite batch) is merely a container for sprites with the requirement that all sprites added to it use the same texture (otherwise you get an error). The texture used by a spritesheet/sprite batch can be a single 16×16 pixels textures for a bullet because you use a lot of bullet sprites, but it’s more effective to use a larger texture atlas texture (eg 1024×1024 pixels) so you can render many different looking sprites using the same spritesheet (sprite batch). This speeds up rendering of sprites in the spritesheet by cutting down the number of draw calls.

A loading screen implementation is also discussed in the book. By using that you can avoid the memory spike when transitioning from one scene to another. If you do it directly, both scenes are in memory at the same time during the transition phase, which can cause memory warnings if the scenes are complex. By using the loading scene in between the old scene’s memory will be freed before the new one is loaded.

Not sure if this is the correct place, but I was hoping somebody could help be with a CCRibbon / CCMotionStreak issue / barrier.

Basically, I am using the above to simulate contrails. So (to keep it simple) I have a MapLayer layer on which I have a CCSprite as child (for an aircraft). I have been experimenting with CCRibbon and CCMotionStreak to add the contrail effect.

The thing is, I have a joystick object to pan the MapLayer up/down/left/right and, while the sprite accompanies the movement faithfully (through some conversion from another UILayer), both CCRibbon and CCMotionStreak go haywire.

The funny thing is CCRibbon works if I merely draw a ribbon (updating it in the TouchesMoved method), i.e. whatever ribbon I have drawn is moved around faithfully by the joystick. However, when I address the CCRibbon / CCMotionStreak from within the Update method, well then things go south. The critical difference seems to be whether I add points from Update in CCLayer or whether I add points from the Update method.

CCMotionStreak goes haywire either way, but I suspect the reason is that, since the Ribbon is not a child of MotionStreal (but an instance object), then the rules behind the Node hierarchy do not apply.

Any comments, pointers, will be greatly appreciated. Meanwhile I’ll continue to work on it. If I resolve anything I’ll post. My next steps is to manually update the position of the CCRibbon within the CCMotionStreak, but it’ll feel dirty if it works![:-)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


Thanks

*sigh* A few minutes later and I have some idea of what the issue *may* be. It may be a bug in the way that CCMotionStreak is anchored in combination with some scheduling concerns. I am including a link of the discussion which itself leads to a bug reported.

http://www.cocos2d-iphone.org/forum/topic/12251

Guess I may have to workaround it in the meantime. If anyone understands this better than I do, an explanation could be useful.

Thanks for this great book! You really made finding the way into cocos2d much more easy and I’m not growing tired of recommending it to everyone who wants to make games on the iPhone (and I know a lot of those guys!).

I have a problem in my own game based on a design choice that I got from your chapter 6. In my own GameScene I use a static accessor to the CCLayer (and also in other places in my code to certain data which I want to have a quick access to without parsing through all child nodes).

Now I am at the point of changing the level by using “replaceScene”. Since the new scene gets created before the old one becomes deallocated, my static variables are pummeled beyond recognition. They get the new values from the new scenes and afterwards are set to “nil” because of the deallocation of my old scene. The new scene is a mess.

Since I do not use large binaries the initialization of my levels is very fast and I do not need an intermediate LoadingScene (which by the way does not help either - the Loading Scene switches so fast to the initialization to the new Level that I still have the same problem. I don’t want to implement an unnecessary waiting mechanic into the Loading Scene and I would not know how long I have to wait since I don’t know when the old Level is completely cleaned up).

Bottom line: Do you have any tips how to work with static members in my nodes since I do not see how this can work at all with level transition? Or is the secret to avoid static members at all?

One solution is to store a reference to the current layer in the nodes that need to access the layer. You should not retain that reference, otherwise you could easily leak the whole scene/layer.

Alternatively, and probably easier, is to not go directly from scene A to B but add a “loading” scene in between. This way, the first scene gets properly deallocated before the next scene gets allocated, and accessing the singleton-layer will work again because the order of alloc/dealloc is preserved. Also, you avoid the memory peak with two scenes being in memory at the same time.

Hi,

Like you are describing in chapter 5 p107-111, I am using composition to display a CCSprite. The code is similar to your example with the Spider object. But what I am also doing is referencing this object (Player instead of Spider) from the Scene (in the example, you do not hold a reference).

I think this is what might be causing a crash when (in certain circumstances) i call replace scene. I say I think, because I am new to memory management, but when I comment out the player object, the scenes can be replaced with no problems. Of course there could be other reasons…

So my question, is it OK to keep a reference to the object? I am assuming so, since it is auto-released. But that damn SIGABRT just won’t go away…

Yes, that is a problem. Consider this: your scene already holds a reference to the Player through the node hierarchy (the children of a node). Now if you have the scene hold on to one of its children, then either cocos2d will clean up the node hierarchy and your player pointer becomes invalid. If you retained the player reference in the scene, the scene may not be released at all. Either way, that’s not good.

Your scene should not need to hold a reference to the player. Instead, whatever code needs the player should be in the Player class, which can get access to the scene via a Singleton pattern (Scene sharedScene).