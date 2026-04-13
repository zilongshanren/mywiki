---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone-mac/html/interface_c_c_transition_scene/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CCTransition.h>`


| id |
|

Base class for CCTransition scenes

| void CCTransitionScene::finish | ( | ) | ` [virtual]` |

called after the transition finishes

| void CCTransitionScene::hideOutShowIn | ( | ) | ` [virtual]` |

used by some transitions to hide the outter scene

initializes a transition with duration and incoming scene

| id CCTransitionScene::transitionWithDuration:scene: | ( |
|

` [static, virtual]`

creates a base transition with duration and incoming scene