---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_action_tween/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CCActionTween.h>`


| id |
|

[CCActionTween](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_action_tween/) is an action that lets you update any property of an object. For example, if you want to modify the "width" property of a target from 200 to 300 in 2 senconds, then:

id modifyWidth = [[CCActionTween](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_action_tween/) actionWithDuration:2 key:"width" from:200 to:300]; [target runAction:modifyWidth];

Another example: [CCScaleTo](http://www.learn-cocos2d.com/) action could be rewriten using CCPropertyAction:

scaleA and scaleB are equivalents id scaleA = [[CCScaleTo](http://www.learn-cocos2d.com/) actionWithDuration:2 scale:3]; id scaleB = [[CCActionTween](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_action_tween/) actionWithDuration:2 key:"scale" from:1 to:3];

| id CCActionTween::actionWithDuration:key:from:to: | ( |
|

` [static, virtual]`

creates an initializes the action with the property name (key), and the from and to parameters.

| id CCActionTween::initWithDuration:key:from:to: | ( |
|

` [virtual]`

initializes the action with the property name (key), and the from and to parameters.