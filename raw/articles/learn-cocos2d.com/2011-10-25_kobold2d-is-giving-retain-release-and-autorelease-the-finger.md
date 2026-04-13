---
title: Kobold2D is giving retain, release and autorelease the finger!
url: http://www.learn-cocos2d.com/2011/10/kobold2d-preview-6-giving-retain-release-autorelease-finger/
author: Jose Antonio Andujar says
published: '2011-10-25'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

**Whaaaaaat?**

You heard right: if you want to forget about using retain, release and autorelease in your code, then the newly introduced [automatic reference counting](http://stackoverflow.com/questions/6385212/how-does-the-new-automatic-reference-counting-mechanism-work) (ARC) mechanism (aka “automatic memory management”) is the way to go. And guess what?

[Kobold2D Preview 6](http://www.kobold2d.com/display/KKSITE/Kobold2D+Download) fully supports ARC out of the box!

You may have heard that Cocos2D is incompatible with ARC at this time, and you’re right. However, the Cocos2D version in Kobold2D Preview 6 released just now has been improved to work with ARC. [This post explains the most important changes to make Cocos2D compatible with ARC](http://www.tinytimgames.com/2011/07/22/cocos2d-and-arc/). All 15 Kobold2D example projects compile with and without ARC, just like the other libraries Kobold2D makes use of!


Kobold2D has ARC enabled by default on all **new** projects if you’re using Xcode 4.2 / iOS 5. ARC is only available in Xcode 4.2, so if you haven’t yet upgraded to iOS 5 SDK with Xcode 4.2 now would be a good time. Otherwise Kobold2D will continue to work normally with ARC automatically disabled.

Note that the default deployment target of Kobold2D projects has been changed to iOS 4.0 since that is the minimum requirement for ARC. Yes, the good news is that ARC doesn’t require iOS 5! And fortunately for us much less than 5% of all devices aren’t yet (or are incapable of) running iOS 4. If you do want to support iOS 3 then you can just [disable ARC in your Kobold2D project](http://kobold2d.com/x/6QkO) and set the deployment target to iOS 3.1 in the Build Settings of your project.

#### Upgrading to ARC: no biggie!

Speaking of upgrading to ARC: Xcode 4.2 provides a conversion tool for legacy code. You can convert your project in Xcode by opening the **Edit** menu and choosing **Refactor -> Convert to Objective-C ARC…**. And the Box2D and Chipmunk template projects will help you [get ARC working with C/C++ code](http://www.kobold2d.com/x/rQkO). The required changes may not be immediately obvious but it is really simple once you know what to do (__bridge casts).

Please read the [Kobold2D: Working with Automatic Reference Counting (ARC)](http://www.kobold2d.com/x/kQkO) documentation before digging into ARCtic ARCheology. In particular if you have a [legacy Kobold2D project that you want to upgrade to ARC](http://www.kobold2d.com/x/sgkO) there are a few simple steps to follow to successfully enable ARC.

#### Library updates

**Chipmunk** (v6.0.2), **Chipmunk SpaceManager** (v0.1.2) and **Cocos3D** (v0.6.2) have all been upgraded to their latest versions. These are mainly maintenance releases, with the exception of Cocos3D which adds particle effects.

While updating I tried to figure out why the Mac OS X Chipmunk SpaceManager 64-Bit builds always froze at the first frame. I found the issue (patch submitted) and enabled 64-Bit Chipmunk SpaceManager builds. That means you can now also create 64-Bit ARC-enabled Chipmunk SpaceManager apps for Lion users.

#### Anything else?

One of the most commonly reported issues I received was that “the code builds successfully but it won’t run”. Although it turned out to be a problem of the “problem is sitting in front of the computer” kind, I made an effort to fix that.

Apparently there are users who don’t know how to change the Xcode build schemes. Well, unfortunately the default scheme selected in Kobold2D workspaces was “box2d-iOS” due to Xcode sorting the schemes alphabetically. Of course one can’t “build & run” a static library like Box2D, and it obviously won’t run. Fortunately I found a way to hide all the static library schemes from the user’s view. All new Kobold2D projects will now only list the project’s schemes, which means if you create a new project, it will run in all cases. This will also present a much simpler scheme selection which will be welcome by everyone.

Apart from that I made several bugfixes for iOS 3 related crashes (yes, iOS 3 is still supported) and a few bugfixes regarding the KKInput class. In particular the pan gesture’s translation property was incorrect.

As always you’ll find the complete list of changes in the [Preview 6 Release Notes](http://www.kobold2d.com/x/QAkO).

#### Try, Catch, Finally…

Happy game coding!

Also, here’s [food for thought](http://www.morewords.com/contains/arc/) if you’re seARChing for more ARC related puns. 😀

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

I think this is the most important feature of the kobold2d. I’m sure a lot of users will change to this framework after this release.

I done it on preview 2. 😉

[…] Kobold2D is giving retain, release and autorelease the finger! […]