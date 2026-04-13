---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/protocol_c_c_touch_one_by_one_delegate-p/
published: '2013-02-23'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#import <CCTouchDelegateProtocol.h>`



[List of all members.](/)

Public Member Functions
|
| (BOOL) | - [ccTouchBegan:withEvent:](../../../../../api-ref/latest_2.x/cocos2d-iphone/html/protocol_c_c_touch_one_by_one_delegate-p/#a5f071f7f7a01efa156eaacfdd9b096d8) |
(void) | - **ccTouchMoved:withEvent:** |
(void) | - **ccTouchEnded:withEvent:** |
(void) | - **ccTouchCancelled:withEvent:** |


## Detailed Description

[CCTouchOneByOneDelegate](../../../../../api-ref/latest_2.x/cocos2d-iphone/html/protocol_c_c_touch_one_by_one_delegate-p/).

Using this type of delegate results in two benefits:

- You don't need to deal with NSSets, the dispatcher does the job of splitting them. You get exactly one UITouch per call.
- You can
*claim* a UITouch by returning YES in ccTouchBegan. Updates of claimed touches are sent only to the delegate(s) that claimed them. So if you get a move/ ended/cancelled update you're sure it is your touch. This frees you from doing a lot of checks when doing multi-touch.

(The name TargetedTouchDelegate relates to updates "targeting" their specific handler, without bothering the other handlers.)

- Since:
- v0.8


## Member Function Documentation

| - (BOOL) ccTouchBegan: |
|
(UITouch *) |
*touch* |
| withEvent: |
|
(UIEvent *) |
*event* |
|
|
| |

Return YES to claim the touch.

- Since:
- v0.8


The documentation for this protocol was generated from the following file:

- CCTouchDelegateProtocol.h