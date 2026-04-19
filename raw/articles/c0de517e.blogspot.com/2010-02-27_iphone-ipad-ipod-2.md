---
title: iPhone iPad iPod
url: https://c0de517e.blogspot.com/2010/02/iphone-ipad-ipod.html
published: '2010-02-27'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

I'm lazy. The iPlatforms are incredibly cool, even if I own only a lowly iPod touch I have to say, it's an impressive product. But I'm lazy.

I don't really care about jumping on the appstore bandwagon, but I'd like to make a few experiments. But in order to make those, I really would like not to have to learn ObjectiveC. I know, that's a problem that a lot of developers have.

I know that ObjectiveC is not bad, maybe it's even better than C++, but it's not interesting enough for me to study as a language, and it's different enough from everything I've played with not to be able to write stuff without reading the documentation...

So I went on for a quest to find a C or C++ example, or library, or something that I could start fiddling with. Of course that's stupid, I could have invested the same time to learn the rudiments of ObjectiveC, but anyway...

The first insight you have to get is that actually ObjectiveC/C++ can compile C/C++ code. So really, you can take the basic OpenGL project provided with XCode, and fiddle with it even just working with C.

[This post](http://www.ignaciosanchezgines.com/2009/08/27/iphone-and-c-opengl-programming/)shows how to convert the template project into something that works with C++.Simple, but what if you want also to create widgets, play with the touch controls and so on, without calling ObjectiveC functions?

Well, there's not much around, but I think, there is enough to start playing. The most useful library that I've found is

[openFrameworks](http://www.openframeworks.cc/). It has an iPhone port, it's C based, and provides a very easy access to OpenGL.[Oolong](http://code.google.com/p/oolongengine/)engine has some very nifty arm assembly snippets. Very worth a look, the arm VPU is peculiar and fun.

I would also love to hack the iPhone using C#. Unfortunately,

They leverage on the javaScript processing port, that uses the (cool) HTML5 canvas element.

[monoTouch](http://monotouch.net/)is commercial only. There are even two (unrelated afaik) incredibly cool hacks to run processing ([.js](http://processingjs.org/)) on the iPhone.They leverage on the javaScript processing port, that uses the (cool) HTML5 canvas element.

## 5 comments:

Hi, I'm like you, looking for C/C++ alternative for iPhone dev. I know many ppl will say we are lazy. I admit too but either I do find one interesting solution. Check out AirPlay SDK. It directly compile C/C++ projects to iPhone executable. Pretty exciting for us! :D

There is also SDL 1.3 version that support iPhone.

All commercial stuff though. oF is the only free one.

I write my iGame entirely in C++. In order to hook my "engine" to Objective-C I used approach described here:



http://iphonedevelopertips.com/cpp/c-on-iphone-part-1.html

(There are 3 parts.)

In two words: Obj-C able to call C-functions. So, you create .h file where you place C-style function declarations and .cpp file where you redirect function calls to C++ part.

Use of this scheme is pretty straightforward. I create a new iPhone project from iPhone/OpenGL template and insert "bridge" calls into a few places. And that's it.

Keeping most of your logic in C++ is fine... but I'm not sure you are saving yourself any effort by not learning objective-c.




It's not that complicated of a language... I actually learned objective-C before I learned C++, and it was like 1/100th the effort.

I think you may be assuming it will be more difficult than it is by comparison with having learned C++. You can probably become proficient at objective-C over a weekend.

http://www.otierney.net/objective-c.html

Post a Comment