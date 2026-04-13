---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone-mac/html/interface_c_c_progress_timer/
published: '2011-12-15'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CCProgressTimer.h>`


| id |
|

CCProgresstimer is a subclass of [CCNode](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone-mac/html/interface_c_c_node/). It renders the inner sprite according to the percentage. The progress can be Radial, Horizontal or vertical.

| id CCProgressTimer::initWithFile: | ( | NSString * | filename | ) | ` [virtual]` |

Initializes a progress timer with an image filename as the shape the timer goes through

Creates a progress timer with the texture as the shape the timer goes through

| id CCProgressTimer::progressWithFile: | ( | NSString * | filename | ) | ` [static, virtual]` |

Creates a progress timer with an image filename as the shape the timer goes through

Creates a progress timer with the texture as the shape the timer goes through

float CCProgressTimer::percentage` [read, write, assign]` |

Percentages are from 0 to 100

CCProgressTimerType CCProgressTimer::type` [read, write, assign]` |

Change the percentage to change progress.