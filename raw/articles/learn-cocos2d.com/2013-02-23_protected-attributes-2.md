---
title: Protected Attributes
url: http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone-extensions/html/struct_h_k_t_m_x_anim_rule/
published: '2013-02-23'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

|
cocos2d-iphone-extensions
0.2
Cocos2D Extensions API Reference (iOS version) for www.kobold2d.com developers
|

`#import <HKTMXLayer.h>`


|

Represents a tile animation state. When animClock == 0.0, each tile is in a state equal to its GID. After entering a state, a tile will look up the AnimRule for that state, wait `delay`

seconds, and then switch to state `next`

. If `next`

is zero, it will stay in the state forever.

As an optimization, `cycleTime`

and `last`

provide information about the complete animation starting at this state. If `last`

is zero, it is an endless loop with a period of `cycleTime`

seconds. If `last`

is nonzero, it will reach state `last`

and terminate in a total of `cycleTime`

seconds.