---
title: Instance Methods
url: http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.0/cocos2d-iphone/html/interface_c_c_action_tween/
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

`#import <CCActionTween.h>`


| (id) | -
|

| (id) | +
|

|

| Properties inherited from
|

CCActionTween

[CCActionTween](http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.0/cocos2d-iphone/html/interface_c_c_action_tween/) is an action that lets you update any property of an object. For example, if you want to modify the "width" property of a target from 200 to 300 in 2 seconds, then:

id modifyWidth = [[CCActionTween](http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.0/cocos2d-iphone/html/interface_c_c_action_tween/) actionWithDuration:2 key:"width" from:200 to:300]; [target runAction:modifyWidth];

Another example: [CCScaleTo](http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.0/cocos2d-iphone/html/interface_c_c_scale_to/) action could be rewriten using CCPropertyAction:

scaleA and scaleB are equivalents id scaleA = [[CCScaleTo](http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.0/cocos2d-iphone/html/interface_c_c_scale_to/) actionWithDuration:2 scale:3]; id scaleB = [[CCActionTween](http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.0/cocos2d-iphone/html/interface_c_c_action_tween/) actionWithDuration:2 key:"scale" from:1 to:3];

| + (id)
|

creates an initializes the action with the property name (key), and the from and to parameters.

initializes the action with the property name (key), and the from and to parameters.