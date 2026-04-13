---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_clipping_node/
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

`#import <CCClippingNode.h>`


| (id) | -
|

[CCClippingNode](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_clipping_node/) is a subclass of [CCNode](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_node/). It draws its content (childs) clipped using a stencil. The stencil is an other [CCNode](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_node/) that will not be drawn. The clipping is done using the alpha part of the stencil (adjusted with an alphaThreshold).

Creates and initializes a clipping node with an other node as its stencil. The stencil node will be retained.

Initializes a clipping node with an other node as its stencil. The stencil node will be retained, and its parent will be set to this clipping node.

The alpha threshold. The content is drawn only where the stencil have pixel with alpha greater than the alphaThreshold. Should be a float between 0 and 1. This default to 1 (so alpha test is disabled).

Inverted. If this is set to YES, the stencil is inverted, so the content is drawn where the stencil is NOT drawn. This default to NO.