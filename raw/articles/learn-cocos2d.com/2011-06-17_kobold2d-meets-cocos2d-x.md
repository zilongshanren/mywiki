---
title: Kobold2D Meets Cocos2D-X
url: http://www.learn-cocos2d.com/2011/06/kobold2d-meets-cocos2dx/
author: Walzer says
published: '2011-06-17'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

[Kobold2D](http://www.kobold2d.org/) is well and alive. Actually so much so that I thought: “Hey, it’s crazy, but maybe not … I’ll give it a shot and see how far I get.”

The thought was to try and add the [cocos2d-x engine](http://www.cocos2d-x.org/) (cocos2d in C++) together with the Hello World example project to the Kobold2D workspace. The result: it took about 90 minutes, most of that figuring out the correct build settings and header search paths. And it just worked.

Surprise! 😀

Right now this is just the iOS version. A cocos2d-x Mac project will be added as soon as the Mac platform is officially supported by cocos2d-x (or does it already and I missed that?). Then developers would have the choice between using either Objective-C or C++ as the primary language for developing their iOS & Mac OS X games.

It also made me think: “Hey, there’s this [other open source 2d game engine](http://www.sparrow-framework.org/) … hmmm….” ![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Official Mac support will take a long time

Only focusing mobile platforms make this project to improve faster.

I don’t believe Mac support is planned for cocos2d-x. See here: http://www.cocos2d-x.org/news/21

“Feature #449 Remove the sources for mac platform. We plan to focus on mobile platforms & reduce the complexity”

I don’t know whether that means they’ll also be removing support for Windows (I hope not).

Oh, didn’t expect a reply from the project founder. Maybe I shouldn’t have said it wasn’t planned.

I’m thinking a good design to deal with the complexity of opengles 1.1 / 2.0 / opengl, after then mac port can be done. But there’s no idea so far.

I hate #ifdef here and there. If we use #ifdef to split opengl & opengles just as cocos2d-iphone do, then #ifdef to split different platforms ios/android/win32/mac/airplay/wophone/meego, there will be 2 * 7 = 14 conditional judgments in many functions. It’s unacceptable. That’s the reason I remove opengl support currently. win32 port hasn’t been and will not be removed because powervr’s opengles1.1 library on it.

Agree on #ifdef and macros in general. If you can avoid them it’s always better not to. Introduces too many different code paths that all need to be tested individually.

I’m not sure what you meant by referring to Sparrow, but I really like it. Not as powerful as Cocos2D (lacks Tile map support last time I checked) but I prefer its way of doing things.

Cool! Will you add also add android support to kobold2d?

Hmmm … it depends on whether you can develop cocos2d-x android apps within Xcode. I haven’t checked that but a quick look showed me this project: http://alex.tapmania.org/2010/09/android-ndk-and-xcode.html