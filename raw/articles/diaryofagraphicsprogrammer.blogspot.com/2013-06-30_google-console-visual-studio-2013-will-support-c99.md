---
title: Google Console / Visual Studio 2013 will support C99
url: http://diaryofagraphicsprogrammer.blogspot.com/2013/06/google-console-visual-studio-2013-will.html
author: Wolfgang Engel
published: '2013-06-30'
source_blog: Diary of a Graphics Programmer
source_site: http://diaryofagraphicsprogrammer.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Google making a console is an interesting news item. Like Apple they can utilize standard mobile phone parts and extend Android to support controllers.

What does it take to make this work:


1. High-end good looking apps: there is no need to have a fallback rendering path, so you can optimize until the last cycle

2. Dedicated section in the app store to highlight the controller-capable apps

3. The NDK needs to be better supported: I mentioned it here in the past, it is good that the NDK exists. This is the most important basic requirement to get existing tech to Android phones ...

4. A good controller with good support goes a long way ...


In other news, Visual Studio 2013 will finally support C99. This is something I always wished for, not only because C99 is a perfect game development language and mighty portable but also because open-source projects quite often favor C99 ... so now we can finally move our code base from C++ to C99 and it will still compile in a C++ environment like Visual Studio. For people who actually write engine code that is cross-platform or shared between teams, this is good news ...






What does it take to make this work:

1. High-end good looking apps: there is no need to have a fallback rendering path, so you can optimize until the last cycle

2. Dedicated section in the app store to highlight the controller-capable apps

3. The NDK needs to be better supported: I mentioned it here in the past, it is good that the NDK exists. This is the most important basic requirement to get existing tech to Android phones ...

4. A good controller with good support goes a long way ...

In other news, Visual Studio 2013 will finally support C99. This is something I always wished for, not only because C99 is a perfect game development language and mighty portable but also because open-source projects quite often favor C99 ... so now we can finally move our code base from C++ to C99 and it will still compile in a C++ environment like Visual Studio. For people who actually write engine code that is cross-platform or shared between teams, this is good news ...

## 3 comments:

Why would you want to port from C++ to C(99)? The tendency is to do the opposite.

Why are you porting from C++ to C? People usually do the opposite. Sometimes when I'm working with C++ I feel like I should be working with C, but the reverse also happens.

If you think of a typical game development team. There is high pressure, all the code needs to perform very well and errors can delay development and shipment of a game.

I consider C99 a better option under those circumstances. Obviously I work with a C / C++ code base all the time when working on other people's code bases and our own is also still C / C++, although we should be able switch to C easily.

Post a Comment