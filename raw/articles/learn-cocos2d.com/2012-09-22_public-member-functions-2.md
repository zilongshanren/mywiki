---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.1/cocos2d-iphone/html/interface_c_c_layer/
published: '2012-09-22'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

|
cocos2d-iphone
1.1
Improved Cocos2D API Reference (iOS version) for www.kobold2d.com developers
|

`#import <CCLayer.h>`


| (void) | -
|

[CCLayer](http://www.learn-cocos2d.com/api-ref/1.1/cocos2d-iphone/html/interface_c_c_layer/) is a subclass of [CCNode](http://www.learn-cocos2d.com/api-ref/1.1/cocos2d-iphone/html/interface_c_c_node/) that implements the TouchEventsDelegate protocol.

All features from [CCNode](http://www.learn-cocos2d.com/api-ref/1.1/cocos2d-iphone/html/interface_c_c_node/) are valid, plus the following new features:

If isTouchEnabled, this method is called onEnter. Override it to change the way [CCLayer](http://www.learn-cocos2d.com/api-ref/1.1/cocos2d-iphone/html/interface_c_c_layer/) receives touch events. ( Default: [[TouchDispatcher sharedDispatcher] addStandardDelegate:self priority:0] ) Example: -(void) registerWithTouchDispatcher { [[TouchDispatcher sharedDispatcher] addTargetedDelegate:self priority:INT_MIN+1 swallowsTouches:YES]; }

Valid only on iOS. Not valid on Mac.

whether or not it will receive Accelerometer events You can enable / disable accelerometer events with this property.

Valid only on iOS. Not valid on Mac.

whether or not it will receive Touch events. You can enable / disable touch events with this property. Only the touches of this node will be affected. This "method" is not propagated to it's children.

Valid on iOS and Mac OS X v10.6 and later.