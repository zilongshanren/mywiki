---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/2.0/cocos2d-iphone/html/interface_c_c_action_interval/
published: '2012-09-22'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

|
cocos2d-iphone
2.0
Improved Cocos2D API Reference (iOS version) for www.kobold2d.com developers
|

`#import <CCActionInterval.h>`


| (id) | -
|

An interval action is an action that takes place within a certain period of time. It has an start time, and a finish time. The finish time is the parameter duration plus the start time.

These [CCActionInterval](http://www.learn-cocos2d.com/api-ref/2.0/cocos2d-iphone/html/interface_c_c_action_interval/) actions have some interesting properties, like:

For example, you can simulate a Ping Pong effect running the action normally and then running it again in Reverse mode.

Example:

CCAction * pingPongAction = [CCSequence actions: action, [action reverse], nil];