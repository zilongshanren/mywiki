---
title: 'Book: Learn Cocos2D 2'
url: http://www.learn-cocos2d.com/store/book-learn-cocos2d/
author: Bekki says
published: '2013-07-16'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

# Book: Learn Cocos2D 2

## Learn Cocos2D 2 (Third Edition)
Also explains TexturePacker, PhysicsEditor, Tiled, Glyph Designer, Particle Designer and other tools. Source code is compatible with Xcode 4.4, iOS 6 and Mountain Lion (Mac OS X 10.8). ## Download Source Code (3rd Edition):
|
|
## Second EditionRelease Date: November 9, 2011 Explains Cocos2D v1.0, introduces Cocos3D and Kobold2D. Also explains TexturePacker, PhysicsEditor, Tiled and other tools. Source code is compatible with Xcode 4 and iOS 5.
|
## First EditionRelease Date: December 2, 2010
|

### Full Description

Create compelling 2D games with **Learn cocos2d 2: Game Development with iOS**. This book shows you how to use the powerful new cocos2d, version 2 game engine to develop games for iPhone and iPad with tilemaps, virtual joypads, Game Center, and more. It teaches you:

- The process and best practices of mobile game development, including sprite batching, texture atlases, parallax scrolling, touch and accelerometer input.
- How to enhance your games using the Box2D and Chipmunk physics engines and other cocos2d-related tools and libraries.
- How to add UIKit views to cocos2d and how to add cocos2d to UIKit apps.
- The ins and outs of the Kobold2D development environment for cocos2d and its pre-configured libraries, including Lua.

Best of all, this book will have you making games right from the very start. It guides you step-by-step through the creation of sample games. These fun examples are modeled after popular App Store games and teach you key concepts of the new cocos2d 2 game engine and relevant tools like TexturePacker (texture atlas), PhysicsEditor (physics collision shapes), Particle Designer (particle effects), Glyph Designer (bitmap fonts), and others.

This book offers a rock-solid introduction to creating games made entirely with cocos2d and little or no iOS SDK and OpenGL code. It also details alternative implementations, identifies the best free and commercial tools for cocos2d game development, features coverage of the author’s improved cocos2d game engine (Kobold2D), and even helps you enhance your game’s marketability on the App Store.

#### Who this book is for

The book is aimed at beginning game developers looking for an easier and even more powerful way to create compelling 2D graphics using OpenGL and Objective-C. It is assumed that the reader will have some knowledge of object-oriented programming and the Apple and iPhone/iPad developer environment.

I’m still working with adding a cocos2d view to a UIKit project. If I take your sample app and add another VC to it, and push ViewController onto a nav controller stack, the second time I load your ViewController, the cocos2d view doesn’t work any more. I just comes up blank and doesn’t respond. Is there some cleanup/re-init or run command that I need to call the second time, since the runningScene is already assigned? I think it has to do with assigning the view for the director in this snippet:

for (UIView *v in [self.view subviews]) {

if ([v isKindOfClass:[CCGLView class]]) {

v.hidden = YES;

[[CCDirectorIOS sharedDirector] setView:v];

break;

}

}

The view probably gets deallocated and gets reset when the VC is popped, but I’m not sure what to do to handle that.

Thanks!

This is a really good book and I learned a lot from it, not only on cocos2d but also on game development in general!

Any plans for a fourth edition that contains maybe an introduction to cocod3d?

I believe in the 2nd edition I had half a chapter devoted to cocos3d. It’s been removed for the 3rd edition because at the time cocos3d was not compatible with cocos2d 2.x which was the focus of the book. Besides that cocos3d is a niche project used only by very few. You may have noticed how little tutorials you can find for it on the web. Pretty much everyone who wants to get serious with 3d development switches over to a purely 3D engine like Unity, UDK, SIO2. Mainly because the use of tools and having a proper asset pipeline is so much more important for 3D game development.

Hi. Maybe someone already pointed that out. Found an issue in sample code from the book (CH12): your way of invoking

CCPhysicsSprite* sprite = [CCPhysicsSprite spriteWithTexture:spriteTexture_ rect:tileRect];

sprite.position = pos;

gives me EXC_BAD_ACCESS with current version of Xcode (4.6) + Cocos2d + Box2D (latest). I think it’s because in the current version of CCPhysicsSprite setting position expects a b2Body to be already defined for the sprite.

Maybe I’ve mixed up stuff somewhere…

Hey whats up. A couple of months back I decided to buy a book of yours called Learn Cocoas2d game development with iOS5 but havent gotten around to reading it until now. Im just wonder since im getting around to it practically a year or 2 after the book was written, should I actually read this book or jump into the newer version of the book you wrote? I know this has manual memory management but im ok with that since by doing this book ill get a refresher again, but Im wondering in your opinion what do you think I should do. And also anothe question if you dont mind, I literally just read there is another framework built on top of cocoas2d which is kobaold2d I believe. Should I just scrap the whole learning cocoas2d path and walk down the kobold2d path? What advantages does that have over cocoas2d? also i dont know if i will get an email with a response to this message so if not can you email me the response, i might forget exactly what article i posted this on and well I would like to hear your response. Thanks

The Learn SpriteBuilder book is just around the corner which also covers cocos2d v3.3.

There is an error in the row below:

int newSize = [ [_sizeCheckers objectAtIndex: _curFile] contentLength ];

The error is as follows:

/Users/wangzhaolong/Kobold2D/Kobold2D-2.0.4/__Kobold2D__/libs/cocos2d-iphone-extensions/Extensions/FilesDownloader/FilesDownloader.m:264:23: Multiple methods named ‘contentLength’ found

I can not delete the error.Can you help me?

Sorry , but where can I find a download link for the book ??

I upgraded to Version 6.0.1 of Xcode between Chapter 4 and 5 and now there is an error in cocos2d-ios in CCAction.m

/Users/muskie/Code/Kobold2D/Kobold2D-2.1.0/__Kobold2D__/libs/cocos2d-iphone/cocos2d/CCAction.m:331:3: Multiple methods named ‘setPosition:’ found

Apparently in the newer versions of cocos2d they’ve fixed this. I’ll try redownloading Kobold2d.

Rolling back to Xcode 5.1.1 downloadable from Apple’s Developer website allowed me to run Kobold2d based projects again.

Hello Steffen,

I am following the steps in your book to covert cocos2d template project to support ARC. After done those step, I got 13 compiler errors, like “Apple Mach-O Linker Error _OBJC_CLASS_$_CCDirector referenced from:”. I am using XCode6.3, iOS SDK8.3 and cocos2d-iphone-classic-2.2.

Could you please suggest? Thank you in advance.

resolved it by myself after repeating those steps in 10 times. In XCode6.3, there is no option for ARC when adding target ‘cocos2d-library’. ARC is yes by default, so after creating the new target, go to build setting and select ARC to No(search ‘auto’). Then it works out.

I am going to build my first game right now!!

I have followed the book’s example project in chapter 7 to code the “ScrollingWithJoy03” project again by myself with XCode6.3, iOS SDK8.3. Now building succeed and running crash into multiple similar messages as “Sprites[29965:2031379] cocos2d: CCSpriteBatchNode: resizing textureAlas capacity from [237] to [317]”.

I don’t find solution yet via google, Has anyone ever faced the issue? Will appreciate if any advise.