---
title: A premature preview of cocos2d-iphone v3 preview
url: http://www.learn-cocos2d.com/2013/11/premature-preview-cocos2diphone-v3-preview/
author: Scott Lembcke says
published: '2013-11-18'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

A preview version of cocos2d-iphone v3 has been available for a couple days now. I thought I’ll take a closer look and summarize what’s been done, what’s working and what isn’t, what’s new and what’s old but revamped.

### Installation

The installer script has been revamped. It has a different name (install.sh) and different parameters (-force instead of -f).![Screen Shot 2013-11-18 at 18.06.21](../../../wordpress/wp-content/uploads/Screen-Shot-2013-11-18-at-18.06.21-300x123.png)


The first thing I noticed is that the installer is downloading Chipmunk2D. Made me wonder why, so I double-checked to confirm: Chipmunk isn’t included in the archive. This means no offline installation.

I’ll explain later why Chipmunk isn’t included.

### Project & File Templates

In the preview there’s only one project template. It doesn’t demo any physics features, it’s your typical “Hello World” example with buttons.

There seems to be an issue with the template where any attempt to save it to a custom location caused Xcode to crash. In fact every time the “Save File” sheet came up and I didn’t click on “Create” right away, Xcode would crash. That’s just one of the reasons why it’s still a preview.

The CCNode File Template isn’t worth mentioning at this point, it creates an empty Objective-C class and is barely different from the regular Objective-C class template at this time.

### Hello World v3

A closer look at the Hello World template reveals that it has finally received some polish.![Screen Shot 2013-11-18 at 17.36.52](../../../wordpress/wp-content/uploads/Screen-Shot-2013-11-18-at-17.36.52-300x163.png)


Gone are the obnoxious, if not condescending comments of the previous templates on just about every line, including imports and implementation. The onEnter and onExit methods already exists with comments to call super, a common mistake with non-obvious consequences made by far too many cocos2d developers.

My enthusiasm for cocos2d finally showing off well-formed code to starters is only dampened by the init style where self is not checked for being nil. That ought to be fixed.

If you build and run, you’ll see a couple developer notes and warnings, and the app launches with a straight out warning to not use the preview for development. Heed that advice. Overall v3 is far from being ready for production use. My advice is to come back and have a look at it next spring - if you’re an early adopter and know how to debug, report and work your way around bugs.

For example when I ran the template using iOS 6 simulators, performance was terrible. Everything was super-smooth on iOS 7 but not iOS 6. This certainly needs some more testing.

### Display Some Sprites

The template project only shows a label and a button. I decided to add some sprites to the mix to see how commonly used code has changed. Can you spot the differences?

|
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 |
CCTexture* texture = [CCTexture textureWithFile:@"Icon.png"]; CCSpriteBatchNode* batchNode = [CCSpriteBatchNode batchNodeWithTexture:texture]; [self addChild:batchNode]; for (NSUInteger i = 0; i < 800; i++) { CCSprite* sprite = [CCSprite spriteWithTexture:texture]; [batchNode addChild:sprite]; sprite.position = CGPointMake(CCRANDOM_0_1()*360+60, CCRANDOM_0_1()*200+60); sprite.rotation = CCRANDOM_0_1() * 360.0; sprite.color = ccc3(CCRANDOM_0_1()*255, CCRANDOM_0_1()*255, CCRANDOM_0_1()*255); sprite.opacity = CCRANDOM_0_1() * 255.0; id rotate = [CCActionRotateBy actionWithDuration:CCRANDOM_0_1()*10 angle:360]; id forever = [CCActionRepeatForever actionWithAction:rotate]; [sprite runAction:forever]; } |

Two changes are noticeable: CCTexture2D is now CCTexture and action classes are now distinguishable by always using the “CCAction” prefix. Everything else works as expected.

Instead of using CCTextureCache - which is no longer imported by the cocos2d.h header - CCTexture’s textureWithFile: initializer is now used.![Screen Shot 2013-11-18 at 18.32.59](../../../wordpress/wp-content/uploads/Screen-Shot-2013-11-18-at-18.32.59-300x209.png)


For better or worse, the API hasn’t changed much. At least not yet. This is good news for cocos2d users but bad for developers who wish to “upgrade” from Sprite Kit to cocos2d-iphone v3 because the differences still far outweigh the similarities on the API level.

The basic API is supposed to be adapted to mimic Sprite Kit. Though even if it won’t, this is easily doable as an add-on, by simply mapping API calls to the cocos2d-iphone equivalent. Most of these changes can be done with “Sprite Kit compatibility” categories and I’m sure someone will please the crowd with such an add-on should v3 not provide that out of the box.

### Cocos2D UI Controls

