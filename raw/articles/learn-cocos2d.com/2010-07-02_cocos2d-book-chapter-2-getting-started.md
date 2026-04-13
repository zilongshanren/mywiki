---
title: 'cocos2d Book, Chapter 2: Getting Started'
url: http://www.learn-cocos2d.com/2010/07/cocos2d-book-chapter-2-started/
author: Josh Butterworth says
published: '2010-07-02'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

[I’m writing a Book: Learn iPhone and iPad Cocos2D Game Development](http://www.learn-cocos2d.com/2010/07/book-learn-iphone-ipad-cocos2d-game-development/)

[cocos2d Book, Chapter 3: Essentials](http://www.learn-cocos2d.com/2010/07/cocos2d-book-chapter-3-essentials/)

### Chapter 2 - Getting Started

This chapter starts with the usual prerequisites. Download and install iPhone SDK and cocos2d. Installing cocos2d Templates. Creating the first project from a cocos2d project template.

From what I already wrote I estimate that will be about one third of the chapter. I think what would be most interesting in this chapter is to talk about general code structure of cocos2d projects. The basic elements like Scenes, Layers and Nodes. How to transition from one screen to another, to see that we’re actually doing something cool with little effort. For that I think the scheduled selectors should also be introduced to time transitions, and one screen might be a Layer which is waiting for touch input to advance to the next screen.

It might also be a good place to discuss cocos2d memory management, like static autorelease initializers, and making sure dealloc gets called when you switch scenes - otherwise you’re obviously having a memory leak.

The goal is to get the reader into a position where he feels comfortable laying out a screen structure in cocos2d. He knows how to initialize objects and how to add and remove them from the scene. The foundation of working with cocos2d if you so will.

### What do you think should be in Chapter 2?

Let me know if you think I’m missing anything important. If you don’t have any suggestions then just think about what you would expect from the chapter by reading this description, that might give you some thoughts.

Also I would welcome any tips and the common pitfalls first-time cocos2d developers might trap themselves into. Expert tips are also welcome, those little nasty things or habits which could bite you later on if you don’t consider them from the beginning.

I’m looking forward to your feedback! The earlier the better. Chapter 2 will be submitted next Friday, July 9th.

### What’s planned for the Chapter after this one

Just to put Chapter 2 in context, for Chapter 3 I’m planning to talk about essential cocos2d classes and processes. Sprites, Labels, Menus, Actions, etc. It’ll show you how to work with them using small code snippets. The chapter will probably have a “reference” character with various code samples, so that experienced users feel comfortable skipping ahead while beginners still find it easy and encouraging to pick up the details.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

[actions](http://www.learn-cocos2d.com/tag/actions/)•

[apress](http://www.learn-cocos2d.com/tag/apress/)•

[autorelease](http://www.learn-cocos2d.com/tag/autorelease/)•

[book](http://www.learn-cocos2d.com/tag/book/)•

[cocos2d](http://www.learn-cocos2d.com/tag/cocos2d/)•

[code](http://www.learn-cocos2d.com/tag/code/)•

[code structure](http://www.learn-cocos2d.com/tag/code-structure/)•

[dealloc](http://www.learn-cocos2d.com/tag/dealloc/)•

[expert](http://www.learn-cocos2d.com/tag/expert/)•

[expert tips](http://www.learn-cocos2d.com/tag/expert-tips/)•

[feedback](http://www.learn-cocos2d.com/tag/feedback/)•

[iphone sdk](http://www.learn-cocos2d.com/tag/iphone-sdk/)•

[memory leak](http://www.learn-cocos2d.com/tag/memory-leak/)•

[memory management](http://www.learn-cocos2d.com/tag/memory-management/)•

[Menus](http://www.learn-cocos2d.com/tag/menus/)•

[pitfalls](http://www.learn-cocos2d.com/tag/pitfalls/)•

[Project](http://www.learn-cocos2d.com/tag/project/)•

[project template](http://www.learn-cocos2d.com/tag/project-template/)•

[sample](http://www.learn-cocos2d.com/tag/sample/)•

[SDK](http://www.learn-cocos2d.com/tag/sdk/)•

[tip](http://www.learn-cocos2d.com/tag/tip/)•

[Tips](http://www.learn-cocos2d.com/tag/tips/)•

[touch input](http://www.learn-cocos2d.com/tag/touch-input/)•

[transition](http://www.learn-cocos2d.com/tag/transition/)•

[user](http://www.learn-cocos2d.com/tag/user/)

Sounds good to me Steffen! The one thing i’d like to see from the getting started chapter is good code structure even in the initial ‘getting stuff on screen’ stage.

From my own experience in the cocos community a lot of the samples and tutorials just ask you to do all your coding in the HelloWorldScene class (mostly in the init method itself), the consequence being that when you’ve finished coding its difficult to know how to apply what you’ve learned to a bigger project without making a huge mess in your code base (this is especially true for people new to objective C).

Hi Josh, that’s exactly what I’m planning to do. I want to keep an eye on teaching good coding practices as well without sacrificing ease of use.

I agree with Josh, please consider reuse of your code. Also include the changes needed when migrating code into a new/separate project.

Also, regarding memory leaks, consider including the steps needed to identify and fix memory leaks.

+ Bitmap fonts, or how to integrate open source true type fonts into a game

+ The book should cover at least 1 project, say a space shoot-em-up complete with high scores, core data storage vs sqllite storage. I learn better with a project than theory.

I do too, so I have at least 3 games planned, or at least the starting points for the games. A sidescroller like Zombieville, the almost unavoidable jumping game and one game that uses physics.

hey man

i just bought your book of pre-lelease

because i saw a lot of things i wanted to learn like side scrolling games and stuff

lets hope its worth the money

I have also purchased the pre-release of the book. Is there a place to download the Xcode projects you refer to in the book? I am in chapter 3 now and you mention the Essentials Xcode project and the NodeHierarchy project.

Thanks,

-Greg

I bought your book and have gone through Chapter 2, it seems that

self.isTouchEnabled = YES;

(doesn’t work for me)

Instead I have to do

#include “CCTouchDispatcher.h”

then in the init() I put in

[CCTouchDispatcher sharedDispatcher] addTargetedDelegate:self priority:0 swallowsTouches:YES];

And as for the ccTouchBegan I had to change that to (BOOL) instead of (void)

I’m using cocos2d v0.99.4

self.isTouchEnabled = YES only works if the class it’s used in is a CCLayer or derived from it. The alternative is ok because any class can receive touch input.

The touch dispatcher knows two types of delegates: standard and targeted touch delegates. Depending on which you use you need either the -(BOOL) ccTouchBegan (targeted) or -(void) ccTouchesBegan (standard). Notice the plural “touches” in the latter method.

Thanks GamingHorror, I got confused and used the ccTouchBegan instead of the ccTouchesBegan , no wonder it wasn’t working!