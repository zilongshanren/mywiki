---
title: Learn & Master Cocos2D Game Development
url: http://www.learn-cocos2d.com/blog/
published: '2015-09-10'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

In case you haven’t heard of my latest project, please check it out: ![Screen Shot 2015-05-01 at 12.26.32](../wordpress/wp-content/uploads/Screen-Shot-2015-05-01-at-12.26.32-300x288.png)


[TilemapKit](http://tilemapkit.com/).

TilemapKit is now [available for sale](https://tilemapkit.com/store) and works with both Cocos2D-ObjC and Cocos2D-SpriteBuilder.

## What is TilemapKit?

In a nutshell, it’s a complete implementation of Tiled’s TMX format and all of Tiled’s features with a super-fast, multithreaded renderer and advanced features such as creating grid graphs for pathfinding, support for normal-mapped lighting of tilemaps, all necessary coordinate conversion methods and then some.

TilemapKit is free of artifacts, you can use multiple tilesets per tile layer, it plays tile animations, and can assign Tiled properties to any object via KVC.

There’s so much more to it, you should simply visit the [features page](http://tilemapkit.com/tilemapkit-features/) from where you can also download the TilemapKit Trial.

Please post your questions and feedback on the [TilemapKit forum](http://forum.tilemapkit.com/) and [browse the roadmap](http://tilemapkit.idea.informer.com/), perhaps you’ll want to vote on one of the items or add your own.

Imagine you downloaded a racing game and launch it. This is the first thing you see:

![Car Ad](../../assets/316a9dbc818e0e23.png)


You think: “Cool, that’s a really nice car! Graphics look even better than on the App Store screenshots. Okay, of course I want to ‘Race Now!'”

Worst case scenario: you are gone, happily playing that new (and arguably better) racing game. The Indie dev gets his *fair* share of the deal: $0.10.

### This rant needs more detail …

Cocos2D “for iPhone” (as in: Objective-C) now has two forks:

[Cocos2D-ObjC](https://github.com/cocos2d/cocos2d-objc)maintained by Lars Birkemose. This fork builds on v3.4 with a focus on making Cocos2D easier to use for beginners. Its website is[cocos2d-objc.org](http://cocos2d-objc.org/).[Cocos2D-SpriteBuilder](https://github.com/spritebuilder/cocos2d-spritebuilder)maintained by Scott Lembcke and others. This fork is currently at v3.4 also but will soon have a v4 release. Its website is[spritebuilder.com](http://www.spritebuilder.com/).

### How did this happen?

[Scott’s thread](http://forum.spritebuilder.com/t/the-future-of-cocos2d-spritebuilder/) explains it to some degree. There’s more info on the [-ObjC thread](http://forum.cocos2d-objc.org/t/the-new-objc-site/). And the [-ObjC mini roadmap](http://forum.cocos2d-objc.org/t/the-cocos2d-objc-mini-roadmap/17316) provides some more insight.

**Long story short:** Lars and Scott disagree on the direction of Cocos2D. Lars continues with the version 3.4 of Cocos2D before any work on v4 has started. Naturally Cocos2D-SpriteBuilder will soon **be** the previously announced v4.

This happened shortly after Apportable stopped sponsoring the development of new Cocos2D/SpriteBuilder features. For Lars, Cocos2D was becoming this big chunk of support code for SpriteBuilder, and he’s now trying to turn the ship around.

### Double-fork all the way - what does it mean?

I thought I’ll give you a demo of the upcoming CCLightNode visual effect that will be available in Cocos2D-Swift v3.4, which comes bundled with the upcoming SpriteBuilder v1.4 (available on the [Mac App Store](https://itunes.apple.com/app/spritebuilder/id784912885) soon, [v1.4 beta is available for download](http://spritebuilder.com/beta)).

### Introducing CCEffect

You may have already heard about the [other shader effects first introduced with Cocos2D-Swift v3.2](http://www.spritebuilder.com/blog/crystals). Below is the Crystals example app, in particular it demonstrates the glass (reflection/refraction) effects:

Pretty neat stuff. More effects have been added in Cocos2D-Swift v3.3. Now with v3.4 around the corner, the CCLightNode and accompanying effects will shine their highly configurable lights on upcoming apps.

### Introducing Lighting via CCLightNode

For the most part, the demo was put together entirely in SpriteBuilder:

It only took a little bit of code to add a light node that you can drag around when touching the screen. I chose to use Swift for this example, if only to highlight that yes, you can use use 100% Swift to make your SpriteBuilder + Cocos2D apps if you wish.

[
Continue reading »
](http://www.learn-cocos2d.com/2015/01/light-demo-cclightnode-cocos2dswift-v34/#more-7376)

A little known secret (apparently) is that [Cocos2D and SpriteBuilder have an actual developer guide](https://www.makeschool.com/docs) that covers a lot of basics and advanced stuff alike.

The only problem with it is that it’s not well-known, hence this post. I’m hoping to bump it in the Google search results by posting and tweeting it, so if you could do the same that would be really appreciated!

Here’s the link to the SpriteBuilder & Cocos2D Developer Guide:

[https://www.makeschool.com/docs](https://www.makeschool.com/docs)

### Cocos2D Swift Examples

Also, let it be known that the developer guide has Cocos2D example code in both Swift and Objective-C.

[ Quick notice: only 10 more days to go!](http://www.apress.com/9781484202630)

Learn SpriteBuilder has a release date set to Nov 24th.

I suppose the eBook version will by available by that date and you can also get many chapters in the alpha program right now.

The print edition may need a few more days to distribute depending on where you live or from where you order.

[Read this](http://www.learn-cocos2d.com/2014/10/coming-learn-spritebuilder-ios-game-development/) if you want to learn more about Learn SpriteBuilder, and [try SpriteBuilder in the App Store](https://itunes.apple.com/app/spritebuilder/id784912885).

Enjoy it! ![:)](../wordpress/wp-includes/images/smilies/simple-smile.png)


This guide goes through the telltale signs of terrible questions asked on stackoverflow. You’ll learn **how not to ask questions**.

If instead you like to learn [how to ask good questions](http://stackoverflow.com/help/how-to-ask) you came to the wrong guide. You may also want to learn to tell people [what the Matt you’ve tried](http://mattgemmell.com/what-have-you-tried/) so far. Jon Skeet has an

[excellent checklist for the perfect question](http://codeblog.jonskeet.uk/2012/11/24/stack-overflow-question-checklist/)that you should go through before submitting your question.

Okay, admittedly I make some poignant observations and suggestions that can be seen as helpful.

If you have been given this link as a response to your question on stackoverflow.com, please don’t take the following personally. I do not intend to offend or insult you, it’s just that I’ve become a little too annoyed to not point out the flaws directly and admittedly without sugarcoating them. Nevertheless there’s good advice in here and I’m sure you’ll know how to apply that to your question and you will get (better) answers because of it. I’m just trying to ~~vent~~ .. help. ![:)](../wordpress/wp-includes/images/smilies/simple-smile.png)


### Any Ideas? Suggestions?

So tell me, what you you **really** want to know?

You can’t expect stackoverflow users to give random suggestions and guidance. This is [not what stackoverflow is about](http://stackoverflow.com/help/on-topic). It is about concrete problems that are likely to have a specific answer (or two).

If you don’t know what specific question you should ask then it’s the same as not asking anything at all. It tells everyone you did not understand your problem well enough to ask a specific question about the problem. Which means any suggestions are very unlikely to point out the flaw in your thinking, or even nudge you in the right direction.

Worse, in some cases it’s obviously just poor laziness. You don’t even want to invest time in properly asking a question? Fine, but please don’t do that on stackoverflow.

### … is not working (properly).

“Not working” is not a problem description. You can say “my car is not working” if you need an excuse for your boss why you’ll be late to work. But even a mechanic won’t be able to diagnose your car’s problem if you can’t describe what you were doing and what the car did.

[
Continue reading »
](http://www.learn-cocos2d.com/2014/10/missing-stackoverflow-topic-terrible-question/#more-7342)

I’m done writing the *Tome of SpriteBuilder*.

There’s only edits and reviews left, page proofing and then it goes out to print. Meanwhile, I’m cleaning up and extending the *Bouncy Beast* project for its App Store release.

Time to share some insights as I haven’t been able to slice some time off to write about the process as I originally intended to.

### What’s in the book?

In the [Learn SpriteBuilder book](http://www.apress.com/9781484202630) you will learn [SpriteBuilder](http://www.spritebuilder.com/) step-by-step while building the Bouncy Beast game.

The book will guide you through the creation of a physics-driven, parallax-scrolling game with the help of SpriteBuilder, Cocos2D (cocos2d-swift) and Objective-C. The level-based structure will enable you to add more content to the game, even without writing additional code.

As your guide I will walk you through the individual steps necessary to create the game project. Along the way I’ll explain the SpriteBuilder features, caveats, workarounds and helpful tips and tricks as you are most likely to come across or need them.

At the end you’ll have a complete game reminiscent of games like Badland.![978-1-4842-0263-0_Figure_13-16](../wordpress/wp-content/uploads/978-1-4842-0263-0_Figure_13-16-300x133.jpg)


The game also runs on Android devices thanks to

[Apportable’s Android plugin for SpriteBuilder](http://android.spritebuilder.com/).

The Bouncy Beast project’s source code will be available.

### Bouncy Beast Demo Video

Here’s a video demonstrating the game. Notice the subtle particle effect on the main menu’s background, the paginating scroll view, the soft-body player character.

**NOTE**: the suboptimal framerate in the video is 100% attributable to the iOS Simulator from which I recorded the video. On an iPod touch 5G the game runs with a constant 60 fps.