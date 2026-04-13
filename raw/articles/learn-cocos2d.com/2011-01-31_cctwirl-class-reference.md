---
title: CCTwirl Class Reference
url: http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_twirl/
published: '2011-01-31'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#import "`

[CCActionGrid3D.h](http://www.learn-cocos2d.com/)"

Inherits [CCGrid3DAction](http://www.learn-cocos2d.com/).

| (id) | -
|

[CCTwirl](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_twirl/) action

| + (id) actionWithPosition: | (CGPoint) | pos |
||
| twirls: | (int) | t |
||
| amplitude: | (float) | amp |
||
| grid: | (
|

creates the action with center position, number of twirls, amplitude, a grid size and duration

| - (id) initWithPosition: | (CGPoint) | pos |
||
| twirls: | (int) | t |
||
| amplitude: | (float) | amp |
||
| grid: | (
|

initializes the action with center position, number of twirls, amplitude, a grid size and duration

- (float) amplitude` [read, write, assign]` |

amplitude

- (float) amplitudeRate` [read, write, assign]` |

amplitude rate

- (CGPoint) position` [read, write, assign]` |

twirl center