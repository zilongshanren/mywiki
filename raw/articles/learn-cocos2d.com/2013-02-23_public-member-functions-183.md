---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_scene/
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

`#import <CCScene.h>`


| (id) | -
|

[CCScene](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_scene/) is a subclass of [CCNode](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_node/) that is used only as an abstract concept.

[CCScene](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_scene/) an [CCNode](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_node/) are almost identical with the difference that [CCScene](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_scene/) has its anchor point (by default) at the center of the screen.

For the moment [CCScene](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_scene/) has no other logic than that, but in future releases it might have additional logic.

It is a good practice to use and [CCScene](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_scene/) as the parent of all your nodes.

initializes a node. The node will be created as "autorelease".

Implements [CCNode](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_node/#ad789cad83aca65c130abd4452d1bc081).

Implemented in [CCTransitionTurnOffTiles](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_transition_turn_off_tiles/#a002e9740f8487af7afd9fe157e99dfcc), [CCTransitionCrossFade](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_transition_cross_fade/#a84e566a9c1ef713de1deaf006b6dbd0f), [CCTransitionZoomFlipAngular](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_transition_zoom_flip_angular/#aff9352d756a5f4688bac73395eed9c90), [CCTransitionZoomFlipY](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_transition_zoom_flip_y/#a5ca9edd127622a0d25322dde9daf7447), [CCTransitionZoomFlipX](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_transition_zoom_flip_x/#a29c33d700630ff1e7b83ad4ba501935b), [CCTransitionFlipAngular](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_transition_flip_angular/#acfbd2cd5d83cccb25e8566f39502df7e), [CCTransitionFlipY](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_transition_flip_y/#a89a277a0795c44498c0dcdd0d15ffd78), [CCTransitionFlipX](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_transition_flip_x/#a826655c1f01b1edf2aaa7663544bc69c), [CCTransitionShrinkGrow](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_transition_shrink_grow/#aaa4d30491aec84748cf226918abd2987), [CCTransitionJumpZoom](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_transition_jump_zoom/#a520ada27cbde20c1b27c81d2bfbcd74a), and [CCTransitionRotoZoom](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_transition_roto_zoom/#a588b1d67980b94489bed54922ae3eb2a).