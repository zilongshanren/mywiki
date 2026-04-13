---
title: What the FAQ is going to happen with Kobold2D?
url: http://www.learn-cocos2d.com/2012/11/faq-happen-kobold2d/
author: Jesse says
published: '2012-11-23'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Since I’ve started to offer [KoboldTouch](http://www.koboldtouch.com/) developers have been wondering what will happen to Kobold2D? I’ll answer these questions here.

#### Kobold2D Updates

When cocos2d 2.1 (stable) is released, I’ll update Kobold2D to include this latest cocos2d version. Same with any other cocos2d version that will be released in 2013. I won’t update to beta versions - sometimes they’re riddled with bugs, other times the next beta comes only a week or two later.

I’ll continue to support and update Kobold2D for as long as there’s interest in it but I’ll definitely focus my efforts on KoboldTouch now.

#### KoboldTouch “Lite”

Sometime in 2013 (probably not before Q2) I’ll release KoboldTouch “Lite” for free, with limited features and support. This Lite version will then take over as the successor of Kobold2D, while Kobold2D will remain available for some time.

KoboldTouch “Lite” will have the MVC framework but not much else. It will not include any additional features such as OS integration, better tilemap rendering, Box2D Objective-C wrappers and what not.

This ought to help developers get accustomed with the MVC framework.

#### Relaunch of www.kobold2d.com

Sooner or later I’ll relaunch the [www.kobold2d.com](http://www.kobold2d.com/) website as [www.koboldtouch.com](http://www.koboldtouch.com/). I’ll go for a simple look & feel (KISS), it will include the Kobold2D articles and I’m going to write all KoboldTouch documentation publicly.

For one this will make it easier for me to write and publish documentation. It should also help KoboldTouch’s popularity to reveal its documentation to both developers and search engines.

#### KoboldTouch compatibility with Kobold2D

KoboldTouch is not 100% compatible with Kobold2D, since I’ve already trimmed the less popular libraries from KoboldTouch: Chipmunk, Chipmunk Spacemanager, Cocos3D, ObjectAL, SneakyInput, iSimulate, AdMob. The remaining libraries are: cocos2d-iphone, cocos2d-iphone-extensions, CocosDenshion, Kobold2D, Box2, Lua and a few smaller additions (BitArray, LOG_EXPR, etc).

You should be able to port code that does not use one of these libraries with ease. Though without adapting to the MVC framework you lose a lot of the benefits of using KoboldTouch.

#### Custom Folders and Source Control

Issues regarding custom folders and source control usage come up frequently. I will alleviate those with KoboldTouch.

The project starter tool will be improved to support creating new projects in a custom folder, with or without copying the offline documentation to the new folder. The project upgrader tool will also work with custom folder locations.

The documentation accounts for most of the disk space usage of a Kobold2D/KoboldTouch project and should therefore not be included when you intend to manage this project with source control. Specifically if it’s an online repository with limited disk space. With the additional libraries stripped and documentation not included, a new KoboldTouch project weighs in at around 15 MB of disk space.

What will remain is that the installer will install to a fixed folder, since you will then be able to create new projects in any custom folder so there’s no real need for a custom folder location during installation.

There are plenty of issues with PackageMaker to overcome to support custom folder locations and I’d rather spend that time on other things. As was always the case, you can of course move the Kobold2D folder anywhere else after the installation completed - it’s just one click & drag operation in Finder.

#### Your question not answered here?

Let me know by writing a comment.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

SneakyInput got the axe? Crud. I assume I can just add it to any future project and use it?

Yes, you can.