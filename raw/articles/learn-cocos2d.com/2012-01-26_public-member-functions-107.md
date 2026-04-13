---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_action_interval/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CCActionInterval.h>`


| id |
|

An interval action is an action that takes place within a certain period of time. It has an start time, and a finish time. The finish time is the parameter duration plus the start time.

These [CCActionInterval](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_action_interval/) actions have some interesting properties, like:

For example, you can simulate a Ping Pong effect running the action normally and then running it again in Reverse mode.

Example:

[CCAction](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_action/) * pingPongAction = [[CCSequence](http://www.learn-cocos2d.com/) actions: action, [action reverse], nil];

| BOOL CCActionInterval::isDone | ( | ) | ` [virtual]` |

how many seconds had elapsed since the actions started to run.