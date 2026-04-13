---
title: Instance Methods
url: http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.2/cocos2d-iphone-mac/html/interface_c_c_action_interval/
published: '2013-06-05'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

|
cocos2d-mac
2.1
Improved Cocos2D API Reference (Mac OS X version) for www.koboldtouch.com developers
|

`#import <CCActionInterval.h>`


| (id) | -
|

| (id) | +
|

|

|

An interval action is an action that takes place within a certain period of time. It has an start time, and a finish time. The finish time is the parameter duration plus the start time.

These [CCActionInterval](http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.2/cocos2d-iphone-mac/html/interface_c_c_action_interval/) actions have some interesting properties, like:

For example, you can simulate a Ping Pong effect running the action normally and then running it again in Reverse mode.

Example:

[CCAction](http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.2/cocos2d-iphone-mac/html/interface_c_c_action/) * pingPongAction = [[CCSequence](http://www.learn-cocos2d.com/) actions: action, [action reverse], nil];

how many seconds had elapsed since the actions started to run.