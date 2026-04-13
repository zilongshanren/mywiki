---
title: CCLayer Class Reference
url: http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_layer/
published: '2011-01-25'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#import "`

[CCLayer.h](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/_c_c_layer_8h_source/)"

Inherits [CCNode](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_node/), [CCStandardTouchDelegate-p](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/protocol_c_c_standard_touch_delegate-p/), and [CCTargetedTouchDelegate-p](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/protocol_c_c_targeted_touch_delegate-p/).

Inherited by [CCLayerColor](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_layer_color/), [CCMenu](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_menu/), and [CCMultiplexLayer](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_multiplex_layer/).

| (void) | -
|

[CCLayer](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_layer/) is a subclass of [CCNode](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_node/) that implements the TouchEventsDelegate protocol.

All features from [CCNode](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_node/) are valid, plus the following new features:

| - (void) registerWithTouchDispatcher |

If isTouchEnabled, this method is called onEnter. Override it to change the way [CCLayer](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_layer/) receives touch events. ( Default: [[TouchDispatcher sharedDispatcher] addStandardDelegate:self priority:0] ) Example: -(void) registerWithTouchDispatcher { [[TouchDispatcher sharedDispatcher] addTargetedDelegate:self priority:INT_MIN+1 swallowsTouches:YES]; }

Valid only on iOS. Not valid on Mac.

- (BOOL) isAccelerometerEnabled` [read, write, assign]` |

whether or not it will receive Accelerometer events You can enable / disable accelerometer events with this property.

Valid only on iOS. Not valid on Mac.

- (BOOL) isTouchEnabled` [read, write, assign]` |

whether or not it will receive Touch events. You can enable / disable touch events with this property. Only the touches of this node will be affected. This "method" is not propagated to it's children.

Valid only on iOS. Not valid on Mac.