There’s now a welcome extra project named cocos2d-ui which includes a couple user interface controls. Nothing mind-boggling, and if you’ve been using the cocos2d-iphone-extensions project there won’t be any surprises for you.

Here’s the list of UI classes that currently exist:

- CCButton
- CCSlider
- CCTextField
- CCScrollView
- CCTableView

Most of them seem to be ports or adaptations of previously existing classes from cocos2d-iphone-extensions.

### All ARC Now

It’s worth mentioning: the cocos2d-iphone codebase has been ported to use ARC. No more retain, release, autorelease.

I find this most exciting because I hate to answer the n-millionth MRC related issue over on stackoverflow.com simply because cocos2d developers start projects based on the current MRC templates and never give ARC a second thought. Or a first one, probably too many don’t care or don’t know about ARC. Exactly those who should be using it I’m afraid.

### Cocos2D Internals

The code is better structured, some classes have been renamed to better names or conform to the conventions. For example CCTouchDispatcher is now two sets of classes, CCResponder and CCResponderManager.

There are now CCLayout and CCLayoutBox class to layout child nodes on a grid. Which should be named CCLayoutGrid but oh well, I’m also someone arguing that Box2D is somewhat of a misnomer since a box is a 3D primitive and its 2D representation is a rectangle. Go, Rect2D, go! 😉

With CCLayout(Box) and CCButton you can create a CCMenu with items, which is why CCMenu itself and related classes no longer exist. About time.

TMX support is currently non-functional. Not only does loading a TMX crash with an unrecognized selector at a very early stage (not related to the TMX file itself). I couldn’t even find any reference to any drawing code. It’s gone. Which is good news because it seriously needed an overhaul anyway.

