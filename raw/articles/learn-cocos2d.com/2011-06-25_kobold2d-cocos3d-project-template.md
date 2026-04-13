---
title: 'Kobold2D: Cocos3D Project Template'
url: http://www.learn-cocos2d.com/2011/06/kobold2d-cocos3d-project-template/
author: Sam says
published: '2011-06-25'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Today I completed the first draft of the [Kobold2D](http://www.kobold2d.org/) chapter which will be in the second edition of the [Learn Cocos2D book](http://www.apress.com/book/view/9781430233039). In that chapter I’m also giving you an introduction to [cocos3d](http://brenwill.com/cocos3d/), the official 3D add-on library for cocos2d. I ported cocos3d’s Xcode project template to Kobold2D and spiced it up a little with some cocos2d nodes in the back- and foreground:

*Notice the “incoming network connection” warning. This is caused by the iSimulate library which is distributed with Kobold2D and activated by default for Simulator builds. You still need to buy the iSimulate App to benefit from it though. If you don’t you can also choose to ignore the dialog or simply disable iSimulate by commenting out a line in the project’s BuildSettings-iOS.xcconfig file.*

I’ve also had great fun with the augmented reality option that the cocos3d CCNodeController class provides. And setting it up is one line of code. Here’s the “camera as live background” demo in action:

Since a picture doesn’t really do it justice, here’s a video:

Admittedly it could run a little faster on my iPhone 3G. It’s pretty taxed and averages around 20 fps with the camera background view and rendering a 3D model. My iPod Touch 4 averages at around 40 fps and it feels a lot smoother.

#### Kobold2D Todo List

One of the biggest items on my todo list for Kobold2D is to design the [website](http://www.kobold2d.org/) and get rid of the “coming soon” page. This includes setting up the wiki and filling it with content, documentation for the most part. And, well, paying $150 each month because I don’t see any alternative to using [Confluence](http://www.atlassian.com/software/confluence/). I want to enjoy working on documentation, and I want you to enjoy browsing and reading it.

I also want to create more template projects. Currently, as you can see in the first screenshot, there’s Hello Kobold2D (iOS & Mac), Hello Cocos3D (iOS) and Hello Cocos2D-X (iOS). I want to add two more templates, one for Chipmunk with SpaceManager (iOS & Mac) and one for Box2D (iOS & Mac). I also want to add the projects from my book as project templates, namely Doodle Drop, the Shoot ’em Up game, the Orthogonal and the Isometric Tilemap projects, and the Cocos2D With UIKit project (all iOS).

Even though Kobold2D won’t have Xcode 4 Project Templates I still want to give you a quick and easy way start a new project based on one of the template projects. Notice the distinction between “project template” (those in Xcode’s New Project dialog) and “template project” (a regular, already existing project). I started writing a tool that allows you to create a copy of an existing Kobold2D template project and rename it, so that the workflow is just as convenient as doing it within Xcode. It works for the specific template I tested it with, but I still have to design the user interface and make the code fail-safe.

*In case you wonder why Kobold2D won’t have Xcode Project Templates: they are not nearly as powerful as they would have to be. And they’re a pain in the rear to create and maintain without some tool support. But worst of all, you have no way of including files in an Xcode 4 project template that must not be added to the Project Navigator. Like, for example, .xcodeproj files.*

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

This looks fantastic, just what I’m trying to do at the moment. Any chance you feel like sharing the source (presuming your book isn’t coming out today or tomorrow - for the impatient) or even a pointer on how to overlay the 3d on video feed background. I can get just a video feed background, and I can get just a 3d cocos 3d ‘hello world’ thing going, but can’t seem to overlay 3D onto camera feed background.

Again, nice work!

You can check this out in Cocos3D. If you use its CCNodeController class (see the Xcode template project) then enabling the live video background is just a single line of code. It’s a property of the CCNodeController class that you need to set to YES.

I did this and it works like a charm

Hi,

Thanks for your work.

you see the frame rate(i can see this in video)? i thinks its very low…….can you describe why?

Thank

The test was done with an iPhone 3G which was pushed to its limit with rendering the live camera background and a 3D model. Enabling the camera consumes a lot of performance.

Hey Steffen,

I wanted to use the Cocos3D templates and I was wondering how you ported cocos3d with Kobold2D. I was wondering if following the usual plug-in instruction for cocos2D hook-up would work the same if I place the downloaded cocos3d into the _Kobold2D_/cocos3d directory. If not, how should I do it?

Thank you very much in advance.

I “simply” added the cocos3d source code as a static library to Kobold2D. If you know how to create a static library (basically: create new static library target, add the cocos3d code to it, done) what remains is to link the target with the library and adding the Header Search Path to Build Settings.

I have since removed cocos3d from Kobold2D because it’s not compatible with cocos2d 2.x and it’s hardly being used. If you want 3D you may be better off looking at the other game engines that excel in 3D rendering (Unity, SIO2, etc.). Mainly because for 3D game development you are much more in need for design tools and a good workflow. Especially the latter is a problem with cocos3d since it only supports the POD file format. You may find it time consuming to convert assets to POD every time you make a change.

Hey Steffen,

By any chance do you know how to make a 3DBox in cocos3D?

I tried this code:

CC3BoundingBox bounds = makeBounds(9.5, 5.0, 4.0, 0, 0, 0);

CC3MeshNode *cube = [[CC3MeshNode alloc] init];

[cube populateAsSolidBox:bounds];

but didn’t work for me. I placed it in the _DTestingScene.m -initializeScene method. Is this correct or did I not implement it correctly?Any advice would be much appreciated.

Thank You,