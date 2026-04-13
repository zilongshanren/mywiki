---
title: Instance Methods
url: http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.0/cocos2d-iphone/html/interface_c_c_layer/
published: '2013-01-09'
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

`#import <CCLayer.h>`


| (void) | -
|

|

| BOOL |
|

| Class Methods inherited from
|

[CCLayer](http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.0/cocos2d-iphone/html/interface_c_c_layer/) is a subclass of [CCNode](http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.0/cocos2d-iphone/html/interface_c_c_node/) that implements the CCTouchEventsDelegate protocol.

All features from [CCNode](http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.0/cocos2d-iphone/html/interface_c_c_node/) are valid, plus the following new features:

| - (void) setAccelerometerInterval: | (float) | interval |

sets the accelerometer's update frequency. A value of 1/2 means that the callback is going to be called twice per second.

|
readwritenonatomicassign |

whether or not it will receive Accelerometer events You can enable / disable accelerometer events with this property.

Valid only on iOS. Not valid on Mac.

|
readwritenonatomicassign |

whether or not it will receive Touch events

|
readwritenonatomicassign |

Touch modes.

|
readwritenonatomicassign |

priority of the touch events. Default is 0