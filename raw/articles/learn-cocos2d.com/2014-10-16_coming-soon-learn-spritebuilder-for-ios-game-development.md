---
title: 'Coming soon: Learn SpriteBuilder for iOS Game Development'
url: http://www.learn-cocos2d.com/2014/10/coming-learn-spritebuilder-ios-game-development/
author: Narinder Bansal says
published: '2014-10-16'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

I’m done writing the *Tome of SpriteBuilder*.

There’s only edits and reviews left, page proofing and then it goes out to print. Meanwhile, I’m cleaning up and extending the *Bouncy Beast* project for its App Store release.

Time to share some insights as I haven’t been able to slice some time off to write about the process as I originally intended to.

### What’s in the book?

In the [Learn SpriteBuilder book](http://www.apress.com/9781484202630) you will learn [SpriteBuilder](http://www.spritebuilder.com/) step-by-step while building the Bouncy Beast game.

The book will guide you through the creation of a physics-driven, parallax-scrolling game with the help of SpriteBuilder, Cocos2D (cocos2d-swift) and Objective-C. The level-based structure will enable you to add more content to the game, even without writing additional code.

As your guide I will walk you through the individual steps necessary to create the game project. Along the way I’ll explain the SpriteBuilder features, caveats, workarounds and helpful tips and tricks as you are most likely to come across or need them.

At the end you’ll have a complete game reminiscent of games like Badland.![978-1-4842-0263-0_Figure_13-16](../../../wordpress/wp-content/uploads/978-1-4842-0263-0_Figure_13-16-300x133.jpg)


The game also runs on Android devices thanks to

[Apportable’s Android plugin for SpriteBuilder](http://android.spritebuilder.com/).

The Bouncy Beast project’s source code will be available.

### Bouncy Beast Demo Video

Here’s a video demonstrating the game. Notice the subtle particle effect on the main menu’s background, the paginating scroll view, the soft-body player character.

**NOTE**: the suboptimal framerate in the video is 100% attributable to the iOS Simulator from which I recorded the video. On an iPod touch 5G the game runs with a constant 60 fps.


### Not Swift

Because I expect this question: no, Swift does not play a role in this book. All code is Objective-C only.

When I started writing this book, Swift wasn’t even known. It took some more time for Cocos2D to support Swift and SpriteBuilder will get the ability to create Swift projects starting with v1.3.

Nevertheless, most of the things you’ll learn about SpriteBuilder directly apply to Swift projects, too. Only the code needs porting.

### Target Audience

Beginning and experienced game developers who want an introduction to and learn to make games with SpriteBuilder.

### Program Versions

The book was built and tested with SpriteBuilder v1.3 and cocos2d-swift v3.3 (both currently in beta) as well as Xcode 5.1 and 6.0. That means by the time the book is available it will cover the most up-to-date versions of SpriteBuilder and Cocos2D.

I’ve taken care to avoid anything obviously version-specific or prone to change. The book’s contents should still be applicable a year from now. In any case there will be errata in case a new version of either SpriteBuilder, Cocos2D or Xcode may introduce any incompatibilities with the book.

### Table of Contents

Following is a list of chapters in this book with short summaries.

- Chapter 1 - Introduction
- Chapter 2 - Laying the Groundwork
- Chapter 3 - Controlling and Scrolling
- Chapter 4 - Physics and Collisions
- Chapter 5 - Timelines and Triggers
- Chapter 6 - Menus and Popovers
- Chapter 7 - MainScene and GameState
- Chapter 8 - Selecting and Unlocking Levels
- Chapter 9 - Physics Joints
- Chapter 10 - Soft-Body Physics
- Chapter 11 - Audio and Labels
- Chapter 12 - Visual Effects and Animations
- Chapter 13 - Porting to Android
- Chapter 14 - Debugging and Best Practices



An introduction to SpriteBuilder and its user interface. The most commonly needed tasks are explained here. Also contains a quick introduction to programming with Cocos2D. You end up with a project that allows you to transition between scenes by the press of a button.


You’ll add touch input and parallax scrolling of multiple background layers in this chapter. You’ll learn to use sprite sheets and prefabs. A player prefab is introduced, its simplistic movement is performed by move actions.


You learn how to add physics to a game, specifically immovable, impenetrable walls as well as dynamic bodies. Player movement is replaced by actual physics. Collision callback methods are used to trigger the level exit. How to enable physics debug drawing is also explained.


Timelines are explained in depth, then used to animate rotating physics objects. You’ll learn how to create trigger areas that run code when the player enters them. The resulting project now makes simple physics interactions possible.


A powerful, yet easy way to create popover menus such as the pause and game over menus is explained. The same concept can be used to create fullscreen menus without interrupting the running scene. The menus are animated with the Timeline, using Timeline delegate methods to receive notifications when a Timeline has ended.


The main menu is designed with an animated background and a settings menu with audio volume sliders. A GameState class is introduced which stores global, user-specific game data via NSUserDefaults.


A level selection screen is added with the help of the Scroll View node. How CCScrollView works and how it can be programmed and how you can respond to its delegate methods is carefully explained. The level selection pages are divided into multiple worlds, with each level unlocked by completing the previous level.


An entire chapter dedicated to creating physics objects out of joints, specifically chains, ropes and springs. How joints work and what you can and probably shouldn’t do with them is explained in detail.


The player prefab is replaced by a soft-body player. A soft body object is a deformable physics object held together by joints, its collision shape divided into multiple smaller bodies. This chapter also introduces custom rendering with Cocos2D as the player’s texture needs to be drawn to match its deformed shape at any time.


You’ll learn how to play short sound effects with the Timeline and programmatically with ObjectAL, and background music. The other half of the chapter deals with Label TTF properties like shadows and outline but also explains how to create, import and use bitmap fonts in SpriteBuilder.


You’ll be creating a sprite frame animation for the first time, and make it work with the player’s custom rendering class. An introduction to Particle Effect nodes is mandatory in a chapter on visual effects. This culminates in the use of the Effect Node, which are essentially shader programs that you can add and design in SpriteBuilder. At the end of this chapter you’ll hardly recognize the main menu scene.


At first you’ll see what is necessary to develop for Android. Then you’ll create a new project with which you’ll test deployment to an Android device. Finally you’ll convert the Bouncy Beast project and fix any compilation, launch and layout issues that occur. You’ll get advice on how to best approach cross-platform development with SpriteBuilder.


This chapter is an introduction to debugging with Xcode and Cocos2D. You’ll learn about techniques to catch or prevent programming bugs. Basically a self-help guide that’ll quickly proof invaluable. There’s also a section on Troubleshooting some of the most common SpriteBuilder and Cocos2D issues.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Hi Steffen

We have game built in cocosbuilder around 2 years back. As you are aware cocosbuilder is no more in active development. Can you please guide us in porting cocosbuilder game to Spritebuilder.

Thanks

Narinder

When will it be available for pre-order?

It’s already available as Alpha Book here: http://www.apress.com/9781484202630

If you buy the alpha book you get a selection of chapters right now, and once the book becomes available you automatically get access to the full eBook version.

Preordering the print version is also possible via the above link, or Ama.. ahem, your local book dealership. 😉

Looks awesome, can’t wait for this book to be out, please email me when it comes out, this has exactly what I need, I just started a physics game with spritebuilder![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


I am allocating few CCScene subclasses But When I am doing this it almost takes more then 10 secs SO What i want to achieve is I want to perform a small CCAnimation like loading logo glowing, so my question is how to load those CCScene subclasses in background and do perform this animation

Please answer asap

I am able to perform these things separately but I want to do these together

[…] Read this if you want to learn more about Learn SpriteBuilder, and try SpriteBuilder in the App Store. […]

Any pre-order ??

I can’t wait to have that book

It’s already available as Alpha Book here: http://www.apress.com/9781484202630

If you buy the alpha book you get a selection of chapters right now, and once the book becomes available you automatically get access to the full eBook version.

Preordering the print version is also possible via the above link, or Ama.. ahem, your local book dealership. 😉

Steffen, I’ve got the alpha book and am going through it. However, I can’t seem to find the assets, which of course, makes things quite a bit more difficult. Do you have a link or could you contact me at the given email address? I realize it’s getting close to publication but I really don’t want to put it down until then.

Thanks!

Gerald

It’s possible that the files will be made available only after the book is published. It’s a pretty large download.

Amazon.com says the book will be published November 21st 2014 (Paperback) while Amazon.de says March 14th 2015. APress says Publishing November 24, What’s the right date?

I would trust Apress. 😉

Book goes to print today. It’ll take a few days to distribute but certainly not until March.

Hi Steffen!

I want to ask this question. Why write about Cocos2D-Swift while using Objective-C? Why not write a lesson that only on pure Swift? You mislead people do not you think? But if you write a lesson using Objective-C is better then not to mention about Swift. I think it would be fair to those who are looking for information on how develop games with Cocos2D but only using Swift syntax.

Well, I explain this in the book. By the time I started writing, Swift wasn’t even announced yet.

Cocos2D itself needed to be updated to become compatible with Swift, and specifically for SpriteBuilder Swift support took a few months (after the initial announcement ie during beta phase). Plus there were (and still are) quite a number of issues associated with Swift, as can be expected from a brand-new programming language. Specifically performance during the beta wasn’t too good.

The fact that cocos2d-iphone is now called Cocos2D-Swift mainly is aimed at expressing that Cocos2D works with Swift in addition to Objective-C. Using Swift with Cocos2D by no means exclusive.

Thanks for the reply! Depressing the fact that the name “Cocos2D-Swift”| mislead people! Usually people are looking for the following items about “cocos2d, swift” and find only the name “Cocos2D-Swift”, but there is no benefit from it. At least, try to find a normal lesson using Swift syntax with Cocos2D. Even API Reference Documentation contains only Objective-C. I think this is nothing more than a disinformation.

Hi Steffen,

Does the book come with source code? Why I’m asking this is because the Apress site for the book doesn’t include a link to the source code. Do I get the source code after I buy the book or what? I intend to get the ebook version next week and will be nice to have the source code alongside while I learn spritebuilder. Thanks.

The source code will be available shortly (this week hopefully) on the Apress website.

>>>> Cocos2D itself needed to be updated to become compatible with Swift

The more I see no reason to rename to “Cocos2D-Swift”.

>>>> and specifically for SpriteBuilder Swift support took a few months

No sense of support if still have not updated the API Documentation for Swift and do not have a single lesson or even be something like “Getting started”.

Once again I repeat - all these marketing rename only mislead people. People are looking for one thing and find something else entirely. In the absence of normal support, documentation and lessons is too early to put the word “Swift”.

Hi there, Do you know where I can download the resources? Bought the book just now and wanted to start learning but i can’t find the resources/assets

The download will become available shortly (over the weekend) on this page: http://www.apress.com/9781484202630

Where I can’t Download the assets??

I have the book ,, but I can’t found the archive, so I can follow

and where your email? so i can contact you if I stack??

waiting your reply

The download will become available shortly (over the weekend) on this page: http://www.apress.com/9781484202630

If you get stuck please post it on http://forum.spritebuilder.com or http://stackoverflow.com so others can search for and benefit from solutions.

Hi Steffen,

I am following the instructions but I got stuck on this (page 50):

-(void) touchBegan:(UITouch *)touch withEvent:(UIEvent *)event

{

_playerNode.position = [touch locationInNode:self];

}

The error i receive is: No visible @interface for ‘UITouch’ declares the selector locationInNode. Any idea on what I did wrong?

Very recently the signature of the touch methods was changed to use CCTouch and CCTouchEvent. Try using it with the new parameters, hopefully this fixes it: