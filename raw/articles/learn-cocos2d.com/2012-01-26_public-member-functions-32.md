---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_timer/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <b2Timer.h>`


|

Timer for profiling. This has platform specific code and may not work on every platform.

| b2Timer::b2Timer | ( | ) |

Constructor.

| float32 b2Timer::GetMilliseconds | ( | ) | const |

Get the time since construction or the last reset.

| void b2Timer::Reset | ( | ) |

Reset the timer.