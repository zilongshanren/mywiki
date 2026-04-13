---
title: CCTransitionScene Class Reference
url: http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_transition_scene/
published: '2011-01-31'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#import "`

[CCTransition.h](http://www.learn-cocos2d.com/)"

Inherits [CCScene](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_scene/).

Inherited by CCTransitionCrossFade, [CCTransitionFade](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_transition_fade/), [CCTransitionFadeTR](http://www.learn-cocos2d.com/), [CCTransitionJumpZoom](http://www.learn-cocos2d.com/), [CCTransitionMoveInL](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_transition_move_in_l/), [CCTransitionPageTurn](http://www.learn-cocos2d.com/), [CCTransitionRadialCCW](http://www.learn-cocos2d.com/), [CCTransitionRotoZoom](http://www.learn-cocos2d.com/), [CCTransitionSceneOriented](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_transition_scene_oriented/), [CCTransitionShrinkGrow](http://www.learn-cocos2d.com/), [CCTransitionSlideInL](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_transition_slide_in_l/), [CCTransitionSplitCols](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_transition_split_cols/), and [CCTransitionTurnOffTiles](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_transition_turn_off_tiles/).

| (void) | -
|

Base class for CCTransition scenes

| - (void) finish |

called after the transition finishes

| - (void) hideOutShowIn |

used by some transitions to hide the outter scene

initializes a transition with duration and incoming scene

creates a base transition with duration and incoming scene