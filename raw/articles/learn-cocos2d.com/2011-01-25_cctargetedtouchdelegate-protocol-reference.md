---
title: <CCTargetedTouchDelegate> Protocol Reference
url: http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/protocol_c_c_targeted_touch_delegate-p/
published: '2011-01-25'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#import "`

[CCTouchDelegateProtocol.h](http://www.learn-cocos2d.com/)"

Inherited by [CCLayer](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_layer/).

| (BOOL) | -
|

Using this type of delegate results in two benefits: 1. You don't need to deal with NSSets, the dispatcher does the job of splitting them. You get exactly one UITouch per call. 2. You can *claim* a UITouch by returning YES in ccTouchBegan. Updates of claimed touches are sent only to the delegate(s) that claimed them. So if you get a move/ ended/cancelled update you're sure it's your touch. This frees you from doing a lot of checks when doing multi-touch.

(The name TargetedTouchDelegate relates to updates "targeting" their specific handler, without bothering the other handlers.)

| - (BOOL) ccTouchBegan: | (UITouch *) | touch |
||
| withEvent: | (UIEvent *) | event | ||

Return YES to claim the touch.