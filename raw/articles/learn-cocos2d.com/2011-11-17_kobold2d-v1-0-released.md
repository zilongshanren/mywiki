---
title: Kobold2D v1.0 Released
url: http://www.learn-cocos2d.com/2011/11/kobold2d-v10-released/
author: João Lopes says
published: '2011-11-17'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Kobold2D v1.0 is now available from the [Kobold2D Download page](http://www.kobold2d.com/display/KKSITE/Kobold2D+Download)!

This is mainly a [maintenance release](http://www.kobold2d.com/display/KKDOC/Kobold2D+v1.0+Release+Notes), I found and fixed all the bugs that had been reported, including some nasty linker issues that occurred with a preference on Snow Leopard. Kobold2D is now thoroughly tested with Xcode 4.0.2, 4.1 and 4.2 under Snow Leopard and Xcode 4.2 under Lion.

Of course the latest updates of [cocos2d-iphone-extensions 0.2](http://www.cocos2d-iphone.org/archives/1641) and [cocos3d 0.6.3](http://brenwill.com/cocos3d-whats-new/) are also included.

And I can’t say it often enough: **Kobold2D supports ARC (automatic reference counting) out of the box!** There’s nothing you need to do! Just have Xcode 4.2 installed and start writing code without retain, release and autorelease ever again.

#### Forward Looking Statement

The motto for the next updates is still “Get Connected!”. I want to add more online features and update the KKGameKitHelper class with [remote config support provided by AppMynx](http://www.appmynx.com/). I will evaluate [ShareKit](http://getsharekit.com/) and hopefully be able to implement that with (if necessary) a reasonably simple interface for Cocos2D apps.

I also have a commercial product for iOS in development that will make sending data over the network a lot simpler. The basic idea being that if, for example, you want to synchronize a sprite’s position and rotation properties with all other devices, you simply write something like this:

[cc lang=”cpp”]

[KKConnect addSharedObject:self

identifier:@”Player1″

properties:@selector(position),

@selector(rotation),

nil];

[/cc]

It works with any properties (except id/pointers). Whenever one of the property values changes, its value is sent to all connected devices and assigned to the property of the local object with the corresponding “Player1” identifier. Dead simple. And coming soon.

#### Learn Cocos2D Game Development with iOS 5

[ It’s also no coincidence that the print and PDF versions of the ](http://www.learn-cocos2d.com/store/book-learn-cocos2d/)[Learn Cocos2D Game Development book (2nd Edition)](http://www.learn-cocos2d.com/store/book-learn-cocos2d/) are available since a few days.

The book uses Cocos2D v1.0.1, the chapters have been significantly improved, Chapter 3 is almost a complete rewrite. There are also two new chapters discussing integration of UIKit views in a Cocos2D app, as well as adding Cocos2D to an existing UIKit app. The other new chapter is about Kobold2D and introduces Lua and Cocos3D.

Readers keep asking me when the Kindle or iBooks versions of the new edition will be out. To be honest: I don’t know. But I’m confident that there will be a Kindle version and one for iBook eventually, and I expect these to be available soon. After all the first Edition is also available through these channels, and so are most (if not all) Apress books. Plus Xmas is coming, just like most companies book publishers are eager to get their best products out the door in time for Xmas.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

I lol’ed so hard when in your book you say “If you work with an artist, make sure SHE is aware of this issue.” haha, males can’t be artists from your point of view? 😛 I’m just kidding, but yeah, it’s wrong. Awesome book. Keep up the great job, i’ll be close at this blog.

I wrote that?![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


I suppose it was made gender-friendly (or whatever the term is for that) either by myself or by the editor. You can write he/she alternating, stick to either he or she, use (s)he, or prefer “she” simply because the “he” may be seen as more sexist because we’re living in a male dominated world. I certainly wasn’t trying to say that artists are all female.