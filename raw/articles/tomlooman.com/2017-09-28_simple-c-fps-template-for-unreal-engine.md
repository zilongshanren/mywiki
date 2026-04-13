---
title: Simple C++ FPS Template for Unreal Engine
url: https://tomlooman.com/unreal-engine-cpp-fps-template/
author: Tom Looman
published: '2017-09-28'
source_blog: Tom Looman
source_site: https://www.tomlooman.com/
category: unreal engine
fetched: '2026-04-13'
---

As I have been preparing some Unreal Engine C++ tutorials, I wanted to use the Built-in C++ FPS Template that ships with the engine as a base project and found it has VR and Touch-input code in the character class which don’t serve any purpose unless you are interested in VR and/or mobile. Since I needed a super simple C++ template to not scare people away from learning this language, I decided to create a simplified version with only the essentials for non-VR projects and make it available to all on [GitHub](https://github.com/tomlooman/SimpleFPSTemplate).

To give you an idea of the changes I made, the Character class is about 1/3 the size in code compared to the built-in FPS Template with the same functionality and several unnecessary coding concepts stripped out (such as a few UPROPERTY meta keywords you don’t need to know as a newbie). The purpose of all this is to make it less intimidating to start using C++ with Unreal Engine.

You may also be interested in some of my other [C++ Tutorials](https://tomlooman.com/unreal-engine-cpp-tutorials) such as [Using Timers in C++](https://tomlooman.com/unreal-engine-cpp-timers) or my [C++ Complete Guide](https://tomlooman.com/unreal-engine-cpp-guide)!