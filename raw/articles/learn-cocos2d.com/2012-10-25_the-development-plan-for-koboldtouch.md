---
title: The Development Plan for KoboldTouch
url: http://www.learn-cocos2d.com/2012/10/development-plan-koboldtouch/
author: Eugene Tulushev says
published: '2012-10-25'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

I like to take a moment and explain what the development process of KoboldTouch will be, and how you will influence the direction of KoboldTouch. But first, let’s have a look what I have planned for the initial version:

#### First Goal: KoboldTouch equals Cocos2D

**To be completed in November**, the main goal is to allow users to use the MVC framework of KoboldTouch with all features of Cocos2D, minus a few exceptions (odd features like CCMotionStreak).

You should be able to write Cocos2D apps with Cocos2D features entirely within the KoboldTouch framework. You’ll experience the KoboldTouch API design goal “feels like Cocoa”.

The first version’s features will be:

- Controller/Model Framework wrapping Cocos2D views
- View Controllers for “view” nodes, minus exceptions (see below)
- Scene Transitions
- Scheduled updates (Step methods in KT)
- Touch & Accelerometer input controllers
- Mouse & Keyboard input controllers
- Simple Audio Controller
- Simple Model Classes
- Archiving & Unarchiving Model Classes
- Basic “Hello World++” Example Project

This first version will be **KoboldTouch v6.0**.


#### Why is the first KoboldTouch version 6.0?

I like naming the KT versions by the main iOS version they’re compatible with. Right now that’s iOS 6 with backward compatibility for iOS 5. Once Apple releases iOS 7, the next KT version will be v7.0 while still supporting iOS 6 and for some time also iOS 5.

New features being added will generally be tested with the current and previous OS version, but not with the third to last. That means KT v7.0 will certainly be compatible with iOS 6 **and** iOS 5 at first. But any new features being added or refactoring of existing features will not be tested to work with iOS 5 anymore.

Apple wants us to keep moving on, and I’m not going to fight that. You can of course continue working with previous versions, and I’ll support them with important bugfixes for a limited time.

#### What will be in KoboldTouch v6.1?

I have some suggestions but it’s really up to you! For KT v6.1 only, I have compiled three “packages” myself to choose from to kickstart the process.

In the future, I’ll take all your suggestions with their votes, see which fit naturally together, then bundle them in a package (a set of required, important and optional features). You can then vote which one will be the development focus for the next version.

The point of these packages is that each is intended to be completed within 8 weeks. The allotted time also leaves room for documentation, bugfixes, support and other things. The end result of a package is a new feature or set of features that distinguishes KoboldTouch from most other iOS/Mac game engines, and Cocos2D specifically.

I like to give each package a short description or slogan, so that each version’s added value is immediately obvious to everyone and marketable.

#### Suggested Packages for KoboldTouch v6.1

I came up with the three initial packages based on what I think will differentiate KoboldTouch from any other game engine, Cocos2D in particular. Those are features I feel ought to be done, and I’ve seen them receive many positive responses. They are:

##### Package A: “Objective-C Physics”

- Complete Objective-C wrapper for Box2D

- Support for PhysicEditor designed shapes

- Simple Physics Game Project Template

- Archiving Physics Model Classes

- Wrapper prevents “spilling C++ code” into your project

- Separate static library to keep non-physics projects small

##### Package B: “Tilemaps: Faster, Endless, Parallax”

- Rewritten Orthogonal Tilemap Renderer (replaces CCTMX*)

- Faster: Map Size not a Performance Issue

- Endless Scrolling

- Parallax Scrolling

- Parallax View Controller (replaces CCParallaxNode)

- Better Tiled Editor Integration

- Autoscale TMX to Display Resolution

- Simple Tilemap Game Project Template

- Archiving Tilemap Model Classes

##### Package C: “All-In OS Integration”

- Integration of game relevant OS features (iOS & Mac):

- Game Center

- Gestures

- Twitter

- Facebook

- iAd

- Movie Playback

- Camera VR Background

- more if time permits (you choose) …

- OS Features Example Project

By joining the KoboldTouch project you can vote on Package A, B and C (feel free to leave a comment, too). The package with the highest number of votes will become the development target for KT v6.1, with development starting in December. At any time you can make suggestions, discuss them and vote on the next version’s features.

#### What if a feature takes over 2 months to complete?

You can always split down large tasks into smaller chunks, and then split the smaller chunks into tiny bits, and then slice the tiny bits down to molecule size, etc. while still creating something usable.

The interesting aspect and the important and healthy challenge is to use the set time to produce something that works and is usable within that time frame.

Let’s say the suggested feature is “Make a great game editor!”. Well, that certainly needs some more specifications, and naturally during that process one expresses individual goals as a [user story](https://en.wikipedia.org/wiki/User_story), for example: “I want to be able to place Sprites on a scene, move, rotate, scale and delete them, and save/load the scene”. That is not much, but it’s a start, pretty straightforward, and easily doable within 2 months.

Obviously 2 months is not enough time to actually complete a game editor. Such a large package needs to define the follow-up packages along with it, up to the point where it can be considered not just usable, but useful. Since this may easily bind a developer like me for many months, this is a task I would seek to get help with so it doesn’t block the regular flow of updates.

#### Long Term

Around 250 subscribers is my budget threshold for getting help, either through outsourcing individual tasks or even teaming up with one or two developers I know. And it really is only a matter of budget before KoboldTouch will transform from just me to a small team, in order to deliver increasingly greater value or simply more at the same time.

Because …

**I want that great game editor as much as you do!**

(I already have the plans in a drawer.)

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Will KT support CocoaPods? You can update the engine and it’s components so easy with it. And the whole thing will be modular.

I don’t know if CocoaPods can be used with Kobold2D projects. I think I remember one developer who used it with Kobold2D, or tried to. I never used it myself.

Support for CocoaPods may be interesting to do

ifa lot of developers are using CocoaPods. And maintenance doesn’t take a lot of time. I’m not sure if CocoaPods can be used for a commercial project though. Not from a legal perspective but accessing the files - I have no idea where CocoaPod gets the library files from but it seems as if they have to be on github in a public repository.I agree with Eugene that it would be very nice if a CocoaPod for Kobold could be created. I noticed there is one for Cocos2d, so I would suspect it could be done for Kobold.

As far as the comment if a lot of developers are using it; I’m not sure but it is pretty much the only game in town for iOS dependency management.