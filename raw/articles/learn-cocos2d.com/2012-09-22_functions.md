---
title: Functions
url: http://www.learn-cocos2d.com/api-ref/latest/Kobold2D/html/_k_k_main_8h/
published: '2012-09-22'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

|
Kobold2D
1.1
Kobold2D API Reference (iOS version) for www.kobold2d.com developers
|

`#import "cocos2d.h"`

`#import "cocos2d-extensions.h"`

`#import "kkLuaInitScript.h"`

| int |
|

Contains the common and platform-specific startup code. Launches the Lua interpreter via Wax.

KKMain handles the cross-platform startup of Kobold2D projects as well as the initialization of Wax and Lua. Kobold2D projects call this method in their main(..) method. The parameters are meant for future expansion in case additional per-app startup parameters need to be passed in which must be set before the AppDelegate takes over.