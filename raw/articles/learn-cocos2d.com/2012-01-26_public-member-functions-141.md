---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_twirl/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CCActionGrid3D.h>`


| id |
|

| id CCTwirl::actionWithPosition:twirls:amplitude:grid:duration: | ( | CGPoint | pos, |
| [twirls] int | t, |
||
| [amplitude] float | amp, |
||
| [grid]
|

` [static, virtual]`

creates the action with center position, number of twirls, amplitude, a grid size and duration

| id CCTwirl::initWithPosition:twirls:amplitude:grid:duration: | ( | CGPoint | pos, |
| [twirls] int | t, |
||
| [amplitude] float | amp, |
||
| [grid]
|

` [virtual]`

initializes the action with center position, number of twirls, amplitude, a grid size and duration

float CCTwirl::amplitude` [read, write, assign]` |

amplitude

float CCTwirl::amplitudeRate` [read, write, assign]` |

amplitude rate

CGPoint CCTwirl::position` [read, write, assign]` |

twirl center