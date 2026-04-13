---
title: 'cocos2d Book, Chapter 8: Shoot ’em Up'
url: http://www.learn-cocos2d.com/2010/08/cocos2d-book-chapter-8-shoot-em/
author: Codingmyassoff Says
published: '2010-08-14'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

### Chapter 8 - Shoot ’em Up

This chapter will finish the shoot ’em up game. There will be enemies and powerups. It raises the issue of good code design when certain things like shooting and moving are common to all objects while other things such as what to shoot and where from and to depend on who is shooting. And then to determine who is hit by whose bullets.

Of course no shoot ’em up game is complete with a boss monster that takes a couple hits to kill. So it’ll need a healthbar. At the end of the chapter this shoot’ em up should be a fully playable game, with Chapter 9 complementing it with visual effects by using the cocos2d particle system. But I’m getting ahead of myself here.

### Summary of working on Chapter 7 - Scrolling With Joy

Once again I renamed the chapter a bit since it’s divided into two parts: a parallax, infinitely scrolling background and input via SneakyInput, featuring a fire button and an analog thumbstick respectively at the end changed to a 8-way digital pad.

The parallax scrolling background consists of several bands or stripes which were created on different layers each in ![2010-08-14_11.57.58](../../../wordpress/wp-content/uploads/2010-08-14_11.57.58-300x156.png)


[Seashore](http://seashore.sourceforge.net/)and then saved as individual 480×320 images. They were then added to the Texture Atlas by

[Zwoptex](http://zwoptexapp.com/). The cool thing about this is that Zwoptex preserves the original image’s size while stripping away all transparent parts. So the images take up little space in the Texture Atlas but in game you don’t have to position them individually, you’ll simply place them at the center of the screen.

To achieve the endless scrolling effect two of each image where added side-by-side to each other, with one flipped on the X axis so the images align neatly. Whenever one image has scrolled outside the screen it is moved back to the right side of the screen. At the end I also fixed the vertical flicker lines which can appear due to round-off errors when moving the sprites. And of course they all are drawn with a CCSpriteBatchNode.

The SneakyInput fire button allows continuous shooting and faster shooting when you just tap it, while the thumb stick controls the ship’s movement in both analog and digital (8-way) variants. The Ship class’ setPosition method is overridden to keep the player’s ship within screen boundaries at all times. Finally an extension class gives SneakyInput the same autorelease initializers used by cocos2d, and adds another good example of just how useful Objective-C categories can be.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

[apress](http://www.learn-cocos2d.com/tag/apress/)•

[book](http://www.learn-cocos2d.com/tag/book/)•

[CCSpriteBatchNode](http://www.learn-cocos2d.com/tag/ccspritebatchnode/)•

[Chapter](http://www.learn-cocos2d.com/tag/chapter/)•

[cocos2d](http://www.learn-cocos2d.com/tag/cocos2d/)•

[digital pad](http://www.learn-cocos2d.com/tag/digital-pad/)•

[enemies](http://www.learn-cocos2d.com/tag/enemies/)•

[fire button](http://www.learn-cocos2d.com/tag/fire-button/)•

[flicker](http://www.learn-cocos2d.com/tag/flicker/)•

[healthbar](http://www.learn-cocos2d.com/tag/healthbar/)•

[monster](http://www.learn-cocos2d.com/tag/monster/)•

[movement](http://www.learn-cocos2d.com/tag/movement/)•

[Objective-C](http://www.learn-cocos2d.com/tag/objective-c/)•

[Parallax](http://www.learn-cocos2d.com/tag/parallax/)•

[playable game](http://www.learn-cocos2d.com/tag/playable-game/)•

[Scrolling](http://www.learn-cocos2d.com/tag/scrolling/)•

[shooting](http://www.learn-cocos2d.com/tag/shooting/)•

[SneakyInput](http://www.learn-cocos2d.com/tag/sneakyinput/)•

[thumbstick](http://www.learn-cocos2d.com/tag/thumbstick/)•

[visual effects](http://www.learn-cocos2d.com/tag/visual-effects/)•

[Zwoptex](http://www.learn-cocos2d.com/tag/zwoptex/)

Hi,

when can we expect new chapters to appear on apress website?

I went trough first 5 chapters rather quickly, itching to get more! 😀

I’m in the same situation. I enjoyed reading the first five chapters of the book, but I think I moved too fast. When do new episodes available?. The last seems very very interesting.

On the other hand, in the book, sometimes, you talk about source code, where we can download if it is available?

The first 5 chapters were made available as I submitted them, so they are the rough drafts. New chapters will be made available after they have been review edited by Apress. It could be another 2-4 weeks, it could be in a couple days, I really don’t know at this point.

Please check in the new chapters.

Bought the book and there are still only the first five chapters ready for download.

I found a working Promo key![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


50% off

Promo key for the book you mean? How did you “find” that?

Hi love the book, love the source code examples. I use everything I learned in my projects.

Question for you. Although the example of the Shootemup in Chapter8 is for standard iPhone size I want it to run in Retina mode.

It does not work when I do that. However I think the problem is my setting in Sneakybutton.m and Inputlayer.m

Here is what I have in Sneakybutton.m

bounds = CGRectMake(0, 0, 480, 320);

center = CGPointMake(428,32);

And her is what I have in InputLayer.m

FireButton.position = CGPointMake(432,28);

FireButton.anchorPoint = CGPointMake(0.5f,0.5f);

Any Ideas of where I going wrong?

Thanks in advance!

Points should be the same in Retina, Retina devices have a size in points of 480×320 as well. Make sure that you provide -hd versions of all images.

What does “does not work” mean?