If TMX support isn’t coming back, or not anytime soon, there will always be the tilemap renderer provided by [OpenGW](http://opengameworld.com/) - that is once OpenGW supports cocos2d-iphone v3, which we’ll do when developers actually start using v3, which will probably not be before well into 2014 - in case you meant to ask.

Coding style: always a matter of subjectivenessity - so I won’t dabble much into that. Just two things I noticed: there are many awkward one-liners of the form `-(BOOL)isPhysicsNode {return NO;}`

. Makes me cringe.

Also you’ll frequently find calls to static inline C functions from Objective-C methods to avoid Objective-C messaging overhead. In many cases this looks a lot like premature optimization.

A very welcome change is the removal of the C libraries, like hash tables. Instead Core Foundation classes are used.

I tried to find the proposed new renderer but couldn’t find anything. Supposedly a lot of progress was already made on the renderer, but no matter where I looked it was nowhere to be found. The rendering code still pretty much looks like v2.1. My sprite test also confirmed that there is no auto-batching in place yet, you still have to create and use CCSpriteBatchNode manually. My guess is the new rendering code is still under wraps and not included in the current preview version.

### Audio Engine: ObjectAL

I’ve long been promoting [ObjectAL](http://kstenerud.github.io/ObjectAL-for-iPhone/) so I’m really happy to see it has replaced CocosDenshion in the cocos2d-iphone distribution.

Compared to CocosDenshion ObjectAL is easier to use, it too has a “simple audio” interface but even the more complex stuff comes more natural. It has more features and fewer issues (in my experience) than CocosDenshion. It’s action support makes changing audio effects over time easy.

In the past ObjectAL’s biggest drawback was not supporting OS X. But OS X has been supported for a couple months now. Internally ObjectAL uses OpenAL and AVAudioPlayer, depending on the task at hand, so its internals are quite similar to CocosDenshion.

### Physics Engines

Currently Box2D is included in the distribution, but there’s no template project for it at the moment. The Hello World template includes the Chipmunk2D files, but doesn’t use them.

The inclusion of Objective-Chipmunk is welcome, but in the current preview it is still closed source as a set of header files and a precompiled static library. Hence the reason why Chipmunk is downloaded and compiled by the install script. Objective-Chipmunk will be released entirely as open source in a future release however.

CCPhysicsNode and CCPhysicsBody are using Objective-Chipmunk internally. All CCPhysics* classes show no indication to be amended with support for plain C Chipmunk2D nor Box2D.

In fact it seems Box2D is all but provided as source code on an “as is” basis in the download with no connection to cocos2d-iphone. Quite frankly I think Box2D should be removed from the distribution altogether if this is to remain. Developers who know why they want to use Box2D should be capable enough to add it by themselves.

Anyhow, CCNode now has a physicsBody property equivalent to Sprite Kit, and the implementation is far more complete and flexible than the previous CCPhysicsSprite “hack”.

### CCBReader included

The new CocosBuilder is now actually called SpriteBuilder, probably to avoid confusion because CB will not support cocos2d-iphone v3 but only cocos2d-x, whereas SpriteBuilder will support cocos2d-iphone v3 but probably not cocos2d-x.

The necessary loader code named CCBReader is now included in cocos2d-iphone v3. That just makes a lot of sense.

What doesn’t make a lot of sense in my opinion is the CCBReader.m code itself. If you’re a developer considering to use CocosBuilder or SpriteBuilder, I dare you to have a look at that file. If you ever need to debug an issue where something doesn’t come out in code quite as you edited it in CB/SB, then, I quote: “Good luck groking this!”

I could start ranting here and never stop, so I’ll just leave it at: XML would have been just fine! Or NSCoding if SB is really only made for cocos2d-iphone v3. Or any other ready-made file archiving solution available as open source library, like, you know, zlib. Shhhh, calm down Steffen …

### I, for one, welcome our new Cocos2D Overlords!

I am of course referring to: *Copyright (c) 2013 Apportable Inc.*

You’ll find this mainly in the CCBReader and related files. After all, and perhaps you didn’t know: the author of CocosBuilder and now Sprite Builder is working for Apportable after some time with Zynga.

And just in case you don’t know this other thing: [Apportable](http://www.apportable.com/) is sponsoring the development of cocos2d-iphone v3. So it has a financial backer, but more importantly a company who has a vested interest in supporting Open Source Objective-C rendering engines.

So where does that leave Zynga’s involvement? A 100% over at cocos2d-x. All the Zynga developers are working on cocos2d-x and all involvement in cocos2d-iphone has stopped, at least as far as I can tell. This should explain why SpriteBuilder split off from CocosBuilder.

And there’s at least some hope that SpriteBuilder might support Sprite Kit in the future. Though that would certainly require lots of re-engineering because SB is so very tightly coupled with cocos2d-iphone.

### Come back next spring!

That’s my advice if you were asking me when to consider using cocos2d-iphone v3. Given that development continues at the current pace, depending on your requirements and your willingness to be an early adopter. Make it summer or later if you want others to do the beta-testing.

Though cocos2d-iphone for the most part remains familiar, both it’s API and the code, there are substantial changes throughout the entire codebase that require everything to be re-verified: iOS versions and various devices, device resolutions and file suffixes, possible bugs due to ARC conversion, whether all tools and data formats are still correctly supported, and so on. Not to mention the proposed new renderer.

I hope you weren’t expecting cocos2d-iphone v3 to be ready before Xmas with all the [proposed features](http://www.cocos2d-iphone.org/forums/topic/cocos2d-v3-is-not-dead/). I wasn’t kidding when I said “3 years” for everything (for a single developer, now there’s more people working on it). Right now the features implemented from the feature list - as far as I can tell - are ARC, integrated physics, some UI components, a few Sprite Kit API adaptations. On the other hand the preview apparently doesn’t include all of the work in progress, so the actual state of v3 can’t be assessed.

Basically what the v3 preview represents is in fact more like a v2.2 update. The true v3 update is yet to be released.

In fact cocos2d-iphone v3 will be split up into old functionality that’s being kept alive for the sake of “backwards compatibility”, while new functionality is added as an alternative to the old way of doing things. I really don’t like this because it’ll make it more confusing for both new users and those upgrading (and those helping those). Personally I was hoping more for a clean slate and fresh start.

To be perfectly honest with you: I’m confused. I’ll revisit v3 another time, next year.

PS: Keep in mind that this is a snapshot of a development build subject to change quickly and rapidly, so take everything with a grain of salt. More so the more time has passed since this article was written.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Speaking to the physics implementation:

Objective-Chipmunk is open source now, we even talked about this a few weeks ago… https://github.com/slembcke/Chipmunk2D/tree/master/objectivec The reason why it (the source code) is downloaded and compiled into a static library is because the installer script was a little rushed for the alpha release. Nothing nefarious. I think it was turned into a separate target instead sometime last week.

CCPhysicsNode is used as the analog of a cpSpace or a b2world, and not the same as the old CCPhysicsSprite class. You are allowed to have multiple simulations within the same scene, and it allows you to adjust the physics coordinates using regular node transforms.

Though not well documented yet for the alpha, the CCPhysics+ObjectiveChipmunk.h header has (most of) the necessary methods you need if you want to write interoperable Objective-Chipmunk or C Chipmunk code. This was something that was intended from the start. Though at first using it might be a little rocky until we can make some example content.

Cool, good to know! I’ll update the article.

Thanks for the great article! This is extremely useful feedback for us. Please don’t hesitate to reach out if you have more detailed feedback that you left out of the article to keep it shorter.

[…] by Core Foundation classes. I don’t have a full overview of the changes, but at least the renderer doesn’t seem to have changed in any significant way. […]