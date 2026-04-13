---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_transition_page_turn/
published: '2013-02-23'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

![]() |
cocos2d-iphone
2.1
Improved Cocos2D API Reference (iOS version) for www.kobold2d.com developers
|

`#import <CCTransitionPageTurn.h>`


| (id) | -
|

[CCTransitionPageTurn](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_transition_page_turn/) transition. A transition which peels back the bottom right hand corner of a scene to transition to the scene beneath it simulating a page turn

This uses a 3DAction so it is strongly recommended that depth buffering is turned on in [CCDirector](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_director/) using:

[[[CCDirector](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_director/) sharedDirector] setDepthBufferFormat:kCCDepthBuffer16];

creates a base transition with duration and incoming scene if back is TRUE then the effect is reversed to appear as if the incoming scene is being turned from left over the outgoing scene

creates a base transition with duration and incoming scene if back is TRUE then the effect is reversed to appear as if the incoming scene is being turned from left over the outgoing scene