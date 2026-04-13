---
title: Learn & Master Cocos2D Game Development
url: http://www.learn-cocos2d.com/knowledge-base/article-collection/
published: '2010-12-23'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

The cocos2d homepage - this should be obvious but since most people land on the google source code repository page for cocos2d iPhone instead of the real homepage www.cocos2d-iphone.org i wanted to post it here. Usually the most noteworthy threads from the forum as well as important blog posts by others are posted on the blog, and of course any new releases and updates to cocos2d.

cocos2d iPhone documentation - a post on the official website explains where you can find what kind of documentation.

Open GL ES 1.1 reference - only needed if you intend to do OpenGL programming - you don’t need to know about OpenGL if you’re using cocos2d but it may come in handy sometimes.

As for books, i can NOT recommend iPhone Games Projects by Apress. Repeat: not recommended! It’s a badly written collection of blog posts about the kind of games most game developers would not want to make (chess etc). It does not contain particularly good or reusable examples of code and the choice of projects is questionable to say the least. It has generally very little value for a cocos2d iPhone developer as all examples are either written in Cocoa Touch or plain OpenGL.

A list of editors useful for cocos2d development is described on the cocos2d’s homepage blog in two parts: part one and part two. It includes tile editors, Texture Atlas and Bitmap Font generators.

Finding memory leaks using the CLANG static analyzer. Don’t leak memory. That’s terrible. Read how you can run a program that tells you with impressive accuracy where there are memory leaks in your code, at least potential ones. Make sure you also read the comments further down since they contain more command line samples that fix some issues for iPhone OS 3.x among other things.

How to obtain the iPhone crashlogs from your beta-testers and costumers. And then there’s Apple’s manual on how to debug crashdumps. In short: always compile both debug and release builds at the same time, then keep both dSYM files and make sure you can later identify to which version and build they belong to. It’s easiest to use source control here and simply flag or label the version you used to create distributed Ad-Hoc or App Store versions with.

Specifically for linking to the App Store you will find Apple’s iTunes Link Maker useful. On Stackoverflow you can learn how to create links to your App that you can send via email. And finally, this Ars Technica article covers all the finer details of creating an App Store link that works for the iPhone’s App Store, including opening the App Store app with a search term - which is the only way to show all the apps of a particular company or developer on the iPhone’s App Store.

8 confusing Objective-C Warnings and Errors explains some of the more confusing things Xcode (actually: GCC) throws at you and leaves you wondering. After reading this article you’ll know what you’re dealing with the next time it comes up.

App Store Rejection reasons - be sure to go through this checklist before submitting your App to iTunes Connect to avoid your App being rejected due to some commonly made mistake or oversight.

How to build an IPA file from Xcode shows you how to setup a build target in Xcode that will output an IPA file. Those are very helpful for Ad-Hoc distribution of your App, as IPA files do not get as easily mangled (leading to errors such as “resources have been modified”), especially on Windows machines. It also makes installing Ad-Hoc builds easier since a simple double-click suffices to open iTunes and install the App. Plus it’ll have a proper icon in iTunes’ Application folder.

How to properly set your App’s iTunes Release Date and the things to watch out for. If you’re about to release an App you must read this otherwise you risk your App not being listed on the “What’s New” list.

How to calculate the App Store size of your iPhone App before approval. It’s not magic nor random, it can actually be calculated to within a rather small margin of error. The good thing is, the error will be that the calculation gives you the maximum size your App could possibly have on the App Store. With experience you’ll learn how good your Apps compress after approval, and that depends highly on the game engine used. Unity is hit especially hard by this, typically Unity apps get added another 4-5 MB to the zipped App you’re uploading, in some cases even more.

How to set and change the list of supported languages in iTunes: according to this post on Stackoverflow all you need is one localized file. What i do is, under Resources, i add a new .strings File and leave it empty. Then right-click, choose Get Info and on the General tab click “Make File Localizable”. Then go back to the General tab and click “Add Localization” until you’ve added all languages your App supports. Note that you do not have to reference or otherwise use that file in your code - it just needs to be there. If you look into your App Bundle (right click: Show Package Contents) you’ll notice that new folders like English.lproj, German.lproj etc. exist. Those are scanned by iTunes to create the supported languages list.

My iPhone & iPad Design Templates for OpenOffice Draw

Open Office Draw Templates for designing iPhone & iPad games. They offer you a canvas to create the visual elements of your game and pitch your ideas. I use them to pitch my ideas or create concept drawings of iPhone/iPad apps and games.

You can either use Open Office Draw to draw on them, or just print out the images and draw on it. Both versions have at least one image where the screen background is white, so you can easily draw on it. The iPad version also has a vector graphics representation, so if you worry too much about the completely dark space for printing - turn it into light gray or even transparent with just the border lines shown.

Download the iPad Design Template for OpenOffice Draw. For the iPad i took extra-care to scale the images to close to original size, and i also recreated the iPad as vector graphics in almost exact original size.

Hi! My name is Steffen Itterheim, I'm a freelance and Indie iPhone Game Developer. I was a Software Engineer, Manager and Game Designer at Electronic Arts Phenomic during my 10-year professional game industry career.

I'm happy to be an Indie and to be able to share my knowledge with you!

Please consider joining my email Newsletter so I can inform you about new Starter Kits, Game Components, Tutorials and major Knowledge Base updates: