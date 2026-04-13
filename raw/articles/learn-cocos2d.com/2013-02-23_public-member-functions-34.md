---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone/html/interface_c_c_node_r_g_b_a/
published: '2013-02-23'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

|
cocos2d-iphone
2.1
Improved Cocos2D API Reference (iOS version) for www.kobold2d.com developers
|

`#import <CCNode.h>`


|

[CCNodeRGBA](http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone/html/interface_c_c_node_r_g_b_a/) is a subclass of [CCNode](http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone/html/interface_c_c_node/) that implements the [CCRGBAProtocol](http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone/html/protocol_c_c_r_g_b_a_protocol-p/) protocol.

All features from [CCNode](http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone/html/interface_c_c_node/) are valid, plus the following new features:

Opacity/Color propagates into children that conform to the [CCRGBAProtocol](http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone/html/protocol_c_c_r_g_b_a_protocol-p/) if cascadeOpacity/cascadeColor is enabled.