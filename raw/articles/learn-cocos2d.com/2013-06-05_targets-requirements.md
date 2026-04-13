---
title: Targets, Requirements
url: http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.2/KoboldTouch-mac/html/index/
published: '2013-06-05'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

KoboldTouch treats you nicely: Automatic reference counting (ARC). Model-View-Controller (MVC) architecture. 100% Objective-C interface. Objective-C physics. Following Cocoa design guidelines.

Visit [http://www.koboldtouch.com/x/64Bq](http://www.koboldtouch.com/x/64Bq) for more info on KoboldTouch.

# Targets, Requirements

- Xcode 4.5+ required (automatic property synthesizing, ObjC literals, subscripting, armv7s)
- Use of ARC is mandatory (already enabled)
- Deployment Targets: iOS 5.0 and Mac OS X 10.7 or higher
- Device Support: iPhone 3GS and newer, iPod touch (3rd generation) and newer, iPad 1 and newer

# Technologies

- Objective-C, ARC
- cocos2d-iphone + extensions
- Box2D
- Lua
- Spine Runtime
- PhysicsEditor
[GB2ShapeCache](/)
- and many more ...

# Design Goals

- Built-in MVC framework.
- View controllers for every cocos2d node class. All custom nodes supported as well.
- Encourage assignment of model, view and controller rather than having to create subclasses.
- Avoid lengthy initializers. Create initialization objects to pass both required and optional parameters (with sensible defaults) to the receiving class.
- Fix the things (project structure, folder locations, tools, bulkiness, source control) that made some users turn away from Kobold2D. (All known issues have been addressed.)
- Some cocos2d actions (ie CCMoveTo/By) break the MVC relationship since actions modify only the view, not the model. Actions are re-implemented as
[KTAction](/) classes (ie [KTMoveAction](/)) acting on the model.

# Known Issues

- Cocos2D/CocosBuilder are completely oblivious to MVC. CocosBuilder can not be used with KT.

# Design Guidelines

Embrace Objective-C! Don't fight it, use it!**

- Write
*everything* in Objective-C first. You can still optimize later if you really really really have to **and** have verified that through profiling.
- Follow
[Cocoa best practices and guidelines](http://developer.apple.com/library/mac/#documentation/Cocoa/Conceptual/CodingGuidelines/CodingGuidelines.html).
- Let Xcode synthesize properties and ivars for you. Saves time, adds consistency.
- Prefix ivars with an underscore (_myVar) just like Xcode does when it synthesizes a property.
- Declare ivars private by default.

Structs and C arrays are notoriously difficult to archive, harder to work with, unsafe, and in 99% of the cases really not worth the trouble. Therefore:

- Don't use structs. Create property-filled Objective-C classes instead. Add an initializer to make it comfortable to use, harder to break. You can still make ivars public if profiling revealed that it does make a noticeable difference (in 99% of cases it won't).
- Don't use CCArray, avoid C arrays whenever possible. Use NSMutableArray and other Objective-C collection classes instead. For storing basic types (float, int, BOOL) in NSArray, etc use NSNumber or
[KTMutableNumber](/).

# Performance Optimization Guideline

Your primary goal is to write code that works, is readable and maintainable. Ignore performance until the very end, or when it shows to be a problem even in release builds, and only on a device.

In other words: the most performance gains in iOS apps is optimizing the usage of resources. Draw less, convert images to lower color depth, use .pvr.ccz images to improve load times, rendering performance & memory usage all at once, reduce particle count, reuse objects instead of repeated alloc/init/dealloc cycles - that's how most performance goes wasted, and those are simple things to fix. Code optimization of game logic typically has far less (little to no) impact on framerate.