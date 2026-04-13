---
title: 'cocos2d Book, Chapter 5: Getting bigger and better'
url: http://www.learn-cocos2d.com/2010/07/cocos2d-book-chapter-5-bigger/
author: Fernando T says
published: '2010-07-23'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

### Chapter 5 - Getting bigger and better

The gist of this chapter will be to discuss the simple game project from the previous chapter. I threw everything into one class, clearly not what you want to do for bigger games. But getting from one-class to real code design is a big step which some hesitate to take. I’ll make that easier and discuss common issues and their solutions, such as what to seperate, what to subclass from and how you can have all the seperated objects communicate with each other and exchange information in various ways.

A big topic will of course be how to take advantage of cocos2d’s scene hierarchy and which pitfalls it may have when moving from a single-layer game to one which has multiple layers and even multiple scenes.

As for the chapter title I’m not so sure if that’ll be it. Maybe along the way while I’m writing I’ll change it. Suggestions welcome!

The chapter will be submitted on Friday, July 30th.

### What’s your take on good cocos2d code structure?

Did you ever struggle with cocos2d design concepts? Or the cocos2d scene hierarchy? Or how to layout a scene and divide your game into logical parts? Tell me about it.

I know theses questions are somewhat generic to ask. It’s about the things that don’t feel right but there doesn’t seem to be a better, more obvious way. I think we all know some of those, if you do, be sure to tell me! Leave a comment or write me an email.

### Summary of working on Chapter 4 - First simple game

![doodledrop](../../../wordpress/wp-content/uploads/doodledrop.png)

*Doodle Drop* and features dropping spiders and an accelerometer controlled alien trying to avoid the spiders. All in all it got divided into 8 concrete steps. Lots and lots of code comments, too.

It starts simple enough, adding resources to Xcode and adding sprites. It gets more gameplay-esque when the accelerometer-driven player controls got tweaked to provide acceleration and deceleration of the player object. In contrast, the spiders movements are driven only by actions.

I introduce you to two undocumented features of cocos2d, namely CCArray which is since v0.99.4 used to store all children of a node. The other are the CGPointExtension class which has all the functions normally provided by a physics engine, however not every game should link a physics engine just because one needs those math functions. That’s why CGPointExtension comes in handy.

With the ccpDistance method the collision checks are done. Simple radial collisions, and in debug mode the collision radii are drawn too.

In between the CCLabel for the score got replaced with a CCBitmapFontAtlas, because it killed the framerate. I shortly mentioned Hiero and how to use it in principle but for all the details there was no room. But while I was at it I created the [Hiero Tutorial](http://www.learn-cocos2d.com/).

At the end of the project I added some polish which isn’t described in the book (too many details) but really adds to the game’s look and feel. The spiders drop, hang in there, then charge before dropping down, all done using actions. I’ve also added the thread they’re hanging from using ccDrawLine. And then there’s a game over label which shows even more action use.

One of the principles I followed is to stay away from fixed coordinates as much as possible. So the project, once finished, did run just fine on an iPad. Although the experience is a different one, there’s more spiders dropping and they drop faster but there’s also more safe space to maneuver to.

Oh and, the game art is all mine. Yes, I know … but Man-Spiders **do** have just six legs! ![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Is the xcodeproj of Doodle Drop available for download ? If so, where do get it ?

This book will be great, tnk y. from Brazil !

Yes, the book’s source code is available here:

http://apress.com/book/downloadfile/4627

[…] Hmmm … somehow this game seems strangely familiar. […]

I love your first edition, learned lots of things from that book. I’m eager to waiting for the second edition.

Also I like to know, some basic math related book those are helpful for game development.

Best Wishes