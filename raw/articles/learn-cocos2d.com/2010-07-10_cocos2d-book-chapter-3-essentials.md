---
title: 'cocos2d Book, Chapter 3: Essentials'
url: http://www.learn-cocos2d.com/2010/07/cocos2d-book-chapter-3-essentials/
author: Choong Hong Cheng says
published: '2010-07-10'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

### Chapter 3 - Essentials

This chapter is a reference about the fundamental classes of cocos2d and how to use them. Nodes, Layers, Scenes, Labels, Sprites, Transitions, Actions, you name it. Also CCDirector, SimpleAudioEngine and other often used singleton classes as well. More advanced concepts will be discussed in a later chapter, Spritesheets for example.

The submission of the first chapter draft is due next Friday, July 16th.

### What do you think should be in Chapter 3?

Do you know a cocos2d class or process that you think is essential and should be discussed in this chapter? Let me know!

### Summary of working on Chapter 2 - Getting Started

For one I detailed the Hello World sample project and made a simple modification using touch input. At the same time at least some basic level of understanding about cocos2d classes was introduced but the gist of it is done in Chapter 3. In addition, there were a lot of theoretical aspects I wanted to discuss as well, most of all Memory Management and available memory as well as setting expectations on testing on Simulator vs. a device. And of course the devices and their subtle differences. I do hope that those kind of details are appreciated even if they’re not 100% related to cocos2d. I regularly see cocos2d developers struggling with memory issues, with unexpected differences on the device vs the Simulator, or comparing framerates of the Simulator and possibly even Debug builds. That made me want to stray off the beaten path for a moment to hopefully save the readers some misconceptions and the pain associated with them.

I also realized how many steps a new developer has to go through and how much there is to learn in case you’ve never been working with the iPhone SDK before. It starts with registering as iPhone developer and doesn’t end with installing the SDK because you also need the provisioning profiles, a much discussed and troublesome feature. For all of this I refered to existing (and excellent) Apple documentation. Typically the processes change with each new iPhone SDK or may even be under NDA, so discussing how all of this works with iPhone SDK 4 wouldn’t be a good idea since shortly after the book is out iPhone SDK 5 may be coming, introducing changes to the Developer Portal and iTunes Connect with it. It did get me the idea, and I know others have it too, that we need some holding-hands Tutorial which takes one through the steps from registering as iPhone Developer to publishing one’s first App, by referring to the correct official documentation for each step while not forgetting about common pitfalls that are not in the official docs.

I also noticed how easy it can be to overlook how you suddenly introduce a new concept without explaining it first. And then you have to decide how much information is necessary to introduce the concept without straying too far away from what you want to talk about in the first place. It’s especially hard for me because I tend to want to explain everything in detail but some things have to be left for a later discussion. I’m looking forward to editorial feedback now. It has helped tremendeously for the first chapter and I learned a lot from the Apress editorial staff, so I find it exciting that the experts point me to the flaws and make suggestions, I go in to fix them and then see how much better it is. That’s how I like to learn things and it’s going to be one of the core concepts of the book. Show how it’s done, how it shouldn’t be done (if it’s often done wrong) and how it can be done even better if you want to avoid trouble in the long run, while explaining why.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Do like you book about cocos2d, just wondering whether you can add more info about accelerometer part especially about low-pass filter and high-pass filter.

More info about it at http://developer.apple.com/iphone/library/documentation/EventHandling/Conceptual/EventHandlingiPhoneOS/MotionEvents/MotionEvents.html

Think is pretty usefully to isolate the gravity component. Building a Raiden type of game with cocos2d now and I find it important to isolate the gravity to get the X and Y movement. Let me know what you think about it ?

Hong Cheng

Thanks, that is an interesting topic indeed! And easily overlooked that there’s a concept called gravity affecting accelerometer data. At least I should make a Note box and point to the link for further information.

Don’t mention it![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


One area that needs a lot more documentation is the spatial characteristics of the node hierarchy.

The relationship between bounds, frames, contentSize, scale etc. Which to change when, and the side effects and implications of changing each. How they are modified (if at all) by parent nodes. Do nodes “shrinkwrap” their bounds around their children? Questions like that.

Some discussion view hierarchy debugging techniques would be great, too. Such as how to determine why child nodes aren’t being displayed at the size/position you expect.

You and everyone else seems to use scenes sparingly, hard-coding them in your classes. For example, in your chapter 3 source code, when you go to the menu scene, you have a button to go back to the HelloWorld scene:

[[CCDirector sharedDirector] replaceScene:[HelloWorld scene]];

But what if I want to have say 10 scenes and move between them with a swipe or navigation arrows? I don’t want to hard code the forward and back scenes in each scene. It would be better to have some kind of scene manager, sort of like a master scene with the other inside it.

Is it possible to have somewhere outside of the scenes:

CCArray NextSceneArrayOfScenes = @”Scene00″, @”Scene01″, @”Scene02″;

chosenScene += 1; // user nagivates forward

CCScene* nextScene = [NextSceneArrayOfScenes objectAtIndex:chosenScene];

[[CCDirector sharedDirector] replaceScene:[nextScene scene]];

Or would you use layers/nodes instead, and just move them to the side, simulating a scene change?

When people make a magazine or something, how is each page handled, as a scene or as layers/nodes ?

I found a tutorial for a sceneManager.

http://www.iphonegametutorials.com/2010/09/07/cocos2d-menu-tutorial-part-2/

It’s pretty clever, creating a layer and wrapping it in a scene and returning it to be the new scene.

It could be modified so that the sceneManager has an array of all possible scenes, and the scene that calls the sceneManager could send a number based on the current position (say if you are doing a magazine or something where scenes are the equivalent of “pages”).

However, something with 50 pages would probably need to be handled even more efficiently, where the pages are somehow generated dynamically, also loading the content dynamically.