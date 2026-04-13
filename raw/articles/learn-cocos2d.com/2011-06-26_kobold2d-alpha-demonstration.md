---
title: Kobold2D (Alpha) Demonstration
url: http://www.learn-cocos2d.com/2011/06/kobold2d-alpha-demonstration/
author: Yehnan Says
published: '2011-06-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

I recorded a screencast to give you a first impression of the current alpha version of [Kobold2D](http://www.kobold2d.org/). I’ll show you what is is, what it includes (so far) and how it improves the cocos2d development process.

Since recording the screencast I’ve added the Doodle Drop project from the book as an iOS game template project. I also added the Box2D & Chipmunk physics projects from the book and improved them to work on both iOS and Mac OS X.

##### Update

Here’s a screenshot showing the current list of template projects (Hello Kobold2D, Hello Cocos3D, Hello Cocos2D-X, Physics Box2D, Physics Chipmunk, Physics Chipmunk SpaceManager, Doodle Drop) and the Doodle Drop template running:

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

very impressive, good to see the progression. When will you release to me?![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


ETA July/August

Did you manage to create the Kobold2d Xcode 4 templates ? I remember you had some problems with that in the past, how did you solve the issue ?

The new Xcode 4 Template system is on one hand more powerful but at the same time tedious to edit, particularly if you don’t have any tool support to create them. And the new template system doesn’t support some crucial features like copying all files of the template, even if they’re not included in the project itself, as well as not being able to create workspaces or references to other .xcodeproj files.

I solved it by showing Apple the finger.![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


I’m writing a tool that allows you to start a new project by creating a copy of one of the template projects in Kobold2D. It’s essentially the same process (pick template, enter name, start coding), except that you have to launch an App instead of going through the File-New-New Project menu.

I’ve been working hard on a Template creator script that could simplify some of the work. I started off the cocos2d template creation tool, it still needs a lot of work:

https://github.com/MrGando/Xcode-4-Template-Generator

The main idea is to use the script from a meta “template build” script in your daily builds or whatever.

Cheers

I think that’s a great idea!

Although it won’t fix the problems with referencing other projects in project templates. Fortunately I’ve made good progress with the Kobold2D Project Starter app.

hey, it would be really great if kobold2d will include an obj-c wrapper for box2d, if it’s possible 😛

Yes, that would be great and it’s possible. Just needs someone to take the time and write the code. Not something you can do over a weekend.

Hi Steffen,

looks promising!

I wonder how easy it will be to update to a newer version of cocos2d or are you trying to keep Kobold2D in sync yourself with every release?

I plan to update Kobold2D with every new cocos2d release.

Hi Steffen,

Amazing stuff here! Can’t wait to play with this baby!