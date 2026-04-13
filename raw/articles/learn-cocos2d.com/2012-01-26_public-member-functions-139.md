---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_timer/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CCScheduler.h>`


| id |
|

Light weight timer

| id CCTimer::initWithTarget:selector: | ( | id | t, |
| [selector] SEL | s |
||
| ) | ` [virtual]` |

Initializes a timer with a target and a selector.

| id CCTimer::initWithTarget:selector:interval: | ( | id | t, |
| [selector] SEL | s, |
||
| [interval]
|

` [virtual]`

Initializes a timer with a target, a selector and an interval in seconds.

| id CCTimer::timerWithTarget:selector: | ( | id | t, |
| [selector] SEL | s |
||
| ) | ` [static, virtual]` |

Allocates a timer with a target and a selector.

| id CCTimer::timerWithTarget:selector:interval: | ( | id | t, |
| [selector] SEL | s, |
||
| [interval]
|

` [static, virtual]`

Allocates a timer with a target, a selector and an interval in seconds.