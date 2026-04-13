---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/2.0/cocos2d-iphone/html/interface_c_c_menu/
published: '2012-09-22'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#import <CCMenu.h>`




[List of all members.](/)


## Detailed Description

A [CCMenu](../../../../../api-ref/2.0/cocos2d-iphone/html/interface_c_c_menu/)

Features and Limitation:

- You can add MenuItem objects in runtime using addChild:
- But the only accecpted children are MenuItem objects


## Member Function Documentation

align items horizontally with padding

- Since:
- v0.7.2

align items in rows of columns

align items in columns of rows

align items vertically with padding

- Since:
- v0.7.2

| - (id) initWithItems: |
|
([CCMenuItem](/) *) |
*item* |
| vaList: |
|
(va_list) |
*args* |
|
|
| |

initializes a [CCMenu](../../../../../api-ref/2.0/cocos2d-iphone/html/interface_c_c_menu/) with its items

creates a [CCMenu](../../../../../api-ref/2.0/cocos2d-iphone/html/interface_c_c_menu/) with its items

set event handler priority. By default it is: kCCMenuTouchPriority


## Property Documentation

- (BOOL) [enabled](../../../../../api-ref/2.0/cocos2d-iphone/html/interface_c_c_menu/#a5cd5e32ca21936168d1dcc704ca1a82f)` [read, write, assign]` |

whether or not the menu will receive events


The documentation for this class was generated from the following file: