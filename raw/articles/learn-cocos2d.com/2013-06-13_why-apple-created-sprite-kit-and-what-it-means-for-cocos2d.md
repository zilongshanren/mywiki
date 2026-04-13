---
title: Why Apple Created Sprite Kit And What It Means For Cocos2D
url: http://www.learn-cocos2d.com/2013/06/apple-create-spritekit/
author: Tomasz says
published: '2013-06-13'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Looking for a Sprite Kit Game Engine? Check out

[!]Kobold Kit

In case you missed the news: **Sprite Kit** is Apple’s 2D rendering engine for games, announced with iOS 7 at WWDC 2013 by merely mentioning it among other new APIs. A small step for Apple, a giant leap for gamedeveloperkind. This changes everything!

Many compare Sprite Kit with cocos2d-iphone. Don’t ask me why, they just do. 😉

If you’re a registered Apple developer you can check out the [Sprite Kit Programming Guide](https://developer.apple.com/library/prerelease/ios/documentation/GraphicsAnimation/Conceptual/SpriteKit_PG/Introduction/Introduction.html#//apple_ref/doc/uid/TP40013043) and the [SpriteKit.framework reference](https://developer.apple.com/library/prerelease/ios/documentation/SpriteKit/Reference/SpriteKitFramework_Ref/_index.html#//apple_ref/doc/uid/TP40013041) yourself.

Sprite Kit is under NDA, like the rest of iOS 7, so I won’t spell out any details here. I posted my [list of strengths and weaknesses of Sprite Kit](https://devforums.apple.com/message/824501#824501) on the developer forum, where we can freely discuss such details.

Here let me just try to answer the questions: why did Apple create Sprite Kit, and why now?

#### The Biggie: Apple acknowledges games!

Apple finally understands the significance of games for their platforms! Sprite Kit is acknowledgement of that fact. Rejoice!

Especially if you consider the rumored Apple TV set: imagine a television set that runs iOS with an App Store to download and buy **YOUR** games. Interestingly, iOS 7 also adds an API for 3rd party game controllers, think of joypads, like those you get with an Xbox or Playstation.


Combine it all: Apple’s television device, an App Store, and game controllers and - tadaaa - you get **Apple’s competitor to Xbox One and Playstation 4**!

For Apple the influx of Indies is great, they don’t care about established business models, so they don’t have to lock out the indies from a closed platform to keep the big publishers happy which simply don’t want to compete with their AAA million $ budget titles with garage games.

The great thing for Apple is that within the mass there’ll always be a few outstanding, innovative, marketable, sales-driving titles being delivered, and incidentally won’t be available on any other platform.

If the Apple TV also turns out to be technically capable enough and manages to gain acceptance by big game publishers as a competitive gaming device for AAA titles, then Microsoft, Sony and especially Nintendo will have a big problem.

#### Hardware & Software Compatibility

I believe this is one of the main reasons why Apple needed to make sure Sprite Kit exists, because it will work with any new Apple hardware from day one. Existing Sprite Kit games published by then will likely be very easy to port to “iTV” and whatever other devices are coming.

And you will not have any compatibility problems with new software releases either, Sprite Kit will work flawlessly with new versions of Xcode, iOS, OS X, and whatever other software Apple changes. It doesn’t happen too often either and comes with prior notice and lots of time to adapt.

For cocos2d-iphone it regularly took several months to adapt to SDK changes and to add support for new devices and for these compatibility issues finding their way into an official (stable) release.

Particularly off-putting is that cocos2d still labels released with “stable” vs “unstable”, yet the meaning is frequently lost while the stable version doesn’t work with current technology, but the unstable version does.

I’m glad we won’t be having any of these issues with Sprite Kit.

#### Dependable API

Despite cocos2d-iphone not having added any significant feature for years, it was constantly being changed. Practically every new version introduced some changes that forced developers to change their code.

The individual refactoring choices of the past years were mostly good ones, and appreciated, but delivering them incrementally among other things instead of doing one complete overhaul is just annoying for a publicly serviced game engine. It’s tiring and frustrating.

Now consider that Sprite Kit will largely remain as is. If you expect Sprite Kit to improve frequently, think again. What you see now is the near final API, and it will likely be 90% of what Sprite Kit will be 3 years from now.

This is a good thing! It means the half-life of knowledge, tutorials and books will increase, perhaps tremendously so. I’m thinking from perhaps 3-9 months up to 1-3 years or more! This makes it easier to pick up on Sprite Kit, and developers are even more likely to service it by writing tutorials, answering questions, building support frameworks, etc.

#### Stay native, dammit!

Sprite Kit is Apple telling developers to use their native APIs, and now in particular for games. Cool 2D games only available on iOS, ideally those **only possible** on iOS is what Apple wants to see from us.

Apple knows how loyal developers are to their platform - just as much as the users of Apple devices and systems - so Sprite Kit is an investment in a growing game developer base.

Now Cocos2d-iphone still is currently the most popular, iOS-only game engine - but in recent years Zynga pulled it towards cross-platform with a Javascript extension and [shifted development focus towards cocos2d-x](http://www.cocos2d-iphone.org/forums/topic/sprite-kit-based-on-cocos-2d/#post-405619). This is neither in the interest of the cocos2d-iphone users, nor can I imagine Apple being happy about the most popular iOS engine being diluted with cross-platform developments.

Sprite Kit is Apple’s way of reassuring, convincing and funneling game developers to stick to iOS and OS X. It is Apple taking control over how game developers create games for Apple devices and computers. Meaning: elegantly and efficiently, but also “locked-in” with no source code.

There are still reasons for using other game engines, but this is now a desire only shared by hardcore programmers. Not the ones Apple is targeting with Sprite Kit.

If you still want to be able to port your Sprite Kit game to Android, there’s [Apportable](http://www.apportable.com/). No doubt they’ll chime in quickly to make their service compatible with Sprite Kit, especially since Sprite Kit will be a ubiquitous and stationary target.

#### So why now? Doesn’t make sense now, right?

Why now? Well perhaps Apple felt Zynga is pulling the rug right out from under them ever since they started directing cocos2d’s development (sometime in 2010-2011). Sprite Kit could have come earlier but I guess cocos2d’s shift towards cross-platform had to happen first.

That and acknowledging how important games are for iOS and how instrumental it was for iOS’ success - ironically that’s something Apple might not have been so quick to accept under Steve Jobs.

The other thing is Apple having this TV device in their pipeline that would greatly benefit from a native rendering engine, especially if it means many existing games can be ported easily and considering that it will compete with Xbox One, Playstation 4 and Wii U. Then consider how long it might have taken cocos2d-iphone to deliver Apple TV support, if at all.

The timing makes a lot of sense. Apple isn’t here to do us a service - that’s just a neat and desirable side effect we happen to benefit from. They aren’t evil either. Now is simply the time for Sprite Kit because Apple is preparing to innovate on a new market (TV & game consoles), for the first time since 2007, and success in that market depends on games to a large degree.

Sprite Kit and the time of its release are nothing but pragmatism. This I love about the post-Jobs Apple.

#### Cocos2d, not nearly as beginner-friendly as it could be

How cocos2d became known to be beginner-friendly is because originally it could only be compared with OpenGL. In that case, yes, far easier than OpenGL, undisputed.

If you’ve been working with other game engines in the past, you know the cocos2d API leaves a lot to be desired, and there are far easier, more elegant ones out there. I see cocos2d developers struggle with the exact same issues or concepts nearly every day - many are the same ones I faced back in 2009. Concise, consistent and complete documentation does not exist anywhere, and new user experience varies greatly depending on what and who they learn from. That’s just sad.

Sprite Kit is beginner-friendly. It has the typical well-designed, trimmed, sleak API you’d expect from Apple. It’s got excellent documentation that’ll stay up to date and is complete.

But the greatest benefits are in the things you don’t really need to consider anymore. Things that Sprite Kit takes care of for you. Things many beginning cocos2d developer isn’t aware or capable of, or interested in doing - those are the tasks a truly beginner-friendly framework takes over from the user. That’s what Sprite Kit does.

Apple started with a clean slate and took great care in designing the Sprite Kit API. Everything falls together as neatly as possible. I’m heavily impressed, and convinced that Sprite Kit is to cocos2d-iphone what ARC is to manual reference counting.

#### The Stepping Stone Theory

Don’t get your hopes up that Sprite Kit will be a stepping-stone for a coming generation of cocos2d developers “upgrading” from Sprite Kit.

Anyone who will have started with Sprite Kit and then tries out cocos2d will find it confusing, inconsistent, archaic, badly documented, unnecessarily complex and requiring a lot more dreadful handiwork. This is not an upgrade, it’s a step backwards.

As iOS 7 adoption reaches the 90% mark there will be little reason to stick with cocos2d-iphone. We’ve seen cocos2d-iphone rise slowly to ubiquity in the past 5 years, it may only take 5 months for it to become a legacy project. In a relatively short time the great majority of cocos2d-iphone will have moved on, to Sprite Kit, to cocos2d-x, or elsewhere.

The only way for cocos2d-iphone to stay relevant is to focus on the strengths it has over Sprite Kit while adapting Sprite Kit’s convenience. It would be huge time investment, and not getting paid to do this makes it highly unlikely.

#### What about 3D games?

Sprite Kit, as the name implies, is 2D only. So why not 3D?

Because that field is really not for beginners - and this goes both ways: Apple developers and Apple’s developers. 3D renderers will immediately compete and be compared with Unity or Unreal technologies and their excellent tool chains. It’s extremely hard to compete with them from scratch, even (or especially) for Apple who are new to the game development field and not that interested in it either.

And let’s be honest: there aren’t that many great 3D apps on either App Store - especially not from indies. The 3D games I remember the most are from id Software, Epic, Ubisoft and EA.

I wager that 80% of iOS games are 2D and even among the 3D games, few are truly 3D in that you can actually move in 3 dimensions. 3D games are a factor of three dimensions more difficult, more expensive and time consuming to create. 3D games are notoriously hard to make visually appealing, especially when compared to an alternative 2D version of the same game.

2D games have had a renaissance since the introduction of the iPhone in 2007. TV sets and newer mobile devices aren’t going to end that trend. 3D games are dominated by big game developers and publishers, it’s one way they can distinguish themselves most easily from Indie productions.

#### Sprite Kit Adoption

With Apple implementing a rendering engine for games, everyone is going to adopt Sprite Kit and in a short time there’ll be more Sprite Kit experts and code add-ons and tools than there ever were cocos2d experts and code add-ons and tools.

Zynga isn’t in it for making a great game engine, for them the engine is as a means to their end to efficiently develop cross-platform games with technology they own (or at least control). So they’re unlikely to chime in and support cocos2d-iphone or a Sprite Kit based engine.

Given the usual iOS adoption rate and the growth of new iOS device sales most developers will inevitably cut support for iOS 6 in 2014. So the backwards compatibility issue is (once again) not going to be an argument for long.

Programming-oriented game developers will then have these choices: use Sprite Kit and go entirely Apple-native with all the goodies (Objective-C, ARC, native APIs) or saddle an elderly cocos2d-iphone horse in “maintenance mode”. What will you choose to do a year from now?

The alternative: bite the bullet and develop cross-platform - either using overpowered 3D technologies like Unity or Unreal, using a low-level and cumbersome C/C++ game engine or one using Javascript or Lua with severe performance penalties.

I believe the choice to use Sprite Kit will be rather obvious for many, especially with Sprite Kit being an “Apple product” and inevitably surrounded by a host of contributing software and tools. Which brings me to my last point.

I started working on ** Kobold Kit**, a game engine built on and extending Sprite Kit! The upcoming

**KoboldTouch 7.0**will use Kobold Kit as its rendering engine in place of cocos2d-iphone.

**Kobold Kit** will be available the day iOS 7 is released. KoboldTouch 7.0 should be available the same day or very soon after that. Needless to say, KoboldTouch 6.x will continue to evolve and be supported and work with iOS 7 and will continue to use cocos2d-iphone.

I know one thing with conviction: Kobold Kit is a once-in-a-lifetime opportunity to build something great, it has to be done, and I want to do it like nothing else. If there was ever one thing I was deeply and utterly convinced of, this is it! Having built two engines on top of cocos2d-iphone, I’m so glad to get the chance to start from a clean slate and apply everything I’ve learned while avoiding all the nasty things I had to do to conform to cocos2d and being able to do the things I just couldn’t do with cocos2d.

More details for registered Apple developers [here](https://devforums.apple.com/thread/190919?tstart=0).

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

[apple](http://www.learn-cocos2d.com/tag/apple/)•

[apple tv](http://www.learn-cocos2d.com/tag/apple-tv/)•

[beginner](http://www.learn-cocos2d.com/tag/beginner/)•

[cocos2d](http://www.learn-cocos2d.com/tag/cocos2d/)•

[cocos2d-iphone](http://www.learn-cocos2d.com/tag/cocos2d-iphone/)•

[cocos2d-x](http://www.learn-cocos2d.com/tag/cocos2d-x/)•

[cross platform](http://www.learn-cocos2d.com/tag/cross-platform/)•

[design](http://www.learn-cocos2d.com/tag/design/)•

[engine](http://www.learn-cocos2d.com/tag/engine/)•

[game controllers](http://www.learn-cocos2d.com/tag/game-controllers/)•

[game developer](http://www.learn-cocos2d.com/tag/game-developer/)•

[game development](http://www.learn-cocos2d.com/tag/game-development/)•

[game engine](http://www.learn-cocos2d.com/tag/game-engine/)•

[game engines](http://www.learn-cocos2d.com/tag/game-engines/)•

[itv](http://www.learn-cocos2d.com/tag/itv/)•

[joypads](http://www.learn-cocos2d.com/tag/joypads/)•

[Kobold](http://www.learn-cocos2d.com/tag/kobold/)•

[KoboldTouch](http://www.learn-cocos2d.com/tag/koboldtouch/)•

[list of strengths and weaknesses](http://www.learn-cocos2d.com/tag/list-of-strengths-and-weaknesses/)•

[Sprite Kit](http://www.learn-cocos2d.com/tag/sprite-kit/)•

[SpriteKit](http://www.learn-cocos2d.com/tag/spritekit/)•

[television set](http://www.learn-cocos2d.com/tag/television-set/)•

[wwdc](http://www.learn-cocos2d.com/tag/wwdc/)

I have just released my game that is built on top of SpriteKit. It’s called “737 Flight Simulator” you can check it out if you want. SpriteKit is still very limited at the moment, but I think it has a great future. I am pretty sure Apple will do it’s best as they always do to make it better.

One of the most in depth reviews about Sprite Kit. Obviously, Sprite Kit will be a major favor in iOS game development. Cocos2d-x still gets its own strength for cross platform games.

What about HTML5 app/games in the future when the phones will be much more powerfull which will eliminate the need for native sdk ?

You mean the same future where we don’t need a desktop OS anymore but instead the browser “becomes” the OS? That will not happen, neither for desktop nor phones, within the next 15-20 years at least. If ever.

For mobile specifically the companies making phones and OSs are way too eager to lock in customers to their native world, so they have little motivation to bring about a HTML (meaning: standardized) phone or OS.

>That will not happen, neither for desktop nor phones, within the next 15-20 years at least. If ever.

Do you have any idea how ridiculous that statement is ?

This is like someone in 1994 predicting that in 2014 windows will never be used for games as DOS is better suited. You simply can’t predict 20 years ahead in this business.

You forget that there is no mobile phone company in the world that is interested in creating a platform based on an open standard (HTML5). Android is locked-in, Windows is locked-in, iOS is locked-in.

It would take a giant of Apple, Microsoft or Samsung caliber to change that and disrupt the market. So no, HTML5 phone will not happen respectively won’t play a notable role within the next 10-15 years, if ever. I don’t think predicting that is ridiculous.

Some game companies have already tried to go down the HTML5-only route but eventually turned towards native apps. Performance certainly was an issue, but mainly it’s things like accessing a phone’s native functionality that is not possible with HTML5 but so important to many games. Like access to photo, music, video libraries, camera, contacts, location data, facebook/twitter accounts, mail, facial recognition, touch input, accelerometer, gyroscope, etc.

IOS devices are but a small part of the mobile devices pie these days, and it is only going to shrink as more and more Android devices find their way out of China.

Apple are going to have a difficult time convincing people to write for IOS only when the largest market is Android.

Don’t mistake “number of devices” for the size of the market. Android in itself is not a market, it is fragmented into a myriad of devices, OS versions, and even competing App stores. Android devices are a ubiquity, while iOS devices are a status symbol. That and because Android owners are on average less affluent they are also less likely to spend any money on apps. Overall revenue margins are still higher on iOS.